
1. Log in and visit your account page. Submit the form for updating your billing and delivery address.
    
2. In Burp, go to the **Proxy > HTTP history** tab and find the `POST /my-account/change-address` request.
    
3. Observe that when you submit the form, the data from the fields is sent to the server as JSON. Notice that the server responds with a JSON object that appears to represent your user. This has been updated to reflect your new address information.
    
4. Send the request to Burp Repeater.
    
5. In Repeater, add a new property to the JSON with the name `__proto__`, containing an object with an arbitrary property:

```json
    "__proto__": { "foo":"bar" }
```
6. Send the request. Observe that the object in the response does not reflect the injected property. However, this doesn't necessarily mean that the application isn't vulnerable to prototype pollution.

![](Pasted_image_20231210180534.png)


7. Insert the following payload do change the key of JSON called `status`

![](Pasted_image_20231210180856.png)

8. Refresh the page, and lab will be solved

![](Pasted_image_20231210180938.png)

