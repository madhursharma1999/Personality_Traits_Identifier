def LeftMargin(path,dx,dy,thresh_hold):
    import cv2
    import numpy as np
    import statistics
    
    image = cv2.imread(path)
    width = image.shape[1]
    
    #grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray',gray)
    cv2.waitKey(0)
    
    #binary
    ret,thresh = cv2.threshold(gray,thresh_hold,255,cv2.THRESH_BINARY_INV)
    cv2.imshow('second',thresh)
    cv2.waitKey(0)
    
    #dilation
    kernel = np.ones((dy,dx), np.uint8) # for lines
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)
    cv2.imshow('dilated',img_dilation)
    cv2.waitKey(0)
    
    #find contours
    ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #sort contours
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
    
    listofx=[]
    leftMargin=[]
    for i, ctr in enumerate(sorted_ctrs):
        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)
    
        # Getting ROI
        roi = image[y:y+h, x:x+w]
        
        listofx.append([x,x+w,y,y+h])
        leftMargin.append(x)
        
        # show ROI
        cv2.imshow('segment no:'+str(i),roi)
        cv2.rectangle(image,(x,y),( x + w, y + h ),(90,0,255),2)
        cv2.waitKey(0)
    
    margin=leftMargin[0]
    if len(leftMargin)>1 :
        margin=statistics.mean(leftMargin)

    cv2.destroyAllWindows()
    print("Personality traits based on left margin of handwriting :")
    if margin<=0.1*(width):
        print("Sense of saving and economy, caution, shyness, introversion")
    elif margin<=0.15*(width):
        print("Equilibrium, good esthetic sense, normal and simple life")
    elif margin<=0.25*(width):
        print("Generosity and extroversion")
    else:
        print("Generosity, audacity, initiative")
