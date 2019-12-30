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

## 构想

尝试迁移前端项目到Python平台。

当然node也是可以调用子线程来处理的。

如果将node 这一套打包机制迁移到多线程的编程语言平台上，会不会很快呢？

因为对于前端打包机制不太清楚，但理论上应该是：

1. 根据文件构建关系
2. 构建内联和引用
3. 根据html结构生成语法树，然后给vue 的SPA应用使用的
4. vuepress 通过一些工具类（本质上也就是正则的方式）将markdown文件翻译为HTML文件

我的构想是，python其实可以调用js平台处理一些事情，这样是可以配合webpack打包机制+python 多线程（之前享受过线程池带来的快感）来处理文件的转化，速度会不会更快呢？

而重点是:
1. vuepress 项目文件关系如何连接
2. 怎么将md文件转为html文件
3. html转为语法树的js文件

工作内容（几乎要翻写一个webpack了）：

- style load
- sass load
- styl load
- scss load
- ts load
- vue load，打包vue项目
- url load
- file load
- markdown-load >
    - markdown-html
- html->AST
- js-load 解析js文件,但也是可以调用JS引擎做一些事情
- v-node load
- python 版本的js压缩工具  

分析了一波，所以需要看一下vuepres 的核心源码是怎么做的，并迁移到python平台

### 目前第一大步骤：build js项目

