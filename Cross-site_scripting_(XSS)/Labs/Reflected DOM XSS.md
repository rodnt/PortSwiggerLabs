----

### Lab description

This lab demonstrates a reflected DOM vulnerability. Reflected DOM vulnerabilities occur when the server-side application processes data from a request and echoes the data in the response. A script on the page then processes the reflected data in an unsafe way, ultimately writing it to a dangerous sink.

To solve this lab, create an injection that calls the `alert()` function.


### Lab Solution

- Using the burp extension dom invader, copy the canary and paste on the search
![](/static/img/Pasted_image_20230627085202.png)

- Insert the payload `\"-alert(1)}//` inside the search box

![](/static/img/Pasted_image_20230627090048.png)