----

### Lab Description

This lab contains a [stored cross-site scripting](https://portswigger.net/web-security/cross-site-scripting/stored) vulnerability in the comment functionality.

To solve this lab, submit a comment that calls the `alert` function when the blog post is viewed

### Lab Solution

- insert the payload  `<script>alert(1)</script>` at the comment box