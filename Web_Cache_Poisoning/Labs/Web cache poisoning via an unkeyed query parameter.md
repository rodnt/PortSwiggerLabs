
1. Add a random cache-buster query param and notice that you can reflect;
2. Notice that utm_content, is supported by the application;
3. Send a request with a `utm_content` parameter that breaks out of the reflected string and injects an [XSS](https://portswigger.net/web-security/cross-site-scripting) payload:
    
    `GET /?utm_content='/><script>alert(1)</script>`

![](/static/img/Pasted_image_20231117123406.png)

4. After request more than 50 times.. you can achieve the cache hit

![](/static/img/Pasted_image_20231117124240.png)



![](/static/img/Pasted_image_20231117124328.png)