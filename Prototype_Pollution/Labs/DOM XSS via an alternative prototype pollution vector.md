
1. Search the sinks with DOM invader extension;
2. Scan for gadgets;
3. Verify that the JavaScript is vulnerable;

![](/static/img/Pasted_image_20231202084816.png)
4. But, when you click on exploit, the exploit will failed because of the numeric sequence;
5. Go back to the previous browser tab and look at the `eval()` sink again in DOM Invader. Notice that following the closing canary string, a numeric `1` character has been appended to the payload.
    
6 Click **Exploit** again. In the new tab that loads, append a minus character (`-`) to the URL and reload the page.
    
7. Observe that the `alert(1)` is called and the lab is solved.

![](/static/img/Pasted_image_20231202084917.png)

