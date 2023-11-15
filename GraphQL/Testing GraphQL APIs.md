----

- GraphQL vulnerabilities generally arise due to implementation and design flaws.


## Finding GraphQL endpoints

- Before you can test a GraphQL API, you first need to find its endpoint. **As GraphQL APIs use the same endpoint for all requests**, this is a valuable piece of information.

### Universal queries

If you send `query{__typename}` to any GraphQL endpoint, it will include the string `{"data": {"__typename": "query"}}` somewhere in its response. This is known as a universal query, and is a useful tool in probing whether a URL corresponds to a GraphQL service.

The query works because every GraphQL endpoint has a reserved field called `__typename` that returns the queried object's type as a string.

### Common endpoint names

GraphQL services often use similar endpoint suffixes. When testing for GraphQL endpoints, you should look to send universal queries to the following locations:

- `/graphql`
- `/api`
- `/api/graphql`
- `/graphql/api`
- `/graphql/graphql`

If these common endpoints don't return a GraphQL response, you could also try appending `/v1` to the path.

### Request methods

The next step in trying to find GraphQL endpoints is to test using different request methods.

**It is best practice for production GraphQL endpoints to only accept POST requests that have a content-type of `application/json`, as this helps to protect against CSRF vulnerabilities**. However, some endpoints may accept alternative methods, such as GET requests or POST requests that use a content-type of `x-www-form-urlencoded`.

If you can't find the GraphQL endpoint by sending POST requests to common endpoints, try resending the universal query using alternative HTTP methods.

### Initial testing

Once you have discovered the endpoint, you can send some test requests to understand a little more about how it works. If the endpoint is powering a website, try exploring the web interface in Burp's browser and use the HTTP history to examine the queries that are sent.

## Exploiting unsanitized arguments

At this point, you can start to look for vulnerabilities. Testing query arguments is a good place to start.

If the API uses arguments to access objects directly, it may be vulnerable to [access control](https://portswigger.net/web-security/access-control) vulnerabilities. A user could potentially access information they should not have simply by supplying an argument that corresponds to that information. This is sometimes known as an insecure direct object reference (IDOR).

## Discovering schema information

The next step in testing the API is to piece together information about the underlying schema.

The best way to do this is to use introspection queries. Introspection is a built-in GraphQL function that enables you to query a server for information about the schema.

Introspection helps you to understand how you can interact with a GraphQL API. It can also disclose potentially sensitive data, such as description fields.


### Using introspection

To use introspection to discover schema information, query the `__schema` field. This field is available on the root type of all queries.

Like regular queries, you can specify the fields and structure of the response you want to be returned when running an introspection query. For example, you might want the response to contain only the names of available mutations.


### Probing for introspection

It is best practice for introspection to be disabled in production environments, but this advice is not always followed.

You can probe for introspection using the following simple query. If introspection is enabled, the response returns the names of all available queries.

`#Introspection probe request { "query": "{__schema{queryType{name}}}" }`

### Running a full introspection query

The next step is to run a full introspection query against the endpoint so that you can get as much information on the underlying schema as possible.

The example query below returns full details on all queries, mutations, subscriptions, types, and fragments.

`#Full introspection query query IntrospectionQuery { __schema { queryType { name } mutationType { name } subscriptionType { name } types { ...FullType } directives { name description args { ...InputValue } onOperation #Often needs to be deleted to run query onFragment #Often needs to be deleted to run query onField #Often needs to be deleted to run query } } } fragment FullType on __Type { kind name description fields(includeDeprecated: true) { name description args { ...InputValue } type { ...TypeRef } isDeprecated deprecationReason } inputFields { ...InputValue } interfaces { ...TypeRef } enumValues(includeDeprecated: true) { name description isDeprecated deprecationReason } possibleTypes { ...TypeRef } } fragment InputValue on __InputValue { name description type { ...TypeRef } defaultValue } fragment TypeRef on __Type { kind name ofType { kind name ofType { kind name ofType { kind name } } } }`


### Visualizing introspection results

Responses to introspection queries can be full of information, but are often very long and hard to process.

You can view relationships between schema entities more easily using a [GraphQL visualizer](http://nathanrandal.com/graphql-visualizer/). This is an online tool that takes the results of an introspection query and produces a visual representation of the returned data, including the relationships between operations and types.

### Using InQL

As an alternative to running an introspection query manually and visualizing the results, you can use Burp Suite's InQL extension.

InQL is a Burp Suite extension that helps you to audit GraphQL APIs securely. When you pass a URL to it (either by providing a live endpoint link or by uploading a JSON file), it issues an introspection query requesting all queries and mutations, and presents a structured view to make it easy to explore the results.

### Suggestions

Even if introspection is entirely disabled, you can sometimes use suggestions to glean information on an API's structure.

Suggestions are a feature of the Apollo GraphQL platform in which the server can suggest query amendments in error messages. These are generally used where a query is slightly incorrect but still recognizable (for example, `There is no entry for 'productInfo'. Did you mean 'productInformation' instead?`).

You can potentially glean useful information from this, as the response is effectively giving away valid parts of the schema.

[Clairvoyance](https://github.com/nikitastupin/clairvoyance) is a tool that uses suggestions to automatically recover all or part of a GraphQL schema, even when introspection is disabled. This makes it significantly less time consuming to piece together information from suggestion responses.

You cannot disable suggestions directly in Apollo. See [this GitHub thread](https://github.com/apollographql/apollo-server/issues/3919#issuecomment-836503305) for a workaround.

## Bypassing GraphQL introspection defenses

If you cannot get introspection queries to run for the API you are testing, try inserting a special character after the `__schema` keyword.

When developers disable introspection, they could use a regex to exclude the `__schema` keyword in queries. You should try characters like spaces, new lines and commas, as they are ignored by GraphQL but not by flawed regex.

As such, if the developer has only excluded `__schema{`, then the below introspection query would not be excluded.

`#Introspection query with newline { "query": "query{__schema {queryType{name}}}" }`

If this doesn't work, try running the probe over an alternative request method, as introspection may only be disabled over POST. Try a GET request, or a POST request with a content-type of `x-www-form-urlencoded`.

The example below shows an introspection probe sent via GET, with URL-encoded parameters.

`# Introspection probe as GET request GET /graphql?query=query%7B__schema%0A%7BqueryType%7Bname%7D%7D%7D`

#### Note

If an endpoint will only accept introspection queries over GET and you want to analyze the results of the query using InQL Scanner, you will first need to save the query results to a file. You can then load this file into InQL, where it will be parsed as normal.


## Bypassing rate limiting using aliases

Ordinarily, GraphQL objects can't contain multiple properties with the same name. Aliases enable you to bypass this restriction by explicitly naming the properties you want the API to return. You can use aliases to return multiple instances of the same type of object in one request.

#### More information

For more information on GraphQL aliases, see [Aliases](https://portswigger.net/web-security/graphql/what-is-graphql#aliases).

While aliases are intended to limit the number of API calls you need to make, they can also be used to brute force a GraphQL endpoint.

Many endpoints will have some sort of rate limiter in place to prevent brute force attacks. Some rate limiters work based on the number of HTTP requests received rather than the number of operations performed on the endpoint. Because aliases effectively enable you to send multiple queries in a single HTTP message, they can bypass this restriction.

The simplified example below shows a series of aliased queries checking whether store discount codes are valid. This operation could potentially bypass rate limiting as it is a single HTTP request, even though it could potentially be used to check a vast number of discount codes at once.

`#Request with aliased queries query isValidDiscount($code: Int) { isvalidDiscount(code:$code){ valid } isValidDiscount2:isValidDiscount(code:$code){ valid } isValidDiscount3:isValidDiscount(code:$code){ valid } }`

## GraphQL CSRF

Cross-site request forgery (CSRF) vulnerabilities enable an attacker to induce users to perform actions that they do not intend to perform. This is done by creating a malicious website that forges a cross-domain request to the vulnerable application.

#### More information

For more information on CSRF vulnerabilities in general, see the [CSRF academy topic](https://portswigger.net/web-security/csrf).

GraphQL can be used as a vector for CSRF attacks, whereby an attacker creates an exploit that causes a victim's browser to send a malicious query as the victim user.

### How do CSRF over GraphQL vulnerabilities arise?

CSRF vulnerabilities can arise where a GraphQL endpoint does not validate the content type of the requests sent to it and no CSRF tokens are implemented.

POST requests that use a content type of `application/json` are secure against forgery as long as the content type is validated. In this case, an attacker wouldn't be able to make the victim's browser send this request even if the victim were to visit a malicious site.

However, alternative methods such as GET, or any request that has a content type of `x-www-form-urlencoded`, can be sent by a browser and so may leave users vulnerable to attack if the endpoint accepts these requests. Where this is the case, attackers may be able to craft exploits to send malicious requests to the API.

The steps to construct a [CSRF attack](https://portswigger.net/web-security/csrf) and deliver an exploit are the same for GraphQL-based CSRF vulnerabilities as they are for "regular" CSRF vulnerabilities. For more information on this process, see [How to construct a CSRF attack](https://portswigger.net/web-security/csrf#how-to-construct-a-csrf-attack).

To defend against GraphQL CSRF vulnerabilities, ensure the following:

- Your GraphQL API only accepts queries over JSON-encoded POST.
- The API validates that content provided matches the supplied content type.
- The API has a secure CSRF token mechanism.