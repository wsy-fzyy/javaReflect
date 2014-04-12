#coding=utf-8
import os
import handleReflect
import reflectHelp

def main(path, *arglist):
    if "-help" in arglist or len(arglist) == 1:
        reflectHelp.printHelp()
        return
    
    elif "-version" in arglist:
        print "javar " + reflectHelp.getVersion()
        os.system("javac -version")
        return 

    if not os.path.exists(path):
        print "路径不存在！"
        return -1;
    filename = arglist[len(arglist)-1]
    fpath = path + "/" + filename
    if not os.path.isfile(fpath):
        print "目标不是一个文件!"
        return -1

    if "-r" not in arglist and "-rs" not in arglist:
        argstr = " "
        for i in range(1, len(arglist)):
            argstr += arglist[i] + " " 
        # run javac
        os.system("javac" + argstr + fpath)

    else:
        if "-rs" in arglist:
            if "-r" in arglist:
                print "no no"
                return -1
            issave = True
            rindex = arglist.index("-rs")
            handleReflect.FormatReflect(path, filename)
        else:
            issave = False
            rindex = arglist.index("-r")
            handleReflect.FormatReflect(path, filename)

        argstr = " "
        for i in range(1, len(arglist)):
            if i == rindex:
                continue
            argstr += arglist[i] + " "

        os.system("mv " + fpath + " " + fpath + "r")
        os.system("mv " + path + "/re_" + filename + " " + fpath)
        os.system("javac" + argstr + fpath)
        if issave:
            os.system("mv " + fpath + " " + fpath[:len(fpath)-5] + ".txt")
        os.system("mv " + fpath + "r " + fpath)


