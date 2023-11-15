----

### Lab Description


This lab contains a [DOM-based cross-site scripting](https://portswigger.net/web-security/cross-site-scripting/dom-based) vulnerability in the search blog functionality. It uses an `innerHTML` assignment, which changes the HTML contents of a `div` element, using data from `location.search`.

To solve this lab, perform a cross-site scripting attack that calls the `alert` function.


- Lab Solution

- insert the following payload inside the search functionality
```
<img%20src%20onerror=alert(1)>
```

![](/static/img/Pasted_image_20230627143103.png)


![](/static/img/Pasted_image_20230627143037.png)