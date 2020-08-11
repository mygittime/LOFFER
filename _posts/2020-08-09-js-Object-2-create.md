---
layout: post
title: 理解对象-创建对象的多种模式
date: 2020-07-24
Author: 来自中世界
tags: [javascript Object]
comments: true
---

### 创建对象的方式

1. 工程模式
2. 构造函数模式
3. 原型模式
4. 组合使用构造函数模式和原型模式
5. 动态原型模式
6. 寄生构造函数模式
7. 稳妥构造函数模式

#### 一、工厂模式

将创建对象的逻辑封装到一个函数中。使用时只需要按照规则进行调用，不需要了解内部逻辑

    var createPerson = function(name, age, job){
        var o = new Object();
        o.name = name;
        o.age = age;
        o.job = o.job;
        o.sayName = function(){
            console.log(this.name);
        }
        return o;
    }

    var person1 = createPerson('xiaohong', 20, 'student');
    var person2 = createPerson('xiaoming', 26, 'driver');

优点：解决了创建多个相似对象的问题

缺点：没有解决对象识别的问题（怎样知道一个对象的类型，不明白的话看构造函数）

#### 二、构造函数模式

    function Person(name, age, job){
        this.name = name;
        this.age = age;
        this.job = job;
        this.sayName = function(){
            console.log(this.name);
        }
    }

    var person1 = new Person('xiaohong', 20, 'student');
    var person2 = new Person('xiaoming', 26, 'driver');

    console.log(person1.constructor === Person) //true
    console.log(person2.constructor === Person) //true

    console.log(person1 instanceof Person) //true
    console.log(person2 instanceof Person) //true

    console.log(person1.sayName === person2.sayName) //false


对象都有一个 **constructor** 属性，构造函数创建的对象 **constructor** 属性指向 **Person**，用instanceof来检测可以得到同样的结果。这就是解决了工厂模式无法识别对象的问题

构造函数首字母要大写（约定俗称）,使用时必须使用new，实际上和 **var person1 = new Object()** 长不多，实际步骤会多一些

1. 创建一个新对象
2. 将构造函数作用域赋给新的对象
3. 执行构造函数中的代码
4. 返回新对象

优点：解决了工厂模式无法识别对象的问题

缺点：构造函数中的方法每次调用都需要重新创建(person1和person2中的sayName方法不是同一个)，虽然可以通过将函数定义在外部来解决，但是也破坏了封装性，同时也让全局函数名不副实（只被某个对象调用）

#### 原型模式

每个构造函数都有一个 **prototype** 属性，这个属性是一个指针，指向一个对象。这个对象的用途是包含这个函数所有实例可以共享的属性和方法，也就是说可以把构造函数中需要共享的属性和方法都放入 **prototype** 中

    function Person(){}
    Person.prototype.name = "xiaoming";
    Person.prototype.sayName = function(){
        console.log(this.name)
    }

    let person1 = new Person();
    let person2 = new Person();
    person1.sayName() //xiaoming

    console.log(person1.sayName === person2.sayName) //true

每个实例也有 **prototype** 属性，但是只能用 **\_\_proto__** 来进行访问，实例的 **prototype** 指向的是构造函数的 **prototype** 

    console.log(Person.prototype === person2.__proto__) //true

每次查找属性时会先在实例中进行查找，查找不到时会沿着  **prototype** 向上继续查找，这就是原型链。如 **person1.sayName()** 会经历两次查找，第一次在person1中未找到，第二次在 **person1.\_\_proto__** 中查找成功。根据这个规则，可以通过在实例中重写某个属性来屏蔽原型属性（不会对原型属性做修改）

    function Person(){}
    Person.prototype.name = "xiaoming";
    Person.prototype.sayName = function(){
        console.log(this.name)
    }

    let person1 = new Person();
    let person2 = new Person();
    
    person1.name = "change";
    console.log(person1.name); //change
    console.log(person2.name); //xiaoming

**获取属性:**

1. in操作符：枚举实例中和原型中的所有属性
2. hasOwnProperty():检测属性是否存在实例中
3. Object.keys()：枚举实例上所有可枚举属性

公共部分：

    function Person(){}
    Person.prototype.name = "xiaoming";
    Person.prototype.sayName = function(){
        console.log(this.name)
    }

    let person1 = new Person();
    let person2 = new Person();

    person1.name = "change";

1.in操作符

    console.log('name' in person1); //true
    console.log('name' in person2); //true

2.hasOwnProperty()

    console.log(person1.hasOwnProperty('name)); //true 存在实例中
    console.log(person2.hasOwnProperty('name)); //false 不存在实例中

3.Object.keys()

    console.log(Object.keys(person1)) //['name']
    console.log(Object.keys(person2)) //[]
    console.log(Object.keys(Person.prototype)) //['name', 'sayName']

**简化原型语法**

    function Person(){}
    Person.prototype = {
        name:"xiaoming",
        sayName:function(){
            console.log(this.name);
        }
    }

此时Person的constructor指向的是Object，按需求将他再指向Person即可

优点：解决了构造函数内部方法需要重复创建的问题
缺点：1.无法传递参数、2.对于引用类型的值不方便处理。例如下面这个例子

    function Person(){}
    Person.prototype = {
        constructor:Person,
        name:"xiaoming",
        friends:['xiaobai','xiaohei']
    }

    var person1 = new Person();
    var person2 = new Person();

    person2.name = 'xiaobai';
    person1.friends.push('xiaohong')

    console.log(person1.friends) //['xiaobai', 'xiaohei', 'xiaohong']
    console.log(person2.friends) //['xiaobai', 'xiaohei', 'xiaohong']

#### 组合使用构造函数模式和原型模式

该模式融合了构造函数模式和原型模式的优点，是目前使用最广泛的一种模式

    function Person(name, age){
        this.name = name;
        this.age = age;
    }
    Person.prototype = {
        constructor:Person,
        sayName:function(){
            console.log(this.name)
        }
    }
    let person1 = new Person('xiaobai', 21);
    let person2 = new Person('xiaohei', 20);

    person1.sayName() //xiaobai
    person1.sayName() //xiaohei

    console.log(person1.sayName === person2.sayName); //true

#### 动态原型模式

组合使用构造函数模式和原型模式的升级版，封装性更好

    function Person(name, age){
        this.name = name;
        this.age = age;
        if(typeof this.sayName != 'function'){
            Person.prototype.sayName = function(){
                console.log(this.name)
            }
        }
    }

#### 寄生构造函数模式


#### 稳妥构造函数模式

没有公共属性，也不引用this的对象。适用于一些安全环境（环境中禁止使用this和new），或者防止数据被其他应用程序改动

    function Person(name){
        var o = new Object();
        o.sayName = function(){
            console.log(name)
        }
        return o;
    }
    var person1 = new Person('xiaoming');
    person1.sayName(); //xiaoming

这个函数的name属性不会被任何程序修改，同时只有调用sayName()方法才能访问name属性