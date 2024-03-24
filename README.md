# Robot-Class
建立一个Python的Robot类，来完成摄像头和麦克风的调用。

***1.conda环境配置： 配置了一个叫baidu_recognition的虚拟环境，Python版本为3.8 这个conda环境（记住名字）专门用来做检测的 
pip install baidu-aip 安装Python SDK（官方文件要求）
pip install opencv-python 安装OpenCV 
pip install chardet
pip install pyaudio  音频识别

conda install chardet 还得安一个这个，不然会报错，而且pip还不行，得conda 
降低requests和urllib3版本,不然也会报错 pip uninstall requests urllib3 conda install requests==2.27 urllib3==1.25.8

安装完记得把解释器改成刚刚建立的conda环境

代码注释/解释在Robot_class.py文件中有详细说明，目前功能已跑通！opl此项目完结~