
### Lab description

This lab contains a [SQL injection](https://portswigger.net/web-security/sql-injection) vulnerability in the product category filter. You can use a UNION attack to retrieve the results from an injected query.

To solve the lab, display the database version string.

#### hint

> You can find some useful payloads on our [SQL injection cheat sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet).


#### Lab solution

- Verify the quantity of columns using union technique 
![](/static/img/Pasted_image_20230606111220.png)
![](/static/img/Pasted_image_20230606111303.png)
- Extract the database content
![](/static/img/Pasted_image_20230606111357.png)
![](/static/img/Pasted_image_20230606111410.png)



