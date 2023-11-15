

## What is web cache poisoning?

- Attacker exploits the behavior of a web server and cache so that a harmful HTTP response is served to other users;
- Attack made by two phases
	- First, the attacker must work out how to elicit a response from the back-end server that inadvertently contains some kind of dangerous payload;
	- Second, once successful the first step, they need to make sure that their response is cached and subsequently served to the intended victims;
-  The impact cold be, such as [XSS](https://portswigger.net/web-security/cross-site-scripting), JavaScript injection, open redirection, and so on.
- 2018 research paper, "Practical Web Cache Poisoning" - https://portswigger.net/research/practical-web-cache-poisoning
- 2020 with a second research paper, "Web Cache Entanglement: Novel Pathways to Poisoning". - https://portswigger.net/research/web-cache-entanglement

- If a server had to send a new response to every single HTTP request separately, this would likely overload the server, resulting in latency issues and a poor user experience, especially during busy periods. Caching is primarily a means of reducing such issues. The cache sits between the server and the user, where it saves (caches) the responses to particular requests, usually for a fixed amount of time. If another user then sends an equivalent request, the cache simply serves a copy of the cached response directly to the user, without any interaction from the back-end. This greatly eases the load on the server by reducing the number of duplicate requests it has to handle.

- Cache Keys
	- When the cache receives an HTTP request, it first has to determine whether there is a cached response;
	- Caches identify equivalent requests by comparing a predefined subset of the request's components, known collectively as the "cache key";
	- Typically, this would contain the request line and `Host` header;
	- 🚨 If the cache key of an incoming request matches the key of a previous request, then the cache considers them to be equivalent;


### Constructing a web cache poisoning attack ( 3 steps )


> You can use the following extension from burp ( Param Miner )
> You can automate the process of identifying unkeyed inputs by adding the [Param Miner](https://portswigger.net/bappstore/17d2949a985c4b7ca092728dba871943) extension to Burp from the BApp store. To use Param Miner, you simply right-click on a request that you want to investigate and click "Guess headers". Param Miner then runs in the background, sending requests containing different inputs from its extensive, built-in list of headers. If a request containing one of its injected inputs has an effect on the response

1. Identify and evaluate unkeyed inputs
	1. You can identify **unkeyed** inputs manually by adding **random inputs** to requests and observing whether or not they have an **effect on the response**;

**Caution:** When testing for unkeyed inputs on a live website, there is a risk of inadvertently causing the cache to serve your generated responses to real users. **Therefore, it is important to make sure that your requests all have a unique cache key** so that they will only be served to you. To do this, y**ou can manually add a cache buster** (such as a unique parameter) to the request line each time you make a request. Alternatively, if you are using Param Miner, there are options for automatically adding a cache buster to every request.

#### Elicit a harmful response from the back-end server

> Once you have identified an unkeyed input, the next step is to evaluate exactly how the website processes it. **Understanding this is essential to successfully eliciting a harmful response.** If an input is reflected in the response from the server without being properly sanitized, or is used to dynamically generate other data, then this is a potential entry point for web cache poisoning.


### Get the response cached

- Manipulating inputs to elicit a harmful response is half the battle, but it doesn't achieve much unless you can cause the response to be cached, which can sometimes be tricky. Whether or not a response gets cached can depend on all kinds of factors, such as the file extension, content type, route, status code, and response headers.


---

### Exploiting cache design flaws

- Websites are vulnerable to web cache poisoning if they handle unkeyed input in an unsafe way and allow the subsequent HTTP responses to be cached.

##### Using web cache poisoning to deliver an XSS attack

1. When unkeyed input is reflected in a cacheable response without proper sanitization.

For example, consider the following request and response:

```http
GET /en?region=uk HTTP/1.1 
Host: innocent-website.com 
X-Forwarded-Host: innocent-website.co.uk 

HTTP/1.1 200 OK Cache-Control: public 
<meta property="og:image" content="https://innocent-website.co.uk/cms/social.png" />`
```

Here, the value of the `X-Forwarded-Host` header is being used to dynamically generate an Open Graph image URL, which is then reflected in the response. Crucially for web cache poisoning, the `X-Forwarded-Host` header is often unkeyed. In this example, the cache can potentially be poisoned with a response containing a simple [XSS](https://portswigger.net/web-security/cross-site-scripting) payload:

```http
GET /en?region=uk HTTP/1.1 
Host: innocent-website.com 
X-Forwarded-Host: a."><script>alert(1)</script>" 
HTTP/1.1 200 OK Cache-Control: public 
<meta property="og:image" content="https://a."><script>alert(1)</script>"/cms/social.png" />
```

If this response was cached, all users who accessed `/en?region=uk` would be served this XSS payload. This example simply causes an alert to appear in the victim's browser, but a real attack could potentially steal passwords and hijack user accounts.

#### Using web cache poisoning to exploit unsafe handling of resource imports

1. Some websites use **unkeyed** headers to dynamically generate URLs for importing resources, such as externally hosted JavaScript files. In this case, if an attacker changes the value of the appropriate header to a domain that they control, they could potentially manipulate the URL to point to their own malicious JavaScript file instead.
2. If the response containing this malicious URL is cached, the attacker's JavaScript file would be imported and executed in the browser session of any user whose request has a matching cache key.

```http
GET / HTTP/1.1 Host: innocent-website.com 
X-Forwarded-Host: evil-user.net 
User-Agent: Mozilla/5.0 Firefox/57.0 HTTP/1.1 200 OK 
<script src="https://evil-user.net/static/analytics.js"></script>
```

#### Using web cache poisoning to exploit cookie-handling vulnerabilities

A common example might be a cookie that indicates the user's preferred language, which is then used to load the corresponding version of the page:

```http
GET /blog/post.php?mobile=1 HTTP/1.1 Host: innocent-website.com 
User-Agent: Mozilla/5.0 Firefox/57.0 
Cookie: language=pl; Connection: close
```

In this example, the Polish version of a blog post is being requested. Notice that the information about which language version to serve is only contained in the `Cookie` header. Let's suppose that the cache key contains the request line and the `Host` header, but not the `Cookie` header. In this case, if the response to this request is cached, then all subsequent users who tried to access this blog post would receive the Polish version as well, regardless of which language they actually selected.

This flawed handling of cookies by the cache can also be exploited using web cache poisoning techniques. In practice, however, this vector is relatively rare in comparison to header-based cache poisoning. When cookie-based cache poisoning vulnerabilities exist, they tend to be identified and resolved quickly because legitimate users have accidentally poisoned the cache.

#### Using multiple headers to exploit web cache poisoning vulnerabilities

> Some websites are vulnerable to simple web cache poisoning exploits, as demonstrated above. However, others require more sophisticated attacks and only become vulnerable when an **attacker is able to craft a request that manipulates multiple unkeyed inputs**.


For example, let's say a website requires secure communication using HTTPS. To enforce this, if a request that uses another protocol is received, the website dynamically generates a redirect to itself that does use HTTPS:

```http
GET /random HTTP/1.1 
Host: innocent-site.com X-Forwarded-Proto: http 
HTTP/1.1 301 moved permanently 
Location: https://innocent-site.com/random
```

By itself, this behavior isn't necessarily vulnerable. However, by combining this with what we learned earlier about vulnerabilities in dynamically generated URLs, an attacker could potentially exploit this behavior to generate a cacheable response that redirects users to a malicious URL.

##### Exploiting responses that expose too much information

