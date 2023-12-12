"""
Basic Media Control Collection that can be triggered by the HCI
@author: ooemperor
"""
import win32api
import platform
import subprocess


def play_pause():
    """
    Playing/Pausing Media Playing on the host system.
    @return: Nothing to return
    @rtype: None
    """
    if platform.system() == "Windows":
        # Windows tested on Python 3.9, 3.10 and 3.11
        VK_MEDIA_PLAY_PAUSE = 0xB3

        hwcode = win32api.MapVirtualKey(VK_MEDIA_PLAY_PAUSE, 0)
        win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, hwcode)

    elif platform.system() == "Linux":
        # this case has not been tested
        subprocess.call(("playerctl", "play-pause"))


if __name__ == '__main__':
    play_pause()
