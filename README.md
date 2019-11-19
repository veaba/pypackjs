# 基于Python 版本 Node平台前端项目打包器

> 这是一个概念性项目，目前作为tensorflow-docs项目的衍生性项目，诞生的原因是vuepress 打包2.5k的markdown文件需要花费3个小时，这一点无法忍受，而webpack是js平台的

如果使用js生态，通过py多线程的方式会更加好一点吧，类似 分布式构建

## 充电中。。
- 【 :battery:充电中：项目暂停：】需要补充下python 的class 概念，否则很难下去~~~
    - 静态方法
    - 静态属性
    - 公用方法
    - 公用属性
    - classMethod
    - staticMethod
    - 类继承
    - 类的方法调用其他类的方法
    - 类的方法调用私有方法
- 【 :battery:充电中：项目暂停：】补充markdown-it 等源码原理


- python是可以调用js平台的一些资源
- python将使用线程池来加快处理（虽然有些吃内存）
- 本项目的理论基础是：对于文件处理来说，万物皆正则(不就是替换的事情嘛))

|进度|pypackjs包名|描述|原理|
|----|----|----|----|
||pypackjs-vue|构建vue项目的依赖关系||
||pypackjs-comporess|压缩js文件和格式化文件|主要是正则格式化|
||pypackjs-vnode|html转js的vnode||
||pypackjs-css|css打包工具||
|进行中...|pypackjs-markdown|markdown转HTML文件、或者markdown直接转AST语法树||
||pypackjs-url|url路径解析工具||
||pypackjs-file|处理文件的依赖||
||pypackjs-ts|处理ts||
||pypackjs-scss|处理scss文件||
|||||


- 本来是markdown->HTML->VNODE、但如果markdown->VNODE应该会很少省事
- 额额额额，我的老天鹅，搞一个模块就要翻写好几个别的依赖模块！！！
- 现在我要用python重写markdown-it(我感觉这个项目可以做十年了)，尽量偷工减料下完成吧！！有点难了

## 参考重点项目
- [webpack.js](https://github.com/webpack/webpack) JS打包工具
- [markdown-it](https://github.com/markdown-it/markdown-it) 一款markdown 格式转为HTML
- [highlight.js](https://github.com/highlightjs/highlight.js) 一款高亮代码
- [astexplore](https://github.com/fkling/astexplorer) 一个集成多个编程语言或者格式转为其他格式AST的web工具集项目 [A web ast tool：AST explore ](https://astexplorer.net/)
- [html2text](https://github.com/aaronsw/html2text) 一个Python版本的HTML转markdown工具
- [prettier](https://prettier.io/) code format

## markdown-it 项目递归结构


- markdown-it
    - linkify-it
        - ucMicro 完成！ pypack-ucMicro
