import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime
from weather import Weather, Unit
weather = Weather(unit=Unit.CELSIUS)
location = weather.lookup_by_latlng(51.5066,-0.4185)
condition = location.condition
import subprocess
from forex_python.converter import CurrencyRates
c = CurrencyRates()
# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

def CurrentTime():
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    now = datetime.now()
    #draw.text((x, top+8),     str(now.strftime('%Y/%m/%d %I:%M:%S')), font=font, fill=255)
    draw.text((x+16, top+16),     str(now.strftime('%I:%M')), font=rateFont, fill=255)
    disp.image(image)
    disp.display()
    time.sleep(.1)

def ForexRate(CurrentForexRate):
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x+15, top+20),    str(CurrentForexRate),  font=rateFont, fill=255)
    disp.image(image)
    disp.display()
    time.sleep(.1)

def Weather(WeatherTemp,WeatherCondition):
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x+80, top+16),     str(WeatherTemp)+'C', font=tempFont, fill=255)
    draw.text((x, top+16),     WeatherCondition, font=condFont, fill=255)
    #if(WeatherCondition=="cloudy"):
        #image = Image.open('Cloudy.ppm').convert('1')
    #elif(WeatherCondition=="sunny"):
        #image = Image.open('Sunny.ppm').convert('1')
    image = Image.open('happycat_oled_64.ppm').convert('1')
    disp.image(image)
    disp.display()
    time.sleep(.1)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()
rateFont=ImageFont.truetype('04B_19__.TTF', 36)
tempFont=ImageFont.truetype('VCR_OSD_MONO_1.001.ttf', 36)
condFont=ImageFont.truetype('VCR_OSD_MONO_1.001.ttf', 16)

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

T=True
S=False
W=False
CurrentForexRate=round(c.get_rate('GBP', 'INR'),2)
WeatherTemp=condition.temp
WeatherCondition=condition.text
start=time.time()
startWeather=time.time()
startForex=time.time()

while True:
    if(time.time()-startWeather>1800.0):
        #weather = Weather(unit=Unit.CELSIUS)
        location = weather.lookup_by_latlng(51.5066,-0.4185)
        condition = location.condition
        WeatherTemp=condition.temp
        WeatherCondition=condition.text
        startWeather=time.time()
    if(time.time()-startForex>21600.0):
        c = CurrencyRates()
        CurrentForexRate=round(c.get_rate('GBP', 'INR'),2)
        startForex=time.time()    
    if((time.time()-start)>2.0):
      if(T==True):
          T=False
          S=True
          W=False
      elif(S==True):
          S=False
          W=True
          T=False
      elif(W==True):
          W=False
          T=True
          S=False
      start=time.time()
    if(T==True):
        CurrentTime()  
    elif(S==True):
        ForexRate(CurrentForexRate)
    elif(W==True):
        Weather(WeatherTemp,WeatherCondition)

