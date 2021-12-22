from abc import abstractproperty
import glob
import os
import cv2
import numpy as np
import sys
import natsort

if __name__ == "__main__":

    if len(sys.argv) < 2:
        raise ValueError("example: python 4lane_list.py <line.txt dir>")

    working_dir_path = os.path.abspath(sys.argv[1])
    mp4_dirs = os.listdir(working_dir_path)

    for path_file in mp4_dirs:
        abs_path_file = working_dir_path + "/" + path_file

        print(abs_path_file)

        # MP4에 있는 txt를 모두 호출하여 리스트에 넣는다.
        abs_lines_data = [file for file in natsort.natsorted(glob.glob(abs_path_file+"/*.lines.txt", recursive=True))]
        lines_data = [file for file in natsort.natsorted(os.listdir(abs_path_file)) if file.endswith(".lines.txt")]

        print(len(abs_lines_data))
        print(len(lines_data))
        print("+=================================================================================")

        # MP4의 txt파일 들을 한개씩 반복
        for data in zip(abs_lines_data, lines_data):
            print(data[1])

            if not os.path.isfile(data[0]):
                raise FileNotFoundError(f"not found {data[0]}")

            with open(data[0], "r") as lane_data:
                zero_one_image = np.zeros((590, 1640), np.uint8) # 저장될 이미지 선언
                lines = lane_data.readlines()

                all_lines = []
                for line in lines:
                    line = line.split(sep=" ")[:-1]
                    all_lines.append(list(map(float, line)))


                a = sorted(all_lines, key=lambda x: x[0])
                # natsort.natsorted(all_lines[:][0])
                # print(a)

                for line in a:
                    print(line[0], end=" ")
                print("")

                left_lines = []
                right_lines = []
                for line in a:
                    if line[0] < 820:
                        left_lines.append(line)
                    else:
                        right_lines.append(line)

                four_lanes = []

                line_limit = 2
                line_cnt = 0
                for i in range(1, len(left_lines)+1):
                    four_lanes.insert(0, left_lines[len(left_lines)-i])
                    line_cnt += 1

                    if line_cnt >= 2:
                        break
                
                line_cnt = 0
                for i in range(len(right_lines)):
                    four_lanes.append(right_lines[i])
                    line_cnt += 1

                    if line_cnt >= 2:
                        break


                # if len(left_lines) > 0 and len(right_lines) > 0:
                #     if len(left_lines) >= 2 and len(right_lines) >= 2:
                #         four_lanes.append(left_lines[-2])
                #         four_lanes.append(left_lines[-1])
                #         four_lanes.append(right_lines[0])
                #         four_lanes.append(right_lines[1])
                #     elif len(left_lines) == 1 and len(right_lines) == 2:  
                #         four_lanes.append(left_lines[-1])
                #         four_lanes.append(right_lines[0])
                #         four_lanes.append(right_lines[1])
                #     elif len(left_lines) == 2 and len(right_lines) == 1:  
                #         four_lanes.append(left_lines[-2])
                #         four_lanes.append(left_lines[-1])
                #         four_lanes.append(right_lines[0])
                #     elif len(left_lines) == 1 and len(right_lines) == 1:  
                #         four_lanes.append(left_lines[-1])
                #         four_lanes.append(right_lines[0])

                f = open(f"{abs_path_file}/{data[1]}", "w+")
                for i in four_lanes:
                    for num in i:
                        f.write(f"{num}")
                        f.write(" ")
                    f.write("\n")
                f.close()

                # raise RuntimeError

                
