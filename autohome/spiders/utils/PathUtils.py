import os


class PathUtils(object):

    @staticmethod
    def createDir(path):
        if not os.path.exists(path):
            os.mkdir(path)

    @staticmethod
    def initDir():
        path = PathUtils.getRootPath()
        PathUtils.createDir(path + '//output')
        PathUtils.createDir(path + '//output//1_originHtml')
        PathUtils.createDir(path + '//output//2_decodeJs')
        PathUtils.createDir(path + '//output//picture')

    @staticmethod
    def getRootPath():
        return os.path.abspath(os.path.join(os.getcwd(), "../../.."))


if __name__ == "__main__":
    print(PathUtils.getRootPath())
