import sys
import os


class FormatReflect:
    # save object
    objdict = {}
    # save new file
    filedict = {}
    conlist = ["public", "private", "protected"]
    # save present method line number and whether has it appended "throws Exception"
    presentmethod = [-1, False, -1]

    def __init__(self, presentpath, filename):
        self.presentpath = presentpath

        self.formatSingle(filename)

    def formatSingle(self, filename):
        # complete path of file
        compath = self.presentpath + '/' + filename

        # save reflect objects
        self.objdict[filename] = {}
        # save simple file
        self.filedict[filename] = []
        isannotation = False

        with open(compath) as ff:
            originallines = ff.readlines()

        # simplify the file
        for orline in originallines:
            orline = orline.strip()

            # if the line is in annotation
            if isannotation:
                i = orline.find("*/")
                if i >= 0:
                    isannotation = False
                    if i < len(orline)-2:
                        self.filedict[filename].append(orline[i+2:].strip()+" ")
                else:
                    self.filedict[filename].append("")

            elif "/*" in orline:
            	i = orline.find("/*")
            	j = orline.find("*/")
            	if i == 0 and j > 0:
                    self.filedict[filename].append(orline[j+2:].strip()+" ")
            	elif i > 0 and j > 0:
                    self.filedict[filename].append(orline[:i]+" ")
                    self.filedict[filename].append(orline[j+2:].strip()+" ")
                elif i ==0 and j < 0:
                    isannotation = True
                    self.filedict[filename].append("")
                else:
                    self.filedict[filename].append(orline[:i]+" ")
                    isannotation = True
            
            elif "//" in orline:
                i = orline.find("//")
                if i == 0:
                    self.filedict[filename].append("");
                else:
                    self.filedict[filename].append(orline[:i])

            elif orline == "":
                self.filedict[filename].append("")

            else:
                self.filedict[filename].append(orline+" ")
                
        # deal with the new file
        for i in range(len(self.filedict[filename])):
            lich = self.filedict[filename][i]
    
            # check if it starts a method 
            liwords = lich.split(" ")
            if liwords[0] in self.conlist:
                if liwords[1] != "class":
                    j = lich.find("throws")
                    if j < 0:
                        j = lich.find("(")
                        
                        # it can not be a variable
                        if j >= 0 and "=" not in lich[:j]:
                            self.presentmethod[0] = i
                            self.presentmethod[1] = False
                            ismark = False
                            bracketsnum = 1
                            for j in range(j+1, len(lich)):
                                if lich[j] == '"':
                                    ismark = not ismark
                                elif lich[j] == "(" and not ismark:
                                    bracketsnum += 1
                                elif lich[j] == ")" and not ismark:
                                    bracketsnum -= 1
                                    if bracketsnum == 0:
                                        self.presentmethod[2] = j
                                        break
                    else:
                        self.presentmethod[0] = i
                        self.presentmethod[1] = True

            if "#" in lich:
                # split using quotation marks
                relis = self.resplit(lich)
                sumlength = 0

                for reli in relis:
                    if reli.startswith("'") or reli.startswith('"') or "#" not in reli:
                        sumlength += len(reli)
                        continue
                    
                    jindex = reli.find("#")
                    inst = jindex + sumlength
                    while jindex >= 0:
                        # "#" between alnum
                        if jindex > 0 and reli[jindex-1].isalnum():
                            mes = 'You are using "#" illegally.\n' + \
                                'You can only put "#" in front of a string variable in which is a class name.\n'
                            self.synError(filename, i, originallines[i], mes)

                        jvalue = ""
                        jkey = ""
                        ch = False
                        # get key and value
                        for j in range(jindex+1, len(reli)):
                            if not ch:
                                if reli[j].isalnum():
                                    jvalue = jvalue + reli[j]
                                elif reli[j] == " ":
                                    ch = True
                                else:
                                    break
                            else:
                                if reli[j].isalnum():
                                    jkey = jkey + reli[j]
                                elif reli[j] == " " and jkey == "":
                                    continue
                                else:
                                    break
                        
                        # check jkey
                        if self.objdict[filename].has_key(jkey):
                            mes = "You are trying to declare a samename variable of class #" +\
                                jvalue + ".\nIt is forbidden in this version.\n"
                            self.synError(filename, i, originallines[i], mes)

                        elif jkey != "":
                            self.objdict[filename][jkey] = jvalue
                            if reli[j] == " ":
                                for j in range(j+1, len(reli)):
                                    if reli[j] != " ":
                                        break
                            # "," ";" after
                            if reli[j] == ";" or reli[j] == ",":
                                self.filedict[filename][i] = lich[:sumlength+jindex] +\
                                    "Object " + jkey + lich[sumlength+j:]
                            
                            # "=" after
                            elif reli[j] == "=":
                                wdl = lich[j+1:]
                                wds = wdl.strip().split(" ")
                               
                               # not "new"
                                if wds[0] != "new":
                                    # deliver a unknown variable
                                    if not self.objdict[filename].has_key(wds[0]):
                                        mes = "You are trying to deliver a unknown variable.\n" +\
                                            "You can only deliver a variable of #" + jvalue + " class.\n"
                                        self.synError(filename, i, originallines[i], mes)

                                    # check if this method has "throws"                    
                                    if not self.conlist[1]:
                                        self.filedict[filename][i] = lich[:j+1] + " throws Exception " + lich[j+1:]
                                        self.conlist[1] = True

                                    self.filedict[filename][i] = lich[:sumlength+jindex] +\
                                        " Object " + jkey + lich[sumlength+j:]

                                # "new" after
                                else:
                                    cls = ""
                                    for ch in wds[1]:
                                        if ch.isalnum() or ch == "#":
                                            cls = cls + ch
                                        else:
                                            break

                                    # wrong class
                                    if cls != "#"+jvalue:
                                        mes = "The object you are trying to new is not the class #" +\
                                            jvalue + ".\n"
                                        self.synError(filename, i, originallines[i], mes)

                                    parst = wdl.find("(")
                                    paren = -1

                                    # can not find "("
                                    if parst < 0:
                                        mes = "Can not find parameters.\n" +\
                                            "Please write the constructor on one line\n"
                                        self.synError(filename, i, originallines[i], mes)

                                    bracketsnum = 1
                                    ismark = False
                                    for ch in range(parst+1, len(wdl)):
                                        if wdl[ch] == '"':
                                            ismark = not ismark
                                        elif wdl[ch] == "(" and not ismark:
                                            bracketsnum = bracketsnum + 1
                                        elif wdl[ch] == ")" and not ismark:
                                            bracketsnum = bracketsnum - 1
                                            if bracketsnum == 0:
                                                paren = ch
                                                break
                                    
                                    # can not find ")"
                                    if paren == -1:
                                        mes = "It is an uncompleted constructor.\n" +\
                                            "Please write the constructor on one line\n"
                                    
                                    parl = wdl[parst+1:paren]
                                    rettuple = self.handleConstructor(parl, jvalue)
                                    
                                    if rettuple[0] != 0:
                                        self.synError(filename, i, originallines[i], rettuple[1])

                                    # check if this method has "throws"                    
                                    if not self.presentmethod[1]:
                                        methodline = self.filedict[filename][self.presentmethod[0]]
                                        methodend = self.presentmethod[2]
                                        self.filedict[filename][self.presentmethod[0]] = methodline[:methodend+1] +\
                                            " throws Exception " + methodline[methodend+1:]
                                        self.presentmethod[1] = True

                                    parl = " Object " + jkey + " =" + rettuple[1]
                                    if inst == 0:
                                        self.filedict[filename][i] = parl + lich[j+paren+2:]
                                    else:
                                        self.filedict[filename][i] = lich[:inst-1] + parl + lich[j+paren+2:]

                        if jindex < len(reli)-1:
                            jindex = reli.find("#", jindex+1)

            else:
                # check object
                for obj in self.objdict[filename].keys():
                    iobj = lich.find(obj)
                    if iobj < 0:
                        continue
                    elif iobj == 0 and lich[iobj+len(obj)].isalnum():
                        continue
                    elif iobj == len(lich)-1 and lich[iobj-1].isalnum():
                        continue
                    elif lich[iobj-1].isalnum() or lich[iobj+len(obj)].isalnum():
                        continue

                    # object in the end
                    if iobj == len(lich)-1:
                        mes = "Wrong use of the object.\n" +\
                            "Please write on one line\n"
                        self.synError(filename, i, originallines[i], mes)

                    jindex = iobj + len(obj)
                    while lich[jindex] != ".":
                        if jindex == len(lich)-1:
                            mes = "Wrong use of the object.\n" +\
                                "Please write on one line\n"
                            self.synError(filename, i, originallines[i], mes)
                        jindex += 1

                    # find the name of method
                    member = ""
                    ismem = True
                    for jindex in range(jindex+1, len(lich)):
                        if lich[jindex] == " ":
                            if member == "":
                                continue
                            else:
                                ismem = False
                        elif lich[jindex].isalnum() and ismem:
                            member += lich[jindex]
                        elif lich[jindex] == "(":
                            break
                        else:
                            mes = "Only methods are supported in this version.\n"
                            self.synError(filename, i, originallines[i], mes)

                    ismark = False
                    paren = -1
                    bracketsnum = 1
                    for ch in range(jindex+1, len(lich)):
                        if lich[ch] == '"':
                            ismark = not ismark
                        elif lich[ch] == "(" and not ismark:
                            bracketsnum += 1
                        elif lich[ch] == ")" and not ismark:
                            bracketsnum -= 1
                            if bracketsnum == 0:
                                paren = ch
                                break

                    if paren == -1:
                        mes = "Wrong use of the object.\n" +\
                            "Please write on one line"
                        self.synError(filename, i, orignallines[i], mes)

                    rettuple = self.handleMethod(lich[jindex+1:paren], member, obj, self.objdict[filename][obj])

                    if rettuple[0] != 0:
                        self.synError(filename, i, originallines[i], rettuple[1])

                    # check if this method has "throws"                    
                    if not self.presentmethod[1]:
                        methodline = self.filedict[filename][self.presentmethod[0]] 
                        methodend = self.presentmethod[2]
                        self.filedict[filename][self.presentmethod[0]] = methodline[:methodend+1] +\
                            " throws Exception " + methodline[methodend+1:]
                        self.presentmethod[1] = True

                    if iobj == 0:
                        self.filedict[filename][i] = rettuple[1] + lich[paren+1:]
                    else:
                        self.filedict[filename][i] = lich[:iobj-1] + rettuple[1] + lich[paren+1:]
                
                    break

        with open(self.presentpath + "/" + "re_" + filename, "w") as ff:
            for line in self.filedict[filename]:
                ff.write(line + "\n")

    # split st using quotation marks
    def resplit(self, st):
        li = []
        dmark = False
        smark = False
        j = 0
        for i in range(len(st)):
            if st[i] == '"' and not smark:
                if dmark:
                    li.append(st[j:i+1])
                    j = i+1
                else:
                    li.append(st[j:i])
                    j = i
                dmark = not dmark
            elif st[i] == "'" and not dmark:
                if smark:
                    li.append(st[j:i+1])
                    j = i+1
                else :
                    li.append(st[j:i])
                    j = i
                smark = not smark
            elif i == len(st)-1:
                li.append(st[j:i])
        return li

    # handle the constructor
    def handleConstructor(self, parl, cls):
        formatnew = ""
        # default constructor
        if parl == "":
            formatnew = "Class.forName(" + cls + ").newInstance()"
            return 0, formatnew

        ret, formatnew = self.handleParameters(parl)
        if ret != 0:
            return ret, formatnew
        formatnew = " Class.forName(" + cls + ").getConstructor(" + formatnew + ").newInstance(" + parl + ")"

        return 0, formatnew

    # handle method
    def handleMethod(self, parl, metname, objname, cls):
        formatnew = ""
        if parl == "":
            formatnew = " Class.forName(" + cls + ").getMethod(" + metname + ").invoke(" + objname + ")"
            return 0, formatnew

        ret, formatnew = self.handleParameters(parl)
        if ret != 0:
            return ret, formatnew
        
        formatnew = " Class.forName(" + cls + ').getMethod("' + metname + '", ' +\
            formatnew + ").invoke(" + objname + ", " + parl + ")"

        return ret, formatnew 

    # handle parameters
    def handleParameters(self, parl):
        formatnew = ""
        pars = []
        types = []
        symbols = {}
        isre = True
        ismark = 0
        for i in parl:
            # in quotation marks
            if ismark!=0 and ismark!=i:
                pars[len(pars)-1] += i
            elif i == "," and len(symbols)==0:
                isre = True
            else:
                if isre:
                    pars.append("")
                    isre = False
                pars[len(pars)-1] += i
                if i == "'":
                    if symbols.has_key("'"):
                        del symbols["'"]
                        ismark = 0
                    else:
                        symbols["'"] = 1
                        ismark = "'"
                elif i == '"':
                    if symbols.has_key('"'):
                        del symbols['"']
                        ismark = 0
                    else:
                        symbols['"'] = 1
                        ismark = '"'
                elif i == "(":
                    if symbols.has_key("("):
                        symbols["("] += 1
                    else:
                        symbols["("] = 1
                elif i == ")":
                    symbols["("] -= 1
                    if symbols["("] == 0:
                        del symbols["("]
                elif i == "{":
                    if symbols.has_key("{"):
                        symbols["{"] += 1
                    else:
                        symbols["{"] = 1
                elif i == "}":
                    symbols["{"] -= 1
                    if symbols["{"] == 0:
                        del symbols["{"]

        for i in pars:
            i = i.strip()
            isfl = i.find(".")
            if i == "":
                formatnew = "Wrong parameters.\n"
                return -1, formatnew
            elif i[0].isalpha():
                formatnew = "Wrong parameters.\n" + "You can only use basic types.\n"
                return -1, formatnew
            elif i.startswith('"') and i.endswith('"'):
                types.append("String.class")
            elif i.endswith("L") or i.endswith("l"):
                if i[:len(i)-1].isdigit():
                    types.append("long.class")
            elif i.isdigit():
                types.append("int.class")
            elif isfl >= 0 and i[:isfl].isdigit() and i[isfl+1:].isdigit():
                types.append("double.class")

        for i in range(len(types)):
            if i != 0:
                formatnew += ", "
            formatnew += types[i]

        return 0, formatnew

    # handle syntax error
    def synError(self, filename, num, line, mes=""):
        wr = 'File "' + filename + '", line ' + str(num) + ' :\n' + \
            line + '\n' + mes
        sys.stderr.write(wr)
        sys.exit(1)


if __name__ == '__main__':
    FormatReflect("/Users/wsy/Documents/JavaReflect", "test.java")

