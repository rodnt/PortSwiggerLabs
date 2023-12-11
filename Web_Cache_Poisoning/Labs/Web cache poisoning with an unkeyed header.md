
1. Verify that if you add any cache key with the header `X-Forwarded-Host` the URL will be replaced. But the cache is `miss`

![](/static/img/Pasted_image_20231115175403.png)

2. Repeat the request until you get the `hit` value

![](/static/img/Pasted_image_20231115175447.png)
3. Go to the exploit server and copy the URL from your lab, and repeat this process, but you need to serve your malicious script;

![](/static/img/Pasted_image_20231115175551.png)

4. Remove the cache key, but keep the exploit server url, and repeat the process until you get the hit.

![](/static/img/Pasted_image_20231115175705.png)

5. Access with your browser.

![](/static/img/Pasted_image_20231115175204.png)