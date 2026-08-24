import cv2
import mediapipe as mp
import numpy as np
from typing import List, Dict, Any, Tuple
import json

class MovementPatternDetector:
    """Detect unique movement patterns in TikTok videos"""
    
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_hands = mp.solutions.hands
        self.mp_face = mp.solutions.face_mesh
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5)
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.5)
        
    def analyze_video(self, video_path: str) -> Dict[str, Any]:
        """Analyze a video for movement patterns"""
        cap = cv2.VideoCapture(video_path)
        
        movements = []
        poses = []
        hand_gestures = []
        frame_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            if frame_count % 5 != 0:  # Sample every 5th frame
                continue
            
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detect pose
            pose_result = self.pose.process(rgb)
            if pose_result.pose_landmarks:
                landmarks = pose_result.pose_landmarks.landmark
                
                # Extract key body positions
                body_positions = self._extract_body_positions(landmarks)
                poses.append(body_positions)
                
                # Track movement between frames
                if len(poses) > 1:
                    movement = self._calculate_movement(poses[-2], poses[-1])
                    movements.append(movement)
            
            # Detect hand gestures
            hands_result = self.hands.process(rgb)
            if hands_result.multi_hand_landmarks:
                for hand_landmarks in hands_result.multi_hand_landmarks:
                    gesture = self._classify_gesture(hand_landmarks)
                    if gesture != "unknown":
                        hand_gestures.append(gesture)
        
        cap.release()
        
        # Analyze patterns
        pattern = {
            "dominant_movement": self._get_dominant_movement(movements),
            "movement_intensity": self._get_movement_intensity(movements),
            "common_gestures": self._get_common_gestures(hand_gestures),
            "pose_pattern": self._get_pose_pattern(poses),
            "frame_count": frame_count
        }
        
        return pattern
    
    def _extract_body_positions(self, landmarks) -> Dict[str, Tuple[float, float]]:
        """Extract key body landmark positions"""
        key_points = {
            "head": (landmarks[0].x, landmarks[0].y),
            "left_shoulder": (landmarks[11].x, landmarks[11].y),
            "right_shoulder": (landmarks[12].x, landmarks[12].y),
            "left_elbow": (landmarks[13].x, landmarks[13].y),
            "right_elbow": (landmarks[14].x, landmarks[14].y),
            "left_wrist": (landmarks[15].x, landmarks[15].y),
            "right_wrist": (landmarks[16].x, landmarks[16].y),
            "left_hip": (landmarks[23].x, landmarks[23].y),
            "right_hip": (landmarks[24].x, landmarks[24].y),
            "left_knee": (landmarks[25].x, landmarks[25].y),
            "right_knee": (landmarks[26].x, landmarks[26].y),
            "left_ankle": (landmarks[27].x, landmarks[27].y),
            "right_ankle": (landmarks[28].x, landmarks[28].y),
        }
        return key_points
    
    def _calculate_movement(self, prev: Dict, curr: Dict) -> Dict[str, float]:
        """Calculate movement between two frames"""
        movements = {}
        for key in prev:
            dx = curr[key][0] - prev[key][0]
            dy = curr[key][1] - prev[key][1]
            movements[key] = np.sqrt(dx**2 + dy**2)
        return movements
    
    def _get_dominant_movement(self, movements: List[Dict]) -> str:
        """Determine the dominant body part moving"""
        if not movements:
            return "static"
        
        # Sum movements for each body part
        total_movements = {}
        for m in movements:
            for part, value in m.items():
                total_movements[part] = total_movements.get(part, 0) + value
        
        # Find the most active body part
        if not total_movements:
            return "static"
        
        dominant = max(total_movements, key=total_movements.get)
        
        # Classify into movement types
        if "wrist" in dominant or "elbow" in dominant:
            return "arm_movement"
        elif "knee" in dominant or "ankle" in dominant or "hip" in dominant:
            return "dance_movement"
        elif "shoulder" in dominant:
            return "upper_body"
        elif "head" in dominant:
            return "head_movement"
        else:
            return "full_body"
    
    def _get_movement_intensity(self, movements: List[Dict]) -> str:
        """Calculate overall movement intensity"""
        if not movements:
            return "low"
        
        total = sum(sum(m.values()) for m in movements)
        avg = total / len(movements)
        
        if avg < 0.01:
            return "very_low"
        elif avg < 0.03:
            return "low"
        elif avg < 0.06:
            return "medium"
        elif avg < 0.1:
            return "high"
        else:
            return "very_high"
    
    def _classify_gesture(self, hand_landmarks) -> str:
        """Classify hand gesture"""
        landmarks = hand_landmarks.landmark
        
        # Get finger positions
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        
        wrist = landmarks[0]
        
        # Check if fingers are extended
        fingers_extended = []
        
        # Thumb
        fingers_extended.append(thumb_tip.x > landmarks[3].x if thumb_tip.x > wrist.x else thumb_tip.x < landmarks[3].x)
        
        # Other fingers
        for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
            fingers_extended.append(landmarks[tip].y < landmarks[pip].y)
        
        # Classify gesture
        if all(fingers_extended):
            return "open_palm"
        elif not any(fingers_extended):
            return "fist"
        elif fingers_extended[1] and not any(fingers_extended[2:]):
            return "pointing"
        elif fingers_extended[1] and fingers_extended[2] and not any(fingers_extended[3:]):
            return "peace_sign"
        elif fingers_extended[1] and fingers_extended[4]:
            return "rock_on"
        elif fingers_extended[4] and not any(fingers_extended[1:4]):
            return "pinky_up"
        else:
            return "unknown"
    
    def _get_common_gestures(self, gestures: List[str]) -> List[str]:
        """Get most common gestures"""
        from collections import Counter
        if not gestures:
            return []
        counter = Counter(gestures)
        return [g for g, count in counter.most_common(3) if count > 2]
    
    def _get_pose_pattern(self, poses: List[Dict]) -> str:
        """Identify common pose patterns"""
        if not poses:
            return "unknown"
        
        # Check for dance-like patterns
        if len(poses) > 10:
            hip_movement = self._calculate_hip_movement(poses)
            arm_movement = self._calculate_arm_movement(poses)
            
            if hip_movement > 0.05 and arm_movement > 0.05:
                return "dance"
            elif arm_movement > 0.05:
                return "gesturing"
            elif hip_movement > 0.05:
                return "swaying"
        
        return "standing"
    
    def _calculate_hip_movement(self, poses: List[Dict]) -> float:
        """Calculate average hip movement"""
        total = 0
        for i in range(1, len(poses)):
            prev = poses[i-1]
            curr = poses[i]
            dx = curr["left_hip"][0] - prev["left_hip"][0]
            dy = curr["left_hip"][1] - prev["left_hip"][1]
            total += np.sqrt(dx**2 + dy**2)
        return total / max(len(poses) - 1, 1)
    
    def _calculate_arm_movement(self, poses: List[Dict]) -> float:
        """Calculate average arm movement"""
        total = 0
        for i in range(1, len(poses)):
            prev = poses[i-1]
            curr = poses[i]
            for arm in ["left_wrist", "right_wrist"]:
                dx = curr[arm][0] - prev[arm][0]
                dy = curr[arm][1] - prev[arm][1]
                total += np.sqrt(dx**2 + dy**2)
        return total / max(len(poses) - 1, 1)

class TrendPatternAggregator:
    """Aggregate movement patterns across multiple videos to find trends"""
    
    def __init__(self):
        self.detector = MovementPatternDetector()
        self.patterns = []
    
    def analyze_videos(self, video_paths: List[str]) -> Dict[str, Any]:
        """Analyze multiple videos and find common patterns"""
        all_patterns = []
        
        for path in video_paths:
            try:
                pattern = self.detector.analyze_video(path)
                all_patterns.append(pattern)
            except Exception as e:
                print(f"Error analyzing {path}: {e}")
        
        if not all_patterns:
            return {"error": "No videos analyzed"}
        
        # Aggregate results
        movements = [p["dominant_movement"] for p in all_patterns]
        gestures = []
        for p in all_patterns:
            gestures.extend(p.get("common_gestures", []))
        
        from collections import Counter
        
        return {
            "total_videos": len(all_patterns),
            "dominant_movement": Counter(movements).most_common(1)[0][0] if movements else "unknown",
            "movement_distribution": dict(Counter(movements)),
            "common_gestures": Counter(gestures).most_common(5),
            "intensity_levels": [p.get("movement_intensity", "low") for p in all_patterns],
            "pose_patterns": [p.get("pose_pattern", "unknown") for p in all_patterns]
        }

if __name__ == "__main__":
    print("Movement Pattern Detection System Ready!")
    print("=" * 50)
    print("This system can detect:")
    print("  - Dance movements")
    print("  - Hand gestures")
    print("  - Body language patterns")
    print("  - Movement intensity")
    print("  - Unique pose patterns")
    print()
    print("To use: Provide video files to analyze")
