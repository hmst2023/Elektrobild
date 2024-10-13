import os
import cv2
import mouse
from gpiozero import Button

shut_But = Button(3)
os.chdir('/home/pi/flight')
cam = cv2.VideoCapture(0)
cap = cv2.VideoCapture('color.mp4')
mask_vid = cv2.VideoCapture('alpha_channel.mp4')

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)

cv2.namedWindow('test', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('test', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
mouse.move(720,480, True )

text_array = ['starting']
font = cv2.FONT_HERSHEY_DUPLEX
font_thickness = 1
font_scale = 1
org = (480,290)
actual_org = list(org)
text2scroll = text_array.pop()


while True:
    ret, foreground_frame = cap.read()
    _, camera_frame = cam.read()
    rot, mask_frame = mask_vid.read()
    (text_width, _), _ = cv2.getTextSize(text2scroll, font, font_scale, font_thickness)
    
    if actual_org[0] < -text_width:
        actual_org = list(org)
        if text_array:
            text2scroll = text_array.pop()
        else:
            try:
                with open(r'test.txt', 'r') as file:
                    for line in file:
                        x = line[:-1]
                        text_array.append(x)
                file.close()
            except FileNotFoundError:
                text2scroll = "check web connection"
    
    if (rot and True):
        im_gray = cv2.cvtColor(mask_frame, cv2.COLOR_BGR2GRAY)
        test = camera_frame[0:320,0:480]
        cv2.bitwise_and(foreground_frame, foreground_frame, test,  mask=im_gray)
        cv2.putText(test, text2scroll, actual_org, font, font_scale, (255, 255, 255), font_thickness)

        cv2.imshow('test', test)
        actual_org[0] -= 2
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        mask_vid.set(cv2.CAP_PROP_POS_FRAMES, 0)

    if cv2.waitKey(40) & 0xFF == ord('q'):
        cap.release()
        cam.release()
        mask_vid.release()
        cv2.destroyAllWindows()
        break
    if shut_But.is_pressed:
        cap.release()
        cam.release()
        mask_vid.release()
        cv2.destroyAllWindows()
        print('going down')
        os.system("shutdown -h now")
        break
