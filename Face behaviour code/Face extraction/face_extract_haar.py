# Face extraction from NTHU training dataset using Haar cascades
# Jonathan Dulce
# Last edited: 5 Nov 2021


# import packages
from PIL import Image
from imutils import face_utils
import imutils
import cv2

# detector from https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
print("[INFO] loading face detector...")
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Training Dataset Terms
set_number = ['001', '002', '005', '006', '008', '009', '012', '013', '015', '020', '023', '024', '031', '032', '033', '034', '035', '036']
subject_type = ['glasses', 'night_noglasses', 'nightglasses', 'noglasses', 'sunglasses']
behaviour_type = ['nonsleepyCombination', 'sleepyCombination', 'slowBlinkWithNodding', 'yawning']
annotation_type = ['drowsiness']
extract_folder = 'NTHU_Training_Dataset/'
save_folder = 'NTHU_Training_Haar/'

#### Annotation
# There are four annotations of each video and a single digit is used to indicate the status of the frame.
# [video name]_drowsiness.txt     : 0 means Stillness and 1 means Drowsy.
# [video name]_head.txt           : 0 means Stillness, 1 means Nodding and 2 means Looking aside.
# [video name]_mouth.txt          : 0 means Stillness and 1 means Yawning and 2 means Talking & Laughing.
# [video name]_eye.txt            : 0 means Stillness and 1 means Sleepy-eyes.

# [Notice] There is no video in Number-005 subject's night_glasses scenario.
# Make a list of video directories to skip
skip_dir_list = []
for behaviours in behaviour_type:
    skip_dir_list.append(extract_folder + '005/nightglasses/' + behaviours + '.avi')


# Loop through all folders and extract frames
for sets in set_number:
    for subjects in subject_type:
        for behaviours in behaviour_type:
            video_file_dir = extract_folder + sets + '/' + subjects + '/' + behaviours + '.avi'

            # Skip directory [Notice] There is no video in Number-005 subject's night_glasses scenario.
            if any(ele in video_file_dir for ele in skip_dir_list):
                continue

            print('\n\n\n\n[INFO] Extracting from...\n\tDirectory:\t', video_file_dir)

            vid = cv2.VideoCapture(video_file_dir)

            # Print video params
            fps = int(vid.get(cv2.CAP_PROP_FPS))
            total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
            f_width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
            f_height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
            print('\tFPS:\t\t', fps)
            print('\tTotal Frames:\t', total_frames)
            print('\tFrame Width:\t', f_width)
            print('\tFrame Height:\t', f_height)

            ### Extract Annotations
            # Annotation type 0: Drowsiness
            drowsiness_notes_dir = extract_folder + sets + '/' + subjects + '/' + sets + '_' + behaviours + '_' + annotation_type[0] + '.txt'
            drowsiness_notes_file = open(drowsiness_notes_dir, "r")
            drowsiness_notes = drowsiness_notes_file.read()
            drowsiness_notes_file.close()

            # Extract Frames
            for i in range(total_frames):
                ret, frame = vid.read()

                if ret:
                    # Attempt face detection
                    frame = imutils.resize(frame, width=500)
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    rects = detector.detectMultiScale(gray, scaleFactor=1.05,
                                  minNeighbors=5, minSize=(30, 30),
                                  flags=cv2.CASCADE_SCALE_IMAGE)

                    # Continue if only 1 face is detected
                    if (rects is not None and (len(rects)==1)): 
                        # Extract face detect params from JSON
                        for (x,y,w,h) in rects:
                                                   
                            # set limits for bounding boxes within the frame to avoid cropping error 
                            if x < 0:
                                x1 = 0
                            else:
                                x1 = int(x)

                            if y < 0:
                                y1 = 0
                            else:
                                y1 = int(y)

                            if (x+w) > f_width:
                                x2 = int(f_width)
                            else:
                                x2 = int(x+w)

                            if (y+h) > f_height:
                                y2 = int(f_height)
                            else:
                                y2 = int(y+h)

                            crop = frame[y1:y2, x1:x2]
                            print('\tExtracting frame:', i)

                        ### Save frame to file based on annotations
                        # check annotation type 0: Drowsiness
                        if drowsiness_notes[i] == '0': # stillness
                            note_type = 'stillness'
                            file_location = save_folder + sets + '/' + subjects + '/' + behaviours + '_' + annotation_type[0] + '/' + note_type + '/'
                            file_name = file_location + sets + '_' + behaviours + '_' + annotation_type[0] + '_' + note_type + '_' + str(i) + '.jpg'
                        elif drowsiness_notes[i] == '1': # drowsy
                            note_type = 'drowsy'
                            file_location = save_folder + sets + '/' + subjects + '/' + behaviours + '_' + annotation_type[0] + '/' + note_type + '/'
                            file_name = file_location + sets + '_' + behaviours + '_' + annotation_type[0] + '_' + note_type + '_' + str(i) + '.jpg'
                        cv2.imwrite(file_name, crop)

            vid.release()

print('\n\n\n\n[INFO] end extraction')