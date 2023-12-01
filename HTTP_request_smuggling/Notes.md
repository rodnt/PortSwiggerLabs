
- What is
	- HTTP request smuggling is a technique for interfering with the way a web site processes sequences of HTTP requests that are received from one or more users.

> Request smuggling vulnerabilities are often critical in nature, allowing an attacker to bypass security controls, gain unauthorized access to sensitive data, and directly compromise other application users.

Request smuggling is primarily **associated with HTTP/1 requests**. However, websites that support **HTTP/2 may be vulnerable**, depending on their back-end architecture.


When the **front-end** server forwards HTTP requests to a **back-end server**, it typically sends several requests over the same back-end network connection, because this is much more efficient and performant. The protocol is very simple; HTTP requests are sent one after another, and the receiving server has to determine where one request ends and the next one begins


## How do HTTP request smuggling vulnerabilities arise?

> HTTP/1 specification provides two different ways to specify where a request ends: the **Content-Length** header and the **Transfer-Encoding header**.



The `Content-Length` header is straightforward: it specifies the length of the message body in bytes. For example:

`POST /search HTTP/1.1 Host: normal-website.com Content-Type: application/x-www-form-urlencoded Content-Length: 11 q=smuggling`


The `Transfer-Encoding` header can be used to specify that the message body uses chunked encoding. This means that the message body contains one or more chunks of data. Each chunk consists of the chunk size in bytes (expressed in hexadecimal), followed by a newline, followed by the chunk contents. The message is terminated with a chunk of size zero. For example:

`POST /search HTTP/1.1 Host: normal-website.com Content-Type: application/x-www-form-urlencoded Transfer-Encoding: chunked b q=smuggling 0`


> As the HTTP/1 specification provides **two different methods for specifying the length of HTTP messages, it is possible for a single message to use both methods at once**, such that they conflict with each other

> The specification attempts to prevent this problem by stating that if both the `Content-Length` and `Transfer-Encoding` headers are present, then the `Content-Length` header **should be ignored.**

- Some servers do not support the `Transfer-Encoding` header in requests.
- Some servers that do support the `Transfer-Encoding` header can be induced not to process it if the header is obfuscated in some way.

> Websites that use HTTP/2 end-to-end are inherently immune to request smuggling attacks. As the HTTP/2 specification introduces a single, robust mechanism for specifying the length of a request, there is no way for an attacker to introduce the required ambiguity.

- HTTP Downgrade
	- However, many websites have an HTTP/2-speaking front-end server, but deploy this in front of back-end infrastructure that only supports HTTP/1. This means that the front-end effectively has to translate the requests it receives into HTTP/1. This process is known as HTTP downgrading. For more information, see [Advanced request smuggling](https://portswigger.net/web-security/request-smuggling/advanced).




## How to perform an HTTP request smuggling attack

- Classic approach
	- Classic request smuggling attacks involve placing both the `Content-Length` header and the `Transfer-Encoding` header into a single HTTP/1 request and manipulating these so that the front-end and back-end servers process the request differently.

The exact way in which this is done depends on the behavior of the two servers:

- CL.TE: the front-end server uses the `Content-Length` header and the back-end server uses the `Transfer-Encoding` header.
- TE.CL: the front-end server uses the `Transfer-Encoding` header and the back-end server uses the `Content-Length` header.
- TE.TE: the front-end and back-end servers both support the `Transfer-Encoding` header, but one of the servers can be induced not to process it by obfuscating the header in some way.

> These techniques are only possible using HTTP/1 requests. Browsers and other clients, including Burp, use HTTP/2 by default to communicate with servers that explicitly advertise support for it during the TLS handshake.
As a result, when testing sites with HTTP/2 support, you need to manually switch protocols in Burp Repeater. You can do this from the Request attributes section of the Inspector panel.


### CL.TE vulnerabilities

Here, the front-end server uses the `Content-Length` header and the back-end server uses the `Transfer-Encoding` header. We can perform a simple HTTP request smuggling attack as follows:

```http
POST / HTTP/1.1 
Host: vulnerable-website.com 
Content-Length: 13 
Transfer-Encoding: chunked 
\r
\n
0 
\r
\n
SMUGGLED
```

1. **POST / HTTP/1.1**: This line indicates that the request is a POST request to the root directory of the HTTP server.
2. **Host: vulnerable-website.com**: This header specifies the host to which the request is being sent.
3. **Content-Length: 13**: This header indicates that the length of the body of the request is 13 bytes. However, this is part of the deceptive nature of the attack.
4. **Transfer-Encoding: chunked**: This header indicates that the body of the request uses 'chunked' transfer encoding, a method where the data is sent in a series of chunks.
5. **0\\r\\n\\r\\n**: This part of the request indicates the end of the chunks for the 'chunked' transfer encoding.
6. **SMUGGLED**: This is the smuggled request or payload.

In a normal scenario, the `Content-Length` and `Transfer-Encoding` headers should not be used together, as they are two different ways of specifying the request body length. However, in this attack, the presence of both headers can confuse the server or intermediary proxies.

- Some servers might give precedence to `Content-Length` and expect a body of 13 bytes.
- Others might use `Transfer-Encoding: chunked` and consider the message body to end after `0\r\n\r\n`, ignoring the `SMUGGLED` part.

This discrepancy allows attackers to 'smuggle' a request (in this case, `SMUGGLED`) to one server in the chain without the other server recognizing it. This can lead to various security issues, such as bypassing security controls, poisoning web caches, and conducting cross-site scripting attacks.

The `13` in `Content-Length: 13` doesn't accurately reflect the actual length of the body in a straightforward sense, but rather is part of the exploitation technique. The actual content that the attacker wants the server to process is the `SMUGGLED` part.


### TE.CL vulnerabilities

Here, the front-end server uses the `Transfer-Encoding` header and the back-end server uses the `Content-Length` header. We can perform a simple HTTP request smuggling attack as follows:

`POST / HTTP/1.1 Host: vulnerable-website.com Content-Length: 3 Transfer-Encoding: chunked 8 SMUGGLED 0`

#### Note

To send this request using Burp Repeater, you will first need to go to the Repeater menu and ensure that the "Update Content-Length" option is unchecked.

You need to include the trailing sequence `\r\n\r\n` following the final `0`.

The front-end server processes the `Transfer-Encoding` header, and so treats the message body as using chunked encoding. It processes the first chunk, which is stated to be 8 bytes long, up to the start of the line following `SMUGGLED`. It processes the second chunk, which is stated to be zero length, and so is treated as terminating the request. This request is forwarded on to the back-end server.

The back-end server processes the `Content-Length` header and determines that the request body is 3 bytes long, up to the start of the line following `8`. The following bytes, starting with `SMUGGLED`, are left unprocessed, and the back-end server will treat these as being the start of the next request in the sequence.


### TE.TE behavior: obfuscating the TE header

Here, the front-end and back-end servers both support the `Transfer-Encoding` header, but one of the servers can be induced not to process it by obfuscating the header in some way.

There are potentially endless ways to obfuscate the `Transfer-Encoding` header. For example:

`Transfer-Encoding: xchunked Transfer-Encoding : chunked Transfer-Encoding: chunked Transfer-Encoding: x Transfer-Encoding:[tab]chunked [space]Transfer-Encoding: chunked X: X[\n]Transfer-Encoding: chunked Transfer-Encoding : chunked`

Each of these techniques involves a subtle departure from the HTTP specification. Real-world code that implements a protocol specification rarely adheres to it with absolute precision, and it is common for different implementations to tolerate different variations from the specification. To uncover a TE.TE vulnerability, it is necessary to find some variation of the `Transfer-Encoding` header such that only one of the front-end or back-end servers processes it, while the other server ignores it.

Depending on whether it is the front-end or the back-end server that can be induced not to process the obfuscated `Transfer-Encoding` header, the remainder of the attack will take the same form as for the CL.TE or TE.CL vulnerabilities already described.


## Finding HTTP request smuggling vulnerabilities using timing techniques

The most generally effective way to detect HTTP request smuggling vulnerabilities is to send requests that will cause a time delay in the application's responses if a vulnerability is present. This technique is used by [Burp Scanner](https://portswigger.net/burp/vulnerability-scanner) to automate the detection of request smuggling vulnerabilities.

### Finding CL.TE vulnerabilities using timing techniques

If an application is vulnerable to the CL.TE variant of request smuggling, then sending a request like the following will often cause a time delay:

```http
POST / HTTP/1.1 
Host: vulnerable-website.com 
Transfer-Encoding: chunked 
Content-Length: 4

1 
A 
X
```

Since the front-end server uses the `Content-Length` header, it will forward only part of this request, omitting the `X`. The back-end server uses the `Transfer-Encoding` header, processes the first chunk, and then waits for the next chunk to arrive. This will cause an observable time delay.

### Finding TE.CL vulnerabilities using timing techniques

If an application is vulnerable to the TE.CL variant of request smuggling, then sending a request like the following will often cause a time delay:

```http
POST / HTTP/1.1 
Host: vulnerable-website.com 
Transfer-Encoding: chunked 
Content-Length: 6

0

X
```

Since the front-end server uses the `Transfer-Encoding` header, it will forward only part of this request, omitting the `X`. The back-end server uses the `Content-Length` header, expects more content in the message body, and waits for the remaining content to arrive. This will cause an observable time delay.

#### Note

The timing-based test for TE.CL vulnerabilities will potentially disrupt other application users if the application is vulnerable to the CL.TE variant of the vulnerability. So to be stealthy and minimize disruption, you should use the CL.TE test first and continue to the TE.CL test only if the first test is unsuccessful.


## Confirming HTTP request smuggling vulnerabilities using differential responses

When a probable request smuggling vulnerability has been detected, you can obtain further evidence for the vulnerability by exploiting it to trigger differences in the contents of the application's responses. This involves sending two requests to the application in quick succession:

- An "attack" request that is designed to interfere with the processing of the next request.
- A "normal" request.

If the response to the normal request contains the expected interference, then the vulnerability is confirmed.

For example, suppose the normal request looks like this:

```http
POST /search HTTP/1.1 
Host: vulnerable-website.com 
Content-Type: application/x-www-form-urlencoded 
Content-Length: 11 

q=smuggling
```

This request normally receives an HTTP response with status code 200, containing some search results.

The attack request that is needed to interfere with this request depends on the variant of request smuggling that is present: CL.TE vs TE.CL.

### Confirming CL.TE vulnerabilities using differential responses

To confirm a CL.TE vulnerability, you would send an attack request like this:

```http
POST /search HTTP/1.1 
Host: vulnerable-website.com 
Content-Type: application/x-www-form-urlencoded 
Content-Length: 49 
Transfer-Encoding: chunked e 
q=smuggling&x= 0 GET /404 HTTP/1.1 
Foo: x
```

If the attack is successful, then the last two lines of this request are treated by the back-end server as belonging to the next request that is received. This will cause the subsequent "normal" request to look like this:

```http
GET /404 HTTP/1.1 
Foo: xPOST /search HTTP/1.1 
Host: vulnerable-website.com 
Content-Type: application/x-www-form-urlencoded 
Content-Length: 11 
q=smuggling
```

Since this request now contains an invalid URL, the server will respond with status code 404, indicating that the attack request did indeed interfere with it.


### Confirming TE.CL vulnerabilities using differential responses

To confirm a TE.CL vulnerability, you would send an attack request like this:

`POST /search HTTP/1.1 Host: vulnerable-website.com Content-Type: application/x-www-form-urlencoded Content-Length: 4 Transfer-Encoding: chunked 7c GET /404 HTTP/1.1 Host: vulnerable-website.com Content-Type: application/x-www-form-urlencoded Content-Length: 144 x= 0`

#### Note

To send this request using Burp Repeater, you will first need to go to the Repeater menu and ensure that the "Update Content-Length" option is unchecked.

You need to include the trailing sequence `\r\n\r\n` following the final `0`.

If the attack is successful, then everything from `GET /404` onwards is treated by the back-end server as belonging to the next request that is received. This will cause the subsequent "normal" request to look like this:

`GET /404 HTTP/1.1 Host: vulnerable-website.com Content-Type: application/x-www-form-urlencoded Content-Length: 146 x= 0 POST /search HTTP/1.1 Host: vulnerable-website.com Content-Type: application/x-www-form-urlencoded Content-Length: 11 q=smuggling`

Since this request now contains an invalid URL, the server will respond with status code 404, indicating that the attack request did indeed interfere with it.

>Some important considerations should be kept in mind when attempting to confirm request smuggling vulnerabilities via interference with other requests:

- The "attack" request and the "normal" request should be sent to the server using **different network connections**. Sending both requests through the same connection won't prove that the vulnerability exists.
- The "attack" request and the "normal" request should use the same URL and parameter names, as far as possible. This is because many modern applications route front-end requests to different back-end servers based on the URL and parameters. Using the same URL and parameters increases the chance that the requests will be processed by the same back-end server, which is essential for the attack to work.
- When testing the "normal" request to detect any interference from the "attack" request, you are in a race with any other requests that the application is receiving at the same time, including those from other users. You should send the "normal" request immediately after the "attack" request. If the application is busy, you might need to perform multiple attempts to confirm the vulnerability.
- In some applications, the front-end server functions as a load balancer, and forwards requests to different back-end systems according to some load balancing algorithm. If your "attack" and "normal" requests are forwarded to different back-end systems, then the attack will fail. This is an additional reason why you might need to try several times before a vulnerability can be confirmed.
- If your attack succeeds in interfering with a subsequent request, but this wasn't the "normal" request that you sent to detect the interference, then this means that another application user was affected by your attack. If you continue performing the test, this could have a disruptive effect on other users, and you should exercise caution.

# Exploiting HTTP request smuggling vulnerabilities

In some applications, the front-end web server is used to implement some security controls, deciding whether to allow individual requests to be processed. Allowed requests are forwarded to the back-end server, where they are deemed to have passed through the front-end controls.

For example, suppose an application uses the front-end server to implement [access control](https://portswigger.net/web-security/access-control) restrictions, only forwarding requests if the user is authorized to access the requested URL. The back-end server then honors every request without further checking. In this situation, an HTTP request smuggling vulnerability can be used to bypass the [access controls](https://portswigger.net/web-security/access-control), by smuggling a request to a restricted URL.

Suppose the current user is permitted to access `/home` but not `/admin`. They can bypass this restriction using the following request smuggling attack:


```http

POST /home HTTP/1.1 
Host: vulnerable-website.com 
Content-Type: application/x-www-form-urlencoded 
Content-Length: 62 
Transfer-Encoding: chunked 

0 
GET /admin HTTP/1.1 
Host: vulnerable-website.com 
Foo: xGET /home HTTP/1.1 
Host: vulnerable-website.com

```

