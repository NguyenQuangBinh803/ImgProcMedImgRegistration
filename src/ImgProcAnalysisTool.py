import os
import sys
import cv2
import numpy as np
import pydicom
import urllib

from PIL import Image, ImageQt
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtOpenGL import *


class ImagesWidgetItem(QTreeWidgetItem):
    def __init__(self, parent, name, icon_path):
        super().__init__(parent)
        self.setText(0, name)
        self.setIcon(0, QtGui.QIcon(icon_path))
        self.parameters = []
    
    def configure_parameters(self):
        # Display dialog configure and write value to attrib
        pass

class Window(QtWidgets.QMainWindow, uic.loadUiType(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../ui/ImgProcAnalysisTool.ui"))[0]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.title = "Image Processing Analysis System"
        
        self.init_attributes()
        print("[INITIALIZATION] COMPLETE INIT SYSTEM ATTRIBUTES")
        self.init_components()
        print("[INITIALIZATION] COMPLETE INIT SYSTEM COMPONENTS")
        self.init_operations()
        print("[INITIALIZATION] COMPLETE INIT SYSTEM OPERATIONS")
        self.show()
        print("[INITIALIZATION] SYSTEM ONLINE .................")
        

    def init_attributes(self):
        self.mouse_position = [150, 150]
        self.original_image = cv2.imread("../rsrc/images/1.jpg", 0)
        # self.currents_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        self.currents_image = self.original_image.copy()
        self.previous_image = [self.currents_image.copy()]

        self.regionoi_sizes = 25
        self.investig_sizes = 100
        self.image_scale    = 1
        self.image_views    = True

    def init_components(self):
        self.setWindowTitle(self.title)
        self.label_6.setAcceptDrops(True)
        self.label_6.setAlignment(QtCore.Qt.AlignLeft)
        # self.label_6.setMouseTracking(True)
        # self.label_6.mouseMoveEvent = self.execute_investig
        self.label_6.wheelEvent     = self.execute_zoomevnt
        self.label_6.dragEnterEvent = self.execute_dragevnt
        self.label_6.dropEvent      = self.execute_dropevnt

        self.tableWidget.setRowCount(self.regionoi_sizes) 
        self.tableWidget.setColumnCount(self.regionoi_sizes)  
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()

        self.treeWidget.setHeaderHidden(True)
        self.tree_item = ImagesWidgetItem(self.treeWidget, "Image Layer 1", "../rsrc/icons/image.ico")
        

    def init_operations(self):
        self.updates_original(self.currents_image)
        

    def execute_kernel_clicked(self):
        print(self.treeWidget.selectedItems())


    def execute_paracfig(self, item):
        pass

    def execute_dragevnt(self, event):
        if event.mimeData().hasImage() or event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def execute_dropevnt(self, event):
        if event.mimeData().hasImage() :
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            # print(file_path)
            self.original_image = cv2.imread(file_path)
            self.previous_image.append(self.currents_image.copy())
            self.currents_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            event.accept()

        elif event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            # print(file_path)
            if os.path.basename(file_path).split(".")[-1] == "dcm":
                file = pydicom.dcmread(file_path, force=True)
                file.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
                self.original_image = ((file.pixel_array * 2**(file.BitsAllocated - file.BitsStored))/256).astype('uint8')
                self.previous_image.append(self.currents_image.copy())
                self.currents_image = self.original_image.copy()
            else:
                try:
                    # print(event.mimeData().urls()[0].toString())
                    req = urllib.request.urlopen(event.mimeData().urls()[0].toString())
                    self.original_image = cv2.imdecode(np.asarray(bytearray(req.read()), dtype=np.uint8), -1)
                    self.previous_image.append(self.currents_image.copy())
                    if len(self.original_image.shape) > 2:
                        self.currents_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
                    else:
                        self.currents_image = self.original_image.copy()
                    event.accept()
                except Exception as exp:
                    pass
        else:
            event.ignore()
        self.init_operations()

    def execute_zoomevnt(self, event):
        delta = event.angleDelta().y()
        x = (delta and delta // abs(delta))
        if not self.image_views:
            return
        else:
            self.investig_sizes += x*10
            if self.investig_sizes > 500:
                self.investig_sizes = 500
            elif self.investig_sizes < 10:
                self.investig_sizes = 10

            input_image = self.currents_image[  self.mouse_position[1] - self.investig_sizes//2 : self.mouse_position[1] + self.investig_sizes//2,
                                                self.mouse_position[0] - self.investig_sizes//2 : self.mouse_position[0] + self.investig_sizes//2].copy()

            input_image = cv2.resize(input_image, (0,0), fx=self.label_6.size().height()/input_image.shape[0], 
                                                fy=self.label_6.size().height()/input_image.shape[0])
            
            disp_image = self.currents_image.copy()
            
            if len(disp_image.shape) == 2:
                disp_image = cv2.cvtColor(disp_image, cv2.COLOR_GRAY2BGR)
            
            cv2.rectangle(disp_image,   (self.mouse_position[0] - self.investig_sizes//2, self.mouse_position[1] - self.investig_sizes//2),
                                        (self.mouse_position[0] + self.investig_sizes//2, self.mouse_position[1] + self.investig_sizes//2),
                                        (0,255,0), 2)
            self.updates_original(disp_image)
            img = Image.fromarray(input_image)
            self.label.setPixmap(QtGui.QPixmap.fromImage(ImageQt.ImageQt(img).copy()))

    def execute_switch_view(self):
        self.image_views = not self.image_views
        

    def process_image(self):
        inputs_image = self.original_image.copy()
        for i in range(self.tree_item.childCount()):
            result_image = self.tree_item.child(i).kernel_execute(inputs_image)
            inputs_image = result_image.copy()
        
        self.previous_image.append(self.currents_image.copy())
        self.currents_image = result_image.copy()
        

    def updates_original(self, input_image):
        input_image_height, input_image_width = input_image.shape[:2]
        if input_image_height > input_image_width:
            self.image_scale = self.label_6.size().height()/input_image_height
        else:
            self.image_scale = self.label_6.size().height()/input_image_width
            
        img = cv2.resize(input_image, (0,0), fx=self.image_scale, fy=self.image_scale)
        img = Image.fromarray(img)
        self.label_6.setPixmap(QtGui.QPixmap.fromImage(ImageQt.ImageQt(img).copy()))

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key()==(Qt.Key_Control and Qt.Key_Z):
            if len(self.previous_image) > 1:
                self.currents_image = self.previous_image.pop()
                self.updates_original(self.currents_image)
                
        elif e.key() == Qt.Key_Delete and self.treeWidget.selectedItems() is not None:
            for item in self.treeWidget.selectedItems():
                self.tree_item.removeChild(item)
            self.process_image()
            disp_image = self.currents_image.copy()
            self.updates_original(disp_image)
            
            
        # elif e.key()==(Qt.Key_Control and Qt.Key_Y):

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    clipboard = app.clipboard()
    main_window = Window()
    app.exec_()
    sys.exit()
