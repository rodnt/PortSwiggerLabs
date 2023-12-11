
1. In Burp's browser, use the lab's search function a couple of times and observe that the website records your recent search history. Send the most recent `POST /` request to Burp Repeater and remove your session cookie before resending the request. Notice that your search history is reset, confirming that it's tied to your session cookie.
2. Config the `attacker` request to exploit the lab

![](Pasted_image_20231209204325.png)


![](Pasted_image_20231209205302.png)

![](Pasted_image_20231209205314.png)

3. Add the following content to the `attacker` request, with more content at `Content-Length` to "leak" more data at `search` func from the app

![](Pasted_image_20231209210526.png)

4. Send the request few times and the result will be

![](Pasted_image_20231209210633.png)


5. Send the request again and search for victim request

![](Pasted_image_20231209210812.png)

6. Copy the session cookie from the "leaked" search and send the request to the `/` and you're done

![](Pasted_image_20231209211016.png)

