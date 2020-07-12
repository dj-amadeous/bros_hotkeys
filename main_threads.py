import threading
import inspect
import ctypes
from pynput.keyboard import Key, Listener
import pyautogui as pag


def handle_click_by_xy(x_coord, y_coord):
    try:
        pag.click(x_coord, y_coord)
    except Exception as e:
        print(e)


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
        self.coord_list_left = [(54, 61), (163, 61), (271, 63), (379, 63)]
        self.coord_list_right = [(499, 63), (605, 63), (712, 63), (818, 63)]
        self.left_table_actions = []
        self.right_table_fold = (516, 772)
        self.right_table_check_call = (660, 770)
        self.right_table_bet = (809, 767)
        self.right_table_pot = (715, 765)
        self.right_table_66_pot = (604, 765)
        self.right_table_half_pot = (500, 770)
        self.right_table_add_table = (480, 113)
        self.left_table_fold = (76, 770)
        self.left_table_bet = (375, 770)
        self.left_table_check_call = (216, 771)
        self.left_table_pot = (260, 768)
        self.left_table_66_pot = (162, 771)
        self.left_table_half_pot = (57, 771)
        self.left_table_add_table = (41, 118)
        self.left_table = None

    def on_press(self, key):
        pass

    def on_release(self, key):
        try:
            if key == Key.space:
                if self.left_table:
                    handle_click_by_xy(self.left_table_bet[0], self.left_table_bet[1])
                else:
                    handle_click_by_xy(self.right_table_bet[0], self.right_table_bet[1])
            elif key.char == 'q':
                handle_click_by_xy(self.coord_list_right[0][0], self.coord_list_right[0][1])
                self.left_table = False
            elif key.char == 'w':
                handle_click_by_xy(self.coord_list_right[1][0], self.coord_list_right[1][1])
                self.left_table = False
            elif key.char == 'e':
                handle_click_by_xy(self.coord_list_right[2][0], self.coord_list_right[2][1])
                self.left_table = False
            elif key.char == 'r':
                handle_click_by_xy(self.coord_list_right[3][0], self.coord_list_right[3][1])
                self.left_table = False
            elif key.char == '1':
                handle_click_by_xy(self.coord_list_left[0][0], self.coord_list_left[0][1])
                self.left_table = True
            elif key.char == '2':
                handle_click_by_xy(self.coord_list_left[1][0], self.coord_list_left[1][1])
                self.left_table = True
            elif key.char == '3':
                handle_click_by_xy(self.coord_list_left[2][0], self.coord_list_left[2][1])
                self.left_table = True
            elif key.char == '4':
                handle_click_by_xy(self.coord_list_left[3][0], self.coord_list_left[3][1])
                self.left_table = True

            elif key.char == '5':
                if self.left_table:
                    handle_click_by_xy(self.left_table_half_pot[0], self.left_table_half_pot[1])
                else:
                    handle_click_by_xy(self.right_table_half_pot[0], self.right_table_half_pot[1])
            elif key.char == 't':
                if self.left_table:
                    handle_click_by_xy(self.left_table_66_pot[0], self.left_table_66_pot[1])
                else:
                    handle_click_by_xy(self.right_table_66_pot[0], self.right_table_66_pot[1])
            elif key.char == 'g':
                if self.left_table:
                    handle_click_by_xy(self.left_table_pot[0], self.left_table_pot[1])
                else:
                    handle_click_by_xy(self.right_table_pot[0], self.right_table_pot[1])
            elif key.char == 'd':
                if self.left_table:
                    handle_click_by_xy(self.left_table_check_call[0], self.left_table_check_call[1])
                else:
                    handle_click_by_xy(self.right_table_check_call[0], self.right_table_check_call[1])
            elif key.char == 'f':
                if self.left_table:
                    handle_click_by_xy(self.left_table_fold[0], self.left_table_fold[1])
                else:
                    handle_click_by_xy(self.right_table_fold[0], self.right_table_fold[1])
            elif key.char == 'p':
                self.event.set()
                return False
        except Exception as e:
            print(e)

    def key_listener(self):
        with Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()