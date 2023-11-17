
1. Add arbitrary query parameters to the request. Observe that you can still get a cache hit even if you change the query parameters. This indicates that they are not included in the cache key.
2. Add origin header to the request and observe that the X-Cache now got miss

![](/static/img/Pasted_image_20231117115835.png)

3. Notice that when you add parameter at URL with Origin header you can inject data

![](/static/img/Pasted_image_20231117120206.png)

4. Insert your malicous payload and keep request until you get X-Cache: Hit

![](/static/img/Pasted_image_20231117120603.png)

5.  Remove the cache-buster `Origin` header and add your payload back to the query string. Replay the request until you have poisoned the cache for normal users. Confirm this attack has been successful by loading the home page in the browser and observing the popup.

![](/static/img/Pasted_image_20231117121435.png)


![](/static/img/Pasted_image_20231117121452.png)

