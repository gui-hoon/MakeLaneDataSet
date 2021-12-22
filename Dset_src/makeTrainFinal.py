import glob
import natsort
import numpy

############################################################## Path
jpg_path = "/home/r320/Desktop/r320_merged_Dset_20210820/"
png_path = "/home/r320/Desktop/r320_merged_Dset_20210820/laneseg_label_w16/"
txt_path = "/home/r320/Desktop/r320_merged_Dset_20210820/"
############################################################## Path
num = []
num_list = []
num_return = []
png_path_list = natsort.natsorted(glob.glob(png_path+"*/*/*.png", recursive=True))
txt_path_list = natsort.natsorted(glob.glob(txt_path+"*/*/*.txt", recursive=True))
jpg_path_list = natsort.natsorted(glob.glob(jpg_path+"*/*/*.jpg", recursive=True))

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
            num.clear()
            # print(line)
            for temp in line:
                if temp == " ":
                    break
                elif temp == ".":
                    break
                else:
                    num.append(temp)
            print(num)

            sum = 0
            is_minus = False
            for j in range(len(num)):
                num_list.clear()
                if num[j] == "-":
                    is_minus = True
                    continue
                sum += (int(num[j]) * (10 ** (len(num) - (j+1))))
            if is_minus:
               sum *= -1
            # print(f"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t{sum}")
            num_list.append(sum)

            # judge each left, right's number of zeros from saved num_list
            for tempn in num_list:
                # print(f"\t\t\t\t\t\t\t\t\t\t{tempn}")

                if tempn < mid_point:
                    left_n += 1
                else:
                    right_n += 1
            #print(left_n)
            #print(right_n)

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

f = open("/home/r320/Desktop/r320_merged_Dset_20210820/list/train.txt", "w")
for i in range(len(jpg_path_list)):
    jpg_path_list[i] = jpg_path_list[i][len(jpg_path)-1:]
    # png_path_list[i] = png_path_list[i][len(png_path)-19:]
    f.write(jpg_path_list[i] + "\n")
    # f.write(png_path_list[i] + " ")
    # number = numcalc(i)
    # f.write(number[0] + number[1] + "\n")
    num_return.clear()
f.close()
