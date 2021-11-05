# Count number of faces extracted
# Jonathan Dulce
# Last edited: 5 Nov 2021

import os

# Training Dataset Terms
set_number = ['001', '002', '005', '006', '008', '009', '012', '013', '015', '020', '023', '024', '031', '032', '033', '034', '035', '036']
subject_type = ['glasses', 'night_noglasses', 'nightglasses', 'noglasses', 'sunglasses']
behaviour_type = ['nonsleepyCombination', 'sleepyCombination', 'slowBlinkWithNodding', 'yawning']
annotation_type = ['drowsiness'] # use drowsiness annotation type for counting
annotation_subtype = ['stillness', 'drowsy']
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


info_file = open("NTHU_Training_Metadata_Haar_framecount.txt", "w")

# Loop through all folders and extract frames
for sets in set_number:
    for subjects in subject_type:
        for behaviours in behaviour_type:
            total_faces = 0
            for subtype in annotation_subtype:
                file_dir = save_folder + sets + '/' + subjects + '/' + behaviours + '_drowsiness' + '/' + subtype

                onlyfiles = next(os.walk(file_dir))[2]
                total_faces = total_faces + len(onlyfiles)
                # print(len(onlyfiles))

            file_dir2 = save_folder + sets + '/' + subjects + '/' + behaviours + '_drowsiness'
            print('\n\n\n\n[INFO] Framecount for...\n\tDirectory:\t', file_dir2)
            print('\n\tNumber of faces detected:\t', total_faces)

            info_text = '\n' + str(total_faces)
            info_file.write(info_text)
 

print('\n\n\n\n[INFO] end count')
info_file.close