import cv2

image = cv2.imread("/home/r320/Downloads/CUlane_dataset/laneseg_label_w16/driver_23_30frame/05151640_0419.MP4/04380.png")

print(image.shape)

for i in range(590):
    for j in range(1640):
        print(image[i][j][0], end="")
    print("")