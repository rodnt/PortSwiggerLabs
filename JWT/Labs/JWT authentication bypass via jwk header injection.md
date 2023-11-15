
This lab uses a JWT-based mechanism for handling sessions. The server supports the `jwk` parameter in the JWT header. This is sometimes used to embed the correct verification key directly in the token. However, it fails to check whether the provided key came from a trusted source.

To solve the lab, modify and sign a JWT that gives you access to the admin panel at `/admin`, then delete the user `carlos`.

You can log in to your own account using the following credentials: `wiener:peter`

* Create new key with JWT Editor

![](../img/Pasted_image_20230524101306.png)

* Change the token
![](../img/Pasted_image_20230524103147.png)
![](../img/Pasted_image_20230524103255.png)

* Solve the lab
![](../img/Pasted_image_20230524103345.png)



