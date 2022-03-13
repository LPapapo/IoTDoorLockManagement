import cv2
import RPi.GPIO as GPIO
import time
from datetime import datetime
import MySQLdb
from enum import Enum

relay = 17;
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(relay , GPIO.OUT)
GPIO.output(relay , 0)
GPIO.output(relay , 1)

# set up camera object
cap = cv2.VideoCapture(0)

# QR code detection object
detector = cv2.QRCodeDetector()

class Severity(Enum):
    ACCESS=1
    DENIED=2
  


db = MySQLdb.connect(host="localhost",   
                     user="user",        
                     passwd="12345",  
                     db="BALENA_DOOR_DB")      

cur = db.cursor()

    
def logger(severity , message , timestamp , userid):
    
       
        if userid is not None :
            cur.execute("INSERT INTO D_LOG(USER_ID, SEVERITY, MESSAGE, CREATED_ON) VALUES(%s, %s, %s, %s)", (userid, severity.name, message, timestamp))
        else:
            cur.execute("INSERT INTO D_LOG(SEVERITY, MESSAGE, CREATED_ON) VALUES(%s, %s, %s)", (severity.name, message, timestamp))
     
            

        # Commit to DB
        db.commit()
        
def startCamera():
    
    prevTime=0
    doorUnlock= False


    while (True):    
        # get the image
        _, img = cap.read()
    
        # get bounding box coords and data
        data, bbox, _ = detector.detectAndDecode(img)
    
        now = datetime.now()
  
    
        # if there is a bounding box, draw one, along with the data
        if(bbox is not None):
        
            for i in range(len(bbox)):
                cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255,
                         0, 255), thickness=2)
            
            cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)
        
        
        
            if data:
                print("data found: ", data)
        
                result =  cur.execute("SELECT * FROM D_USER WHERE QR_CODE= %s", [data])
            
                if(result)>0:
                
                    user = cur.fetchone()
        
                    print('Access Granted')
                
                    GPIO.output(17 , 0)
                    prevTime = time.time()
                
                    strTime = now.strftime("%d/%m/%Y %H:%M:%S")
                
                    userid = user[0]
                    message = "User: "+user[1]+' '+user[2]+" was granted access at " + strTime
            
                    doorUnlock = True
                    
                    print('Door Open ')
                            
                else:
                    print('Access Denied')
                
                    logger(Severity.DENIED ,"Acess was denied at "+now.strftime("%d/%m/%Y %H:%M:%S") , now,None)
           
                
    
        if doorUnlock == True and time.time() - prevTime > 5:    
            
            doorUnlock = False
            GPIO.output(17 , 1)
        
            logger(Severity.ACCESS , message, now,userid)
        
            print('Door Locked ')
                
                
        # Below will display the live camera feed to the Desktop on Raspberry Pi OS preview
        cv2.imshow("code detector", img)
    
        #At any point if you want to stop the Code all you need to do is press 'q' on your keyboard
        if(cv2.waitKey(1) == ord("q")):
            break
            

    
  