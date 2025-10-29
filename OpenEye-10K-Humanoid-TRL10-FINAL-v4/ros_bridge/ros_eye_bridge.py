
#!/usr/bin/env python3
"""ROS2 bridge (optional).
- In real setup, import rclpy and publish/subscribe to topics.
- Here we simulate a heartbeat file for server to detect LIVE mode.
"""
import argparse, time, os, pathlib, sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["sim","live"], default="sim")
    args = ap.parse_args()
    art = pathlib.Path("artifacts"); art.mkdir(exist_ok=True)
    hb = art/"ros_heartbeat"
    try:
        print(f"[ros_bridge] Starting ({args.mode}) ... Ctrl+C to stop.")
        while True:
            if args.mode=="live":
                hb.write_text(str(time.time()))
            else:
                if hb.exists(): hb.unlink()
            time.sleep(2)
    except KeyboardInterrupt:
        if hb.exists(): hb.unlink()
        print("[ros_bridge] Stopped.")

if __name__ == "__main__":
    main()
