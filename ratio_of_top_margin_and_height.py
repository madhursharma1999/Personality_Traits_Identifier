def TopMargin(path,dx,dy,thresh_hold):
    import cv2
    import numpy as np
    import statistics
    
    #import image
    image = cv2.imread(path)
    height = image.shape[0]
    
    #grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #cv2.imshow('gray',gray)
    #cv2.waitKey(0)
    
    #binary
    ret,thresh = cv2.threshold(gray,thresh_hold,255,cv2.THRESH_BINARY_INV)
    
    #dilation
    kernel = np.ones((dy,dx), np.uint8) # for lines
    #kernel = np.ones((5,12), np.uint8)  # for words
    #kernel = np.ones((5,2), np.uint8) # for characters
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)
    
    #find contours
    ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #sort contours
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[1])
    
    listofx=[]
    for i, ctr in enumerate(sorted_ctrs):
        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)
    
        # Getting ROI
        roi = image[y:y+h, x:x+w]
        
        listofx.append([x,x+w,y,y+h])
        
     #   show ROI
     #   cv2.imshow('segment no:'+str(i),roi)
     #   cv2.rectangle(image,(x,y),( x + w, y + h ),(90,0,255),2)
     #   cv2.waitKey(0)
    
    topMargin=listofx[0][2]

    print("Personality traits based on top margin of handwriting :")
    if topMargin<=0.1*(height):
        print("Need for prominence, proximity feelings towards the others or excessive trust, extroversion, tendency to selfishness")
    elif topMargin<=0.2*(height):
        print("Knows how to listen and how to provide space for the others to communicate. Formality, introversion")
    else:
        print("Introversion, difficulty for relating to others")
