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
from skimage.metrics import peak_signal_noise_ratio as compare_psnr
import joblib

WORKPATH = "C:/Users/Johan/Documents/PycharmProjects/MaplestoryM-Assistant"
desired_window = "BlueStacks App Player"
adb_port = 59487
os.chdir(WORKPATH)



if __name__ == "__main__":
    print(os.popen('adb devices').read())
    connect = os.popen("adb connect 127.0.0.1:" + str(adb_port)).read()
    print(connect)

    model = joblib.load("./output/ckpt/status-predictor.pkl")
    # Quest_State = 0
    # Quest_Timer = 0

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
    CloseInvitation1_Button_pic = cv2.imread("./raw_data/US/Buttons/CloseInvitation1-Button.png")
    CloseInvitation2_Button_pic = cv2.imread("./raw_data/US/Buttons/CloseInvitation2-Button.png")
    ReviveInTown_Button_pic  = cv2.imread("./raw_data/US/Buttons/ReviveInTown-Button.png")
    AutoBattle_Status_pic  = cv2.imread("./raw_data/US/Status/AutoBattle-Status.png")
    AutoQuest_Status_pic  = cv2.imread("./raw_data/US/Status/AutoQuest-Status.png")

    WaitQuestTime = 0

    c = 0.55
    run_count = 0
    while True:
        clear_output(wait=True)
        run_count += 1
        print(f"Current round count:{run_count}")
        if run_count%10000==0:
            os.system("adb shell kill-server")
            os.system("adb shell start-server")
            os.popen("adb connect 127.0.0.1:" + str(adb_port))
        print(datetime.datetime.now())
        s = time.time()
        try:
            os.system('adb shell screencap -p /sdcard/screenshot.png')
            os.system('adb pull /sdcard/screenshot.png ./screenshot.png')
            # print("copy .\\screenshot.png .\\raw_data\\US\\Status\\raw_data\\" + str(datetime.datetime.now()).replace(" ", "_").replace(":", "_") + ".png")
            # os.system("copy .\\screenshot.png .\\raw_data\\US\\Status\\raw_data\\" + str(datetime.datetime.now()).replace(" ", "_").replace(":", "_") + ".png")
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
            WaitQuestTime = 0
            time.sleep(0.1)
        elif locateOnPicture(equip_button_pic, im, confidence = 0.8):
            print("Auto Equip")
            retVal = locateCenterOnPicture(equip_button_pic, im, confidence = 0.8)
            os.system("adb shell input tap " + str(retVal[0]) + " " + str(retVal[1]))
            WaitQuestTime = 0
            time.sleep(0.1)
        elif locateOnPicture(ReviveInTown_Button_pic, im, confidence=0.9):
            print("Revive In Town")
            retVal = locateCenterOnPicture(ReviveInTown_Button_pic, im, confidence=0.9)
            os.system("adb shell input tap " + str(retVal[0]) + " " + str(retVal[1]))
            WaitQuestTime = 0
            time.sleep(0.1)
        elif locateOnPicture(claim_button_pic, im, confidence = c):
            print("Claim")
            retVal = locateCenterOnPicture(claim_button_pic, im, confidence = c)
            # os.system("adb shell input tap " + str(retVal[0]) + " " + str(retVal[1]))
            os.system("adb shell input tap 637 648")
            WaitQuestTime = 0
            time.sleep(0.1)
        elif locateOnPicture(accept_button_pic, im, confidence = c): # tap: 1096 427
            print("Accept")
            retVal = locateCenterOnPicture(accept_button_pic, im, confidence = c)
            os.system("adb shell input tap " + str(retVal[0]) + " " + str(retVal[1]))
            os.system("adb shell input tap 1096 427")
            WaitQuestTime = 0
            time.sleep(0.1)
        elif locateOnPicture(confirm_button_pic, im, confidence = c):
            print("Confirm")
            retVal = locateCenterOnPicture(confirm_button_pic, im, confidence = c)
            os.system("adb shell input tap " + str(retVal[0]) + " " + str(retVal[1]))
            os.system("adb shell input tap 1096 427")
            WaitQuestTime = 0
            time.sleep(0.1)
        elif locateOnPicture(complete_button_pic, im, confidence = c):
            print("Complete")
            retVal = locateCenterOnPicture(complete_button_pic, im, confidence = c)
            os.system("adb shell input tap " + str(retVal[0]) + " " + str(retVal[1]))
            os.system("adb shell input tap 1096 427")
            WaitQuestTime = 0
            time.sleep(0.1)
        elif locateOnPicture(Complete_ComplexButton_pic, im, confidence = 0.9):
            print("Complex Choice: Complete")
            retVal = locateCenterOnPicture(Complete_ComplexButton_pic, im, confidence = 0.9)
            os.system("adb shell input tap " + str(retVal[0]) + " " + str(retVal[1]))
            WaitQuestTime = 0
            time.sleep(0.1)
        elif locateOnPicture(Available2Start_ComplexButton_pic, im, confidence = 0.8):
            print("Complex Choice: Accept")
            retVal = locateCenterOnPicture(Available2Start_ComplexButton_pic, im, confidence = 0.8)
            os.system("adb shell input tap " + str(retVal[0]) + " " + str(retVal[1]))
            WaitQuestTime = 0
            time.sleep(0.1)
        elif locateOnPicture(go_manully_button_pic, im, confidence = 0.8):
            print("In Autoplay Status")
            WaitQuestTime = 0
            time.sleep(5)
        elif locateOnPicture(autoplay_button_pic, im, confidence = 0.8):
            print("AutoPlay Stopped, Tap to Continue!")
            retVal = locateCenterOnPicture(autoplay_button_pic, im, confidence = 0.8)
            print(retVal)
            os.system("adb shell input tap " + str(retVal[0]) + " " + str(retVal[1]))
            WaitQuestTime = 0
            time.sleep(10)
        elif locateOnPicture(CloseInvitation1_Button_pic, im, confidence=0.80):
            print("Close Invitation 1")
            retVal = locateCenterOnPicture(CloseInvitation1_Button_pic, im, confidence=0.80)
            os.system("adb shell input tap " + str(retVal[0]) + " " + str(retVal[1]))
            WaitQuestTime = 0
            time.sleep(0.1)
        elif locateOnPicture(CloseInvitation2_Button_pic, im, confidence=0.80):
            print("Close Invitation 2")
            retVal = locateCenterOnPicture(CloseInvitation2_Button_pic, im, confidence=0.80)
            os.system("adb shell input tap " + str(retVal[0]) + " " + str(retVal[1]))
            WaitQuestTime = 0
            time.sleep(0.1)
        elif locateOnPicture(CloseMail_Button_pic, im, confidence=0.95):
            print("Close All Mail")
            retVal = locateCenterOnPicture(CloseMail_Button_pic, im, confidence=0.95)
            os.system("adb shell input tap " + str(retVal[0]) + " " + str(retVal[1]))
            WaitQuestTime = 0
            time.sleep(0.1)
        # elif pixelMatchesColor(cv2.cvtColor(im,cv2.COLOR_BGR2RGB)[203, 95], (6, 171, 96), tolerance=20) and locateOnPicture(AutoBattle_Status_pic, im[610:700, 390:450], confidence = 0.90) and not locateOnPicture(AutoQuest_Status_pic, im[610:700, 390:450], confidence = 0.90) and Quest_State == 0:
        # elif pixelMatchesColor(cv2.cvtColor(im,cv2.COLOR_BGR2RGB)[203, 95], (6, 171, 96), tolerance=20) :
        #     # print("./raw_data/US/Status/data/"+ str(datetime.datetime.now()).replace(" ", "_").replace(":", "_")+ ".png" )
        #     # cv2.imwrite("./raw_data/US/Status/data/"+ str(datetime.datetime.now()).replace(" ", "_").replace(":", "_") + ".png", im[625:685, 390:455])
        #     print("Start Machine Learning Model")
        #     print(cv2.cvtColor(im[625:685, 390:455], cv2.COLOR_BGR2GRAY).shape)
        #     result = model.predict(cv2.cvtColor(im[625:685, 390:455], cv2.COLOR_BGR2GRAY).reshape(1, -1))
        #     print("Prediction Result: " + result[0])
        #     if result[0] == "AutoBattle" or WaitQuestTime > 300:
        #         print("Start Quest")
        #         os.system("adb shell input tap 200 200")
        #         WaitQuestTime = 0
        #         time.sleep(1)
        #     else:
        #         print("Keep Quest, WaitQuestTime: " + str(WaitQuestTime))
        #         # os.system("adb shell input tap 857 655")
        #         WaitQuestTime += 1
        #         time.sleep(1)
        #         continue
        elif model.predict(cv2.cvtColor(im[625:685, 390:455], cv2.COLOR_BGR2GRAY).reshape(1, -1))[0] == "AutoBattle" or WaitQuestTime > 300:
            # print("./raw_data/US/Status/data/"+ str(datetime.datetime.now()).replace(" ", "_").replace(":", "_")+ ".png" )
            # cv2.imwrite("./raw_data/US/Status/data/"+ str(datetime.datetime.now()).replace(" ", "_").replace(":", "_") + ".png", im[625:685, 390:455])
            print("Start Quest")
            os.system("adb shell input tap 200 200")
            WaitQuestTime = 0
            time.sleep(1)
        elif pixelMatchesColor(cv2.cvtColor(im,cv2.COLOR_BGR2RGB)[40, 110], (210, 195, 140), tolerance=20):
            print("Skip")
            WaitQuestTime = 0
            time.sleep(0.1)
        else:
            os.system("adb shell input tap 1161 481")
            plt.imshow(im)
            print("Talking or Nothing to Do")
            os.system("adb shell input tap 587 655")
            WaitQuestTime = 0
            time.sleep(0.1)

        # Quest_Timer += 1
        # if Quest_State == Quest_Timer and Quest_State == 1:
        #     os.system("adb shell input tap 200 200")
        #     time.sleep(2)
        # else:
        #     Quest_State = 0
        #     Quest_Timer = 0

    '''
    State 1: Confirm/Accept/Complete/Claim
        Repete = 1
    State 2: Talking or Nothing to Do
        Repete = Many Times
    State 3: Start Quest
        Repete = 1
    State 4: Auto Assign/Auto Equip
        Repete = 1
    State 5: Close All Mail
        Repete = 1
    State 6: go_manully_button
        Repete = Many Times
    State 7: Go Auto
        repete = 1
    '''