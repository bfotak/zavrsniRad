import cv2
import trackingObjekta as trackiranje
import konture
import detekcijaBoja
import mjerenjeObjekta

#volim jesti mahune

cap = cv2.VideoCapture(0)

# TRACKER INITIALIZATION
tracker = cv2.TrackerCSRT_create()
success, frame = cap.read()
bbox = cv2.selectROI("Tracking",frame, False) #bbox ce biti odreden konturama
tracker.init(frame, bbox)

# određivanje slike
frameWidth = 720
frameHeight = 1280
cap.set(10,160)
cap.set(3, frameHeight)
cap.set(4, frameWidth)

scale = 3 #sluzi za povecanje slika i da podaci budu tocniji ugl sve kasnije treba dijelit sa scaleom
wP = 210 * scale #širina papira A4
hP= 297 * scale  #visina papira A4



def ispisFpsa(img, Pokreni): #ispis fpsa u cosku malo over kill //BITNO! prosljedit iz maina fpse i ovo maknit van u neki utils
    if Pokreni:
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        if fps > 60:
            myColor = (20, 230, 20)
        elif fps > 20:
            myColor = (230, 20, 20)
        else:
            myColor = (20, 20, 230)
        cv2.putText(img, str(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, myColor, 2);
    else: pass

def privremenaFunkcija(): #mumbo jumbo za ispis mjerenja tu je negdje bug vjv
    cv2.polylines(imgContours2, [obj[2]], True, (0, 255, 0), 2)
    nPoints = mjerenjeObjekta.reorder(obj[2])
    nH = round((mjerenjeObjekta.findDis(nPoints[0][0] // scale, nPoints[1][0] // scale) / 10), 1)
    nW = round((mjerenjeObjekta.findDis(nPoints[0][0] // scale, nPoints[2][0] // scale) / 10), 1)
    cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]),
                    (nPoints[1][0][0], nPoints[1][0][1]),
                    (255, 0, 255), 3, 8, 0, 0.05)
    cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]),
                    (nPoints[2][0][0], nPoints[2][0][1]),
                    (255, 0, 255), 3, 8, 0, 0.05)
    x, y, w, h = obj[3]
    cv2.putText(imgContours2, '{}cm'.format(nW), (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                (255, 0, 255), 2)
    cv2.putText(imgContours2, '{}cm'.format(nH), (x - 70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                (255, 0, 255), 2)

konture.sliderKonture() #dosta slicni kao za slidere za boje
detekcijaBoja.slideriBoje() #vjv bitniji od dva slidera treba ih usporediti


#u glavnom kodu se moraju pozivat funkcije redosljedom Original, pračenje, boja, konture, mjerenja
#//ako bude vremena dodati izravno prepoznavanje predmeta i detaljna analiza #bitćevremenamorabit
#ostalo smece koje ide tu je timer bez kojeg se nemreju tickat frameovi
#
#
#
while True:#glavni kod koji je za sad smece
    timer = cv2.getTickCount()
    success, img = cap.read()

    detekcijaBoja.detekcijaBojaMain(img)

    videoSadrzaj=konture.mainContours(img = detekcijaBoja.detekcijaBojaMain(img))

    trackiranje.obradaIspisaSlike(img, tracker)
    ispisFpsa(img, Pokreni = True)
    cv2.imshow("Tracking", img)

    imgContours, conts = mjerenjeObjekta.getContoursMeasurements(img, minArea=50000, filter=4) #s ovim se treba poigrati npr maknit filter
    if len(conts) != 0: #prisjeti se cemu len sluzi
        biggest = conts[0][2]#ovo je za uzimanje papira to je oke
        # print(biggest)
        imgWarp = mjerenjeObjekta.warpImg(img, biggest, hP, wP)
        imgContours2, conts2 = mjerenjeObjekta.getContoursMeasurements(imgWarp,#tu se isto par stvari tereba maknut npr ovaj draw i filter
                                                 minArea=2000, filter=15,
                                                 cThr=[50, 50], draw=False)
        if len(conts) != 0:#kad skuzi da je nesto na papiru napravi mjere
            for obj in conts2:
                privremenaFunkcija()
        cv2.imshow('A4', imgContours2)

    img = cv2.resize(img, (0, 0), None, 0.5, 0.5) #nezz tocno sto ovo radi
    cv2.imshow('Original', img)
    if cv2.waitKey(1) & 0xff == ord('q'):
       break


