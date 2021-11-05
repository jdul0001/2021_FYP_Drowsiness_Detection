# FYP 2021: Drowsiness Detection and Anti-Sleep Alarm System
Jonathan Dulce and Harold Johnson

Supervisor: Dr. Faezeh Marzbanrad

This repository contains the code used for this FYP.

## Face Behaviour Monitoring
This portion of the project involved using the NTHU training dataset (http://cv.cs.nthu.edu.tw/php/callforpaper/datasets/DDD/) to explore face detection and face behaviour monitoring techniques. The following code is included for reference:

- **Face extraction/ :**  Face extraction files for creation of extracted face directories based on annotations, and face detector testing.
- **Annotation extraction/ :**  Annotation extraction files to analyse Eye Aspect Ratio (EAR) and Mouth Aspect Ratio (MAR) from extracted faces.
- **Video testing/ :** Testing code for use on a video from the training dataset, to evaluate and explore eye and mouth movements/behaviours.
- **MATLAB code (Face Behaviour)/ :**  MATLAB code for evaluating extracted EAR and MAR annotations.

## Heart Rate Monitoring
This portion of the project involved using the Bed Based Ballistocardiography Database (https://ieee-dataport.org/open-access/bed-based-ballistocardiography-dataset) to explore peak detection and frequency domain analysis for use of classifying alertness states from BCG signals. The following MATLAB code is included for reference:

- **Data_Analysis.m:** Analysis file for analysing heart rate (HR) and heart rate variability (HRV) from extracted BCG signals.
- **HRV.m:** Spectral analysis for HRV.
- **BlandAltmanPlot.m:** Comparing and evaluating BCG signal processing with a reference PPG signal via a Bland-Altman plot.
