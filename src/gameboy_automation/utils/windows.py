import ctypes
from ctypes import wintypes
from PIL import Image, ImageGrab

user32 = ctypes.WinDLL("user32", use_last_error=True)

class RECT(ctypes.Structure):
    """Windows rectangle coordinates."""

    _fields_ = [
        ("left", wintypes.LONG),
        ("top", wintypes.LONG),
        ("right", wintypes.LONG),
        ("bottom", wintypes.LONG),
    ]

EnumWindowsProc = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    wintypes.LPARAM,
)


user32.EnumWindows.argtypes = [
    EnumWindowsProc,
    wintypes.LPARAM,
]
user32.EnumWindows.restype = wintypes.BOOL

user32.GetWindowThreadProcessId.argtypes = [
    wintypes.HWND,
    ctypes.POINTER(wintypes.DWORD),
]
user32.GetWindowThreadProcessId.restype = wintypes.DWORD

user32.IsWindowVisible.argtypes = [
    wintypes.HWND,
]
user32.IsWindowVisible.restype = wintypes.BOOL

user32.GetWindowTextLengthW.argtypes = [
    wintypes.HWND,
]
user32.GetWindowTextLengthW.restype = ctypes.c_int

user32.GetWindowTextW.argtypes = [
    wintypes.HWND,
    wintypes.LPWSTR,
    ctypes.c_int,
]
user32.GetWindowTextW.restype = ctypes.c_int

user32.GetWindowRect.argtypes = [
    wintypes.HWND,
    ctypes.POINTER(RECT),
]
user32.GetWindowRect.restype = wintypes.BOOL

def get_window_title(window_handle: int) -> str:
    """Return the title of a Windows window."""

    title_length = user32.GetWindowTextLengthW(window_handle)

    if title_length == 0:
        return ""

    title_buffer = ctypes.create_unicode_buffer(title_length + 1)

    user32.GetWindowTextW(
        window_handle,
        title_buffer,
        len(title_buffer),
    )

    return title_buffer.value


def find_window_by_process_id(process_id: int) -> int | None:
    """
    Find a visible top-level window owned by a process.

    Args:
        process_id:
            Windows process ID to search for.

    Returns:
        The native window handle, or None when no matching window exists.
    """

    matching_window: int | None = None

    @EnumWindowsProc
    def enum_window_callback(
        window_handle: int,
        _parameter: int,
    ) -> bool:
        nonlocal matching_window

        window_process_id = wintypes.DWORD()

        user32.GetWindowThreadProcessId(
            window_handle,
            ctypes.byref(window_process_id),
        )

        if window_process_id.value != process_id:
            return True

        if not user32.IsWindowVisible(window_handle):
            return True

        window_title = get_window_title(window_handle)

        if not window_title:
            return True

        matching_window = window_handle

        return False

    user32.EnumWindows(
        enum_window_callback,
        0,
    )

    return matching_window

def get_window_bounds(
    window_handle: int,
) -> tuple[int, int, int, int]:
    """
    Return the screen coordinates of a Windows window.

    Returns:
        A tuple containing:

        left, top, right, bottom

    Raises:
        OSError:
            If Windows cannot retrieve the window coordinates.
    """

    rectangle = RECT()

    success = user32.GetWindowRect(
        window_handle,
        ctypes.byref(rectangle),
    )

    if not success:
        raise ctypes.WinError(ctypes.get_last_error())

    return (
        rectangle.left,
        rectangle.top,
        rectangle.right,
        rectangle.bottom,
    )

def capture_window(
    window_handle: int,
) -> Image.Image:
    """
    Capture a screenshot of a Windows window.

    Args:
        window_handle:
            Native Windows window handle.

    Returns:
        A Pillow image containing the entire window.
    """

    left, top, right, bottom = get_window_bounds(
        window_handle,
    )

    return ImageGrab.grab(
        bbox=(
            left,
            top,
            right,
            bottom,
        )
    )
