from time import sleep
import RPi.GPIO as GPIO
import time

LedPin = 11  # pin11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)

pwm = GPIO.PWM(3, 50)
pwm.start(0)

blink_state = 0


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
    GPIO.setup(LedPin, GPIO.OUT)  # Set LedPin's mode is output
    GPIO.output(LedPin, GPIO.HIGH)  # Set LedPin high(+3.3V) to turn on led

    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def SetAngle(angle):
    duty = angle / 18 + 2
    # GPIO.output(3, True)
    pwm.ChangeDutyCycle(duty)
    # time.sleep(0.5)
    # GPIO.output(3, False)
    # pwm.ChangeDutyCycle(0)


def setTargeAngle(angle):
    time.sleep(0.5)
    SetAngle()


def ledon():
    GPIO.output(LedPin, GPIO.HIGH)  # led on


def ledoff():
    GPIO.output(LedPin, GPIO.LOW)  # led on


def blink():
    blink.state = 0
    if blink.state == 0:
        GPIO.output(LedPin, GPIO.HIGH)  # led on
        blink.state = 1
        print('Led on')
    else:
        GPIO.output(LedPin, GPIO.LOW)  # led off
        blink.state = 0
        print('Led off')


def run():
    angletmp = 90
    run.counter = 0
    while True:
        input_state = GPIO.input(12)
        if input_state == False:
            # print('Button Pressed')
            time.sleep(0.1)

            run.counter = run.counter + 1;
            if run.counter > 5:
                ledon()

            if run.counter > 10:
                ledoff()
                run.counter = 0
            if angletmp < 170:
                angletmp = angletmp + 2
            SetAngle(angletmp)

        else:
            ledon()
            time.sleep(0.1)
            if angletmp > 10:
                angletmp = angletmp - 2
            SetAngle(angletmp)


def destroy():
    GPIO.output(LedPin, GPIO.LOW)  # led off
    GPIO.cleanup()  # Release resource
    pwm.stop()


if __name__ == '__main__':  # Program start from here
    setup()
    try:
        run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()