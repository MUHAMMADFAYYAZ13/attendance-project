from numpy import load
import face_recognition
import cv2
import numpy as np
import os
from utils import *
import pandas as pd
from IPython.display import HTML

df = Initialize_attendance()
cv2.namedWindow('Video',cv2.WINDOW_NORMAL)
cv2.resizeWindow('Video', 640,480)
video_capture = cv2.VideoCapture(0)
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
known_faces_encoded = enrolled_students
known_names = student_names
known_ids = student_ids
process_this_frame = True
i = 1
while True:
 # Grab a single frame of video
    ret, frame = video_capture.read()
    
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    # Display the results
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_faces_encoded, face_encoding)
        name = "Unknown"
        
        face_distances = face_recognition.face_distance(known_faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_names[best_match_index]
            ids = known_ids[best_match_index]
        
           # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
    
    # Draw a box around the face
        if name != "Unknown":
            _, time = getDate_Time()
            df = update_attendance(df, time, ids)
            cv2.rectangle(frame, (left-30, top-30), (right+30, bottom+30), (0, 128, 0), 2)
            text = "Attendance Marked"
           # Draw a label with a name below the face
            cv2.rectangle(frame, (left-30, bottom), (right+30, bottom+30), (0, 128, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, ids, (left + 6, bottom + 25), font, 1.0, (255, 255, 255), 1)
            cv2.putText(frame, text, (30, 30), font, 1.0, (0, 128, 0), 1)
        else:
            cv2.rectangle(frame, (left-30, top-30), (right+30, bottom+30), (0, 0, 255), 2)
    
           # Draw a label with a name below the face
            cv2.rectangle(frame, (left-30, bottom), (right+30, bottom+30), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom + 25), font, 1.0, (255, 255, 255), 1)
        
    # Display the resulting image
    cv2.imshow('Video', frame)
    #cv2.imwrite('output/Frame' + str(i) + '.jpg', frame)
    i = i + 1
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# Release handle to the webcam
export_reports(df)
#HTML(df.to_html(classes='table table-striped'))
video_capture.release()
cv2.destroyAllWindows()