
1. Use param miner extension to exploit, to scan some possibilities;
2. Param miner will find 2 possibilities `X-Forwarded-Host` and `X-Original-URL`
![](/static/img/Pasted_image_20231116154834.png)
3. Verify that `data.host` are being used inside a JavaScript that is concat with translations.json

![](/static/img/Pasted_image_20231116155207.png)

4. Add to exploit server the following payload

![](/static/img/Pasted_image_20231116155318.png)

5. Search for the request that have the localized=1 query param. And set your exploit server at `X-Forwarded-Host` header

![](/static/img/Pasted_image_20231116155636.png)

6. Now, we need to chain this exploit with users from En. First, verify that `X-Original-Url` can be used to exploit that lab:

```
X-Original-Url: /setlang\es
```

![](/static/img/Pasted_image_20231116160257.png)

7. Now we need to cache the two pages (2 repeater tabs)


![](/static/img/Pasted_image_20231116162305.png)


![](/static/img/Pasted_image_20231116162318.png)

![](/static/img/Pasted_image_20231116162241.png)