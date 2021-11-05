# Face extraction from NTHU training dataset using MTCNN (facenet)
# Jonathan Dulce
# Last edited: 5 Nov 2021

# import packages
from facenet_pytorch import MTCNN
from PIL import Image
import torch
from imutils import face_utils
import imutils
import cv2

# setup MTCNN from facenet-pytorch
device = 'cuda' if torch.cuda.is_available() else 'cpu'
detector = MTCNN(select_largest=False, device=device)

# Training Dataset Terms
set_number = ['001', '002', '005', '006', '008', '009', '012', '013', '015', '020', '023', '024', '031', '032', '033', '034', '035', '036']
subject_type = ['glasses', 'night_noglasses', 'nightglasses', 'noglasses', 'sunglasses']
behaviour_type = ['nonsleepyCombination', 'sleepyCombination', 'slowBlinkWithNodding', 'yawning']
annotation_type = ['drowsiness', 'eye', 'head', 'mouth']
extract_folder = 'NTHU_Training_Dataset/'
save_folder = 'NTHU_Training_Fast_Extracted/'

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

            # Annotation type 1: Eye
            eye_notes_dir = extract_folder + sets + '/' + subjects + '/' + sets + '_' + behaviours + '_' + annotation_type[1] + '.txt'
            eye_notes_file = open(eye_notes_dir, "r")
            eye_notes = eye_notes_file.read()
            eye_notes_file.close()

            # Annotation type 2: Head
            head_notes_dir = extract_folder + sets + '/' + subjects + '/' + sets + '_' + behaviours + '_' + annotation_type[2] + '.txt'
            head_notes_file = open(head_notes_dir, "r")
            head_notes = head_notes_file.read()
            head_notes_file.close()

            # Annotation type 3: Mouth
            mouth_notes_dir = extract_folder + sets + '/' + subjects + '/' + sets + '_' + behaviours + '_' + annotation_type[3] + '.txt'
            mouth_notes_file = open(mouth_notes_dir, "r")
            mouth_notes = mouth_notes_file.read()
            mouth_notes_file.close()

            # Extract Frames
            for i in range(total_frames):
                ret, frame = vid.read()

                if ret:
                    # Attempt face detection
                    frame = imutils.resize(frame, width=500)
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    boxes, probs = detector.detect(frame, landmarks=False)
                    # print('\t\tboxes:',boxes)
                    # print('\t\tprobs:',probs)

                    # Continue if only 1 face is detected
                    if (boxes is not None and (len(boxes)==1)): 
                        # Extract face detect params from JSON
                        box = boxes[0]
                        conf = probs[0]
                        x1, y1, x2, y2 = box[0], box[1], box[2], box[3]
                        
                        # set limits for bounding boxes within the frame to avoid cropping error 
                        if x1 < 0:
                            x1 = 0
                        else:
                            x1 = int(x1)

                        if y1 < 0:
                            y1 = 0
                        else:
                            y1 = int(y1)

                        if x2 > f_width:
                            x2 = int(f_width)
                        else:
                            x2 = int(x2)

                        if y2 > f_height:
                            y2 = int(f_height)
                        else:
                            y2 = int(y2)

                        
                        # crop face if >50% confident and only 1 face detected
                        if conf > 0.5:
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
                            
                            # check annotation type 1: Eye
                            if eye_notes[i] == '0': # stillness
                                note_type = 'stillness'
                                file_location = save_folder + sets + '/' + subjects + '/' + behaviours + '_' + annotation_type[1] + '/' + note_type + '/'
                                file_name = file_location + sets + '_' + behaviours + '_' + annotation_type[1] + '_' + note_type + '_' + str(i) + '.jpg'
                            elif eye_notes[i] == '1': # sleepy eyes
                                note_type = 'sleepyEyes'
                                file_location = save_folder + sets + '/' + subjects + '/' + behaviours + '_' + annotation_type[1] + '/' + note_type + '/'
                                file_name = file_location + sets + '_' + behaviours + '_' + annotation_type[1] + '_' + note_type + '_' + str(i) + '.jpg'
                            cv2.imwrite(file_name, crop)

                            # check annotation type 2: Head
                            if head_notes[i] == '0': # stillness
                                note_type = 'stillness'
                                file_location = save_folder + sets + '/' + subjects + '/' + behaviours + '_' + annotation_type[2] + '/' + note_type + '/'
                                file_name = file_location + sets + '_' + behaviours + '_' + annotation_type[2] + '_' + note_type + '_' + str(i) + '.jpg'
                            elif head_notes[i] == '1': # nodding
                                note_type = 'nodding'
                                file_location = save_folder + sets + '/' + subjects + '/' + behaviours + '_' + annotation_type[2] + '/' + note_type + '/'
                                file_name = file_location + sets + '_' + behaviours + '_' + annotation_type[2] + '_' + note_type + '_' + str(i) + '.jpg'
                            elif head_notes[i] == '2': # looking aside
                                note_type = 'lookingAside'
                                file_location = save_folder + sets + '/' + subjects + '/' + behaviours + '_' + annotation_type[2] + '/' + note_type + '/'
                                file_name = file_location + sets + '_' + behaviours + '_' + annotation_type[2] + '_' + note_type + '_' + str(i) + '.jpg'
                            cv2.imwrite(file_name, crop)

                            # check annotation type 3: Mouth
                            if mouth_notes[i] == '0': # stillness
                                note_type = 'stillness'
                                file_location = save_folder + sets + '/' + subjects + '/' + behaviours + '_' + annotation_type[3] + '/' + note_type + '/'
                                file_name = file_location + sets + '_' + behaviours + '_' + annotation_type[3] + '_' + note_type + '_' + str(i) + '.jpg'
                            elif mouth_notes[i] == '1': # yawning
                                note_type = 'yawning'
                                file_location = save_folder + sets + '/' + subjects + '/' + behaviours + '_' + annotation_type[3] + '/' + note_type + '/'
                                file_name = file_location + sets + '_' + behaviours + '_' + annotation_type[3] + '_' + note_type + '_' + str(i) + '.jpg'
                            elif mouth_notes[i] == '2': # talking/laughing
                                note_type = 'talking'
                                file_location = save_folder + sets + '/' + subjects + '/' + behaviours + '_' + annotation_type[3] + '/' + note_type + '/'
                                file_name = file_location + sets + '_' + behaviours + '_' + annotation_type[3] + '_' + note_type + '_' + str(i) + '.jpg'
                            cv2.imwrite(file_name, crop)

            vid.release()

print('\n\n\n\n[INFO] end extraction')