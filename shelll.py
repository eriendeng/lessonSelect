#coding: utf-8

from PIL import Image
import requests
import json
import os
import msvcrt

def start():
    session = requests.session()
    login(session)
    shell_loop(session)

def shell_loop(session):
    print("\n")
    commond = input("    请选择<选课 || 退选>:")
    print("\n")
    if commond =="选课":
        selectDo(session)
    elif commond =="退选":
        selectUndo(session)
    #elif commond == "查课表":
        #r = session.get("http://222.200.98.147/xsgrkbcx!xsAllKbList.action?xnxqdm=201702")
    else:
        print("  ————————————")
        print("  |     请正确输入！     |")
        print("  ————————————")
    shell_loop(session)

def getVerifyCode(session):
    r = session.get("http://222.200.98.147/yzm?d=")
    with open("verifyCode.png","wb") as p:
        p.write(r.content)
        p.close()
    img = Image.open('verifyCode.png')
    return img.show()

def pwd_input():
    chars = []
    msvcrt.putch(" ".encode(encoding="utf-8"))
    msvcrt.putch(" ".encode(encoding="utf-8"))
    msvcrt.putch(" ".encode(encoding="utf-8"))
    msvcrt.putch(" ".encode(encoding="utf-8"))
    msvcrt.putch("p".encode(encoding="utf-8"))
    msvcrt.putch("a".encode(encoding="utf-8"))
    msvcrt.putch("s".encode(encoding="utf-8"))
    msvcrt.putch("s".encode(encoding="utf-8"))
    msvcrt.putch("w".encode(encoding="utf-8"))
    msvcrt.putch("o".encode(encoding="utf-8"))
    msvcrt.putch("r".encode(encoding="utf-8"))
    msvcrt.putch("d".encode(encoding="utf-8"))
    msvcrt.putch(":".encode(encoding="utf-8"))
    while True:
        try:
            newChar = msvcrt.getch().decode(encoding="utf-8")
        except:
            return input("你很可能不是在cmd命令行下运行，密码输入将不能隐藏:")
        if newChar in '\r\n': # 如果是换行，则输入结束
             msvcrt.putch("\n".encode(encoding="utf-8"))
             break
        elif newChar == '\b': # 如果是退格，则删除密码末尾一位并且删除一个星号
             if chars:
                 del chars[-1]
                 msvcrt.putch('\b'.encode(encoding='utf-8')) # 光标回退一格
                 msvcrt.putch( ' '.encode(encoding='utf-8')) # 输出一个空格覆盖原来的星号
                 msvcrt.putch('\b'.encode(encoding='utf-8')) # 光标回退一格准备接受新的输入
        else:
            chars.append(newChar)
            msvcrt.putch('*'.encode(encoding='utf-8')) # 显示为星号
    return (''.join(chars) )

def login(session):
    print("\n")
    print("  ————————————")
    print("  |       开始登录       |")
    print("  ————————————")
    account = input("    account:")
    password = pwd_input()
    getVerifyCode(session)
    code = input("    verifycode:")
    r = session.post("http://222.200.98.147/new/login?account=%s&pwd=%s&verifycode=%s"%(account,password,code))
    if "登录成功" in r.content.decode("utf-8"):
        print("  ————————————")
        print("  |       登录成功       |")
        print("  ————————————")
    else:
        print("  ————————————")
        print("  |   登录失败，请重试   |")
        print("  ————————————")
        login(session)

def selectUndo(session):
    # 已选课程
    r = session.post("http://222.200.98.147/xsxklist!getXzkcList.action")
    jsonObj = json.loads(r.content.decode("utf-8"))
    print("  ————————————")
    print("  | 您已经选择的课程有： |")
    print("  ————————————")
    dm = []
    i = 1
    for item in jsonObj:
        print("    " + str(i) + ". " + item["kcmc"] + " " + "课程形式:" + item["xmmc"])
        dm.append(item)
    kcrwdm = int(input("\n  请输入你要退选的课程编号:"))
    if (kcrwdm >0)&(kcrwdm<=len(dm)) :
        r = session.post("http://222.200.98.147/xsxklist!getCancel.action?jxbdm=%s&kcrwdm=%s&kcmc=%s"%(dm[kcrwdm-1]["jxbdm"],dm[kcrwdm-1]["kcrwdm"],dm[kcrwdm-1]["kcmc"]))
        if r.content.decode("utf-8") == "1" :
            print("  ————————————")
            print("  |       退选成功       |")
            print("  ————————————")
        elif r.content.decode("utf-8") == 0:
            print("  ————————————")
            print("  |       已经退选       |")
            print("  ————————————")
    else:
        print("  ————————————")
        print("  |     请正确输入！     |")
        print("  ————————————")

def selectDo(session):
    #可选列表
    r = session.post("http://222.200.98.147/xsxklist!getDataList.action")
    jsonObj = json.loads(r.content.decode("utf-8"))
    print("  ————————————")
    print("  | 您可以选择的课程有： |")
    print("  ————————————")
    dm = []
    i = 1
    for item in jsonObj["rows"]:
        print("    "+ str(i) + ". " + item["kcmc"] + " " + "课程形式:" + item["xmmc"])
        dm.append(item)
        i += 1
    kcrwdm = int(input("\n    请输入你要选择的课程编号:"))
    if (kcrwdm > 0) & (kcrwdm <= len(dm)):
        r = session.post("http://222.200.98.147/xsxklist!getAdd.action?kcrwdm=%s&kcmc=%s"%(dm[kcrwdm-1]["kcrwdm"],dm[kcrwdm-1]["kcmc"]))
        if r.content.decode("utf-8") == "1" :
            print("  ————————————")
            print("  |       选课成功       |")
            print("  ————————————")
        elif r.content.decode("utf-8") == "您已经选了该门课程":
            print("  ————————————")
            print("  |       已选课程       |")
            print("  ————————————")

    else:
        print("  ————————————")
        print("  |     请正确输入！     |")
        print("  ————————————")

if __name__ == '__main__':
    os.system("cls")
    start()