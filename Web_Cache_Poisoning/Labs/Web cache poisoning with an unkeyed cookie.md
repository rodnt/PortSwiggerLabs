

1. Verify that when you access the site for the first time, the web site sends to you a cookie called `fehost`
![](/static/img/Pasted_image_20231115180653.png)

2. Using a cache key, verify that if you change the value of the cookie `fehost` you can "inject" content inside the javascript.

![](/static/img/Pasted_image_20231115181709.png)

3. Insert the following payload at `fehost` cookie
`fehost=prod-cache-01"-alert(1)-"rodnt`

4. Remove the cache key and send the request until you get the hit at the response.

![](/static/img/Pasted_image_20231115181842.png)

5. Refresh the main page until you solve the lab

![](/static/img/Pasted_image_20231115181922.png)


