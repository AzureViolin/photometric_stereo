#!/usr/bin/env python
# coding=utf-8
'''
Author:Tai Lei
Date:Thursday, April 26, 2018 PM02:36:19 HKT
Info:
'''

import os
import sys
import numpy as np
from PIL import Image
import pickle
import cv2
import matplotlib.pyplot as plt
from scipy.stats import rankdata
import csv

class DenominatorFinder():
    def __init__(self, name_list, root_path, dataset_name, img_size=[224,224], print_flag = False):
        self.name_list = name_list
        self.root_path = root_path
        self.name_len = len(name_list)
        self.img_size = img_size
        self.imgs = np.zeros([self.name_len]+self.img_size, dtype=np.int32)
        self.ranks = np.zeros([self.name_len]+self.img_size, dtype=np.int32)
        self.dataset_name = dataset_name
        self.print = print_flag

    def load_image(self, idx=None):
        if idx:
            img = np.array(Image.open(os.path.join(self.root_path, "image"+str(self.name_list[self.denominator_idx]).zfill(4)+".bmp")).convert('L'))
            return img
        else:
            for i,item in enumerate(self.name_list):
                img = np.array(Image.open(os.path.join(self.root_path, "image"+str(item).zfill(4)+".bmp")).convert('L'))
                self.imgs[i,:,:] = img[:,:]

    def denominatorfind(self):
        imgs_flatten = self.imgs.reshape(self.name_len, -1)
        ranks_flatten = self.ranks.reshape(self.name_len, -1)

        for i in range(self.img_size[0]*self.img_size[1]):
            ranks_flatten[:,i] = rankdata(imgs_flatten[:,i], method='min')

        rank_70_flag = (ranks_flatten>self.name_len*0.7)
        rank_70_counts = np.sum(rank_70_flag, axis=1)
        rank_70_mean = np.sum(rank_70_flag*ranks_flatten, axis=1) / rank_70_counts
        self.denominator_idx = np.argmax((rank_70_mean<self.name_len*0.9)*rank_70_counts)
        return self.denominator_idx, self.name_list[self.denominator_idx]

    def read_lightvecs(self):
        lightvecs = []
        self.x = []
        self.y = []
        self.z = []
        with open(os.path.join(self.root_path, 'lightvec.txt'),"r") as csvfile:
            readCSV = csv.reader(csvfile, delimiter=' ')
            for (i, row) in enumerate(readCSV):
                x = float(row[0])
                y = float(row[1])
                z = float(row[2])
                self.x.append(x)
                self.y.append(y)
                self.z.append(z)
                lightvecs.append([x,y,z])

        self.lightvecs = np.array(lightvecs)

    def matrix_build(self, denominator_name, denominator_idx):
        self.mat = np.zeros((self.img_size[0], self.img_size[1], self.name_len-1, 3), dtype=np.float32)
        self.normal_mat = np.zeros((self.img_size[0], self.img_size[1], 3), dtype=np.float32)
        print('mat.shape: ',self.mat.shape)
        print('normal_mat.shape: ',self.normal_mat.shape)
        print('denominator_name:', denominator_name)
        l2 = self.lightvecs[denominator_name]
        print('l2: ',l2)
        ratio_list = list(self.name_list[:])
        print('ratio_list before remove: ',ratio_list)
        print('ratio_list len: ',len(ratio_list))
        ratio_list.remove(denominator_name)
        print('ratio_list after remove: ',ratio_list)
        print('ratio_list len: ',len(ratio_list))
        for row in range(self.img_size[0]):
            print('Computing SVD for '+self.dataset_name+' row ', row)
            for col in range(self.img_size[1]):
                I2 = self.imgs[denominator_idx][row][col]
                if self.print == True :
                    print('!!!!!!!!!!!!!!!!!!!!!!!!! row ',row,' col ', col)
                    print('I2: ',I2)
                for (i, item) in enumerate(ratio_list):
                    #if item != denominator_name:
                    I1 = self.imgs[i][row][col]
                    l1 = self.lightvecs[item]
                    self.mat[row][col][i][:]=I1*l2-I2*l1
                        #self.mat[row][col][i][1]=I1*l2[1]-I2*l1[1]
                        #self.mat[row][col][i][2]=
                    self.normal_mat[row][col] = np.linalg.svd(self.mat[row][col])[2][2]
                    if self.print == True :
                        print('i = ', i, ' item = ', item)
                        print('I1: ',I1)
                        print('l1: ',l1)
                        print('self.mat[',row,'][',col,'][',i,'][:] is:\n',self.mat[row][col][i][:])
                        print('self.mat[',row,'][',col,'] is:\n',self.mat[row][col])
                        print('np.linalg.svd(self.mat[row][col]):\n',np.linalg.svd(self.mat[row][col]))
                        print('np.linalg.svd(self.mat[row][col])[2]:\n',np.linalg.svd(self.mat[row][col])[2])
                        print('np.linalg.svd(self.mat[row][col])[2][2]:\n',np.linalg.svd(self.mat[row][col])[2][2])
        #print (self.normal_mat)
        #with open("normal_mat.pickle", "wb") as output_file:
        #    pickle.dump(self.normal_mat, output_file)

if __name__=="__main__":
    name_list_path="./resample_list.pickle"
    root_path="../data08_teapot/data08/"
    pil_img = Image.open(root_path+'image0001.bmp')
    img_width, img_height = pil_img.size
    img_size = [img_height, img_width]

    with open(name_list_path,"rb") as f:
        name_list = np.array(pickle.load(f))


    obj = DenominatorFinder(name_list, root_path, dataset_name = 'data08_teapot', img_size=img_size, print_flag = False)
    obj.load_image()

    ##==== find and show denominator imagbe=====
    idx, name = obj.denominatorfind()
    print("denominator name: ", name)
    #plt.imshow(obj.load_image(idx))
    #plt.show()

    ##==== initial normal vector estimation=====
    obj.read_lightvecs()
    print('name_list:\n',obj.name_list)
    print('name_len: ',obj.name_len)
    obj.matrix_build(name, idx)
    import scipy.io
    scipy.io.savemat('./normal_test.mat',mdict={'normal':obj.normal_mat})
