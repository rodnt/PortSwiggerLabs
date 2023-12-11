
1. Observe that the login page references an endpoint at `/js/localize.js` that is vulnerable to response header injection via the `Origin` request header, provided the `[cors](https://portswigger.net/web-security/cors)` parameter is set to `1`.

![](/static/img/Pasted_image_20231118103255.png)

2. Use the `Pragma: x-get-cache-key` header to identify that the server is vulnerable to cache key injection, meaning the header injection can be triggered via a crafted URL.

![](/static/img/Pasted_image_20231118103401.png)

3. Combine the following requests, send both to repeater and cache both

![](/static/img/Pasted_image_20231118103451.png)

![](/static/img/Pasted_image_20231118103459.png)


![](/static/img/Pasted_image_20231118102953.png)