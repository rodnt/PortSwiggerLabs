1. Log in with peter crendentials;
2. Try to access the admin path;

![](/static/img/Pasted_image_20231202122933.png)

3. Verify the JWT token and try to crack them;

![](/static/img/Pasted_image_20231202123407.png)

4. We need to Generate a forged signing key

	1. Go to JWT Editor tool;
	2. Generate a new  symmetric key;
	3. Change the `k` value with the value from `secret1`  but with base64;
		![](/static/img/Pasted_image_20231202123824.png)
	
		![](/static/img/Pasted_image_20231202124029.png)
> Note you can use, other methods like the site jwt.io and paste the secret1 key inside the signature

4. Just delete carlos user;
![](/static/img/Pasted_image_20231202124334.png)

![](/static/img/Pasted_image_20231202124408.png)

