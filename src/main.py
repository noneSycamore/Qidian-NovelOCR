from queue import Queue
import threading
import time

from ScreenShort import *
from FlipSimulate import *
from OCR import *


def prepare(method="adb"):
    """
    initialize AndroidEmulator object, if adb not work, init the window.
    :return: AndroidEmulator object
    """
    android_emulator = AndroidEmulator()
    if method == "window":
        android_emulator.choose_avd_window()
    return android_emulator


def producer(avd, queue, num_pages):
    """
    生产者线程：负责截图和翻页
    :param avd:
    :param queue:
    :param num_pages:
    :return:
    """
    for i in range(num_pages):
        filename = f"screenshot_{i}.png"
        take_screenshot(avd.device, filename, method="adb")
        queue.put(filename)  # 将截图路径放入队列
        flip_page(avd.device)  # 翻页
        time.sleep(0.2)  # 等待翻页完成
    queue.put(None)  # 用 None 表示结束


def consumer(queue):
    """
    消费者线程：负责 OCR 处理
    :param queue:
    :return:
    """
    while True:
        filepath = queue.get()
        if filepath is None:
            queue.task_done()
            break  # 收到结束信号，退出
        image_path = f"../screenshots/{filepath}"
        text = ocr_image_paddle(image_path)
        output_result(text, "../temp.txt")
        queue.task_done()


def main():
    avd = prepare(method="adb")
    num_pages = 8
    queue = Queue()

    # 创建并启动生产者和消费者线程
    producer_thread = threading.Thread(target=producer, args=(avd, queue, num_pages))
    consumer_thread = threading.Thread(target=consumer, args=(queue,))
    producer_thread.start()
    consumer_thread.start()

    # 等待生产者完成
    producer_thread.join()
    # 等待队列清空
    queue.join()
    print("All tasks are done.")


if __name__ == '__main__':
    main()
