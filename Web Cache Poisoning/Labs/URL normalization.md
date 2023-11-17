


1. In Burp Repeater, browse to any non-existent path, such as `GET /random`. Notice that the path you requested is reflected in the error message.
2. Add a suitable [reflected XSS](https://portswigger.net/web-security/cross-site-scripting/reflected) payload to the request line:
    
    `GET /random</p><script>alert(1)</script><p>foo`
3. Notice that if you request this URL in the browser, the payload doesn't execute because it is URL-encoded.