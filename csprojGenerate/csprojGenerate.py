# -*- coding: UTF-8 -*- 

'''
Copyright(c) Funova

FileName        : csprojGenerate.py
Creator         : pengpeng
Date            : 2014-12-25 11:11
Comment         : 
ModifyHistory   :

'''

__version__ = '1.0.0.0'
__author__ = 'pengpeng'

import os, sys
import re, string
import argparse

g_TestSuite     = r"csprojGenerate"
g_RootPath      = r"E:\WorkSpace\gunsoul_mobile\game\project"
g_SrcPath       = r"game-xx"
g_DstPath       = r"game-xx-logic"
g_SrcProj       = r"Assembly-CSharp-vs.csproj"
g_SrcProjTemp   = r"Assembly-CSharp-vs.csproj.template"
g_DstProj       = r"Assembly-CSharp-vs.csproj"
g_DstProjTemp   = r"Assembly-CSharp-vs.csproj.template"
g_Keywords      = r"Assets\scripts"
g_LogFile       = r"logs\csprojGenerate.log"

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

# 对于源工程文件，删掉所有的脚本(Assets\scripts)
def DelScripts(projfile):
    print 'projfile: ' + projfile
    regx = re.compile(r"<Compile Include=\"(Assets\\scripts\\.+\.cs)\" />")

    scriptscount = 0
    lines = open(projfile, 'r').readlines()
    if len(lines) > 0:
        for index in xrange(0, len(lines) - 1):
            # print lines[index]
            if len(lines[index].replace(" ", "").replace("\n", "").replace("\r", "")) > 0:
                if 'Assets\\scripts\\' in lines[index]:
                    # print(lines[index])
                    pass
                # print(lines[index])
                results = re.findall(regx, lines[index])
                if results and len(results) > 0:
                    # print results[0]
                    scriptscount = scriptscount + 1
                    # print(lines[index])
                    lines[index] = ""
                    pass
                elif "game-xx/Assets/plugins/ICSharpCode.SharpZipLib.dll" in lines[index]:
                    lines[index] = "<HintPath>..\game-xx\Assets\plugins\ICSharpCode.SharpZipLib.dll</HintPath>"
                    pass
                else:
                    lines[index] = lines[index].replace('UNITY_STANDALONE_WIN', 'UNITY_ANDROID')
                    lines[index] = lines[index].replace('ENABLE_PROFILER_WIN', 'ENABLE_PROFILER')
                    lines[index] = lines[index].replace(';UNITY_EDITOR', '')
                    lines[index] = lines[index].replace(';UNITY_EDITOR_WIN', '')
                pass
        pass
    print "Total delete scripts count: %s"  % scriptscount
    # print projfile[:-len(".template")]
    # open(projfile[:-len(".template")], 'w').writelines(lines)
    print projfile
    open(projfile, 'w').writelines(lines)
    pass

# 对于目的工程文件，添加所有的脚本(Assets\scripts)
# E:\workspace\gunsoul_mobile\game\project\game-xx-logic\Assets\scripts\video\VideoManager.cs
# <Compile Include="Assets\scripts\GameResourcePreLoader.cs" />
def AddScripts(projfile, scripts):
    linetemp = r'<Compile Include="%s" />'
    lines = []
    for script in scripts:
        path = script[len(g_RootPath + g_DstPath) + 2:]
        line = linetemp % path
        # print line
        lines.append(line)

    content = open(projfile, 'r').read()
    open(projfile[:-len(".template")], 'w').write(content % ("\n\t".join(lines)))
    pass

if __name__ == "__main__":
    import time
    print("begin at: %s" % (time.strftime('%Y-%m-%d -- %H:%M:%S',time.localtime(time.time()))))
    startTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    parser = argparse.ArgumentParser()
    parser.add_argument('-d')
    parser.add_argument('-srcproj')
    parser.add_argument('-dstproj')
    parser.print_help()
    args = parser.parse_known_args()[0]

    if args.d:
        g_RootPath      = args.d
        g_SrcPath       = args.srcproj
        g_DstPath       = args.dstproj
        srcprojfile     = g_RootPath + "\\" + g_SrcPath + "\\" + g_SrcProj
        dstprojfile     = g_RootPath + "\\" + g_DstPath + "\\" + g_DstProjTemp
        print srcprojfile
        print dstprojfile

        if os.path.exists(srcprojfile):
            DelScripts(srcprojfile)
            pass

        if os.path.exists(dstprojfile):
            files = []
            files = FindFiles(g_RootPath + "\\" + g_DstPath + "\\Assets\\scripts", files, [".cs", ".js"])
            print len(files)
            AddScripts(dstprojfile, files)
            pass

    else:
        print "path is None."
    
    print("end at: %s" % (time.strftime('%Y-%m-%d -- %H:%M:%S', time.localtime(time.time()))))
