
----

### Lab Description

This lab contains a [DOM-based cross-site scripting](https://portswigger.net/web-security/cross-site-scripting/dom-based) vulnerability in the stock checker functionality. It uses the JavaScript `document.write` function, which writes data out to the page. The `document.write` function is called with data from `location.search` which you can control using the website URL. The data is enclosed within a select element.

To solve this lab, perform a cross-site scripting attack that breaks out of the select element and calls the `alert` function.


### Lab solution

- Insert the payload 
```
https://academyID.net/product?productId=1&storeId="></select><img%20src=1%20onerror=alert(1)>
```


### Sources and sinks in third-party dependencies

Modern web applications are typically built using a number of third-party libraries and frameworks, which often provide additional functions and capabilities for developers. It's important to remember that some of these are also potential sources and sinks for DOM XSS.

#### DOM XSS in jQuery

If a JavaScript library such as jQuery is being used, look out for sinks that can alter DOM elements on the page. For instance, jQuery's `attr()` function can change the attributes of DOM elements. If data is read from a user-controlled source like the URL, then passed to the `attr()` function, then it may be possible to manipulate the value sent to cause XSS. For example, here we have some JavaScript that changes an anchor element's `href` attribute using data from the URL:

`$(function() { $('#backLink').attr("href",(new URLSearchParams(window.location.search)).get('returnUrl')); });`

You can exploit this by modifying the URL so that the `location.search` source contains a malicious JavaScript URL. After the page's JavaScript applies this malicious URL to the back link's `href`, clicking on the back link will execute it:

`?returnUrl=javascript:alert(document.domain)`