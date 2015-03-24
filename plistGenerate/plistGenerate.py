#coding=utf-8

'''
Copyright(c) Funova

FileName        : plistGenerate.py
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

g_workDir = "/Volumes/Work/www"
g_subDir = ["autobranch", "packagebranches"]
g_plistTemp = '''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
        <key>items</key>
        <array>
                <dict>
                        <key>assets</key>
                        <array>
                                <dict>
                                        <key>kind</key>
                                        <string>software-package</string>
                                        <key>url</key>
                                        <string>http://macbuild.funova.com/test/Bulletgirls.ipa</string>
                                </dict>
                        </array>
                        <key>metadata</key>
                        <dict>
                                <key>bundle-identifier</key>
                                <string>com.funova.bulletgirls</string>
                                <key>bundle-version</key>
                                <string>1.1</string>
                                <key>kind</key>
                                <string>software</string>
                                <key>title</key>
                                <string>Bulletgirls</string>
                        </dict>
                </dict>
        </array>
</dict>
</plist>
'''

g_pinstallTemp = '''
<html>
<head>
<center>
<title></title>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<!--meta http-equiv="refresh" content="0;url=http://macbuild.funova.com:8080"-->
<replace_IOS/>
<replace_Android/>
</center>
</head>
</html>
'''
g_linkIOS = '<a href="itms-services://?action=download-manifest&url=%s" style="font-size:50px;">Install Bulletgirls for IOS</p>'
g_linkAndroid = '<a href="%s" style="font-size:50px;">Install Bulletgirls for Android</p>'

g_pathTemp = '''
<html>
<head>
<center>
<title></title>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<!--meta http-equiv="refresh" content="0;url=http://macbuild.funova.com:8080"-->
<replace/>
</center>
</head>
</html>
'''
g_autobranchPath = '<a href="http://macbuild.funova.com/autobranch/%s/index.htm" style="font-size:30px;">%s</p>'
g_packagebranchesPath = '<a href="http://macbuild.funova.com/packagebranches/Dailybuild/%s" style="font-size:30px;">%s</p>'

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

def FindFolders(dir, out, level):
    '''
    level == 0 indicate current level
    '''
    index = 0
    if not os.path.exists(dir):
        print "path not exists."
        return
    listdir = os.listdir(dir)
    for file in listdir:
        filename = os.path.join(dir, file)
        if os.path.isfile(filename):
            #
            pass
        elif os.path.isdir(filename):
            if file == ".svn":
                continue
            out.append(filename)
            if index < level:
                out = FindFiles(filename, out, index)
                pass
    return out

def FindCurrentFolders(dir, out, level):
    '''
    Get the level == 1 only
    '''
    index = 0
    if not os.path.exists(dir):
        print "path not exists."
        return
    listdir = os.listdir(dir)
    for file in listdir:
        filename = os.path.join(dir, file)
        if os.path.isfile(filename):
            #
            pass
        elif os.path.isdir(filename):
            if file == ".svn":
                continue
            if index == level:
                out.append(filename)
            else:
                out = FindFiles(filename, out, level - 1)
                pass
    return out

'''
1. 找出目录下所有的ipa
2. 判断是否有对应的plist文件
3. 有跳出; 没有，创建plist
'''
if __name__ == "__main__":
    import time
    print("begin at: %s" % (time.strftime('%Y-%m-%d -- %H:%M:%S',time.localtime(time.time()))))
    startTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    parser = argparse.ArgumentParser()
    parser.add_argument('-d')
    parser.print_help()
    args = parser.parse_known_args()[0]

    if args.d:
        g_workDir = args.d
        print g_workDir

        bResult = True
        keys_postfix = ".plist"

        files = []
        # create plist
        files = FindFiles(g_workDir + "/autobranch", files, [".ipa"])
        if files and len(files) > 0:
            for f in files:
                print f
                pfile = f[:len(f)-len(".ipa")] + keys_postfix
                # print(pfile)
                if not os.path.exists(pfile):
                    # http://macbuild.funova.com/test/Bulletgirls.ipa
                    print f
                    print pfile
                    url = "http://macbuild.funova.com" + f[len(g_workDir):]
                    print url
                    regx = "http://macbuild.funova.com/test/Bulletgirls.ipa"
                    xml = re.sub(regx, url, g_plistTemp)
                    # print xml
                    fileobj = file(pfile, "w")
                    fileobj.writelines(xml)
                    fileobj.close()
                    pass
                else:
                    print("The plist is exists.")
        # create index.htm
        files = []
        files = FindFiles(g_workDir + "/autobranch", files, [".plist", ".apk"])
        if files and len(files) > 0:
            for f in files:
                # print f
                repl = ""
                p, e = os.path.splitext(f)
                if e == ".apk":
                    repl = g_linkAndroid % ("http://macbuild.funova.com" + f[len(g_workDir):])
                elif e == ".plist":
                    repl = g_linkIOS % ("https://macbuild.funova.com" + f[len(g_workDir):])
                else:
                    print("This file is no need process: " + f)
                    continue
                p, n = os.path.split(f)
                hfile = p + "/index.htm"
                # print(hfile)
                if not os.path.exists(hfile):
                    # print(repl)
                    regx2 = re.compile("<replace/>")
                    htm = re.sub(regx2, repl, g_pinstallTemp, 1)
                    # print htm
                    fileobj = file(hfile, "w")
                    fileobj.writelines(htm)
                    fileobj.close()
                    pass
                else:
                    # print(repl)
                    regx1 = re.compile(repl)
                    fileobj = file(hfile, "r")
                    content = fileobj.read()
                    fileobj.close()
                    result1 = re.findall(regx1, content)
                    if not result1 or len(result1) <= 0:
                        regx2 = re.compile("<replace/>")
                        htm = re.sub(regx2, repl, content, 1)
                        # print htm
                        fileobj = file(hfile, "w")
                        fileobj.writelines(htm)
                        fileobj.close()
                        pass
                    else:
                        print("The download link is exists.")

        # create plist
        files = []
        files = FindFiles(g_workDir + "/packagebranches", files, [".ipa"])
        if files and len(files) > 0:
            for f in files:
                print f
                pfile = f[:len(f)-len(".ipa")] + keys_postfix
                # print(pfile)
                if not os.path.exists(pfile):
                    # http://macbuild.funova.com/test/Bulletgirls.ipa
                    print f
                    print pfile
                    url = "http://macbuild.funova.com" + f[len(g_workDir):]
                    print url
                    regx = "http://macbuild.funova.com/test/Bulletgirls.ipa"
                    xml = re.sub(regx, url, g_plistTemp)
                    # print xml
                    fileobj = file(pfile, "w")
                    fileobj.writelines(xml)
                    fileobj.close()
                    pass
                else:
                    print("The plist is exists.")
        # create index.htm
        files = []
        files = FindFiles(g_workDir + "/packagebranches", files, [".plist", ".apk"])
        if files and len(files) > 0:
            for f in files:
                # print f
                repl = ""
                bIOS = False
                p, e = os.path.splitext(f)
                if e == ".apk":
                    repl = g_linkAndroid % ("http://macbuild.funova.com" + f[len(g_workDir):])
                elif e == ".plist":
                    repl = g_linkIOS % ("https://macbuild.funova.com" + f[len(g_workDir):])
                    bIOS = True
                else:
                    print("This file is no need process: " + f)
                    continue
                p, n = os.path.split(f)
                hfile = p + "/index.htm"
                # print(hfile)
                if not os.path.exists(hfile):
                    # print(repl)
                    xx = "<replace_Android/>"
                    if bIOS:
                        xx = "<replace_IOS/>"
                        pass
                    regx2 = re.compile(xx)
                    htm = re.sub(regx2, repl, g_pinstallTemp, 1)
                    # print htm
                    fileobj = file(hfile, "w")
                    fileobj.writelines(htm)
                    fileobj.close()
                    pass
                else:
                    # print(repl)
                    regx1 = re.compile(repl)
                    fileobj = file(hfile, "r")
                    content = fileobj.read()
                    fileobj.close()
                    result1 = re.findall(regx1, content)
                    if not result1 or len(result1) <= 0:
                        xx = "<replace_Android/>"
                        if bIOS:
                            xx = "<replace_IOS/>"
                            pass
                        regx2 = re.compile(xx)
                        htm = re.sub(regx2, repl, content, 1)
                        # print htm
                        fileobj = file(hfile, "w")
                        fileobj.writelines(htm)
                        fileobj.close()
                        pass
                    else:
                        print("The download link is exists.")

        # create index.htm for folder
        folder = []
        folder = FindFolders(g_workDir + "/autobranch", folder, 0)
        if folder and len(folder) > 0:
            # g_pathTemp  <replace/>  g_linkPath
            links = []
            for f in folder:
                print f
                p, n = os.path.split(f)
                temp = g_autobranchPath % (n, n)
                links.append(temp)

            repl = "</p>\r\n".join(["%s" % (v) for v in links])
            regx2 = re.compile("<replace/>")
            htm = re.sub(regx2, repl, g_pathTemp, 1)

            fileobj = file(g_workDir + "/autobranch/index.htm", "w")
            fileobj.writelines(htm)
            fileobj.close()
            pass
        
        folder = []
        folder = FindFolders(g_workDir + "/packagebranches/Dailybuild", folder, 0)
        if folder and len(folder) > 0:
            # g_pathTemp  <replace/>  g_linkPath
            links = []
            for f in folder:
                print f
                p, n = os.path.split(f)
                temp = g_packagebranchesPath % (n, n)
                links.append(temp)

            repl = "</p>\r\n".join(["%s" % (v) for v in links])
            regx2 = re.compile("<replace/>")
            htm = re.sub(regx2, repl, g_pathTemp, 1)

            fileobj = file(g_workDir + "/packagebranches/Dailybuild/index.htm", "w")
            fileobj.writelines(htm)
            fileobj.close()
            pass

        files = []
        # create plist
        files = FindFiles(g_workDir + "/package/Manualbuild", files, [".ipa"])
        if files and len(files) > 0:
            for f in files:
                print f
                pfile = f[:len(f)-len(".ipa")] + keys_postfix
                # print(pfile)
                if not os.path.exists(pfile):
                    # http://macbuild.funova.com/test/Bulletgirls.ipa
                    print f
                    print pfile
                    url = "http://macbuild.funova.com" + f[len(g_workDir):]
                    print url
                    regx = "http://macbuild.funova.com/test/Bulletgirls.ipa"
                    xml = re.sub(regx, url, g_plistTemp)
                    # print xml
                    fileobj = file(pfile, "w")
                    fileobj.writelines(xml)
                    fileobj.close()
                    pass
                else:
                    print("The plist is exists.")
        # create index.htm
        files = []
        files = FindFiles(g_workDir + "/package/Manualbuild", files, [".plist", ".apk"])
        if files and len(files) > 0:
            for f in files:
                # print f
                repl = ""
                bIOS = False
                p, e = os.path.splitext(f)
                if e == ".apk":
                    repl = g_linkAndroid % ("http://macbuild.funova.com" + f[len(g_workDir):])
                elif e == ".plist":
                    repl = g_linkIOS % ("https://macbuild.funova.com" + f[len(g_workDir):])
                    bIOS = True
                else:
                    print("This file is no need process: " + f)
                    continue
                p, n = os.path.split(f)
                hfile = p + "/index.htm"
                # print(hfile)
                if not os.path.exists(hfile):
                    # print(repl)
                    xx = "<replace_Android/>"
                    if bIOS:
                        xx = "<replace_IOS/>"
                        pass
                    regx2 = re.compile(xx)
                    htm = re.sub(regx2, repl, g_pinstallTemp, 1)
                    # print htm
                    fileobj = file(hfile, "w")
                    fileobj.writelines(htm)
                    fileobj.close()
                    pass
                else:
                    # print(repl)
                    regx1 = re.compile(repl)
                    fileobj = file(hfile, "r")
                    content = fileobj.read()
                    fileobj.close()
                    result1 = re.findall(regx1, content)
                    if not result1 or len(result1) <= 0:
                        xx = "<replace_Android/>"
                        if bIOS:
                            xx = "<replace_IOS/>"
                            pass
                        regx2 = re.compile(xx)
                        htm = re.sub(regx2, repl, content, 1)
                        # print htm
                        fileobj = file(hfile, "w")
                        fileobj.writelines(htm)
                        fileobj.close()
                        pass
                    else:
                        print("The download link is exists.")

    else:
        print "path is None."
    
    print("end at: %s" % (time.strftime('%Y-%m-%d -- %H:%M:%S', time.localtime(time.time()))))
