import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://final-face-recog-attendance-default-rtdb.firebaseio.com/',
    'storageBucket':'final-face-recog-attendance.appspot.com'
})

# import img
folderPath = 'Images'
PathList = os.listdir(folderPath)
print(PathList)
imgList = []
studentsId = []
for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentsId.append(os.path.splitext(path)[0])
    imgName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(imgName)
    blob.upload_from_filename(imgName)


print(studentsId)

def findEncodings(imageList):
    encodeList = []
    for img in imageList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)


    return encodeList

print("encoding started")
encodeListSearched = findEncodings(imgList)
encodeListSearchedWithIds = [encodeListSearched, studentsId]
#print(encodeListSearched)
print("encoding finished")

file = open("DneEncodeFile.pickle", "wb")
pickle.dump(encodeListSearchedWithIds, file)
file.close()
print("saved!")
