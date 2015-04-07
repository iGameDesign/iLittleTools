#coding=utf-8

'''
Copyright(c) Funova

FileName        : PrefabScriptsChecker.py
Creator         : pengpeng
Date            : 2014-12-25 11:11
Comment         : 
ModifyHistory   :
    1. find all scripts in folder "Assets\scripts", except NGUI
    2. find all .prefab files, and the reference scripts
    3. if the script is in folder "Assets\scripts", log it.

'''

__version__ = '1.0.0.0'
__author__ = 'pengpeng'

import os
import sys
import re
import string
import csv
import argparse
import md5, hashlib

g_TestSuite         = r"PrefabScriptsChecker"
g_RootPath          = r"E:\WorkSpace\gunsoul_mobile\game\project\game-xx"
g_LogFile           = r"logs\PrefabScriptsChecker.log"
g_JUnitLog          = r"logs\PrefabScriptsChecker.xml"

g_strScriptsFolder  = r'Assets/scripts'
g_strPrefabsFolder  = r'Assets'

g_listScripts       = []
g_listPrefabs       = []

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
    pass

if __name__ == "__main__":
    import time
    startTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print("begin at: %s" % (time.strftime('%Y-%m-%d -- %H:%M:%S',time.localtime(time.time()))))
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-r')
    parser.print_help()
    args = parser.parse_known_args()[0]

    if args.r:
        g_RootPath = args.r
        print g_RootPath

        bResult = True
        g_strScriptsFolder  = g_RootPath + os.sep + g_strScriptsFolder
        g_strPrefabsFolder  = g_RootPath + os.sep + g_strPrefabsFolder

        g_listScripts       = FindFiles(g_strScriptsFolder, g_listScripts, ['.cs', '.js'])
        g_listPrefabs       = FindFiles(g_strPrefabsFolder, g_listPrefabs, ['.prefab'])

        listScriptsMD5      = {}
        listPrefabsMD5      = {}

        for script in g_listScripts:
            # print script

            # get md5 from .meta
            filename = script + '.meta'
            regx = re.compile(r'guid: (\w*)')
            f = open(filename, 'r')
            content = f.read()
            f.close()
            results = re.findall(regx, content)
            if results and len(results) > 0:
                for md5 in results:
                    # keys = listScriptsMD5.keys()
                    # print md5
                    listScriptsMD5[md5] = script

            # f = open(script, 'rb')
            # m = hashlib.md5()
            # m.update(f.read())
            # f.close()
            # md5 = m.hexdigest()
            # listScriptsMD5[md5] = script
            # print md5

            # if not listScriptsMD5[md5]:
            #     listScriptsMD5[md5] = script
            # else:
            #     print 'md5 is repeat: md5(%s) file(%s)' % (md5, script)

        for prefab in g_listPrefabs:
            # print prefab
            regx = re.compile(r'm_Script: {fileID: \d*, guid: (\w*), type: \d*}')
            f = open(prefab, 'r')
            content = f.read()
            f.close()
            results = re.findall(regx, content)
            if results and len(results) > 0:
                for md5 in results:
                    listPrefabsMD5[md5] = prefab

        keys = listScriptsMD5.keys()
        for md5 in listPrefabsMD5:
            if md5 in keys:
                print 'this script file should not be referred by this prefab: prefab(%s) md5(%s) file(%s)' % (listPrefabsMD5[md5], md5, listScriptsMD5[md5])

        endTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    else:
        print "path is None."
    
    print("end at: %s" % (endTime))
