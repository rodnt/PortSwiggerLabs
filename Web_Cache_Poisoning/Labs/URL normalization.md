


1. In Burp Repeater, browse to any non-existent path, such as `GET /random`. Notice that the path you requested is reflected in the error message.

![](/static/img/Pasted_image_20231118101647.png)

2. Add a suitable [reflected XSS](https://portswigger.net/web-security/cross-site-scripting/reflected) payload to the request line:
    
    `GET /random</p><script>alert(1)</script><p>foo`

![](/static/img/Pasted_image_20231118101725.png)

3. Notice that if you request this URL in the browser, the payload doesn't execute because it is URL-encoded.
4. Poison the request until you get the X-Cache: hit and send to the victim via the following link

![](/static/img/Pasted_image_20231118101934.png)


![](/static/img/Pasted_image_20231118101842.png)
> <alert(1) is wrong i known rsrs
![](/static/img/Pasted_image_20231118102054.png)