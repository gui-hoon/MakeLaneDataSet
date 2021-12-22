import cv2
import glob
import os

mp4_path = "/home/r320/Desktop/r320-500Dset-joono/dtg_video/"
final_path = "/home/r320/Desktop/r320-500Dset-joono/cut_dtg_video/"

for mp4_file in os.listdir(mp4_path):
    cap = cv2.VideoCapture(mp4_path + mp4_file)
    count = 0
    fps =30
    print(mp4_file)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        transform_image = cv2.resize(frame, (1640, 590))
        cv2.waitKey(1)

        if int(cap.get(1) % fps == 0):
            if os.path.isdir(final_path + mp4_file) == False:
                os.mkdir(final_path + mp4_file)
            print(f"Saved image number: {int(cap.get(1))}")
            cv2.imwrite(final_path + mp4_file+'/%05d.jpg' % (fps * count), transform_image)
            count += 1