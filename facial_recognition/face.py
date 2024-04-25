import cv2
import dlib

# Load face detector from dlib
detector = dlib.get_frontal_face_detector()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for face in faces:
        left = face.left()
        top = face.top()
        right = face.right()
        bottom = face.bottom()    
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
    
    cv2.imshow('Video', frame)
    if cv2.waitKey(25) == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
