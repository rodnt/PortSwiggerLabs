

1. Login and change the email account. Verify that `csrf` cookie and parameter are equal;
![](/static/img/Pasted_image_20231107174651.png)
2. Note that, the CSRF tokens are compared with each one;

![](/static/img/Pasted_image_20231107174923.png)
3. The search parameter is vulnerable to CRLF Injection
![](/static/img/Pasted_image_20231107175155.png)
4. Save the following exploit into the exploit server and deliver to victim;
![](/static/img/Pasted_image_20231107175555.png)
![](/static/img/Pasted_image_20231107175619.png)

