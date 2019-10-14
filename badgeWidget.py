
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPointF
from PyQt5.QtWidgets import QWidget, QMainWindow, QGridLayout, QSlider, QPushButton, QShortcut, QLabel
from PyQt5.QtGui import QColor, QPainterPath, QPainter, QPen, QKeySequence, QIcon, QPalette, QBrush, QFont, QPixmap, QImage

class _Renderer(QWidget):

    def __init__(self, score_info, bmap_info, user_info, graph, hitmap):
        super(_Renderer, self).__init__()  
        self.graph = graph
        self.score_info = score_info
        self.bmap_info = bmap_info
        self.user_info = user_info
        self.hitmap = hitmap
        self.setFixedSize(616,192)  # stollen from some banner site
        self.update()

    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.painter.setRenderHint(QPainter.HighQualityAntialiasing)
        self.painter.setRenderHint(QPainter.TextAntialiasing, True)
        self.painter.setRenderHint(QPainter.Antialiasing, True)
        self.painter.setPen(QPen(QColor(0, 0, 0, 180)))
        index = 0
        # background
        pixmap = QPixmap(f"Covers/{self.bmap_info['beatmapset_id']}.jpg")
        self.painter.drawPixmap(0,0,616,192, pixmap)
        for i in self.graph:
            index += 1
            self.draw_bar(i, index)
        self.draw_hitmap()        
        self.draw_info()

    def draw_bar(self, size, index):
        sliderbody = QPainterPath()

        _pen = self.painter.pen()
        _pen.setWidth(13)
        _pen.setCapStyle(Qt.RoundCap)
        _pen.setJoinStyle(Qt.RoundJoin)
        sliderbody.moveTo(5+20*index, 192-20)
        if size >= 0.01:
            sliderbody.lineTo(5+20*index, 192-20- ((192-120)*size))
        else:
            sliderbody.lineTo(5+20*index, 192-20+0.01)


        self.painter.setPen(_pen)
        self.painter.drawPath(sliderbody)

    def draw_info(self):
        _pen = QPen(QColor(0, 0, 0, 180))
        _pen.setWidth(0)
        self.painter.setPen(_pen)
        self.painter.setBrush(QBrush(QColor(0, 0, 0, 180)))

        score_info = self.score_info

        _pen = self.painter.pen()
        kek = QPainterPath()

        bmap_artist = self.bmap_info["artist"]
        bmap_title = self.bmap_info["title"]
        bmap_creator = self.bmap_info["creator"]
        bmap_diff = self.bmap_info["version"]

        username = self.user_info["username"]

        kek.addText(15, 30,QFont("Exo 2", pointSize=20, weight=500), bmap_title)
        kek.addText(352, 30, QFont("Exo 2", pointSize=10, weight=500), bmap_diff)
        kek.addText(15, 55, QFont("Exo 2", pointSize=15, weight=500), f'{score_info["count100"]}x100 | {score_info["count50"]}x50 | {score_info["countmiss"]}x0 | mods:NC')
        acc = round(((int(score_info["count300"])*300) + (int(score_info["count100"])*100) + (int(score_info["count50"])*50)) / ( 300 * (int(score_info["count300"]) + int(score_info["count50"]) + int(score_info["count100"])) )*100,2)
        kek.addText(15, 80, QFont("Exo 2", pointSize=15, weight=500),f'{score_info["maxcombo"]}x/625x | {acc}% | played by {username}')
        score_info["pp"] = round(float(score_info["pp"]),2) if not score_info["pp"] == None else 0
        kek.addText(365, 192-15, QFont("Exo 2", pointSize=38, weight=500, italic=True), f'{score_info["pp"]}PP')  # {round(float(score_info["pp"]),2)}
        kek.addText(533- (20 if len(score_info["rank"]) == 2 else 0), 90, QFont("Exo 2", pointSize=55, weight=800), score_info["rank"] if score_info["rank"] != "SH" else "S+")
        self.painter.drawPath(kek)
        self.painter.end()
    
    def draw_hitmap(self):
        _pen = self.painter.pen()
        c = _pen.color()
        _pen = QPen(QColor(c.red(), c.green(), c.blue(), 20))
        _pen.setWidth(0)
        self.painter.setBrush(QBrush(QColor(c.red(), c.green(), c.blue(), 30)))
        self.painter.setPen(_pen)
        self.painter.drawEllipse(616-(100)-10, 15, 100, 100)  # Qpoint placed it at the wrong position, no idea why
        _pen = QPen(QColor(c.red(), c.green(), c.blue(), 60))
        _pen.setWidth(2)
        self.painter.setPen(_pen)
        offset_x, offset_y = 616-(100)-10+50, 15+50
        for i in self.hitmap:
            self.painter.drawPoint((i.x*100)+offset_x,(i.y*100)+offset_y)


class _Interface(QWidget):
    def __init__(self, a, b, c, d, e):
        super(_Interface, self).__init__()
        self.renderer = _Renderer(a,b,c,d,e)

        self.layout = QGridLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.layout.addWidget(self.renderer, 0, 0, 1, 1)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)



class VisualizerWindow(QMainWindow):
    def __init__(self, a, b, c, d, e):
        super(VisualizerWindow, self).__init__()
        self.setWindowTitle("Visualizer")
        self.interface = _Interface(a,b,c,d,e)
        self.setCentralWidget(self.interface)
        img = QImage(616,192, QImage.Format_ARGB32_Premultiplied)
        painter = QPainter(img)
        self.interface.render(painter)
        painter.end()
        img.save("export.jpg")
        print("@exported png")
