
* JWT libraries typically provide one method for verifying tokens and another that just decodes them. For example, the Node.js library `jsonwebtoken` has `verify()` and `decode()`.

* Occasionally, developers confuse these two methods and only pass incoming tokens to the `decode()` method. This effectively means that the application doesn't verify the signature at all.

---
* JWT authentication bypass via unverified signature

`To solve the lab, modify your session token to gain access to the admin panel at `/admin`, then delete the user `carlos``

* Using JWT editor tool

![](../img/Pasted_image_20230523190331.png)

* Change the value of `sub` to `administrador`

![](../img/Pasted_image_20230523190713.png)

* Delete the user to **solve** the lab

![](../img/Pasted_image_20230523190819.png)


