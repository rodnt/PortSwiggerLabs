


1. Using dom invader, scan for possible sinks;
2. After scan for gadgets;
3. Click Exploit;

![](/static/img/Pasted_image_20231202093702.png)


![](/static/img/Pasted_image_20231202093558.png)

##### Manual approach


1. Inject the following payload at URL
`/?__proto__[foo]=bar`
2. Verify at the browser console that you can inject the Object;

- Identify the gadget

**Identify a gadget**

1. In the browser DevTools panel, go to the **Sources** tab.
    
2. Study the JavaScript files that are loaded by the target site and look for any DOM [XSS](https://portswigger.net/web-security/cross-site-scripting) sinks.
    
3. In `searchLoggerConfigurable.js`, notice that if the `config` object has a `transport_url` property, this is used to dynamically append a script to the DOM.
    
4. Observe that a `transport_url` property is defined for the `config` object, so this doesn't appear to be vulnerable.
    
5. Observe that the next line uses the `Object.defineProperty()` method to make the `transport_url` unwritable and unconfigurable. However, notice that it doesn't define a `value` property.
    

**Craft an exploit**

1. Using the prototype pollution source you identified earlier, try injecting an arbitrary value property:
    
    `/?__proto__[value]=foo`
2. In the browser DevTools panel, go to the **Elements** tab and study the HTML content of the page. Observe that a `<script>` element has been rendered on the page, with the `src` attribute `foo`.
    
3. Modify the payload in the URL to inject an XSS proof-of-concept. For example, you can use a `data:` URL as follows:
    
    `/?__proto__[value]=data:,alert(1);`
4. Observe that the `alert(1)` is called and the lab is solved.