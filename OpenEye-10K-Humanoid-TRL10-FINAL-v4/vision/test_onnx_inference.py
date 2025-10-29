
"""Minimal smoke tests for ONNX hooks (runs stubs if models/runtime absent)."""
try:
    import cv2  # type: ignore
except Exception:
    cv2 = None

from yolo_infer import detect_objects
from midas_depth import infer_depth
from emotion_recog import classify_emotion

def main():
    img = None
    if cv2 is not None:
        img = (255 * __import__('numpy').ones((480,640,3), dtype='uint8'))

    dets = detect_objects(img)
    depth = infer_depth(img)
    emo = classify_emotion(img)
    print({"detections": dets, "depth": depth, "emotion": emo})

if __name__ == "__main__":
    main()
