Crawling AC milan football club photogallery, using python chrome selenium

# 开始
1. 可以直接下载本目录里/app/pics下的图片。图片由我下载至本地，上传至此网站
2. 可以试着在你的机器里运行docker，一劳永逸，随心下载。参看下面说明部分


# docker说明
1. 安装Docker desktop 下载链接：https://www.docker.com/products/docker-desktop

2. 在C盘或者其他盘新建文件夹，以 `C:\milan`为例。在此文件夹下，新建文件，文件名`docker-compose.yml`，内容如下：
```
version: "3.6"
services:
  mysql:
    container_name: milan
    image: milan-img:latest
    volumes:
      - ./app:/home
    command: bash -c "cd /home && python run.py"
```
或者拷贝[docker-compose.yml](https://github.com/liulirun/ac_milan_pic/blob/main/docker-compose.yml) 到 C:\milan

3. 确保docker运行 -- 在开始菜单，输入cmd, 然后在cmd里输入`docker container ls`,应该无错误。

4. 在cmd里
    - 输入`cd C:\milan`切换到milan文件夹
    - 输入`docker-compose up`, 程序即运行（首次下载需要半小时），直到cmd里出现**下载完成**字样即完成。完成后docker container自动关闭。图片下载至 `C:\milan\app\pics`里。

5. 再次下载只需重复第**4**步
