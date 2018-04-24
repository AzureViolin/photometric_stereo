from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import csv
import math

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

    def plot(self):
        for i in range(2,11):
            self.x.clear()
            self.y.clear()
            self.z.clear()
            print('show dataset lightvec: ', i)
            i=i-2
            file_name = '../'+self.dataset_names[i]+'/'+self.dataset_nums[i]+'/lightvec.txt'
            print(file_name)
            with open(file_name) as csvfile:
                readCSV = csv.reader(csvfile, delimiter=' ')
                for row in readCSV:
                    self.x.append(float(row[0]))
                    self.y.append(float(row[1]))
                    self.z.append(float(row[2]))
            fig = pyplot.figure()
            ax = Axes3D(fig)
            ax.scatter(self.x,self.y,self.z)
            pyplot.show()
            input('press enter to continue')
            fig.clf()

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
        self.original_12_vertices = [
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
                ]
        self.original_20_face_mid_points = [
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
                ]
        print('t =',self.t)
        print('a =',self.a)
        print('b =',self.b)
        print('c =',self.c)
        print('d =',self.d)
        print('cc =',self.cc)
        print('dd =',self.dd)
        print(self.original_20_face_mid_points)

        self.x.clear()
        self.y.clear()
        self.z.clear()
        fig.clf()
        for row in self.original_20_face_mid_points:
            self.x.append(float(row[0]))
            self.y.append(float(row[1]))
            self.z.append(float(row[2]))
        fig = pyplot.figure()
        ax = Axes3D(fig)
        ax.scatter(self.x,self.y,self.z)
        pyplot.show()
        input('press Enter to see verticies:')
        fig.clf()
        self.x.clear()
        self.y.clear()
        self.z.clear()
        for row in self.original_12_vertices:
            self.x.append(float(row[0]))
            self.y.append(float(row[1]))
            self.z.append(float(row[2]))
        print(len(self.x))
        fig = pyplot.figure()
        ax = Axes3D(fig)
        ax.scatter(self.x,self.y,self.z)
        pyplot.show()


if __name__=="__main__":
    obj = LightVector()
    obj.plot()
    #obj.icosahegron()
