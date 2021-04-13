import face_recognition
import numpy as np
import cv2
import os

#Used to compare the similarity of id images obtained
def compare_images(imageA, imageB):
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	return err 


#used to draw rectangle on frame, face detection and returns coordinates of the faces, draw rectangle on faces
def imageCapture(frame,quality):
    face_locations = []
    small_frame = cv2.resize(frame, (0,0), fx=0.5, fy= 0.5)    
    rgb_small_frame = small_frame[:,:,::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=quality)

    for (top,right,bottom,left) in face_locations:
        top*=2
        right*=2
        bottom*=2
        left*=2
        cv2.rectangle(frame, (left,top),(right,bottom), (0,0,255), 2)
    cv2.rectangle(frame, (300, 250), (20, 70), (0,255,0), 2)
    id_cropped = frame[70:250,20:300]
    id_cropped_resized = cv2.resize(id_cropped,(500,500))

    return face_locations,frame,id_cropped_resized


#used to verify face
def similarityChecker(encoding_1,encoding_2):
    distance = face_recognition.face_distance(np.array(encoding_1),np.array(encoding_2))
    print(distance)
    if(distance<0.45):
        return True
    else:
        return False


#load original ID images for similarity check
def loadIds():
    path = r'.\id'
    files = os.listdir(path)
    Ids = []
    for file in files:
        extension = os.path.splitext(file)
        if extension[1] in ['.jpg','.png','.jpeg']:
            img = cv2.imread(os.path.join(path,file))
            img_resized = cv2.resize(img,(500,500))
            Ids.append(img_resized)
    return Ids


global images
images = loadIds()
#check ID 
def idChecker(imageToVerify):
    isOriginal = False
    imageToVerify_resized = cv2.resize(imageToVerify,(500,500))
    for item in images:
        score = (compare_images(item, imageToVerify_resized))
        print(score)
        if (score< 15000):
            isOriginal = True
            #print("ginal ginal original")
            break
    return isOriginal


#check Face
def faceVerification(coords):
    img = face_recognition.load_image_file('image.jpg')
    encoding_one = face_recognition.face_encodings(img,[coords[0]])
    encoding_two = face_recognition.face_encodings(img,[coords[1]])

    return(similarityChecker(encoding_one,encoding_two))


#Main verification function
def verification(coords):
    idImg = cv2.imread('id.jpg')
    if(idChecker(idImg)):
        if(faceVerification(coords)):
            return "VerificationSuccess"
        else:
            return "FaceVerificationFailed"
    else:
        print("verification failed")
        return "IdVerificationFailed"





