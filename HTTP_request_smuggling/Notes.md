
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