
----

### Lab description

This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. To construct such an attack, you need to combine some of the techniques you learned in previous labs.

The database contains a different table called `users`, with columns called `username` and `password`.

To solve the lab, perform a [SQL injection UNION](https://portswigger.net/web-security/sql-injection/union-attacks) attack that retrieves all usernames and passwords, and use the information to log in as the `administrator` user.


#### Lab Solution

1 - Get the number of columns with order by or null payloads

![](/static/img/Pasted_image_20230613221425.png)

2 - Retrieve the usernames and passwords change the string values from commands
![](/static/img/Pasted_image_20230613221327.png)

3 - Lab solved!