
----

### Lab Description

This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response so you can use a UNION attack to retrieve data from other tables.

The database contains a different table called `users`, with columns called `username` and `password`.

To solve the lab, perform a [SQL injection UNION](https://portswigger.net/web-security/sql-injection/union-attacks) attack that retrieves all usernames and passwords, and use the information to log in as the `administrator` user.



#### Lab solution

- Try to get more data than one will trigger an erro

![](/static/img/Pasted_image_20230613221943.png)


- Using the string concat from Oracle, we can solve the lab

![](/static/img/Pasted_image_20230613222323.png)

