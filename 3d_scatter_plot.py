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

    def read_lightvec(self,dataset_num):
        lightvec = []
        i = dataset_num
        #for i in range(2,11):
        lightvec.clear()
        self.clear_xyz()
        print('show dataset lightvec: ', i)
        i=i-2
        file_name = '../'+self.dataset_names[i]+'/'+self.dataset_nums[i]+'/lightvec.txt'
        file_name = './lightvec.txt'
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
                lightvec.append([x,y,z])
        #self.plot()
        #print('lightvec:\n',lightvec)

        self.lightvec = np.asarray(lightvec)
        print('lightvec.shape: ',self.lightvec.shape)
        print(self.lightvec)

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
        #print(self.dome_points)
        print('dome_points shape: ',self.dome_points.shape)
        #self.plot()

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
    obj.dome(1.0,310)
    obj.read_lightvec(2)
    #obj.icosahegron()
