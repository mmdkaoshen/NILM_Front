import pyqtgraph as pg


class CurrentCurve(pg.PlotWidget):
    def __init__(self, deviceName: str):
        super().__init__()
        self.autoPixelRange = True
        self.enableMouse(False)
        self.setTitle(deviceName, color="#000000", size="14pt")
        self.setLabel("left", "电流")
        self.setLabel("bottom", "时间/ms")
        self.currentCurve = self.getPlotItem().plot(pen=pg.mkPen("b", width=2))

    def plotCurrentCurve(self, x: list, y: list):
        self.currentCurve.setData(x, y)

