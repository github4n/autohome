import xlwt

from autohome.spiders.utils.DbUtils import DbUtils
from autohome.spiders.utils.PathUtils import PathUtils


class Excel(object):

    def __init__(self):
        self.workBook = xlwt.Workbook()
        self.workSheet = self.workBook.add_sheet('配置详情')
        self.rowNum = 1
        self.headerFlag = False

    # 生成表格头
    def createHeader(self, resultItem):
        if not self.headerFlag:
            colNum = 0
            for key in resultItem:
                self.workSheet.write(0, colNum, str(key))
                colNum = colNum + 1
        self.headerFlag = True

    # 生成内容
    def createContent(self, resultItem):
        length = len(list(resultItem.values())[0])
        for i in range(length):
            colNum = 0
            for key in resultItem:
                self.workSheet.write(self.rowNum, colNum, str(resultItem[key][i]))
                colNum = colNum + 1
            self.rowNum = self.rowNum + 1

    # 参数解析
    def resolveJson(self, originItem, resultItem):
        configItemList = originItem['config']
        optionItemList = originItem['option']
        bagItemList = originItem['bag']

        for configItem in configItemList:
            configItemData = configItem['paramitems']
            for car in configItemData:
                resultItem[car['name']] = []
                for item in car['valueitems']:
                    resultItem[car['name']].append(item['value'])

        for optionItem in optionItemList:
            optionItemData = optionItem['configitems']
            for car in optionItemData:
                resultItem[car['name']] = []
                for item in car['valueitems']:
                    resultItem[car['name']].append(item['value'])

        for bagItem in bagItemList:
            bagItemData = bagItem['bagitems']
            for car in bagItemData:
                resultItem[car['name']] = []
                for item in car['valueitems']:
                    resultItem[car['name']].append(item['value'])

    # 保存Excel
    def save(self):
        PathUtils.initDir()
        rootPath = PathUtils.getRootPath()
        self.workBook.save(rootPath + '/output/config/config_6_config.xlsx')

    # 生成Excel
    def generateExcel(self, resultList):
        for i in range(len(resultList)):
            resultItem = {}

            # 解析数据
            self.resolveJson(resultList[i], resultItem)

            # 生成表格头
            self.createHeader(resultItem)

            # 生成内容
            self.createContent(resultItem)

            # 保存Excel
            self.save()


if __name__ == "__main__":
    # 数据库操作
    dbUtils = DbUtils('config_6_config')
    queryItems = dbUtils.selectByPage(None, 0, 3)
    excel = Excel()
    excel.generateExcel(list(queryItems))
