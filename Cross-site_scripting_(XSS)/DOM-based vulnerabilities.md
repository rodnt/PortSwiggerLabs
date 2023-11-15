----

## What is the DOM?

The Document Object Model (DOM) is a web browser's hierarchical representation of the elements on the page. Websites can use JavaScript to manipulate the nodes and objects of the DOM, as well as their properties. DOM manipulation in itself is not a problem. In fact, it is an integral part of how modern websites work. However, JavaScript that handles data insecurely can enable various attacks. DOM-based vulnerabilities arise when a website contains JavaScript that **takes an attacker-controllable value, known as a source, and passes it into a dangerous function, known as a sink**.

## Taint-flow vulnerabilities

Many DOM-based vulnerabilities **can be traced back to problems with the way client-side code manipulates attacker-controllable data**.

### What is taint flow?

To either exploit or mitigate these vulnerabilities, it is important to first familiarize yourself with the basics of taint flow between sources and sinks.

- Source
> A **source** is a JavaScript property that accepts data that is potentially attacker-controlled. An example of a source is the `location.search` property because it reads input from the query string, which is relatively simple for an attacker to control. Ultimately, **any property that can be controlled by the attacker is a potential source**. This includes the referring URL (exposed by the `document.referrer` string), the user's cookies (exposed by the `document.cookie` string), and web messages.

- Sink
> A sink is a potentially dangerous JavaScript function or DOM object that can cause undesirable effects if attacker-controlled data is passed to it. For example, the `eval()` function is a sink because it processes the argument that is passed to it as JavaScript. An example of an HTML sink is `document.body.innerHTML` because it potentially allows an attacker to inject malicious HTML and execute arbitrary JavaScript.

- Fundamentally, DOM-based vulnerabilities arise when a website passes data from a source to a sink, which then handles the data in an unsafe way in the context of the client's session

### Common sources

The following are typical sources that can be used to exploit a variety of taint-flow vulnerabilities:

`document.URL document.documentURI document.URLUnencoded document.baseURI location document.cookie document.referrer window.name history.pushState history.replaceState localStorage sessionStorage IndexedDB (mozIndexedDB, webkitIndexedDB, msIndexedDB) Database`



----

## DOM XSS combined with reflected and stored data

Some pure DOM-based vulnerabilities are self-contained within a single page. If a script reads some data from the URL and writes it to a dangerous sink, then the vulnerability is entirely client-side.

However, **sources aren't limited to data that is directly exposed by browsers** - they can also originate from the website. For example, websites often reflect URL parameters in the HTML response from the server. This is commonly associated with normal XSS, but it can also lead to reflected DOM XSS vulnerabilities.

In a reflected DOM XSS vulnerability, the server processes data from the request, and echoes the data into the response. The reflected data might be placed into a JavaScript string literal, or a data item within the DOM, such as a form field. A script on the page then processes the reflected data in an unsafe way, ultimately writing it to a dangerous sink.  Example

`eval('var data = "reflected string"');`

Websites may also store data on the server and reflect it elsewhere. In a stored DOM XSS vulnerability, the server receives data from one request, stores it, and then includes the data in a later response. A script within the later response contains a sink which then processes the data in an unsafe way.

`element.innerHTML = comment.author`

## Which sinks can lead to DOM-XSS vulnerabilities?

https://portswigger.net/web-security/cross-site-scripting/dom-based#dom-xss-combined-with-reflected-and-stored-data


## Exploiting DOM XSS with different sources and sinks

- In principle, a website is vulnerable to DOM-based cross-site scripting if there is an executable path via which data can propagate from source to sink. In practice, different sources and sinks have differing properties and behavior that can affect exploitability, and determine what techniques are necessary.

The `innerHTML` sink doesn't accept `script` elements on any modern browser, nor will `svg onload` events fire. This means you will need to use alternative elements like `img` or `iframe`. Event handlers such as `onload` and `onerror` can be used in conjunction with these elements. For example:

`element.innerHTML='... <img src=1 onerror=alert(document.domain)> ...'`

Another potential sink to look out for is jQuery's `$()` selector function, which can be used to inject malicious objects into the DOM.

jQuery used to be extremely popular, and a classic DOM XSS vulnerability was caused by websites using this selector in conjunction with the `location.hash` source for animations or auto-scrolling to a particular element on the page. This behavior was often implemented using a vulnerable `hashchange` event handler, similar to the following:

`$(window).on('hashchange', function() { var element = $(location.hash); element[0].scrollIntoView(); });`

As the `hash` is user controllable, an attacker could use this to inject an XSS vector into the `$()` selector sink. More recent versions of jQuery have patched this particular vulnerability by preventing you from injecting HTML into a selector when the input begins with a hash character (`#`). However, you may still find vulnerable code in the wild.

To actually exploit this classic vulnerability, you'll need to find a way to trigger a `hashchange` event without user interaction. One of the simplest ways of doing this is to deliver your exploit via an `iframe`:

`<iframe src="https://vulnerable-website.com#" onload="this.src+='<img src=1 onerror=alert(1)>'">`

In this example, the `src` attribute points to the vulnerable page with an empty hash value. When the `iframe` is loaded, an XSS vector is appended to the hash, causing the `hashchange` event to fire.