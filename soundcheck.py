import sounddevice as sd
import numpy as np
import time
import os


fs = 44100     # 采样率
length = 5     # 采样时长

# sd.default.device[0] 标识默认音频输入
# 执行 sd.query_devices()
# 选择立体声混音通道
sd.default.device[0] = 17

while(True):
    print('开始检测5秒声音')
    recording = sd.rec(frames=fs*length, samplerate=fs, blocking=True,
                       channels=1)

    maxAmplitude = np.max(recording)
    print('max amplitude = %f' % maxAmplitude)

    # 经过测试 在没有音频播放时，最大值小于0.00
    if maxAmplitude > 0.005:
        print('当前有声音输出')
    else:
        print('当前没有声音，执行脚本')
        os.system('C:/Tool/AutoHotkey/AutoHotkey64.exe D:/videoplay.ahk')
        time.sleep(5)
