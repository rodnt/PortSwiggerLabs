----

### Lab description

This lab reflects your input in a JavaScript URL, but all is not as it seems. This initially seems like a trivial challenge; however, the application is blocking some characters in an attempt to prevent [XSS](https://portswigger.net/web-security/cross-site-scripting) attacks.

To solve the lab, perform a [cross-site scripting](https://portswigger.net/web-security/cross-site-scripting) attack that calls the `alert` function with the string `1337` contained somewhere in the `alert` message.


### Lab solution


- Insert the payload `&'},x=x=>{throw/**/onerror=alert,1337},toString=x,window+'',{x:'` 
![](/static/img/Pasted_image_20230620224735.png)