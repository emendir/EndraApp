import os
from oqs import oqs
import ctypes
import platform
from ctypes import c_void_p, cast


def get_library_path(lib: ctypes.CDLL) -> str:
    """
    Return the absolute filesystem path of a loaded ctypes.CDLL library.
    Works on Linux, macOS, and Windows.
    """

    system = platform.system()

    # ---------------------------
    #        Windows
    # ---------------------------
    if system == "Windows":
        from ctypes import wintypes

        GetModuleFileName = ctypes.windll.kernel32.GetModuleFileNameW
        GetModuleFileName.argtypes = [wintypes.HMODULE, wintypes.LPWSTR, wintypes.DWORD]
        GetModuleFileName.restype = wintypes.DWORD

        handle = lib._handle  # HMODULE
        buf = ctypes.create_unicode_buffer(32768)  # large max path support
        GetModuleFileName(handle, buf, len(buf))
        return buf.value

    # ---------------------------
    #   Linux / BSD / macOS
    # ---------------------------
    else:

        class Dl_info(ctypes.Structure):
            _fields_ = [
                ("dli_fname", ctypes.c_char_p),
                ("dli_fbase", ctypes.c_void_p),
                ("dli_sname", ctypes.c_char_p),
                ("dli_saddr", ctypes.c_void_p),
            ]

        # macOS: dladdr in libSystem
        # Linux/BSD: dladdr in libc
        libc_path = "libSystem.B.dylib" if system == "Darwin" else "libc.so.6"
        libc = ctypes.CDLL(libc_path)

        dladdr = libc.dladdr
        dladdr.argtypes = [c_void_p, ctypes.POINTER(Dl_info)]
        dladdr.restype = ctypes.c_int

        info = Dl_info()

        # Use the address of *any* symbol inside the library
        # OQS_init always exists
        symbol = lib.OQS_init
        dladdr(cast(symbol, c_void_p), ctypes.byref(info))

        return info.dli_fname.decode()


def get_oqs_lib_path():
    liboqs_path = get_library_path(oqs.native())
    assert os.path.exists(liboqs_path)
    assert os.path.isabs(liboqs_path)
    return liboqs_path
