
import time
import threading
import ctypes

import uiautomation as auto
import sounddevice as sd
import numpy as np

class WinSound():
    def __init__(self):
        self.fs = 44100             # 采样率
        self.length = 5             # 采样时长
        sd.default.device[0] = 19   # 虚拟声卡

    def Check(self):
        rec = sd.rec(frames=self.fs*self.length, samplerate=self.fs, blocking=True, channels=1)
        maxAmplitude = np.max(rec)
        if maxAmplitude > 0.005:
            return True
        else:
            return False

class WinUIA():
    def __init__(self, className='Chrome_WidgetWin_1'): # 默认EDGE浏览器
        self.Item = None
        self.Window = auto.WindowControl(searchDepth=1, ClassName=className)
        
    def FindWindowItem(self, window, name):
        for item in window.GetChildren():
            if self.Item is not None:
                return
            # print(item)
            if len(item.Name.strip()) > 0:
                if name in item.Name:
                    self.Item = item
                    return
            self.FindWindowItem(item, name)

    def GetItem(self, itemName):
        if not self.Window.Exists(3, 1):
            # print('Can not find Edge window')
            return None
        self.Item = None
        self.FindWindowItem(self.Window, itemName)
        if self.Item is None:
            # print('Can not find item:', itemName) 
            return None
        return self.Item

    def WindowMaximize(self):
        if self.Window is not None:
            self.Window.Maximize()

    def WindowMinimize(self):
        if self.Window is not None:
            self.Window.Minimize()

    def WindowClick(self, x, y):
        if self.Window is not None:
            self.Window.Click(x, y)

    def Click(self, item):
        if item is not None:
            self.Window.Maximize()
            item.Click(0, 0)
            self.Window.Minimize()


def closeMessage(title, close_until_seconds):
    time.sleep(close_until_seconds)
    wd = ctypes.windll.user32.FindWindowA(0, title)
    ctypes.windll.user32.SendMessageA(wd, 0x0010, 0, 0)
    return

def MessageBox(text, title='银商学堂', code=0x41):
    return ctypes.windll.user32.MessageBoxA(0, text, title, code)


def AutoCloseMessageBox(text, title='银商学堂', close_until_seconds=5):
    t = threading.Thread(target=closeMessage, args=(title.encode('gbk'), close_until_seconds))
    t.start()
    return MessageBox(text, title.encode('gbk'))

def GetLocalTime():
    return time.strftime('%H:%M:%S', time.localtime(time.time()))


if __name__ == '__main__':
    
    winSound = WinSound()
    winUIA = WinUIA()

    while True:
        print(GetLocalTime(), 'Listening...')
        winUIA.WindowMinimize()
        time.sleep(30)
        
        if winSound.Check() is True:
            continue

        winUIA.WindowMaximize()
        time.sleep(1)

        item = winUIA.GetItem('继续学习')
        if item is not None:
            if AutoCloseMessageBox('视频播放暂停，是否忽略？'.encode('gbk')) != 2:
                continue
            pos = item.GetPosition()
            winUIA.WindowClick(pos[0], pos[1]+30)
            print(GetLocalTime(), '播放状态：', '点击继续学习')
            continue

        item = winUIA.GetItem('秒')
        if item is not None:
            print('剩余时间：', item.Name.strip())
            
        item = winUIA.GetItem('恭喜您已完成本视频的学习')
        if item is not None:
            print(GetLocalTime(),  '播放状态：', '已完成')
            MessageBox('播放完毕。', code=0x40)
            continue

        print(GetLocalTime(), '播放状态：', '未检测到播放页面')
        MessageBox('未检测到播放页面', code=0x40)
