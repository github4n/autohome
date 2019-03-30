import xlwt

from autohome.spiders.utils.DbUtils import DbUtils
from autohome.spiders.utils.PathUtils import PathUtils


class ExcelUtils(object):

    # 创建表头
    def createHeader(self, workSheet, itemDict):
        i = 0
        for (key, value) in itemDict.items():
            workSheet.write(0, i, str(key))
            i = i + 1

    # 生成内容
    def createContent(self, workSheet, resultList):
        for i in range(len(resultList)):
            j = 0
            for (key, value) in resultList[i].items():
                workSheet.write(i + 1, j, str(value))
                j = j + 1

    # 生成Excel
    def generateExcel(self, folderName, sheetName, resultList):
        workBook = xlwt.Workbook()
        workSheet = workBook.add_sheet(sheetName)

        # 创建表头
        self.createHeader(workSheet, resultList[0])

        # 生成内容
        self.createContent(workSheet, resultList)

        # 设置列宽
        self.setColumnWidth(workSheet, resultList)

        # 保存文件
        self.save(workBook, folderName, sheetName)

    # 保存Excel
    def save(self, workBook, folderName, sheetName):
        PathUtils.initDir()
        rootPath = PathUtils.getRootPath()
        workBook.save(rootPath + '/output/%s/%s.xlsx' % (folderName, sheetName))

    # 字符串长度
    def strLen(self, value):
        return len(value.encode('utf-8'))

    # 设置列宽
    def setColumnWidth(self, workSheet, resultList):
        for i in range(len(resultList[0].items())):
            # 使用表头的长度来初始化
            columnWidth = self.strLen((list(resultList[0].keys()))[i])
            # 获取一列数据
            columnList = self.getColumnList(resultList, i)
            # 获取该列数据中最大长度
            for j in range(len(columnList)):
                currentWidth = self.strLen(str(columnList[j]))
                columnWidth = self.getMax(columnWidth, currentWidth)
            # 设置该列的宽度
            if columnWidth > 10:
                workSheet.col(i).width = 256 * (columnWidth + 1)

    # 获取一列数据
    def getColumnList(self, resultList, i):
        columnList = []
        for k in range(len(resultList)):
            columnList.append((list(resultList[k].values()))[i])
        return columnList

    # 获取最大值
    def getMax(self, a, b):
        if a > b:
            return a
        return b


if __name__ == "__main__":
    dbUtils = DbUtils('3_series')
    queryItems = dbUtils.select(None)
    excelUtils = ExcelUtils()
    excelUtils.generateExcel('config', '3_series', list(queryItems))
