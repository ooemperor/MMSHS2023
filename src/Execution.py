"""
Media Pipe tutorial for the MMS HS 23 Project
@author:
"""

import mediapipe as mp
import cv2
from Analytics import Analytics


class Execution:
    """
    Execution class which runs the Data Collection
    """

    def __init__(self, head=1, hand=1, eye=0):
        self.analytics = Analytics()
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_holistic = mp.solutions.holistic
        self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)

        self.use_eye = True if eye == 1 else False
        self.use_head = True if head == 1 else False
        self.use_hand = True if hand == 1 else False

    def run(self):
        """
            Tutorial for the mediapip
            @return: No Return Value
            """

        cap = cv2.VideoCapture(0)
        # Initiate holistic model
        with self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

            while cap.isOpened():
                ret, frame = cap.read()

                # Recolor Feed
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Make Detections
                results = holistic.process(image)
                self.process_results(results)
                # print(results.face_landmarks)

                # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks

                # Recolor image back to BGR for rendering
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # 1. Draw face landmarks
                #         mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS,
                self.mp_drawing.draw_landmarks(image, results.face_landmarks, self.mp_holistic.FACEMESH_TESSELATION,
                                          self.mp_drawing.DrawingSpec(color=(80, 110, 10), thickness=1, circle_radius=1),
                                          self.mp_drawing.DrawingSpec(color=(80, 256, 121), thickness=1, circle_radius=1)
                                          )

                # 2. Right hand
                self.mp_drawing.draw_landmarks(image, results.right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS,
                                          self.mp_drawing.DrawingSpec(color=(80, 22, 10), thickness=2, circle_radius=4),
                                          self.mp_drawing.DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2)
                                          )

                # 3. Left Hand
                self.mp_drawing.draw_landmarks(image, results.left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS,
                                          self.mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                          self.mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2)
                                          )

                # 4. Pose Detections
                self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_holistic.POSE_CONNECTIONS,
                                          self.mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                                          self.mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                          )

                cv2.imshow('Raw Webcam Feed', image)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()

    def process_results(self, results):
        """
        Process the results that are received in the Data Collection part below
        """

        mp_holistic = mp.solutions.holistic

        # Hand part
        if self.use_hand:
            right_hand = results.right_hand_landmarks
            left_hand = results.left_hand_landmarks

            self.analytics.push_data_hand(left_hand, right_hand)

        if self.use_head:
            try:
                left_shoulder = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER]
                right_shoulder = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER]
                nose = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE]

                # nose to left shoulder
                h1 = left_shoulder.y - nose.y
                # nose to right shoulder
                h2 = right_shoulder.y - nose.y

                self.analytics.push_data_head(h1, h2)

            except AttributeError as err:
                # one of the parameters above has not been found:
                pass


if __name__ == '__main__':
    Execution(head=1, hand=1, eye=0).run()
