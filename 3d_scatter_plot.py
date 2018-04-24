from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import csv

dataset_names = []
dataset_nums = []
with open('./dataset_name_list.txt') as dataset_name_file:
    read_names = csv.reader(dataset_name_file, delimiter=' ')
    for row in read_names:
        dataset_names.append(row[0])
        dataset_nums.append(row[1])

print(dataset_names)
print(dataset_nums)

x = []
y = []
z = []


for i in range(2,11):
    x.clear
    y.clear
    z.clear
    print('show dataset lightvec: ', i)
    i=i-2

    file_name = '../'+dataset_names[i]+'/'+dataset_nums[i]+'/lightvec.txt'
    print(file_name)
    with open(file_name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=' ')
        for row in readCSV:
            x.append(float(row[0]))
            y.append(float(row[1]))
            z.append(float(row[2]))

    fig = pyplot.figure()
    ax = Axes3D(fig)
    ax.scatter(x,y,z)
    pyplot.show()

    input('press enter to continue')
