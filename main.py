import sys
import threading
import queue
import time
from urllib.parse import urlparse
from core import mainUI
from queue import Queue
from scripts import watcher, webdriver,globalVar
from config.helper import config

if __name__ == '__main__':
    # if len(sys.argv) == 1 or not urlparse(sys.argv[1]).scheme:
    #     print('Invalid url provided, please check...')
    #     sys.exit(1)
    globalVar._init()
    globalVar.set_value("url","")
    globalVar.set_value("linkFlag",False)
    globalVar.set_value("index", 0)
    globalVar.set_value("queue",Queue(maxsize=0))

    m = threading.Thread(target=mainUI.init,)
    m.start()

    while not globalVar.get_value("linkFlag") :
        time.sleep(0.2)

    t = threading.Thread(target=webdriver.go, args=(globalVar.get_value("url"),))
    t.start()

    w = watcher.Watcher(directory=config()['watchdog']['dir'])
    w.run()
    
