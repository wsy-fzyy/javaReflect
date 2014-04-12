#coding=utf-8
import os
import sys
import platform


def env_check():
    # check system
    if platform.uname()[0] == "Windows":
        print "对不起，此版本不支持Windows!"
        sys.exit(1)

    # check jdk
    if not os.path.exists("/usr/bin/javac") and not os.path.exists("/usr/local/bin/javac"):
        print "Java Development Kit 未安装..."
        sys.exit(1)

    # check Python.h
    for i in range(7, 4, -1):
        if os.path.exists("/usr/include/python2." + str(i)):
            pyversion = i
            break
    if pyversion == 0:
        print "Python 未安装..."
        sys.exit(1)
    if not os.path.exists("/usr/include/python2." + str(pyversion) + "/Python.h"):
        print "Python.h 不存在..."
        print "请安装 python-dev 或 python-devel"
        sys.exit(1)
    return pyversion

def create_makefile(pyversion):
    mflist = []
    mflist.append("CXX = gcc")
    mflist.append("TARGET = javar")
    mflist.append("C_FLAGS += -g -Wall")
    mflist.append("INC = -I/usr/include/python2." + str(pyversion))
    mflist.append("LIB = -lpython2." + str(pyversion))
    mflist.append("all: $(TARGET)")
    mflist.append("javar: javar.o")
    mflist.append("\t$(CXX) -o $@ $^ $(C_FLAGS) $(LIB)")
    mflist.append(".c.o:")
    mflist.append("\t$(CXX) -c -o $*.o $(INC) $(C_FLAGS) $*.c")
    mflist.append("install:")
    mflist.append("\tcp -f javar /usr/local/bin/")
    mflist.append("\tif [ ! -e '/etc/javareflect/' ]; then mkdir /etc/javareflect/; fi")
    mflist.append("\tcp -f handleMain.py /etc/javareflect/")
    mflist.append("\tcp -f handleReflect.py /etc/javareflect/")
    mflist.append("\tcp -f reflectHelp.py /etc/javareflect/")
    mflist.append("clean:")
    mflist.append("\trm -f *.o $(TARGET)")

    with open("makefile", "w") as ff:
        for mf in mflist:
            ff.write(mf + "\n")

def main():
    pyversion = env_check()
    create_makefile(pyversion)

if __name__ == "__main__":
    main()
