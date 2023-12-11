

1. Send the request to the `/` with the following configuration;

![](Pasted_image_20231210221548.png)

2. if the server response is delayed, maybe is vulnerable to CL.TE 
3. Next step is poison the back end;

4. Send the following payload to the backend to smuggle the request;

![](Pasted_image_20231210222134.png)

> Content-Length is 3 because we sent just one byte..
> Try to send new request and verify that everything is working correctly ( 404 response rsrs)

![](Pasted_image_20231210222252.png)

5. Go to any post and verify that the status code from the response;

![](Pasted_image_20231210222419.png)

> 302 we need this to exploit with the smuggle

6. Poison the request with that post ID

![](Pasted_image_20231210222606.png)

> Send the normal request and verify that works.

![](Pasted_image_20231210222636.png)

7. To redirect the victim we need to poison with arbitrary host;

![](Pasted_image_20231210222851.png)

![](Pasted_image_20231210222858.png)

8. Replace the URL for exploit server URL

![](Pasted_image_20231210224022.png)

