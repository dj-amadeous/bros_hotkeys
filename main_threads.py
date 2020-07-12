import threading
import inspect
import ctypes
from pynput.keyboard import Key, Listener


def _async_raise(tid, exctype):
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")


class CustomThread(threading.Thread):
    def _get_my_tid(self):
        if not self.is_alive():
            raise threading.ThreadError("Thread is not active")

        if hasattr(self, "_thread_id"):
            return self._thread_id

        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid

        raise AssertionError("Could not determine the thread's id")

    def raise_exc(self, exctype):
        _async_raise(self._get_my_tid(), exctype)

    def terminate(self):
        self.raise_exc(SystemExit)


class ThreadKiller:
    def __init__(self, thread_to_kill, event):
        self.thread_to_kill = thread_to_kill
        self.event = event

    def on_press(self, key):
        pass

    def on_release(self, key):
        try:
            if key.char == 'p':
                self.thread_to_kill.terminate()
                self.event.set()
                return False
        except Exception as e:
            print(e)

    def key_listener(self):
        with Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()


class HotkeyListener:
    def __init__(self, event):
        self.event = event

    def on_press(self, key):
        pass

    def on_release(self, key):
        try:
            if key.char == 'q':
                print("q was pressed")
                # click mouse q
            elif key.char == 'w':
                print("w was pressed")
                # click mouse w
            elif key.char == 'e':
                print("e was pressed")
                # click mouse e
            elif key.char == 'r':
                print("r was pressed")
                # click mouse r
            elif key.char == 'p':
                self.event.set()
        except Exception as e:
            print(e)

    def key_listener(self):
        with Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()