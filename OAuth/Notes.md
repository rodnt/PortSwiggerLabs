	
----

### What is Oauth

- OAuth is a commonly used authorization framework that enables websites and web applications to request limited access to a user's account on another application.
- Allows the user to grant this access **without** exposing their login credentials to the requesting application.
### How does OAuth work ?

- Have 3 components:
	- **Client application** - The website or web application that wants to access the user's data.
	- **Resource owner** - The user whose data the client application wants to access.
	- **OAuth service provider** - The website or application that controls the user's data and access to it. They support OAuth by providing an API for interacting with both an authorization server and a resource server.
- OAuth have many process to be used also as ( Oauth flows or grant types )
	- **Authorization code** and **Implicit** are the most used.
	- The `scope` parameter tells which data the app needs to access ( data from user )
		- `scope` are just strings
		- Can be many formats, such as urls and others thinks.
	- When Oauth is used for authentication the standard way is to use **OpenID** to connect to the scope
		- Example -> The scope `openid profile` will grant the client application read access to a predefined set of basic information about the user, such as their email address, username, and so on.

#### Authorization code ( this grant type is arguably the most secure )

- The client application (Web/Mobile app) and OAuth service first use redirects to exchange a series of browser-based HTTP requests that initiate the flow.
- If the user accept the 'pop up' the app is granted an `authorization code`.
- The `authorozization code` is send to Oauth service as is set as `Access token` which is user to make API calls.
- A `client_secret` is also generated  which the client application must use to authenticate itself when sending these server-to-server requests.

#### Inspect the Authorization code grant type

1. ( Authorization request) The app ask to the OAuth service the permission to access the user data.
	1. Endpoint usually have the `client_id` with the URL `https://app.com/auth?client_id=123&redirect_url=https://app.com/callback`
	2. `client_id` is unique for the app
	3. `redirect_uri` The URI to which the user's browser should be redirected when sending the authorization code to the client application. This is also known as the "callback URI" or "callback endpoint". Many OAuth attacks are based on exploiting flaws in the validation of this parameter
	4. If the URL has the `response_type` determines which kind of response the client application is expecting and, therefore, which flow it wants to initiate. For the authorization code grant type, the value should be `code`
	5. `scope` used to specify which subset of the user's data the client application wants to access
	6. `state` stores a unique, unguessable value that is tied to the current session on the client application this parameter serves as a form of [CSRF](https://portswigger.net/web-security/csrf) token for the client application by making sure that the request to its `/callback` endpoint is from the same person who initiated the OAuth flow
2. ( User login and consent )
	1. When the authorization server receives the initial request, it will redirect the user to a login page, where they will be prompted to log in to their account with the OAuth provider. For example, this is often their social media account.
	2. The data that the app will use is based on the `scope` variable
	3. It is important to note that once the user has approved a given scope for a client application, this step will be completed automatically as long as the user still has a valid session with the OAuth service.
3. ( Authorization code grant )
	1. If the user consents to the requested access, their browser will be redirected to the `/callback` endpoint that was specified in the `redirect_uri` parameter of the authorization request
	2. The resulting `GET` request will contain the authorization code as a query parameter. Depending on the configuration, it may also send the `state` parameter with the same value as in the authorization request
4. ( Access token request )
	1. Once the client application receives the authorization code, it needs to exchange it for an access token. Sends a server-to-server `POST` request to the OAuth service's `/token` endpoint.
	2. All communication from this point on takes place in a secure back-channel and, (  therefore, cannot usually be observed or controlled by an attacker
5. (  Access token grant )
	1. The OAuth service will validate the access token request. If everything is as expected, the server responds by granting the client application an access token with the requested scope.
 6. ( API call)
	 1. Now the client application has the access code, it can finally fetch the user's data from the resource server. To do this, it makes an API call to the OAuth service's `/userinfo` endpoint. The access token is submitted in the `Authorization: Bearer` header to prove that the client application has permission to access this data.
7. ( Resource grant )
	1. The resource server should verify that the token is valid and that it belongs to the current client application. If so, it will respond by sending the requested resource i.e. the user's data based on the scope of the access token.

### Implicit grant ( much simpler )

- Rather than first obtaining an authorization code and then exchanging it for an access token, the client application receives the access token immediately after the user gives their consent.
- When using the implicit grant type, all communication happens via browser redirects - there is no secure back-channel like in the **authorization code flow**.

#### Inspect the implicit grant

1. ( Authorization request )
	1. The implicit flow starts in much the same way as the authorization code flow. The only major difference is that the `response_type` parameter must be set to `token` and the Authorization code is `code`
2. ( User login and consent ) The user logs in and decides whether to consent to the requested permissions or not. This process is exactly the same as for the authorization code flow.
3. ( Access token grant )
	1. If the user gives their consent to the requested access, this is where things start to differ. The OAuth service will redirect the user's browser to the `redirect_uri` specified in the authorization request. However, instead of sending a query parameter containing an authorization code, it will send the access token and other token-specific data as a URL fragment.
	2. As the access token is sent in a URL fragment, it is never sent directly to the client application. Instead, the client application must use a suitable script to extract the fragment and store it.
4. ( API call )
	1. Once the client application has successfully extracted the access token from the URL fragment, it can use it to make API calls to the OAuth service's `/userinfo` endpoint. Unlike in the authorization code flow, this also happens via the browser
5. ( Resource grant)
	1. The resource server should verify that the token is valid and that it belongs to the current client application. If so, it will respond by sending the requested resource i.e. the user's data based on the scope associated with the access token.