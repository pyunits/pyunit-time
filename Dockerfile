FROM alpine
MAINTAINER Jytoui <jtyoui@qq.com>

COPY ./ /mnt/pyunit-time

# 加入pip源
ENV pypi https://pypi.douban.com/simple

# 更换APK源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

# 安装Python3环境
RUN apk add --no-cache python3

# 更换pip3
RUN pip3 install --upgrade pip -i ${pypi}

# 安装flask插件
RUN pip3 install flask -i ${pypi}

# 安装项目第三方库
RUN pip3 install --no-cache-dir -r /mnt/pyunit-time/requirements.txt -i ${pypi}
RUN pip3 install /mnt/pyunit-time/whl/uWSGI-2.0.18-cp38-cp38-linux_x86_64.whl

RUN rm -rf /mnt/pyunit-time/whl
CMD [ "sh", "/mnt/pyunit-time/app.sh" ]