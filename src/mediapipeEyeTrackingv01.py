import mediapipe as mp

import cv2
import numpy as np
import math

# mp_drawing = mp.solutions.drawing_utils
# mp_holistic = mp.solutions.holistic
# mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2)
mp_face_mesh = mp.solutions.face_mesh

# Define the dimensions of the screen resolution
# TODO get resolution dynamically
screenResHeight = 1080
screenResWidth = 1920
# Create a black image with the specified dimensions
imageBG = np.zeros((screenResHeight, screenResWidth, 3), np.uint8)

# Define the dimensions of the webcam resolution
# TODO get resolution dynamically
webcamResHeight = 480
webcamResWidth = 640
#calculate offset to place webcam feed in middle
x_offset=math.floor((screenResWidth-webcamResWidth)/2)
y_offset=math.floor((screenResHeight-webcamResHeight)/2)

#calculate offset to place eyes feed
x_offsetEyeLeft=math.floor(screenResWidth*.3)
y_offsetEyeLeft=math.floor(screenResHeight*.1)
x_offsetEyeRight=math.floor(screenResWidth*.6)
y_offsetEyeRight=math.floor(screenResHeight*.1)

imageYellow = np.ones((50, 50, 3), np.uint8)
imageYellow[:, :] = [0, 255, 255]

cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

LEFT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
# right eyes indices
RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ] 
LEFT_IRIS = [474,475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]

eyeXmax=0.5
eyeXmin=0.5
eyeYmax=0.5
eyeYmin=0.5
lastX=[]
lastY=[]


def showEyesEnlarged(inputImage, inputImageBG, posOnScreenX, posOnScreenY, sizeX, sizeY, mesh_points):
    x,y,w,h = cv2.boundingRect(mesh_points)
    # cv2.rectangle(inputImage,(x,y),(x+w,y+h),(0,255,0),2)
    crop_img = inputImage[y:y+h, x:x+w]
    crop_img = cv2.resize(crop_img, (sizeX, sizeY), interpolation = cv2.INTER_AREA)
    crop_img = cv2.flip(crop_img, 1)
    inputImageBG[posOnScreenY:posOnScreenY+crop_img.shape[0], posOnScreenX:posOnScreenX+crop_img.shape[1]] = crop_img
    return inputImageBG
    
def eyePos(mesh_pointsEye, mesh_pointsIRIS):
    global eyeXmax
    global eyeXmin
    global eyeYmax
    global eyeYmin
    x,y,w,h = cv2.boundingRect(mesh_pointsEye)
    (r_cx, r_cy), r_radius = cv2.minEnclosingCircle(mesh_pointsIRIS)
    
    gazeX = abs((r_cx-x)/(w))
    gazeY = abs((r_cy-y)/(h))
    if(gazeX > eyeXmax):
        eyeXmax = gazeX
    if(gazeX < eyeXmin):
        eyeXmin = gazeX
    if(gazeY > eyeYmax):
        eyeYmax = gazeY
    if(gazeY < eyeYmin):
        eyeYmin = gazeY

    estimatedGazeX = (screenResWidth / (eyeXmax-eyeXmin))*gazeX
    estimatedGazeY = (screenResHeight / (eyeYmax-eyeYmin))*gazeY
    x_offsetYellow=math.floor(estimatedGazeX)
    y_offsetYellow=math.floor(estimatedGazeY)
    return x_offsetYellow, y_offsetYellow

cap = cv2.VideoCapture(0)
# Initiate holistic model
#with mp_holistic.Holistic(refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as face_mesh:

    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor Feed
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Make Detections
        #results = holistic.process(image)
        results = face_mesh.process(image)
        # print(results.face_landmarks)
        
        # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks
        
        # Recolor image back to BGR for rendering
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        img_h, img_w = image.shape[:2]
        if results.multi_face_landmarks:
            # 1. Draw face landmarks
    #         mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS,
            # mp_drawing.draw_landmarks(image, results.multi_face_landmarks, mp_holistic.FACEMESH_TESSELATION,
            #                         mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
            #                         mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
            #                         )
                           
            mesh_points=np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in results.multi_face_landmarks[0].landmark])
            # print(mesh_points.shape)
            cv2.polylines(image, [mesh_points[LEFT_IRIS]], True, (0,255,0), 1, cv2.LINE_AA)
            cv2.polylines(image, [mesh_points[RIGHT_IRIS]], True, (0,255,0), 1, cv2.LINE_AA)
            cv2.polylines(image, [mesh_points[LEFT_EYE]], True, (0,255,0), 1, cv2.LINE_AA)
            cv2.polylines(image, [mesh_points[RIGHT_EYE]], True, (0,255,0), 1, cv2.LINE_AA)
            imageBG = showEyesEnlarged(image, imageBG, x_offsetEyeLeft, y_offsetEyeLeft, 400, 200, mesh_points[LEFT_EYE])
            imageBG = showEyesEnlarged(image, imageBG, x_offsetEyeRight, y_offsetEyeRight, 400, 200, mesh_points[RIGHT_EYE])


            x_offsetYellowR, y_offsetYellowR = eyePos(mesh_points[RIGHT_EYE], mesh_points[RIGHT_IRIS])
            x_offsetYellowL, y_offsetYellowL = eyePos(mesh_points[LEFT_EYE], mesh_points[LEFT_IRIS])
            x_offsetYellow = math.floor((x_offsetYellowL + x_offsetYellowR)/2)
            y_offsetYellow = math.floor((y_offsetYellowL + y_offsetYellowR)/2)

            image = cv2.flip(image, 1)
            imageBG[y_offset:y_offset+image.shape[0], x_offset:x_offset+image.shape[1]] = image
            if(x_offsetYellow+imageYellow.shape[1] > screenResWidth):
                x_offsetYellow = screenResWidth - imageYellow.shape[1]
            if(y_offsetYellow+imageYellow.shape[0] > screenResHeight):
                y_offsetYellow = screenResHeight - imageYellow.shape[0]   
            imageBG[y_offsetYellow:y_offsetYellow+imageYellow.shape[0], x_offsetYellow:x_offsetYellow+imageYellow.shape[1]] = imageYellow
            # cv2.circle(image, center_left, int(l_radius), (255,0,255), 5, cv2.LINE_AA)
            # cv2.circle(image, center_right, int(r_radius), (255,0,255), 5, cv2.LINE_AA)

        # cv2.imshow('Raw Webcam Feed', image)

        # use numpy indexing to place the resized image in the center of background image

        
        # imageBG[y_offsetEyeLeft:y_offsetEyeLeft+crop_img.shape[0], x_offsetEyeLeft:x_offsetEyeLeft+crop_img.shape[1]] = crop_img
        

        cv2.imshow("window", imageBG)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
