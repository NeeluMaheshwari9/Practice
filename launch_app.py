import logging
import subprocess
import os
import time
import datetime
from ppadb.client import Client as AdbClient, Client

client: Client = AdbClient(host="127.0.0.1", port=5037)
phone = client.device("emulator-5554")
package_name = "com.google.android.apps.maps"


def launch_application(pack_name):
    try:
        print(pack_name)
        status = phone.shell("am start {}".format(pack_name))
        time.sleep(10)
        if status:
            print("App Launched")
        else:
            print("App not launched")

        # ret_val = verify(os.path.join(path, 'launch_logs.txt'), "pkg=com.google.android.apps.youtube.music cmp" \
        #                                                         "=com.google.android.apps.youtube.music/.activities.MusicActivity")
        # if ret_val:
        #     print("Youtube-Music application verified by logs Successfully")
        #     logging.info("Youtube-Music application verified by logs Successfully")
        # else:
        #     print("Application launch not successful")
        #     logging.info("Application launch not successful")
    except Exception as ex:
        print("Something went wrong", ex)
        logging.error("Something went wrong", ex)


if __name__ == "__main__":
    launch_application(package_name)
