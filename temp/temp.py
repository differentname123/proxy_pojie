# -- coding: utf-8 --
""":authors:
    zhuxiaohu
:create_date:
    2022/12/21 16:04
:last_date:
    2022/12/21 16:04
:description:
    
"""



def fun():
    """
    程序入口
    :return:
    """
    passwordSetList = set()
    with open('temp1.txt') as lines:
        for line in lines:
            if len(line.strip()) < 6:
                continue
            passwordSetList.add(line.strip())

    with open("ok_pass.txt", 'w') as writer:
        for password in passwordSetList:
            writer.write("%s\n" % password)

    pass
if __name__ == "__main__":
    fun()
