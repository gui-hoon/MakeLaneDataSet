import glob
import os
import cv2
import numpy as np
import natsort

def drawAndWriteline(image, point_list:list):
    point_list = tuple(map(tuple, point_list))
    for line in point_list:
        if line[0] > 0:
        # 
        # 
            image = cv2.line(image, tuple(np.int32(line)), tuple(np.int32(point_list[-1])), (255,255,255), 10)
            break
    return image
    # 
    # 
    # if (os.path.isdir('/2020') == False):
    #     os.mkdir('/2020')

path_dir = natsort.natsorted(glob.glob("/home/r320/Desktop/r320-CUlane/driver_23_30frame/*"))
dir_list = os.listdir("/home/r320/Desktop/asdf/png_test/")
# final path is /home/r320/Desktop/asdf/label/png_test/~.MP4/~.png

# 
locates = []
result = []
temp = ""
tmp = []

# 
file_list = [file for file in path_dir]

#
for path_file in file_list:
    # 
    current_dir_path = path_file
    my_string = current_dir_path
    # 
    idx = my_string.find('driver_23_30frame')
    final_dir_path = my_string[:idx] + 'laneseg_label_w16/' + my_string[idx:] + '/'
    # 
    # print(final_dir_path)

    # 
    lines_data = [file for file in natsort.natsorted(glob.glob(path_file+"/*.lines.txt"))]

    # 
    for data in lines_data:
        # 
        current_file_path = data
        my_string = current_file_path
        idx = my_string.find('driver_23_30frame')
        # 
        final_path = my_string[:idx] + 'laneseg_label_w16/' + my_string[idx:len(my_string)-10]
        # 
        print(final_path)
        # 
        lane_data = open(data, 'r')
        # print(lane_data)
        zero_one_image = np.zeros((590, 1640), np.uint8) #
        lines = lane_data.readlines()
        # 
        for line in lines:
            # print(line)
            for coordinate in line:
                if coordinate == " ":
                    locates.append(int(float(temp)))
                    temp = ""
                elif coordinate == "\n":
                    break
                else:
                    temp += coordinate
            for i in range(0, len(locates), 2):
                result.append([locates[i], locates[i+1]])
            # print(locates)
            locates.clear()
            # 
            zero_one_image = drawAndWriteline(zero_one_image, result)
            result.clear()
        #
        if os.path.isdir(final_dir_path) == False:
            # 
            os.makedirs(final_dir_path)
            cv2.imwrite(final_path+'.png', zero_one_image)
        # 
        else:
            # 
            cv2.imwrite(final_path+'.png', zero_one_image)