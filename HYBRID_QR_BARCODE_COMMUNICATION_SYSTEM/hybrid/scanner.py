# hybrid/scanner.py
"""
Scanner with lazy import of pyzbar so GUI can run even if native zbar is missing.
If zbar is not installed, calling scan functions raises a RuntimeError with instructions.
"""
from typing import List, Dict
from PIL import Image
import cv2
import numpy as np

def _ensure_pyzbar():
    try:
        from pyzbar.pyzbar import decode  # type: ignore
        return decode
    except Exception as e:
        # Friendly runtime error describing how to fix native dependency
        raise RuntimeError(
            "pyzbar/zbar native library not available. "
            "Install ZBar (native) before using scanning features. "
            "On Windows, install via Chocolatey: 'choco install zbar' or use Conda: "
            "'conda install -c conda-forge pyzbar zbar'.\n\n"
            f"Original error: {e}"
        )

def scan_image(path: str) -> List[Dict]:
    decode = _ensure_pyzbar()
    img = Image.open(path).convert("RGB")
    decoded = decode(img)
    results = []
    for d in decoded:
        results.append({
            "type": d.type,
            "data": d.data.decode("utf-8", errors="ignore"),
            "rect": (d.rect.left, d.rect.top, d.rect.width, d.rect.height)
        })
    return results

def scan_cv_frame(frame: np.ndarray) -> List[Dict]:
    decode = _ensure_pyzbar()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    decoded = decode(gray)
    results = []
    for d in decoded:
        results.append({
            "type": d.type,
            "data": d.data.decode("utf-8", errors="ignore"),
            "rect": (d.rect.left, d.rect.top, d.rect.width, d.rect.height)
        })
    return results

def scan_from_webcam(timeout_seconds: int = 15):
    # If zbar missing this will raise the RuntimeError from _ensure_pyzbar()
    cap = cv2.VideoCapture(0)
    import time
    start = time.time()
    found = []
    print("Opening webcam... Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        try:
            results = scan_cv_frame(frame)
        except RuntimeError as e:
            cap.release()
            raise
        if results:
            found.extend(results)
            for r in results:
                x,y,w,h = r["rect"]
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
                cv2.putText(frame, r["data"], (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0),2)
        cv2.imshow("Scan (press q to exit)", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if time.time() - start > timeout_seconds:
            break
    cap.release()
    cv2.destroyAllWindows()
    unique = { (r["type"], r["data"]) : r for r in found }
    return list(unique.values())
 