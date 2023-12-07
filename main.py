import json
import subprocess
import sys
import numpy as np
import time

import pymysql
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from MainUI import MainUI
from StatusLabel import StatusLabel


class MyWindow(QMainWindow, MainUI):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.setFocusPolicy(Qt.ClickFocus)
        self.x = [i for i in range(1000)]
        self.cnt = 0
        self.deviceMap = {
            0: 'iPad',
            1: '电锅',
            2: '显示器',
            3: '暖风机',
            4: '手机',
            5: '未知设备'
        }

        self.getResultDataTimer = QTimer()
        self.getResultDataTimer.timeout.connect(self.getResultRequest)

        self.resultDataManager = QNetworkAccessManager()
        self.resultDataManager.finished.connect(self.resultDataHandler)

        self.connection = pymysql.Connect(
            host="localhost",
            user="root",
            password="123456"
        )

        self.getCurrentButton.clicked.connect(self.startGetCurrentTimer)
        self.startSamplerButton.clicked.connect(self.startSampler)
        self.energyInquiryButton.clicked.connect(self.inquireHistoryEnergy)
        self.statusInquiryButton.clicked.connect(self.inquireHistoryStatus)

    # def select_file(self):  # 选择检测文件按钮事件绑定
    #     self.timer.stop()
    #     self.cnt = 0
    #     # directory = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件", "data/", "All Files (*);;Text Files (*.txt)")
    #     directory = QFileDialog.getOpenFileName(
    #         self, "选取文件", "./data", "All Files (*);;NPY Files (*.npy)"
    #     )
    #
    #     if directory[0] != "":
    #         print(directory[0])
    #         if directory[0].split("/")[-1][-4:] == ".npy":
    #             self.data = np.load(directory[0])
    #             print(self.data.shape)
    #             self.currentCurveTimer.start(2000)
    #
    #         elif directory[0].split("/")[-1][-4:] == ".dat":
    #             ...
    #
    #         else:
    #             QMessageBox.information(
    #                 self, "信息提示框", "请选择正确的dat/csv文件", QMessageBox.Yes
    #             )

    def plot(self, status, data):
        self.postProcess(status, data)

        self.iPadCurrentWidget.plotCurrentCurve(self.x, data[0])

        self.potCurrentWidget.plotCurrentCurve(self.x, data[1])

        self.monitorCurrentWidget.plotCurrentCurve(self.x, data[2])

        self.fanCurrentWidget.plotCurrentCurve(self.x, data[3])

        self.phoneCurrentWidget.plotCurrentCurve(self.x, data[4])

    def startGetCurrentTimer(self):
        self.getResultDataTimer.start(1000)

    @staticmethod
    def startSampler():
        subprocess.run(r"D:\ProgramData\code\c++\T3\Release\T3.exe")

    def getResultRequest(self):
        url = "http://localhost:2020/disaggregate"  # 修改为您所需的URL
        request = QNetworkRequest(QUrl(url))
        self.resultDataManager.get(request)
        self.cnt += 1

    def resultDataHandler(self, reply):
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll().data().decode('utf-8')
            data = json.loads(data)
            self.changeStatus(data['status'])
            self.recordEnergy(data['energy'])
            self.plot(data['status'], data['disaggregation'])
        else:
            print("请求出错: {0}".format(reply.errorString()))

        reply.deleteLater()

    def inquireHistoryEnergy(self):
        self.historyEnergy.clear()
        content = ''
        devices = self.energyComboCheckBox.currentText().split(';')
        inquiryDevices = set()
        for device in devices:
            inquiryDevices.add(self.getDeviceId(device))
        startDateTime = self.startTimeEditEnergy.getTime()
        endDateTime = self.endTimeEditEnergy.getTime()
        queryUse = "use powermonitoring;"
        querySelect = "select * from device_energy where start_time >= %s AND end_time <= %s AND device_id in %s;"

        self.connection.ping(True)
        with self.connection.cursor() as cursor:
            cursor.execute(queryUse)
            cursor.execute(querySelect, (startDateTime, endDateTime, inquiryDevices))
            results = cursor.fetchall()
            for result in results:
                content += f'{self.deviceMap[result[0]]}消耗电量: {result[3]}\n'
            self.historyEnergy.changeText(content)

    def inquireHistoryStatus(self):
        self.historyStatus.clear()
        onDevice = []
        content = ''
        devices = self.energyComboCheckBox.currentText().split(';')
        inquiryDevices = set()
        for device in devices:
            inquiryDevices.add(self.getDeviceId(device))
        startDateTime = self.startTimeEditEnergy.getTime()
        endDateTime = self.endTimeEditEnergy.getTime()
        queryUse = "use switchstatus;"
        querySelect = "select * from switch_status where start_time <= %s AND end_time >= %s AND device_is in %s;"

        self.connection.ping(True)
        with self.connection.cursor() as cursor:
            cursor.execute(queryUse)
            cursor.execute(querySelect, (startDateTime, endDateTime, inquiryDevices))
            results = cursor.fetchall()
            for result in results:
                onDevice.append(self.deviceMap[result[0]])
            for k, v in self.deviceMap.items():
                if v in onDevice:
                    content += f'{v}的开关状态：开机\n'
                else:
                    content += f'{v}的开关状态：关机\n'
            self.historyStatus.changeText(content)

    def changeStatus(self, status: list):
        status = np.array(status)
        idx = np.where(status == -1)
        status[idx] = 1

        # self.iPadStatusLabel.changeIcon(f'./Assets/icon/iPad{status[0]}.png')
        # self.potStatusLabel.changeIcon(f'./Assets/icon/pot{status[1]}.png')
        # self.monitorStatusLabel.changeIcon(f'./Assets/icon/monitor{status[2]}.png')
        # self.fanStatusLabel.changeIcon(f'./Assets/icon/fan{status[3]}.png')
        # self.phoneStatusLabel.changeIcon(f'./Assets/icon/phone{status[4]}.png')
        for i in reversed(range(1, self.horizontalLayoutStatus.count())):
            widget = self.horizontalLayoutStatus.itemAt(i).widget()
            self.horizontalLayoutStatus.removeWidget(widget)
            widget.setParent(None)
            widget.deleteLater()
        cnt = 0
        for i in range(len(status)):
            if status[i] == 1:
                statusLabel = StatusLabel(f'./Assets/icon/{self.deviceMap[i]}1.png')
                self.horizontalLayoutStatus.addWidget(statusLabel)
                cnt += 1

    def recordEnergy(self, energy):
        self.iPadEnergyLabel.changeText(str(round(energy[0], 3)))
        self.phoneEnergyLabel.changeText(str(round(energy[1], 3)))
        self.monitorEnergyLabel.changeText(str(round(energy[2], 3)))
        self.fanEnergyLabel.changeText(str(round(energy[3], 3)))
        self.potEnergyLabel.changeText(str(round(energy[4], 3)))

    @staticmethod
    def postProcess(status, data):
        for i, s in enumerate(status):
            if s == 0:
                data[i] = [0] * len(data[i])

    def getDeviceId(self, value):
        for key, val in self.deviceMap.items():
            if val == value:
                return key


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec()
