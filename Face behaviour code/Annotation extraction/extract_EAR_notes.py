# Extract EAR annotations from saved extracted faces
# Jonathan Dulce
# Last edited: 5 Nov 2021

# import packages
from imutils import face_utils
import imutils
import dlib
import cv2
import math
import os
import time

# file path for extracted face images
extract_folder = 'NTHU_Training_Fast_Extracted/'

# path directories
set_number = ['001/', '002/', '005/', '006/', '008/', '009/', '012/', '013/', '015/', '020/', '023/', '024/', '031/', '032/', '033/', '034/', '035/', '036/']
subject_type = ['glasses/', 'night_noglasses/', 'nightglasses/', 'noglasses/', 'sunglasses/']
behaviour_type = ['nonsleepyCombination', 'sleepyCombination', 'slowBlinkWithNodding', 'yawning']
annotation_type = ['_drowsiness/', '_eye/', '_head/', '_mouth/']
eye_subtype = ['stillness/', 'sleepyEyes/']

#initialise dlib face detector (http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)
#detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68.dat")

# initial matrices for notes
processcount = 0
left_ear = []
right_ear = []
avg_ear = []

for sets in set_number:
    for subjects in subject_type:
        for behaviours in behaviour_type:
            # Change this to extract different eye annotation type
            path = extract_folder+sets+subjects+behaviours+annotation_type[1]+eye_subtype[1]

            for filename in os.listdir(path):
                # load the input image from disk, resize, and convert to grayscale
                img_path = path+filename
                print(img_path)
                image = cv2.imread(img_path)
                image = imutils.resize(image, width=500)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # draw rectangle over face (not required)
                x = 0
                y = 0
                h, w, channels = image.shape
                cv2.rectangle(image, (x,y), (x+w, y+h), (0, 255, 0) ,3)

                # detect landmarks with dlib
                drect = dlib.rectangle(int(x),int(y), int(x+w), int(y+h))
                landmarks = predictor(gray, drect)
                points = face_utils.shape_to_np(landmarks)
                for (x,y) in points:
                    cv2.circle(image, (x,y), 2, (0, 255, 0), -1)


                # EAR of left eye
                lp2p6 = math.hypot(abs(points[37][0]-points[41][0]),abs(points[37][1]-points[41][1]))
                lp3p5 = math.hypot(abs(points[38][0]-points[40][0]),abs(points[38][1]-points[40][1]))
                lp1p4 = math.hypot(abs(points[36][0]-points[39][0]),abs(points[36][1]-points[39][1]))
                left_ear.insert(processcount, (lp2p6+lp3p5)/(2*lp1p4))
                

                # EAR of right eye
                rp2p6 = math.hypot(abs(points[43][0]-points[47][0]),abs(points[43][1]-points[47][1]))
                rp3p5 = math.hypot(abs(points[44][0]-points[46][0]),abs(points[44][1]-points[46][1]))
                rp1p4 = math.hypot(abs(points[42][0]-points[45][0]),abs(points[42][1]-points[45][1]))
                right_ear.insert(processcount, (rp2p6+rp3p5)/(2*rp1p4))

                avg_ear.insert(processcount, (left_ear[-1]+right_ear[-1])/2)
                

                # dlib 68 landmarks key:
                # 1-17 = cheekbones and chin
                # 18-22 = left eyebrow      23-27 = right eyebrow
                # 28-31 = nose bridge       32-36 = bottom of nose
                # 37-42 = left eye          43-48 = right eye
                # 49-60 = outer lip         61-68 = inner lip

                processcount+=1
                # cv2.imshow("Image",image)

# save annotations to file
EAR_file = open("EAR_sleepyEyes.txt", "w")
EAR_file.write(repr(avg_ear))
EAR_file.close

# cv2.destroyAllWindows()
