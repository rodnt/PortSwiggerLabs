

### Lab description

This lab contains a [SQL injection](https://portswigger.net/web-security/sql-injection) vulnerability in the product category filter. The results from the query are returned in the application's response so you can use a UNION attack to retrieve data from other tables.

The application has a login function, and the database contains a table that holds usernames and passwords. You need to determine the name of this table and the columns it contains, then retrieve the contents of the table to obtain the username and password of all users.

To solve the lab, log in as the `administrator` user.


#### Hint

> On Oracle databases, every `SELECT` statement must specify a table to select `FROM`. If your `UNION SELECT` attack does not query from a table, you will still need to include the `FROM` keyword followed by a valid table name. There is a built-in table on Oracle called `dual` which you can use for this purpose. For example: `UNION SELECT 'abc' FROM dual` For more information, see our [SQL injection cheat sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet).


#### Lab solution

- Getting the database columns with union technique
![](/static/img/Pasted_image_20230606114647.png)
- getting the table with `union all select table_name,null from all_tables`
![](/static/img/Pasted_image_20230606114916.png)

- Getting username and passwords
![](/static/img/Pasted_image_20230606115510.png)

- Authenticate with admin and password retrieved and.. **lab solved!**  