## 环境搭建步骤：
### 1、安装python3.9
```
# 下载地址
https://www.python.org/downloads/release/python-396/

# 安装
安装的时候记得自定义安装：
1、add to path
2、安装位置
等
```

### 2、下载代码
```
# 为了不在windows server上下载git，我直接下载的下面工程的zip包，120M左右
https://github.com/ganyipeng/tr
```

### 3、安装tr
```sh
python setup.py install
```

### 4、安装依赖

```sh
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple fitz
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple PyMuPDF
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple setuptools wheel
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip setuptools wheel
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pillow
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple flask
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple flask-restful
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pdf2docx
```

### 5、验证

```sh
# 验证tr环境：上传file1.pdf并执行下面命令
python pdf2csv.py

# 用来验证http://122.112.251.254:5000/ 上传图片
mkdir upload
python app.py	
```

=============================
### 遇到的问题

* 问题：dll-load-failed-error-when-importing-cv2
* 解决办法：需要重启windows server服务器
```
https://izziswift.com/dll-load-failed-error-when-importing-cv2/

Solution 4:
Recently I have faced the similar issue in Azure Windows Server 2012 r2 . Tried all option with and without Anaconda but none of them helped. After lot of findings I found that mfplat.dll was missing which is related to Window Media Service.

Hence you have to manually install the features so that you can get dll related to window media service.
1.Turn windows features on or off
2.Skip the roles screen and directly go to Feature screen
3.Select “Desktop Experience” under “User Interfaces and Infrastructure”
After this all required dll of media services for opencv would be available.
So if you are planning to run your code in cloud(Window Server) then please dont forget to select Desktop Experience feature.
```

* 上面说的Turn windows features on or off在哪找，参考如下：
```
https://www.tenforums.com/tutorials/7247-turn-windows-features-off-windows-10-a.html

控制面板=》程序和功能=》启用或关闭windows功能=》下一步 下一步 下一步=>
此时到达功能界面=》选择最下方倒数第七个【用户界面和基础结构】=》
桌面体验，执行安装，安装需要花费几分钟，安装之后重启电脑才能生效
```
