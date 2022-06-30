import cv2
import board
import digitalio
from PIL import Image, ImageDraw
import ssd1306 as adafruit_ssd1306
from picamera2 import Picamera2
import numpy as np

WIDTH = 128
HEIGHT = 64

i2c = board.I2C()
oled_reset = digitalio.DigitalInOut(board.D4)
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3c, reset=oled_reset)

image = Image.new('1', (oled.width, oled.height))
draw = ImageDraw.Draw(image)
frameCounter = 0
frameSkip = 1
lowerThresh = 0

picamera2 = Picamera2()
picamera2.configure(picamera2.preview_configuration(main={"size": (WIDTH, HEIGHT)}))

picamera2.start()

while True:
    request = picamera2.capture_request()
    image = request.make_array("main")
    retval, buf = cv2.imencode('.webp', image)
    webp = cv2.imdecode(buf, 1)
    gray = cv2.cvtColor(webp, cv2.COLOR_BGR2GRAY)
    thresh, bw = cv2.threshold(gray, lowerThresh, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)    
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    screenframe = Image.fromarray(bw).convert("1")
    request.release()
    oled.image(screenframe)
    oled.show()
    print(screenframe)
