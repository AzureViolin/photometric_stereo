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
    def __init__(self, name_list, root_path, dataset_name, img_size=[224,224]):
        self.name_list = name_list
        self.root_path = root_path
        self.name_len = len(name_list)
        self.img_size = img_size
        self.imgs = np.zeros([self.name_len]+self.img_size, dtype=np.int32)
        self.ranks = np.zeros([self.name_len]+self.img_size, dtype=np.int32)
        self.dataset_name = dataset_name

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
        #self.mat = np.zeros((self.img_size[0], self.img_size[1], self.name_len-1, 3), dtype=np.float32)
        self.mat = np.zeros((self.img_size[0], self.img_size[1], self.name_len, 3), dtype=np.float32)
        self.normal_mat = np.zeros((self.img_size[0], self.img_size[1], 3), dtype=np.float32)
        l2 = self.lightvecs[denominator_name]
        #print ('l2: ',l2)
        ratio_list = list(self.name_list[:])
        #ratio_list.remove(denominator_name)
        ratio_list_len = len(ratio_list)
        I_mat = np.zeros(( ratio_list_len,1), dtype=np.float32)
        L_mat = np.zeros(( ratio_list_len,3), dtype=np.float32)
        print('L_mat shape', L_mat.shape)
        print('ratio_list len: ',ratio_list_len)
        print('ratio_list: \n',ratio_list)
        for row in range(self.img_size[0]):
            print('Computing SVD for '+self.dataset_name+' row ', row)
            for col in range(self.img_size[1]):
                #print('col = ', col)
                I2 = self.imgs[denominator_idx][row][col]
                #print ('I2: ',I2)
                for (i, item) in enumerate(ratio_list):
                    #print('i = ', i, ' item = ', item)
                    #if item != denominator_name:
                    if i<denominator_idx:
                        j=i
                    else:
                        j=i+1
                        j=i
                    I1 = self.imgs[j][row][col]
                    I_mat[j] = self.imgs[j][row][col]
                    #print ('I1: ',I1)
                    l1 = self.lightvecs[item]
                    #print ('l1: ',l1)
                    L_mat[j] = self.lightvecs[item]
                    self.mat[row][col][i][:]=I1*l2-I2*l1
                    #print ('I1*l2-I2*l1:\n',I1*l2-I2*l1)
                        #self.mat[row][col][i][1]=I1*l2[1]-I2*l1[1]
                        #self.mat[row][col][i][2]=
                L_T = np.transpose(L_mat)
                LTL = L_T.dot(L_mat)
                #print('LTL shape: ',LTL.shape)
                #print('LTL: ',LTL)
                LTL_inv = np.linalg.inv(LTL)
                #print('LTL_inv shape: ',LTL_inv.shape)
                #print('LTL_inv : ',LTL_inv)
                LTI = L_T.dot(I_mat)
                #print('LTI shape: ',LTI.shape)
                #print('LTI : ',LTI)
                G = LTL_inv.dot(LTI)
                #print('G: \n',G)
                kd = np.linalg.norm(G)
                #print('kd: ',kd)
                N = G/kd
                #print('N: ',N)
                #print('L_mat:\n',L_mat)
                #print('L_T :\n',L_T)
                #U,S,V = np.linalg.svd(self.mat[row][col])
                #self.normal_mat[row][col] = V[2]
                self.normal_mat[row][col] = N.reshape(3)
                #print ('self.mat[row][col] shape: ',self.mat[row][col].shape)
                #print ('self.mat[row][col]: \n',self.mat[row][col])
                #print ('u shape ',U.shape)
                #print ('u content:\n ',U)
                #print ('s shape ',S.shape)
                #print ('s content:\n ',S)
                #print ('v shape ',V.shape)
                #print ('v content:\n',V)
                #print ('N.reshape   : ', N.reshape(3))
                #print ('v[2] content: ',V[2])
                #print ('v[:,2] content:\n',V[:,2])
        #print (self.normal_mat)
        #with open("normal_mat.pickle", "wb") as output_file:
        #    pickle.dump(self.normal_mat, output_file)

if __name__=="__main__":
    name_list_path="./resample_list.pickle"
    root_path="../data02_tile1/data02/"
    img_size = [110, 124]
    with open(name_list_path,"rb") as f:
        name_list = np.array(pickle.load(f))


    obj = DenominatorFinder(name_list, root_path, dataset_name = 'data02_tile1', img_size=img_size)
    obj.load_image()

    ##==== find and show denominator imagbe=====
    idx, name = obj.denominatorfind()
    print("denominator name: ", name)
    #plt.imshow(obj.load_image(idx))
    #plt.show()

    ##==== initial normal vector estimation=====
    obj.read_lightvecs()
    print(obj.name_list)
    print(obj.name_len)
    obj.matrix_build(1718, 5)
    #import scipy.io
    #scipy.io.savemat('./normal.mat',mdict={'normal':obj.normal_mat})
