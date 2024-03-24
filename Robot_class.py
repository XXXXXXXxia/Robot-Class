import time
import cv2
from aip import AipBodyAnalysis
from threading import Thread

import pyaudio
import wave

#定义录音文件存储路径
input_filename = "input.wav"  # 麦克风采集的语音输入
input_filepath = "D:/Python project/Robot_class/store_data/"  # 输入文件的path，此处路径为录音文件的存储位置！！！
in_path = input_filepath + input_filename

# 以下是配置百度ai的APP_ID API_KEY SECRET_KEY，如果需要的话取消注释即可，
#示例可以去找人体特征识别与手势识别项目下的HumanFeatures_recognition.py或者Gesture_recognition.py中查看，此处不调用
'''
APP_ID = '3267XXXXX'
API_KEY = 'cwdGvBSqxNtc4hXXXXXXXX'
SECRET_KEY = 'vAEIwcYDD2qDxdzBgXXXXXXXXXXXXX'
'''

########定义Robot类，其中有调用摄像头和麦克风的方法
########该Robot类的使用方法：创建一个实例对象（如下面创建了robot对象，然后直接调用robot的方法即可：robot.OpenCamera()就是打开摄像头，robot.OpenMicrophone()
# 是打开麦克风，打开麦克风是会询问一下是否打开，需在运行窗口内输入“是”并回车，之后会进行五秒钟的录音（时间可改），并且将录音结果存至指定位置（位置在上面定义的地方也可以改））
class Robot:

    ####定义调用摄像头的方法
    def OpenCamera(self):
        capture = cv2.VideoCapture(0)  # 0为默认摄像头
        exit_flag_Video = False

        def camera():
            global exit_flag_Video
            while True:
                ret, frame = capture.read()  # 调用OpenCV拍照
                cv2.imshow('frame', frame)  # OpenCV显示图片
                if cv2.waitKey(1) == ord('q'):
                    exit_flag_Video = True
                    break

        Thread(target=camera).start()

        while not exit_flag_Video:
            try:
                ret, frame = capture.read()
                image = cv2.imencode('.jpg', frame)[1]

                print('正在调用摄像头，按q键(英文输入法)停止')

            except:
                print('摄像头打开失败')

            time.sleep(1)

    ####定义调用麦克风的方法
    def OpenMicrophone(self):
        def get_audio(filepath):
            aa = str(input("是否开始录音？（是/否），请在运行窗口直接输入"))
            if aa == str("是"):
                CHUNK = 256
                FORMAT = pyaudio.paInt16
                CHANNELS = 1  # 声道数
                RATE = 11025  # 采样率
                RECORD_SECONDS = 5
                WAVE_OUTPUT_FILENAME = filepath
                p = pyaudio.PyAudio()

                stream = p.open(format=FORMAT,
                                channels=CHANNELS,
                                rate=RATE,
                                input=True,
                                frames_per_buffer=CHUNK)

                print("*" * 10, "开始录音：请在5秒内输入语音")
                frames = []
                for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                    data = stream.read(CHUNK)
                    frames.append(data)
                print("*" * 10, "录音结束\n")

                stream.stop_stream()
                stream.close()
                p.terminate()

                wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
                wf.close()
            elif aa == str("否"):
                exit()
            else:
                print("无效输入，请重新选择")
                get_audio(in_path)

        get_audio(in_path)



########类定义结束，建立实例对象演示

robot = Robot()
#robot.OpenCamera()                ###目前写法是将调用摄像头和录音作为两个独立的线程运行，用到哪个就把哪个的注释取消掉！！！
robot.OpenMicrophone()




'''
######################代码注释/解释：

p = pyaudio.PyAudio()：
这行代码创建了一个 PyAudio 对象 p，用于管理音频设备和流。通过调用 pyaudio.PyAudio() 构造函数，创建了一个 PyAudio 实例，可以用来进
行音频输入和输出操作。

stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)：
这行代码打开了一个音频流 stream，用于从麦克风获取音频数据。
参数解释：
format：指定音频采样位数和编码格式，这里使用了 FORMAT 变量，表示采用之前定义的采样格式。
channels：指定声道数，即音频数据的通道数，这里使用了 CHANNELS 变量，表示采用之前定义的声道数。
rate：指定采样率，即每秒采样点数，这里使用了 RATE 变量，表示采用之前定义的采样率。
input：指定该流是用于输入还是输出。这里设置为 True，表示这个流用于音频输入，即从麦克风获取音频数据。
frames_per_buffer：指定每次读取的音频帧大小，即每次读取的音频数据量。这里使用了 CHUNK 变量，表示每次读取 CHUNK 个音频帧。
这两行代码的作用是初始化并打开了一个音频流，使得后续可以通过这个音频流从麦克风获取音频数据。


            如果限定录制时间的话，解除这个注释
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):   
                data = stream.read(CHUNK)
                frames.append(data)
            print("*" * 10, "录音结束\n")
            



frames = []：
这行代码创建了一个空列表 frames，用于存储从音频流中读取的音频数据。

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
这行代码通过循环来读取多个音频帧，循环次数由 int(RATE / CHUNK * RECORD_SECONDS) 决定。
RATE / CHUNK 表示每秒读取的音频帧数，即音频采样率除以每次读取的音频帧大小。
RECORD_SECONDS 表示需要录制的总时长，通过乘以每秒读取的音频帧数，就可以得到需要读取的音频帧数。

data = stream.read(CHUNK)：
在每次循环中，这行代码调用音频流对象 stream 的 read() 方法，读取指定数量 (CHUNK 个) 的音频数据，并将其存储在 data 变量中。
CHUNK 表示每次读取的音频帧大小，即读取的音频数据量。

frames.append(data)：
这行代码将每次读取的音频数据 data 添加到列表 frames 中，以便后续对录制的音频数据进行处理或保存。
通过这两行代码，程序会不断地从音频流中读取音频数据，并将每次读取的音频数据存储在列表 frames 中，最终得到的 frames 列表就包含了录制的完整
音频数据。


stream.stop_stream()：
这行代码调用音频流对象 stream 的 stop_stream() 方法，用于停止音频流的读取或写入操作。
在录制完成后，调用该方法可以停止从麦克风读取音频数据，以便关闭音频流。

stream.close()：
这行代码调用音频流对象 stream 的 close() 方法，用于关闭音频流。
在停止音频流后，调用该方法可以关闭音频流，释放相关资源。

p.terminate()：
这行代码调用 PyAudio 对象 p 的 terminate() 方法，用于终止 PyAudio 对象。
在完成所有音频操作后，调用该方法可以终止 PyAudio 对象，释放相关资源。
通过这三行代码，程序会停止音频流的操作并关闭音频流，最后终止 PyAudio 对象，以释放相关资源，确保程序正常结束并释放所占用的系统资源。



            使用录制的音频数据进行语音转文字，通常情况下是不需要将音频数据写入到 WAV 文件中的,具体解释详见下面注释
            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            


wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')：
打开一个 WAV 文件，用于写入音频数据。
WAVE_OUTPUT_FILENAME 是之前定义的保存音频文件的文件名。
'wb' 表示以二进制写入模式打开文件。

wf.setnchannels(CHANNELS)：
设置音频文件的声道数。
CHANNELS 是之前定义的声道数，用于指定录制音频的声道数。

wf.setsampwidth(p.get_sample_size(FORMAT))：
设置音频文件的采样位宽。
p.get_sample_size(FORMAT) 获取指定格式 FORMAT 的音频数据的采样位宽。
FORMAT 是之前定义的音频采样格式。

wf.setframerate(RATE)：
设置音频文件的采样率。
RATE 是之前定义的采样率，用于指定录制音频的采样率。

wf.writeframes(b''.join(frames))：
将录制的音频数据写入到 WAV 文件中。
frames 是之前存储录制音频数据的列表，通过 b''.join(frames) 将列表中的音频数据合并成一个字节串，然后将这个字节串写入到 WAV 文件中。

wf.close()：
关闭 WAV 文件，释放相关资源。

将录制的音频数据写入到 WAV 文件中有几个重要的原因：
格式标准化： WAV 是一种通用的音频文件格式，在多个平台和设备上都有良好的兼容性。通过将音频数据保存为 WAV 文件，可以确保其在不同的软件和设备上能够被正常读取和处理。
信息保存： WAV 文件中除了音频数据外，还可以保存一些音频相关的信息，如采样率、声道数、采样位宽等。这些信息对于后续的音频处理和播放是非常重要的。
可编辑性： 将音频数据保存为 WAV 文件后，可以随时对其进行编辑、剪辑和处理。许多音频编辑软件都支持 WAV 格式，因此可以方便地对录制的音频进行后续处理。
方便分享和传输： WAV 文件可以作为一种常见的音频文件格式，方便进行分享和传输。无论是通过网络传输还是在不同设备之间共享，都可以直接使用 WAV 文件进行交换。
因此，将录制的音频数据保存为 WAV 文件能够提供更多的灵活性和便利性，使得音频数据可以被更广泛地应用和使用。


如果想使用录制的音频数据进行语音转文字，通常情况下是不需要将音频数据写入到 WAV 文件中的。语音转文字的 API 通常接受音频数据的输入，你可以
直接将录制的音频数据作为参数传递给语音转文字的 API。
在这种情况下，你只需要确保录制的音频数据满足语音转文字 API 的要求，比如采样率、采样位宽、声道数等参数需要与 API 的要求相匹配。然后，将这些
音频数据传递给语音转文字的 API 接口即可，API 将会对音频数据进行识别并返回相应的文本结果。
因此，不必将录制的音频数据写入到 WAV 文件中，直接使用录制的音频数据即可进行语音转文字的操作。


get_audio(in_path) 是调用了定义的 get_audio() 函数，并传递了参数 in_path。这句代码的作用是执行 get_audio() 函数，启动录音功能。具体地说，它将执行 get_audio() 函数，并将 in_path 作为参数传递给函数。在 get_audio() 函数中，会根据用户的输入来判断是否开始录音，然后进行相应的录音操作
。因此，通过调用 get_audio(in_path)，整个录音过程会被触发和执行。


'''