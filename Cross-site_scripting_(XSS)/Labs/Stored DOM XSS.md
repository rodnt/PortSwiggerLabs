----

### Lab Description

This lab demonstrates a stored DOM vulnerability in the blog comment functionality. To solve this lab, exploit this vulnerability to call the `alert()` function.

### Lab Solution

- Verify the `replace` function, only replace onetime

![](/static/img/Pasted_image_20230627091335.png)

- Set the payload `<><img src=1 onerror=alert(1)><

![](/static/img/Pasted_image_20230627091550.png)