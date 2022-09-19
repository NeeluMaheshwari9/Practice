"""
This code help us to identify name of the application launched in android device.
here I used adb-pure-python to capture adb device logs, multithreading and file handling
to read, compare(string matching) and write required data on file.
"""


import os
import sys
import codecs
from threading import *
import logging
from time import sleep
import subprocess
import datetime
from ppadb.client import Client as AdbClient
from pynput.keyboard import Listener, Key
import yaml


path = os.path.join('C:/Users/admin/PycharmProjects/Practice/LogParser/logs/',
                    datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'), )
os.makedirs(path, exist_ok=True)


def dump_logcat(connection):
    """ to collect android logs in log.txt
    :param connection:
    :arg: connected adb device
    :returns: write adb logs in yaml parse file
    """
    # with codecs.open(parse_yaml['file'], "w", "utf-8") as streamfile:
    with codecs.open(os.path.join(path, 'log.txt'), "w", "utf-8") as streamfile:
        while True:
            global STOP_THREADS
            if STOP_THREADS:
                break
            try:
                data = connection.read(1024)
                streamfile.write(data.decode('utf-8'))
            except UnicodeDecodeError:
                print('something went wrong')
                logging.info('something went wrong')
                break
        var = connection.close()


class StartLogs(Thread):
    """ to clear android connection older logs and call dump_logcat
    :arg: Thread thread_StartLogs
    :returns: write adb logs by calling dump_logcat
    """
    def run(self):
        print("Logs started")
        logging.info("Logs started")
        device.shell("logcat -c")
        device.shell("logcat", handler=dump_logcat)


class Action(Thread):
    """ read yaml parse file and compare yaml text_match to identify which is application operated
    :arg: Thread t2
    :returns: key when log file and yaml text matching take place
    """
    def run(self):
        print("Start Action")
        logging.info("Start Action")
        try:
            # file = open(parse_yaml['file'], 'r', encoding='utf-8')
            file = open(os.path.join(path, 'log.txt'), 'r', encoding='utf-8')
            pos = 0
            while True:
                file.seek(pos)
                file.readline()

                for text in file:
                    for key, value in parse_yaml['text_match'].items():
                        if value in text:
                            print(key)

                pos = file.tell()
                global STOP_THREADS  # to stop action thread
                if STOP_THREADS:
                    break
        except Exception as logFileError:
            print("log file is not available..")
            print(logFileError)


def clear_logfile():
    """ This function is to clear previous logs from existing yaml parse file
    :arg: NA
    :returns: clear the yaml log file
    """
    if os.path.exists(os.path.join(path, 'log.txt')):
        # file = open(parse_yaml['file'], "r+")
        file = open(os.path.join(path, 'log.txt'), "r+")
        file.seek(0)                                   # absolute file pointer positioning
        file.truncate()                                 # to erase available data of log file
        print("Ready for new logs")
        logging.info("Ready for new logs")


def on_press(key):
    """ to add a keyboard listener to exit with space key
    :arg: key
    :returns: exit program execution
    """
    if key == Key.space:
        print("Space key pressed to exit")
        logging.info("Space key pressed to exit")
        sys.exit(0)


if __name__ == "__main__":
    # accessing yaml for data serialization
    with open('C:/Users/admin/PycharmProjects/Practice/LogParser/config/log_parser.yml', 'r')as yml_f:
        parse_yaml = yaml.safe_load(yml_f)
    # logger configuration - result logs will save in yaml parse logfile
    logging.basicConfig(filename=os.path.join(path, parse_yaml['logfile']), level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(module)s:%(lineno)d:%(message)s')
    # subprocess to check which device connected
    sp1 = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           universal_newlines=True)
    out, err = sp1.communicate()
    print(out)
    logging.info(out)                           # to get list of device connected
    if parse_yaml['device'] not in out:         # to verify yaml device is listed or not ... if not than exit
        print('device not connected')
        logging.info('device not connected')
        sys.exit(1)

    print("device connected")
    logging.info("device connected")
    print("Erasing older Logs ")
    logging.info("Erasing older Logs ")

    clear_logfile()                         # to clear previous logs if already exist

    STOP_THREADS = False                    # used as global variable to control the threads.

    client = AdbClient(host="127.0.0.1", port=5037)     # android device setup from yaml
    device = client.device(parse_yaml['device'])

    thread_StartLogs = StartLogs()                  # threads creation
    thread_Action = Action()

    thread_StartLogs.start()                        # threads start
    sleep(2)
    thread_Action.start()

    with Listener(on_press=on_press) as listener:           # Set-up the listener for key pressed
        listener.join()

    STOP_THREADS = True                         # after space key pressed global variable reassigned to true

    print("Program exit")                       # all threads stopped and exit
    logging.info("Program exit")
