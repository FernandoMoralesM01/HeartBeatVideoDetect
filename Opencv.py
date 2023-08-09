import cv2
import numpy as np
import time
import mediapipe as mp
import matplotlib.pyplot as plt
from numpy import savetxt
import scipy.signal as sgnl
from scipy.signal import find_peaks

mpFaceDetection = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
faceDetectio = mpFaceDetection.FaceDetection()

def faceDetect(frame):
    if frame is not None:
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = faceDetectio.process(imgRGB)

        if (results.detections):
            for id,detection in enumerate (results.detections):
                ih, iw, ic = frame.shape
                
                keypoints = detection.location_data.relative_keypoints
                rightEye = int(keypoints[0].y * ih), int(keypoints[0].x * iw)
                leftEye = int(keypoints[1].y * ih), int(keypoints[1].x * iw)
                lips = int(keypoints[3].y * ih), int(keypoints[3].x * iw)

                bboxC = detection.location_data.relative_bounding_box
                bbox = int (bboxC.xmin * iw), int (bboxC.ymin * ih), int (bboxC.width * iw), int (bboxC.height * ih)
                #cv2.rectangle(frame, bbox, (255, 0, 255), 2)
                #cv2.circle(frame, (keypoints[0]), radius=1, color=(0, 0, 255), thickness=-1)
                frame[rightEye[0]: rightEye[0]+5, rightEye[1]: rightEye[1]+5] = [0, 0, 255]
                frame[leftEye[0]: leftEye[0]+5, leftEye[1]: leftEye[1]+5] = [0, 0, 255]
                frame[lips[0]: lips[0]+5, lips[1]: lips[1]+5] = [0, 0, 255]
                

                #cv2.putText(frame, f'Guapeton: {int(detection.score[0] * 100)} %', (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (0, 0, 255), 1)
                
                #crop_img = frame[bbox[1]:bbox[3] + bbox[1], bbox[0]:bbox[2] + bbox[0]]

                cachetes = frame[bbox[1] - int(0.1 * bbox[1]): rightEye[0] - int(0.09 * rightEye[0]) ,rightEye[1]-int(0.02 * rightEye[1]):leftEye[1] + int(0.02 * leftEye[1])]
                #bbox2 = rightEye[1], leftEye[0] - 20, (leftEye[1]  - rightEye[1]), -50
                #cv2.rectangle(frame, bbox2, (255, 100, 0), 2)
                

            return cachetes, True, frame
        else:
            return frame, True, frame
    return frame, False, frame



def main():
    butter = sgnl.butter(6, [1*2/12, 2*2/12], output='sos', btype= 'bandpass')

    B = []
    G = []
    R = []

    B_G = []
    B_R = []

    G_B = []
    G_R = []

    R_B = []
    R_G = []

    Combina = []
    #url = "http://192.168.1.72:8080/video"
    #url = 0
    #url = "C://Users//fercy//OneDrive//Escritorio//HeartBeatCam//Prueba1.mp4"
    url = 'C:/Users/fercy/OneDrive/Escritorio/HeartBeatCam/Test.mp4'
    #url ="C:/Users/fercy/Downloads/20230808_210554.mp4"
    #url = "C:/Users/fercy/OneDrive/Documentos/ITALIA/20230408_132718.mp4"

    cap = cv2.VideoCapture(url)
    pTime = 0
    
    while (cap.isOpened()):
        
        camera, imag = cap.read()
        
        frame, siLee, og = faceDetect(imag)
        if(not siLee):
            break
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        #print(fps)
        #cv2.putText(frame, f'fps: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, (255, 0, 0), 1)

        frame[:,:, 1] = frame[:,:, 1] ** 2
        frame[:,:, 0] = frame[:,:, 0] ** 2
        frame[:,:, 2] = frame[:,:, 0] ** 2

        B.append(np.mean(frame[:,:, 0]))
        G.append(np.mean(frame[:,:, 1]))
        R.append(np.mean(frame[:,:, 2])) 
        
        if(len(G) > 94):
            G_filt = sgnl.sosfiltfilt(butter, G)
            B_filt = sgnl.sosfiltfilt(butter, B)
            R_filt = sgnl.sosfiltfilt(butter, R)
            

            Combina.append (G_filt[-1] * 0.5  + B_filt[-1] * 0.3 + R_filt[-1] * 0.1)
            peaks, _ = find_peaks(Combina, height= - 0.05)
            print(peaks)
            if((peaks != None).any()):
                print(peaks[-1], len(Combina))
                if(len(Combina) - 2 == peaks[-1] or len(Combina) - 2 == peaks[-1] + 1 or len(Combina) - 2 == peaks[-1] + 2):
                    #frame[:,:, 1] = frame[:,:, 1] * 1.0
                    #frame[:,:, 0] = frame[:,:, 0] * 1.0
                    frame[:,:, 2] = 255 + frame[:,:, 2]
                    #time.sleep(0.5)
                    print("Latido")
                
        cv2.imshow("Frame", og)
        cv2.waitKey(30)
        
    
    B = np.array(B)
    G = np.array(G)
    R = np.array(R)

    plt.figure()
    Combina = np.array(Combina)
    plt.plot(Combina)
    
    plt.plot(peaks, Combina[peaks], "x")
    plt.plot(np.zeros_like(Combina), "--", color="gray")

    plt.show()
    print(peaks)

    Guarda = [B[40:], G[40:], Combina]
    savetxt("C:/Users/fercy/OneDrive/Escritorio/HeartBeatCam/colores.csv", Guarda, delimiter=',')
    print("Guardado")

if __name__ == "__main__":
    main()

#if (R[-1]/G[-1] > 3.3):
#print("HB",np.mean(frame[2]) )
#frame[:,:, 0] = 255
#frame[:,:, 1] = 1
#frame[:,:, 2] = 1 