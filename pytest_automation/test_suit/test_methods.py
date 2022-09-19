import logging
import subprocess
import os
import time
import datetime
from ppadb.client import Client as AdbClient, Client

client: Client = AdbClient(host="127.0.0.1", port=5037)
phone = client.device("emulator-5554")

path = os.path.join('pytest_automation/logs', datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'), )
os.makedirs(path, exist_ok=True)

logger = os.path.join('pytest_automation/logs', datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'), )
os.makedirs(path, exist_ok=True)
logging.basicConfig(filename=(os.path.join(logger, "logfile.log")), format='%(asctime)s %(process)d [%(filename)s:%('
                                                                         'lineno)d] [%(module)s] ' '%(funcName)s  '   '%(levelname)s ' '%(message)s%(name)s',
                    level=logging.DEBUG, datefmt='%m-%d-%Y %I:%M:%S %p')


def start_log():
    print("Logs started")
    logging.info('"Logs started"')
    with open(os.path.join(path, 'launch_logs.txt'), 'w', encoding='utf-8') as f:
        process = subprocess.Popen(["adb", "shell", "logcat -d"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            output = process.stdout.readline()
            if output == b'' and process.poll() is not None:
                break
            if output:
                out = output.decode()
                f.write(out)
        f.close()


def launch_application():
    try:
        phone.shell("am start com.google.android.apps.youtube.music")
        ret_val = verify(os.path.join(path, 'launch_logs.txt'), "pkg=com.google.android.apps.youtube.music cmp" \
                                                                "=com.google.android.apps.youtube.music/.activities.MusicActivity")
        if ret_val:
            print("Youtube-Music application verified by logs Successfully")
            logging.info("Youtube-Music application verified by logs Successfully")
        else:
            print("Application launch not successful")
            logging.info("Application launch not successful")
    except Exception as ex:
        print("Something went wrong", ex)
        logging.error("Something went wrong", ex)


def verify(file_name, text):
    try:
        with open(file_name, 'r', encoding="utf-8") as file:
            for line in file:
                if text in line:
                    return True
            return False
    except Exception as ex:
        print("something went wrong in verification:", ex)
        logging.error("Something went wrong", ex)


def functionalities(argument):
    try:
        phone.shell("input keyevent {}".format(argument))
        time.sleep(10)
    except Exception as e:
        print("something went wrong", e)
        logging.error("Something went wrong", e)
    return phone, client


def teardown():
    try:
        phone.shell("am force-stop com.google.android.apps.youtube.music")
        time.sleep(5)
    except Exception as e:
        print("something went wrong", e)
        logging.error("something went wrong", e)

    return phone, client


def stop_logs():
    try:
        status = phone.shell("killall -2 logcat")
        if status:
            return True
        else:
            return False
    except Exception as e:
        print("Logs are Not Stopped", e)
        logging.error("something went wrong", e)
