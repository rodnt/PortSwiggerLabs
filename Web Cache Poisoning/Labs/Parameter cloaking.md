
1. Using param miner scan using the `Rails parameter cloaking scan` option
2. Access the file /js/geolocate.js and verify that you cant execute without the callback parameter. 
![](/static/img/Pasted_image_20231117170304.png)
3. Observe that every page imports the script `/js/geolocate.js`, executing the callback function `setCountryCookie()`. Send the request `GET /js/geolocate.js?callback=setCountryCookie` to Burp Repeater.
4. Observe that if you add duplicate `callback` parameters, only the final one is reflected in the response, but both are still keyed. However, if you append the second `callback` parameter to the `utm_content` parameter using a semicolon, it is excluded from the cache key and still overwrites the callback function in the response:

![](/static/img/Pasted_image_20231117170526.png)


5. Send the request again, but this time pass in `alert(1)` as the callback function:

![](/static/img/Pasted_image_20231117170637.png)

