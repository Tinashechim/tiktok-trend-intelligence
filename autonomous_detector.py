import cv2
import mediapipe as mp
import numpy as np
from typing import List, Dict, Any, Tuple
from collections import Counter
import json
from datetime import datetime

class AutonomousTrendDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_hands = mp.solutions.hands
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.movement_signatures = {}
        self.gesture_counts = Counter()
        self.pose_patterns = Counter()
    
    def analyze_video_stream(self, video_path):
        cap = cv2.VideoCapture(video_path)
        frame_count = 0
        gesture_history = []
        pose_history = []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1
            if frame_count % 3 != 0:
                continue
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pose_result = self.pose.process(rgb)
            if pose_result.pose_landmarks:
                landmarks = pose_result.pose_landmarks.landmark
                pose_type = self._identify_pose_pattern(landmarks)
                pose_history.append(pose_type)
            hands_result = self.hands.process(rgb)
            if hands_result.multi_hand_landmarks:
                for hand in hands_result.multi_hand_landmarks:
                    gesture = self._identify_gesture(hand)
                    gesture_history.append(gesture)
        cap.release()
        
        dominant_gesture = Counter(gesture_history).most_common(1)
        dominant_pose = Counter(pose_history).most_common(1)
        
        return {
            'dominant_gesture': dominant_gesture[0][0] if dominant_gesture else 'none',
            'dominant_pose': dominant_pose[0][0] if dominant_pose else 'none',
            'frame_count': frame_count
        }
    
    def _identify_gesture(self, hand_landmarks):
        lm = hand_landmarks.landmark
        fingers = {
            'thumb': (lm[4], lm[3]),
            'index': (lm[8], lm[6]),
            'middle': (lm[12], lm[10]),
            'ring': (lm[16], lm[14]),
            'pinky': (lm[20], lm[18])
        }
        extended = {}
        for name, (tip, pip) in fingers.items():
            if name == 'thumb':
                extended[name] = abs(tip.x - lm[2].x) > abs(pip.x - lm[2].x)
            else:
                extended[name] = tip.y < pip.y
        if all(extended.values()):
            return 'open_palm'
        elif not any(extended.values()):
            return 'fist'
        elif extended['index'] and not any([extended['middle'], extended['ring'], extended['pinky']]):
            return 'pointing'
        elif extended['index'] and extended['middle'] and not any([extended['ring'], extended['pinky']]):
            return 'peace_sign'
        elif extended['thumb'] and extended['pinky'] and not any([extended['index'], extended['middle'], extended['ring']]):
            return 'rock_on'
        else:
            return 'other'
    
    def _identify_pose_pattern(self, landmarks):
        hands_up = landmarks[15].y < landmarks[0].y and landmarks[16].y < landmarks[0].y
        hip_y = (landmarks[23].y + landmarks[24].y) / 2
        knee_y = (landmarks[25].y + landmarks[26].y) / 2
        ankle_y = (landmarks[27].y + landmarks[28].y) / 2
        crouching = hip_y > knee_y - 0.1
        jumping = ankle_y < hip_y + 0.1
        if hands_up and jumping:
            return 'jumping_hands_up'
        elif hands_up:
            return 'hands_up'
        elif crouching:
            return 'crouching'
        elif jumping:
            return 'jumping'
        else:
            return 'standing'
    
    def find_emerging_patterns(self, video_analyses):
        gesture_counter = Counter()
        pose_counter = Counter()
        for analysis in video_analyses:
            gesture_counter[analysis.get('dominant_gesture', 'none')] += 1
            pose_counter[analysis.get('dominant_pose', 'none')] += 1
        total = len(video_analyses)
        emerging = []
        for gesture, count in gesture_counter.most_common():
            if count / total > 0.3 and gesture != 'none':
                emerging.append({'type': 'gesture', 'pattern': gesture, 'trend_strength': round(count / total * 100, 2)})
        for pose, count in pose_counter.most_common():
            if count / total > 0.3 and pose != 'none':
                emerging.append({'type': 'movement', 'pattern': pose, 'trend_strength': round(count / total * 100, 2)})
        return {'total_analyzed': total, 'emerging_patterns': emerging}

print('Movement Detector ready!')
print('This system detects: hand gestures, body poses, and emerging movement trends')
