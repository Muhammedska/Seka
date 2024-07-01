import os
import random
import sqlite3
import requests
import sys
import csv
import pandas
import urllib3
import json

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5 import QtCore,QtGui
from PyQt5.QtCore import QTimer,QUrl,Qt
from PyQt5.QtGui import QPixmap,QIcon,QKeySequence,QFont

from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel,
                             QGridLayout, QFileDialog)

import sys
from bs4 import BeautifulSoup
import sys
import os
from os import path

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, \
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox
from PyQt5.QtCore import Qt, QEvent, QObject, QCoreApplication, QTimer
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

import win32gui
import win32ui
import win32con

import io
import win32clipboard
from PIL import Image

#for exporting error log
sys.stdout = open('stdout.txt', 'w+',encoding="utf-8")

global UI_PATH,OP_PATH

UI_PATH = "./UI/"
OP_PATH = "./data/"

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(UI_PATH+'mainwindow.ui', self)

        h = QtWidgets.QDesktopWidget().screenGeometry().height()
        w = QtWidgets.QDesktopWidget().screenGeometry().width()

        #flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        #self.setWindowFlags(flags)
        #self.next_win = False

        #self.label.setPixmap(QPixmap(data["icon-top-left"]))
        #self.label_4.setPixmap(QPixmap(data["login-middle"]))
        #self.base.move(int((w-400)/2),int((h-540)/2))
        #self.syprexrunner.clicked.connect(self.syprexcomrunner)
        #self.login.clicked.connect(self.login_)
        #self.label_3.setText(company)

        self.takescreenshot.clicked.connect(self.tsc)
        self.questiondb.clicked.connect(self.tsc)
        self.createexam.clicked.connect(self.tsc)
    def tsc(self):
        self.reqcretor = screenshotapp()
        self.reqcretor.show()
        self.close()
        print("screenshooter startted")


class screenshotapp(QtWidgets.QMainWindow):
    def __init__(self):
        super(screenshotapp, self).__init__()
        print(1)
        uic.loadUi(UI_PATH + 'snapshot.ui', self)

        self.region_screenshot.clicked.connect(self.take_region_snapshot)
        print(2)
    def take_region_snapshot(self):

        screenshooter()
        self.close()

    def selectArea(self):


        print(3)


        print(4)


        print(5)

def screenshooter():
    print()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()