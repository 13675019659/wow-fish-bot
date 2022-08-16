# -*- coding: utf-8 -*-
import os
import random
import sys
import time
import webbrowser

import cv2
import numpy as np
#
import pyautogui
from PIL import ImageGrab
from infi.systray import SysTrayIcon
#
from win10toast import ToastNotifier
from win32gui import GetWindowText, GetForegroundWindow, GetWindowRect

#日志
from logging import config,getLogger
from log import logsettings
config.dictConfig(logsettings.LOGGING_DIC)#在logging模块中加在logsettings.py中定义的字典
logger1=getLogger('钓鱼日志')#获取到定义的loggers来产生日志

dev = False
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def app_pause(systray):
    global is_stop
    is_stop = False if is_stop is True else True
    # print ("Is Pause: " + str(is_stop))
    if is_stop is True:
        systray.update(
            hover_text=app + " - On Pause")
    else:
        systray.update(
            hover_text=app)

def app_destroy(systray):
    # print("Exit app")
    sys.exit()

def app_about(systray):
    # print("github.com/YECHEZ/wow-fish-bot")
    webbrowser.open('https://github.com/YECHEZ/wow-fish-bot')


def find_float(img_name):
    logger1.info('Looking for float')

    # todo: maybe make some universal float without background?
    for x in range(0, 13):
        template = cv2.imread('var/fishing_float_' + str(x) + '.png', 0)

        img_rgb = cv2.imread(img_name)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        # print('got images')
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.6
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        if loc[0].any():
            print('Found ' + str(x) + ' float')
            if dev:
                cv2.imwrite('var/fishing_session_' + str(int(time.time())) + '_success.png', img_rgb)
            return (loc[1][0] + w / 2) / 2, (loc[0][0] + h / 2) / 2


def move_mouse(place):
    x, y = place[0], place[1]
    logger1.info("Moving cursor to " + str(place))
    # autopy.mouse.smooth_move(int(screen_start_point[0]) + x , int(screen_start_point[1]) + y)
    # win32api.SetCursorPos([x, y])
    pyautogui.moveTo(x + 650, y + 200, 0.3)

#加鱼饵 限制10分30秒加一次鱼饵
def add_bait(starttime):
    baitTime = 60*10+30;
    endtime = time.time();

    timeArrayStart = time.localtime(starttime)
    otherStyleTimeStart = time.strftime("%Y-%m-%d %H:%M:%S", timeArrayStart)
    timeArrayEnd = time.localtime(endtime)
    otherStyleTimeEnd = time.strftime("%Y-%m-%d %H:%M:%S", timeArrayEnd)
    logger1.info("加鱼饵时间时间对比开始时间---开始时间="+otherStyleTimeStart+";---结束时间="+otherStyleTimeEnd)
    if(endtime-starttime>baitTime):
        #按2键开始上鱼饵
        logger1.info("模拟键2==!")
        pyautogui.press('2')
        #休眠10秒 返回当前时间
        time.sleep(10)
        logger1.info("上鱼饵完成，返回")
        return time.time();
    else:
        #返回原来的时间
        return starttime;

if __name__ == "__main__":
    starttime = time.time();
    is_stop = True
    flag_exit = False
    lastx = 0
    lasty = 0
    is_block = False
    new_cast_time = 0
    recast_time = 40
    wait_mes = 0
    app = "WoW Fish BOT by YECHEZ"
    link = "github.com/YECHEZ/wow-fish-bot"
    app_ico = resource_path('wow-fish-bot.ico')
    menu_options = (("Start/Stop", None, app_pause),
                    (link, None, app_about),)
    systray = SysTrayIcon(app_ico, app,
                          menu_options, on_quit=app_destroy)
    systray.start()
    toaster = ToastNotifier()
    toaster.show_toast(app,
                       link,
                       icon_path=app_ico,
                       duration=5)
    while flag_exit is False:
        if is_stop == False:
            if GetWindowText(GetForegroundWindow()) != "魔兽世界":
                if wait_mes == 5:
                    wait_mes = 0
                    toaster.show_toast(app,
                                       "Waiting for World of Warcraft"
                                       + " as active window",
                                       icon_path='wow-fish-bot.ico',
                                       duration=5)
                logger1.info("等待魔兽世界作为活动窗口")
                systray.update(
                    hover_text=app
                    + " - Waiting for World of Warcraft as active window")
                wait_mes += 1
                time.sleep(2)
            else:
                #已进入worldofwarcraft以开始监控
                logger1.info("已进入worldofwarcraft以开始监控")
                systray.update(hover_text=app)
                rect = GetWindowRect(GetForegroundWindow())

                if is_block == False:
                    logger1.info("模拟键1==开始钓鱼！")
                    lastx = 0
                    lasty = 0
                    pyautogui.press('1')
                    new_cast_time = time.time()
                    is_block = True
                    time.sleep(2)
                else:
                    #left ;top; right;bottom;
                    #分别表示该窗口的/左侧/顶部/右侧/底部坐标
                    fish_area = (0, rect[3] / 2, rect[2], rect[3])

                    img = ImageGrab.grab(fish_area)
                    img_np = np.array(img)
                    #cv2.COLOR_BGR2RGB = 正常的图像
                    #cv2.COLOR_BGR2HSV = 染色 红色
                    #cv2.cvtColor()用来实现类型转换，比如BGR==>HSV或者BGR==>GRAY等等，下面的物体跟踪就是基于HSV值来做的。

                    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
                    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                    cv2.imwrite(os.path.join('abc1.jpg'), frame)
                    cv2.imwrite(os.path.join('abc2.jpg'), frame_hsv)

                    #0,0,255 蓝色
                    #255,0,255 深红色
                    h_min = np.array((0, 0, 253), np.uint8)
                    h_max = np.array((255, 0, 255), np.uint8)
                    #然后利用cv2.inRange函数设阈值，去除背景部分
                    #第一个参数：hsv指的是原图
                    #第二个参数：lower_red指的是图像中低于这个lower_red的值，图像值变为0
                    #第三个参数：upper_red指的是图像中高于这个upper_red的值，图像值变为0
                    #而在lower_red～upper_red之间的值变成255
                    mask = cv2.inRange(frame_hsv, h_min, h_max)

                    #图像矩将帮助我们计算一些特征，如物体的质心，物体的面积等
                    #cv2.moments() 函数可以给出计算后所有矩值的字典dictionary
                    #（1）空间矩
                    #零阶矩：m00
                    #一阶矩：m10, m01
                    #二阶矩：m20, m11, m02
                    #三阶矩：m30, m21, m12, m03
                    #（2）中心矩
                    #二阶中心矩：mu20, mu11, mu02
                    #三阶中心矩：mu30, mu21,mu12, mu03
                    #（3）归一化中心矩
                    #二阶Hu矩：nu20, nu11, nu02
                    #三阶Hu矩：nu30, nu21, nu12, nu03
                    moments = cv2.moments(mask, 1)
                    dM01 = moments['m01']
                    dM10 = moments['m10']
                    dArea = moments['m00']

                    b_x = 0
                    b_y = 0
                    #判断屏幕发生变化是，把鼠标移动到变化的位置进行点击
                    if dArea > 0:
                        b_x = int(dM10 / dArea)
                        b_y = int(dM01 / dArea)
                    if lastx > 0 and lasty > 0:
                        if lastx != b_x and lasty != b_y:
                            logger1.info("监测到浮漂有动静")
                            is_block = False
                            if b_x < 1: b_x = lastx
                            if b_y < 1: b_y = lasty

                            # 控制鼠标移动,duration为持续时间
                            pyautogui.moveTo(b_x, b_y+fish_area[1], duration=0.3)

                            #place = find_float('abc1.jpg')
                            #print('Float found at ' + str(place))
                            #move_mouse(place);

                            #pyautogui.keyDown('shiftleft')
                            pyautogui.mouseDown(button='right')
                            pyautogui.mouseUp(button='right')
                            #pyautogui.keyUp('shiftleft')
                            logger1.info("Catch !")
                            #按2键上鱼饵 2键绑定上鱼饵红
                            starttime = add_bait(starttime);
                            sleepi = random.randrange(2,5);
                            time.sleep(sleepi);
                    lastx = b_x
                    lasty = b_y

                    # show windows with mask
                    #cv2.imshow("fish_mask", mask)
                    #cv2.imshow("fish_frame", frame)

                    if time.time() - new_cast_time > recast_time:
                        logger1.info("40秒过去了鱼还没上钩,重新抛竿")
                        is_block = False
            #if cv2.waitKey(1) & 0xFF == 27:
            #    print("break")
            #    break
        else:
            logger1.info("当前是暂停状态")
            systray.update(hover_text=app + " - On Pause")
            time.sleep(2)