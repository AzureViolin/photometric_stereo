from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import csv
import math
import numpy as np

class LightVector():
    def __init__(self):
        self.dataset_names = []
        self.dataset_nums = []
        with open('./dataset_name_list.txt') as dataset_name_file:
            read_names = csv.reader(dataset_name_file, delimiter=' ')
            for row in read_names:
                self.dataset_names.append(row[0])
                self.dataset_nums.append(row[1])
        print(self.dataset_names)
        print(self.dataset_nums)
        self.x = []
        self.y = []
        self.z = []

    def read_lightvecs(self,dataset_num):
        lightvecs = []
        i = dataset_num
        #for i in range(2,11):
        #self.clear_xyz()
        print('show dataset lightvecs: ', i)
        i=i-2
        file_name = '../'+self.dataset_names[i]+'/'+self.dataset_nums[i]+'/lightvec.txt'
        #file_name = './lightvec.txt'
        print(file_name)
        with open(file_name) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=' ')
            for row in readCSV:
                x = float(row[0])
                y = float(row[1])
                z = float(row[2])
                self.x.append(x)
                self.y.append(y)
                self.z.append(z)
                lightvecs.append([x,y,z])
        #self.plot()
        #print('lightvecs:\n',lightvecs)

        self.lightvecs = np.asarray(lightvecs)
        print('lightvecs.shape: ',self.lightvecs.shape)
        #print(self.lightvecs)

    def clear_xyz(self):
        self.x.clear()
        self.y.clear()
        self.z.clear()

    def plot(self):
        fig = pyplot.figure()
        ax = Axes3D(fig)
        ax.scatter(self.x,self.y,self.z)
        pyplot.show()
        #input('press enter to continue')
        #fig.clf()

    def dome(self, r, num_of_points):
        area = 4 * math.pi * r * r / (2 * num_of_points)
        d = math.sqrt(area)
        self.dome_point_max_dist_from_each_other = d / 2.0
        Mv = math.floor(math.pi * r / d)
        dv = math.pi * r / Mv
        dphi = area / dv
        self.dome_points = np.array([])
        points = []
        self.clear_xyz()
        for m in range(0,math.floor(Mv / 2)):
            v = math.pi * (m + 0.5) / Mv
            Mphi = math.floor (2 * math.pi * math.sin(v) * r / dphi)
            for n in range(0, Mphi):
                phi = 2 * math.pi * n / Mphi
                x = r * math.sin(v) * math.cos(phi)
                y = r * math.sin(v) * math.sin(phi)
                z = r * math.cos(v)
                points.append([x,y,z])
                self.x.append(x)
                self.y.append(y)
                self.z.append(z)

        self.dome_points = np.asarray(points)
        print('dome_points shape: ',self.dome_points.shape)
        #print(self.dome_points)
        #self.plot()

    def resample(self):
        print('dome_points.shape: ',self.dome_points.shape)
        print('lightvecs.shape: ',self.lightvecs.shape)
        #for lightvec in lightvecs:
        #    for dome_point in dome_points:
        self.resampled_points = []
        len_dome_points = self.dome_points.shape[0]
        len_lightvecs = self.lightvecs.shape[0]
        shortest_dist = self.dome_point_max_dist_from_each_other
        shortest_lightvec_num = -1
        shortest_dome_point_num = -1
        found = False
        for i in range(0,len_dome_points):
            for j in range(0,len_lightvecs):
                dist = np.linalg.norm(self.lightvecs[j]-self.dome_points[i])
                if dist < shortest_dist :
                    shortest_dome_point_num = i
                    shortest_lightvec_num = j
                    shortest_dist = dist
                    found = True

            if found == True :
                #print('current i,j: ',i,j)
                #print('shortest_dome_point_num: ',shortest_dome_point_num)
                #print('shortest_lightvec_num: ',shortest_lightvec_num)
                #print('shortest_dist: ',shortest_dist)
                #print('max_dist: ',self.dome_point_max_dist_from_each_other)
                self.resampled_points.append([shortest_lightvec_num + 1,shortest_dome_point_num])
                found = False
                shortest_lightvec_num = -1
                shortest_dome_point_num = -1
                shortest_dist = self.dome_point_max_dist_from_each_other
        #print(self.resampled_points)
        #print(np.asarray(self.resampled_points))
        print('resammpled_points shape: ',np.asarray(self.resampled_points).shape)


    def icosahegron(self):
        self.t = (1 + math.sqrt(5))/2
        self.a = math.sqrt(self.t)/math.pow(5,1/4)
        self.b = 1/(math.sqrt(self.t) * math.pow(5,1/4))
        self.c = self.a + 2 * self.b
        self.d = self.a + self.b
        self.cc = 1/self.b
        self.dd = math.pow(self.t,3/2)/math.pow(5,1/4)
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        self.original_12_vertices = np.array([
                [ 0, -a, -b],
                [ 0, -a,  b],
                [ 0,  a, -b],
                [ 0,  a,  b],
                [-b,  0, -a],
                [-b,  0,  a],
                [ b,  0, -a],
                [ b,  0,  a],
                [-a, -b,  0],
                [-a,  b,  0],
                [ a, -b,  0],
                [ a,  b,  0],
                ])
        self.original_20_face_mid_points = np.array([
                [-d, -d, -d],
                [-d, -d,  d],
                [-d,  d, -d],
                [-d,  d,  d],
                [ d, -d, -d],
                [ d, -d,  d],
                [ d,  d, -d],
                [ d,  d,  d],
                [ 0, -a, -c],
                [ 0, -a,  c],
                [ 0,  a, -c],
                [ 0,  a,  c],
                [-c,  0, -a],
                [-c,  0,  a],
                [ c,  0, -a],
                [ c,  0,  a],
                [-a, -c,  0],
                [-a,  c,  0],
                [ a, -c,  0],
                [ a,  c,  0],
                ])
        self.original_20_face_mid_points = self.original_20_face_mid_points / 3.0
        print('t =',self.t)
        print('a =',self.a)
        print('b =',self.b)
        print('c =',self.c)
        print('d =',self.d)
        print('cc =',self.cc)
        print('dd =',self.dd)
        print(self.original_20_face_mid_points)

        self.clear_xyz()
        for row in self.original_20_face_mid_points:
            self.x.append(float(row[0]))
            self.y.append(float(row[1]))
            self.z.append(float(row[2]))

        self.plot()
        self.clear_xyz()
        for row in self.original_12_vertices:
            self.x.append(float(row[0]))
            self.y.append(float(row[1]))
            self.z.append(float(row[2]))
        print(self.original_12_vertices)
        self.plot()

        # to keep using this method requires build a mesh datastructure
        # which I prefer not to do at this moment.
        kk = self.original_20_face_mid_points[0]
        length = kk[0] ** 2 + kk[1] ** 2 + kk[2] ** 2
        print(length)

if __name__=="__main__":
    obj = LightVector()
    #obj.icosahegron()
    obj.dome(1.0,310) # 310 is the magic number here to get 306 sample points
    obj.read_lightvecs(2) # 2 means dataset2. works from 2-10.
    obj.resample() # obj.resampled_points is a 2xN array, with the first column being the resampled picture ID
