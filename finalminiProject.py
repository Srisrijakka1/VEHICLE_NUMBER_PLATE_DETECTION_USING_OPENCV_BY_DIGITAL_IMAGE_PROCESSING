#-----requred libraries------#
import cv2 #opencv lib 
import numpy as np
import pytesseract 
import collections
#---------------------------#
 
#---------------------1st half start----------------------------------------------#
''' 
In this 1st half we perform th following actions:1.img loading
                                                 2.graying image 
                                                 3.extract the number plate
'''

#img loading
image = cv2.imread("carForTest_K.jpg")    #img file reading

cv2.imshow("loaded image ",image) ; cv2.waitKey(0);  

#graying image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) ; #cv2.imshow("grayed image",gray) ; cv2.waitKey(0);

# load the number plate detector
n_plate_detector = cv2.CascadeClassifier("haarcascade_russian_plate_number1.xml")

detections = list(n_plate_detector.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=15)) 

for (x, y, w, h) in detections:
    # extract the number plate from the grayscale & smootening image
    imag = gray[y:y + h, x:x + w] ;
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 355, 355), 4)
    #cv2.imshow("detected image",image) ; cv2.waitKey(0);
        
    #cv2.imshow("detected image",imag) ; cv2.waitKey(0);
    
#---------------------1st half end----------------------------------------------#


#--------------------2nd half start---------------------------------------------#
''' 
In this 2nd half we perform th following actions:4.increase the threshold value of the image
                                                 5.extracting the characters from the image
'''
#-------4.increase the threshold value of the image-#
#-->smoothening img detections
imagesmoothened = cv2.bilateralFilter(gray, 15, 75, 75)
#cv2.imshow('image after Smoothened', imagesmoothened) ;cv2.waitKey()
for l in n_plate_detector.detectMultiScale(imagesmoothened, scaleFactor=1.05, minNeighbors=15):
    detections.append(l) 
#-------------------#
#---->sharpening-----#
'''
GEEKSFORGEEKS
Python OpenCV – Filter2D() Function
In this article, we are going to see about the filter2d() function from OpenCV. In a nutshell, with this function, we can convolve an image with the kernel (typically a 2d matrix) to apply a filter on the images.

Syntax: filter2D (src, dst, ddepth, kernel)

Parameters:  

Src – The source image to apply the filter on.
Dst – Name of the output image after applying the filter
Ddepth – Depth of the output image [ -1 will give the output image depth as same as the input image]
Kernel – The 2d matrix we want the image to convolve with.
'''
kernel = np.array([[0, -1, 0],
                   [-1, 5,-1],
                   [0, -1, 0]])
image_sharp = cv2.filter2D(src=gray, ddepth=-1, kernel=kernel)
#cv2.imshow('image after Sharpened', image_sharp) ;cv2.waitKey() 
for l in n_plate_detector.detectMultiScale(imagesmoothened, scaleFactor=1.05, minNeighbors=15):
    detections.append(l) 
#-------------------#
#--------------------------------------------------#
#--5.extracting the characters from the image------#
#-----------#
def get_mst_accurate_letter(lst_txts):
    d =  collections.defaultdict(lambda : 0)
    for lst in lst_txts:
        #print(">>",lst,"<<")
        for letter in lst:
            d[letter] += 1 
    ds = list(sorted(d.items(), key = lambda x : x[1],reverse = True)) 
    #print(ds,"sorted sdictionsry")
    fnl_lst_letters = []
    for i in range(len(ds)):
        fnl_lst_letters.append(ds[i][0])
    return fnl_lst_letters
#-----------# 
list_txts = []
for (x,y,w,h) in detections:
    img_detected = gray[y : y+h , x : x + w] 
    txt_detected = pytesseract.image_to_string(img_detected)
    org_txt_detected = "" #eliminating spaces 
    for letter in txt_detected:
        if '0'<=letter<='9' or 'a'<=letter<='z' or 'A'<=letter<='Z':
            org_txt_detected += letter
    list_txts.append(org_txt_detected)
fnl_lst_letters = get_mst_accurate_letter(list_txts)
print(">>",fnl_lst_letters,"<<")
print("output>>") 
rs = ""
for i in range(min(len(max(list_txts,key = len)),10)):  #txt len iterarion
    for txt in list_txts: #lst iteration
        try:
            if txt[i] in fnl_lst_letters:
                rs += txt[i]
                #print(txt[i],end="")
                break
        except:
            continue
#print(end="\n")
#--modify correct formate--#
dic_ltr_to_num = {'A':'9','Q':'9','T':'7','B' : '8' ,'I':'1','O':'0','S':'5','D':'0','G':'4', 'Z' : '2'}
for idx in range( len(rs) ):
    letter = rs[idx]
    if idx in [2,3,6,7,8,9] and ('A'<=letter<='Z' or 'a'<=letter<='z'):  
        try:
            letter = dic_ltr_to_num[letter]
        except:
            pass
    print(letter,end ="")
print(end="\n")
#-------------------------#
#--------------------------------------------------#
#--------------------2nd half end-----------------------------------------------#