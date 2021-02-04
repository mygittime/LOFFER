---
layout: post
title: 学习Promise
date: 2021-02-04
Author: 来自中世界
tags: [javascript]
comments: true
---

### 实现promise

promise[文档](https://www.runoob.com/w3cnote/javascript-promise-object.html)

1.根据文档可知，promise有三种状态：pending、fulfilled、rejected。和一个then方法

    const PENDING = "pending";
    const FULFILLED = "fulfilled";
    const REJECTED = "rejected";

    class myPromise{
        constructor(func){
            this.status = PENDING; //状态
            this.successData = null; //成功的信息
            this.failData = null; //失败的信息

            func(this.resolve, this.reject);
        }
        resolve = (data) => {
            if(this.status != PENDING) return;
            this.status = FULFILLED; //修改状态为成功
            this.successData = data; //成功的信息
        }
        reject = (data) => {
            if(this.status != PENDING) return;
            this.status = REJECTED; //修改状态为失败
            this.failData = data; //失败的信息
        }
        then = (successFunc, failFunc) => {
            if(this.status == FULFILLED){
                successFunc(this.successData);
            }else if(this.status == REJECTED){
                failFunc(this.failData);
            }
        }
    }

    new myPromise((resolve, reject) => {
        resolve('success')
    }).then(resp=>{
        console.log(resp); //success
    })

2.promise的架构已确定，下面添加异步逻辑。需要添加变量缓存成功和失败的回调函数

    const PENDING = "pending";
    const FULFILLED = "fulfilled";
    const REJECTED = "rejected";

    class myPromise{
        constructor(func){
            this.status = PENDING; //状态
            this.successData = null; //成功的信息
            this.failData = null; //失败的信息

            this.successFunc = null; //成功后的回调函数
            this.failFunc = null; //失败后的回调函数

            func(this.resolve, this.reject);
        }
        resolve = (data) => {
            if(this.status != PENDING) return;
            this.status = FULFILLED; //修改状态为成功
            this.successData = data; //成功的信息

            this.successFunc && this.successFunc(data); //异步调用
        }
        reject = (data) => {
            if(this.status != PENDING) return;
            this.status = REJECTED; //修改状态为失败
            this.failData = data; //失败的信息

            this.failFunc && this.failFunc(data); //异步调用
        }
        then = (successFunc, failFunc) => {
            if(this.status == FULFILLED){ //同步调用
                successFunc(this.successData);
            }else if(this.status == REJECTED){ //同步调用
                failFunc(this.failData);
            }else{
                //缓存回调函数
                this.successFunc = successFunc;
                this.failFunc = failFunc;
            }
        }
    }

    new myPromise((resolve, reject) => {
        setTimeout(() => {
            resolve('success')
        })
    }).then(resp=>{
        console.log(resp); //success
    })

3.还差一步，then方法可以被多次调用。then函数返回一个新的promise

    const PENDING = "pending";
    const FULFILLED = "fulfilled";
    const REJECTED = "rejected";

    class myPromise{
        constructor(func){
            this.status = PENDING; //状态
            this.successData = null; //成功的信息
            this.failData = null; //失败的信息

            this.successFunc = null; //成功后的回调函数
            this.failFunc = null; //失败后的回调函数

            func(this.resolve, this.reject);
        }
        resolve = (data) => {
            if(this.status != PENDING) return;
            this.status = FULFILLED; //修改状态为成功
            this.successData = data; //成功的信息

            this.successFunc && this.successFunc(data); //异步调用
        }
        reject = (data) => {
            if(this.status != PENDING) return;
            this.status = REJECTED; //修改状态为失败
            this.failData = data; //失败的信息

            this.failFunc && this.failFunc(data); //异步调用
        }
        then = (successFunc, failFunc) => {
            return new myPromise((resolve, reject) => {
                if(this.status == FULFILLED){ //同步调用
                    let promise = successFunc(this.successData);
                    isPromise(promise, resolve, reject);
                }else if(this.status == REJECTED){ //同步调用
                    failFunc(this.failData);
                }else{
                    //缓存回调函数
                    this.successFunc = successFunc;
                    this.failFunc = failFunc;
                }
            })
        }
    }
    function isPromise(p, resolve, reject){
        if(p instanceof myPromise){
            //如果调用的then返回一个新的promise
            p.then(resolve, reject);
        }else{
            //如果调用的then返回的不是promise
            resolve();
        }
    }

    new myPromise((resolve, reject) => {
        resolve('success')
    }).then(resp=>{
        console.log(resp); //success
        return new myPromise(resolve => {
            resolve('success2')
        })
    }).then( resp => {
        console.log(resp); //success2
    })

4.上一步实现了then可以被多次调用，但是多次调用时异步处理会失效。

    const PENDING = "pending";
    const FULFILLED = "fulfilled";
    const REJECTED = "rejected";

    class myPromise{
        constructor(func){
            this.status = PENDING; //状态
            this.successData = null; //成功的信息
            this.failData = null; //失败的信息

            this.successFunc = null; //成功后的回调函数
            this.failFunc = null; //失败后的回调函数

            func(this.resolve, this.reject);
        }
        resolve = (data) => {
            if(this.status != PENDING) return;
            this.status = FULFILLED; //修改状态为成功
            this.successData = data; //成功的信息

            this.successFunc && this.successFunc(); //异步调用
        }
        reject = (data) => {
            if(this.status != PENDING) return;
            this.status = REJECTED; //修改状态为失败
            this.failData = data; //失败的信息

            this.failFunc && this.failFunc(); //异步调用
        }
        then = (successFunc, failFunc) => {
            return new myPromise((resolve, reject) => {
                if(this.status == FULFILLED){ //同步调用
                    let promise = successFunc(this.successData);
                    isPromise(promise, resolve, reject);
                }else if(this.status == REJECTED){ //同步调用
                    failFunc(this.failData);
                }else{
                    //缓存回调函数--修改缓存的异步调用函数
                    this.successFunc = ()=>{
                        setTimeout(()=>{
                            let promise = successFunc(this.successData);
                            isPromise(promise, resolve, reject);
                        })
                    };
                    this.failFunc = ()=>{
                        setTimeout(()=>{
                            let promise = failFunc(this.failData);
                            isPromise(promise, resolve, reject);
                        })
                    }
                }
            })
        }
    }
    function isPromise(p, resolve, reject){
        if(p instanceof myPromise){
            //如果调用的then返回一个新的promise
            p.then(resolve, reject);
        }else{
            //如果调用的then返回的不是promise
            resolve();
        }
    }

    new myPromise((resolve, reject) => {
        setTimeout(()=>{
            resolve('success');
        },1000)
    }).then(resp=>{
        console.log(resp); //success
        return new myPromise(resolve => {
            resolve('success2')
        })
    }).then( resp => {
        console.log(resp); //success2
    })