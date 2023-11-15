
### Lab description


The user management functions for this lab are powered by a GraphQL endpoint. The lab contains an [access control](https://portswigger.net/web-security/access-control) vulnerability whereby you can induce the API to reveal user credential fields.

To solve the lab, sign in as the administrator and delete the username `carlos`.

We recommend that you install the InQL extension before attempting this lab. InQL makes it easier to modify GraphQL queries in Repeater, and enables you to scan the API schema.

For more information on using InQL, see [Working with GraphQL in Burp Suite](https://portswigger.net/burp/documentation/desktop/testing-workflow/session-management/working-with-graphql).

[](https://portswigger.net/academy/labs/launch/ccda6760929ebeccab51242f59b1573dd478087800b63c88fc8aa308db137802?referrer=%2fweb-security%2fgraphql%2flab-graphql-accidental-field-exposure)


### Lab solution

- Download the Jython extension at [https://www.jython.org/download.html](https://www.jython.org/download.html)
- Go to `Extensions` -> `Extension settings` -> `python enviroment`  -> `select file`  and chose the `.jar`  jython
- Go to `Extensions` tab and search for the extension ``

![](/static/img/Pasted_image_20230703190648.png)
- Visit any blog post and copy the graphql URL. Paste the URL at `InQL Scanner` at the Burp's menu and click at Load button and wait.

![](/static/img/Pasted_image_20230703190822.png)
- Get the `GetUser` schema.
> OBS: You can use the introspection query :) to get the schemas 

```json

{"query":"query IntrospectionQuery {\n  __schema {\n    queryType {\n      name\n    }\n    mutationType {\n      name\n    }\n    subscriptionType {\n      name\n    }\n    types {\n      ...FullType\n    }\n    directives {\n      name\n      description\n      args {\n        ...InputValue\n      }\n    }\n  }\n}\n\nfragment FullType on __Type {\n  kind\n  name\n  description\n  fields(includeDeprecated: true) {\n    name\n    description\n    args {\n      ...InputValue\n    }\n    type {\n      ...TypeRef\n    }\n    isDeprecated\n    deprecationReason\n  }\n  inputFields {\n    ...InputValue\n  }\n  interfaces {\n    ...TypeRef\n  }\n  enumValues(includeDeprecated: true) {\n    name\n    description\n    isDeprecated\n    deprecationReason\n  }\n  possibleTypes {\n    ...TypeRef\n  }\n}\n\nfragment InputValue on __InputValue {\n  name\n  description\n  type {\n    ...TypeRef\n  }\n  defaultValue\n}\n\nfragment TypeRef on __Type {\n  kind\n  name\n  ofType {\n    kind\n    name\n    ofType {\n      kind\n      name\n      ofType {\n        kind\n        name\n      }\n    }\n  }\n}\n"}

```

![](/static/img/Pasted_image_20230703191112.png)

- Change the query data as follows:

![](/static/img/Pasted_image_20230703191201.png)

- Lab solved!
  
  ![](/static/img/Pasted_image_20230703191258.png)