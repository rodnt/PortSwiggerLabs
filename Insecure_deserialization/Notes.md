
- **Serialization** is the process of converting complex data structures, such as objects and their fields, into a "flatter" format that can be sent and received as a sequential stream of bytes. Serializing data makes it much simpler to:
	- Write complex data to inter-process memory, a file, or a database
	- Send complex data, for example, over a network, between different components of an application, or in an API call

> Crucially, when serializing an object, its state is also persisted. In other words, the object's attributes are preserved, along with their assigned values.

**Deserialization** is the process of restoring this byte stream to a fully functional replica of the original object, in the exact state as when it was serialized. The website's logic can then interact with this deserialized object, just like it would with any other object.

> To prevent a field from being serialized, it must be explicitly marked as "transient" in the class declaration.

> Be aware that when working with different programming languages, serialization may be referred to as marshalling (Ruby) or pickling (Python). These terms are synonymous with "serialization" in this context.

> Insecure deserialization is when user-controllable data is deserialized by a website

- It is even possible to replace a serialized object with an object of an entirely different class


#### How to identify 


PHP uses a mostly human-readable string format, with letters representing the data type and numbers representing the length of each entry. For example, consider a `User` object with the attributes:

`$user->name = "carlos"; $user->isLoggedIn = true;`

When serialized, this object may look something like this:

`O:4:"User":2:{s:4:"name":s:6:"carlos"; s:10:"isLoggedIn":b:1;}`

This can be interpreted as follows:

- `O:4:"User"` - An object with the 4-character class name `"User"`
- `2` - the object has 2 attributes
- `s:4:"name"` - The key of the first attribute is the 4-character string `"name"`
- `s:6:"carlos"` - The value of the first attribute is the 6-character string `"carlos"`
- `s:10:"isLoggedIn"` - The key of the second attribute is the 10-character string `"isLoggedIn"`
- `b:1` - The value of the second attribute is the boolean value `true`

The native methods for PHP serialization are `serialize()` and `unserialize()`. If you have source code access, you should start by looking for `unserialize()` anywhere in the code and investigating further.


Java, objects always begin with the same bytes, which are encoded as `ac ed` in hexadecimal and `rO0` in Base64.


Any class that implements the interface `java.io.Serializable` can be serialized and deserialized. If you have source code access, take note of any code that uses the `readObject()` method, which is used to read and deserialize data from an `InputStream`.


##### How to exploit

 - As the object state is persisted, you can study the serialized data to identify and edit interesting attribute values. You can then pass the **malicious** object into the website via its deserialization process. This is the initial step for a basic deserialization exploit.
>
Broadly speaking, there are two approaches you can take when manipulating serialized objects. You can either edit the object directly in its byte stream form, or you can write a short script in the corresponding language to create and serialize the new object yourself. The latter approach is often easier when working with binary serialization formats.

#### Magic Methods


- Magic methods are a special subset of methods that you do not have to explicitly invoke. Instead, **they are invoked automatically whenever a particular event or scenario occurs**. Magic methods are a common feature of object-oriented programming in various languages. They are sometimes indicated by prefixing or surrounding the method name with double-underscores.

> Magic methods are widely used **and do not represent a vulnerability on their own**. But they can become dangerous when the code that they execute handles attacker-controllable data, for example, from a deserialized object. This can be exploited by an attacker to automatically invoke methods on the deserialized data when the corresponding conditions are met.


In Java deserialization, the same applies to the `ObjectInputStream.readObject()` method, which is used to read data from the initial byte stream and essentially acts like a constructor for "re-initializing" a serialized object. However, `Serializable` classes can also declare their own `readObject()` method as follows:

`private void readObject(ObjectInputStream in) throws IOException, ClassNotFoundException { // implementation }`

A `readObject()` method declared in exactly this way acts as a magic method that is invoked during deserialization. This allows the class to control the deserialization of its own fields more closely.

You should pay close attention to any classes that contain these types of magic methods. They allow you to pass data from a serialized object into the website's code before the object is fully deserialized. This is the starting point for creating more advanced exploits.


#### Gadget chains

> A "gadget" is a snippet of code that exists in the application that can help an attacker to achieve a particular goal.

> It is important to understand that, unlike some other types of exploit, a gadget chain is not a payload of chained methods constructed by the attacker.

All of the code **already exists on the website**. The only thing the attacker controls is the data that is passed into the gadget chain. This is typically done using a magic method that is invoked during deserialization, sometimes known as a "kick-off gadget".

> In the wild, many insecure deserialization vulnerabilities will only be exploitable through the use of gadget chains

###### Working with pre-built gadget chains

- Manually identifying gadget chains can be a fairly **arduous process**, and is almost impossible without source code access. Fortunately, there are a few options for working with pre-built gadget chains that you can try first.


#### ysoserial

One such tool for Java deserialization is "ysoserial". This lets you choose one of the provided gadget chains for a library that you think the target application is using, then pass in a command that you want to execute. It then creates an appropriate serialized object based on the selected chain. This still involves a certain amount of trial and error, but it is considerably less labor-intensive than constructing your own gadget chains manually.


In Java versions 16 and above, you need to set a series of command-line arguments for Java to run ysoserial. For example:

`java -jar ysoserial-all.jar \ --add-opens=java.xml/com.sun.org.apache.xalan.internal.xsltc.trax=ALL-UNNAMED \ --add-opens=java.xml/com.sun.org.apache.xalan.internal.xsltc.runtime=ALL-UNNAMED \ --add-opens=java.base/java.net=ALL-UNNAMED \ --add-opens=java.base/java.util=ALL-UNNAMED \ [payload] '[command]'`


