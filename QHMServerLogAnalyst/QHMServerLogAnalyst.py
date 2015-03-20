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
g_LogPath       = r"log"
g_LogFile       = r"logs\QHMServerLogAnalyst.log"

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
    if not os.path.exists(filename):
        bRet = False
        szMsg = ("%s: %s") % (filename, " -- not exists.")
        return bRet, szMsg
    else:
        fileobj = file(filename, "r")
        content = fileobj.read()
        fileobj.close()

        # prepare regx
        # regx1 = re.compile(r"\[\d+-\d+:\d+:\d+ ERROR] (\.+) \[\d+-\d+:\d+:\d+ \w+]")
        regx1 = re.compile(r"(\[\d+-\d+:\d+:\d+ ERROR]\s*.*)\s*")
        results = re.findall(regx1, content)
        if results and len(results) > 0:
            # print len(results)
            # print results
            bRet = False
            szMsg = string.join(results, "\n")

        return bRet, szMsg
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
        g_LogPath = g_RootPath + '\\' + g_LogPath
        print g_LogPath

        bResult = True
        szResMsg = ""
        logfileobj = open(g_LogFile, "w")

        files = []
        files = FindFiles(g_LogPath, files, [".log"])
        print len(files)
        if files and len(files) > 0:
            for f in files:
                bRet, szMsg = Analysis(f)
                if not bRet:
                    bResult = False
                    szResMsg = szResMsg + f + "\n" + szMsg + "\n\n"
                else:
                    pass

        logfileobj.write(szResMsg)
        logfileobj.close()

        endTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    else:
        print "path is None."
    
    print("end at: %s" % (time.strftime('%Y-%m-%d -- %H:%M:%S', time.localtime(time.time()))))
    print("exit 1")