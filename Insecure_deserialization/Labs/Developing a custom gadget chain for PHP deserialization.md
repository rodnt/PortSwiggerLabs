
1. Login into a application and verify the following PHP serialized object;

![](Pasted_image_20231210212134.png)

![](Pasted_image_20231210212203.png)

2. Verify the following HTML comment;

![](Pasted_image_20231210212307.png)

3.  Access the following endpoint with the ~ at the end of the endpoint;

![](Pasted_image_20231210212404.png)


4. Develop the following exploit;

1. You can exploit this gadget chain to invoke `exec(rm /home/carlos/morale.txt)` by passing in a `CustomTemplate` object where:
    
    `CustomTemplate->default_desc_type = "rm /home/carlos/morale.txt"; CustomTemplate->desc = DefaultMap; DefaultMap->callback = "exec"`
    
    If you follow the data flow in the source code, you will notice that this causes the `Product` constructor to try and fetch the `default_desc_type` from the `DefaultMap` object. As it doesn't have this attribute, the `__get()` method will invoke the callback `exec()` method on the `default_desc_type`, which is set to our shell command.



![](Pasted_image_20231210212715.png)