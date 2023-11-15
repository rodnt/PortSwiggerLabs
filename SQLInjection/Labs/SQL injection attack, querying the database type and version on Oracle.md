
### lab description

This lab contains a [SQL injection](https://portswigger.net/web-security/sql-injection) vulnerability in the product category filter. You can use a UNION attack to retrieve the results from an injected query.

To solve the lab, display the database version string.


#### hint

> On Oracle databases, every `SELECT` statement must specify a table to select `FROM`. If your `UNION SELECT` attack does not query from a table, you will still need to include the `FROM` keyword followed by a valid table name. There is a built-in table on Oracle called `dual` which you can use for this purpose. For example: `UNION SELECT 'abc' FROM dual`For more information, see our [SQL injection cheat sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet).


### lab solution

- Finding the quantity tables using `order by clause`
![](/static/img/Pasted_image_20230606110016.png)
![](/static/img/Pasted_image_20230606110033.png)

- Retrieve the database content `2 columns` (null,null)
![](/static/img/Pasted_image_20230606110133.png)
- Lab solved
![](/static/img/Pasted_image_20230606110823.png)
![](/static/img/Pasted_image_20230606110836.png)


