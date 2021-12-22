import glob
import os
import cv2
import numpy as np
import sys

def numcalc(txt_data):
    left_n = 0
    right_n = 0
    mid_point = 820
    max_lines = 10

    # Read text and save c label in num_list in inle
    if not txt_data:
        pass

    for line in txt_data:
        line = line.split(sep=" ")
        x_coord = float(line[0])

        if x_coord < mid_point:
            left_n += 1
        else:
            right_n += 1

    start_label = max_lines // 2 + 1 - left_n
    end_label = max_lines // 2 + right_n

    #print(num_return)
    return start_label, end_label

# image에다가 라인을 그려주는 함수이다.
def drawAndWriteline(image, point_list, label):
    for i in range(len(point_list)-1):
    # 임의로 밝기를 보기 편하게 255로 설정
    # 저장을 할때에는 밝기를 1로 줄여주어야 한다.
        image = cv2.line(image, tuple(np.int32(point_list[i])), tuple(np.int32(point_list[i+1])), label, 16)

    return image

if __name__ == "__main__":

    if len(sys.argv) < 3:
        raise ValueError("example: python convert_txt2png.py <line.txt dir> <label target dir>")

    working_dir_path = os.path.abspath(sys.argv[1])
    labels_path = os.path.abspath(sys.argv[2])
    mp4_dirs = os.listdir(working_dir_path)

    print(working_dir_path)
    print(labels_path)
    print(mp4_dirs)

    # if there is no dir then, make dirs
    if not os.path.isdir(labels_path):
        print("[INFO] make dirs" + labels_path)
        os.makedirs(labels_path)

    # MP4 file들을 이용해서 반복문 들어가기
    for path_file in mp4_dirs:
        abs_path_file = working_dir_path + "/" + path_file
        final_dir_path = labels_path + "/" + path_file

        # MP4에 있는 txt를 모두 호출하여 리스트에 넣는다.
        # print(path_file+"/*.lines.txt")
        abs_lines_data = [file for file in glob.glob(abs_path_file+"/*.lines.txt", recursive=True)]
        lines_data = [file for file in os.listdir(abs_path_file) if file.endswith(".lines.txt")]

        # MP4의 txt파일 들을 한개씩 반복
        for data in zip(abs_lines_data, lines_data):
            if not os.path.isfile(data[0]):
                raise FileNotFoundError(f"not found {data[0]}")                

            with open(data[0], "r") as lane_data:
                zero_one_image = np.zeros((590, 1640), np.uint8) # 저장될 이미지 선언
                lines = lane_data.readlines()

                start_label, end_label = numcalc(lines)
                label = start_label
                for line in lines:
                    result = []
                    locates = []
                    line = line.split(sep=" ")

                    locates = list(map(float, line[:-1]))
                    for i in range(0, len(locates), 2):
                        result.append((locates[i], locates[i+1]))

                    # label validation
                    if 1 <= label <= 10:
                        zero_one_image = drawAndWriteline(zero_one_image, result, label)
                    else:
                        print(f"error file : {data[0]}")

                    label += 1
                    locates.clear()
                    result.clear()


                final_path = final_dir_path + '/' + data[1][:-10] + ".png"
                print(f"final_path png: {final_path}")
                print(f"final_path dir: {final_dir_path}")
                cv2.imwrite(final_path, zero_one_image)

                # 만약 dir의 경로가 존재하지 않는다면
                if not os.path.isdir(final_dir_path):
                    # mkdir을 이용해 하위디렉토리까지 모두 만든다.
                    os.mkdir(final_dir_path)
                    cv2.imwrite(final_path, zero_one_image)
                # 아닐 경우
                else:
                    # 그 디렉토리에 저장.
                    cv2.imwrite(final_path, zero_one_image)

