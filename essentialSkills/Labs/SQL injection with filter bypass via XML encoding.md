### Lab description

This lab contains a [SQL injection](https://portswigger.net/web-security/sql-injection) vulnerability in its stock check feature. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables.

The database contains a `users` table, which contains the usernames and passwords of registered users. To solve the lab, perform a SQL injection attack to retrieve the admin user's credentials, then log in to their account.


#### Hint
> A web application firewall (WAF) will block requests that contain obvious signs of a SQL injection attack. You'll need to find a way to obfuscate your malicious query to bypass this filter. We recommend using the [Hackvertor](https://portswigger.net/bappstore/65033cbd2c344fbabe57ac060b5dd100) extension to do this.
> Tutorial can be found here: https://portswigger.net/research/bypassing-wafs-and-cracking-xor-with-hackvertor


### Solution
- verify the input `1 + 1` return
![](/static/ima/Pasted_image_20230528175534.png)
- WAF block the payload `union select null`
![](/static/img/Pasted_image_20230528175624.png)
- Using the burp extension hackvector to bypass the waf with **dec_entities/hex_entities**
![](/static/img/Pasted_image_20230528175744.png)

- Log with admin account and solve the lab!