## 环境搭建
* 该文档还需要再修改！！！

### 拉取ubuntu18.0.4镜像
```sh
docker pull ubuntu:18.04
```

### 创建ubuntu18.0.4容器
```sh
docker run -itd --name ubuntu-18-test3 ubuntu
```

### 进入ubuntu18.0.4容器
```sh
docker exec -it 8c5f75c73df1 /bin/bash
```

### 系统环境准备
```sh
apt-get update
apt-get upgrade
apt-get install zlib1g-dev libbz2-dev libssl-dev libncurses5-dev libsqlite3-dev libreadline-dev tk-dev libgdbm-dev libdb-dev libpcap-dev xz-utils libexpat1-dev liblzma-dev libffi-dev libc6-dev
```
    
### 下载并安装Python3.8版本
```sh
apt-get install wget
wget https://cdn.npm.taobao.org/dist/python/3.8.3/Python-3.8.3.tgz
tar -xzf Python-3.8.3.tgz
cd Python-3.8.3
mkdir -p /usr/local/python3.8
./configure --prefix=/usr/local/python3.8
make
make install
ln -s /usr/local/python3.8/bin/python3.8 /usr/bin/python3.8
ln -s /usr/local/python3.8/bin/python3.8-config /usr/bin/python3.8-config
python3.8 -V
python3.8 -m pip -V
```
   
### 使用scp命令将tr工程复制到容器的/gyp目录下
```sh
docker cp /Users/gyp/workspace2021/python/tr 8c5f75c73df1:/gyp
```
   
### 安装tr
```sh
python3.8 setup.py install
```
   
### 将3个非tr的py代码和file1.pdf文件拷到容器的/gyp/tr目录
```sh
docker cp /Users/gyp/workspace2021/java/tr_pic2csv/getVerticalBorder.py 8c5f75c73df1:/gyp/tr
docker cp /Users/gyp/workspace2021/java/tr_pic2csv/pdf2csv.py 8c5f75c73df1:/gyp/tr
docker cp /Users/gyp/workspace2021/java/tr_pic2csv/runtr.py 8c5f75c73df1:/gyp/tr
docker cp /Users/gyp/workspace2021/java/be44629b3330c66874b4e00ac94664d5/file1.pdf 8c5f75c73df1:/gyp/tr
```

### 安装如下依赖
```sh
python3.8 -m pip install fitz
python3.8 -m pip install PyMuPDF
python3.8 -m pip install setuptools wheel
python3.8 -m pip install --upgrade pip setuptools wheel
python3.8 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python
python3.8 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pillow
```
   
### 执行pdf2csv.py
```sh
python3.8 pdf2csv.py
```
   
### 查看执行结果
```sh
ll | grep file1
python3.8 pdf2csv.py
ll | grep file1
ll file1
```

### 执行结果如下

```sh
root@8c5f75c73df1:/gyp/tr# ll file1
total 9708
drwxr-xr-x  2 root root       4096 Aug  6 00:45 ./
drwxr-xr-x 12  502 dialout    4096 Aug  6 00:45 ../
-rw-r--r--  1 root root       1613 Aug  6 00:45 0.csv
-rw-r--r--  1 root root    5037091 Aug  6 00:45 0.png
-rw-r--r--  1 root root       2232 Aug  6 00:45 1.csv
-rw-r--r--  1 root root    4883353 Aug  6 00:45 1.png
root@8c5f75c73df1:/gyp/tr#
```


### 将上面👆的容器打包成新的镜像
```sh
docker commit 8c5f75c73df1 gyp-pdf:v1
sha256:3d5c6773982d2f3c422db0d830df7b92c04525bf84a3a2e5c6bb92237d3106f7
```

### 创建容器并进行端口映射
```sh
docker run -p 2021:5000  -itd --name gyp-pdf-c1 gyp-pdf:v1
```

### 安装依赖
```sh
python3.8 -m pip install flask
python3.8 -m pip install flask-restful
python3.8 -m pip install pdf2docx
```
   
### 将文件上传的代码scp到容器
```sh
docker cp /Users/gyp/PycharmProjects/pdf2json/pdfParser.py aeee637a5cbf:/gyp/tr
docker cp /Users/gyp/PycharmProjects/pdf2json/app.py aeee637a5cbf:/gyp/tr
docker cp /Users/gyp/PycharmProjects/pdf2json/templates aeee637a5cbf:/gyp/tr
```

### 创建upload文件夹
```sh
mkdir upload
```
   
### 修改app.py、gyptest.py
```sh
vim app.py
vim gyptest.py
```
   
### 运行 app.py
```sh
python3.8 app.py
```
