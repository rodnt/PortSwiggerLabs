----

### Lab Description


This lab contains a [DOM-based cross-site scripting](https://portswigger.net/web-security/cross-site-scripting/dom-based) vulnerability in the submit feedback page. It uses the jQuery library's `$` selector function to find an anchor element, and changes its `href` attribute using data from `location.search`.

To solve this lab, make the "back" link alert `document.cookie`.


### Lab Solution

- Set the canary token at the `feeback` parameter, and verify inside the dom invader burp suite extension

![](/static/img/Pasted_image_20230627143602.png)

- Insert the payload `javascript:alert(1)` at `returnPath` parameter

![](/static/img/Pasted_image_20230627143740.png)