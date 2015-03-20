#coding=gb18030

'''
Copyright(c) Funova

FileName        : UIOptimizePNGModify.py
Creator         : pengpeng
Date            : 2014-12-25 11:11
Comment         : 
ModifyHistory   :

'''

__version__ = '1.0.0.0'
__author__ = 'pengpeng'

import os
import sys
import re
import string
import csv
import argparse

g_TestSuite     = r"UIOptimizePNGModify"
g_RootPath      = r"E:\WorkSpace\gunsoul_mobile\game\project\game-xx"
g_UIPath        = r"E:\WorkSpace\gunsoul_mobile\game\project\game-xx\Assets\resourcex\ui\altas"
g_LogFile       = r"logs\UIOptimizePNGModify.log"
g_JUnitLog      = r"logs\UIOptimizePNGModify.xml"

g_rule_1        = [{'textureSettings':'', 'filterMode':1, 'lineGap':1},
                    {'buildTarget':'iPhone', 'textureFormat':33, 'lineGap':2},
                    {'buildTarget':'Android', 'textureFormat':12, 'lineGap':2}]

def FindFiles(dir, out, filter):
    if not os.path.exists(dir):
        print "path not exists."
        return
    listdir = os.listdir(dir)
    for file in listdir:
        filename = os.path.join(dir, file)
        if os.path.isfile(filename):
            ext = os.path.splitext(filename)[1]
            # print ext
            if ext.lower() in filter or ext == '':
                # print filename
                out.append(filename)
        elif os.path.isdir(filename):
            if file == ".svn":
                continue
            out = FindFiles(filename, out, filter)
    return out

def ReadTabFile(filepath):
    reader = csv.reader(open(filepath, "r"), delimiter="\t")
    i = 0
    res = []
    for row in reader:
        i = i + 1
        if i > 1:
            res.append(row[0])
    return res
    pass

def Analysis(file_path, keys_prefix, keys_postfix):
    """Extract the path from the give file.
    
    Return a set.
    """
    fileobj = file(file_path, "r")
    filecontent = fileobj.read() # read the content, this is also for lua special
    fileobj.close()
    
    outset = set()
    
    regx = re.compile(r"(%s[/|\\].+?\.(%s))" % (keys_prefix, keys_postfix), re.I)
    results = re.findall(regx, filecontent)
    for result in results:
        if len(result) > 0:
            if "\t" not in result[0]:
                afterformat = string.replace(result[0], "\\\\", "\\")
                afterformat = string.replace(afterformat, "/", "\\")
                outset.add(afterformat)
    
    return outset

def Check_rule_1(i, filepath, rules = ""):
    """Check the rule of meta file is valid or not.
    
    Return a bool: True -> no error, or otherwise.
    """
    
    bRet = True
    szName = ("Path: %s \n") % (filepath[len(g_RootPath)+1:])
    szMsg = ""
    szJMsg = ""
    JUnitResult = {}
    if not os.path.exists(filepath):
        bRet = False
        szMsg = ("%s: %s") % (szName, " -- not exists.")
        szJMsg = ('''
        <testcase classname="%s" caseId="%s" result="%s" name="%s">
            <failure type="Error">
            </failure>
        </testcase>
        ''') % (i, i, bRet, szName)
        return bRet, szMsg, szJMsg
    else:
        fileobj = file(filepath, "r")
        lines = fileobj.readlines()
        fileobj.close()

        index = 0
        # prepare regx
        regx1 = re.compile(r"(textureSettings):")
        regx2 = re.compile(r"filterMode: (\d+)")
        regx3 = re.compile(r"buildTarget: (\w+)")
        regx4 = re.compile(r"textureFormat: (\d+)")


        # for line in lines:
        for index in xrange(0,len(lines) - 1):
            # print lines[index]
            results = re.findall(regx1, lines[index])
            if results and len(results) > 0:

                if results[0] == 'textureSettings':
                    # print results[0]
                    index = index + 1
                    if len(lines[index]) > 0:
                        results2 = re.findall(regx2, lines[index])
                        if results2 and len(results2) > 0:
                            # print results2[0]
                            if results2[0] == '1':
                                # bRet = True
                                # szMsg = szMsg + "\t[Rule 1] Success: the value of 'textureFormat' with buildTarget 'Standalone' matched. Expected(4) Actual(%s).\n" % (results2[0])
                                szMsg = szMsg + "\t[Rule 1] Success.\n"
                            else:
                                bRet = False
                                szMsg = szMsg + "\t[Rule 1] Failed: the value of 'textureFormat' with buildTarget 'Standalone' not match. Expected(4) Actual(%s).\n" % (results2[0])
                        else:
                            bRet = False
                            szMsg = szMsg + "\t[Rule 1] Failed: 'textureFormat' not exists or have no vaule with buildTarget 'Standalone'.\n"
                        pass
                if results[0] == 'iPhone':
                    # print results[0]
                    index = index + 2
                    if len(lines[index]) > 0:
                        results2 = re.findall(regx2, lines[index])
                        if results2 and len(results2) > 0:
                            # print results2[0]
                            if results2[0] == '4':
                                # bRet = True
                                # szMsg = szMsg + "\t[Rule 2] Success. the value of 'textureFormat' with buildTarget 'iPhone' matched. Expected(4) Actual(%s).\n" % (results2[0])
                                szMsg = szMsg + "\t[Rule 2] Success.\n"
                            else:
                                bRet = False
                                szMsg = szMsg + "\t[Rule 2] Failed: the value of 'textureFormat' with buildTarget 'iPhone' not match. Expected(4) Actual(%s).\n" % (results2[0])
                        else:
                            bRet = False
                            szMsg = szMsg + "\t[Rule 2] Failed: 'textureFormat' not exists or have no vaule with buildTarget 'iPhone'.\n"
                        pass
                if results[0] == 'Android':
                    # print results[0]
                    index = index + 2
                    if len(lines[index]) > 0:
                        results2 = re.findall(regx2, lines[index])
                        if results2 and len(results2) > 0:
                            # print results2[0]
                            if results2[0] == '4':
                                # bRet = True
                                # szMsg = szMsg + "\t[Rule 3] Success: the value of 'textureFormat' with buildTarget 'Android' matched. Expected(4) Actual(%s).\n" % (results2[0])
                                szMsg = szMsg + "\t[Rule 3] Success.\n"
                            else:
                                bRet = False
                                szMsg = szMsg + "\t[Rule 3] Failed: the value of 'textureFormat' with buildTarget 'Android' not match. Expected(4) Actual(%s).\n" % (results2[0])
                        else:
                            bRet = False
                            szMsg = szMsg + "\t[Rule 3] Failed: 'textureFormat' not exists or have no vaule with buildTarget 'Android'.\n"
                        pass
            # index = index + 1
        if bRet:
            szJMsg = ('''
            <testcase classname="%s" caseId="%s" result="%s" name="%s"/>
            ''') % (i, i, "Passed", szName)
            pass
        else:
            szJMsg = ('''
            <testcase classname="%s" caseId="%s" result="%s" name="%s">
                <failure type="Error">
                    %s
                </failure>
            </testcase>
            ''') % (i, i, "Failed", szName + szMsg, szMsg)
        return bRet, szMsg, szJMsg
    pass

if __name__ == "__main__":
    import time
    print("begin at: %s" % (time.strftime('%Y-%m-%d -- %H:%M:%S',time.localtime(time.time()))))

    str1 = '''textureSettings:
    filterMode: 1'''
    regx1 = re.compile(r"(textureSettings):")
    regx2 = re.compile(r"filterMode: (\d+)")

    result = re.findall(regx1, str1)
    print result
    result = re.findall(regx2, str1)
    print result
    result = re.sub(regx2, "filterMode: 2", str1)
    print result
    
    
    print("end at: %s" % (time.strftime('%Y-%m-%d -- %H:%M:%S', time.localtime(time.time()))))
