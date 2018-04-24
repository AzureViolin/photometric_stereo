from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import csv

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
            self.x.clear
            self.y.clear
            self.z.clear
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

if __name__=="__main__":
    obj = LightVector()
    obj.plot()
