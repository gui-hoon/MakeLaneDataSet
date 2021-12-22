import glob
import cv2
import natsort
import numpy as np
import sys
import os

def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global result
        global locates
        global jpg_name_list
        cv2.circle(img, (x, y), 5, (255, 0, 0), -1)
        # print(x, y)
        locates.append([x, y])
        if len(locates) == 2:
            print(locates)
            m = (locates[1][1] - locates[0][1])/(locates[1][0] - locates[0][0])
            n = locates[0][1] - (m * locates[0][0])
            # Set Y dim range
            if locates[1][1] <= 240:
                lim = 240

            else:
                lim = locates[1][1]

            for i in range(590, lim-10, -10):
                re = round((i - n)/m, 3)
                result.append([re, i])
            locates = []

            line_data = tuple(map(tuple, np.int32(result)))
            cv2.line(img, (line_data[0]), (line_data[-1]), (255, 0, 0), 8)
            if result:
                for item in result:
                    f.write(f"{item[0]} {item[1]}")
                    f.write(" ")
            f.write("\n")
            print(result)
            result = []

    elif event == cv2.EVENT_RBUTTONDOWN:
        global curv_line
        global curv_locate
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        curv_locate.append([x, y])

        # joono
        for n in range(len(curv_locate) - 1):
            # line equation
            m = (curv_locate[n + 1][1] - curv_locate[n + 0][1]) / (curv_locate[n + 1][0] - curv_locate[n + 0][0])
            nL = curv_locate[n + 0][1] - (m * curv_locate[n + 0][0])

        # orig
        if len(curv_locate) == 5:
            for n in range(4):
                # line equation
                m = (curv_locate[n + 1][1] - curv_locate[n + 0][1]) / (curv_locate[n + 1][0] - curv_locate[n + 0][0])
                nL = curv_locate[n + 0][1] - (m * curv_locate[n + 0][0])

                if n == 0:
                    for i in range(590, curv_locate[n+1][1] - 1, -10):
                        x_coord = round((i - nL)/m, 3)
                        curv_line.append([x_coord, i])
                        cv2.circle(img, (int(x_coord), i), 3, (255, 0, 255), 1)
                else:
                    for i in range((curv_locate[n][1] // 10) *10- 10, curv_locate[n+1][1] - 1, -10):
                        x_coord = round((i - nL) / m, 3)
                        curv_line.append([x_coord, i])
                        cv2.circle(img, (int(x_coord), i), 3, (255, 0, 255), 1)

            # poliyline
            # cv2.polylines(img, np.array(curv_line, dtype=np.int32), False, (255, 0, 255), 16)

            line_data = tuple(map(tuple, curv_line))
            # cv2.line(img, np.int32(line_data[n+0]), np.int32(line_data[n+1]), (255, 0, 255), 16)

            print(line_data)
            line_data = np.array(line_data, dtype=np.int32)

            cv2.polylines(img, [line_data], False, (255, 0, 255), 8)
            if line_data.any():
                for item in line_data:
                    f.write(f"{item[0]} {item[1]}")
                    f.write(" ")
            f.write("\n")
            curv_locate = []
            curv_line = []

if __name__ == "__main__":
    # gao
    # if len(sys.argv) < 2:
        # raise ValueError("example: python drawLine.py <working dir>")

    ############################################################## Path
    path = os.path.abspath("/home/r320ws/Desktop/guihoon/modify")
    # path = "C:\\Users\\201710858\\Desktop\\500Dset\\r320-500Dset-woo\\20201027_173014_N.m4v\\"
    ############################################################## Path
    locates = []
    result = []
    cycle = 0
    curv_locate = []
    curv_line = []
    # 4815 create
    path = path+"/"

    print(path)
    jpg_name_list = natsort.natsorted(glob.glob(path+"/*.jpg", recursive=True))
    print(jpg_name_list)
    images = [cv2.imread(i) for i in jpg_name_list]

    for img in images:
        # Text file open
        txtname = jpg_name_list[cycle][len(path):-4]
        # txt Path setting
        f = open(path+txtname+".lines.txt", "w+")
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', draw_circle)
        cv2.line(img, (0, 240), (1639, 240), (0, 255, 0), 2)
        while (1):
            cv2.imshow('image', img)
            if cv2.waitKey(20) & 0xFF == 100:
                cycle += 1
                break
        print(path+txtname)
        print(f"{len(jpg_name_list)- cycle} left...")
        f.close()
    # close image when all images are processed
    cv2.destroyAllWindows()

















