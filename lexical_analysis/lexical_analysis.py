import re
import argparse

# 关键字字典
keyWord = {
    "auto": 1,    "break": 2,    "case": 3,    
    "char": 4,    "const": 5,    "continue": 6,
    "default": 7,    "do": 8,    "double": 9,    
    "else": 10,    "enum": 11,    "extern": 12,
    "float": 13,    "for": 14,    "goto": 15,    
    "if": 16,    "int": 17,    "long": 18,
    "register": 19,    "return": 20,    "short": 21,   
    "signed": 22,    "sizeof": 23,    "static": 24,
    "struct": 25,    "switch": 26,    "typedef": 27,   
    "union": 28,    "unsigned": 29,    "void": 30,
    "volatile": 31,    "while": 32,
}
# 操作符及界符字典
operatorOrDelimiter = {
    "-": 33,    "--": 34,    "-=": 35,    "->": 36,    
    "!": 37,    "!=": 38,    "%": 39,    "%=": 40,    
    "&": 41,    "&&": 42,    "&=": 43,    "(": 44,    
    ")": 45,    "*": 46,    "*=": 47,    ",": 48,
    ".": 49,    "/": 50,    "/=": 51,    ":": 52,
    ";": 53,    "?": 54,    "[": 55,    "]": 56,
    "^": 57,    "^=": 58,    "{": 59,    "|": 60,
    "||": 61,    "|=": 62,    "}": 63,    "~": 64,
    "+": 65,    "++": 66,    "+=": 67,    "<": 68,
    "<<": 69,    "<<=": 70,    "<=": 71,    "=": 72,
    "==": 73,    ">": 74,    ">=": 75,    ">>": 76,
    ">>=": 77,    '"': 78,
}


def checkToken(mode, str):
    """
    功能说明:根据传入的不同的mode,对传入的str,和对应的字典进行token的匹配

    @param mode:识别的模式,用于使用不同的字典进行匹配
    @param str :待匹配的字符串

    返回值:
    ① √ 若匹配成功则返回一个 token 元组 (单词符号，种别码)
    ② × 若匹配失败则返回-1
    """
    if mode == "alpha":
        if str in keyWord:
            return (str, keyWord[str])
    if mode == "mark":
        if str in operatorOrDelimiter:
            return (str, operatorOrDelimiter[str])
    return -1


def scanStr(str):
    """
    功能说明:扫描传入的字符串,并进行简单的词法分析
    @param str:待扫描的字符串

    返回值:扫描的结果,是一个元素为元组的列表 List[(单词，种别码),(单词，种别码),..,(单词，种别码)]
    """

    lastMode = "start"  # 上一次扫描时的模式
    tempResult = []  # 存储结果的列表
    nowCharBuffer = ""  # 当前缓存区
    checkMode = ""  # 当前字符的模式

    for ch in str:
        # 如果是空格或者是制表符则需要对buffer中的字符进行判断
        if ch == " " or ch == "\t":
            # 如果之前模式是mark则需要清空
            if lastMode == "mark":
                nowCharBuffer = ""
            # 判断buffer中的字符串是否匹配关键字
            result = checkToken(checkMode, nowCharBuffer)
            # 如果匹配则将结果添加到tempResult列表中
            if result != -1:
                tempResult.append(result)
            # 如果不匹配且buffer中存在字符则为标识符
            elif len(nowCharBuffer) != 0:
                tempResult.append((nowCharBuffer, 81))
            nowCharBuffer = ""
            checkMode = "space"

        elif ch.isalpha():
            if lastMode == "mark":
                nowCharBuffer = ""
            checkMode = "alpha"
            nowCharBuffer = nowCharBuffer + ch

        elif ch.isnumeric():
            # 如果前模式为字母，则说明该数字为标识符中的数字，无需进行模式的转换
            if lastMode == "mark":
                nowCharBuffer = ""
            # 如果前面的模式不为字母，则说明并非标识符中的数字，应将转换模式为数字
            if lastMode != "alpha":
                checkMode = "number"
            nowCharBuffer = nowCharBuffer + ch
        elif ch:
            checkMode = "mark"

            # 当前字符和前模式发生了变化，应对之前的buffer进行匹配
            if lastMode == "alpha":
                result = checkToken("alpha", nowCharBuffer)
                if result != -1:
                    tempResult.append(result)
                elif len(nowCharBuffer) != 0:
                    tempResult.append((nowCharBuffer, 81))
                    nowCharBuffer = ""
            elif lastMode == "number":
                tempResult.append((nowCharBuffer, 80))
                nowCharBuffer = ""

            # 对新来的token的处理
            # 如果之前是mark模式,则需要考虑多个字符组合的情况
            if lastMode == "mark":
                nowCharBuffer = nowCharBuffer + ch
                # buffer 追加扫描的字符,然后对组合后的字符串传入匹配
                result = checkToken("mark", nowCharBuffer)
                # 如果加上新的字符后匹配成功
                if result != -1:
                    # 弹出上一轮添加的token
                    tempResult.pop()
                    # 压入新的匹配结果
                    tempResult.append(result)
                # 如果加上新的字符后匹配失败,则对新来的字符单独识别
                else:
                    result = checkToken(checkMode, ch)
                    if result != -1:
                        tempResult.append(result)
            # 之前为非mark模式,则只需要对进入的新字符进行单独的判断
            else:
                nowCharBuffer = nowCharBuffer + ch
                result = checkToken(checkMode, nowCharBuffer)
                if result != -1:
                    tempResult.append(result)
        # 更新lastmode
        lastMode = checkMode
    return tempResult


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="appoint file path")
    parser.add_argument(
        "-s", "--string", help="input string and analysis", action="store_true"
    )
    args = parser.parse_args()
    if args.file != None and args.string == True:
        parser.error("-f and -s args CAN NOT use together")
    if args.file != None:
        filepath = args.file
        line = 0
        codeStr = ""
        f = open(filepath, "r", encoding="utf-8")
        line = f.readline()
        while line:
            codeStr = codeStr + line
            line = f.readline()

        # 删去预处理指令
        codeStr = re.sub("#.*\\n", "", codeStr)
        # 删去行注释
        codeStr = re.sub("//.*", "", codeStr)
        # 删去块注释 (使用非贪婪匹配)
        codeStr = re.sub("/\*.*?\*/", "", codeStr, flags=re.S | re.M)
        print(codeStr)

        result = scanStr(codeStr)
        for one_result in result:
            print(one_result)
    else:
        codeStr = input("Please input the code:")
        # print(codeStr)
        # 删去预处理指令
        codeStr = re.sub("#.*\\n", "", codeStr)
        # 删去行注释
        codeStr = re.sub("//.*", "", codeStr)
        # 删去块注释 (使用非贪婪匹配)
        codeStr = re.sub("/\*.*?\*/", "", codeStr, flags=re.S | re.M)
        print(codeStr)

        result = scanStr(codeStr)
        for one_result in result:
            print(one_result)

# https://www.cnblogs.com/unixfy/p/3242917.html 博客园
# https://blog.csdn.net/qq_36711003/article/details/82975586
