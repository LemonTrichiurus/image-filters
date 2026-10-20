# Image Processing & Stylized Filters · 图像处理与滤镜

Originally written in 2023 as my high school programming final project, using Python, NumPy, Pillow, and OpenCV.

这是我 2023 年高中编程课的期末大作业，使用了 Python、NumPy、Pillow 和 OpenCV。

---

## 1. Mirroring · 图片镜像

Loops over every pixel and copies one half of the image onto the other half (`mirrorr`, `mirrorHorizontal`).

镜像是把图片分成两半，再将一半复制到另一半。从右向左镜像时，把 `img[row, col]` 和 `img[row, img_width-1-col]` 反过来赋值；从上向下镜像时，把宽换成高、列换成行即可。

![Mirror result](images/mirror_result.jpg)

---

## 2. Edge detection · 边缘检测

Compares each pixel with its neighbor using the Euclidean distance between their colors:

`diff = sqrt((B2-B1)^2 + (G2-G1)^2 + (R2-R1)^2)`

If `diff` is above a threshold, the pixel is marked black (edge); otherwise white. Comparing left–right neighbors finds vertical edges, and comparing up–down neighbors finds horizontal edges.

边缘检测是对比相邻的两个像素，用上面的公式计算颜色差异。差异超过阈值就标黑，表示边缘，其余为白色。测试时上下比较取 20，左右比较取 13。左右比较更容易发现竖直边缘，上下比较更容易发现水平边缘。

| Left–right comparison · 左右比较 | Up–down comparison · 上下比较 |
| --- | --- |
| ![](images/edge_left_right.jpg) | ![](images/edge_up_down.jpg) |

---

## 3. Game-inspired filter · 图片滤镜

While playing the Naruto mobile game, I loved the look of its ultimate-skill cutscenes: dark edges, film grain, and a slight blur. I tried to recreate that style in Python.

玩火影忍者手游时，我觉得里面的奥义图特别好看，就想用 Python 做一个类似的效果。它的特点是：越靠边缘越暗（晕影），有噪点，还有一点模糊。

| Inspiration · 灵感 | Inspiration · 灵感 |
| --- | --- |
| ![](images/inspiration_1.jpg) | ![](images/inspiration_2.jpg) |

The pipeline:
1. Lowers brightness and saturation, raises contrast
2. Color-grades each RGB channel
3. Adds Gaussian noise with NumPy
4. Adds a vignette with a blurred elliptical mask
5. Exports a "camera shake" GIF from randomly offset frames (written with ChatGPT's help)

制作过程：
1. **调色**：降低亮度和饱和度、提高对比度，再分别调整 R、G、B 三个通道。
2. **噪点**：用 `np.random.normal` 生成高斯噪声。网上的代码运行时报错，我改成把图片和噪声都转为数组相加，再把像素值限制在 0–255 之间。
3. **晕影**：用 Pillow 的 `composite`，以白色椭圆作为 mask，把原图贴到黑色底板上；mask 再加高斯模糊，让边缘过渡自然。
4. **抖动**：网上没找到做法，这部分让 ChatGPT 帮我写，生成随机偏移的帧并导出 GIF。

| Before · 原图 | After · 效果 |
| --- | --- |
| ![](images/filter_before.jpg) | ![](images/filter_after.jpg) |

With camera shake · 抖动效果：

![Shake GIF](images/filter_shake.gif)

*Inspiration screenshots are from the Naruto mobile game (© Masashi Kishimoto / Shueisha and the game's publisher). Demo artwork © HoYoverse (Genshin Impact). All images are used for non-commercial demonstration only.*

*灵感截图来自火影忍者手游，演示原图来自原神（© HoYoverse），仅用于非商业展示。*

---

## How to run · 运行方法

```bash
pip install numpy pillow opencv-python
python filters.py   # expects a photo named test.jpg in the same folder
                    # 在同一文件夹放一张名为 test.jpg 的图片
```

---

## Reflection · 总结

**What I learned:** I spent a lot of time searching for information, and learned how to install libraries and use many basic Pillow methods and filters.

**What I would improve now:**
- Detect edges in both directions in one pass
- Replace pixel-by-pixel Python loops with vectorized NumPy operations for speed

**收获：** 花了很多时间查资料，学会了安装各种库，以及 Pillow 的一些基本用法和滤镜效果。

**现在会改进的地方：** 一次同时检测两个方向的边缘；用 NumPy 向量化运算代替逐像素循环，提高速度。
