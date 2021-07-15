def MarginVariance(path,dx,dy,thresh_hold):
    import cv2
    import numpy as np
    import statistics
    import math
    
    #import image
    image = cv2.imread(path)
    
    #grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    
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

    
    var_left_margin=0
    if len(leftMargin)>1 :
        var_left_margin=abs(statistics.variance(leftMargin))
        
    dev_left_margin=math.sqrt(var_left_margin)
    
    mean_left_margin=leftMargin[0]
    
    if len(leftMargin)>1 :
        mean_left_margin=statistics.mean(leftMargin)
    
    per=0
    if mean_left_margin!=0:
        per=(dev_left_margin/mean_left_margin)*100

    print("Personality traits based on whether left margin is regular or not :")
    if per<=30 :
        print("Constant left margin which indicates good manners")
    else:
        print("Irregular left margin which indicates careless in nature")

