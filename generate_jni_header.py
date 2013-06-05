#!/usr/bin/env python

import os

java_src_path = "../src"
classes_path = "../bin/classes"
jni_src_path = "../jni"
list = []

def find_src():
    arg = "-rl --include=*.java \"native\" " + java_src_path
    pipe = os.popen("grep " + arg)
    while True:
        line = pipe.readline()
        if line != '':
            list.append(line)
        else:
            break
        
def process_jni():
    for src in list:
        file = os.path.basename(src)
        package = src[len(java_src_path) + 1 : len(src) - len(file) - 1].replace('/', '.')
        class_name = package + "." + file
        class_name = class_name[:len(class_name) - 6]
        print("Generate jni header:" + class_name)
        command = "javah -classpath " + classes_path + " -d " + jni_src_path + " " + class_name
        os.system(command)

if __name__ == '__main__':
    find_src()
    process_jni()
    