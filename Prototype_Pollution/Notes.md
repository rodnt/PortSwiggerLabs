
- Prototype pollution is a JavaScript vulnerability that enables an attacker to add arbitrary properties to global object prototypes.

- Prototype pollution vulnerabilities typically arise when a JavaScript function recursively merges an object containing user-controllable properties into an existing object, without first sanitizing the keys.
	- This can allow an attacker to inject a property with a key like `__proto__`, along with arbitrary nested properties.
	- It's possible to pollute any prototype object, but this most commonly occurs with the [built-in global `Object.prototype`](https://portswigger.net/web-security/prototype-pollution/javascript-prototypes-and-inheritance#the-prototype-chain).
- Successful exploitation of prototype pollution requires the following key components:
	- [A prototype pollution source](https://portswigger.net/web-security/prototype-pollution#prototype-pollution-sources) - This is any input that enables you to poison prototype objects with arbitrary properties.
	- [A sink](https://portswigger.net/web-security/prototype-pollution#prototype-pollution-sinks) - In other words, a JavaScript function or DOM element that enables arbitrary code execution.
	- [An exploitable gadget](https://portswigger.net/web-security/prototype-pollution#prototype-pollution-gadgets) - This is any property that is passed into a sink without proper filtering or sanitization.

- **As prototype pollution lets you control properties that would otherwise be inaccessible**, this potentially enables you to reach a number of additional sinks within the target application. Developers who are unfamiliar with prototype pollution may wrongly assume that these properties are not user controllable, which means there may only be minimal filtering or sanitization in place.

> Although prototype pollution is often unexploitable as a standalone vulnerability, it lets an attacker control properties of objects that would otherwise be inaccessible. If the application subsequently handles an attacker-controlled property in an unsafe way, this can potentially be chained with other vulnerabilities. In client-side JavaScript, this commonly leads to [DOM XSS](https://portswigger.net/web-security/cross-site-scripting/dom-based), while server-side prototype pollution can even result in remote code execution.


## Prototype pollution sources

A prototype pollution source is any user-controllable input that enables you to add arbitrary properties to prototype objects. The most common sources are as follows:
- The [URL](https://portswigger.net/web-security/prototype-pollution#prototype-pollution-via-the-url) via either the query or fragment string (hash)
- [JSON-based input](https://portswigger.net/web-security/prototype-pollution#prototype-pollution-via-json-input) 
- Web messages

## Finding client-side prototype pollution sources manually

- Finding [prototype pollution sources](https://portswigger.net/web-security/prototype-pollution#prototype-pollution-sources) manually is largely a case of trial and error. In short, you need to try different ways of adding an arbitrary property to `Object.prototype` until you find a source that works.

When testing for client-side vulnerabilities, this involves the following high-level steps:

1. Try to inject an arbitrary property via the query string, URL fragment, and any JSON input. For example:
    
    `vulnerable-website.com/?__proto__[foo]=bar`
2. In your browser console, inspect `Object.prototype` to see if you have successfully polluted it with your arbitrary property:
    
    `Object.prototype.foo // "bar" indicates that you have successfully polluted the prototype // undefined indicates that the attack was not successful`
3. If the property was not added to the prototype, try using different techniques, such as switching to dot notation rather than bracket notation, or vice versa:
    
    `vulnerable-website.com/?__proto__.foo=bar`
4. Repeat this process for each potential source.

#### Other methods to source manually

-  Prototype pollution via the constructor

- So far, we've looked exclusively at how you can get a reference to prototype objects via the special `__proto__` accessor property. As this is the classic technique for prototype pollution, a common defense is to strip any properties with the key `__proto__` from user-controlled objects before merging them. This approach is flawed as there are alternative ways to reference `Object.prototype` without relying on the `__proto__` string at all.

- Unless its [prototype is set to `null`](https://portswigger.net/web-security/prototype-pollution/preventing#preventing-an-object-from-inheriting-properties), every JavaScript object has a `constructor` property, which contains a reference to the constructor function that was used to create it. For example, you can create a new object either using literal syntax or by explicitly invoking the `Object()` constructor as follows:

`let myObjectLiteral = {}; let myObject = new Object();`

- You can then reference the `Object()` constructor via the built-in `constructor` property:

`myObjectLiteral.constructor // function Object(){...} myObject.constructor // function Object(){...}`

- Remember that functions are also just objects under the hood. Each constructor function has a `prototype` property, which points to the prototype that will be assigned to any objects that are created by this constructor. As a result, you can also access any object's prototype as follows:

`myObject.constructor.prototype // Object.prototype myString.constructor.prototype // String.prototype myArray.constructor.prototype // Array.prototype`

- As `myObject.constructor.prototype` is equivalent to `myObject.__proto__`, this provides an alternative vector for prototype pollution.

## Finding client-side prototype pollution gadgets manually

Once you've [identified a source](https://portswigger.net/web-security/prototype-pollution/client-side#finding-client-side-prototype-pollution-sources-manually) that lets you add arbitrary properties to the global `Object.prototype`, the next step is to find a suitable gadget that you can use to craft an exploit. In practice, we recommend [using DOM Invader](https://portswigger.net/web-security/prototype-pollution/client-side#finding-client-side-prototype-pollution-gadgets-using-dom-invader) to do this, but it's useful to look at the manual process as it may help solidify your understanding of the vulnerability.

1. Look through the source code and identify any properties that are used by the application or any libraries that it imports.
    
2. In Burp, enable response interception (**Proxy > Options > Intercept server responses**) and intercept the response containing the JavaScript that you want to test.
    
3. Add a `debugger` statement at the start of the script, then forward any remaining requests and responses.
    
4. In Burp's browser, go to the page on which the target script is loaded. The `debugger` statement pauses execution of the script.
    
5. While the script is still paused, switch to the console and enter the following command, replacing `YOUR-PROPERTY` with one of the properties that you think is a potential gadget:
    
    `Object.defineProperty(Object.prototype, 'YOUR-PROPERTY', { get() { console.trace(); return 'polluted'; } })`
    
    The property is added to the global `Object.prototype`, and the browser will log a stack trace to the console whenever it is accessed.
    
6. Press the button to continue execution of the script and monitor the console. If a stack trace appears, this confirms that the property was accessed somewhere within the application.
    
7. Expand the stack trace and use the provided link to jump to the line of code where the property is being read.
    
8. Using the browser's debugger controls, step through each phase of execution to see if the property is passed to a sink, such as `innerHTML` or `eval()`.
    
9. Repeat this process for any properties that you think are potential gadgets.

## Bypassing flawed key sanitization

An obvious way in which websites attempt to prevent prototype pollution is by sanitizing property keys before merging them into an existing object. However, a common mistake is failing to recursively sanitize the input string. For example, consider the following URL:

`vulnerable-website.com/?__pro__proto__to__.gadget=payload`

If the sanitization process just strips the string `__proto__` without repeating this process more than once, this would result in the following URL, which is a potentially valid prototype pollution source:

`vulnerable-website.com/?__proto__.gadget=payload`


