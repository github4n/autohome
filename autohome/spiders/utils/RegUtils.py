class Reg(object):
    # QQ号校验
    QQ = '^[1-9][0-9]{4,10}$'
    # 微信号校验
    weChat = '^[a-zA-Z][a-zA-Z0-9_-]{5,19}$'
    # 邮箱校验
    email = '^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(.[a-zA-Z0-9-]+)*.[a-zA-Z0-9]{2,6}$'
    # 手机号校验
    cellPhone = '^1[3456789][0-9]{9}$'
    # 固定电话校验
    fixedPhone = '^0[0-9]{2}-[0-9]{8}$|^0[0-9]{3}-[0-9]{7}$'


if __name__ == "__main__":
    print(Reg.QQ)
