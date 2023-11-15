----

DOM-based XSS (also known as [DOM XSS](https://portswigger.net/web-security/cross-site-scripting/dom-based)) arises when an application contains some client-side JavaScript that processes data from an untrusted source in an unsafe way, usually by writing the data back to the DOM.

In the following example, an application uses some JavaScript to read the value from an input field and write that value to an element within the HTML:

`var search = document.getElementById('search').value; var results = document.getElementById('results'); results.innerHTML = 'You searched for: ' + search;`

If the attacker can control the value of the input field, they can easily construct a malicious value that causes their own script to execute:

`You searched for: <img src=1 onerror='/* Bad stuff here... */'>`

In a typical case, the input field would be populated from part of the HTTP request, such as a URL query string parameter, allowing the attacker to deliver an attack using a malicious URL, in the same manner as reflected XSS.

- DOM-based XSS vulnerabilities usually arise when JavaScript takes data from an attacker-controllable source, such as the URL, and passes it to a sink that supports dynamic code execution, such as `eval()` or `innerHTML`
- To deliver a DOM-based XSS attack, you need to place data into a source so that it is propagated to a sink and causes execution of arbitrary JavaScript.

