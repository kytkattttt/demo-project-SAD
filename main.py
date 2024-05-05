from cvzone.FaceDetectionModule import FaceDetector
import os
import pickle
import bbox
import numpy as np
import cvzone
import numpy as np
import cv2
import face_recognition
import numpy as np
import datetime
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://final-face-recog-attendance-default-rtdb.firebaseio.com/',
    'storageBucket': 'final-face-recog-attendance.appspot.com'
})

bucket = storage.bucket()
cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)

camUI = cv2.imread('resources/background.png')

# Importing the files images into a list
folderFilesPath = 'resources/FILES'
filesPathList = os.listdir(folderFilesPath)
imgFilesList = []
for path in filesPathList:
    imgFilesList.append(cv2.imread(os.path.join(folderFilesPath, path)))
#print(len(imgFilesList))

# encoding file
print("loading")
file = open('DneEncodeFile.pickle', 'rb')
encodeListSearchedWithIds = pickle.load(file)
file.close()
encodeListSearched, studentsId = encodeListSearchedWithIds

# print(studentsId)
print("saved encoded files!")

imgFileType = 0
counter = 0
id = -1
imageStudents = 0

while True:
    success, img = cap.read()

    imgSize = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgSize = cv2.cvtColor(imgSize, cv2.COLOR_BGR2RGB)

    # current frame
    facesFrame = face_recognition.face_locations(imgSize)
    eFrame = face_recognition.face_encodings(imgSize, facesFrame)

    camUI[162:162 + 480, 55:55 + 640] = img
    camUI[44:44 + 633, 808:808 + 414] = imgFilesList[imgFileType]

    for encodeFace, faceLocation in zip(eFrame, facesFrame):
        matches = face_recognition.compare_faces(encodeListSearched, encodeFace)
        distance = face_recognition.face_distance(encodeListSearched, encodeFace)
        # print("matches", matches)
        # print("distance", distance)

        matchIndx = np.argmin(distance)
        # print("matchIndx", matchIndx)

        if matches[matchIndx]:
            # print("Student found")
            # print(studentsId[matchIndx])
            y1, x2, y2, x1 = faceLocation
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
            camUI = cvzone.cornerRect(camUI, bbox, rt=0, t=1)

            id = studentsId[matchIndx]
            if counter == 0:
                counter = 1
                imgFileType = 1

        if counter != 0:

            if counter == 1:
                # data
                studentsIdInfo = db.reference(f'Students/{id}').get()
                print(studentsIdInfo)

                # get image
                blob = bucket.blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imageStudents = cv2.imdecode(array, cv2.COLOR_BGR2RGB)
            # start error
              #  datetimeObject = datetime.strptime(studentsIdInfo['recent_attendance'],
              #                    "%Y-%m-%d %H:%M:%S")
              #  secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
              #  print(secondsElapsed)
              #  if secondsElapsed > 30:
              #   ref = db.reference(f'Students/{id}')
              #   studentsIdInfo = ref.get()#stop part
            # ref.child('recent_attendance').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                # end error

        if 10<counter<20:
            imgFileType = 2
            camUI[44:44 + 633, 808:808 + 414] = imgFilesList[imgFileType]



        if counter<=10:
            cv2.putText(camUI, str(studentsIdInfo['Program']), (1006, 550),
                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (50, 50, 50), 1)
            cv2.putText(camUI, str(studentsIdInfo['block&year']), (1006, 610),
                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (50, 50, 50), 1)
            cv2.putText(camUI, str(id), (1006, 493),
                        cv2.FONT_HERSHEY_COMPLEX, 0.6, (50, 50, 50), 1)

            (w, h), _ = cv2.getTextSize(studentsIdInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
            offset = (440 - w) // 2
            cv2.putText(camUI, str(studentsIdInfo['name']), (810 + offset, 445),
                        cv2.FONT_HERSHEY_COMPLEX, 0.8, (100, 100, 100), 1)

            camUI[175:175 + 216, 909:909 + 216] = imageStudents

        counter += 1

        if counter >= 20:
            counter = 0
            imgFileType = 0
            studentsIdInfo = []
            imageStudents = []
            camUI[44:44 + 633, 808:808 + 414] = imgFilesList[imgFileType]


    #cv2.imshow("attendance", img)
    cv2.imshow("Student-face-cam", camUI)
    cv2.waitKey(1)
