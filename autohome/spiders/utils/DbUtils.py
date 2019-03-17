from pymongo import MongoClient
from scrapy.utils.project import get_project_settings


class DbUtils(object):

    def __init__(self, collectionName):
        # 获取setting.py信息
        settings = get_project_settings()
        host = settings.get('MONGO_IP')
        port = settings.get('MONGO_PORT')
        dataBase = settings.get('MONGO_DATABASE')
        # 连接mongoDb
        client = MongoClient(host=host, port=port)
        self.db = client[dataBase][collectionName]

    # 插入数据
    def insert(self, obj):
        return self.db.insert(obj)

    # 插入一条数据
    def insertOne(self, obj):
        return self.db.insert_one(obj)

    # 插入多条数据
    def insertMany(self, obj):
        return self.db.insert_many(obj)

    # 查询数据
    def select(self, obj):
        return self.db.find(obj)

    # 分页查询
    def selectByPage(self, obj, start, count):
        return self.db.find(obj).skip(start).limit(count)

    # 查询数据数量
    def selectCount(self, obj):
        return self.db.find(obj).count()

    # 删除数据
    def delete(self, obj):
        return self.db.remove(obj)

    # 更新数据
    def update(self, find, update):
        return self.db.update(find, update, False, True)


if __name__ == "__main__":
    dbUtil = DbUtils('test')
    # 插入测试
    dbUtil.insert({"_id": "3", "name": "banana"})
    dbUtil.insertOne({"_id": "0", "name": "root"})
    dbUtil.insertMany([{"_id": "1", "name": "wind"}, {"_id": "2", "name": "future"}])

    # 查询测试  pageList必须要访问才看得见数据
    pageList = dbUtil.select(None)
    pageInfo = dbUtil.selectByPage({}, 0, 20)
    count = dbUtil.selectCount(None)

    # 删除测试
    dbUtil.delete({"name": "root"})

    # 更新测试
    dbUtil.update({"name": "wind"}, {"$set": {"name": "apple"}})
