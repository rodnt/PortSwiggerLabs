

1. Login in with credentials and verify the stay logged in cookie

![](/static/img/Pasted_image_20231106221427.png)

2. Note that, the cookie have the following pattern

```
user + random md5 hash
```
3. The md5 hash is the password from the user
4. Add the following request to the burp intruder
![](/static/img/Pasted_image_20231106222334.png)
5. Setup the processing payloads
![](/static/img/Pasted_image_20231106222408.png)

![](/static/img/Pasted_image_20231106222441.png)

![](/static/img/Pasted_image_20231106222517.png)

```
Found : 159753
(hash = 5583413443164b56500def9a533c7c70)
```

