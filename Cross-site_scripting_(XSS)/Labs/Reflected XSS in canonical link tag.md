----

### Lab description

This lab reflects user input in a canonical link tag and escapes angle brackets.

To solve the lab, perform a [cross-site scripting](https://portswigger.net/web-security/cross-site-scripting) attack on the home page that injects an attribute that calls the `alert` function.

To assist with your exploit, you can assume that the simulated user will press the following key combinations:

- `ALT+SHIFT+X`
- `CTRL+ALT+X`
- `Alt+X`

### Lab Solution

- Insert the payload  `%27accesskey=%27x%27onclick=%27alert(1)`  at `/`

![](/static/img/Pasted_image_20230620221800.png)