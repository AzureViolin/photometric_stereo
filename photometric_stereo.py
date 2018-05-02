from light_vector_resampler import LightVectorResampler
from denominator_finder import DenominatorFinder
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import scipy.io

for dataset_num in range(1,2):
    sample_points_num = 100
    ##==== resample light vectors =====
    lvres_obj = LightVectorResampler(dataset_num)
    lvres_obj.dome(1.0,sample_points_num) # 310 is the magic number here to get 306 sample points
    lvres_obj.read_lightvecs(dataset_num) # 2 means dataset2. works from 2-10.
    lvres_obj.resample() # lvres_obj.resampled_points is a 2xN array, with the first column being the resampled picture ID
    print (lvres_obj.resampled_points)

    ##==== find and show denominator imagbe=====
    name_list = np.array(lvres_obj.resampled_points)
    pil_img = Image.open(lvres_obj.dataset_path+'image0001.bmp')
    img_width, img_height = pil_img.size
    dataset_name = lvres_obj.dataset_names[dataset_num-1]
    df_obj = DenominatorFinder(name_list , lvres_obj.dataset_path, dataset_name, img_size=[img_height,img_width])
    df_obj.load_image()
    idx, name = df_obj.denominatorfind()
    print("denominator name: ", name, 'index: ', idx)
    #plt.imshow(df_obj.load_image(idx))
    #plt.show()
    ##==== initial normal vector estimation=====
    df_obj.read_lightvecs()
    print(df_obj.name_len)
    df_obj.matrix_build(name, idx)

    ##==== save normal vector to .mat format =====
    scipy.io.savemat('./normal_dataset'+str(dataset_num)+'.mat',mdict={'normal_dataset'+str(dataset_num) : df_obj.normal_mat})
