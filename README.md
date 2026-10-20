**English** | [简体中文](README.zh-CN.md)

# Image Processing & Stylized Filters

Originally written in 2023 as my high school programming final project, using Python, NumPy, Pillow, and OpenCV.

## 1. Mirroring
Loops over every pixel and copies one half of the image onto the other half (`mirrorr`, `mirrorHorizontal`).

![Mirror result](images/mirror_result.jpg)

## 2. Edge detection
Compares each pixel with its neighbor using the Euclidean distance between their colors:

`diff = sqrt((B2-B1)^2 + (G2-G1)^2 + (R2-R1)^2)`

If `diff` is above a threshold, the pixel is marked black (edge); otherwise white. I used a threshold of 20 for up–down comparison and 13 for left–right. Comparing left–right neighbors finds vertical edges, and comparing up–down neighbors finds horizontal edges.

| Left–right comparison | Up–down comparison |
| --- | --- |
| ![](images/edge_left_right.jpg) | ![](images/edge_up_down.jpg) |

## 3. Game-inspired filter
While playing the Naruto mobile game, I loved the look of its ultimate-skill cutscenes: dark edges, film grain, and a slight blur. I tried to recreate that style in Python.

| Inspiration | Inspiration |
| --- | --- |
| ![](images/inspiration_1.jpg) | ![](images/inspiration_2.jpg) |

The pipeline:
1. **Color grading**: lowers brightness and saturation, raises contrast, and adjusts each RGB channel
2. **Noise**: adds Gaussian noise with `np.random.normal`. Code I found online kept throwing errors, so I converted both the image and the noise into arrays, added them, and clipped the values to 0–255
3. **Vignette**: uses Pillow's `composite` with a white elliptical mask over a black background; the mask is Gaussian-blurred for a smooth fade
4. **Camera shake**: generates randomly offset frames and exports a GIF (written with ChatGPT's help)

| Before | After |
| --- | --- |
| ![](images/filter_before.jpg) | ![](images/filter_after.jpg) |

With camera shake:

![Shake GIF](images/filter_shake.gif)

*Inspiration screenshots are from the Naruto mobile game (© Masashi Kishimoto / Shueisha and the game's publisher). Demo artwork © HoYoverse (Genshin Impact). All images are used for non-commercial demonstration only.*

## How to run
```bash
pip install numpy pillow opencv-python
python filters.py   # expects a photo named test.jpg in the same folder
```

## Reflection
**What I learned:** I spent a lot of time searching for information, and learned how to install libraries and use many basic Pillow methods and filters.

**What I would improve now:**
- Detect edges in both directions in one pass
- Replace pixel-by-pixel Python loops with vectorized NumPy operations for speed
