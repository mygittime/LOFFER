---
layout: post
title: script async vs defer
date: 2020-07-19
Author: 来自中世界
tags: [javascript]
comments: true
---
图解 **script** 标签 **async** 和 **defer** 属性

### Legend

![legend](https://mygittime.github.io/myblog/images/async-vs-defer/legend.png)

### \<script>

**script** 会中断HTML文件解析，直到script文件下载并解析完成

![script](https://mygittime.github.io/myblog/images/async-vs-defer/script.png)

### \<script async>

**async** 在HTML解析期间下载文件，并在完成下载后暂停HTML解析器以执行该文件

![script-async](https://mygittime.github.io/myblog/images/async-vs-defer/script-async.png)

### \<script defer>

**defer** 在HTML解析期间下载文件，并且仅在解析器完成后执行。defer还保证脚本按照它们在文档中出现的顺序执行（实际上多个defer时不能保证执行顺序）

![script-defer](https://mygittime.github.io/myblog/images/async-vs-defer/script-defer.png)

