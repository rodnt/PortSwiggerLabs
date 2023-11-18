

1. Observe that any changes to the query string are always reflected in the response. This indicates that the external cache includes this in the cache key. Use Param Miner to add a dynamic cache-buster query parameter. This will allow you to bypass the external cache.

![](/static/img/Pasted_image_20231118104104.png)

![](/static/img/Pasted_image_20231118104208.png)

![](/static/img/Pasted_image_20231118104408.png)

![](/static/img/Pasted_image_20231118104630.png)

2. Send the request. If you get lucky with your timing, you will notice that your exploit server URL is reflected three times in the response. However, most of the time, you will see that the URL for the canonical link element and the `analytics.js` import now both point to your exploit server, but the `geolocate.js` import URL remains the same.

![](/static/img/Pasted_image_20231118105444.png)


3. Go to the exploit server and create a file at `/js/geolocate.js` containing the payload `alert(document.cookie)`. Store the exploit.
4. Remove the `X-Forwarded-Host` header and resend the request. Notice that the internally cached fragment still reflects your exploit server URL, but the other two URLs do not. This indicates that the header is unkeyed by the internal cache but keyed by the external one. Therefore, you can poison the internally cached fragment using this header.

![](/static/img/Pasted_image_20231118105727.png)

![](/static/img/Pasted_image_20231118110952.png)

![](/static/img/Pasted_image_20231118110944.png)
