import face_recognition
import numpy as np
import cv2
import os
 
class UserVerification:
    
    def __init__(self,images):
        self.images = images

    #compares the obtained two images compare the mean squared error between them and returns the error
    #the lesser the error similar the images
    def mse(self,imageA, imageB):
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])
        return err 

    #Used to compare the similarity of id images obtained
    def compare_images(self,imageA, imageB):
        m = self.mse(imageA, imageB)
        return m

    #used to draw rectangle on frame, face detection and returns coordinates of the faces, draw rectangle on faces
    def imageCapture(self,frame,quality):
        face_locations = []
        #ret, frame = cap.read()
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
    def verifyFace(self,encoding_1,encoding_2):
        #compute similarity of face
        distance = np.linalg.norm(np.array(encoding_1) - np.array(encoding_2), axis=1)
        if(distance<0.45):
            return True
        else:
            return False

    #check id similarity
    def verifyID(self,imageToVerify):
        isOriginal = False
        imageToVerify_resized = cv2.resize(imageToVerify,(500,500))
        for item in self.images:
            score = (self.compare_images(item, imageToVerify_resized))
            if (score< 1500000):
                isOriginal = True
                #print("ginal ginal original")
                break
        return isOriginal

    # verify faces
    def faceVerification(self,coords):
        img = face_recognition.load_image_file('image.jpg')
        encoding_one = face_recognition.face_encodings(img,[coords[0]])
        encoding_two = face_recognition.face_encodings(img,[coords[1]])

        return(self.verifyFace(encoding_one,encoding_two))

    #main verification function
    def verification(self,coords):
        idImg = cv2.imread('id.jpg')
        if(self.verifyID(idImg)):
            if(self.faceVerification(coords)):
                return "VerificationSuccess"
            else:
                return "FaceVerificationFailed"
        else:
            return "IdVerificationFailed"






