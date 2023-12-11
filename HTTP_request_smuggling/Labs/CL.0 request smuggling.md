
> We need to find a endpoint that ignores the content-length. But we need to find some endpoints to trigger that behavior.


1. POST request to a static file
2. POST request to a server level redirect
3. POST request that triggers a server side error

> After find that endpoint we need to keep in mind that we need some request settings

1. Send attack request over the same TCP connection
	1. header connection: Keep-alive
	2. Enable HTTP/1 connection Re-use
	3. Send Group - single connection

1. Send the following request to the lab.. and add the following configuration


![](Pasted_image_20231209223520.png)

> The servers returns timeout because with POST request we need to send some content.. 

> By default burp not use `connection: keep-alive` header so we need to do those config


![](Pasted_image_20231209224125.png)

> Add the 2 requests attacker and normal request ( GET request to /) as tab group


![](Pasted_image_20231209224240.png)

> The following images shows the results


![](Pasted_image_20231209224417.png)


![](Pasted_image_20231209224425.png)

> Add the /admin path and send it again

![](Pasted_image_20231209224625.png)

![](Pasted_image_20231209224644.png)

> Delete carlos


![](Pasted_image_20231209224715.png)

![](Pasted_image_20231209224721.png)

![](Pasted_image_20231209224736.png)
