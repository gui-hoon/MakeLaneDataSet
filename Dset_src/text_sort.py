from abc import abstractproperty
import glob
import os
import cv2
import numpy as np
import sys
import natsort
from tqdm import tqdm

if __name__ == "__main__":

    if len(sys.argv) < 2:
        raise ValueError("example: python text_sort.py <line.txt dir>")

    working_dir_path = os.path.abspath(sys.argv[1])
    mp4_dirs = os.listdir(working_dir_path)

    for path_file in mp4_dirs:
        abs_path_file = working_dir_path + "/" + path_file

        # MP4에 있는 txt를 모두 호출하여 리스트에 넣는다.
        abs_lines_data = [file for file in natsort.natsorted(glob.glob(abs_path_file+"/*.lines.txt", recursive=True))]
        lines_data = [file for file in natsort.natsorted(os.listdir(abs_path_file)) if file.endswith(".lines.txt")]


        # MP4의 txt파일 들을 한개씩 반복
        for data in tqdm(zip(abs_lines_data, lines_data)):

            if not os.path.isfile(data[0]):
                raise FileNotFoundError(f"not found {data[0]}")

            with open(data[0], "r") as lane_data:
                zero_one_image = np.zeros((590, 1640), np.uint8) # 저장될 이미지 선언
                lines = lane_data.readlines()

                all_lines = []
                for line in lines:
                    line = line.split(sep=" ")[:-1]
                    all_lines.append(list(map(float, line)))


                sorted_lanes = sorted(all_lines, key=lambda x: x[0])


                f = open(f"{abs_path_file}/{data[1]}", "w+")
                for line in sorted_lanes:
                    for num in line:
                        f.write(f"{num}")
                        f.write(" ")
                    f.write("\n")
                f.close()


                
