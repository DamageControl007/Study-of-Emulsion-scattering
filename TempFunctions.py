#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 11:42:17 2022

@author: somendrasinghjadon
"""

file_path = open("normpath.txt","a")
file_path.write("Hello"+"\t")
file_path.write("name"+"\t")
file_path.write("Age"+"\t")
file_path.write("\n")
file_path.write("(path/itr)"+"\t")
file_path.write("str(front/itr)"+"\t")
file_path.write("str(back/itr)"+"\t")
file_path.close()