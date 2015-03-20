#coding=gb18030

'''
Copyright(c) Funova

FileName        : UIOptimizeChecker.py
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
# import yaml
# from PIL import Image
import Image

g_TestSuite     = r"UIOptimizeChecker"
g_RootPath      = r"E:\WorkSpace\gunsoul_mobile\game\project\game-xx"
g_UIPath        = r"E:\WorkSpace\gunsoul_mobile\game\project\game-xx\Assets\resourcex\ui\altas"
g_TabFile       = r"UIMetaCheckerConfig.tab"
g_LogTab        = r"logs\UIMetaCheckerLog.tab"
g_LogFile       = r"logs\UIOptimizeChecker.log"
g_JUnitLog      = r"logs\UIOptimizeChecker.xml"

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

def Check_rule_1(i, f_png, rules = ""):
    """Check the rule of meta file is valid or not.
    
    Return a bool: True -> no error, or otherwise.
    """
    
    bRet = True
    szName = ("Path: %s \n") % (f_png[len(g_RootPath)+1:])
    szMsg = ""
    szJMsg = ""
    logresult = []
    JUnitResult = {}
    if not os.path.exists(f_png):
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
        # 1. Get the size of the png
        img = Image.open(f_png)
        # print f[:-4] + keys_postfix
        # print img.size
        area = img.size[0] * img.size[1]

        # 2. Get the size of the sub in the pefab png.
        f_prefab = f_png[:-4] + keys_postfix
        if os.path.exists(f_prefab):

            png_subs = []
            fileobj = file(f_prefab, "r")
            lines = fileobj.readlines()
            fileobj.close()

            # index = 0
            # prepare regx
            regx1 = re.compile(r"name: (\w+)")
            regx2 = re.compile(r"width: (\d+)")
            regx3 = re.compile(r"height: (\d+)")

            # for line in lines:
            for index in xrange(0,len(lines) - 1):
                # print lines[index]
                results = re.findall(regx1, lines[index])
                if results and len(results) > 0:
                    # print results[0]
                    # index = index + 3
                    if lines[index + 3] and lines[index + 4]:
                        results2 = re.findall(regx2, lines[index + 3])
                        results3 = re.findall(regx3, lines[index + 4])
                        if (results2 and len(results2) > 0) and (results3 and len(results3) > 0):
                            # print results2[0]
                            width = int(results2[0])
                            height = int(results3[0])
                            area_t = width * height
                            png_subs.append(area_t)
                    
                # index = index + 1

            sub_area = 0
            for item in png_subs:
                sub_area = sub_area + item
            # print area, sub_area
            ratio = float(sub_area) / float(area)
            logresult = [f_png[len(g_RootPath)+1:], area, sub_area, ratio]
            # print ratio
            if 1.00 > ratio > 0.85:
                bRet = True
                szMsg = "Thie png file no need to be optimized."
                szJMsg = ('''
                <testcase classname="%s" caseId="%s" result="%s" name="%s"/>
                ''') % (i, i, "Passed", szName)
                pass
            else:
                bRet = False
                szMsg = "Thie png file need to be optimized. Total area(%s), Actual area(%s), Ratio(%.2f%%)." % (area, sub_area, ratio * 100)
                szJMsg = ('''
                <testcase classname="%s" caseId="%s" result="%s" name="%s">
                    <failure type="Error">
                        %s
                    </failure>
                </testcase>
                ''') % (i, i, "Failed", szName + szMsg, szMsg)
        return bRet, szMsg, szJMsg, logresult
    pass

if __name__ == "__main__":
    import time
    print("begin at: %s" % (time.strftime('%Y-%m-%d -- %H:%M:%S',time.localtime(time.time()))))
    startTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    parser = argparse.ArgumentParser()
    parser.add_argument('-r')
    parser.add_argument('-d')
    parser.print_help()
    args = parser.parse_known_args()[0]

    if args.d:
        g_RootPath = args.r
        g_UIPath = args.d
        print g_UIPath

        bResult = True
        szResMsg = ""
        szJUnitMsg = ""
        nTotalFailedCount = 0
        str1 = ""
        keys_postfix = ".prefab"
        logfileobj = open(g_LogFile, "w")
        junitfileobj = open(g_JUnitLog, "w")
        logtabobj = open(g_LogTab, "w")

        logresult = []
        files = []
        files = FindFiles(g_UIPath, files, [".png"])
        if files:
            i = 0
            for f in files:
                i = i + 1
                bRet, szMsg, szJMsg, temp = Check_rule_1(i, f)
                if not bRet:
                    bResult = False
                    szResMsg = szResMsg + szMsg

                    szJUnitMsg = szJUnitMsg + szJMsg
                    logresult.append(temp)
                else:
                    szJUnitMsg = szJUnitMsg + szJMsg


            # if bResult:
            #     # print "Success."
            #     str1 = "Passed"
            # else:
            #     # print szResMsg
            #     str1 = "Failed"

        # Test
        # i = 0
        # f1 = r"E:\workspace\gunsoul_mobile\game\project\game-xx\Assets\resourcex\ui\altas\beibao\nxbeibao.png"
        # f2 = r"E:\workspace\gunsoul_mobile\game\project\game-xx\Assets\resourcex\ui\altas\beibao\nxbeibao.prefab"
        # Check_rule_1(i, f1, f2)

        # logfileobj.write(szResMsg)
        # logfileobj.close()

        # logtabobj
        logtabobj.write("filename\tarea\t(KB)\tsub_area\t(KB)\tratio\n")
        for item in logresult:
            print item
            logtabobj.write("%s\t%s\t%s\t%s\t%s\t%.2f%%\n" % (item[0], item[1], item[1] / 1024, item[2], item[2] / 1024, item[3] * 100))
        logtabobj.close()

        endTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        junitfileobj.write(r'<?xml version="1.0" encoding="utf-8"?>')
        junitfileobj.write(r'<testsuite classname="%s" name="%s" result="%s" startTime="%s" endTime="%s" errorInfo="">' 
            % ("Resource Check", g_TestSuite, str1, startTime, endTime))
        junitfileobj.write(r'<testsuite>')
        junitfileobj.write(szJUnitMsg)
        junitfileobj.write(r'</testsuite>')
        junitfileobj.write(r'</testsuite>')
        junitfileobj.close()
    else:
        print "path is None."
    
    print("end at: %s" % (time.strftime('%Y-%m-%d -- %H:%M:%S', time.localtime(time.time()))))
