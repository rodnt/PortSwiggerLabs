
1. Log in with `wiener` credentials;
2. Submit the form for updating your billing and delivery address;
3. Observe that when you submit the form, the data from the fields is sent to the server as JSON;
![](Pasted_image_20231210175407.png)

4. Verify the server response has a user object;

![](Pasted_image_20231210175506.png)

5. Add the following payload to the JSON request;

![](Pasted_image_20231210175620.png)


```json
"__proto__": { "foo":"bar" }
```

6. Notice that the object in the response now includes the arbitrary property that you injected, but no `__proto__` property. This strongly suggests that you have successfully polluted the object's prototype and that your property has been inherited via the prototype chain.

![](Pasted_image_20231210175731.png)

7. Add the following payload to become admin;

![](Pasted_image_20231210175917.png)


```json
"__proto__": {
    "isAdmin":true
}
```

8. Delete carlos;

![](Pasted_image_20231210180021.png)

