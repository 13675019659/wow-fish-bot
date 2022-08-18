import tkinter
from multiprocessing import process
from tkinter import *
from tkinter.ttk import *
import win32api
import win32gui
import win32con
import win32process
import win32ui
import time

import psutil
import subprocess
from PIL import Image
import os

def main():
    root = Tk()
    root.title('贱工坊-窗口句柄')  # 程序的标题名称
    root.geometry("480x320+512+288")  # 窗口的大小及页面的显示位置
    root.resizable(False, False)  # 固定页面不可放大缩小
    root.iconbitmap("picture.ico")  # 程序的图标

    canvas = tkinter.Canvas(root, bg="#ebebeb", height=400, width=700, borderwidth=-3)  # 创建画布
    canvas.pack(side='top')  # 放置画布（为上端）

    canvas_2 = tkinter.Canvas(root, bg="#ebebeb",cursor='target', height=50, width=50, borderwidth=-2)  # 创建画布
    canvas_2.place(x=402, y=70)  # 放置画布（为上端）
    image_file = tkinter.PhotoImage(file="./Key.png")  # 加载图片文件
    canvas_2.create_image(0, 0, anchor='nw', image=image_file)  # 将图片置于画布上

    canvas_3 = tkinter.Canvas(root, bg="red",  height=40, width=40, borderwidth=-2)  # 创建画布
    canvas_3.place(x=332, y=74)  # 放置画布（为上端）


    # 配置窗口句柄
    var_hwnd = tkinter.StringVar()
    tkinter.Entry(root, width=20,borderwidth=1,bg='#ebebeb',textvariable=var_hwnd).place(x=70,y=10)

    # 配置标题名称
    var_title = tkinter.StringVar()
    tkinter.Entry(root, width=54, borderwidth=1,bg='#ebebeb', textvariable=var_title).place(x=70, y=40)

    # 配置窗口类名
    var_clsname = tkinter.StringVar()
    tkinter.Entry(root, width=20, borderwidth=1, bg='#ebebeb', textvariable=var_clsname).place(x=306, y=10)

    # 配置线程ID
    var_hread_id = tkinter.StringVar()
    tkinter.Entry(root, width=10, borderwidth=1, bg='#ebebeb', textvariable=var_hread_id).place(x=70, y=70)

    # 配置进程ID
    var_process_id = tkinter.StringVar()
    tkinter.Entry(root, width=10, borderwidth=1, bg='#ebebeb', textvariable=var_process_id).place(x=204, y=70)

    # 配置程序名称
    var_process = tkinter.StringVar()
    tkinter.Entry(root, width=29, borderwidth=1, bg='#ebebeb', textvariable=var_process).place(x=70, y=100)

    # 配置程序路径
    var_p_bin = tkinter.StringVar()
    tkinter.Entry(root, width=54, borderwidth=1, bg='#ebebeb', textvariable=var_p_bin).place(x=70, y=130)

    # 配置CPU利用率
    var_mem_percent = tkinter.StringVar()
    tkinter.Entry(root, width=20, borderwidth=1, bg='#ebebeb', textvariable=var_mem_percent).place(x=70, y=160)

    # 配置线程数
    var_num_threads = tkinter.StringVar()
    tkinter.Entry(root, width=20, borderwidth=1, bg='#ebebeb', textvariable=var_num_threads).place(x=306, y=160)

    # 配置窗口左上
    var_top = tkinter.StringVar()
    tkinter.Entry(root, width=6, borderwidth=1, bg='#ebebeb', textvariable=var_top).place(x=70, y=190)

    # 配置窗口左下
    var_left = tkinter.StringVar()
    tkinter.Entry(root, width=6, borderwidth=1, bg='#ebebeb', textvariable=var_left).place(x=70, y=220)

    # 配置窗口右上
    var_right = tkinter.StringVar()
    tkinter.Entry(root, width=6, borderwidth=1, bg='#ebebeb', textvariable=var_right).place(x=194, y=190)

    # 配置窗口右下
    var_bottom = tkinter.StringVar()
    tkinter.Entry(root, width=6, borderwidth=1, bg='#ebebeb', textvariable=var_bottom).place(x=194, y=220)

    # 配置坐标x,y
    var_point = tkinter.StringVar()
    tkinter.Entry(root, width=24, borderwidth=1, bg='#ebebeb', textvariable=var_point).place(x=70, y=250)

    image_file_3 = tkinter.PhotoImage(file="pictures.png")  # 软件第一次打开时要呈现的图片
    Button_2 = Button(canvas_3, image=image_file_3).place(x=0, y=0)
    # 更换软件图标
    def picture():
        try:
            image_file_3.config(file='icon.png')   # 替换
        except:
            pass
    # 图标尺寸
    ico_x = 32
    # 获取软件图标
    def ICON(exePath2):
        try:
            exePath = exePath2.replace("\\", "/")  # 替换
            large, small = win32gui.ExtractIconEx(f'{exePath}', 0)
            useIcon = large[0]
            destroyIcon = small[0]
            win32gui.DestroyIcon(destroyIcon)
            hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
            hbmp = win32ui.CreateBitmap()
            hbmp.CreateCompatibleBitmap(hdc, ico_x, ico_x)
            hdc = hdc.CreateCompatibleDC()
            hdc.SelectObject(hbmp)
            hdc.DrawIcon((0, 0), useIcon)
            bmpstr = hbmp.GetBitmapBits(True)
            img = Image.frombuffer(
                'RGBA',
                (32, 32),
                bmpstr, 'raw', 'BGRA', 0, 1
            )
            img.save('icon.png')
        except:
            pass


    # 通过鼠标移动获取函数
    def showMenu(event):
        try:
            point = win32api.GetCursorPos()  # 鼠标位置
            hwnd = win32gui.WindowFromPoint(point)   # 窗口句柄
            title = win32gui.GetWindowText(hwnd)    # 窗口标题
            clsname = win32gui.GetClassName(hwnd)   # 窗口类名
            hread_id, process_id = win32process.GetWindowThreadProcessId(hwnd)  #线程ID  进程ID
            process = psutil.Process(process_id)     # 程序名称  通过进程ID获取
            p_bin = psutil.Process(process_id).exe()   # 程序路径  通过进程ID获取
            mem_percent = psutil.Process(process_id).memory_percent()   # CPU利用率  通过进程ID获取
            num_threads = psutil.Process(process_id).num_threads()     # 线程数  通过进程ID获取
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)   #窗口坐标  通过窗口句柄获取 四个角的坐标
            picture()    # 更换软件图标
            ICON(p_bin)  # 获取软件图标
            var_hwnd.set(hwnd)
            var_title.set(title)
            var_clsname.set(clsname)
            var_hread_id.set(hread_id)
            var_process_id.set(process_id)
            var_process.set(process.name())
            var_p_bin.set(p_bin)
            var_mem_percent.set(mem_percent)
            var_num_threads.set(num_threads)
            var_left.set(left)
            var_top.set(top)
            var_right.set(right)
            var_bottom.set(bottom)
            var_point.set(point)
        except:
            pass

    # 置顶 通过句柄
    def set_top():
        try:
            win32gui.SetWindowPos(var_hwnd.get(), win32con.HWND_TOPMOST, 0, 0, 0, 0,win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
        except:
            pass
    # 取消置顶 通过句柄
    def set_down():
        try:
            win32gui.SetWindowPos(var_hwnd.get(), win32con.HWND_NOTOPMOST, 0, 0, 0, 0,win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
        except:
            pass
    # 显示在顶部 通过句柄
    def set_yop_p():
        try:
            win32gui.SetForegroundWindow(var_hwnd.get())
        except:
            pass

    # 终止程序
    def kill():
        try:
            subprocess.Popen("taskkill /F /T /PID " + var_process_id.get(), shell=True)
            subprocess.Popen("taskkill /F /T /IM " + process.get(), shell=True)
        except:
            pass

    # 打开文件夹
    def bin():
        pbin = var_p_bin.get().replace("\\", "/")  # 替换
        pbin = os.path.split(pbin)[0].replace("\\", "/")
        os.startfile(str(pbin))

    def Label():
        # 标签
        tkinter.Label(canvas, bg="#ebebeb", text='窗口句柄').place(x=10, y=8)
        tkinter.Label(canvas, bg="#ebebeb", text='窗口标题').place(x=10, y=38)
        tkinter.Label(canvas, bg="#ebebeb", text='窗口类名').place(x=248, y=8)
        tkinter.Label(canvas, bg="#ebebeb", text='线程ID').place(x=10, y=68)
        tkinter.Label(canvas, bg="#ebebeb", text='进程ID').place(x=154, y=68)
        tkinter.Label(canvas, bg="#ebebeb", text='进程名称').place(x=10, y=98)
        tkinter.Label(canvas, bg="#ebebeb", text='进程路径').place(x=10, y=128)
        tkinter.Label(canvas, bg="#ebebeb", text='CPU用量').place(x=10, y=158)
        tkinter.Label(canvas, bg="#ebebeb", text='线程数').place(x=258, y=158)
        tkinter.Label(canvas, bg="#ebebeb", text='窗口左上').place(x=10, y=188)
        tkinter.Label(canvas, bg="#ebebeb", text='窗口左下').place(x=10, y=218)
        tkinter.Label(canvas, bg="#ebebeb", text='窗口右上').place(x=134, y=188)
        tkinter.Label(canvas, bg="#ebebeb", text='窗口右下').place(x=134, y=218)
        tkinter.Label(canvas, bg="#ebebeb", text='坐标x,y').place(x=10, y=248)

    # 鼠标移动控件
    canvas_2.bind("<B1-Motion>", showMenu)
    Button(root, text='强制置顶',   command=set_top).place(x=10, y=280)
    Button(root, text='取消置顶', command=set_down).place(x=100, y=280)
    Button(root, text='显示顶部', command=set_yop_p).place(x=190, y=280)
    Button(root, text='强制终止', command=kill).place(x=280, y=280)
    Button(root, text='打开文件所在位置', command=bin).place(x=370, y=280)

    # 放置二维码
    canvas_4 = tkinter.Canvas(root, bg="red", height=80, width=200, borderwidth=-2)
    canvas_4.place(x=250, y=190)
    image_file_4 = tkinter.PhotoImage(file="./share.png")  # 加载图片文件
    canvas_4.create_image(0, 0, anchor='nw', image=image_file_4)  # 将图片置于画布上

    Label()
    root.mainloop() #运行

if __name__ == '__main__':
    main()

