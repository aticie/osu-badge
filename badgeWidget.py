
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPointF
from PyQt5.QtWidgets import QWidget, QMainWindow, QGridLayout, QSlider, QPushButton, QShortcut, QLabel
from PyQt5.QtGui import QColor, QPainterPath, QPainter, QPen, QKeySequence, QIcon, QPalette, QBrush, QFont, QPixmap, QImage

class _Renderer(QWidget):

    def __init__(self, score_info, graph, hitmap):
        super(_Renderer, self).__init__()
        self.graph = graph
        self.score_info = score_info
        self.hitmap = hitmap
        self.setFixedSize(616,192)  # stollen from some banner site
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(QPen(QColor(0, 0, 0, 180)))
        index = 0
        # background
        pixmap = QPixmap("background.png")
        painter.drawPixmap(0,0,616,192, pixmap)
        for i in self.graph:
            index += 1
            self.draw_bar(painter, i, index)
        self.draw_hitmap(painter, self.hitmap)        
        self.draw_info(painter, self.score_info)

    def draw_bar(self, painter, size, index):
        sliderbody = QPainterPath()

        _pen = painter.pen()
        _pen.setWidth(13)
        _pen.setCapStyle(Qt.RoundCap)
        _pen.setJoinStyle(Qt.RoundJoin)
        sliderbody.moveTo(5+20*index, 192-20)
        if size >= 0.01:
            sliderbody.lineTo(5+20*index, 192-20- ((192-120)*size))
        else:
            sliderbody.lineTo(5+20*index, 192-20+0.01)


        painter.setPen(_pen)
        painter.drawPath(sliderbody)

    def draw_info(self, painter, score_info):
        _pen = QPen(QColor(0, 0, 0, 180))
        _pen.setWidth(0)
        painter.setPen(_pen)
        painter.setBrush(QBrush(QColor(0, 0, 0, 180)))

        _pen = painter.pen()
        kek = QPainterPath()
        kek.addText(15, 30,QFont("Exo 2", pointSize=20, weight=500), "Setting Sail, Coming Home")
        kek.addText(352, 30, QFont("Exo 2", pointSize=10, weight=500),"[Insane]")
        kek.addText(15, 55, QFont("Exo 2", pointSize=15, weight=500), f'{score_info["count100"]}x100 | {score_info["count50"]}x50 | {score_info["countmiss"]}x0 | mods:NC')
        acc = round(((int(score_info["count300"])*300) + (int(score_info["count100"])*100) + (int(score_info["count50"])*50)) / ( 300 * (int(score_info["count300"]) + int(score_info["count50"]) + int(score_info["count100"])) )*100,2)
        kek.addText(15, 80, QFont("Exo 2", pointSize=15, weight=500),f'{score_info["maxcombo"]}x/625x | {acc}% | played by ] [')
        score_info["pp"] = round(float(score_info["pp"]),2)
        kek.addText(365, 192-15, QFont("Exo 2", pointSize=38, weight=500, italic=True), f'{score_info["pp"]}PP')  # {round(float(score_info["pp"]),2)}
        kek.addText(533- (20 if len(score_info["rank"]) == 2 else 0), 90, QFont("Exo 2", pointSize=55, weight=800), score_info["rank"] if score_info["rank"] != "SH" else "S+")
        painter.drawPath(kek)
    
    def draw_hitmap(self, painter, hitmap):
        _pen = painter.pen()
        c = _pen.color()
        _pen = QPen(QColor(c.red(), c.green(), c.blue(), 20))
        _pen.setWidth(0)
        painter.setBrush(QBrush(QColor(c.red(), c.green(), c.blue(), 30)))
        painter.setPen(_pen)
        painter.drawEllipse(616-(100)-10, 15, 100, 100)  # Qpoint placed it at the wrong position, no idea why
        _pen = QPen(QColor(c.red(), c.green(), c.blue(), 60))
        _pen.setWidth(2)
        painter.setPen(_pen)
        offset_x, offset_y = 616-(100)-10+50, 15+50
        for i in hitmap:
            painter.drawPoint((i.x*100)+offset_x,(i.y*100)+offset_y)


class _Interface(QWidget):
    def __init__(self, a, b,c):
        super(_Interface, self).__init__()
        self.renderer = _Renderer(a,b,c)

        self.layout = QGridLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.layout.addWidget(self.renderer, 0, 0, 1, 1)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)



class VisualizerWindow(QMainWindow):
    def __init__(self, a, b,c):
        super(VisualizerWindow, self).__init__()
        self.setWindowTitle("Visualizer")
        self.interface = _Interface(a,b,c)
        self.setCentralWidget(self.interface)
        img = QImage(616,192, QImage.Format_ARGB32_Premultiplied)
        painter = QPainter(img)
        self.interface.render(painter)
        painter.end()
        img.save("export.jpg")
        print("@exported png")
