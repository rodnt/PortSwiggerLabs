

### Lab description

This lab contains a [blind SQL injection](https://portswigger.net/web-security/sql-injection/blind) vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and no error messages are displayed. But the application includes a "Welcome back" message in the page if the query returns any rows.

The database contains a different table called `users`, with columns called `username` and `password`. You need to exploit the blind [SQL injection](https://portswigger.net/web-security/sql-injection) vulnerability to find out the password of the `administrator` user.

To solve the lab, log in as the `administrator` user.

#### Hint

> You can assume that the password only contains lowercase, alphanumeric characters.

#### Solution

- Condition `true` at cookie ( welcome back message appears )
	- payload `' and 1=1 --`
![](/static/img/Pasted_image_20230529095428.png)

- Payload `' and 1=2 --` (welcome back! message not appears )
![](/static/img/Pasted_image_20230529095633.png)

- Exploitation
	- confirming that the username is administrator
	- 1. Verify that the condition is true, confirming that there is a user called `administrator`.![](../img/Pasted_image_20230529115850.png)
- 2. The next step is to determine how many characters are in the password of the `administrator` user

![](/static/img/Pasted_image_20230529120631.png)

- Length of password: `' and (select 'a' from users where username='administrator' and length(password)>19)='a`

##### Hint: 
> You can do this manually using [Burp Repeater](https://portswigger.net/burp/documentation/desktop/tools/repeater), since the length is likely to be short. When the condition stops being true (i.e. when the "Welcome back" message disappears), you have determined the length of the password, which is in fact 20 characters long.

- 3.  After determining the length of the password, the next step is to test the character at each position to determine its value. This involves a much larger number of requests, so you need to use [Burp Intruder](https://portswigger.net/burp/documentation/desktop/tools/intruder). Send the request you are working on to Burp Intruder, using the context menu.

![](/static/img/Pasted_image_20230529123150.png)

![](/static/img/Pasted_image_20230529123210.png)

- Lab Solved 
	- `' AND (SELECT SUBSTRING(password,20,1) FROM users WHERE username='administrator')='j`
![](/static/img/Pasted_image_20230529130043.png)

