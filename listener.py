from queue import Empty
from time import sleep

import win32api
import win32con
import win32gui

from pynput import keyboard

#import keyboard

# 点击按钮
def on_press(key):
    print('alphanumeric key {0} pressed'.format(key.char))
    if hwnd != Empty :
        print("hwnd is not Empty")
        title = win32gui.GetWindowText(hwnd)    # 窗口标题
        print(title)
        tid = win32gui.FindWindowEx(hwnd, None, 'Edit', None)
        win32gui.SendMessage(tid, win32con.WM_SETTEXT, None, '{0}'.format(key.char));




global hwnd;
hwnd= Empty

# 释放按钮，按esc按键会退出监听
def on_release(key):
    global hwnd
    print('{0} 被释放'.format(key))
    #keyboard.KeyCode.from_char('q')

    if key == keyboard.Key.f2 :
        print("in===")
        point = win32api.GetCursorPos()  # 鼠标位置
        hwnd = win32gui.WindowFromPoint(point)   # 窗口句柄

    if key == keyboard.Key.esc:
        return False


# 创建监听
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

if __name__ == "__main__":
    pass

