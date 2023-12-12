"""
Analytics Class
This file contains all the classes and functionalities for the analytics used to determine if to start or stop
@author: ooemperor
"""

from PausePlay import play_pause
import numpy as np
import time


class Analytics:
    """
    Analytics to store and analyze the data from the MediaPipe
    """

    def __init__(self):
        """
        Constructor of the Analytics class
        """

        # creating the empty data.
        self.eye_data = np.array([])
        self.head_data = np.array([])
        self.hand_data = np.array([])

        # Time stamps to prevent multiple triggers in a short time
        self.last_hand_event = time.time()  # time stamp since the last detectino event.
        self.last_head_down_event = time.time()
        self.last_head_up_event = time.time()

        # Configuration Parameters
        self.DEBUG = True  # True if debug message shall be printed.
        self.HAND_LIMIT = 5  # amount of seconds to wait between events from the hand.
        self.HEAD_LIMIT = 2  # amount of seconds to wait between event from the head

    def push_data_head(self, h1: float, h2: float):
        """
        Push the data for the head into the analyzer class
        @param h1: The height from the left shoulder to the chin
        @param h2: The height from the right shoulder to the chin
        @return: No return value
        """

        self.head_data = np.append(self.head_data, h1)
        self.head_data = np.append(self.head_data, h2)

        # limiting the amount of data in the array so it wont get unresponsive over time because of too much data
        if len(self.head_data) > 100:
            self.head_data = np.delete(self.head_data, 0)
            self.head_data = np.delete(self.head_data, 0)

        med = np.median(self.head_data)
        avg = np.average(self.head_data)
        std = np.std(self.head_data)

        upper_limit = med + 3 * std
        lower_limit = med - 3 * std

        if np.average([h1, h2]) > upper_limit:
            if self.DEBUG: print("Head UP Detected")

            # IF statement to determine if play pause must be triggered or not
            if time.time() - self.last_head_up_event > self.HAND_LIMIT:

                if self.DEBUG: print("Head UP Triggered")

                self.last_head_up_event = time.time()
                # emptying head_data array so if a new movement after short time is detected it will get triggered
                self.head_data = np.array([])
                play_pause()
            else:
                # limit of seconds has not passed, do nothing
                pass

        elif np.average([h1, h2]) < lower_limit:
            if self.DEBUG: print("Head DOWN Detected")

            # IF statement to determine if play pause must be triggered or not
            if time.time() - self.last_head_down_event > self.HAND_LIMIT:

                if self.DEBUG: print("Head DOWN Triggered")

                self.last_head_down_event = time.time()
                # emptying head_data array so if a new movement after short time is detected it will get triggered
                self.head_data = np.array([])
                play_pause()
            else:
                # limit of seconds has not passed, do nothing
                pass

    def push_data_eye(self):
        """
        Push the data for the eye
        @return:
        """
        raise NotImplementedError

    def push_data_hand(self, left_hand_data, right_hand_data):
        """
        Push the data for the hand.
        @return:
        """
        if left_hand_data is not None or right_hand_data is not None:
            if self.DEBUG: print("Hand Detected")
            if time.time() - self.last_hand_event > self.HAND_LIMIT:
                if self.DEBUG: print("Hand Triggered")
                self.last_hand_event = time.time()
                play_pause()
            else:
                # not 5 seconds have passed, do nothing
                pass
        elif left_hand_data is None and right_hand_data is None:
            self.last_hand_event = time.time() - self.HAND_LIMIT

    @staticmethod
    def trigger_play_pause(self):
        play_pause()
        return True
