from machine import Pin, I2C
from time import sleep_ms
import urandom
import neopixel
from I2C_LCD import I2cLcd

# --- NeoPixels ---
np_1 = neopixel.NeoPixel(Pin(46), 25)
np_2 = neopixel.NeoPixel(Pin(3), 25)

# --- Buttons ---
btn_np1 = Pin(12, Pin.IN, Pin.PULL_UP)  # change NeoPixel 1
btn_np2 = Pin(13, Pin.IN, Pin.PULL_UP)   # change NeoPixel 2
btn_mode = Pin(14, Pin.IN, Pin.PULL_UP) # change mode
btn_score1 = Pin(11, Pin.IN, Pin.PULL_UP)
btn_score2 = Pin(10, Pin.IN, Pin.PULL_UP)

# --- LED indicators for button presses ---
led_np1 = Pin(18, Pin.OUT)
led_np2 = Pin(17, Pin.OUT)
led_score1 = Pin(16, Pin.OUT)
led_score2 = Pin(15, Pin.OUT)
led_mode = Pin(8, Pin.OUT)

# --- Colors ---
red    = [255, 0, 0]
green  = [0, 255, 0]
blue   = [0, 0, 255]
yellow = [255, 255, 0]
pink   = [255, 0, 255]
cyan   = [0, 255, 255]
litir = [red, green, blue, yellow, pink, cyan]

# --- Shapes for 8 LEDs ---
SHAPES = {

    # Full outer border
    "square": [
        0, 1, 2, 3, 4,
        5, 			9,
        10, 		14,
        15, 		19,
        20, 21, 22, 23, 24
    ],

    # Centered X shape
    "x": [
        0, 6, 12, 18, 24,
        4, 8, 12, 16, 20
    ],


    # Diamond
    "diamond": [
               2,
          6,  7,  8,
      10, 11, 12, 13, 14,
          16, 17, 18,
               22
    ],

    # Triangle (point up)
    "triangle_up": [
        5, 6, 7, 8, 9,
         11, 12, 13,
             17
    ],

    # Triangle (point down)
    "triangle_down": [
        7, 11, 12, 13, 15, 16, 17, 18, 19
    ],


    # Two lines vertical
    "two_lines_v": [
        1, 3, 6, 8, 11, 13, 16, 18, 21, 23
    ],
    
    # Two lines Horizontal
    "two_lines_h": [
        5, 6, 7, 8, 9,
        15, 16, 17, 18, 19
    ],
    
    # Three lines Vertical
    "three_lines_v": [
        0, 2, 4, 5, 7, 9, 10, 12, 14, 15, 17, 19, 20, 22, 24
    ],
    
    # Three lines horizontal
    "three_lines horizontal": [
        0, 1, 2, 3, 4,
        10, 11, 12, 13, 14,
        20, 21, 22, 23, 24
    ],
    
}

shape_list = list(SHAPES.keys())

# --- LCD Setup ---
# --- LCD Setup ---
i2c = I2C(0, scl=Pin(6), sda=Pin(5), freq=400000)
devices = i2c.scan()

if len(devices) == 0:
    print("No i2c device !")
    lcd = None
else:
    lcd = I2cLcd(i2c, devices[0], 2, 16)  # use only first detected device


# --- Game variables ---
p1_score = 0
p2_score = 0
mode_shape = True  # True = SHAPE mode, False = COLOR mode
current_shape_1 = shape_list[0]
current_shape_2 = shape_list[1]
current_color_1 = litir[0]
current_color_2 = litir[1]
first_pressed = None  # Track first player press

# --- Draw Shape Function ---
def show_shape(np, shape_name, color):
    np.fill((0, 0, 0))
    for led in SHAPES[shape_name]:
        np[led] = color
    np.write()

# --- Debounce ---
def wait_release(button):
    sleep_ms(20)
    while button.value() == 0:
        sleep_ms(10)
    sleep_ms(20)

# --- Update Mode ---
def toggle_mode():
    global mode_shape
    mode_shape = not mode_shape
    led_mode.value(1)
    wait_release(btn_mode)
    led_mode.value(0)

# --- Update NeoPixel Strip ---
def update_strip(np, current_shape, current_color):
    current_shape = shape_list[urandom.randint(0, len(shape_list)-1)]
    current_color = litir[urandom.randint(0, len(litir)-1)]
    show_shape(np, current_shape, current_color)
    return current_shape, current_color

# --- Reaction-based scoring ---
def check_reaction_score():
    global p1_score, p2_score, first_pressed
    p1_down = btn_score1.value() == 0
    p2_down = btn_score2.value() == 0

    # Show LED indicators
    led_score1.value(p1_down)
    led_score2.value(p2_down)

    # Record first press
    if first_pressed is None:
        if p1_down:
            first_pressed = 'P1'
        elif p2_down:
            first_pressed = 'P2'

    # If a player has pressed first, check for match
    if first_pressed is not None:
        match = False
        if mode_shape and current_shape_1 == current_shape_2:
            match = True
        elif not mode_shape and current_color_1 == current_color_2:
            match = True

        # Give point to first player if match
        if match:
            if first_pressed == 'P1':
                p1_score += 1
            else:
                p2_score += 1

        # Reset for next round
        first_pressed = None
        wait_release(btn_score1)
        wait_release(btn_score2)

# --- Main Loop ---
while True:

    # --- Check mode button ---
    if btn_mode.value() == 0:
        toggle_mode()

    # --- Check NeoPixel 1 button ---
    if btn_np1.value() == 0:
        current_shape_1, current_color_1 = update_strip(np_1, current_shape_1, current_color_1)
        led_np1.value(1)
        wait_release(btn_np1)
    else:
        led_np1.value(0)

    # --- Check NeoPixel 2 button ---
    if btn_np2.value() == 0:
        current_shape_2, current_color_2 = update_strip(np_2, current_shape_2, current_color_2)
        led_np2.value(1)
        wait_release(btn_np2)
    else:
        led_np2.value(0)

    # --- Check reaction scoring ---
    check_reaction_score()

    # --- LCD Update ---
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr("P1:%d " % p1_score)
    lcd.move_to(10,0)
    lcd.putstr("P2:%d " % p2_score)
    lcd.move_to(2,1)
    lcd.putstr("MODE:" + ("SHAPE" if mode_shape else "COLOR"))

    sleep_ms(50)

