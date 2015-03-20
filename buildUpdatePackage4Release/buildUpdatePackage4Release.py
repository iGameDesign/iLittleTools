# -*- coding: UTF-8 -*- 

'''
Copyright(c) Funova

FileName        : buildUpdatePackage4Release.py
Creator         : pengpeng
Date            : 2014-12-25 11:11
Comment         : 
ModifyHistory   :
Description     : 
	1. Generate 
	2. Copy zip file to update server
	3. Unzip

'''

__version__ = '1.0.0.0'
__author__ = 'pengpeng'

import os, sys
import string
import re
import argparse
import md5, hashlib
from ftplib import FTP

g_TestSuite         = r"buildUpdatePackage4Release"
g_RootPath          = r"E:\workspace\gunsoul_mobile\game\project\game-xx"
g_ScriptsDllPath    = r"Assets\resourcex\gamelogic"

g_LogFile           = r"logs\buildUpdatePackage4Release.log"

g_updatefilename    = "update.ini"
g_resourcemetatable = "resources.metatable"
g_platform          = "android"
g_version           = "0.1.%s"
g_ResourceType      = 14 #bytes
g_smbAddress        = r"\\gscdn.funova.com\update"

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

def convert( inputfile, outputfile, in_enc = "gbk", out_enc="UTF8" ):  
    try:
        #print "convert " + inputfile,  
        content = open(inputfile).read()
        new_content = content.decode(in_enc).encode(out_enc)        
        open(outputfile, 'w').write(new_content)
    except Exception,e:
        print "convert error:", inputfile
        print e

def ftp_upload(filename): 
    ftp = FTP()
    ftp.set_debuglevel(2)#打开调试级别2，显示详细信息;0为关闭调试信息
    ftp.connect('192.168.0.1','21')#连接
    ftp.login('admin','admin')#登录，如果匿名登录则用空串代替即可
    #print ftp.getwelcome()#显示ftp服务器欢迎信息
    #ftp.cwd('xxx/xxx/') #选择操作目录
    bufsize = 1024#设置缓冲块大小
    file_handler = open(filename,'rb')#以读模式在本地打开文件
    ftp.storbinary('STOR %s' % os.path.basename(filename),file_handler,bufsize)#上传文件
    ftp.set_debuglevel(0)
    file_handler.close()
    ftp.quit()
    print "ftp up OK"

def smb_upload(filename, smb_address):
    path, name = os.path.split(filename)

    open(smb_address + "\\" + name, 'wb').write(open(filename, 'rb').read())
    print "smb upload OK"

#'''
if __name__ == "__main__":
    import time
    print("begin at: %s" % (time.strftime('%Y-%m-%d -- %H:%M:%S',time.localtime(time.time()))))
    startTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    parser = argparse.ArgumentParser()
    parser.add_argument('-d') # tab file dir
    parser.add_argument('-p') # platform

    parser.print_help()
    args = parser.parse_known_args()[0]

    if args.d:
        g_RootPath      = args.d
        g_platform      = args.p
        print g_RootPath

        postfix1 = ".assetbundle"
        dlls = []
        upfiles = []

        ScriptsDllFileName = g_RootPath + '\\' + g_ScriptsDllPath + '\\' + g_ScriptsDllFile

        # rename
        # content = open(ScriptsDllFileName).read()
        # open(ScriptsDllFileName + '.assetbundle', 'w').write(content)
        # os.rename(ScriptsDllFileName, ScriptsDllFileName + '.assetbundle')
        dlls.append(ScriptsDllFileName)

        metadatas = []
        for file in dlls:
            print file
            tfilename = 'gamelogic' + '_' + os.path.split(file)[1] #[:-len(postfix1)]
            print tfilename
            f = open(file, 'rb')
            m = hashlib.md5()
            m.update(f.read())
            f.close()
            md5 = m.hexdigest()
            fsize = os.path.getsize(file)
            metadata = "%s|%s|%s|%s|" % (tfilename, g_ResourceType, md5.upper(), fsize)
            # print metadata
            metadatas.append(metadata)

            out = os.path.split(file)[0] + '\\' + 'gamelogic' + '_' + os.path.split(file)[1] + '.assetbundle'
            open(out, 'wb').write(open(file, 'rb').read())
            upfiles.append(out)

        outstring = g_platform + ";" + ";".join(metadatas)
        # print outstring
        open(g_RootPath + '\\' + g_ScriptsDllPath + "\\" + g_resourcemetatable, "w").write(outstring)

        upfiles.append(g_RootPath + '\\' + g_ScriptsDllPath + "\\" + g_resourcemetatable)

        # 获取子版本号
        path = g_smbAddress + "\\" + g_platform + "\\" + g_updatefilename
        f = open(path, 'r')
        content = f.read()
        print content
        f.close()
        regx = re.compile(r"index=(\d+)")
        results = re.findall(regx, content)
        print results[0]

        # 修改子版本号
        regx2 = re.compile(r"upVer=(.+)")
        subversion = (int(results[0]) + 1)
        g_version = g_version % subversion
        content = re.sub(regx2, r"upVer=%s" % g_version, content)
        content = re.sub(regx, r"index=%s" % subversion, content)
        print content
        f = open(path, 'w')
        f.write(content)
        f.close()

        # 上传ftp
        # files = []
        # files = FindFiles(g_RootPath + '\\' + g_ScriptsDllPath, files, [".assetbundle", ".metatable"])
        for file in upfiles:
            # ftp_upload(file)
            print file
            path = g_smbAddress + "\\" + g_platform + "\\assets\\" + g_version
            print path
            if not os.path.exists(path):
                os.mkdir(path)
                pass
            smb_upload(file, g_smbAddress + "\\" + g_platform + "\\assets\\" + g_version)
    else:
        print "path is None."
    
    print("end at: %s" % (time.strftime('%Y-%m-%d -- %H:%M:%S', time.localtime(time.time()))))
#'''
