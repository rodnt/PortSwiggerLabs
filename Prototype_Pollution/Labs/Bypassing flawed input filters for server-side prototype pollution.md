
1. Log in and visit your account page. Submit the form for updating your billing and delivery address.
    
2. In Burp, go to the **Proxy > HTTP history** tab and find the `POST /my-account/change-address` request.
    
3. Observe that when you submit the form, the data from the fields is sent to the server as JSON. Notice that the server responds with a JSON object that appears to represent your user. This has been updated to reflect your new address information.
    
4. Send the request to Burp Repeater.

5. Send the following payload the to the JSON request

![](Pasted_image_20231210181831.png)

6. Verify that all spaces are included
> Switch to Raw mode in burp tab

7. Insert the Admin gadget to exploit the issue;

![](Pasted_image_20231210182038.png)
![](Pasted_image_20231210182059.png)