# Prepare directories for face extraction from NTHU training dataset
# Jonathan Dulce
# Last edited: 5 Nov 2021

# import packages
import os

# Training Dataset Terms
set_number = ['001', '002', '005', '006', '008', '009', '012', '013', '015', '020', '023', '024', '031', '032', '033', '034', '035', '036']
subject_type = ['glasses', 'night_noglasses', 'nightglasses', 'noglasses', 'sunglasses']
behaviour_type = ['nonsleepyCombination', 'sleepyCombination', 'slowBlinkWithNodding', 'yawning']
annotation_type = ['drowsiness', 'eye', 'head', 'mouth']

# Folder name for extraction and save folder locations
extract_folder = 'NTHU_Training_Dataset/'
save_folder = 'NTHU_Training_Haar'

#### Annotation
# There are four annotations of each video and a single digit is used to indicate the status of the frame.
# [video name]_drowsiness.txt     : 0 means Stillness and 1 means Drowsy.
# [video name]_head.txt           : 0 means Stillness, 1 means Nodding and 2 means Looking aside.
# [video name]_mouth.txt          : 0 means Stillness and 1 means Yawning and 2 means Talking & Laughing.
# [video name]_eye.txt            : 0 means Stillness and 1 means Sleepy-eyes.



for sets in set_number:
    path = save_folder + '/' + sets
    os.mkdir(path)
    for subjects in subject_type:
        path = save_folder + '/' + sets + '/' + subjects
        os.mkdir(path)
        for behaviours in behaviour_type:
            for annotations in annotation_type:
                path = save_folder + '/' + sets + '/' + subjects+ '/' + behaviours + '_' + annotations
                os.mkdir(path)
                if annotations == annotation_type[0]:
                    path = save_folder + '/' + sets + '/' + subjects+ '/' + behaviours + '_' + annotations + '/stillness'
                    os.mkdir(path)
                    path = save_folder + '/' + sets + '/' + subjects+ '/' + behaviours + '_' + annotations + '/drowsy'
                    os.mkdir(path)
                elif annotations == annotation_type[1]:
                    path = save_folder + '/' + sets + '/' + subjects+ '/' + behaviours + '_' + annotations + '/stillness'
                    os.mkdir(path)
                    path = save_folder + '/' + sets + '/' + subjects+ '/' + behaviours + '_' + annotations + '/sleepyEyes'
                    os.mkdir(path)
                elif annotations == annotation_type[2]:
                    path = save_folder + '/' + sets + '/' + subjects+ '/' + behaviours + '_' + annotations + '/stillness'
                    os.mkdir(path)
                    path = save_folder + '/' + sets + '/' + subjects+ '/' + behaviours + '_' + annotations + '/nodding'
                    os.mkdir(path)
                    path = save_folder + '/' + sets + '/' + subjects+ '/' + behaviours + '_' + annotations + '/lookingAside'
                    os.mkdir(path)
                elif annotations == annotation_type[3]:
                    path = save_folder + '/' + sets + '/' + subjects+ '/' + behaviours + '_' + annotations + '/stillness'
                    os.mkdir(path)
                    path = save_folder + '/' + sets + '/' + subjects+ '/' + behaviours + '_' + annotations + '/yawning'
                    os.mkdir(path)
                    path = save_folder + '/' + sets + '/' + subjects+ '/' + behaviours + '_' + annotations + '/talking'
                    os.mkdir(path)

print("DONE")