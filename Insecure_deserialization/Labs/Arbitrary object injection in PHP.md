
1. Lab hint 
	1. You can sometimes read source code by appending a tilde (`~)` to a filename to retrieve an editor-generated backup file.
2. Looking at the source page we can find a HTML comment

![](/static/img/Pasted_image_20231123185912.png)

3. Append ~ to the file we can retrieve the "backup" of this file:

![](/static/img/Pasted_image_20231123185940.png)

4. Construct the following payload:

`O:14:"CustomTemplate":1:{s:14:"lock_file_path";s:23:"/home/carlos/morale.txt";}`

5. Concat with the session cookie

![](/static/img/Pasted_image_20231123191152.png)

6. Send the request again, but change the new session "crafted" cookie;

![](/static/img/Pasted_image_20231123191132.png)
