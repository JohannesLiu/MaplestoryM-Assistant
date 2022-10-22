"""
# -*- coding:utf-8 -*-
@Project : SmartKartRider
@File : main.py.py
@Author : Johan
@Time : 10/20/2022 12:35 AM

"""
import cv2
import matplotlib.pyplot as plt
import time
import os
from IPython.display import clear_output
import datetime
from MapleKit.Utils.location import locateOnPicture, locateCenterOnPicture, pixelMatchesColor

WORKPATH = "C:/Users/Johan/Documents/PycharmProjects/MaplestoryM-Assistant"
desired_window = "BlueStacks App Player"
adb_port = 13221
os.chdir(WORKPATH)


if __name__ == "__main__":
    print(os.popen('adb devices').read())
    connect = os.popen("adb connect 127.0.0.1:" + str(adb_port)).read()
    print(connect)

    accept_button_pic = cv2.imread("./raw_data/US/Buttons/Accept_Button.png")
    claim_button_pic = cv2.imread("./raw_data/US/Buttons/ClaimReward_Button.png")
    complete_button_pic = cv2.imread("./raw_data/US/Buttons/Complete_Button.png")
    confirm_button_pic = cv2.imread("./raw_data/US/Buttons/Confirm_Button.png")
    autoplay_button_pic = cv2.imread("./raw_data/US/Buttons/AutoPlay.png")
    go_manully_button_pic = cv2.imread("./raw_data/US/Buttons/GoManully.png")
    autoassign_button_pic = cv2.imread("./raw_data/US/Buttons/AutoAssign_Button.png")
    equip_button_pic = cv2.imread("./raw_data/US/Buttons/Equip-Button.png")
    Available2Start_ComplexButton_pic = cv2.imread("./raw_data/US/Buttons/Available2Start-ComplexButton.png")
    Complete_ComplexButton_pic = cv2.imread("./raw_data/US/Buttons/Complete-ComplexButton.png")
    CloseMail_Button_pic = cv2.imread("./raw_data/US/Buttons/CloseMail-Button.png")

    AutoBattle_Status_pic  = cv2.imread("./raw_data/US/Status/AutoBattle-Status.png")
    AutoQuest_Status_pic  = cv2.imread("./raw_data/US/Status/AutoQuest-Status.png")
    c = 0.5

    run_count = 0
    while True:
        clear_output(wait=True)
        run_count += 1
        print(f"Current round count:{run_count}")
        if run_count%500==0:
            os.system("adb shell kill-server")
            os.system("adb shell start-server")
            os.popen("adb connect 127.0.0.1:" + str(adb_port))
        print(datetime.datetime.now())
        s = time.time()
        try:
            print("ForegroundWindow not BlueStacks, adb screencap is using.")
            os.system('adb shell screencap -p /sdcard/screenshot.png')
            os.system('adb pull /sdcard/screenshot.png ./screenshot.png')
            im = cv2.imread('./screenshot.png')
            os.system('adb shell rm /sdcard/screenshot.png')
            os.remove('./screenshot.png')
        except:
            print("Restart adb service")
            os.system("adb shell kill-server")
            os.system("adb shell start-server")
            os.popen("adb connect 127.0.0.1:" + str(adb_port))
            continue
        print("Begin Perturbation!")
        if locateOnPicture(autoassign_button_pic, im, confidence = 0.8):
            print("Auto Assign")
            retVal = locateCenterOnPicture(autoassign_button_pic, im, confidence = 0.8)
            os.system("adb shell input tap " + str(retVal[0]) + " " + str(retVal[1]))
            time.sleep(1)
        elif locateOnPicture(equip_button_pic, im, confidence = 0.8):
            print("Auto Equip")
            retVal = locateCenterOnPicture(equip_button_pic, im, confidence = 0.8)
            os.system("adb shell input tap " + str(retVal[0]) + " " + str(retVal[1]))
            time.sleep(1)
        elif locateOnPicture(CloseMail_Button_pic, im, confidence=0.95):
            print("Close All Mail")
            retVal = locateCenterOnPicture(CloseMail_Button_pic, im, confidence=0.95)
            os.system("adb shell input tap " + str(retVal[0]) + " " + str(retVal[1]))
            time.sleep(1)
        elif locateOnPicture(accept_button_pic, im, confidence = c):
            print("Accept")
            retVal = locateCenterOnPicture(accept_button_pic, im, confidence = c)
            os.system("adb shell input tap " + str(retVal[0]) + " " + str(retVal[1]))
            time.sleep(2)
        elif locateOnPicture(claim_button_pic, im, confidence = c):
            print("claim")
            retVal = locateCenterOnPicture(claim_button_pic, im, confidence = c)
            os.system("adb shell input tap " + str(retVal[0]) + " " + str(retVal[1]))
            time.sleep(2)
        elif locateOnPicture(confirm_button_pic, im, confidence = c):
            print("confirm")
            retVal = locateCenterOnPicture(confirm_button_pic, im, confidence = c)
            os.system("adb shell input tap " + str(retVal[0]) + " " + str(retVal[1]))
            time.sleep(2)
        elif locateOnPicture(complete_button_pic, im, confidence = c):
            print("complete")
            retVal = locateCenterOnPicture(complete_button_pic, im, confidence = c)
            os.system("adb shell input tap " + str(retVal[0]) + " " + str(retVal[1]))
            time.sleep(2)
        elif locateOnPicture(Complete_ComplexButton_pic, im, confidence = 0.9):
            print("Complex Choice: Complete")
            retVal = locateCenterOnPicture(Complete_ComplexButton_pic, im, confidence = 0.9)
            os.system("adb shell input tap " + str(retVal[0]) + " " + str(retVal[1]))
            time.sleep(2)
        elif locateOnPicture(Available2Start_ComplexButton_pic, im, confidence = 0.9):
            print("Complex Choice: Accept")
            retVal = locateCenterOnPicture(Available2Start_ComplexButton_pic, im, confidence = 0.9)
            os.system("adb shell input tap " + str(retVal[0]) + " " + str(retVal[1]))
            time.sleep(2)
        elif locateOnPicture(go_manully_button_pic, im, confidence = 0.8):
            print("In Autoplay Status")
            time.sleep(5)
        elif locateOnPicture(autoplay_button_pic, im, confidence = 0.8):
            print("AutoPlay Stopped, Tap to Continue!")
            retVal = locateCenterOnPicture(autoplay_button_pic, im, confidence = 0.8)
            print(retVal)
            os.system("adb shell input tap " + str(retVal[0]) + " " + str(retVal[1]))
            time.sleep(10)
        elif pixelMatchesColor(cv2.cvtColor(im,cv2.COLOR_BGR2RGB)[203, 95], (6, 171, 96), tolerance=20) and locateOnPicture(AutoBattle_Status_pic, im, confidence = 0.8) and not locateOnPicture(AutoQuest_Status_pic, im, confidence = 0.8):
            print("Start Quest")
            os.system("adb shell input tap 200 200")
            time.sleep(2)
        elif pixelMatchesColor(cv2.cvtColor(im,cv2.COLOR_BGR2RGB)[40, 110], (210, 195, 140), tolerance=20):
            print("Skip")
            os.system("adb shell input tap 284 402")
            time.sleep(2)
        else:
            os.system("adb shell input tap 1161 481")
            plt.imshow(im)
            print("Talking or Nothing to Do")
            time.sleep(1)