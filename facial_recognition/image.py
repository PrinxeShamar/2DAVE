import cv2
import dlib

# Load face detector from dlib
detector = dlib.get_frontal_face_detector()

# Load the image
image = cv2.imread('IMG_8770.JPG')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faces = detector(gray)
for face in faces:
    left = face.left()
    top = face.top()
    right = face.right()
    bottom = face.bottom()    
    cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)

cv2.imshow('Image with faces detected', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
