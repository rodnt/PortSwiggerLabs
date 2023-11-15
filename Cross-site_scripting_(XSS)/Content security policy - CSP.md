----

- CSP is a browser security mechanism that aims to mitigate [XSS](https://portswigger.net/web-security/cross-site-scripting) and some other attacks. It works by restricting the resources (such as scripts and images) that a page can load and restricting whether a page can be framed by other pages. To enable CSP, a response needs to include an HTTP response header called `Content-Security-Policy` with a value containing the policy. The policy itself consists of one or more directives, separated by semicolons

## Mitigating XSS attacks using CSP

The following directive will only allow scripts to be loaded from the [same origin](https://portswigger.net/web-security/cors/same-origin-policy) as the page itself:

`script-src 'self'`

The following directive will only allow scripts to be loaded from a specific domain:

`script-src https://scripts.normal-website.com`

- It's quite common for a CSP to block resources like `script`. However, many CSPs do allow image requests. This means you can often use `img` elements to make requests to external servers in order to disclose [CSRF](https://portswigger.net/web-security/csrf) tokens, for example.

## Mitigating dangling markup attacks using CSP

The following directive will only allow images to be loaded from the same origin as the page itself:

`img-src 'self'`

The following directive will only allow images to be loaded from a specific domain:

`img-src https://images.normal-website.com`

Note that these policies will prevent some dangling markup exploits, because an easy way to capture data with no user interaction is using an `img` tag. However, it will not prevent other exploits, such as those that inject an anchor tag with a dangling `href` attribute.

## Bypassing CSP with policy injection

You may encounter a website that reflects input into the actual policy, most likely in a `report-uri` directive. If the site reflects a parameter that you can control, you can inject a semicolon to add your own CSP directives. Usually, this `report-uri` directive is the final one in the list. This means you will need to overwrite existing directives in order to exploit this vulnerability and bypass the policy.

Normally, it's not possible to overwrite an existing `script-src` directive. However, Chrome recently introduced the `script-src-elem` directive, which allows you to control `script` elements, but not events. Crucially, this new directive allows you to [overwrite existing `script-src` directives](https://portswigger.net/research/bypassing-csp-with-policy-injection)