----


### Lab description

This lab uses an OAuth service to allow users to log in with their social media account. Flawed validation by the client application makes it possible for an attacker to log in to other users' accounts without knowing their password. To solve the lab, log in to Carlos's account. His email address is `carlos@carlos-montoya.net`. You can log in with your own social media account using the following credentials: `wiener:peter`.

### Lab Solution

1. Login with `wiener` and verify the `authenticate`  endpoint
2. Replace the `email` parameter value to `carlos@carlos-montoya.net`
3. Right at the request on repeater `Request in browser` `in original session`
![[Pasted image 20230725103036.png]]