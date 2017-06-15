import cv2
import sys

# parameters
image_path = sys.argv[1]
detection_model_path = './trained_models/haarcascade_frontalface_default.xml'

x_offset_emotion = 0
y_offset_emotion = 0

# loading models
face_detection = cv2.CascadeClassifier(detection_model_path)
frame = cv2.imread(image_path)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

faces = face_detection.detectMultiScale(gray, 1.3, 5)
exportCount = 0
for (x,y,w,h) in faces:
    
    gray_face = gray[(y - y_offset_emotion):(y + h + y_offset_emotion),
                    (x - x_offset_emotion):(x + w + x_offset_emotion)]

    print(gray_face)
    try:
        if len(gray_face) <= 0: continue
        gray_face = cv2.resize(gray_face, (48, 48))
        cv2.imwrite('./images/face-exports/gray_' + str(exportCount) + '.png', gray_face)
        exportCount = exportCount + 1
    except:
       continue