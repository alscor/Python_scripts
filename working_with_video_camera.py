### Copied from this source: https://www.codingforentrepreneurs.com/blog/opencv-python-web-camera-quick-test/    by  Justin Mitchel, February 22, 2018.
import cv2                      # OpenCV2 module - must be installed before running Video exercises
                                
# How to install OpenCV
# Run the command below in your cmd (Windows)    
# pip install opencv-contrib-python --upgrade
# How to test?
# in python session:
# import cv2; print(cv2.__version__)

####################################################################
# Do not proceed until cv2 is properly working
# Сначала надо установить библиотеки CV2. 
####################################################################

### Working with video
cap = cv2.VideoCapture(0)                           # Camera capture object

while(True):                                        # Infinite loop, will work until you press: q 
    # Capture frame-by-frame
    ret, frame = cap.read()                         # Reading camera input - frame by frame

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Converting original capture into gray frames
    
    # Unblock to draw the frame
    # gray[100:-100,100:105]  = 255
    # gray[100:-100,500:505]  = 255
    # gray[100:105,100:505]   = 255
    # gray[-105:-100,100:505] = 255
    # Display the resulting frame                   
    cv2.imshow('frame',frame)                       # show original frame   
    cv2.imshow('gray',gray)                         # show gray frame
    if cv2.waitKey(20) & 0xFF == ord('q'):          # Condition to break the loop
        break

# When everything done, release the capture
cap.release()                                       # After the loop is over, release camera
cv2.destroyAllWindows()                             # Destroy open windows
