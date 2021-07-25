import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog, QAction, QWidget
from PyQt5.QtGui import QIcon, QPixmap
import math
import random

#Our files
import getPointsCV2
import interpolinomial as pol
import interLagrange as lge
import intersplines as spl

#Simpy
from sympy import lambdify, Symbol

class Canvas(FigureCanvas):
    rgb = []
    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(5,3))
        super().__init__(fig)
        self.setParent(parent)
        self.ax.grid()
        self.ax.set(xlim=(0,800), ylim=(0,800))
        for i in range (50):
            self.rgb.append((random.randint(50,200)/255,random.randint(50,200)/255,random.randint(50,200)/255))
    def cleanGraph(self):
        self.ax.clear()
        self.ax.grid()
        self.ax.set(xlim=(0,800), ylim=(0,800))

    def updateGraphPonts(self, points):
        #Clear graph
        self.ax.clear()
        self.ax.grid()
        #Graph the points
        x_val = [x[0] for x in points]
        y_val = [x[1] for x in points]
        self.ax.plot(x_val,y_val,'o')
        self.ax.autoscale_view()
    
    def updateGraphInter1(self, points, visible, function, x1, polP):
        #Clear graph
        self.ax.clear()
        self.ax.grid()
        if(visible == True):
            #Graph the points
            x_val = [x[0] for x in points]
            y_val = [x[1] for x in points]
            self.ax.plot(x_val,y_val,'o', color='orange')
        # Data for plotting
        self.ax.plot(x1, function(x1), color='tab:green')
        self.ax.autoscale_view()
        # Text to print
        func = str(polP).replace("**", "^")
        msg1 = "Function({} ,{} ,{} )".format(func,points[0][0],points[len(points)-1][0])
        return msg1


    def updateGraphInter2(self, points, visible, function, x1, lagP):
        #Clear graph
        self.ax.clear()
        self.ax.grid()
        if(visible == True):
            #Graph the points
            x_val = [x[0] for x in points]
            y_val = [x[1] for x in points]
            self.ax.plot(x_val,y_val,'o', color='orange')
        # Data for plotting
        self.ax.plot(x1, function(x1), color='tab:blue')
        self.ax.autoscale_view()
        # Text to print
        func = str(lagP).replace("**", "^")
        msg2 = "Function({} ,{} ,{} )".format(func,points[0][0],points[len(points)-1][0])
        return msg2

    def updateGraphInter3(self, points, visible, function):
        #Clear graph
        self.ax.clear()
        self.ax.grid()
        if(visible == True):
            #Graph the points
            x_val = [x[0] for x in points]
            y_val = [x[1] for x in points]
            self.ax.plot(x_val,y_val,'o', color='orange')
        # Data for plotting
        x = Symbol('x')
        functionPrint = ""
        for i in range(len(function)):
            x2 = np.linspace(points[i][0], points[i + 1][0], num = 100)
            fnt = lambdify(x, function[i], 'numpy')
            #Create string function to print
            func = str(fnt(x)).replace("**", "^")
            functionPrint += "Function( {} , {}, {} ) \n".format(func,points[i][0],points[i + 1][0])
            #Graph the function
            if i == 0:
                self.ax.plot(x2, fnt(x2), color = self.rgb[i], label = "Splines")
            else:
                self.ax.plot(x2, fnt(x2), color = self.rgb[i])

        self.ax.autoscale_view()
        return functionPrint

class Ui_MainWindow(object):
    #Points from image
    points = []
    final_points = []
    nPoints = 6
    mayor = ()
    menor = ()
    mayorFinal = ()
    menorFinal = ()
    vis1 = True
    vis2 = True
    vis3 = True
    #Polinomial
    fnp = 0
    polP = 0
    ecspl = 0

    #Lagrange
    fnl = 0
    lagP = 0
    #Splines

    #Colors
    rgb = []

    #Msg
    msg1 = ""
    msg2 = ""
    msg3 = ""


    def setupUi(self, MainWindow):
        #Setup window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(230, 230, 230);")

        

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")



        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(430, 0, 450, 50))
        self.title.setStyleSheet("color:rgb(72, 73, 75); font-size:35px;")
        


        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setAutoFillBackground(False)
        self.title.setObjectName("title")

        
        ###################


        



        #Font subtitles
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(65)
        font.setPointSize(14)


        #Title load image
        self.label_original = QtWidgets.QLabel(self.centralwidget)
        self.label_original.setGeometry(QtCore.QRect(50, 55, 165, 25))
        self.label_original.setStyleSheet("color:rgb(72, 73, 75);")
        self.label_original.setFont(font)
        self.label_original.setObjectName("label_original")
        #Img load image
        self.img_original = QtWidgets.QLabel(self.centralwidget)
        self.img_original.setGeometry(QtCore.QRect(10, 80, 250, 250))
        self.img_original.setText("")
        self.img_original.setPixmap(QtGui.QPixmap("assets/imgGUI/loadImage.png"))
        self.img_original.setScaledContents(True)
        self.img_original.setObjectName("img_original")

        #Button load image
        self.buttonLoad = QtWidgets.QPushButton(self.centralwidget)
        self.buttonLoad.setGeometry(QtCore.QRect(10, 80, 250, 250))
        self.buttonLoad.setStyleSheet("background-color:transparent;")
        self.buttonLoad.setObjectName("buttonLoad")



        #Title HSV
        self.label_hsv = QtWidgets.QLabel(self.centralwidget)
        self.label_hsv.setGeometry(QtCore.QRect(330, 55, 170, 25))
        self.label_hsv.setStyleSheet("color:rgb(72, 73, 75);")
        self.label_hsv.setFont(font)
        self.label_hsv.setObjectName("label_hsv")
        #Img hsv 
        self.img_hsv = QtWidgets.QLabel(self.centralwidget)
        self.img_hsv.setGeometry(QtCore.QRect(290, 80, 250, 250))
        self.img_hsv.setText("")
        self.img_hsv.setPixmap(QtGui.QPixmap("assets/imgGUI/hsv.png"))
        self.img_hsv.setScaledContents(True)
        self.img_hsv.setObjectName("img_hsv")


        #Title Puntos
        self.label_puntos = QtWidgets.QLabel(self.centralwidget)
        self.label_puntos.setGeometry(QtCore.QRect(560, 55, 250, 20))
        self.label_puntos.setStyleSheet("color:rgb(72, 73, 75);")
        self.label_puntos.setFont(font)
        self.label_puntos.setObjectName("label_puntos")
        #Graph points puntos
        self.img_points = QtWidgets.QLabel(self.centralwidget)
        self.img_points.setGeometry(QtCore.QRect(550, 80, 250, 250))
        self.img_points.setText("")
        self.img_points.setPixmap(QtGui.QPixmap("assets/imgGUI/puntosCV2.png"))
        self.img_points.setScaledContents(True)
        self.img_points.setObjectName("img_points")


        #Font def coord
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(60)

        #Subtitles def coord X1
        self.label_x1 = QtWidgets.QLabel(self.centralwidget)
        self.label_x1.setGeometry(QtCore.QRect(825, 65, 25, 20))
        self.label_x1.setFont(font)
        self.label_x1.setObjectName("label_x1")
        #Form coord X1
        self.text_x1 = QtWidgets.QTextEdit(self.centralwidget)
        self.text_x1.setGeometry(QtCore.QRect(805, 85, 60, 31))
        self.text_x1.setStyleSheet("font-size: 15px; background:rgb(255, 255, 255);")
        self.text_x1.setObjectName("text_x1")
        
        #Subtitles def coord Y1
        self.label_y1 = QtWidgets.QLabel(self.centralwidget)
        self.label_y1.setGeometry(QtCore.QRect(825, 120, 31, 20))
        self.label_y1.setFont(font)
        self.label_y1.setObjectName("label_y1")
        #Form coord Y1
        self.text_y1 = QtWidgets.QTextEdit(self.centralwidget)
        self.text_y1.setGeometry(QtCore.QRect(805, 140, 60, 31))
        self.text_y1.setStyleSheet("font-size: 15px; background:rgb(255, 255, 255);")
        self.text_y1.setObjectName("text_y1")

        
        #Subtitles def coord X2
        self.label_x2 = QtWidgets.QLabel(self.centralwidget)
        self.label_x2.setGeometry(QtCore.QRect(825, 185, 31, 20))
        self.label_x2.setFont(font)
        self.label_x2.setObjectName("label_x2")
        #Form coord X2
        self.text_x2 = QtWidgets.QTextEdit(self.centralwidget)
        self.text_x2.setGeometry(QtCore.QRect(805, 205, 60, 31))
        self.text_x2.setStyleSheet("font-size: 15px; background:rgb(255, 255, 255);")
        self.text_x2.setObjectName("text_x2")
        #Subtitles def coord Y2
        self.label_y2 = QtWidgets.QLabel(self.centralwidget)
        self.label_y2.setGeometry(QtCore.QRect(825, 240, 31, 20))
        self.label_y2.setFont(font)
        self.label_y2.setObjectName("label_y2")
        #Form coord Y2
        self.text_y2 = QtWidgets.QTextEdit(self.centralwidget)
        self.text_y2.setGeometry(QtCore.QRect(805, 260, 60, 31))
        self.text_y2.setStyleSheet("font-size: 15px; background:rgb(255, 255, 255);")
        self.text_y2.setObjectName("text_y2")

        #Subtitles def coord Npoints
        self.label_npoints = QtWidgets.QLabel(self.centralwidget)
        self.label_npoints.setGeometry(QtCore.QRect(870, 50, 55, 20))
        self.label_npoints.setFont(font)
        self.label_npoints.setObjectName("label_npoints")
        #Form def coord Npoints
        self.text_npoints = QtWidgets.QTextEdit(self.centralwidget)
        self.text_npoints.setGeometry(QtCore.QRect(930, 45, 35, 31))
        self.text_npoints.setStyleSheet("font-size: 15px; background:rgb(255, 255, 255);")
        self.text_npoints.setObjectName("text_npoints")


        #Botón definir coordenadas
        self.buttonDefine = QtWidgets.QPushButton(self.centralwidget)
        self.buttonDefine.setGeometry(QtCore.QRect(805, 300, 60, 40))
        self.buttonDefine.setObjectName("buttonDefine")
        self.buttonDefine.setStyleSheet("background-color:rgb(102, 103, 105); color:rgb(255,255,255);")



        #Title gráfico puntos
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(70)
        self.label_grafico = QtWidgets.QLabel(self.centralwidget)
        self.label_grafico.setGeometry(QtCore.QRect(1010, 55, 171, 20))
        self.label_grafico.setStyleSheet("color:rgb(72, 73, 75);")
        self.label_grafico.setFont(font)
        self.label_grafico.setObjectName("label_grafico")

        

        
        #Graph the points matplot
        self.chart_points = Canvas(self.centralwidget)
        self.chart_points.setGeometry(QtCore.QRect(870, 80, 400, 250))
        self.chart_points.setStyleSheet("border: 1px solid rgb(72, 73, 75);")
        self.chart_points.setObjectName("chart_points")
        
        #Font Title Intepolacion
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)

        #Title interpolacion
        self.subtitle = QtWidgets.QLabel(self.centralwidget)
        self.subtitle.setGeometry(QtCore.QRect(530, 330, 190, 28))
        self.subtitle.setStyleSheet("color:rgb(72, 73, 75);")
        self.subtitle.setFont(font)
        self.subtitle.setAutoFillBackground(False)
        self.subtitle.setObjectName("subtitle")

        

        #FOnt interpolaciones
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)


        #Title interpolacion lineal
        self.label_inter1 = QtWidgets.QLabel(self.centralwidget)
        self.label_inter1.setGeometry(QtCore.QRect(130, 360, 280, 20))
        self.label_inter1.setFont(font)
        self.label_inter1.setStyleSheet("color:rgb(72, 73, 75);")
        self.label_inter1.setObjectName("label_inter1")


        self.label_inter2 = QtWidgets.QLabel(self.centralwidget)
        self.label_inter2.setGeometry(QtCore.QRect(550, 360, 280, 20))
        self.label_inter2.setFont(font)
        self.label_inter2.setStyleSheet("color:rgb(72, 73, 75);")
        self.label_inter2.setObjectName("label_inter2")

        self.label_inter3 = QtWidgets.QLabel(self.centralwidget)
        self.label_inter3.setGeometry(QtCore.QRect(940, 360, 280, 20))
        self.label_inter3.setFont(font)
        self.label_inter3.setStyleSheet("color:rgb(72, 73, 75);")
        self.label_inter3.setObjectName("label_inter3")


        #Graphs
        #Img graph interpolacion lineal
        #Graph the points matplot
        self.chart_interpol1 = Canvas(self.centralwidget)
        self.chart_interpol1.setGeometry(QtCore.QRect(20, 385, 400, 250))
        self.chart_interpol1.setStyleSheet("border: 1px solid rgb(72, 73, 75);")
        self.chart_interpol1.setObjectName("chart_points")

        #Img graph interpolacion lineal
        self.chart_interpol2 = Canvas(self.centralwidget)
        self.chart_interpol2.setGeometry(QtCore.QRect(440, 385, 400, 250))
        self.chart_interpol2.setStyleSheet("border: 1px solid rgb(72, 73, 75);")
        self.chart_interpol2.setObjectName("chart_points")


        #Img graph interpolacion lineal
        self.chart_interpol3 = Canvas(self.centralwidget)
        self.chart_interpol3.setGeometry(QtCore.QRect(860, 385, 400, 250))
        self.chart_interpol3.setStyleSheet("border: 1px solid rgb(72, 73, 75);")
        self.chart_interpol3.setObjectName("chart_points")

        #Form undergraph
        #Form equation 1
        self.text_eq1 = QtWidgets.QTextEdit(self.centralwidget)
        self.text_eq1.setGeometry(QtCore.QRect(20, 645, 400, 30))
        self.text_eq1.setStyleSheet("font-size: 15px; background:rgb(255, 255, 255);")
        self.text_eq1.setObjectName("text_eq1")

        #Form equation 2
        self.text_eq2 = QtWidgets.QTextEdit(self.centralwidget)
        self.text_eq2.setGeometry(QtCore.QRect(440, 645, 400, 30))
        self.text_eq2.setStyleSheet("font-size: 15px; background:rgb(255, 255, 255);")
        self.text_eq2.setObjectName("text_eq2")

        #Form equation 3
        self.text_eq3 = QtWidgets.QTextEdit(self.centralwidget)
        self.text_eq3.setGeometry(QtCore.QRect(860, 645, 400, 30))
        self.text_eq3.setStyleSheet("font-size: 15px; background:rgb(255, 255, 255);")
        self.text_eq3.setObjectName("text_eq3")
        

        #Button procesar interpolaciones
        self.buttonProcessInterpol = QtWidgets.QPushButton(self.centralwidget)
        self.buttonProcessInterpol.setGeometry(QtCore.QRect(710, 332, 30, 30))
        self.buttonProcessInterpol.setStyleSheet("background-color:rgb(102, 103, 105);")
        self.buttonProcessInterpol.setObjectName("buttonProcessInterpol")

        #Buttons visibility points
        #Button visib interpol1
        self.buttonVisInter1 = QtWidgets.QPushButton(self.centralwidget)
        self.buttonVisInter1.setGeometry(QtCore.QRect(395, 355, 25, 25))
        self.buttonVisInter1.setStyleSheet("background-color:rgb(102, 103, 105);")
        self.buttonVisInter1.setObjectName("buttonVisInter1")

        #Button visib interpol2
        self.buttonVisInter2 = QtWidgets.QPushButton(self.centralwidget)
        self.buttonVisInter2.setGeometry(QtCore.QRect(815, 355, 25, 25))
        self.buttonVisInter2.setStyleSheet("background-color:rgb(102, 103, 105);")
        self.buttonVisInter2.setObjectName("buttonVisInter2")

        #Button visib interpol3
        self.buttonVisInter3 = QtWidgets.QPushButton(self.centralwidget)
        self.buttonVisInter3.setGeometry(QtCore.QRect(1235, 355, 25, 25))
        self.buttonVisInter3.setStyleSheet("background-color:rgb(102, 103, 105);")
        self.buttonVisInter3.setObjectName("buttonVisInter3")

       
        #Set MainWindow
        MainWindow.setCentralWidget(self.centralwidget)


        #Top menubat
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 21))
        self.menubar.setStyleSheet("background-color:rgb(102, 103, 105); color:rgb(255,255,255);")
        self.menubar.setObjectName("menubar")
        #Menu archivo
        self.menuArchivo = QtWidgets.QMenu(self.menubar)
        self.menuArchivo.setObjectName("menuArchivo")
        #Add menubar to mainWindow
        MainWindow.setMenuBar(self.menubar)

        

        #Load Image
        self.actionLoad_Image = QtWidgets.QAction(MainWindow)
        self.actionLoad_Image.setObjectName("actionLoad_Image")
        self.menuArchivo.addAction(self.actionLoad_Image)

        #Export functions
        self.exportFunction = QtWidgets.QAction(MainWindow)
        self.exportFunction.setObjectName("exportFunction")
        self.menuArchivo.addAction(self.exportFunction)

        
        self.menubar.addAction(self.menuArchivo.menuAction())


        #Lines that start all
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #Actions

        #Load Image
        self.actionLoad_Image.triggered.connect(self.loadImage)
        self.buttonLoad.clicked.connect(self.loadImage)

        #Exportar funciones
        self.exportFunction.triggered.connect(self.exportFunc)

        #PressButton Define points
        self.buttonDefine.clicked.connect(self.calcPoints)
        #Process Interpolacion
        self.buttonProcessInterpol.clicked.connect(self.processInterpolation)

        #PressButton vis1
        self.buttonVisInter1.clicked.connect(self.changeVis1)
        #PressButton vis2
        self.buttonVisInter2.clicked.connect(self.changeVis2)
        #PressButton vis3
        self.buttonVisInter3.clicked.connect(self.changeVis3)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Proyecto Metodos Numericos 2021-I       Interpolador"))
        self.title.setText(_translate("MainWindow", "Proyecto métodos 2021-I"))
        self.label_original.setText(_translate("MainWindow", "Imagen original"))
        self.label_hsv.setText(_translate("MainWindow", "Imagen BGR2HSV"))
        self.label_puntos.setText(_translate("MainWindow", "Puntos encontrados: ",))
        self.label_grafico.setText(_translate("MainWindow", "Gráfico de puntos"))
        self.subtitle.setText(_translate("MainWindow", "Interpolación"))
        self.label_inter1.setText(_translate("MainWindow", "Interpolación polinomial"))
        self.buttonDefine.setText(_translate("MainWindow", "Def"))
        self.label_inter2.setText(_translate("MainWindow", "Interpolación Lagrange"))
        self.label_inter3.setText(_translate("MainWindow", "Interpolación por splines"))
        self.label_x1.setText(_translate("MainWindow", "X1:"))
        self.label_y1.setText(_translate("MainWindow", "Y1:"))
        self.label_x2.setText(_translate("MainWindow", "X2:"))
        self.label_y2.setText(_translate("MainWindow", "Y2:"))
        self.label_npoints.setText(_translate("MainWindow", "# puntos:"))
        self.menuArchivo.setTitle(_translate("MainWindow", "Archivo"))
        self.actionLoad_Image.setText(_translate("MainWindow", "Cargar imagen"))
        self.exportFunction.setText(_translate("MainWindow", "Exportar funciones"))

        #Button Define points
        pixmap = QPixmap("assets/imgGUI/coordinate_system_100px.png")
        self.buttonDefine.setIcon(QIcon(pixmap))
        #Button process
        pixmap = QPixmap("assets/imgGUI/services_60px.png")
        self.buttonProcessInterpol.setIcon(QIcon(pixmap))
        #Button visi 1 2 3
        pixmap = QPixmap("assets/imgGUI/eye_52px.png")
        self.buttonVisInter1.setIcon(QIcon(pixmap))
        self.buttonVisInter2.setIcon(QIcon(pixmap))
        self.buttonVisInter3.setIcon(QIcon(pixmap))
    #Methods
    def loadImage(self):
        pixmap = QPixmap("assets/imgGUI/loadImage.png")
        self.img_original.setPixmap(pixmap)
        pixmap = QPixmap("assets/imgGUI/hsv.png")
        self.img_hsv.setPixmap(pixmap)
        pixmap = QPixmap("assets/imgGUI/hsv.png")
        self.img_hsv.setPixmap(pixmap)
        pixmap = QPixmap("assets/imgGUI/puntosCV2.png")
        self.img_points.setPixmap(pixmap)
        #Get image path
        imagePath, _ = QFileDialog.getOpenFileName()
        #Get points, mayor y menor
        self.points, self.menor, self.mayor = getPointsCV2.getPointsImage(imagePath)
        if (type(self.points) is list):
            #Load image
            pixmap = QPixmap(imagePath)
            self.img_original.setPixmap(pixmap)
            pixmap = QPixmap("assets/imgMod/hsv.jpeg")
            self.img_hsv.setPixmap(pixmap)
            pixmap = QPixmap("assets/imgMod/points.jpeg")
            self.img_points.setPixmap(pixmap)
            self.label_puntos.setText("Puntos encontrados:  " + str(len(self.points)))
        else:
            pixmap = QPixmap("assets/imgGUI/error_load.png")
            self.img_original.setPixmap(pixmap)
            pixmap = QPixmap("assets/imgGUI/error_load.png")
            self.img_hsv.setPixmap(pixmap)
            pixmap = QPixmap("assets/imgGUI/error_load.png")
            self.img_points.setPixmap(pixmap)

    #Calculate points to graph
    def calcPoints(self): 
        if (type(self.points) is list and len(self.points)>0): 
            self.mayorFinal = self.mayor
            self.menorFinal = self.menor
            #Calc number of points
            if(self.text_npoints.toPlainText() == "" or (int(self.text_npoints.toPlainText())<4)):
                self.nPoints = 6
                if (self.text_x1.toPlainText() != "" and self.text_y1.toPlainText() != "" and self.text_x2.toPlainText() != "" and self.text_y2.toPlainText() != "" ):
                    self.nPoints = self.nPoints-1
            elif (int(self.text_npoints.toPlainText())>len(self.points)):
                self.nPoints = len(self.points)
            else:
                self.nPoints = int(self.text_npoints.toPlainText())
                if (self.text_x1.toPlainText() != "" and self.text_y1.toPlainText() != "" and self.text_x2.toPlainText() != "" and self.text_y2.toPlainText() != "" ):
                    self.nPoints = self.nPoints-1
            #Set jumpSize
            inPoint = len(self.points)
            numPoints = self.nPoints - 1
            while (inPoint % (numPoints) != 0):
                inPoint = inPoint-1
            jumpSize = int(inPoint/numPoints)
            self.final_points = self.points[0:inPoint:jumpSize]
            self.final_points.append(self.points[len(self.points)-1])

            if (self.text_x1.toPlainText() != "" and self.text_y1.toPlainText() != "" and self.text_x2.toPlainText() != "" and self.text_y2.toPlainText() != "" ):
                if(self.text_x1.toPlainText() != self.text_x2.toPlainText()):
                    self.mayorFinal = (float(self.text_x1.toPlainText()),float(self.text_y1.toPlainText()))
                    self.menorFinal = (float(self.text_x2.toPlainText()),float(self.text_y2.toPlainText()))
                    self.final_points = getPointsCV2.transformPoints(self.final_points, self.menor,self.mayor,self.mayorFinal,self.menorFinal)
            #Update the graph of points
            self.chart_points.updateGraphPonts(self.final_points)
            self.chart_points.draw()
        else:
            self.chart_points.cleanGraph()
            self.chart_points.draw()
    
    def processInterpolation(self):
        if (type(self.final_points) is list and len(self.final_points)>0): 
            #Set vis to true
            self.vis1 = True
            self.vis2 = True
            self.vis3 = True
            #Set points
            x = Symbol('x')
            self.x1 = np.linspace(self.final_points[0][0], self.final_points[len(self.final_points) - 1][0], num = 100)

            #Interpol 1
            self.polP = pol.polinomial(self.final_points)
            self.fnp = lambdify(x, self.polP, 'numpy')
            self.msg1 = self.chart_interpol1.updateGraphInter1(self.final_points, self.vis2, self.fnp, self.x1, self.polP)
            self.chart_interpol1.draw()
            self.text_eq1.setText(self.msg1)

            #Interpol 2
            self.lagP = lge.lagrange(self.final_points)
            self.fnl = lambdify(x, self.lagP, 'numpy')
            self.msg2 = self.chart_interpol2.updateGraphInter2(self.final_points, self.vis2, self.fnl, self.x1, self.lagP)
            self.chart_interpol2.draw()
            self.text_eq2.setText(self.msg2)

            #Interpol 3
            self.ecspl = spl.splines(self.final_points)
            self.msg3 = self.chart_interpol3.updateGraphInter3(self.final_points, self.vis3, self.ecspl)
            self.chart_interpol3.draw()
            self.text_eq3.setText(self.msg3)
        else:
            #Interpol 1
            self.chart_interpol1.cleanGraph()
            self.chart_interpol1.draw()
            #Interpol 2
            self.chart_interpol2.cleanGraph()
            self.chart_interpol2.draw()
            #Interpol 3
            self.chart_interpol3.cleanGraph()
            self.chart_interpol3.draw()
        
    def changeVis1(self):
        if (type(self.final_points) is list and len(self.final_points)>0): 
            self.vis1 = not self.vis1
            self.chart_interpol1.updateGraphInter1(self.final_points, self.vis1, self.fnp, self.x1, self.polP)
            self.chart_interpol1.draw()

    def changeVis2(self):
        if (type(self.final_points) is list and len(self.final_points)>0): 
            self.vis2 = not self.vis2
            self.chart_interpol2.updateGraphInter2(self.final_points, self.vis2, self.fnl, self.x1, self.lagP)
            self.chart_interpol2.draw()

    def changeVis3(self):
        if (type(self.final_points) is list and len(self.final_points)>0): 
            self.vis3 = not self.vis3
            self.chart_interpol3.updateGraphInter3(self.final_points, self.vis3, self.ecspl)
            self.chart_interpol3.draw()

    def exportFunc(self):
        if(self.msg1 != "" and self.msg2 != "" and self.msg3 != ""):
            #Erasing all inside document
            open('funciones.txt', 'w').close()
            # Opening and Closing  "funciones.txt"
            file1 = open("funciones.txt","a")

            L = ["                              Proyecto métodos numéricos 2021-1\n","                              ------------------------------------ \n","\n",
            "Proyecto realizado por: \n","      Nicolás Darío Mejía Borda \n","     Juan Sebastián Rodríguez Castellanos\n",
            "\n","\n","Las funciones que se muestran a continuación se pueden graficar distintas aplicaciones, como por ejemplo Geogebra.","\n","\n"
            ] 
            file1.writelines(L)
            file1.write("\n\n\nInterpolación polinomial: \n\n{}\n".format(self.msg1))
            file1.write("\n\nInterpolación Lagrange: \n\n{}\n".format(self.msg2))
            file1.write("\n\nInterpolación por Splines: \n\n{}\n".format(self.msg3))
            file1.close()
        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
