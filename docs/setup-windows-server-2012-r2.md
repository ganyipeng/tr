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
