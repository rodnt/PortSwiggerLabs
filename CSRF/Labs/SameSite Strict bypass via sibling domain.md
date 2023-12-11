
1. Access the lab and verify that the cookie has the `strict` flag;

![](Pasted_image_20231210193831.png)

> With strict mode session cookie wont be send between cross site requests


2. Verify that the following request has no CSRF tokens;

![](Pasted_image_20231210194158.png)

3. Find the XSS at the login name;

![](Pasted_image_20231210195350.png)

4. 