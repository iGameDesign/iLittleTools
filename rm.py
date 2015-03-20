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

g_workDir = "/Volumes/Work/www"

if __name__ == "__main__":
    import time
    print("begin at: %s" % (time.strftime('%Y-%m-%d -- %H:%M:%S',time.localtime(time.time()))))

    parser = argparse.ArgumentParser()
    parser.add_argument('-d')
    parser.print_help()
    args = parser.parse_known_args()[0]

    if args.d:
        g_workDir = args.d
        print g_workDir

        files = []
        files = FindFiles(g_workDir + "/autobranch", files, [".htm"])
        files = FindFiles(g_workDir + "/packagebranches", files, [".htm"])
        for f in files:
            print f
            os.remove(f)    

    print("end at: %s" % (time.strftime('%Y-%m-%d -- %H:%M:%S', time.localtime(time.time()))))
