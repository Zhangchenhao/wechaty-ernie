# coding=utf-8

######  欢迎使用脚本任务，首先让我们熟悉脚本任务的一些使用规则  ######
# 脚本任务支持两种运行方式 

# 1.shell 脚本. 在 run.sh 中编写项目运行时所需的命令，并在启动命令框中填写 bash run.sh <参数1> <参数2>使脚本任务正常运行.

# 2.python 指令. 在 run.py 编写运行所需的代码，并在启动命令框中填写 python run.py <参数1> <参数2> 使脚本任务正常运行.

#注：run.sh、run.py 可使用自己的文件替代。

###数据集文件目录
# datasets_prefix = '/root/paddlejob/workspace/train_data/datasets/'

# 数据集文件具体路径请在编辑项目状态下通过左侧导航「数据集」中文件路径拷贝按钮获取
# train_datasets =  '通过路径拷贝获取真实数据集文件路径 '

# 输出文件目录. 任务完成后平台会自动把该目录所有文件压缩为tar.gz包，用户可以通过「下载输出」可以将输出信息下载到本地.
# output_dir = "/root/paddlejob/workspace/output"

# 日志记录. 任务会自动记录环境初始化日志、任务执行日志、错误日志、执行脚本中所有标准输出和标准出错流(例如print()),用户可以在「提交」任务后,通过「查看日志」追踪日志信息.
# coding=utf-8

######  欢迎使用脚本任务，首先让我们熟悉脚本任务的一些使用规则  ######
# 脚本任务支持两种运行方式 

# 1.shell 脚本. 在 run.sh 中编写项目运行时所需的命令，并在启动命令框中填写 bash run.sh <参数1> <参数2>使脚本任务正常运行.

# 2.python 指令. 在 run.py 编写运行所需的代码，并在启动命令框中填写 python run.py <参数1> <参数2> 使脚本任务正常运行.

#注：run.sh、run.py 可使用自己的文件替代。

###数据集文件目录
# datasets_prefix = '/root/paddlejob/workspace/train_data/datasets/'

# 数据集文件具体路径请在编辑项目状态下通过左侧导航「数据集」中文件路径拷贝按钮获取
# train_datasets =  '通过路径拷贝获取真实数据集文件路径 '

# 输出文件目录. 任务完成后平台会自动把该目录所有文件压缩为tar.gz包，用户可以通过「下载输出」可以将输出信息下载到本地.
# output_dir = "/root/paddlejob/workspace/output"

# 日志记录. 任务会自动记录环境初始化日志、任务执行日志、错误日志、执行脚本中所有标准输出和标准出错流(例如print()),用户可以在「提交」任务后,通过「查看日志」追踪日志信息.
import os
import cv2
import asyncio
import numpy as np
import paddlehub as hub
import zipfile
import paddle
from typing import Optional, Union
from wechaty import Wechaty, Contact
from wechaty.user import Message, Room
from wechaty import (
    Contact,
    FileBox,
    Message,
    Wechaty,
    ScanStatus,
)

# 定义model

dio_model = hub.Module(name='ernie_gen_couplet')




async def on_message(msg: Message):
    from_contact = msg.talker()
    text = msg.text()
    room = msg.room()
        
    if msg.type() == Message.Type.MESSAGE_TYPE_TEXT:
        if msg.talker().contact_id!="@ae6825f39d97ecfba30eedbc2fc5a8efc102ffac3f43870ee5f3f1d15277891f":
            if text == "['']":
              print("空值")
            elif len(text)>2:
                if "小昊bot" in text:
                    print("text:",text)
                    human = [text.replace("@小昊bot","")]
              
                    robot = dio_model.generate(texts=human, beam_width=1)
                    robot = str(robot[0]).replace("[", "").replace("]", "").replace("'", "")
                    conversation:Union[Room, Contact] = from_contact if room is None else room
                    await conversation.ready()
                    await conversation.say(robot)
                else:
                    print("不回复")



    if msg.text() == '图片':
        url = 'http://qrul2d5a1.hn-bkt.clouddn.com/image/street.jpg'
        
        # 构建一个FileBox
        file_box_1 = FileBox.from_url(url=url, name='xx.jpg')

        await msg.say(file_box_1)



async def on_scan(
        qrcode: str,
        status: ScanStatus,
        _data,
):
    print('Status: ' + str(status))
    print('View QR Code Online: https://wechaty.js.org/qrcode/' + qrcode)


async def on_login(user: Contact):
    print(user)


async def main():
    # 确保我们在环境变量中设置了WECHATY_PUPPET_SERVICE_TOKEN
    if 'WECHATY_PUPPET_SERVICE_TOKEN' not in os.environ:
        print('''
            Error: WECHATY_PUPPET_SERVICE_TOKEN is not found in the environment variables
            You need a TOKEN to run the Python Wechaty. Please goto our README for details
            https://github.com/wechaty/python-wechaty-getting-started/#wechaty_puppet_service_token
        ''')

    bot = Wechaty()

    bot.on('scan',      on_scan)
    bot.on('login',     on_login)
    bot.on('message',   on_message)

    await bot.start()

    print('[Python Wechaty] Ding Dong Bot started.')


asyncio.run(main())