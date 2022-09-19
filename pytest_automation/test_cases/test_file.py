"""
Automate a android music application using PPADB and PYTest Frame work
"""

import pytest
from pytest_automation.test_suit.test_methods import *


@pytest.fixture
def setup():
    print("Test Execution started")
    start_log()
    time.sleep(3)
    launch_application()
    time.sleep(3)
    yield
    """ Teardown for closing mobile application """
    ret_status = teardown()
    if not ret_status:
        print("Application is not closed")
    else:
        print("Mobile application closed success")
    print("Test execution done.....!!!")


@pytest.mark.Tc_01
def test_launch(setup):
    """ Stop logs"""
    ret_val = stop_logs()
    if not ret_val:
        print("Logs are not stopped")
    else:
        print("logs are stopped")
    time.sleep(3)


@pytest.mark.Tc_02
def test_play(setup):
    """ 126 is key event for play button """
    status = functionalities(126)
    if not status:
        print("not success")
    else:
        print("play the music success")
    """ Stop logs"""
    ret_val = stop_logs()
    if not ret_val:
        print("Logs are not stopped")
    else:
        print("logs are stopped")


@pytest.mark.Tc_03
def test_pause(setup):

    """ Play the Music """
    phone.shell("input keyevent 126")
    time.sleep(10)

    """ 127 is key event for pause button """
    status = functionalities(127)
    if not status:
        print("not success")
    else:
        print("pause the music success")
    """ Stop logs"""
    ret_val = stop_logs()
    if not ret_val:
        print("Logs are not stopped")
    else:
        print("logs are stopped")


@pytest.mark.Tc_04
def test_volume_up(setup):

    """ Play the Music """
    phone.shell("input keyevent 126")
    time.sleep(10)

    """ 24 is key event for Volume-up button """
    status = functionalities(24)
    if not status:
        print("not success")
    else:
        print("Volume-up  success")

    """ Stop logs"""
    ret_val = stop_logs()
    if not ret_val:
        print("Logs are not stopped")
    else:
        print("logs are stopped")


@pytest.mark.Tc_05
def test_mute(setup):

    """ Play the Music """
    phone.shell("input key event 126")
    time.sleep(10)

    """ 164 is key event for Volume-up button """
    status = functionalities(164)
    if not status:
        print("not success")
    else:
        print("Mute success")
    phone.shell("input key event 24")
    time.sleep(2)
    """ Stop logs"""
    ret_val = stop_logs()
    if not ret_val:
        print("Logs are not stopped")
    else:
        print("logs are stopped")


@pytest.mark.Tc_06
def test_prev(setup):

    """ Play the Music """
    phone.shell("input keyevent 126")
    time.sleep(10)

    """ 88 is key event for previous song button """
    status = functionalities(88)
    if not status:
        print("not success")
    else:
        print("Previous button is success")


@pytest.mark.Tc_07
def test_next(setup):

    """ Play the Music """
    phone.shell("input keyevent 126")
    time.sleep(10)

    """ 87 is key event for next button """
    status = functionalities(87)
    if not status:
        print("not success")
    else:
        print("Next keycode success")
    """ Stop logs"""
    ret_val = stop_logs()
    if not ret_val:
        print("Logs are not stopped")
    else:
        print("logs are stopped")
