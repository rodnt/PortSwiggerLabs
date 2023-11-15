
* Obfuscating attacks using encodings
	* To take your skills further, you'll need to **adapt the techniques you've learned to overcome these additional obstacles**, unearthing vulnerabilities that other testers may have overlooked;
	* In this section, we'll provide some suggestions on how you **can obfuscate harmful payloads to evade input filters and other flawed defenses**. Specifically, you'll learn how to use standard encodings to take advantage of misconfigurations and handling discrepancies between connected systems.
*  Using [Burp Scanner](https://portswigger.net/burp/vulnerability-scanner) during manual testing
	* you can optimize your workflow by using Burp Scanner to supplement your own knowledge and intuition.
	* Not only does this reduce the chance of you overlooking things, it can save you valuable time by helping you to rapidly identify potential attack vectors;
	* This means you can concentrate your time and effort on things that can't be easily automated, such as working out how to exploit the vulnerable behavior or chain it with your other findings.

--- 

### Using Burp Scanner during manual testing

* Scanning a specific request
	* When you come across an interesting function or behavior, your first instinct may be to send the relevant requests to Repeater or Intruder and investigate further. **But it's often beneficial to hand the request to Burp Scanner as well**. It can get to work on the more repetitive aspects of testing while you put your skills to better use elsewhere;
	![](/static/img/Pasted_image_20230527112538.png)
---

### Scanning custom insertion points

* Testing specific inputs
	* First, send the request to **Burp Intruder**. On the **Positions** tab, add payload positions to any insertion points you're interested in, then right-click and select **Scan defined insertion points**
	* You can then configure and launch a scan that will place payloads in these positions only. This lets you focus on the inputs you're interested in **rather than scanning a whole bunch of cookies that you know are unlikely to be of any use**
![](/static/img/Pasted_image_20230527115840.png)
 * it's often quicker to use the [Scan manual insertion point](https://portswigger.net/bappstore/ca7ee4e746b54514a0ca5059329e926f) extension in this case. You can then highlight any sequence of characters within the request, typically a parameter value, and select **Extensions > Scan manual insertion point** from the context menu.
 * This approach can yield results incredibly quickly, giving you something to work with in just a couple of seconds. It also means you can choose to scan inputs that Burp Scanner normally doesn't use, such as custom header values.
---

### Scanning non-standard data structures

* As you're free to define insertion points in arbitrary positions, you can also target a specific substring within a value. Among other things, this can be useful for scanning non-standard data structures.
* Burp Scanner will treat this string `user=12312-carlos` as unique string. By manually defining an insertion point on each part of the value separately, you can accurately scan even non-standard data structures like this

![](/static//img/Pasted_image_20230527120847.png)


--- 

### Obfuscating attacks using encodings

*  Context-specific decoding
	* Both clients and servers use a variety of different encodings to pass data between systems.
	* When they want to actually use the data, this often means they have to decode it first
	* When constructing an attack, you should think about where exactly your payload is being injected
	* If you can infer how your input is being decoded based on this context, you can potentially identify alternative ways to represent the same payload
* Decoding discrepancies
	* Injection attacks often involve injecting payloads that use recognizable patterns, such as HTML tags, JavaScript functions, or SQL statements.
	*  websites often implement defences that block requests containing these suspicious patterns.
	* However, these kinds of **input filters** also need **to decode the input in order to check whether it's safe or not**
	* It's vital that the decoding performed when checking the input is the same as the decoding performed by the back-end server or browser when it eventually uses the data.
* Obfuscation via URL encoding
	* In URLs, a series of reserved characters carry special meaning Ex:
		* `&` ->  separate parameters
		* = -> receive a value
		* ?parameter= -> this a full parameter
	* **Browsers automatically URL encode any characters that may cause ambiguity for parsers**. This usually means substituting them with a `%` character and their 2-digit hex code as follows:
		* `[...]/?search=Fish+%26+Chips`
	 * **Any URL-based input is automatically URL decoded server-side** before it is assigned to the relevant variables
	* Sequences like `%22`, `%3C`, and `%3E` in a query parameter are synonymous with `"`, `<`, and `>` characters respectively. ( you can inject URL-encoded data via the URL and it will usually still be interpreted correctly by the back-end application ).
	* Smuggle payloads to the back-end application simply by encoding any characters or words that are blacklisted, example:
		*  For example, in a SQL injection attack, you might encode the keywords, so `SELECT` becomes `%53%45%4C%45%43%54` and so on.
*  Obfuscation via double URL encoding
	*  Some servers perform **two rounds of URL decoding** on any URLs they receive.
	* This discrepancy enables an attacker to smuggle malicious input to the back-end by simply encoding it twice.
	* If you are blocked using the URL encode payload ``[...]/?search=%3Cimg%20src%3Dx%20onerror%3Dalert(1)%3E`` try to double encode using %25 for each `%` character. Example: ``[...]/?search=%253Cimg%2520src%253Dx%2520onerror%253Dalert(1)%253E`` . As the WAF only decodes this once, **it may not be able to identify that the request is dangerous. If the back-end server subsequently double-decodes** this input, the payload will be successfully injected
* Obfuscation via HTML encoding
	* In HTML documents, certain characters **need to be escaped or encoded** to prevent the browser from incorrectly interpreting them as part of the markup.
	* This is achieved by substituting the offending characters with a reference, prefixed with an ampersand and terminated with a semicolon.
	* This is achieved by substituting the offending characters with a reference, prefixed with an ampersand and terminated with a semicolon, example `&colon`; or can be a hexadecimal or decimal number: `&#58;` `&#x3a;` 
	* Browsers will automatically decode these  references (ampersand references)  when they parse the document;
	* You can occasionally take advantage of this to **obfuscate payloads for client-side attack**.
	*  If the server-side checks are looking for the `alert()` payload explicitly, they might not spot this if you HTML encode one or more of the characters: `<img src=x onerror="&#x61;lert(1)">` ( When the browser renders the page, it will decode and execute the injected payload. )
* Leading Zeros
	* Using decimal or hex-style HTML encoding, you can optionally include arbitrary number of leading zeros in the code point to by pass WAF.
	* If your payloads still gets block after the HTML encoding it, you can evade this filter using a prefixing with few zeros
	  `<a href="javascript&#00000000000058;alert(1)">Click me</a>`
	  `&#00000000000058;` -> %3a -> &#x3a -> `:` ( double dots : encoding )
* ## Obfuscation via unicode escaping
	*  **Unicode** escape sequences consist of the prefix `\u` followed by the four-digit hex code for the character.
	* `\003a` represents a colon.
	* ES6 also supports a new form of unicode escape using curly braces: `\u{3a}`.
	* **Most programming languages** decode these unicode escapes. ( this includes the **JavaScript engine used by browsers** ).
	* You can **obfuscate client-side payloads using unicode**, just like we did with HTML escapes
	* For example, let's say you're trying to exploit [DOM XSS](https://portswigger.net/web-security/cross-site-scripting/dom-based) where your input is passed to the `eval()` sink as a string. If your initial attempts are blocked, try escaping one of the characters as follows: ``eval("\u0061lert(1)")``
	* **Inside a string, you can escape any characters like this**. However, outside of a string, escaping some characters will result in a syntax error. This includes opening and closing parentheses. `<a href="javascript\u{0000000003a}alert(1)">Click me</a>`
 -  Obfuscation via hex escaping
	 - Another option when injecting into a string context is to use hex escapes.
	 - Represent characters using their hexadecimal code point, prefixed with `\x`
	 - For example, the lowercase letter `a` is represented by `\x61`
	 - Just like **unicode escapes**, these **will be decoded client-side as long as the input is evaluated as a string**: `eval("\x61lert")` ( remember inside strings " " not outside ! )
	 - Note that you can sometimes also obfuscate SQL statements in a similar manner using the prefix `0x`. For example, `0x53454c454354` may be decoded to form the `SELECT` keyword.
-  Obfuscation via XML encoding
	- XML also supports character encoding using the same numeric scape sequences
	- Even if you don't need to encode any special characters to avoid syntax errors, you can potentially take advantage of this behavior to obfuscate payloads in the same way as you do with HTML encoding,
-  Obfuscation via octal escaping
	- Octal escaping works in pretty much the same way as hex escaping, uses 8 numbering system rather than base-16.
	- These are prefixed with a standalone backslash, meaning that the lowercase letter `a` is represented by `\141`. Example of `paylaod` `eval("\141lert(1)")`
- Obfuscation via multiple encodings
	- It is important to note that you can combine encodings to hide your payloads
	- Example: `<a href="javascript:&bsol;u0061lert(1)">Click me</a>`
	- Browsers will first HTML decode `&bsol;,` resulting in a backslash. This has the effect of turning the otherwise arbitrary `u0061` characters into the unicode escape `\u0061`:
		``<a href="javascript:\u0061lert(1)">Click me</a>``
- Obfuscation via the SQL CHAR() function
	- By concatenating the returned values, you can use this approach to obfuscate blocked keywords. For example, even if `SELECT` is blacklisted, the following injection initially appears harmless:
	- `CHAR(83)+CHAR(69)+CHAR(76)+CHAR(69)+CHAR(67)+CHAR(84)`
	- However, when this is processed as SQL by the application, it will dynamically construct the `SELECT` keyword and execute the injected query.
	- SQLMap has this encode [https://book.hacktricks.xyz/pentesting-web/sql-injection/sqlmap](https://book.hacktricks.xyz/pentesting-web/sql-injection/sqlmap)
--- 

### Identifying unknown vulnerabilities

> Mystery labs have vulnerabilities that are unknown by people :) 
> You need to go alone here :D 

[https://portswigger.net/web-security/mystery-lab-challenge](https://portswigger.net/web-security/mystery-lab-challenge)