# Qidian Novel OCR
## Introduction
起点小说OCR，**仅学习使用**！

~~VIP章节经测试也可以，方案的缺点是需要有一个人进行订阅~~

**实现思路**: 
1. Windows下安装Android Studio，运行一个Android Emulator，安装好起点小说App
2. 截图，实现了两种方法
   - Windows OS下，Android Emulator窗口截图，理论上不可能被起点屏蔽
   - 调用adb命令截图，不确定是否会被起点屏蔽
3. OCR 识别截图文字内容 (Tesseract)
4. adb 模拟点击翻页

## Environment

### Android Studio

这部分不赘述了，总之就是装一个安卓虚拟机，然后下载好起点App

### 安装 Python 环境

提供了 conda 的环境：`environment.yml`

### 安装 Tesseract
**(注意：不再需要此工具，百度飞桨对中文识别的效果更好！)**

1. 从 [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) 下载并安装 Tesseract。
  安装完成后，记住安装路径（如：“D:\Program Files\Tesseract-OCR”）
  顺便下载中文训练数据：
  <img src="https://res.cloudinary.com/sycamore/image/upload/v1734276486/Typera/2024/12/cdfed6c26bb76075c0121590ef15cee2.png" alt="image-20241216022802538" style="zoom:75%;" />
2. 如果没有下载中文训练数据，还可以从 [Tesseract tessdata GitHub](https://github.com/tesseract-ocr/tessdata) 获得，chi_sim.traineddata（简体中文）或 chi_tra.traineddata（繁体中文）。
    将 `.traineddata` 文件放在 Tesseract 的 `tessdata` 目录中。

## Usage

直接运行`main.py`就可以，

但需要手动设置需要截图的页数，

如果出现问题，需要调试一下翻页 tap 的位置、翻页后等待的时长等参数
