
----

- GraphQL is an API query language that is designed to facilitate efficient communication between clients and servers. It enables the user to specify exactly what data they want in the response, helping to avoid the large response objects and multiple calls that can sometimes be seen with REST APIs. GraphQL services define a contract through which a client can communicate with a server. The client doesn't need to know where the data resides. Instead, clients send queries to a GraphQL server, which fetches data from the relevant places. As GraphQL is platform-agnostic, it can be implemented with a wide range of programming languages and can be used to communicate with virtually any data store.

- How it works
	- GraphQL schemas define the structure of the service's data, listing the available objects (known as types), fields, and relationships.
	- **All GraphQL operations use the same endpoint**, and are generally sent as a POST request. This is significantly different to REST APIs, which use operation-specific endpoints across a range of HTTP methods. With GraphQL, the type and name of the operation define how the query is handled, rather than the endpoint it is sent to or the HTTP method used.

## What is a GraphQL schema?

In GraphQL, the schema represents a contract between the frontend and backend of the service. It defines the data available as a series of types, using a human-readable schema definition language. These types can then be implemented by a service.

Most of the types defined are object types. which define the objects available and the fields and arguments they have. Each field has its own type, which can either be another object or a scalar, enum, union, interface, or custom type.

The example below shows a simple schema definition for a Product type. The `!` operator indicates that the field is non-nullable when called (that is, mandatory).

`#Example schema definition type Product { id: ID! name: String! description: String! price: Int }`

Schemas must also include at least one available query. Usually, they also contain details of available mutations.

## What are GraphQL queries?

GraphQL queries retrieve data from the data store. They are roughly equivalent to GET requests in a REST API.

Queries usually have the following key components:

- A `query` operation type. This is technically optional but encouraged, as it explicitly tells the server that the incoming request is a query.
- A query name. This can be anything you want. **The query name is optional**, but encouraged as it can help with debugging.
- A data structure. This is the data that the query should return.
- Optionally, one or more arguments. These are used to create queries that return details of a specific object (for example "give me the name and description of the product that has the ID 123").

The example below shows a query called `myGetProductQuery` that requests the name, and description fields of a product with the `id` of `123`.

`#Example query query myGetProductQuery { getProduct(id: 123) { name description } }`

Note that the product type may contain more fields in the schema than those requested here. The ability to request only the data you need is a significant part of the flexibility of GraphQL.

## What are GraphQL mutations?

Mutations change data in some way, either adding, deleting, or editing it. They are roughly equivalent to a REST API's POST, PUT, and DELETE methods.

Like queries, mutations have an operation type, name, and structure for the returned data. **However, mutations always take an input of some type**. This can be an inline value, but in practice is generally provided **as a variable**.

The example below shows a mutation to create a new product and its associated response. In this case, the service is configured to automatically assign an ID to new products, which has been returned as requested.

`#Example mutation request mutation { createProduct(name: "Flamin' Cocktail Glasses", listed: "yes") { id name listed } }` `#Example mutation response { "data": { "createProduct": { "id": 123, "name": "Flamin' Cocktail Glasses", "listed": "yes" } } }`

## Components of queries and mutations

The GraphQL syntax includes several common components for queries and mutations.

### Fields

All GraphQL types contain items of queryable data called fields. When you send a query or mutation, you specify which of the fields you want the API to return. The response mirrors the content specified in the request.

The example below shows a query to get ID and name details for all employees, and its associated response. In this case, `id`, `name.firstname`, and `name.lastname` are the fields requested.

`#Request query myGetEmployeeQuery { getEmployees { id name { firstname lastname } } }` `#Response { "data": { "getEmployees": [ { "id": 1, "name" { "firstname": "Carlos", "lastname": "Montoya" } }, { "id": 2, "name" { "firstname": "Peter", "lastname": "Wiener" } } ] } }`

### Arguments

Arguments are values that are provided for specific fields. The arguments that can be accepted for a type are defined in the schema.

When you send a query or mutation that contains arguments, the GraphQL server determines how to respond based on its configuration. For example, it might return a specific object rather than details of all objects.

The example below shows a `getEmployee` request that takes an employee ID as an argument. In this case, the server responds with only the details of the employee who matches that ID.

`#Example query with arguments query myGetEmployeeQuery { getEmployees(id:1) { name { firstname lastname } } }` `#Response to query { "data": { "getEmployees": [ { "name" { "firstname": Carlos, "lastname": Montoya } } ] } }`



### Variables

Variables enable you to pass dynamic arguments, rather than having arguments directly within the query itself.

Variable-based queries use the same structure as queries using inline arguments, but certain aspects of the query are taken from a separate JSON-based variables dictionary. They enable you to reuse a common structure among multiple queries, with only the value of the variable itself changing.

When building a query or mutation that uses variables, you need to:

- Declare the variable and type.
- Add the variable name in the appropriate place in the query.
- Pass the variable key and value from the variable dictionary.

The example below shows the same query as in the previous example, but with the ID passed as a variable instead of as a direct part of the query string.

`#Example query with variable query getEmployeeWithVariable($id: ID!) { getEmployees(id:$id) { name { firstname lastname } } } Variables: { "id": 1 }`

In this example, the variable is declared in the first line with (`$id: ID!`). The `!` indicates that this is a required field for this query. It is then used as an argument in the second line with (`id:$id`). Finally, the value of the variable itself is set in the variable JSON dictionary. For information on how to test for these vulnerabilities, see [Testing GraphQL APIs](https://portswigger.net/web-security/graphql).


### Aliases

GraphQL objects **can't contain multiple properties with the same name**. For example, the following query is invalid because it tries to return the `product` type twice.

`#Invalid query query getProductDetails { getProduct(id: 1) { id name } getProduct(id: 2) { id name } }`

Aliases enable you to bypass this restriction by explicitly naming the properties you want the API to return. You can use aliases to return multiple instances of the same type of object in one request. This helps to reduce the number of API calls needed.

In the example below, the query uses aliases to specify a unique name for both products. This query now passes validation, and the details are returned.

`#Valid query using aliases query getProductDetails { product1: getProduct(id: "1") { id name } product2: getProduct(id: "2") { id name } }` `#Response to query { "data": { "product1": { "id": 1, "name": "Juice Extractor" }, "product2": { "id": 2, "name": "Fruit Overlays" } } }`


### Fragments

Fragments are reusable parts of queries or mutations. They contain a subset of the fields belonging to the associated type.

Once defined, they can be included in queries or mutations. If they are subsequently changed, the change is included in every query or mutation that calls the fragment.

The example below shows a `getProduct` query in which the details of the product are contained in a `productInfo` fragment.

`#Example fragment fragment productInfo on Product { id name listed }` `#Query calling the fragment query { getProduct(id: 1) { ...productInfo stock } }` `#Response including fragment fields { "data": { "getProduct": { "id": 1, "name": "Juice Extractor", "listed": "no", "stock": 5 } } }`


### Fragments

Fragments are reusable parts of queries or mutations. They contain a subset of the fields belonging to the associated type.

Once defined, they can be included in queries or mutations. If they are subsequently changed, the change is included in every query or mutation that calls the fragment.

The example below shows a `getProduct` query in which the details of the product are contained in a `productInfo` fragment.

`#Example fragment fragment productInfo on Product { id name listed }` `#Query calling the fragment query { getProduct(id: 1) { ...productInfo stock } }` `#Response including fragment fields { "data": { "getProduct": { "id": 1, "name": "Juice Extractor", "listed": "no", "stock": 5 } } }`


## Subscriptions

Subscriptions are a special type of query. They enable clients to establish a long-lived connection with a server so that the server can then push real-time updates to the client without the need to continually poll for data. They are primarily useful for small changes to large objects and for functionality that requires small real-time updates (like chat systems or collaborative editing).

As with regular queries and mutations, the subscription request defines the shape of the data to be returned.

Subscriptions are commonly implemented using [WebSockets](https://portswigger.net/web-security/websockets).

## Introspection

Introspection is a built-in GraphQL function that enables you to query a server for information about the schema. It is commonly used by applications such as GraphQL IDEs and documentation generation tools.

Like regular queries, you can specify the fields and structure of the response you want to be returned. For example, you might want the response to only contain the names of available mutations.

Introspection can represent a serious [information disclosure](https://portswigger.net/web-security/information-disclosure) risk, as it can be used to access potentially sensitive information (such as field descriptions) and help an attacker to learn how they can interact with the API. It is best practice for introspection to be disabled in production environments.