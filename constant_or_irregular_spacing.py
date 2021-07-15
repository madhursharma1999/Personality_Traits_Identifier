def spacing(path,dx,dy,dxw,dyw,thresh_hold) :
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
    kernel = np.ones((dy,dx), np.uint8) # lines
    #kernel = np.ones((5,12), np.uint8)  # for words
    #kernel = np.ones((5,1), np.uint8) # for characters
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)
    
    #find contours
    ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #sort contours
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
    
    listofx=[]
    spaces=[]
    for i, ctr in enumerate(sorted_ctrs):
        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)
    
        # Getting ROI
        roi = image[y:y+h, x:x+w]
        
        #########################################
        image2 = roi
        
        #grayscale
        gray2 = cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY)
        
        #binary
        ret2,thresh2 = cv2.threshold(gray2,97,255,cv2.THRESH_BINARY_INV)
        
        #dilation
        kernel2 = np.ones((dyw,dxw), np.uint8)  # for words
        img_dilation2 = cv2.dilate(thresh2, kernel2, iterations=1)
        
        #find contours
        ctrs2, hier2 = cv2.findContours(img_dilation2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
        #sort contours
        sorted_ctrs2 = sorted(ctrs2, key=lambda ctr3: cv2.boundingRect(ctr3)[0])
        temp=[[]]
        temp.clear()
        for i2, ctr2 in enumerate(sorted_ctrs2):
            # Get bounding box
            x2, y2, w2, h2 = cv2.boundingRect(ctr2)
            temp.append([x2,y2,x2+w2,y2+h2])
            # Getting ROI
            roi2 = image2[y2:y2+h2, x2:x2+w2]
   
        for coord in range(len(temp)-1):
            #print(temp[coord+1][0]-temp[coord][2])
            spaces.append(temp[coord+1][0]-temp[coord][2])
        
    variance_data=0
    if len(spaces)>1 :
        variance_data=abs(statistics.variance(spaces))
    
    dev_data=math.sqrt(variance_data)
    
    mean_data=spaces[0]
    if len(spaces)>1 :
        mean_data=statistics.mean(spaces)
    
    per=0
    if mean_data!=0:
        per=(dev_data/mean_data)*100

    cv2.destroyAllWindows()
    print("Personality traits based on whether spacing between words is regular or not :")
    if per<=40 :
        print("Regular spacing indicates confidence, regularity and maturity")
    else :
        print("Irregular spacing indicates confusion, irregularity and risk taking behaviour")
