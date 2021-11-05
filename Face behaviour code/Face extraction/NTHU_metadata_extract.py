# Extract metadata from NTHU dataset videos
# Jonathan Dulce
# Last edited: 5 Nov 2021

import cv2

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

info_file = open("NTHU_Training_Metadata_summary.txt", "w")
fps_file = open("NTHU_Training_Metadata_fps.txt", "w")
totalFrames_file = open("NTHU_Training_Metadata_totalFrames.txt", "w")
fwidth_file = open("NTHU_Training_Metadata_frameWidth.txt", "w")
fheight_file = open("NTHU_Training_Metadata_frameHeight.txt", "w")

# Loop through all folders and extract frames
for sets in set_number:
    for subjects in subject_type:
        for behaviours in behaviour_type:
            video_file_dir = extract_folder + sets + '/' + subjects + '/' + behaviours + '.avi'

            # Skip directory [Notice] There is no video in Number-005 subject's night_glasses scenario.
            if any(ele in video_file_dir for ele in skip_dir_list):
                
                info_header = '\n\n\n\n[INFO] Metadata for...\n\tDirectory:\t' + video_file_dir
                info_file.write(info_header)

                # print all metadata to a summary file
                fps_print = '\n*****'
                totalframe_print = '\n*****'
                fwidth_print = '\n*****'
                fheight_print = '\n*****'
                info_file.write(fps_print)
                info_file.write(totalframe_print)
                info_file.write(fwidth_print)
                info_file.write(fheight_print)

                # Print metadata to individual files
                fps_text = '\n*****'
                totalframe_text = '\n*****'
                fwidth_text = '\n*****'
                fheight_text = '\n*****'
                fps_file.write(fps_text)
                totalFrames_file.write(totalframe_text)
                fwidth_file.write(fwidth_text)
                fheight_file.write(fheight_text)
                continue

            print('\n\n\n\n[INFO] Metadata for...\n\tDirectory:\t', video_file_dir)
            info_header = '\n\n\n\n[INFO] Metadata for...\n\tDirectory:\t' + video_file_dir
            info_file.write(info_header)

            vid = cv2.VideoCapture(video_file_dir)

            # Print video params to console
            fps = int(vid.get(cv2.CAP_PROP_FPS))
            total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
            f_width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
            f_height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
            print('\tFPS:\t\t', fps)
            print('\tTotal Frames:\t', total_frames)
            print('\tFrame Width:\t', f_width)
            print('\tFrame Height:\t', f_height)

            # print all metadata to a summary file
            fps_print = '\n\tFPS:\t\t' + str(fps)
            totalframe_print = '\n\tTotal Frames:\t' + str(total_frames)
            fwidth_print = '\n\tFrame Width:\t' + str(f_width)
            fheight_print = '\n\tFrame Height:\t' + str(f_height)
            info_file.write(fps_print)
            info_file.write(totalframe_print)
            info_file.write(fwidth_print)
            info_file.write(fheight_print)

            # Print metadata to individual files
            fps_text = '\n' + str(fps)
            totalframe_text = '\n' + str(total_frames)
            fwidth_text = '\n' + str(f_width)
            fheight_text = '\n' + str(f_height)
            fps_file.write(fps_text)
            totalFrames_file.write(totalframe_text)
            fwidth_file.write(fwidth_text)
            fheight_file.write(fheight_text)



            # info_file.write(fwidth_text)
            # info_file.write(fheight_text)

            vid.release()

print('\n\n\n\n[INFO] end info')
info_file.close
fps_file.close
totalFrames_file.close
fwidth_file.close
fheight_file.close