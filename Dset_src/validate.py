import glob
import os
import cv2
import numpy as np
import sys
import natsort

def numcalc(index):
    left_n = 0
    right_n = 0
    global txt_path_list
    global num
    mid_point = 820
    # Read text and save c label in num_list in inle
    txt_data = [open(txt_path_list[index], "r")]
    if not txt_data:
        return ['0 0 0 0 0 ', '0 0 0 0 0 ']
    for data in txt_data:
        lines = data.readlines()

        for line in lines:
            line = line.split(sep=" ")
            x_coord = float(line[0])

            if x_coord < mid_point:
                left_n += 1
            else:
                right_n += 1

    # write 0, 1 after judgement
    if left_n == 0:
        num_return.append('0 0 0 0 0 ')
    elif left_n == 1:
        num_return.append('0 0 0 0 1 ')
    elif left_n == 2:
        num_return.append('0 0 0 1 1 ')
    elif left_n == 3:
        num_return.append('0 0 1 1 1 ')
    elif left_n == 4:
        num_return.append('0 1 1 1 1 ')
    elif left_n >= 5:
        num_return.append('1 1 1 1 1 ')

    if right_n == 0:
        num_return.append('0 0 0 0 0 ')
    elif right_n == 1:
        num_return.append('1 0 0 0 0 ')
    elif right_n == 2:
        num_return.append('1 1 0 0 0 ')
    elif right_n == 3:
        num_return.append('1 1 1 0 0 ')
    elif right_n == 4:
        num_return.append('1 1 1 1 0 ')
    elif right_n >= 5:
        num_return.append('1 1 1 1 1 ')
    #print(num_return)
    return num_return

if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise ValueError(f"ex) python validate <dirs path> <png_path>")

    ############################################################## Path
    jpg_path = "/Users/joono/Desktop/r320-500Dset-realjoono/"
    png_path = "/Users/joono/Desktop/png_test/"
    txt_path = "/Users/joono/Desktop/r320-500Dset-realjoono/"

    jpg_path = os.path.abspath(sys.argv[1])
    txt_path = jpg_path
    png_path = os.path.abspath(sys.argv[2])
    ############################################################## Path
    num = []
    num_list = []
    num_return = []
    png_path_list = natsort.natsorted(glob.glob(png_path + "/*/*.png", recursive=True))
    txt_path_list = natsort.natsorted(glob.glob(txt_path + "/*/*.lines.txt", recursive=True))
    jpg_path_list = natsort.natsorted(glob.glob(jpg_path + "/*/*.jpg", recursive=True))

    with open(txt_path + "/../train_gt_val.txt", "w+") as f:
        for i in range(len(png_path_list)):
            f.write(jpg_path_list[i] + " ")
            f.write(png_path_list[i] + " ")
            number = numcalc(i)
            f.write(number[0] + number[1] + "\n")
            num_return.clear()

    gt_file_path = txt_path + "/../train_gt_val.txt"
    with open(gt_file_path) as gt_file:
        while True:
            gt_line = gt_file.readline()
            if not gt_line:
                print("validation done")
                break

            gt_line = gt_line.split(sep=" ")
            jpg_img = cv2.imread(gt_line[0])
            png_img = cv2.imread(gt_line[1])
            png_img = np.uint8(png_img) * 255

            jpg_img = cv2.add(jpg_img, png_img)
            # imread
            cv2.imshow("orgin", jpg_img)
            # cv2.imshow("png", png_img)
            gt = " ".join(gt_line[2:])

            # logging
            print("jpg path: ", gt_line[0])
            print("png path: ", gt_line[1])
            print("gt      : ", gt)
            print('\n')

            # wait for entering key
            if cv2.waitKey(0) & 0xFF == 100:
                continue



