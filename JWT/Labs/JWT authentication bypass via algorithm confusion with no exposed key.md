

### Lab description

This lab uses a JWT-based mechanism for handling sessions. It uses a robust RSA key pair to sign and verify tokens. However, due to implementation flaws, this mechanism is vulnerable to algorithm confusion attacks.

To solve the lab, first obtain the server's public key. Use this key to sign a modified session token that gives you access to the admin panel at `/admin`, then delete the user `carlos`.

You can log in to your own account using the following credentials: `wiener:peter`

* Lab hint s
> We recommend familiarizing yourself with [how to work with JWTs in Burp Suite](https://portswigger.net/burp/documentation/desktop/testing-workflow/session-management/jwts) before attempting this lab.
> You can assume that the server stores its public key as an X.509 PEM file.

### Solution

* Access the lab, login and copy the `session` token.
* Log out and login again to get another `session` token
* Running the tool with the tokens that you got
`docker run --rm -it portswigger/sig2n <token1> <token2>`
![](/static/img/Pasted_image_20230526232453.png)
![](/static/img/Pasted_image_20230526233935.png)
* Replace the session cookie with this new JWT (from the output of the tool) and then send the request
![](/static/img/Pasted_image_20230526234000.png)

* Copy  the x509 key from the output tool and go to `JWT Editor Tab`
*  Create a new `symetric key` and change the value of `k` of the x509 copied from previous step
* Go back to repeater and at `JSON Web Token` tab change the value of `sub` to administrador, after that click at the bottom `sign` button.
![](/static/img/Pasted_image_20230526234412.png)

Send the request to `/admin/delete?username=carlos`

* Lab solved!
  ![](/static/img/Pasted_image_20230526234532.png)
