
import sys
import time

import win32gui
import win32con
#http://t.zoukankan.com/Anec-p-14644939.html
from pykeyboard import PyKeyboard



if __name__ == "__main__":
    print('==');
    win = win32gui.FindWindow(None,'新建文本文档 (2).txt - 记事本')
    print(win);
    tid = win32gui.FindWindowEx(win, None, 'Edit', None)
    print(tid);

    win32gui.SendMessage(tid, win32con.WM_SETTEXT, None, 'hello');

    #win32gui.SetForegroundWindow(tid)  # 设置前置窗口
    #time.sleep(3)
    #win32gui.SendMessage(win, win32con.WM_SETTEXT, None, 'hello')
    #win32gui.SendMessage(tid, win32con.WM_SETTEXT, None, 'helloddddsada');

    #k = PyKeyboard();
    #k.tap_key('e')
    exit();
