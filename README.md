# 项目介绍
### 项目文档 []([https://markdown.com.cn](https://28-zu.gitbook.io/shu-ju-jie-gou-ke-cheng-she-ji-28-zu-xiang-mu-wen-dang))
### 开发技术栈选项

后端/数据库/前端

* `Java Spring Boot/MongoDB/React`
* `Python/Folium/Leaflet.js` /`ChatGPT 3.5`

### 版本管理选项

* Git/GitHub
* QQ群

### 地图数据集获取选项

* `OpenStreetMap` 自动导出各景区`.osm`文件（地图数据），使用解析程序转换为符合要求的数据结构进行存储使用。此方案中建筑物，道路及服务设施均与现实一致。

### 程序结构

#### 模块一 主界面

程序主界面，提供各子模块的启动入口，并对该系统大体功能进行展示。

#### 模块二 游学项目初步规划

为当前用户按需求新建一个游学项目，提供一个类似于”工作台“样式的规划模块规划游学路线，指定该服务覆盖的游学景点后可添加的游学途径地点（_两级地点均可根据热度推荐_），游学开始时间以及相关备注。并在规划完成后生成一份游学计划，其中包含各地点和浏览路线，用户可在模块五中查看该计划。

#### 模块三 游学项目管理

当前用户可管理已创建的游学项目，进行增删改查操作。

#### 模块四 游学计划查看

可根据用户已生成的游学计划对用户进行展示。用户可查看计划中各景点内部的情况，软件会给出景点内部的示意图，列出当前浏览计划的途径地点，建议浏览路线（_实现要求中的最短时间以及最短距离策略_）。同时，在选定一个浏览地点后，用户可以使用”搜周边“功能，选择该浏览地点周边用户也可将该地点一键添加到当前规划中。

#### 模块五 游学日记编辑

用户可从已生成的计划中新建一篇游记，图文编辑可使用第三方方案，例如`Markdown`。游记可与已创建的行程进行关联。创建完成后，用户还可以对游记在平台内共享，导出PDF文件等。

#### 模块六 游学日记社区

该模块为社区功能。用户可查看自己已创建的游记，也可查看平台内其他用户选择共享的游记，可以对其他用户的游记进行评价。社区内，对各篇游记的热度进行排序，用户可选择不同排序策略。（\*PPT中游学日记管理功能）

### 开发计划

* 第五周-中期检查后：完成程序后端模块一至四的开发工作，并开发一个简易前端平台进行展示。
* 中期检查-验收：完成模块五六的前后端开发工作，设计前端页面，完善UI/UX设计，Bug Fix。

### 任务分配

| 任务编号 | 任务                  |
| ---- | ------------------- |
| 1    | 数据对象定义及接口定义         |
| 2    | 地图数据获取，解析程序编写       |
| 3    | 推荐算法相关接口实现          |
| 4    | 地图规划功能相关接口实现        |
| 5    | Spring Boot框架、数据库接入 |
| 6    | 简易前端界面设计            |
