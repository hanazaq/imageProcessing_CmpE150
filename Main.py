
# return img, nested list
def read_ppm_file(f):
    fp = open(f)
    fp.readline()  # reads P3 (assume it is P3 file)
    lst = fp.read().split()
    n = 0
    n_cols = int(lst[n])
    n += 1
    n_rows = int(lst[n])
    n += 1
    max_color_value = int(lst[n])
    n += 1
    img = []
    for r in range(n_rows):
        img_row = []
        for c in range(n_cols):
            pixel_col = []
            for i in range(3):
                pixel_col.append(int(lst[n]))
                n += 1
            img_row.append(pixel_col)
        img.append(img_row)
    fp.close()
    return img, max_color_value


# Works
def img_printer(img):
    row = len(img)
    col = len(img[0])
    cha = len(img[0][0])
    for i in range(row):
        for j in range(col):
            for k in range(cha):
                print(img[i][j][k], end=" ")
            print("\t|", end=" ")
        print()


filename = input()
operation = int(input())


# DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE


def choose_operation(num,lst):
    if num == 1:
        #first input new min
        #second input new max
        #absloute value for old min is 0
        img_printer(min_max_normalization(lst, int(input()), int(input()), 0, max_color_value))
    if num == 2:
        img_printer(z_normalization(lst))
    if num == 3:
        img_printer(black_white(lst))
    if num == 4:
        #first input filter file
        #second input stride
        img_printer(convolution(lst, filter(f"./{input()}"), int(input())))
    if num==5:
        # first input filter file
        # second input stride
        img_printer(convolution_pad_zeros(lst,filter(f"./{input()}"),int(input())))
    if num == 6:
        rows = len(lst)
        cols = len(lst[0])
        # int input is the quantized range
        # row-1, col-1 in order to keep inside the index of the lst
        img_printer(rec_print(rows - 1, cols - 1, lst, rows, cols, int(input())))
    if num == 7:
        rows = len(lst)
        cols = len(lst[0])
        # int input is the quantized range
        img_printer(result(rows, cols, lst, int(input())))

# operation one function
def min_max_normalization(lst, new_min, new_max, old_min, old_max):
    #iterate over each element in the 3d lst of the img
    for a in range(len(lst)):
        for b in range(len(lst[a])):
            for c in range(len(lst[a][b])):
                #apply equation to each element
                new_value = ((lst[a][b][c] - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
                #format to only 4 decimal numbers after the .
                lst[a][b][c] = float("{:.4f}".format(new_value))
    return lst
#operation two function
def z_normalization(lst):
    mean_value_channels = []
    deviation_value_channels = []

    for k in range(3): #[red, green, blue]
        mean_value = 0 #mean value for each channel
        for i in range(len(lst)):
            for j in range(len(lst)):
                mean_value += lst[i][j][k]
        mean_value = mean_value / (len(lst) ** 2)
        mean_value_channels.append((mean_value))


    for k in range(3): #[red, green, blue]
        deviation_value = 0
        for i in range(len(lst)):
            for j in range(len(lst)):
                #calculate deviation for each channel
                deviation_value += (lst[i][j][k] - mean_value_channels[k]) ** 2
        deviation_value = (deviation_value / (len(lst)) ** 2) ** 0.5
        deviation_value_channels.append(deviation_value + (10 ** (-6)))

    for k in range(3): #[red, green, blue]
        for i in range(len(lst)): #rows
            for j in range(len(lst)): #cols
                z = (lst[i][j][k] - mean_value_channels[k]) / deviation_value_channels[k]
                lst[i][j][k] = float("{:.4f}".format(z)) # update the elements in the lst
    return lst
# operation three function
def black_white(lst):
    for a in range(len(lst)): #rows
        for b in range(len(lst[a])): #cols
            sum = 0 #sum of the red, green, blue values of a single pixle
            for c in range(3): #[red, green, blue]
                sum += lst[a][b][c]

            # the value of red and green and blue is the same now = the average of the given red , green, blue values
            lst[a][b] = [int(sum / 3)] * 3
    return lst

# operation four functions
def filter(file):
    #read the content of the filter file
    fp = open(file)
    my_filter = fp.read() #save the content of the file as a string in my_filter variable
    fp.close()
    my_filter = my_filter.split("\n") #my_filter is now a list of strings (each line is represented as a string)
    lst_filter = []
    for i in my_filter:
        my_lst=[]
        for item in i.split(" "): #i.split(" ") is lst of the elements (type string) in each line
            if(len(item)>0): #not empty
                if '.' in item: #has decimal point
                    my_lst.append(float(item))
                else:
                    my_lst.append(int(item))
        lst_filter.append(my_lst)

    return lst_filter  # return the filter as 2d list of integers


def clip(sum):
    #aim to keep the value of the items within the range from zero >> to max_color_value
    global max_color_value
    if sum < 0: #less than zero will be zero
        return 0
    elif sum > max_color_value: #more than max_color_value will be equal to max_color value
        return int(max_color_value)
    else:
        return int(sum)


def convolution(lst, filter, stride):
    new_lst = []  # 3d image lst
    for row in range(0,len(lst),stride): # the steps in the forloop= stride
        if len(lst) - row >= len(filter):  # we should stop before reaching the bottom of the image
            my_row = []
            for col in range(0, len(lst[row]), stride):  # the steps in the forloop= stride
                if len(lst[row]) - col >= len(filter[0]):  # we should stop before reaching the right edge of the image
                    color = []  # [red, green, blue]
                    for i in range(3):  # three colors [red, green, blue]
                        sum = 0
                        #iterate over the filter
                        for y in range(len(filter)):
                            for x in range(len(filter[y])):
                                sum += (lst[row + y][col + x][i] * filter[y][x])  # multiply each number in the filter to its corresponding value in the image
                        color.append(clip(sum))  # clip function to make sure value of the sum >= 0 and sum<= max_color_value
                    my_row.append(color)
            new_lst.append(my_row)
    return new_lst

# operation five functions
def convolution_pad(lst, filter, stride):
    new_lst = []  # 3d image lst

    for row in range(0,len(lst),stride):
        if len(lst) - row >= len(filter):  # we should stop before reaching the bottom of the image
            my_row = []
            for col in range(0, len(lst[row]), stride):  # the steps in the forloop= stride
                if len(lst[row]) - col > len(filter[0]):  # we should stop before reaching the right edge of the image
                    color = []  # [red, green, blue]
                    for i in range(3):  # three colors [red, green, blue]
                        sum = 0
                        for y in range(len(filter)):
                            for x in range(len(filter[y])):
                                sum += (lst[row + y][col + x][i] * filter[y][x])  # multiply each number in the filter to its corresponding value in the image
                        color.append(clip(sum))  # clip function to make sure value of the sum >= 0 and sum<= max_color_value
                    my_row.append(color)
            new_lst.append(my_row)
    return new_lst
def convolution_pad_zeros(lst,filter,stride):
    new_img=[] #will contain the original img+ additional cols of zeros at the beginning and end
    for row in range(len(lst)):
        zero_items=[] #additional cols of zeros
        for x in range((len(filter[0])-1)//2): # (filter[0])-1)//2 is the number of zero cols added
            zero_items.append([0,0,0])
        new_img.append(zero_items+lst[row]+zero_items)

    zero_row=[] #rows of zeros will be added at the beginning and at the end of the img
    for y in range((len(filter)-1)//2): # (filter[0])-1)//2 is the number of zero rows added
        items=[]
        for i in range(len(new_img[0])): #len(new_img[0] is the news width of the img
            items.append([0,0,0])
        zero_row.append(items)
    lst=zero_row+new_img.copy()+zero_row #lst is the original img with boarder of zeros

    return convolution_pad(lst,filter,stride) #now convolute the new lst

# operation six functions
def check_quantize_color(lst, rows, cols, q_range):
    # check if the pixel is within the range with the previous one , and if so change its value
    global previous_pixel
    within_range = True
    for i in range(3):  # [red,green,blue]
        # used max and min to avoid minus values (big-small) always >0
        if max(lst[rows][cols][i], previous_pixel[i]) - min(lst[rows][cols][i], previous_pixel[i]) > q_range:
            within_range = False
            break
    if within_range == True:
        lst[rows][cols] = previous_pixel
    previous_pixel = lst[rows][cols]  # update the value of previous pixel


def last_part(rows, cols, ideal, x, y, q_range):
    # this part is needed when the dimension of the img is even
    if rows < 0:
        return
    check_quantize_color(ideal, rows, cols, q_range)
    last_part(rows - 1, cols, ideal, x, y, q_range)
    return ideal


def rec_print(rows, cols, ideal, x, y, q_range):
    if rows < 0 or rows >= x:
        if cols % 2 == 0:
            return rec_print(0, cols - 1, ideal, x, y, q_range)  # prepare to move from top to bottom
        else:
            return rec_print(x - 1, cols - 1, ideal, x, y, q_range)  # prepare to move from bottom to top
    ####
    if cols < 0:  # stop recursion
        return
    ####
    if cols % 2 == 0:
        rec_print(rows - 1, cols, ideal, x, y, q_range)  # upward
    else:
        rec_print(rows + 1, cols, ideal, x, y, q_range)  # downward
    ####
    # check if it is within the range of quantization
    check_quantize_color(ideal, rows, cols, q_range)
    ####
    if x % 2 == 0 and cols == y - 1:
        # even dimension needs to complete the recursion to the end
        return last_part(x - 2, cols, ideal, x, y, q_range)

    if x % 2 == 1 and cols == y - 1:
        # odd dimension the recusrsion is already completed return
        return ideal


# operation seven functions
def complete_rec_red_blue_even(rows, cols, lst, x, y, i, q_range):
    if rows < 0:
        return
    check_quantized_3d(lst, rows, cols, q_range, i)
    complete_rec_red_blue_even(rows - 1, cols, lst, x, y, i, q_range)
    return lst


def rec_red_blue(rows, cols, lst, x, y, i, q_range):
    # achieve this path
    # 1 6 7
    # 2 5 8
    # 3 4 9
    if rows < 0 or rows >= x:
        if cols % 2 == 0:
            return rec_red_blue(0, cols - 1, lst, x, y, i, q_range)
        else:
            return rec_red_blue(x - 1, cols - 1, lst, x, y, i, q_range)
    ####
    if cols < 0:
        return
    ####
    if cols % 2 == 0:
        rec_red_blue(rows - 1, cols, lst, x, y, i, q_range)
    else:
        rec_red_blue(rows + 1, cols, lst, x, y, i, q_range)

    check_quantized_3d(lst, rows, cols, q_range, i)
    ###
    if x % 2 == 0 and cols == y - 1:  # the scan over even dimension img need to be completed
        return complete_rec_red_blue_even(x - 2, cols, lst, x, y, i, q_range)

    if x % 2 == 1 and cols == y - 1:  # the scan over odd dimension img is done
        return lst


def complete_rec_green_even(lst, rows, cols, x, y, k, q_range):
    if rows >= x - 1:
        return

    check_quantized_3d(lst, rows, cols, q_range, k)
    return complete_rec_green_even(lst, rows + 1, cols, x, y, k, q_range)


def rec_green(lst, rows, cols, x, y, k, q_range, checked):
    # achieve this path
    # 9 4 3
    # 8 5 2
    # 7 6 1
    if x % 2 == 0 and cols == y - 1 and checked == False:  # the scan over even dimension img need to be completed
        checked = True  # just go over them once
        complete_rec_green_even(lst, 0, y - 1, x, y, k, q_range)
    ###
    if rows < 0 or rows >= x:
        if cols % 2 == 0:
            return rec_green(lst, 0, cols - 1, x, y, k, q_range, checked)
        if cols % 2 == 1:
            return rec_green(lst, x - 1, cols - 1, x, y, k, q_range, checked)
    ###
    if cols < 0:  # stop
        return
    ###
    if cols % 2 == 0:
        check_quantized_3d(lst, rows, cols, q_range, k)
        rec_green(lst, rows - 1, cols, x, y, k, q_range, checked)
    ###
    if cols % 2 == 1:
        check_quantized_3d(lst, rows, cols, q_range, k)
        rec_green(lst, rows + 1, cols, x, y, k, q_range, checked)
    return lst


def result(rows, cols, lst, q_range):
    for i in range(3):  # [red, green,blue] i=0, 1, 2
        if i % 2 == 0:  # 0,2 forward scan

            # rows minus 1 to fit in as a lst index
            # cols minus 1 to fit in as a lst index
            rec_red_blue(rows - 1, cols - 1, lst, rows, cols, i, q_range)
        ###
        else:  # 1 backward scan

            # False is needed for even dimension img in order to make sure that we scanned over the last col just once
            rec_green(lst, rows - 1, cols - 1, rows, cols, i, q_range, False)

    return lst


def check_quantized_3d(lst, rows, cols, q_range, i):
    global previous_num

    # check if the difference between two value is within the quantized range
    if max(lst[rows][cols][i], previous_num) - min(lst[rows][cols][i], previous_num) <= q_range:
        lst[rows][cols][i] = previous_num

    previous_num = lst[rows][cols][i]  # update the value of previous num


lst,max_color_value=read_ppm_file(f"./{filename}")
previous_pixel = lst[0][0]  # used as the initial value in the 2 d quantization
previous_num = lst[0][0][0]  # used as the initial value in the 3 d quantization
choose_operation(operation,lst)


# DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE

