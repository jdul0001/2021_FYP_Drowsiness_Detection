# Video testing for face detection and behaviour tracking
# Jonathan Dulce
# Last edited: 5 Nov 2021
# uses a pretrained MTCNN face detector
# uses a pretrained dlib predictor model to map landmarks

# Uses a video feed as a reference and detects face and landmarks in each frame.

# expressions monitored:
# Ear Aspect Ratio (EAR) 
#   - Blink Rate
#   - PERCLOS
# Mouth Aspect Ratio (MAR)


# import packages
from imutils import face_utils
from imutils.video import VideoStream
from facenet_pytorch import MTCNN
from PIL import Image
import torch
import imutils
import dlib
import time
import cv2
import math

# setup MTCNN from facenet-pytorch
device = 'cuda' if torch.cuda.is_available() else 'cpu'
detector = MTCNN(select_largest=False, device=device)

# File path for video for testing
path = "NTHU_Training_Dataset/009/noglasses/nonsleepyCombination.avi"


#initialise dlib face detector (http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)
predictor = dlib.shape_predictor("shape_predictor_68.dat")

# capture video file
vid = cv2.VideoCapture(path)

# metadata from video
fps = int(vid.get(cv2.CAP_PROP_FPS))
total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
print("FPS: ", fps)
print("Total Frame: ", total_frames)

# read every N frames
framecount = 0
N = 1

# initialise arrays for landmarks analysis
processcount = 0
left_ear = []
right_ear = []
avg_ear = []
mouth = []

EAR_threshold = 0.22
eye_closed_count = 0
PERCLOS_count = 0
blink_rate_count = 0
blink_rate_20 = "..."
PERCLOS_20 = "..."
seconds = 0

# loop through each video frame and perform face detection
print("[INFO] performing face detection...")

while (vid.isOpened()):
    framecount+=1
    #grab frame from video stream 
    ret, frame = vid.read()
    # print(framecount)

    # process every N valid frames
    if (frame is not None and framecount % N == 0):
        # Resize frame, convert to grayscale and detect faces
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        boxes, probs = detector.detect(frame, landmarks=False)
        

        # loop through each detected faces and draw over face
        # Execute only when one face is detected
        if (boxes is not None and (len(boxes)==1)):
            # Extract face detect params from JSON
            box = boxes[0]
            conf = probs[0]
            x1, y1, x2, y2 = box[0], box[1], box[2], box[3] # box bounds

            # create 68 landmarks from dlib
            drect = dlib.rectangle(int(x1),int(y1), int(x2), int(y2))
            landmarks = predictor(gray, drect)
            points = face_utils.shape_to_np(landmarks)

            for (x,y) in points: # draw circles over landmarks
                cv2.circle(frame, (x,y), 2, (0, 255, 0), -1)

            # dlib 68 landmarks key:
            # 1-17 = cheekbones and chin
            # 18-22 = left eyebrow      23-27 = right eyebrow
            # 28-31 = nose bridge       32-36 = bottom of nose
            # 37-42 = left eye          43-48 = right eye
            # 49-60 = outer lip         61-68 = inner lip
        
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

            # mean EAR based on left and right
            avg_ear.insert(processcount, (left_ear[-1]+right_ear[-1])/2)

            # MAR
            mp2p6 = math.hypot(abs(points[61][0]-points[67][0]),abs(points[61][1]-points[67][1]))
            mp3p5 = math.hypot(abs(points[63][0]-points[65][0]),abs(points[63][1]-points[65][1]))
            mp1p4 = math.hypot(abs(points[60][0]-points[64][0]),abs(points[60][1]-points[64][1]))
            mouth.insert(processcount, (mp2p6+mp3p5)/(2*mp1p4))

            # determine blinks
            if avg_ear[-1]<EAR_threshold:
                eye_closed_count+=1
                PERCLOS_count+=1
            else:
                if eye_closed_count>0.1*fps:
                    blink_rate_count += 1
                    # print("blink!")
                eye_closed_count = 0

            # Blink rate and perclos update over 20 second window
            if framecount % (20*fps) == 0:

                blink_rate_20 = str(blink_rate_count*3)
                blink_rate_count = 0

                PERCLOS_20 = str((PERCLOS_count*3)/(20*fps))
                PERCLOS_count = 0

            # print seconds of video
            if framecount % (fps) == 0:
                seconds +=1
                print(seconds)

            # Print behaviour metrics over frame
            EAR_text = "EAR: " + str(round(avg_ear[-1],2))
            MAR_text = "MAR: " + str(round(mouth[-1],2))
            BLINK_text = "Blink rate: " + str(blink_rate_20) + "/min"
            PERCLOS_text = "PERCLOS: " + str(PERCLOS_20) + "%"

            cv2.putText(frame, EAR_text, (320, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (25, 25, 255), 2)
            cv2.putText(frame, MAR_text, (320, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (25, 25, 255), 2)
            cv2.putText(frame, BLINK_text, (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (25, 25, 255), 2)
            cv2.putText(frame, PERCLOS_text, (25, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (25, 25, 255), 2)

            # Head angle (experimental)
            # 1: point between eyes
            # cv2.line(frame, (points[39][0],points[39][1]), (points[42][0], points[42][1]), (0,0,255),2)

            # 2: point between middle of face and nose
            # cv2.rectangle(frame, (int(x1),int(y1)), (int(x2),int(y2)), (255,0,0),2)
            # cv2.circle(frame, (int((x1+x2)/2),int((y1+y2)/2)), 2, (0, 0, 255), -1)
            # cv2.circle(frame, (points[33][0], points[33][1]), 2, (0, 255, 0), -1)
            # cv2.line(frame, (int((x1+x2)/2),int((y1+y2)/2)), (points[33][0], points[33][1]), (0,0,255),2)

            cv2.imshow("Frame", frame)
            processcount+=1
        
        # break loop if 'q' pressed
        key = cv2.waitKey(25) & 0xFF
        if key == ord("q"):
            break


    
# release video
vid.release()

# cleanup
cv2.destroyAllWindows()

print("[INFO] end stream")