# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 23:03:26 2022

@author: 805
"""

import xml.etree.ElementTree as ET
from pydicom import dcmread
from pydicom.data import get_testdata_files
from os.path import join
import os, fnmatch


def get_xml_researchgroup(xml_dir): # 拆解XML架構，以取出目標標籤內容，並回傳。
    tree = ET.ElementTree(file=xml_dir) # 將XML拆解為結構樹
    root = tree.getroot()   # 取得根標籤

    for elem in tree.iter(tag='researchGroup'):
            # print("elemt",elem.text)
            attribute=elem.text # 將搜尋到符合條件的標籤內容以文字取出
    return attribute
            
def add_researchgroup_to_dcm(dcm_dir,attribute): # 將標籤內容寫入DCM檔案中
    ds=dcmread(dcm_dir)
    # try:
    #     t=ds[0x0008,0x1080]
    #     x=input("the tag has been exist, do you want to recover?(y/n)")
    # except:
    #     x="y"
        
    # if x!="y" or x!="Y":
    #     return 0
    
    ds.add_new([0x0008,0x1080], 'LO', attribute)
    
    p=dcm_dir.split("/")
    o=p[-1]
    u="/"+o[:15]+o[-18:-4] # 取出檔名前面的patient id 與末端識別碼
    c=os.path.abspath(os.getcwd()) # 取得程式碼當前之路徑
    c=c.replace("\\", "/")
    if os.path.isdir(c+u): # 如果此目錄已存在，就直接將資料存入
        ds.save_as(c+u+"/"+o)
    else:
        os.makedirs(c+u)
        ds.save_as(c+u+"/"+o)
    return ds[0x0008,0x1080] 
        
def findSome(nPath, fTypes, txtFile): # 搜尋所有副檔名為定類型的檔案
    allFiles = []
    for dirs, subdirs, files in os.walk( nPath ):
        for extension in ( tuple(fTypes) ):
            for filename in fnmatch.filter(files, extension):
                filepath = os.path.join(dirs, filename)		
                if os.path.isfile( filepath ):
                    allFiles.append(filepath)
                    # print(filepath)
    
    # 把結果存檔，以供驗證
    f = open( txtFile,'w',encoding='utf-8' ) 
    for i in allFiles:
        print(f'{i}',file=f)
    f.close()
    
    return allFiles  # 傳回這個list


def search_file(path): # 找到所有符合搜尋條件的dcm檔案
    p=path.split("/")
    if len(p)>3:    # 檢查xml 的檔案深度，已決定搜尋的種子點位置
        n=len(p)-3
    else:
        n=0
    x=""
    for i in range(n):
        x+=(p[i]+"/")
    path=x
    
    text1='result.txt' # 設定結果儲存檔名
    filetypes=['*.dcm'] # 設定搜尋副檔名類型
    retsome=findSome(path, filetypes, text1)
    if len(retsome)==0:
        n=0
        x=""
        for i in range(n):
            x+=(p[i]+"/")
        path=x
        retsome=findSome(path, filetypes, text1)
        
        if len(retsome)==0:
# =============================================================================
            # choose DCM file
            target_dcm_list = list(filedialog.askopenfilenames(
                filetypes = (("DICOM files","*.DCM"),("all files","*.*")), 
                title="Choose DICOM file")) # 會儲存檔案路徑, list
            return len(retsome),len(target_dcm_list),target_dcm_list
# =============================================================================

    dir_file_txt=open('result.txt','r')
    dir_file=dir_file_txt.read()
    dir_file=dir_file.replace("\\","/")
    dir_file_list=dir_file.split("\n")
    
    
    target_dcm_list=[]
    
    for i in dir_file_list: # 將所有的dcm檔逐個取出，比對末端識別碼，是否符合篩選條件
        if i[-10:-4]==p[-1][-10:-4]:
            target_dcm_list.append(i)
            
    if len(retsome):
        return len(retsome),len(target_dcm_list),target_dcm_list

def check_and_move_xml(xml_path,dcm_num): # 檢查添加完標籤的檔案數量，與原始檔案數量是否相符
    p=xml_path.split("/")                 # 如果相符，就將xml檔案移至其下方自動產生的已完成子目錄
    o=p[-1]
    u="/"+o[:15]+o[-18:-4]
    c=os.path.abspath(os.getcwd())
    c=c.replace("\\", "/")
    xml_dir=""
    for i in p[:-1]:
        xml_dir=xml_dir+i+"/" 
    new_dcm_dir=c+u
    initial_count = 0
    for path in os.listdir(new_dcm_dir):
        if os.path.isfile(os.path.join(new_dcm_dir, path)):
            initial_count += 1
    if  initial_count==dcm_num:
        if os.path.isdir(xml_dir+"have_been_done/"):
            os.replace(xml_path,xml_dir+"have_been_done/"+o)
        else:
            os.makedirs(xml_dir+"have_been_done/")
            os.replace(xml_path,xml_dir+"have_been_done/"+o)
    return new_dcm_dir


print(os.path.dirname(os.path.realpath(__file__)))







