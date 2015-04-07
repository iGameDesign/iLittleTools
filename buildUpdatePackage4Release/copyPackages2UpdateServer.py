# -*- coding: UTF-8 -*- 

'''
Copyright(c) Funova

FileName        : copyPackages2UpdateServer.py
Creator         : pengpeng
Date            : 2014-12-25 11:11
Comment         : 
ModifyHistory   :
Description     : 
	1. mount_smbfs //gscdn.funova.com/update /mnt_update
	2. Generate the version number
	3. Copy zip file to update server
	4. Unzip to the right folder with right version

	source: ${GameXDirAndroidm}/Assets/StreamingAssets
	target: /mnt_update/android/assets/0.0.1
			/mnt_update/android/update.ini

'''

__version__ = '1.0.0.0'
__author__ = 'pengpeng'

import os, sys
import string
import re
import argparse
import md5, hashlib
from ftplib import FTP
import subprocess

g_TestSuite         = r"copyPackages2UpdateServer"
g_RootPath          = r"E:\workspace\gunsoul_mobile\game\project\game-xx"

g_LogFile           = r"logs\copyPackages2UpdateServer.log"

g_version           = "0.0.%s"

# resource 
g_ResourcePath		= r"Assets/StreamingAssets"
g_resourcemetatable = "resources.metatable"

# version for update server
g_smbAddress        = r"\\gscdn.funova.com\update"
g_platform          = "android2"
g_updatefilename    = "update.ini"

# version for client
g_ConfigsPath		= r"Assets/resourcex/configs"
g_ClientConfig		= "GameConfig.cfg"
g_ClientVersion		= "version.cfg"


def FindFiles(dir, out, filter = []):
    if not os.path.exists(dir):
        print "path not exists."
        return
    listdir = os.listdir(dir)
    for file in listdir:
        filename = os.path.join(dir, file)
        if os.path.isfile(filename):
            ext = os.path.splitext(filename)[1]
            # print ext
            if filter == [] or(filter and ext.lower() in filter) or ext == '':
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

	open(smb_address + "/" + name, 'wb').write(open(filename, 'rb').read())
	# print "smb upload OK"

def doCMD(arg):
	'''
	Run a shell command.
	'''
	print "==>", arg
	cmd = subprocess.Popen(arg, shell = True, stdout = subprocess.PIPE)
	temp = cmd.communicate()
	# print temp
	temp = temp[0]
	regx = re.compile(r": (\d+)")
	results = re.findall(regx, temp)
	if len(results) > 2:
		return results[1]
	else:
		return Null
	pass

def GetVersion():
	return doCMD("svn info %s" % (g_RootPath))

#'''
if __name__ == "__main__":
    import time
    print("begin at: %s" % (time.strftime('%Y-%m-%d -- %H:%M:%S',time.localtime(time.time()))))
    startTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    parser = argparse.ArgumentParser()
    parser.add_argument('-s') # source file dir
    parser.add_argument('-d') # destination file dir
    parser.add_argument('-p') # platform

    parser.print_help()
    args = parser.parse_known_args()[0]

    if args.d:
        g_RootPath		= args.s
        g_smbAddress	= args.d
        g_platform      = args.p
        print g_RootPath, g_smbAddress, g_platform
        # g_platform		= "android2"

        upfiles = []

        # 修改客户端的版本号
        path_1 = g_RootPath + '/' + g_ConfigsPath + '/' + g_ClientConfig
        path_2 = g_RootPath + '/' + g_ConfigsPath + '/' + g_ClientVersion
        regx_1 = re.compile(r"BUILDVERSION=(.+)")
        regx_2 = re.compile("\"svnVersion\":\"(.+)\"")

        f = open(path_2, 'r')
        content = f.read()
        f.close()
        results = re.findall(regx_2, content)
        print results
        if results and len(results) > 0:
            subversion = results[0]
            g_version = g_version % subversion
            print "\"svnVersion\":\"%s\"" % subversion

            # 修改update上的版本号
            path = g_smbAddress + "/" + g_platform + "/" + g_updatefilename
            f = open(path, 'r')
            content = f.read()
            # print content
            f.close()
            regx = re.compile(r"index=(\d+)")
            regx2 = re.compile(r"upVer=(.+)")
            # results = re.findall(regx, content)
            # print results[0]
            # subversion = (int(results[0]) + 1)
            # g_version = g_version % subversion
            content = re.sub(regx2, r"upVer=%s" % g_version, content)
            content = re.sub(regx, r"index=%s" % subversion, content)
            # print content
            f = open(path, 'w')
            f.write(content)
            f.close()

            # 上传ftp
            # print g_RootPath
            upfiles = FindFiles(g_RootPath + '/' + g_ResourcePath, upfiles, [])
            path = g_smbAddress + "/" + g_platform + "/assets/" + g_version
            # print path
            if upfiles and len(upfiles) > 0:
                print len(upfiles)
                for file in upfiles:
                    # ftp_upload(file)
                    # print file
                    if not os.path.exists(path):
                        os.mkdir(path)
                        pass
                    smb_upload(file, path)
                pass
        
    else:
        print "path is None."
    
    print("end at: %s" % (time.strftime('%Y-%m-%d -- %H:%M:%S', time.localtime(time.time()))))
#'''
