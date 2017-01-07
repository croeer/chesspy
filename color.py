import cv2
import numpy as np
import imutils

def getTargetField( img_board ):
    imgray = cv2.cvtColor(img_board,cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(imgray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #print 'Found %d contours' % (len(contours))
    # find board
    max_area = 0
    best_cnt = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            if area > max_area:
                max_area = area
                best_cnt = cnt
    
    mask = np.zeros((img_board.shape),np.uint8)
    cv2.drawContours(mask,[best_cnt],0,255,-1)
    cv2.drawContours(mask,[best_cnt],0,0,2)
    res = cv2.bitwise_and(img_board,mask)
    #cv2.imwrite('detectedtarget.png',res)

    return res, cv2.boundingRect(best_cnt)

def detectTargetField( img_rgb):
    lower = np.array([250, 120, 80], dtype="uint8")
    upper = np.array([255, 130, 90], dtype="uint8")

    mask = cv2.inRange(img_rgb, lower, upper)
    output = cv2.bitwise_and(img_rgb, img_rgb, mask = mask)

    return getTargetField( output )

if __name__ == '__main__':
    img = cv2.imread("outboard.png")
    #output = detectTargetField( img )
    #img_masked,b = getTargetField( output )

    img_masked,b = detectTargetField( img )

    print b
    img_field = img[ b[1]:b[1]+b[3] , b[0]:b[0]+b[2] ]
    cv2.imshow("detected target field", img_field)
    cv2.waitKey(0)