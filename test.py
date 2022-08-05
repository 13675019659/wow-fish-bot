import os

from win32gui import GetWindowText, GetForegroundWindow, GetWindowRect
from PIL import ImageGrab
import numpy as np
import cv2
import time
import pyautogui
if __name__ == "__main__":
    flag_exit = False
    while flag_exit is False:
        lastx = 0
        lasty = 0
        rect = GetWindowRect(GetForegroundWindow())

        fish_area = (0, rect[3] / 2, rect[2], rect[3])

        #截图
        img = ImageGrab.grab(fish_area)

        img.save("abc0.png");

        img_np = np.array(img)

        print(img_np)
        #cv2.COLOR_BGR2RGB = 正常的图像
        #cv2.COLOR_BGR2HSV = 染色 红色
        frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


        cv2.imwrite(os.path.join('abc1.jpg'), frame)
        cv2.imwrite(os.path.join('abc2.jpg'), frame_hsv)
        #frame.save("abc1.png");
        #frame_hsv.save("abc2.png");

        #cv2.cvtColor()用来实现类型转换，比如BGR==>HSV或者BGR==>GRAY等等，下面的物体跟踪就是基于HSV值来做的。
        #cv2.inRange()在这里主要是用来根据设定阈值范围生成掩模，根据掩模再与原图像进行按位与运算。为了查找方便，附上各个颜色与其对应的HSV值：
        #https://blog.csdn.net/weixin_44525085/article/details/102561269


        h_min = np.array((0, 0, 253), np.uint8)
        h_max = np.array((255, 0, 255), np.uint8)

        mask = cv2.inRange(frame_hsv, h_min, h_max)

        moments = cv2.moments(mask, 1)
        dM01 = moments['m01']
        dM10 = moments['m10']
        dArea = moments['m00']
        print(dM01)
        print(dM10)
        print(dArea)

        b_x = 0
        b_y = 0

        if dArea > 0:
            b_x = int(dM10 / dArea)
            b_y = int(dM01 / dArea)
        if lastx > 0 and lasty > 0:
            if lastx != b_x and lasty != b_y:
                print("Floating power starts to finish!")
                is_block = False
                if b_x < 1: b_x = lastx
                if b_y < 1: b_y = lasty
                pyautogui.moveTo(b_x, b_y + fish_area[1], 0.3)
                pyautogui.keyDown('shiftleft')
                pyautogui.mouseDown(button='right')
                pyautogui.mouseUp(button='right')
                pyautogui.keyUp('shiftleft')
                print("Catch !")
                time.sleep(5)
                exit();
        lastx = b_x
        lasty = b_y

        time.sleep(5)
    exit();