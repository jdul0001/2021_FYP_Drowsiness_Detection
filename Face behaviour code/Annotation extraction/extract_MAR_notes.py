# Extract MAR annotations from saved extracted faces
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
mouth_subtype = ['stillness/', 'talking/', 'yawning/']

#initialise dlib face detector (http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)
#detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68.dat")

# initial matrices for notes
processcount = 0
mouth = []

for sets in set_number:
    for subjects in subject_type:
        for behaviours in behaviour_type:
            # Change this to extract different mouth annotation type
            path = extract_folder+sets+subjects+behaviours+annotation_type[3]+mouth_subtype[0]

            for filename in os.listdir(path):
                # load the input image from disk, resiqze, and convert to grayscale
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

                # create rectangle from haar
                drect = dlib.rectangle(int(x),int(y), int(x+w), int(y+h))
                landmarks = predictor(gray, drect)
                points = face_utils.shape_to_np(landmarks)
                for (x,y) in points:
                    cv2.circle(image, (x,y), 2, (0, 255, 0), -1)


                # MAR
                mp2p8 = math.hypot(abs(points[61][0]-points[67][0]),abs(points[61][1]-points[67][1]))
                mp3p7 = math.hypot(abs(points[62][0]-points[66][0]),abs(points[62][1]-points[66][1]))
                mp4p6 = math.hypot(abs(points[63][0]-points[65][0]),abs(points[63][1]-points[65][1]))
                mp1p5 = math.hypot(abs(points[60][0]-points[64][0]),abs(points[60][1]-points[64][1]))
                mouth.insert(processcount, (mp2p8+mp3p7+mp4p6)/(3*mp1p5))
                

                # dlib 68 landmarks key:
                # 1-17 = cheekbones and chin
                # 18-22 = left eyebrow      23-27 = right eyebrow
                # 28-31 = nose bridge       32-36 = bottom of nose
                # 37-42 = left eye          43-48 = right eye
                # 49-60 = outer lip         61-68 = inner lip

                processcount+=1
                # cv2.imshow("Image",image)

# save annotations to file
MAR_file = open("MAR_stillness.txt", "w")
MAR_file.write(repr(mouth))
MAR_file.close

# cv2.destroyAllWindows()
