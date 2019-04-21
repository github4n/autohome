# MongoDB常用命令



## 数据库操作

```mongoDb
//显示所有数据库
show databases

//指定数据库
use autohome

//查看当前数据库下collections
show collections  

//删除当前collection
db.collections.drop()

//查看当前在哪个数据库下
db.getName()

//删除当前数据库
db.dropDatabase()
```



## 查询

| 操作     | 格式                 |                    |
| -------- | -------------------- | ------------------ |
| 查询所有 | db.collection.find() | 没有参数就查询所有 |



### 条件查询

| 操作     | 示例                                     |
| -------- | ---------------------------------------- |
| 等于     | db.collection.find({“key”:value})        |
| 大于     | db.collection.find({“key”:{$gt:value}})  |
| 小于     | db.collection.find({“key”:{$lt:value}})  |
| 小于等于 | db.collection.find({“key”:{$lte:value}}) |
| 大于等于 | db.collection.find({“key”:{$gte:value}}) |
| 不等于   | db.collection.find({“key”:{$ne:value}})  |



### 逻辑查询

| 操作 | 格式                                           |
| ---- | ---------------------------------------------- |
| and  | db.collection.find({$and:[{条件一},{条件二}]}) |
| or   | db.collection.find({$or:[{条件一},{条件二}]})  |



### 排序

| 操作 | 格式                               | 解释     |
| ---- | ---------------------------------- | -------- |
| 升序 | db.collection.find().sort({id:1})  | 1是升序  |
| 降序 | db.collection.find().sort({id:-1}) | -1是降序 |



### 分页

| 操作 | 格式                                    | 解释                                       |
| ---- | --------------------------------------- | ------------------------------------------ |
| 分页 | db.collection.find().skip(10).limit(20) | 跳过前10个,查询后20    ==>   查10-30的数据 |



### 记录条数

| 操作     | 格式                         |
| -------- | ---------------------------- |
| 记录条数 | db.collection.find().count() |





## 插入

```JavaScript
//插入
db.collection.insert()
```



## 修改

```JavaScript
//修改单条
db.collection.update({条件}，{$set:{新数据}})
//修改多条
db.collection.update({条件}，{$set:{新数据}}，{multi:true})
```



## 删除

```javascript
//删除
db.collection.remove({条件})
```