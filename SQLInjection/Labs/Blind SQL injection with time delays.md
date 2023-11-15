

### Lab description

This lab contains a [blind SQL injection](https://portswigger.net/web-security/sql-injection/blind) vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows or causes an error. However, since the query is executed synchronously, it is possible to trigger conditional time delays to infer information.

To solve the lab, exploit the [SQL injection](https://portswigger.net/web-security/sql-injection) vulnerability to cause a 10 second delay.

#### Hint

> You can find some useful payloads on our [SQL injection cheat sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet).


### Lab solution

1. Access the app and submit the payload below inside the `trackingid` cookie
![](/static/img/Pasted_image_20230530105424.png)
2. lab solved!
