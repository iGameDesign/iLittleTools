#coding=utf8

'''
Copyright(c) Funova

FileName        : QHMServerTest.py
Creator         : pengpeng
Date            : 2014-12-25 11:11
Comment         : 
ModifyHistory   :
    1. svn up
    2. modify server\Config\config_operator.lua
    3. run the Robot

'''

__version__ = '1.0.0.0'
__author__ = 'pengpeng'

import os
import sys
import re
import string
import csv
import argparse
import subprocess

g_TestSuite     = r"QHMServerTest"
g_RootPath      = r"E:\WorkSpace\gunsoul_mobile\game\project\server"
g_LogPath       = r"log"
g_LogFile       = r"logs/QHMServerTest.log"
g_ConfigFile    = r'Config/config_operator.lua'

g_RobotIndex    = 1
g_RobotCount    = 20
g_ServerID      = 32
g_WorldIP       = '192.168.1.132'

g_strRepl       = '''
Center.open             = false 
Logic.open              = false
World.open              = false
Battle.open             = false
Cross.open              = false
Client.open             = false
Gateway.open            = false

Client.open             = true

-- robot client config
Client.open             = true
client_robot.userExt    = {%s, %s}
client_robot.serverId   = %s

--cfg.clientRobot.worldip = '123.59.33.192'
cfg.clientRobot.worldip = '%s'
'''

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
        return Nil
    pass

def RunRobot():
    return doCMD("svn info %s" % (g_RootPath))

if __name__ == "__main__":
    import time
    print("begin at: %s" % (time.strftime('%Y-%m-%d -- %H:%M:%S',time.localtime(time.time()))))
    startTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    parser = argparse.ArgumentParser()
    parser.add_argument('-r')
    parser.add_argument('-robotindex')
    parser.add_argument('-robotcount')
    parser.add_argument('-serverid')
    parser.add_argument('-worldip')
    parser.print_help()
    args = parser.parse_known_args()[0]

    if args.r:
        g_RootPath      = args.r
        g_RobotIndex    = args.robotindex
        g_RobotCount    = args.robotcount
        g_ServerID      = args.serverid
        g_WorldIP       = args.worldip

        # modify config file
        g_ConfigFile = g_RootPath + os.sep + g_ConfigFile
        print g_ConfigFile
        content = open(g_ConfigFile, 'r').read()
        content = content + g_strRepl % (g_RobotIndex, g_RobotCount, g_ServerID, g_WorldIP)
        print content
        open(g_ConfigFile, 'w').write(content)

        # run the Robot
        # cmd = subprocess.Popen('cd ' + g_RootPath, shell = True, stdout = subprocess.PIPE)
        # temp = cmd.communicate()
        # cmd = subprocess.Popen('dir ', shell = True, stdout = subprocess.PIPE)
        # temp = cmd.communicate()
        # os.system('%s\\NXServer_x64_Debug.exe %s\\Lua main %s\\Log NXServer 1' % (g_RootPath, g_RootPath, g_RootPath))
        # os.system('NXServer_x64_Debug.exe Lua main Log NXServer 1')
        # cmd = subprocess.Popen('NXServer_x64_Debug.exe Lua main Log NXServer 1', shell = True, stdout = subprocess.PIPE)
        # print 'Running...'

        endTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    else:
        print "path is None."
    
    print("end at: %s" % (time.strftime('%Y-%m-%d -- %H:%M:%S', time.localtime(time.time()))))
    print("exit 1")