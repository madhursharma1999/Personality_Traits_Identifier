def RightMargin(path,dx,dy,thresh_hold):
    import cv2
    import numpy as np
    import statistics
    
    image = cv2.imread(path)
    width = image.shape[1]
    
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
    rightMargin=[]
    for i, ctr in enumerate(sorted_ctrs):
        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)
    
        # Getting ROI
        roi = image[y:y+h, x:x+w]
        
        listofx.append([x,x+w,y,y+h])
        rightMargin.append(x+w)

    
    margin=width-rightMargin[0]
    if len(rightMargin)>1 :
        margin=width-statistics.mean(rightMargin)
    
    print("Personality traits based on right margin of handwriting :")
    if margin<=0.08*(width):
        print("Extroversion, sociability, precipitation, aggression in order to defend himself from the pressure of the environment")
    elif margin<=0.12*(width):
        print("Expresses equilibrium in relationships, self-control, prudence, reserved, originality, good taste, distinction")
    else:
        print("Fear to risk, to the future, shyness, introversion")
