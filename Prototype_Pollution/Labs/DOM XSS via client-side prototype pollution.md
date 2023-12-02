

1. Load the DOM invader extension;
![](/static/img/Pasted_image_20231202082731.png)

2. Search for possible sinks;

![](/static/img/Pasted_image_20231202082826.png)
3. Scan for targets;
4. Scan finish;

![](/static/img/Pasted_image_20231202082924.png)


![](/static/img/Pasted_image_20231202082700.png)

#### Manual approach

1. Inject the property at URL;

![](/static/img/Pasted_image_20231202083127.png)

2. Verify that everything load correctly; 
3. Next step is identify the `gadget`;
4. Study the javascript at `sources` inside the browser;

![](/static/img/Pasted_image_20231202083407.png)

5. Notice that no `transport_url` property is defined for the `config` object. This is a potential gadget for controlling the `src` of the `<script>` element.
6. Create the exploit;
	1. Using the prototype pollution source you identified earlier, try injecting an arbitrary `transport_url` property:
    
    `/?__proto__[transport_url]=foo`
	1. In the browser DevTools panel, go to the **Elements** tab and study the HTML content of the page. Observe that a `<script>` element has been rendered on the page, with the `src` attribute `foo`.
    
	2. Modify the payload in the URL to inject an XSS proof-of-concept. For example, you can use a `data:` URL as follows:

	    `/?__proto__[transport_url]=data:,alert(1);`
	1. Observe that the `alert(1)` is called and the lab is solved.