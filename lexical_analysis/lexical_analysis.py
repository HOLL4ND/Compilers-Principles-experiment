import re
import sys
import argparse

reserveWord ={ "auto":1, "break":2, "case":3, "char":4, "const":5, "continue":6,
    "default":7, "do":8, "double":9, "else":10, "enum":11, "extern":12,
    "float":13, "for":14, "goto":15, "if":16, "int":17, "long":18,
    "register":19, "return":20, "short":21, "signed":22, "sizeof":23, "static":24,
    "struct":25, "switch":26, "typedef":27, "union":28, "unsigned":29, "void":30,
    "volatile":31, "while":32}

operatorOrDelimiter={"-":33,"--":34,"-=":35,"->":36,"!":37,
                    "!=":38,"%":39,"%=":40,"&":41,"&&":42,"&=":43,
                    "(":44,")":45,"*":46,"*=":47,",":48,".":49,"/":50,
                    "/=":51,":":52,";":53,"?":54,"[":55,"]":56,"^":57,
                    "^=":58,"{":59,"|":60,"||":61,"|=":62,"}":63,"~":64,
                    "+":65,"++":66,"+=":67,"<":68,"<<":69,"<<=":70,"<=":71,
                    "=":72,"==":73,">":74,">=":75,">>":76,">>=":77,"\"":78}
preproDirective = ["#include","#define","#undef","#if","#ifdef","#ifndef","#elif","#endif"]

def printCharByChar(f):
    while True:
        char = f.read(1)
        print(char)
        if not char:
            break
    f.close()

def readFileLineByLine(f): 
    line = f.readline()
    while line: 
        for ch in line:
            print(ch,end='')
        line = f.readline() 
    f.close

def printTxtFile(f):
    print(f.read())
    f.close()


def checkToken(mode,str):
    if mode == "alpha":
        if str in reserveWord:
            return (str,reserveWord[str])
    if mode == "mark":
        if str in operatorOrDelimiter:
            return (str,operatorOrDelimiter[str])
    return -1

def scanStr(str):
    lastMode = "start"
    tempResult = []
    nowCharBuffer = ""
    for ch in str:
        if ch == ' ' or ch == '\t':
            if lastMode == "mark":
                nowCharBuffer = ""
            result = checkToken(checkMode,nowCharBuffer)
            if result != -1:
                tempResult.append(result)
            elif len(nowCharBuffer)!=0:
                tempResult.append((nowCharBuffer,81))
            nowCharBuffer = ""
            checkMode = "space"

        elif ch.isalpha():
            if lastMode == "mark":
                nowCharBuffer = ""
            checkMode="alpha"
            nowCharBuffer = nowCharBuffer + ch

        elif ch.isnumeric():
            if lastMode == "mark":
                nowCharBuffer = ""
            if lastMode != "alpha":
                checkMode="number"
            nowCharBuffer = nowCharBuffer + ch
        elif ch:
                checkMode="mark"

                # 对之前的token的处理
                if lastMode == "alpha":
                    result = checkToken("alpha",nowCharBuffer)
                    if result != -1:
                        tempResult.append(result)
                    elif len(nowCharBuffer)!=0:
                        tempResult.append((nowCharBuffer,81))
                        nowCharBuffer = ""
                elif lastMode == "number":
                    tempResult.append((nowCharBuffer,80))
                    nowCharBuffer = ""

                # 对新来的token的处理
                if lastMode == "mark":
                    nowCharBuffer = nowCharBuffer + ch
                    result = checkToken("mark",nowCharBuffer)
                    if result != -1:
                        tempResult.pop()
                        tempResult.append(result)
                    else:
                        result = checkToken(checkMode,ch)
                        if result != -1:
                            tempResult.append(result)
                else:
                    nowCharBuffer = nowCharBuffer + ch
                    result = checkToken(checkMode,nowCharBuffer)
                    if result != -1:
                        tempResult.append(result)
        lastMode = checkMode
    return tempResult


if __name__=="__main__":


    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--file",help="appoint file path")
    parser.add_argument("-s","--string",help="input string and analysis",action="store_true")

    args = parser.parse_args()
    if args.file != None and args.string != None:
        parser.error('-f and -s args CAN NOT use together')
    print(args)
    if args.file != None:
        filepath = args.file
        line = 0
        codeStr = ""
        f = open(filepath,'r',encoding = "utf-8")
        line = f.readline()
        while line:
            codeStr = codeStr + line
            line = f.readline()
        
        # 删去预处理指令
        codeStr = re.sub('#.*\\n',"",codeStr)
        # 删去行注释
        codeStr = re.sub('//.*',"",codeStr)
        # 删去块注释 (使用非贪婪匹配)
        codeStr = re.sub('/\*.*?\*/',"",codeStr,flags=re.S|re.M)
        print(codeStr)
        result = scanStr(codeStr)
        for one_result in result:
            print(one_result)
    else :
        codeStr = input("Please input the code:")
        # print(codeStr)
        # 删去预处理指令
        codeStr = re.sub('#.*\\n',"",codeStr)
        # 删去行注释
        codeStr = re.sub('//.*',"",codeStr)
        # 删去块注释 (使用非贪婪匹配)
        codeStr = re.sub('/\*.*?\*/',"",codeStr,flags=re.S|re.M)
        print(codeStr)
        result = scanStr(codeStr)
        for one_result in result:
            print(one_result)

# https://www.cnblogs.com/unixfy/p/3242917.html 博客园
# https://blog.csdn.net/qq_36711003/article/details/82975586
