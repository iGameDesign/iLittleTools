#coding=gb18030

'''
Copyright(c) Funova

FileName        : QHMServerLogAnalyst.py
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

g_TestSuite     = r"QHMServerLogAnalyst"
g_RootPath      = r"E:\WorkSpace\gunsoul_mobile\game\project\server"
g_LogPath       = r"Log"
g_LogFile       = r"logs/QHMServerLogAnalyst.log"
g_JUnitLog      = r"logs/UIMetaChecker.xml"

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

def Analysis(filename):
    """Check the rule of meta file is valid or not.
    
    Return a bool: True -> no error, or otherwise.
    """
    
    bRet = True
    szMsg = ""
    szClassName = ""
    szName = ""
    szJMsg = ""
    if not os.path.exists(filename):
        bRet = False
        szMsg = ("%s: %s") % (filename, " -- not exists.")
        return bRet, szMsg
    else:
        fileobj = file(filename, "r")
        content = fileobj.read()
        fileobj.close()

        # prepare regx
        # regx1 = re.compile(r"(\[\d+-\d+:\d+:\d+ ERROR]\s*.*)\s*")
        # regx1 = re.compile(r"TestCaseEnd, TestCaseResult: False, Fail/All \((\d+)/(\d+)\)")
        regx1 = re.compile(r"TestCaseEnd, TestCaseResult: False, Fail/All \(\d+/\d+\)")
        regx2 = re.compile(r"TestCaseName: (.*)")
        regx3 = re.compile(r"==========  \[  (.*)  \] finish actions ==========")

        results2 = re.findall(regx2, content)
        if results2 and len(results2) > 0:
            print len(results2)
            print results2
            szClassName = results2[0]

        results3 = re.findall(regx3, content)
        if results3 and len(results3) > 0:
            print len(results3)
            print results3
            szName = results3[0]

        results = re.findall(regx1, content)
        if results and len(results) > 0:
            print len(results)
            print results
            bRet = False
            # szMsg = string.join(results[0], "\n")
            szMsg = results[0]

            if bRet:
                szJMsg = ('''
                <testcase classname="%s" result="%s" name="%s"/>
                ''') % (szClassName, "Passed", szName)
                pass
            else:
                szJMsg = ('''
                <testcase classname="%s" result="%s" name="%s">
                    <failure type="Error">
                        %s
                    </failure>
                </testcase>
                ''') % (szClassName, "Failed", szName, szMsg)

        return bRet, szMsg, szJMsg
    pass

if __name__ == "__main__":
    import time
    print("begin at: %s" % (time.strftime('%Y-%m-%d -- %H:%M:%S',time.localtime(time.time()))))
    startTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    parser = argparse.ArgumentParser()
    parser.add_argument('-r')
    parser.print_help()
    args = parser.parse_known_args()[0]

    if args.r:
        g_RootPath = args.r
        g_LogPath = g_RootPath + os.sep + g_LogPath
        print g_LogPath

        bResult = True
        szResMsg = ""
        str1 = ""
        szJUnitMsg = ""
        # logfileobj = open(g_RootPath + os.sep + g_LogFile, "w")
        junitfileobj = open(g_RootPath + os.sep + g_JUnitLog, "w")

        files = []
        files = FindFiles(g_LogPath, files, [".log"])
        print len(files)
        if files and len(files) > 0:
            for f in files:
                print f
                bRet, szMsg, szJMsg = Analysis(f)
                if not bRet and szJMsg != "":
                    bResult = False
                    szResMsg = szResMsg + f + "\n" + szMsg + "\n\n"

                    szJUnitMsg = szJUnitMsg + szJMsg
                else:
                    szJUnitMsg = szJUnitMsg + szJMsg
                    pass
            if bResult:
                print "Success."
                str1 = "Passed"
            else:
                print szResMsg
                str1 = "Failed"

        # logfileobj.write(szResMsg)
        # logfileobj.close()

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
    print("exit 1")