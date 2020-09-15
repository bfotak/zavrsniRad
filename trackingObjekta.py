import cv2

def drawBox(img,bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 3 )

def isipisStanja(img, stanje):
    if stanje == "Tracking":
        cv2.putText(img, stanje, (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(img, stanje, (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

def ispisStatusa(img):
    cv2.rectangle(img,(15,15),(200,90),(255,0,255),2)
    cv2.putText(img, "Fps:", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,255), 2);
    cv2.putText(img, "Status:", (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2);

def obradaIspisaSlike(img, tracker): #ovo nisam uspio bolje zapakirat might not be needed

    success, bbox = tracker.update(img)
    if success:
        #trackiranje.drawBox(img, bbox) #leti van koristi se samo za debugiranje
        isipisStanja(img, stanje="Tracking")
    else:
        isipisStanja(img, stanje= "Lost")

    ispisStatusa(img)

def ispisFpsa(img, Pokreni, fps):
    if Pokreni:

        if fps > 60:
            myColor = (20, 230, 20)
        elif fps > 20:
            myColor = (230, 20, 20)
        else:
            myColor = (20, 20, 230)
        cv2.putText(img, str(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, myColor, 2);
    else: pass