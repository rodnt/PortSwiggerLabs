1. Send the request to repeater and verify that, you can change the host header to any host, and the app make the request

![](/static/img/Pasted_image_20231119154120.png)


2. Generate the ips address using `prips` binary from linux or using burp intruder

![](/static/img/Pasted_image_20231119152630.png)

3. Don't forget to "unselect" the following check

![](/static/img/Pasted_image_20231119153010.png)

4. Order by status and verify the path

![](/static/img/Pasted_image_20231119154253.png)


4. You need to setup the following headers at you request ( don't forget the `application/x-www-form-urlencoded`)

![](/static/img/Pasted_image_20231119154401.png)

![](/static/img/Pasted_image_20231119154549.png)
![](/static/img/Pasted_image_20231119154627.png)