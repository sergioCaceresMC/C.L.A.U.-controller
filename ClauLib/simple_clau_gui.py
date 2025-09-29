#==============================================================
# Librería para una visualización rápida del controlador CLAU
#==============================================================

import sys
import numpy as np 
from PyQt5 import QtWidgets
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from scipy.spatial.transform import Rotation as R
from clau import Clau


class CubeViewer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        # Vista 3D
        self.view = gl.GLViewWidget()
        self.view.opts['distance'] = 10
        self.layout.addWidget(self.view)

        # Ejes de referencia
        axis = gl.GLAxisItem()
        axis.setSize(2, 2, 2)
        self.view.addItem(axis)

        # Crear el cubo
        verts = np.array([
            [-1, -1, -1],
            [ 1, -1, -1],
            [ 1,  1, -1],
            [-1,  1, -1],
            [-1, -1,  1],
            [ 1, -1,  1],
            [ 1,  1,  1],
            [-1,  1,  1],
        ])
        faces = np.array([
            [0,1,2], [0,2,3],  # abajo
            [4,5,6], [4,6,7],  # arriba
            [0,1,5], [0,5,4],  # frente
            [2,3,7], [2,7,6],  # atrás
            [1,2,6], [1,6,5],  # derecha
            [0,3,7], [0,7,4],  # izquierda
        ])
        colors = np.array([[1,0,0,1] for _ in range(len(faces))])  # rojo

        self.mesh = gl.GLMeshItem(vertexes=verts, faces=faces, faceColors=colors, smooth=False, drawEdges=True)
        self.view.addItem(self.mesh)

        # Timer para animación
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_cube)
        self.timer.start(16)  # 20 fps

        # Variables de estado
        self.position = np.array([0, 0, 0])
        self.quaternion = np.array([1.0, 0.0, 0.0, 0.0])  # w,x,y,z

    def set_transform(self, position, quaternion):
        # Actualizar posición y orientación desde fuera
        self.position = np.array(position)
        self.quaternion = np.array(quaternion)

    def update_cube(self):
        # Rotación desde quaternion
        r = R.from_quat(self.quaternion)  # [x, y, z, w] en scipy
        rot_matrix = r.as_matrix()

        # Transformación homogénea 4x4
        transform = np.eye(4)
        transform[:3,:3] = rot_matrix
        transform[:3, 3] = self.position

        self.mesh.resetTransform()
        self.mesh.setTransform(pg.Transform3D(transform))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = CubeViewer()
    win.resize(600, 600)
    win.show()
    #Calibración y conexión con el clau
    clau_obj = Clau(port="COM5",n_data=10)
    calibrate = clau_obj.calibrate()
    print("status:", calibrate["status"])
    
    from PyQt5.QtCore import QTimer

    def animate():
        global clau_obj
        data = clau_obj.collect_data()
        if data is None:
            return  # esperar siguiente frame

        pos = data["position"] #data["position"]
        q = data["quaternion"]

        print("cuat:", q)
        win.set_transform([pos[0], pos[1],0], q)

    timer = QTimer()
    timer.timeout.connect(animate)
    timer.start(11)

    sys.exit(app.exec_())
