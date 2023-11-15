
* JWT -> Json web tokens
	*  most commonly used in authentication, session management and access control

![](img/Pasted_image_20230523183126.png)

* What is JWT ?
	* JSON web tokens (JWTs) are a standardized format for sending cryptographically signed JSON data between systems.
	* They can contain any kind of data, but majority of times is used for access controle of users (session handler);
	* **JWT are stored in client-side A.K.A Browser**;
	* Are the common choice because of interection between servers;

* JWT Format
	* 3 Parts
		* header: **base64** part of the JWT (JSON Object)
		* Payload: **base64** part of the JWT (JSON Object)
		* Signature: Contains clains **claims** about the user
	 * In most cases, this data can be easily read or modified by anyone with access to the token. Therefore, the security of any JWT-based mechanism is **heavily reliant on the cryptographic signature**
	* Use the site [https://jwt.io/](https://jwt.io/) to decode the JWT or burp decoder function or bash;
	* JWT Example
	 ``` eyJraWQiOiI5MTM2ZGRiMy1jYjBhLTRhMTktYTA3ZS1lYWRmNWE0NGM4YjUiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTY0ODAzNzE2NCwibmFtZSI6IkNhcmxvcyBNb250b3lhIiwic3ViIjoiY2FybG9zIiwicm9sZSI6ImJsb2dfYXV0aG9yIiwiZW1haWwiOiJjYXJsb3NAY2FybG9zLW1vbnRveWEubmV0IiwiaWF0IjoxNTE2MjM5MDIyfQ.SYZBPIBg2CRjXAJ8vCER0LA_ENjII1JakvNQoP-Hw6GG1zfl4JyngsZReIfqRvIAEi5L4HV0q7_9qGhQZvy9ZdxEJbwTxRs_6Lb-fZTDpW6lKYNdMyjw45_alSCZ1fypsMWz_2mTpQzil0lOtps5Ei_z7mM7M8gCwe_AGpI53JxduQOaB5HkT5gVrv9cKu9CsW5MS6ZbqYXpGyOG5ehoxqm8DL5tFYaW3lB50ELxi0KsuTKEbD0t5BCl0aCR2MBJWAbN-xeLwEenaqBiwPVvKixYleeDQiBEIylFdNNIMviKRgXiYuAvMziVPbwSgkZVHeEdF5MQP1Oe2Spac-6IfA```

* Decoded JWT
![Pasted_image_20230523183914.png](img/Pasted_image_20230523183914.png)


* JWT Signature
	* The server that issues the token typically generates the signature by **hashing the header and payload** ( this can be encrypted ) this process need a  **sign key** to verify if the data inside the token was tampered. 
		* **Without knowing the server's secret signing key, it shouldn't be possible to generate the correct signature for a given header or payload.**

* JWT vs JWS vs JWE
	* The JWT spec is extended by both the JSON Web Signature (JWS) and JSON Web Encryption (JWE) specifications, which define concrete ways of actually implementing JWTs.

![](img/Pasted_image_20230523184655.png)

* JWT is a common JWS 
* JWE (E) are encrypted istead of encoding like JWS (JWT)

---

* Attacking JWT
	* Attack JWT usually tamper the JWT tokens to impersonate someone or broken the access control;
	* If an **attacker is able to create their own valid tokens with arbitrary values**, they may be able to escalate their own **privileges or impersonate other users**, taking full control of their accounts.
	* Flaws usually mean that **the signature of the JWT is not verified properly**;
	* If the server key is leaked in some way, or can be guessed or brute-forced, an attacker can generate a valid signature for any arbitrary token, compromising the entire mechanism;

* Exploiting JWT
	* By design, servers don't usually store any information about the JWTs that they issue;
	* The server doesn't actually know anything about the original contents of the token;

* Brute force the keys
	* Some signing algorithms, such as **HS256 (HMAC + SHA-256)**, use an arbitrary, standalone string as the secret key;
	* Just like a password, it's crucial that this secret **can't be easily guessed** or brute-forced by an attacker;
	* If the server uses an extremely weak secret, it may even be possible to brute-force this character-by-character rather than using a wordlist;
	* Wordlist to crack [https://raw.githubusercontent.com/wallarm/jwt-secrets/master/jwt.secrets.list](https://raw.githubusercontent.com/wallarm/jwt-secrets/master/jwt.secrets.list)
	* I'ts better to install hashcat [https://hashcat.net/hashcat/](https://hashcat.net/hashcat/)
		* Alternatives:
			* [https://github.com/ojensen5115/jwtcrack](https://github.com/ojensen5115/jwtcrack)
	* How to install [https://hashcat.net/wiki/doku.php?id=frequently_asked_questions#how_do_i_install_hashcat](https://hashcat.net/wiki/doku.php?id=frequently_asked_questions#how_do_i_install_hashcat)
	* Use the command bellow to run the hashcat with the wordlist
```bash
hashcat -a 0 -m 16500 <jwt> <wordlist>
```

* JWT Header parameter injections
	* According to the JWS specification, only the `alg` header parameter is mandatory. In practice, however, JWT headers (also known as JOSE headers) often contain several other parameters. **The following ones are of particular interest to attackers**
		* `jwk` (JSON Web Key) - Provides an embedded JSON object representing the key;
		*  `jku` (JSON Web Key Set URL) - Provides a URL from which servers can fetch a set of keys containing the correct key;
		* `kid` (Key ID) - Provides an ID that servers can use to identify the correct key in cases where there are multiple keys to choose from. Depending on the format of the key, this may have a matching `kid` parameter.

* Injecting self-signed JWTs via the jwk parameter
	* The JSON Web Signature (JWS) specification describes an optional `jwk` header parameter, which servers can use to **embed their public key directly within the token** itself in JWK format.
	* A JWK (JSON Web Key) is a standardized format for representing keys as a JSON object.
```json
{ 

"kid": "ed2Nf8sb-sD6ng0-scs5390g-fFD8sfxG", "typ": "JWT", "alg": "RS256", 
"jwk": { "kty": "RSA", "e": "AQAB", "kid": "ed2Nf8sb-sD6ng0-scs5390g-fFD8sfxG", "n": "yy1wpYmffgXBxhAUJzHHocCuJolwDqql75ZWuCQ_cb33K2vh9m" } }

```

* Ideally, servers should only use a **limited whitelist of public keys to verify JWT signatures**.However, misconfigured servers sometimes use any key that's embedded in the `jwk` parameter. You can exploit this behavior by signing a modified JWT **using your own RSA private key**, then embedding the matching public key in the `jwk` header
* How to do that, using burp:
	* With the extension loaded, in Burp's main tab bar, go to the **JWT Editor Keys** tab.
	* [Generate a new RSA key.](https://portswigger.net/burp/documentation/desktop/testing-workflow/session-management/jwts#adding-a-jwt-signing-key)
	* Send a request containing a JWT to Burp Repeater.
	* In the message editor, switch to the extension-generated **JSON Web Token** tab and [modify](https://portswigger.net/burp/documentation/desktop/testing-workflow/session-management/jwts#editing-jwts) the token's payload however you like.
	* Click **Attack**, then select **Embedded JWK**. When prompted, select your newly generated RSA key.
	* Send the request to test how the server responds.
	* **You can also perform this attack manually by adding the `jwk` header yourself. However, you may also need to update the JWT's `kid` header parameter to match the `kid` of the embedded key. The extension's built-in attack takes care of this step for you.**

* Injecting self-signed JWTs via the jku parameter
	* Instead of embedding public keys directly using the `jwk` header parameter, some servers let you use the `jku` (JWK Set URL) header parameter to reference a JWK Set containing the key. When verifying the signature, the server fetches the relevant key from this URL;
	* JWK Sets like this are sometimes exposed publicly via a standard endpoint, such as `/.well-known/jwks.json`.
	* More secure websites will only fetch keys from **trusted domains, but you can sometimes take advantage of URL parsing discrepancies to bypass this kind of filtering**
	* A JWK Set is a JSON object containing an array of JWKs representing different keys. You can see an example of this below

`{ "keys": [ { "kty": "RSA", "e": "AQAB", "kid": "75d0ef47-af89-47a9-9061-7c02a610d5ab", "n": "o-yy1wpYmffgXBxhAUJzHHocCuJolwDqql75ZWuCQ_cb33K2vh9mk6GPM9gNN4Y_qTVX67WhsN3JvaFYw-fhvsWQ" }, { "kty": "RSA", "e": "AQAB", "kid": "d8fDFo-fS9-faS14a9-ASf99sa-7c1Ad5abA", "n": "fc3f-yy1wpYmffgXBxhAUJzHql79gNNQ_cb33HocCuJolwDqmk6GPM4Y_qTVX67WhsN3JvaFYw-dfg6DH-asAScw" } ] }`

* Injecting self-signed JWTs via the kid parameter
	* Servers may use several cryptographic keys for signing different kinds of data, not just JWTs. For this reason, the header of a JWT may contain a `kid` (Key ID) parameter, which helps the server identify which key to use when verifying the signature;
	* **Verification keys `kid` are often stored as a JWK Set**. In this case, the server may simply look for the JWK **with the same `kid` as the token**. However, the JWS specification doesn't define a concrete structure for this ID - **it's just an arbitrary string of the developer's choosing**. For example, they might use the `kid` parameter to point to a particular entry in a database, or even the name of a file;
	* If this parameter is also vulnerable to [directory traversal](https://portswigger.net/web-security/file-path-traversal), an attacker could potentially force the server to use an arbitrary file from its filesystem as the verification key.
	  `{ "kid": "../../path/to/file", "typ": "JWT", "alg": "HS256", "k":`
	  ``
	  * This is especially dangerous if the server also supports JWTs signed using a [symmetric algorithm](https://portswigger.net/web-security/jwt/algorithm-confusion#symmetric-vs-asymmetric-algorithms). In this case, an attacker could potentially point the `kid` parameter to a predictable, static file, then sign the JWT using a secret that matches the contents of this file;
	  * You could theoretically do this with any file, but one of the simplest methods is to use `/dev/null`, which is present on most Linux systems. As this is an empty file, reading it returns an empty string. Therefore, signing the token with a empty string will result in a valid signature;
	  * **If you're using the JWT Editor extension, note that this doesn't let you sign tokens using an empty string. However, due to a bug in the extension, you can get around this by using a Base64-encoded null byte**
	 > If the server stores its verification keys in a database, the `kid` header parameter is also a potential vector for [SQL injection](https://portswigger.net/web-security/sql-injection) attacks
	 
* Other interesting JWT header parameters
	*  `cty` ( Content Type) - Sometimes used to declare a media type for the content in the JWT payload.
	* If you have found a way to bypass signature verification, you can try injecting a `cty` header to change the content type to `text/xml` or `application/x-java-serialized-object`, which can potentially enable new vectors for [XXE](https://portswigger.net/web-security/xxe) and [deserialization](https://portswigger.net/web-security/deserialization) attacks
	* `x5c` (X.509 Certificate Chain) - Sometimes used to pass the X.509 public key certificate or certificate chain of the key used to digitally sign the JWT. This header parameter can be used to inject self-signed certificates, similar to the [`jwk` header injection](https://portswigger.net/web-security/jwt#injecting-self-signed-jwts-via-the-jwk-parameter) attacks.
	* Check out [CVE-2017-2800](https://talosintelligence.com/vulnerability_reports/TALOS-2017-0293) and [CVE-2018-2633](https://mbechler.github.io/2018/01/20/Java-CVE-2018-2633).
*  JWT algorithm confusion
	* Even if a server uses robust secrets that you are unable to brute-force you may still be able to forge valid **JWTs by signing the token using an algorithm that the developers haven't anticipated**. This is known as an algorithm confusion attack
	* https://portswigger.net/web-security/jwt/algorithm-confusion
		* Occur when an attacker is able to force the server to verify the signature of a JSON web token ([JWT](https://portswigger.net/web-security/jwt)) using a different algorithm than is intended by the website's developers
		* This may enable attackers to forge valid JWTs containing arbitrary values **without needing to know the server's secret signing key**.
* Algorithm confusion
	* Algorithm confusion vulnerabilities typically arise due to flawed implementation of JWT libraries.
	* These methods rely on the `alg` parameter in the token's header to determine the type of verification they should perform.
	 * Steps to reproduce the algorithm confusion attack
		 * [Obtain the server's public key](https://portswigger.net/web-security/jwt/algorithm-confusion#step-1-obtain-the-server-s-public-key)
		 * [Convert the public key to a suitable format](https://portswigger.net/web-security/jwt/algorithm-confusion#step-2-convert-the-public-key-to-a-suitable-format)
		 * [Create a malicious JWT](https://portswigger.net/web-security/jwt/algorithm-confusion#step-3-modify-your-jwt) with a modified payload and the `alg` header set to `HS256`
		 *  [Sign the token with HS256](https://portswigger.net/web-security/jwt/algorithm-confusion#step-4-sign-the-jwt-using-the-public-key), using the public key as the secret.
	 *  Convert the public key to a suitable format
		 * With the extension loaded, in Burp's main tab bar, go to the **JWT Editor Keys** tab.
		 * Click **New RSA** Key. In the dialog, paste the JWK that you obtained earlier.
		 * Select the **PEM** radio button and copy the resulting PEM key.
		 * Go to the **Decoder** tab and Base64-encode the PEM.
		 * Go back to the **JWT Editor Keys** tab and click **New Symmetric Key**.
		 * In the dialog, click **Generate** to generate a new key in JWK format.
		 * Replace the generated value for the `k` parameter with a Base64-encoded PEM key that you just copied.
		 * Save the key.
	 * Modify the JWT 
		 * Once you have the public key in a suitable format, you can [modify the JWT](https://portswigger.net/burp/documentation/desktop/testing-workflow/session-management/jwts#editing-jwts) however you like. Just make sure that the `alg` header is set to `HS256`.
	 * Sign the JWT using the public key
		 * [Sign the token](https://portswigger.net/burp/documentation/desktop/testing-workflow/session-management/jwts#adding-a-jwt-signing-key) using the HS256 algorithm with the RSA public key as the secret
* Deriving public keys from existing tokens
	* In cases where the public key isn't readily available, you may still be able to test for algorithm confusion by deriving the key from a pair of existing JWTs.
	* This process is relatively simple using tools such as `jwt_forgery.py` on the [`rsa_sign2n` GitHub repository](https://github.com/silentsignal/rsa_sign2n)
	* To create a local container use the docker command bellow
	* `docker run --rm -it portswigger/sig2n <token1> <token2>`
	* This tool uses the JWTs that you provide to calculate one or more potential values of `n`. Don't worry too much about what this means - all you need to know is that only one of these matches the value of `n` used by the server's key. For each potential value, our script outputs:
		*  A Base64-encoded PEM key in both X.509 and PKCS1 format.
		* A forged JWT signed using each of these keys.
		* To identify the correct key, **use Burp Repeater to send a request containing each of the forged JWTs**. **Only one** of these will be accepted by the server. You can then use the matching key to construct an algorithm confusion attack.
		* For more information on how this process works, and details of how to use the standard `jwt_forgery.py` tool, please refer to the documentation provided in the [repository](https://github.com/silentsignal/rsa_sign2n).
--- 

* Dealing with JWT with burpsuite


![](img/Pasted_image_20230523185653.png)
![](img/Pasted_image_20230523185706.png)
![](img/Pasted_image_20230523185714.png)


--- 

###  Symmetric vs asymmetric algorithms

*  **HS256** (HMAC + SHA-256) use a "symmetric" key. (Symetric ("S" single key))
	* This means that the server uses a **single key** to both sign and verify the token (Just like a password).

![](img/Pasted_image_20230526215855.png)

* **RS256** (RSA + SHA-256) use an "asymmetric" key pair.
	* Private key, which the server uses to sign the token, and a mathematically related public key that can be used to verify the signature.

![](img/Pasted_image_20230526220003.png)

* As the names suggest, the private key **must be kept secret**, but the public key is often shared so that anybody can verify the signature of tokens issued by the server.
--- 

### How to FIX/Prevent JWT issues

You can protect your own websites against many of the attacks we've covered by taking the following high-level measures:

-   Use an up-to-date library for handling JWTs and make sure your developers fully understand how it works, along with any security implications. Modern libraries make it more difficult for you to inadvertently implement them insecurely, but this isn't foolproof due to the inherent flexibility of the related specifications.
-   Make sure that you perform robust signature verification on any JWTs that you receive, and account for edge-cases such as JWTs signed using unexpected algorithms.
-   Enforce a strict whitelist of permitted hosts for the `jku` header.
-   Make sure that you're not vulnerable to [path traversal](https://portswigger.net/web-security/file-path-traversal) or SQL injection via the `kid` header parameter.
Although not strictly necessary to avoid introducing vulnerabilities, we recommend adhering to the following best practice when using JWTs in your applications:
-   Always set an expiration date for any tokens that you issue.
-   Avoid sending tokens in URL parameters where possible.
-   Include the `aud` (audience) claim (or similar) to specify the intended recipient of the token. This prevents it from being used on different websites.
-   Enable the issuing server to revoke tokens (on logout, for example).
