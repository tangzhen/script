#!/usr/bin/env python

import os

class jni_module:
    def __init__(self):
        self.module_name = ""
        self.module_path = ""
        self.is_source_folder = False
        self.is_header_folder = False
        self.header_list = []
        self.source_list = []       

header_postfix = ('.h')
source_postfix = ('.c', '.cpp', '.cxx')
exclude_dirs = ('tests', 'cmake', 'CMakeFiles')

root_path = "../jni"
makefile_name = "Android.mk"
android_makefile = root_path + "/" + makefile_name
fileinfo = open(android_makefile, 'w')

local_module = ""
module_list = []

def process_module(module, dir):
    dir_list = dir.split("/")
    
    index = dir_list.index(os.path.basename(root_path))
    name = ""
    for i in range(index, len(dir_list)):
        name += dir_list[i]
        if ((i + 1) != len(dir_list)):
            name += "_"
            
    module.module_name = name.replace(dir_list[index], local_module)
    module.module_path = dir.replace(root_path, "$(LOCAL_PATH)")

def walk_dir(dir, topdown=True):
    for root, dirs, files in os.walk(dir, topdown):
        if root.endswith(exclude_dirs):
            continue
        
        module_item = jni_module()
        process_module(module_item, root)
        
        if root == root_path:
            temp = ""
        else:
            temp = root.replace(root_path + "/", "") + "/"
        
        for name in files:
            if name.endswith(source_postfix):
                module_item.source_list.append(temp +  name)
                module_item.is_source_folder = True
            if name.endswith(header_postfix):
                module_item.header_list.append(temp + name)
                module_item.is_header_folder = True

        if module_item.is_source_folder and module_item.is_header_folder:
            module_list.append(module_item)

def write_header():
    fileinfo.write("LOCAL_PATH := $(call my-dir)")
    fileinfo.write("\n\n")
    fileinfo.write("include $(CLEAR_VARS)")
    fileinfo.write("\n\n")
    
def write_footer():
    fileinfo.write("LOCAL_LDLIBS    := -llog")
    fileinfo.write("\n")
    fileinfo.write("LOCAL_MODULE    := " + local_module)
    fileinfo.write("\n\n")
    fileinfo.write("include $(BUILD_SHARED_LIBRARY)")

def generate():
    print("Generate Android Makefile : " + android_makefile)
    write_header()
    walk_dir(root_path)

    for item in module_list:
        fileinfo.write(item.module_name + " = \\\n")
        for source in item.source_list:
            fileinfo.write("\t" + source)
            if ((item.source_list.index(source) + 1) != item.source_list.__len__()):
                fileinfo.write(" \\\n")
            else:
                fileinfo.write("\n")

        fileinfo.write("\n")

    fileinfo.write("LOCAL_SRC_FILES := \\\n")
    for item in module_list:
        fileinfo.write("\t$(" + item.module_name + ")")
        if ((module_list.index(item) + 1) != module_list.__len__()):
            fileinfo.write(" \\\n")
        else:
            fileinfo.write("\n")
        
    fileinfo.write("\n")

    fileinfo.write("LOCAL_C_INCLUDES := \\\n")
    for item in module_list:
        fileinfo.write("\t" + item.module_path)
        if ((module_list.index(item) + 1) != module_list.__len__()):
            fileinfo.write(" \\\n")
        else:
            fileinfo.write("\n")
            
    fileinfo.write("\n\n")
    write_footer()

if __name__ == '__main__':
    local_module = input('Please enter module name:')
    generate()
