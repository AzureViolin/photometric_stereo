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

class DenominatorFinder():
    def __init__(self, name_list, root_path, img_size=[224,224]):
        self.name_list = name_list
        self.root_path = root_path
        self.name_len = len(name_list)
        self.img_size = img_size
        self.imgs = np.zeros([self.name_len]+self.img_size, dtype=np.int32)
        self.ranks = np.zeros([self.name_len]+self.img_size, dtype=np.int32)
        self.load_image()

    def load_image(self, idx=None):
        if idx:
            img = np.array(Image.open(self.root_path+str(self.name_list[self.denominator_idx]).zfill(4)+".bmp").convert('L'))
            return img
        else:
            for i,item in enumerate(self.name_list):
                img = np.array(Image.open(self.root_path+str(item).zfill(4)+".bmp").convert('LA'))
                self.imgs[i,:,:] = img[:,:,0]

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


if __name__=="__main__":
    name_list_path="./resample_list.pickle"
    root_path="../data02_tile1/data02/image"
    img_size = [110, 124]
    with open(name_list_path,"rb") as f:
        name_list = np.array(pickle.load(f))[:,0]

    obj = DenominatorFinder(name_list, root_path, img_size=img_size)
    idx, name = obj.denominatorfind()
    print("denominator name: ", name)
    plt.imshow(obj.load_image(idx))
    plt.show()
