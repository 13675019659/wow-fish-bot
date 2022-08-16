
import io
import sys

from logging import config,getLogger

from log import logsettings

if __name__ == "__main__":
    #系统编码
    #
    print('=='+sys.getdefaultencoding());
    s = "你好，世界！".encode('GBK').decode('GBK');
    print(s);

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
    print("中文乱麻麻");

    config.dictConfig(logsettings.LOGGING_DIC)#在logging模块中加在logsettings.py中定义的字典
    logger1=getLogger('用户账户')#获取到定义的loggers来产生日志
    logger1.info('这是一条日志')#写入的日志内容


    exit();