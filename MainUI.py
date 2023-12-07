from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
from PyQt5.QtWidgets import QSizePolicy, QSpacerItem

from PushButton import PushButton
from StatusLabel import StatusLabel
from CurrentCurve import CurrentCurve
from EnergyLabel import EnergyLabel
from TimeEdit import TimeEdit
from DeviceComboCheckBox import ComboCheckBox


class MainUI(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1080, 1080)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("./icon/paint.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        MainWindow.setWindowIcon(icon)

        self.centralWidget = QtWidgets.QWidget()
        self.centralWidget.setObjectName("centralWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName("verticalLyout")

        self.horizontalLayoutStatus = QtWidgets.QHBoxLayout()
        self.horizontalLayoutStatus.setAlignment(QtCore.Qt.AlignLeft)
        spacer = QSpacerItem(20, 100)  # 宽度为20像素，高度为40像素的空白区域
        self.horizontalLayoutStatus.addItem(spacer)
        self.horizontalLayoutEnergy = QtWidgets.QHBoxLayout()
        self.horizontalLayoutData = QtWidgets.QHBoxLayout()

        self.iPadStatusLabel = StatusLabel('./Assets/icon/iPad1.png')
        self.phoneStatusLabel = StatusLabel('./Assets/icon/phone1.png')
        self.monitorStatusLabel = StatusLabel('./Assets/icon/monitor1.png')
        self.fanStatusLabel = StatusLabel('./Assets/icon/fan1.png')
        self.potStatusLabel = StatusLabel('./Assets/icon/pot1.png')

        # self.horizontalLayoutStatus.addWidget(self.iPadStatusLabel)
        # self.horizontalLayoutStatus.addWidget(self.potStatusLabel)
        # self.horizontalLayoutStatus.addWidget(self.monitorStatusLabel)
        # self.horizontalLayoutStatus.addWidget(self.fanStatusLabel)
        # self.horizontalLayoutStatus.addWidget(self.phoneStatusLabel)

        self.iPadEnergyLabel = EnergyLabel()
        self.iPadEnergyLabel.setFixedSize(100, 40)
        self.phoneEnergyLabel = EnergyLabel()
        self.phoneEnergyLabel.setFixedSize(100, 40)
        self.monitorEnergyLabel = EnergyLabel()
        self.monitorEnergyLabel.setFixedSize(100, 40)
        self.fanEnergyLabel = EnergyLabel()
        self.fanEnergyLabel.setFixedSize(100, 40)
        self.potEnergyLabel = EnergyLabel()
        self.potEnergyLabel.setFixedSize(100, 40)

        # self.horizontalLayoutEnergy.addWidget(self.iPadEnergyLabel)
        # self.horizontalLayoutEnergy.addWidget(self.potEnergyLabel)
        # self.horizontalLayoutEnergy.addWidget(self.monitorEnergyLabel)
        # self.horizontalLayoutEnergy.addWidget(self.fanEnergyLabel)
        # self.horizontalLayoutEnergy.addWidget(self.phoneEnergyLabel)

        self.hLine = QtWidgets.QFrame()
        self.hLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.hLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hLine.setObjectName("hLine")

        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollWidget = QtWidgets.QWidget()
        self.scrollWidget.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.curveLayout = QtWidgets.QVBoxLayout(self.scrollWidget)
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.currentCurve = QtWidgets.QGridLayout()

        self.getCurrentButton = PushButton('getCurrentButton')
        self.startSamplerButton = PushButton('startSampler')
        self.buttonLayout.addWidget(self.startSamplerButton)
        self.buttonLayout.addWidget(self.getCurrentButton)
        self.buttonLayout.setAlignment(QtCore.Qt.AlignHCenter)
        # self.buttonLayout.addStretch()

        pg.setConfigOption("background", "w")

        self.iPadCurrentWidget = CurrentCurve('iPad电流')
        self.currentCurve.addWidget(self.iPadCurrentWidget, 0, 0)

        self.potCurrentWidget = CurrentCurve('电锅电流')
        self.currentCurve.addWidget(self.potCurrentWidget, 1, 0)

        self.monitorCurrentWidget = CurrentCurve('显示器电流')
        self.currentCurve.addWidget(self.monitorCurrentWidget, 2, 0)

        self.fanCurrentWidget = CurrentCurve('暖风机电流')
        self.currentCurve.addWidget(self.fanCurrentWidget, 3, 0)

        self.phoneCurrentWidget = CurrentCurve('手机电流')
        self.currentCurve.addWidget(self.phoneCurrentWidget, 4, 0)

        self.curveLayout.addLayout(self.buttonLayout)
        self.curveLayout.addLayout(self.currentCurve)

        self.scrollArea.setWidget(self.scrollWidget)
        self.horizontalLayoutData.addWidget(self.scrollArea)
        # self.horizontalLayoutData.addStretch()

        self.vLine = QtWidgets.QFrame()
        self.vLine.setFrameShape(QtWidgets.QFrame.VLine)
        self.vLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.vLine.setObjectName("vLine")

        self.historyLayout = QtWidgets.QVBoxLayout()
        # self.historyLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.energyHistoryInquiry = QtWidgets.QGridLayout()
        # self.energyHistory.setAlignment(QtCore.Qt.AlignHCenter)
        self.statusHistoryInquiry = QtWidgets.QGridLayout()
        # self.statusHistory.setAlignment(QtCore.Qt.AlignHCenter)

        self.energyComboCheckBox = ComboCheckBox(['iPad', '电锅', '显示器', '暖风机', '手机'])
        self.startTimeEditEnergy = TimeEdit()
        self.endTimeEditEnergy = TimeEdit()
        self.energyInquiryButton = PushButton('energyInquiryButton')
        self.historyEnergy = EnergyLabel()

        self.statusComboCheckBox = ComboCheckBox(['iPad', '电锅', '显示器', '暖风机', '手机'])
        self.startTimeEditStatus = TimeEdit()
        self.endTimeEditStatus = TimeEdit()
        self.statusInquiryButton = PushButton('statusInquiryButton')
        self.historyStatus = EnergyLabel()

        self.hLine2 = QtWidgets.QFrame()
        self.hLine2.setFrameShape(QtWidgets.QFrame.HLine)
        self.hLine2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hLine2.setObjectName("hLine2")

        self.energyHistoryInquiry.addWidget(self.energyComboCheckBox, 0, 0)
        self.energyHistoryInquiry.addWidget(self.startTimeEditEnergy, 1, 0)
        self.energyHistoryInquiry.addWidget(self.endTimeEditEnergy, 1, 1)
        self.energyHistoryInquiry.addWidget(self.energyInquiryButton, 0, 1)
        self.statusHistoryInquiry.addWidget(self.statusComboCheckBox, 0, 0)
        self.statusHistoryInquiry.addWidget(self.startTimeEditStatus, 1, 0)
        self.statusHistoryInquiry.addWidget(self.endTimeEditStatus, 1, 1)
        self.statusHistoryInquiry.addWidget(self.statusInquiryButton, 0, 1)

        self.historyEnergyHLayout = QtWidgets.QHBoxLayout()
        self.historyEnergyHLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.historyEnergyHLayout.addWidget(self.historyEnergy)

        self.historyStatusHLayout = QtWidgets.QHBoxLayout()
        self.historyStatusHLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.historyStatusHLayout.addWidget(self.historyStatus)

        self.historyLayout.addLayout(self.energyHistoryInquiry)
        self.historyLayout.addLayout(self.historyEnergyHLayout)
        self.historyLayout.addStretch()
        self.historyLayout.addWidget(self.hLine2)
        self.historyLayout.addLayout(self.statusHistoryInquiry)
        self.historyLayout.addLayout(self.historyStatusHLayout)
        self.historyLayout.addStretch()

        self.horizontalLayoutData.addWidget(self.vLine)
        self.horizontalLayoutData.addLayout(self.historyLayout)

        self.verticalLayout.addLayout(self.horizontalLayoutStatus)
        self.verticalLayout.addLayout(self.horizontalLayoutEnergy)
        self.verticalLayout.addWidget(self.hLine)
        self.verticalLayout.addLayout(self.horizontalLayoutData)

        self.retranslateUi(MainWindow)
        MainWindow.setCentralWidget(self.centralWidget)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("MainWindow", "NILM系统"))
        self.getCurrentButton.setText(_translate("MainWindow", "开始获取电流"))
        self.startSamplerButton.setText(_translate("MainWindow", "启动采样器"))
        self.energyInquiryButton.setText(_translate("MainWindow", "查询"))
        self.statusInquiryButton.setText(_translate("MainWindow", "查询"))
