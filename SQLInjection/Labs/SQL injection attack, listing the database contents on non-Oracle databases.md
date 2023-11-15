

### Lab description

This lab contains a [SQL injection](https://portswigger.net/web-security/sql-injection) vulnerability in the product category filter. The results from the query are returned in the application's response so you can use a UNION attack to retrieve data from other tables.

The application has a login function, and the database contains a table that holds usernames and passwords. You need to determine the name of this table and the columns it contains, then retrieve the contents of the table to obtain the username and password of all users.

To solve the lab, log in as the `administrator` user.


#### hint

> You can find some useful payloads on our [SQL injection cheat sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet).


#### lab solution

- Finding the number of columns with union ( two columns )
![](/static/img/Pasted_image_20230606112249.png)
- Finding the table contents with `information_schema.tables`
![](/static/img/Pasted_image_20230606112818.png)
- finding user credentials table, `replace the tables with columns`
![](/static/img/Pasted_image_20230606113204.png)
- Access credentials
![](/static/img/Pasted_image_20230606113538.png)
- Lab solved!
