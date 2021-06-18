import os
import sys
from pathlib import Path
import cv2

def _add_dll_directory(path: Path):
    from ctypes import c_wchar_p, windll  # type: ignore
    from ctypes.wintypes import DWORD

    AddDllDirectory = windll.kernel32.AddDllDirectory
    AddDllDirectory.restype = DWORD
    AddDllDirectory.argtypes = [c_wchar_p]
    AddDllDirectory(str(path))

def kinect():
    if sys.platform != "win32":
        return
    env_path = os.getenv("KINECT_LIBS", None)
    if env_path:
        candidate = Path(env_path)
        dll = candidate / "k4a.dll"
        if dll.exists():
            _add_dll_directory(candidate)
            return
    # autodetecting
    program_files = Path("C:\\Program Files\\")
    for dir in sorted(program_files.glob("Azure Kinect SDK v*"), reverse=True):
        candidate = dir / "sdk" / "windows-desktop" / "amd64" / "release" / "bin"
        dll = candidate / "k4a.dll"
        if dll.exists():
            _add_dll_directory(candidate)
            return

kinect()

from pyk4a import PyK4A
from example.helpers import colorize

# Load camera with the default config
k4a = PyK4A()
k4a.start()

# Get the next capture (blocking function)
capture = k4a.get_capture()
img_color = capture.color

cv2.imshow("Transformed Depth", colorize(capture.transformed_depth, (None, 5000)))
cv2.imshow("Color", capture.color) # (720, 1280, 4)

# Display with pyplot
from matplotlib import pyplot as plt
plt.imshow(img_color[:, :, 2::-1]) # BGRA to RGB
plt.show()