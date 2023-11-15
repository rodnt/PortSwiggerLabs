----

### Lab description

The user management functions for this lab are powered by a hidden GraphQL endpoint. You won't be able to find this endpoint by simply clicking pages in the site. The endpoint also has some defenses against introspection.

To solve the lab, find the hidden endpoint and delete Carlos.

We recommend that you install the InQL extension before attempting this lab. InQL makes it easier to modify GraphQL queries in Repeater, and enables you to scan the API schema.

For more information on using InQL, see [Working with GraphQL in Burp Suite](https://portswigger.net/burp/documentation/desktop/testing-workflow/session-management/working-with-graphql).

### Lab Solution

- Using burp access the endpoint `/api` you got an error 
![](/static/img/Pasted_image_20230703204049.png)
- Use the schema trick, to achieve the Graphql
![](/static/img/Pasted_image_20230703204155.png)
- I made a simple python script to encode those chars to bypass the filter

```python
import urllib.parse

import sys

json = sys.argv[1]

json_query = urllib.parse.quote(json)

print(json_query)

# usage python3 encode.py query={__schema{types{name,fields{name}}}}

```
- Fuzzing the with the words got from the others labs, i found the type `getUser`

![](/static/img/Pasted_image_20230703205251.png)

- After find the correct params of the selection i found the endpoint

![](/static/img/Pasted_image_20230703205804.png)

- Finding the types
![](/static/img/Pasted_image_20230703210402.png)
- Types with mutation

![](/static/img/Pasted_image_20230703210559.png)

- To delete the user carlos, we need to perform the mutation below 

![](/static/img/Pasted_image_20230703210705.png)

- Delete user and solve the lab

![](/static/img/Pasted_image_20230703211106.png)

![](/static/img/Pasted_image_20230703211301.png)

