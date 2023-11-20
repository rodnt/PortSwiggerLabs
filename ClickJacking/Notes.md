
- Protection against CSRF attacks is often provided by the use of a [CSRF token](https://portswigger.net/web-security/csrf#common-defences-against-csrf): a session-specific, single-use number or nonce. 
- Clickjacking attacks are not mitigated by the CSRF token as a target session is established with content loaded from an authentic website and with all requests happening on-domain.
- CSRF tokens are placed into requests and passed to the server as part of a normally behaved session. The difference compared to a normal user session is that the process occurs within a hidden iframe.

### Simple ClickJacking Payload


```html
<head> <style> #target_website { position:relative; width:128px; height:128px; opacity:0.00001; z-index:2; } #decoy_website { position:absolute; width:300px; height:400px; z-index:1; } </style> </head> ... <body> <div id="decoy_website"> ...decoy web content here... </div> <iframe id="target_website" src="https://vulnerable-website.com"> </iframe> </body>

```

#### Payload explained 

- The target website iframe is positioned within the browser so that there is a precise overlap of the target action with the decoy website using appropriate width and height position values. Absolute and relative position values are used to ensure that the target website accurately overlaps the decoy regardless of screen size, browser type and platform. The z-index determines the stacking order of the iframe and website layers. The opacity value is defined as 0.0 (or close to 0.0) so that the iframe content is transparent to the user. Browser clickjacking protection might apply threshold-based iframe transparency detection (for example, Chrome version 76 includes this behavior but Firefox does not). The attacker selects opacity values so that the desired effect is achieved without triggering protection behaviors.