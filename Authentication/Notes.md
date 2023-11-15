
#### Vulnerabilities in password-based login

- User's can register account or account is create by admin;
- User account is associated with **unique** a username and a password;
- 🚨 Consequently, the security of the website would be compromised if an attacker is able to either obtain or guess the login credentials of another user.

#### Brute-force attacks

> A brute-force attack is when an attacker uses a system of trial and error to guess valid user credentials. These attacks are typically automated using wordlists of usernames and passwords

- This attack can be fine tune with public knowledge or guessing;
- If the web site not protect the web site with captcha the site is highly vulnerable;

##### Brute-forcing usernames

> Usernames are especially easy to guess if they conform to a recognizable pattern, such as an email address

> it is very common to see business logins in the format `firstname.lastname@somecompany.com`. However, even if there is no obvious pattern, sometimes even high-privileged accounts are created using predictable usernames, such as `admin` or `administrator`.

- You should also check HTTP responses to see if any email addresses are disclosed. Occasionally, responses contain email addresses of high-privileged users, such as administrators or IT support.
###### Brute-forcing passwords

- Sometimes, passwords are:
	- Complex, with high entropy;
	- Hard do guess;

> However, while high-entropy passwords are difficult for computers alone to crack, we can use a basic knowledge of human behavior to exploit the vulnerabilities that users unwittingly introduce to this system.

- Users often take a password that they can remember and try to crowbar it into fitting the password policy;
- This knowledge of likely credentials and predictable patterns means that brute-force attacks can often be much more sophisticated, and therefore effective, than simply iterating through every possible combination of characters.


###### Username enumeration

- Username enumeration is when an attacker is able to **observe changes in the website's behavior** in order to identify whether a given username is valid.
- While brute-forcing login page pay attention on:
	- Status code page;
	- Error messages;
	- Response times;


##### Flawed brute-force protection

The two most common ways of preventing brute-force attacks are:

- Locking the account that the remote user is trying to access if they make too many failed login attempts
- Blocking the remote user's IP address if they make too many login attempts in quick succession
	- 🚨 Try to brute force using a combination with valid and invalid users;

###### Account locking

> Just as with normal login errors, responses from the server indicating that an account is locked can also help an attacker to enumerate usernames.

Locking an account offers a certain amount of protection against targeted brute-forcing of a specific account. However, this approach fails to adequately prevent brute-force attacks in which the attacker is just trying to gain access to any random account they can.

For example, the following method can be used to work around this kind of protection:

1. Establish a list of candidate usernames that are likely to be valid. This could be through username enumeration or simply based on a list of common usernames.
2. Decide on a very small shortlist of passwords that you think at least one user is likely to have. Crucially, the number of passwords you select must not exceed the number of login attempts allowed. For example, if you have worked out that limit is 3 attempts, you need to pick a maximum of 3 password guesses.
3. Using a tool such as Burp Intruder, try each of the selected passwords with each of the candidate usernames. This way, you can attempt to brute-force every account without triggering the account lock. You only need a single user to use one of the three passwords in order to compromise an account.
* 🚨 Account locking also fails to protect against credential stuffing attacks. This involves using a massive dictionary of `username:password` pairs, composed of genuine login credentials stolen in data breaches.

###### User rate limiting

Another way websites try to prevent brute-force attacks is through user rate limiting. In this case, making too many login requests within a short period of time causes your IP address to be blocked. Typically, the IP can only be unblocked in one of the following ways:

- Automatically after a certain period of time has elapsed;
- Manually by an administrator;
- Manually by the user after successfully completing a CAPTCHA;

##### HTTP basic authentication

-  In HTTP basic authentication, the client receives an authentication token from the server, which is constructed by concatenating the username and password, and encoding it in Base64.
- This token is stored and managed by the browser, which automatically adds it to the `Authorization` header of every subsequent request as follows:

`Authorization: Basic base64(username:password)`

For a number of reasons, this is generally not considered a secure authentication method. Firstly, it involves repeatedly sending the user's login credentials with every request. Unless the website also implements HSTS, user credentials are open to being captured in a man-in-the-middle attack.

In addition, implementations of HTTP basic authentication often don't support brute-force protection. As the token consists exclusively of static values, this can leave it vulnerable to being brute-forced.

HTTP basic authentication is also particularly vulnerable to session-related exploits, notably [CSRF](https://portswigger.net/web-security/csrf), against which it offers no protection on its own.

In some cases, exploiting vulnerable HTTP basic authentication might only grant an attacker access to a seemingly uninteresting page. However, in addition to providing a further attack surface, the credentials exposed in this way might be reused in other, more confidential contexts.

#### Vulnerabilities in other authentication mechanisms

- In addition to the basic login functionality, most websites provide supplementary functionality to allow users to manage their account. For example, users can typically change their password or reset their password when they forget it. These mechanisms can also introduce vulnerabilities that can be exploited by an attacker.

##### Keeping users logged in

- A common feature is the option to stay logged in even after closing a browser session. This is usually a simple checkbox labeled something like "Remember me" or "Keep me logged in".
- This functionality is often implemented by generating a "remember me" token of some kind, which is then stored in a persistent cookie. **As possessing this cookie effectively allows you to bypass the entire login process**.
-  If an attacker is able to create their own account because they can study their own cookie and potentially deduce how it is generated. Once they work out the formula, they can try to brute-force other users' cookies to gain access to their accounts.

- 🚨 In some rare cases, it may be possible to obtain a user's actual password in cleartext from a cookie, even if it is hashed. Hashed versions of well-known password lists are available online, so if the user's password appears in one of these lists, decrypting the hash can occasionally be as trivial as just pasting the hash into a search engine. This demonstrates the importance of salt in effective encryption.

##### Resetting user passwords

- Websites have to rely on alternative methods to make sure that the real user is resetting their own password;
- There are a few different ways that this feature is commonly implemented, with varying degrees of vulnerability.
	- Sending passwords by email, specially in plain text;
	- Resetting passwords using a URL
		- Less secure implementations of this method use a URL with an easily guessable parameter to identify which account is being reset, for example:
		  `http://vulnerable-website.com/reset-password?user=victim-user`
	- If the URL in the reset email is generated dynamically, this may also be vulnerable to password reset poisoning. In this case, an attacker can potentially steal another user's token and use it change their password.

##### Changing user passwords

* Typically, changing your password involves entering your current password and then the new password twice;
* Password change functionality can be particularly dangerous if it allows an attacker to access it directly without being logged in as the victim user.

### Fixing 

- All fixing are listed bellow:

https://portswigger.net/web-security/authentication/securing

