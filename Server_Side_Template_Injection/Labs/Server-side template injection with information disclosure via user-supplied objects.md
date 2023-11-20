
1. Login into the lab with the credentials from the lab;
2. Edit the template from the lab;

![](/static/img/Pasted_image_20231120112432.png)

3. Add the following payload:
`<strong> hi {% debug %} </strong>`

![](/static/img/Pasted_image_20231120112529.png)

4. Verify that is a django framework
5. Use the following payload to get the secret key

`{{settings.SECRET_KEY}}`

![](/static/img/Pasted_image_20231120112649.png)

![](/static/img/Pasted_image_20231120112659.png)