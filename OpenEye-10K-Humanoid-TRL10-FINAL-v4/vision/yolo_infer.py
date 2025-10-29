
# YOLO ONNX inference hook (stub fallback)
# To enable real inference, install onnxruntime & opencv-python, then set YOLO_ONNX.
YOLO_ONNX = "models/yolov8n.onnx"  # put your model here

def detect_objects(image_bgr):
    # Fallback stub: one fake 'person'
    return [{"bbox":[100,100,120,120],"conf":0.9,"cls":"person"}]
