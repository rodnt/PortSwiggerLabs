
1. Login into any provided account;
2. Verify that, the request has two CSRF protection, one is cookie protection and token protection;
![](/static/img/Pasted_image_20231107160032.png)
3. Login with another account, and copy the `csrfKey` and `csrf` values and test with the account request of the step 2 and verify that works.
4. The search function from the blog, is vulnerable to CRLF injection;
5. Use this CRLF injection to create a following exploit and with CSRF PoC chain;

![](/static/img/Pasted_image_20231107160551.png)
![](/static/img/Pasted_image_20231107160608.png)
