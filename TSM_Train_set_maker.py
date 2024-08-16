#Code that is uploaded on Raspberry PI, GUI by pygame
#Records Audio in all polar angles

import pygame
import sys
import tkinter
import tkinter.filedialog

# 화면 크기 설정
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# 색상 정의
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 204, 212)

# pygame 초기화 및 설정
pygame.init()
pygame.display.set_caption("__TSM__")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 아이콘 이미지 설정
iconimg = pygame.image.load('/home/guccimane/Desktop/program/data/unedu.bmp')
pygame.display.set_icon(iconimg)

# 초기 위치 설정
pos_x = 200
pos_y = 200

# 버튼 색상 설정
color_light = (170, 170, 170)  # 밝은 색상
color_dark = (100, 100, 100)  # 어두운 색상

# 화면의 너비와 높이 가져오기
width = screen.get_width()
height = screen.get_height()

# 텍스트 출력 함수 (폰트 크기와 색상 포함)
def text(arg, fontsize, fontcolor):
    font = pygame.font.Font('/home/guccimane/Desktop/program/data/public-pixel-font/arcadelit.ttf', fontsize)
    text = font.render(str(arg), False, fontcolor)
    textRect = text.get_rect()
    return text, textRect

# 주어진 위치가 사각형 안에 있는지 확인하는 함수
def in_rect(pos, object):
    rect = object.rect
    if rect.left <= pos[0] <= rect.right and rect.top <= pos[1] <= rect.bottom:
        return True
    return False

# 버튼 객체 클래스 정의
class py_button:
    def __init__(self, ttx, pos, show=True):
        font = pygame.font.Font('/home/guccimane/Desktop/program/data/public-pixel-font/arcadelit.ttf', 13)
        self.text = font.render(str(ttx), False, black)
        self.rect = self.text.get_rect()
        self.rect.move_ip(pos[0], pos[1])
        self.show = show

# 모든 버튼을 화면에 그리는 함수
def blit_button(objects):
    for obj in objects:
        screen.blit(obj.text, obj.rect)

# 파일 선택 대화상자 열기
def prompt_file():
    filename = tkinter.filedialog.askdirectory()
    return filename

# 화면에 표시될 버튼들 생성
playsoundBT = py_button("play sound", (250, 50 + 50))
testsoundBT = py_button("test sound", (250, 100 + 50))
rotatetestBT = py_button("rotate test", (250, 150 + 50))
setcurrentangleBT = py_button("set current angle", (250, 200 + 50))
exitBT = py_button("exit", (250, 250 + 50))
homeBT = py_button("home", (5, 0))

soundcntTT = py_button(" ", (250, 100))
esttimeTT = py_button(" ", (250, 150))
letsgoBT = py_button("letsgo", (250, 200))

percentTT = py_button(" ", (250, 100))
audioTT = py_button(" ", (250, 200))

# 초기 상태 변수 설정
screentense = "1"
soundready = False
esttime = -1
esttime_secs = -1
objects = []
audios = []

# 서보모터 및 스테퍼 모터 설정
import RPi.GPIO as GPIO
import time

DUTY_MIN = 2.5  # 서보모터의 최소 듀티
DUTY_MAX = 11.5  # 서보모터의 최대 듀티
i = 0

servo1_pin = 15
servo2_pin = 9

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo1_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)

servo1 = GPIO.PWM(servo1_pin, 50)
servo2 = GPIO.PWM(servo2_pin, 50)

servo1.start(0)
servo2.start(0)

pol_angle = 0

# 서보모터를 특정 각도로 설정하는 함수
def posContDeg(deg, servo):
    duty = DUTY_MIN + (deg * (DUTY_MAX - DUTY_MIN) / 180)
    servo.ChangeDutyCycle(duty)

# 서보모터 각도 설정 함수
def servo_setDegree():
    global pol_angle
    deg = pol_angle
    global servo1, servo2
    posContDeg(180 - deg, servo1)
    posContDeg(deg, servo2)

# 스테퍼 모터 클래스 정의
class stepper():
    def __init__(self, pins, multiplier):
        self.pin = pins
        self.angle = 0
        self.multiplier = multiplier
        self.i = 0
        self.positive = 0
        self.negative = 0
        self.y = 0
        self.t = 0.01
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)

    def initGPIO(self):
        GPIO.setmode(GPIO.BCM)

    def move(self, angle):
        self.angle += angle
        GPIO.output(self.pin[0], GPIO.LOW)
        GPIO.output(self.pin[1], GPIO.LOW)
        GPIO.output(self.pin[2], GPIO.LOW)
        GPIO.output(self.pin[3], GPIO.LOW)
        x = angle * self.multiplier
        x = int(x)
        i = self.i
        negative = self.negative
        positive = self.positive
        y = int(self.y)
        if x > 0 and x <= 900:
            for y in range(x, 0, -1):
                if negative == 1:
                    if i == 7:
                        i = 0
                    else:
                        i = i + 1
                    y = y + 2
                    negative = 0
                    positive = 1
                if i == 0:
                    GPIO.output(self.pin[0], GPIO.HIGH)
                    GPIO.output(self.pin[1], GPIO.LOW)
                    GPIO.output(self.pin[2], GPIO.LOW)
                    GPIO.output(self.pin[3], GPIO.LOW)
                    time.sleep(self.t)
                elif i == 1:
                    GPIO.output(self.pin[0], GPIO.HIGH)
                    GPIO.output(self.pin[1], GPIO.HIGH)
                    GPIO.output(self.pin[2], GPIO.LOW)
                    GPIO.output(self.pin[3], GPIO.LOW)
                    time.sleep(self.t)
                elif i == 2:
                    GPIO.output(self.pin[0], GPIO.LOW)
                    GPIO.output(self.pin[1], GPIO.HIGH)
                    GPIO.output(self.pin[2], GPIO.LOW)
                    GPIO.output(self.pin[3], GPIO.LOW)
                    time.sleep(self.t)
                elif i == 3:
                    GPIO.output(self.pin[0], GPIO.LOW)
                    GPIO.output(self.pin[1], GPIO.HIGH)
                    GPIO.output(self.pin[2], GPIO.HIGH)
                    GPIO.output(self.pin[3], GPIO.LOW)
                    time.sleep(self.t)
                elif i == 4:
                    GPIO.output(self.pin[0], GPIO.LOW)
                    GPIO.output(self.pin[1], GPIO.LOW)
                    GPIO.output(self.pin[2], GPIO.HIGH)
                    GPIO.output(self.pin[3], GPIO.LOW)
                    time.sleep(self.t)
                elif i == 5:
                    GPIO.output(self.pin[0], GPIO.LOW)
                    GPIO.output(self.pin[1], GPIO.LOW)
                    GPIO.output(self.pin[2], GPIO.HIGH)
                    GPIO.output(self.pin[3], GPIO.HIGH)
                    time.sleep(self.t)
                elif i == 6:
                    GPIO.output(self.pin[0], GPIO.LOW)
                    GPIO.output(self.pin[1], GPIO.LOW)
                    GPIO.output(self.pin[2], GPIO.LOW)
                    GPIO.output(self.pin[3], GPIO.HIGH)
                    time.sleep(self.t)
                elif i == 7:
                    GPIO.output(self.pin[0], GPIO.HIGH)
                    GPIO.output(self.pin[1], GPIO.LOW)
                    GPIO.output(self.pin[2], GPIO.LOW)
                    GPIO.output(self.pin[3], GPIO.HIGH)
                    time.sleep(self.t)
                if i == 7:
                    i = 0
                    continue
                i = i + 1
        elif x < 0 and x >= -900:
            x = x * -1
            for y in range(x, 0, -1):
                if positive == 1:
                    if i == 0:
                        i = 7
                    else:
                        i = i - 1
                    y = y + 3
                    positive = 0
                    negative = 1
                if i == 0:
                    GPIO.output(self.pin[0], GPIO.HIGH)
                    GPIO.output(self.pin[1], GPIO.LOW)
                    GPIO.output(self.pin[2], GPIO.LOW)
                    GPIO.output(self.pin[3], GPIO.LOW)
                    time.sleep(self.t)
                elif i == 1:
                    GPIO.output(self.pin[0], GPIO.HIGH)
                    GPIO.output(self.pin[1], GPIO.HIGH)
                    GPIO.output(self.pin[2], GPIO.LOW)
                    GPIO.output(self.pin[3], GPIO.LOW)
                    time.sleep(self.t)
                elif i == 2:
                    GPIO.output(self.pin[0], GPIO.LOW)
                    GPIO.output(self.pin[1], GPIO.HIGH)
                    GPIO.output(self.pin[2], GPIO.LOW)
                    GPIO.output(self.pin[3], GPIO.LOW)
                    time.sleep(self.t)
                elif i == 3:
                    GPIO.output(self.pin[0], GPIO.LOW)
                    GPIO.output(self.pin[1], GPIO.HIGH)
                    GPIO.output(self.pin[2], GPIO.HIGH)
                    GPIO.output(self.pin[3], GPIO.LOW)
                    time.sleep(self.t)
                elif i == 4:
                    GPIO.output(self.pin[0], GPIO.LOW)
                    GPIO.output(self.pin[1], GPIO.LOW)
                    GPIO.output(self.pin[2], GPIO.HIGH)
                    GPIO.output(self.pin[3], GPIO.LOW)
                    time.sleep(self.t)
                elif i == 5:
                    GPIO.output(self.pin[0], GPIO.LOW)
                    GPIO.output(self.pin[1], GPIO.LOW)
                    GPIO.output(self.pin[2], GPIO.HIGH)
                    GPIO.output(self.pin[3], GPIO.HIGH)
                    time.sleep(self.t)
                elif i == 6:
                    GPIO.output(self.pin[0], GPIO.LOW)
                    GPIO.output(self.pin[1], GPIO.LOW)
                    GPIO.output(self.pin[2], GPIO.LOW)
                    GPIO.output(self.pin[3], GPIO.HIGH)
                    time.sleep(self.t)
                elif i == 7:
                    GPIO.output(self.pin[0], GPIO.HIGH)
                    GPIO.output(self.pin[1], GPIO.LOW)
                    GPIO.output(self.pin[2], GPIO.LOW)
                    GPIO.output(self.pin[3], GPIO.HIGH)
                    time.sleep(self.t)
                if i == 0:
                    i = 7
                    continue
                i = i - 1
        self.i = i
        self.negative = negative
        self.positive = positive
        self.y = y

    def setZero(self):
        self.angle = 0

# 스텝 각도를 설정하는 함수
def setStepAngle():
    global pol_angle
    aziStep.setZero()
    pol_angle = 0
    servo_setDegree()

# 스텝을 설정하는 함수
def setStep(azi, pol):
    if azi == -1 and pol == -1:
        setStep(180, 180)
        setStep(-180, 0)
        setStep(0, 0)
        print("360 done")
    else:
        aziStep.move(azi - aziStep.angle)
        global pol_angle
        pol_angle = pol
        servo_setDegree()

# GPIO 초기화 및 스테퍼 객체 생성
stepper.initGPIO(stepper)
aziStep = stepper((27, 17, 22, 18), 2 / 0.9)

# 메인 루프
while True:
    mouse = pygame.mouse.get_pos()
    screen.fill(white)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()

        if ev.type == pygame.MOUSEBUTTONDOWN:
            if screentense == '1':
                if in_rect(mouse, exitBT):
                    exit()
                elif in_rect(mouse, playsoundBT):
                    screentense = "playsound"
                elif in_rect(mouse, setcurrentangleBT):
                    screentense = "setcurrentangle"
                elif in_rect(mouse, testsoundBT):
                    screentense = "testsound"
                elif in_rect(mouse, rotatetestBT):
                    screentense = "rotatetest"

            if in_rect(mouse, homeBT):
                screentense = "1"

            if screentense == "playsound" and soundready:
                if in_rect(mouse, letsgoBT):
                    screentense = "runnin"

    if screentense == "1":
        objects = [playsoundBT, testsoundBT, setcurrentangleBT, rotatetestBT, exitBT, homeBT]
        soundready = False
        audios = []

    elif screentense == "playsound":
        objects = [homeBT]
        if not soundready:
            dir_path = prompt_file()
            import os
            res = []
            for path in os.listdir(dir_path):
                if os.path.isfile(os.path.join(dir_path, path)):
                    res.append(path)
            for p in res:
                path = dir_path + '/' + p
                audios.append((pygame.mixer.Sound(path), p))
            soundready = True

        if soundready:
            objects = [homeBT, soundcntTT, esttimeTT, letsgoBT]
            dur = 0
            for a in audios:
                dur += a[0].get_length()
            font = pygame.font.Font('./data/public-pixel-font/arcadelit.ttf', 13)
            soundcntTT.text = font.render(str(len(audios)), False, black)
            esttime = int(len(audios) * 36 * 72 * 1.1 * dur / 60 / 60)
            esttime_secs = esttime * 3600
            esttimeTT.text = font.render(str(esttime), False, black)

    elif screentense == "runnin":
        objects = [percentTT, esttimeTT, audioTT]
        task = 0
        setStep(1, 1)
        for audioinf in audios:
            audio = audioinf[0]
            audioname = audioinf[1]
            percent = (task / (360 / 5) * (180 / 5) * len(audios)) * 100
            esttime -= audio.get_length()
            esttime = int(esttime_secs / 60 / 60)
            font = pygame.font.Font('./data/public-pixel-font/arcadelit.ttf', 13)
            percentTT.text = font.render(str(percent), False, black)
            esttimeTT.text = font.render(str(esttime), False, black)
            audioTT.text = font.render(str(audioname), False, black)
            angleStep = 20

            for azi in range(-180, 180, angleStep):
                for pol in range(0, 180, angleStep):
                    setStep(azi, pol)
                    time.sleep(1)
                    print(audioname, azi, pol)
                    file_name = audioname[0:-4] + '_azi_' + str(azi) + '_pol_' + str(pol)
                    file_dir = '/media/guccimane/seagate/'
                    sleep_length = int(audio.get_length()) + 1
                    L_rec = 'arecord -D plughw:2,0 -t wav --duration=' + str(sleep_length) + ' -f cd ' + file_dir + file_name + 'L.wav'
                    R_rec = 'arecord -D plughw:1,0 -t wav --duration=' + str(sleep_length) + ' -f cd ' + file_dir + file_name + 'R.wav'
                    print(L_rec)
                    subprocess.Popen(shlex.split(L_rec))
                    subprocess.Popen(shlex.split(R_rec))
                    audio.play()
                    time.sleep(sleep_length)
                    print("sound record success")
                    task += 1
        screentense = '1'

    elif screentense == "testsound":
        objects = [homeBT]
        if not soundready:
            dir_path = prompt_file()
            import os
            res = []
            for path in os.listdir(dir_path):
                if os.path.isfile(os.path.join(dir_path, path)):
                    res.append(path)
            for p in res:
                path = dir_path + '/' + p
                audios.append(pygame.mixer.Sound(path))
            soundready = True

        if soundready:
            audios[0].play(maxtime=5000)
            screentense = "1"
            print("soundtest success!")

    elif screentense == "rotatetest":
        objects = [homeBT]
        setStep(-1, -1)
        screentense = '1'
        print("rotate test success")

    elif screentense == "setcurrentangle":
        objects = [homeBT]
        setStepAngle()
        screentense = '1'
        print("current angle set as (0, 0)")

    for items in objects:
        if in_rect(mouse, items):
            pygame.draw.rect(screen, gray, items.rect)
        blit_button(objects)

    pygame.display.update()
