import glob
import os
import cv2
import numpy as np
import natsort
import sys


if __name__ == "__main__":

    if len(sys.argv) < 2:

        raise ValueError(f"ex) python flip.py <dir to flip>")


    working_dir_path = os.path.abspath(sys.argv[1])

    flip_dir_path = working_dir_path + "_flip"


    if not os.path.isdir(flip_dir_path):

        print(f"mkdir {flip_dir_path}")

        os.makedirs(flip_dir_path)


    print(f"working dir: {working_dir_path}")

    print(f"flip    dir: {flip_dir_path}")


    mp4_dirs = os.listdir(working_dir_path)


    # MP4 file들을 이용해서 반복문 들어가기

    for path_file in mp4_dirs:

        final_dir_path = flip_dir_path + "/" + path_file

        abs_path_file = working_dir_path + "/" + path_file


        # MP4에 있는 txt를 모두 호출하여 리스트에 넣는다.

        lines_data = [file for file in os.listdir(abs_path_file) if file.endswith(".lines.txt")]

        jpg_data = [file for file in os.listdir(abs_path_file) if file.endswith(".jpg")]


        print(len(lines_data))

        print(len(jpg_data))


        line_jpg_data = list(zip(lines_data, jpg_data))


        # read MP4의 lines.txt file and flip 

        for data in line_jpg_data:

            with open(abs_path_file + "/" + data[0], "r") as line_file:

                zero_one_image = np.zeros((590, 1640), np.uint8) # 저장될 이미지 선언

                lines = line_file.readlines()


            if not os.path.isdir(final_dir_path):

                # mkdir을 이용해 하위디렉토리까지 모두 만든다.

                os.mkdir(final_dir_path)


            # convert line string and write txt

            with open(flip_dir_path + '/' + path_file + '/' + data[0], "w") as f:

                for line in lines:

                    line = line.split(sep=" ")

                    locates = list(map(float, line[:-1]))


                    for i in range(0, len(locates), 2):

                        locates[i] = round(1640 - locates[i], 3)


                    final_path = flip_dir_path + '/' + data[0]

                    

                    for i in locates:

                        f.write(str(i)+" ")

                    f.write("\n")


            image = cv2.imread(working_dir_path + "/" + path_file + '/' + data[1])

            filp_image = cv2.flip(image, 1)

            cv2.imwrite(flip_dir_path + "/" + path_file + "/" + data[1], filp_image)


            print(f"final_path jpg: {flip_dir_path + '/' + path_file + '/' + data[1]}")

            print(f"final_path txt: {flip_dir_path + '/' + path_file + '/' + data[0]}")