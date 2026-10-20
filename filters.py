"""Image processing final project (high school, 2023).

Task 1: image mirroring
Task 2: edge detection
Task 3: a game-inspired stylized filter (noise + vignette + color grading + shake GIF)
"""
import math

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw


# ---------- Task 1: mirroring (OpenCV image arrays) ----------

def mirrorr(img):
    """Mirror the right half of the image onto the left half."""
    img_width = img.shape[1]   # image width
    img_height = img.shape[0]  # image height
    for row in range(img_height):
        for col in range(img_width // 2):
            img[row, col] = img[row, img_width - 1 - col]
    return img


def mirrorHorizontal(img):
    """Mirror the top half of the image onto the bottom half."""
    img_width = img.shape[1]
    img_height = img.shape[0]
    for row in range(img_height // 2):
        for col in range(img_width):
            upPixel = img[row, col]
            img[img_height - 1 - row, col] = upPixel
    return img


# ---------- Task 2: edge detection ----------

def colorDiff(p1, p2):
    """Euclidean distance between two BGR colors."""
    b1, g1, r1 = (int(v) for v in p1)
    b2, g2, r2 = (int(v) for v in p2)
    return math.sqrt((b2 - b1) ** 2 + (g2 - g1) ** 2 + (r2 - r1) ** 2)


def edgeupdown(img, dist):
    """Compare each pixel with the one below it; mark large differences black."""
    img_width = img.shape[1]
    img_height = img.shape[0]
    for i in range(img_height - 1):
        for j in range(img_width):
            currentPixel = img[i, j]
            nextPixel = img[i + 1, j]
            diff = colorDiff(currentPixel, nextPixel)
            if diff > dist:            # edge found
                img[i, j] = [0, 0, 0]
            else:                      # no edge
                img[i, j] = [255, 255, 255]
    return img


# ---------- Task 3: stylized filter (Pillow images) ----------

def noise(image):
    """Add Gaussian noise."""
    a = image.height
    b = image.width
    c = (a + b) / 60
    noise = np.random.normal(0, c, (a, b, 3))
    noisy = np.array(image, dtype=np.int64)
    noisy = noisy + noise
    noisy = np.clip(noisy, 0, 255)
    noisy = Image.fromarray(np.uint8(noisy))
    return noisy


def vignette(image):
    """Darken the edges using a blurred elliptical mask."""
    x, y = image.size
    mask = Image.new('L', (x, y))
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, x, y), 255)
    mask = mask.filter(ImageFilter.GaussianBlur((x + y) / 6))
    result = Image.composite(image, Image.new('RGB', image.size), mask)
    return result


def shake(image, num_frames=10, max_offset=5):
    """Create camera-shake frames (this function was written with ChatGPT's help)."""
    frames = []
    for _ in range(num_frames):
        offset_x = np.random.randint(-max_offset, max_offset)
        offset_y = np.random.randint(-max_offset, max_offset)
        frame = image.copy().convert("RGBA")
        shake_frame = Image.new("RGBA", frame.size)
        shake_frame.paste(frame, (offset_x, offset_y))
        frames.append(shake_frame.convert("RGB"))
    return frames


def huoying(image):
    """Full filter pipeline; saves shaking.gif and returns the still image."""
    img = Image.open(image).convert("RGB")
    img = ImageEnhance.Brightness(img).enhance(0.4)
    img = ImageEnhance.Color(img).enhance(0.4)
    img = ImageEnhance.Contrast(img).enhance(3.0)
    r, g, b = img.split()
    b = b.point(lambda i: i * 0.8)
    g = g.point(lambda i: i * 1.15)
    r = r.point(lambda i: i * 1.4)
    img = Image.merge('RGB', (r, g, b))
    img = noise(img)
    img = vignette(img)
    img = img.filter(ImageFilter.GaussianBlur(1.5))
    frames = shake(img)
    frames[0].save('shaking.gif', save_all=True, append_images=frames[1:],
                   optimize=False, duration=40, loop=0)
    return img


if __name__ == "__main__":
    # Put your own photo next to this file and rename it test.jpg
    cv2.imwrite("mirror.jpg", mirrorr(cv2.imread("test.jpg")))
    cv2.imwrite("edges.jpg", edgeupdown(cv2.imread("test.jpg"), 20))
    huoying("test.jpg").save("filtered.jpg")
    print("Saved mirror.jpg, edges.jpg, filtered.jpg, shaking.gif")
