#==============================================================
# Librería para una visualización rápida del controlador CLAU
#==============================================================

import sys, time
import numpy as np 
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from scipy.spatial.transform import Rotation as R
from .clau import Clau


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
        axis.setSize(3, 3, 3)
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
        colors = np.array([[0,1,1,1] for _ in range(len(faces))])  # rojo

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

def cube_view(port="COM5", n_data=10, clk=115200, logs=True):
    app = QtWidgets.QApplication(sys.argv)
    win = CubeViewer()
    win.resize(600, 600)
    win.show()

    #Calibración y conexión con el clau
    clau_obj = Clau(port, n_data)
    clau_obj.set_clk(clk)
    calibrate = clau_obj.calibrate()
    print("status:", calibrate["status"])

    def animate():
        data = clau_obj.collect_data()
        if data is None:
            return  # esperar siguiente frame

        pos = [2,2,2] #data["position"]
        q = data["quaternion"]

        if logs: print("cuat:", q)
        win.set_transform(pos, q)

    timer = QTimer()
    timer.timeout.connect(animate)
    timer.start(11)

    sys.exit(app.exec_())

    app = QtWidgets.QApplication(sys.argv)
    win = CubeViewer()
    win.resize(600, 600)
    win.show()

    # Calibración y conexión con el clau
    clau_obj = ClauBNO055(port, n_data)
    clau_obj.set_clk(clk)
    clau_obj.set_shake_umbral(umbral)
    calibrate = clau_obj.calibrate()
    print("status:", calibrate["status"])

    # Variables para animación suave
    animation_active = False
    animation_start = 0.0
    animation_duration = 2.0  # segundos (ida y vuelta)
    animation_direction = np.array([0.0, 0.0, 0.0])

    def animate():
        nonlocal animation_active, animation_start, animation_direction

        data = clau_obj.collect_data()
        if data is None:
            return  # esperar siguiente frame

        q = data["quaternion"]
        shake = clau_obj.get_shake()
        acc = np.array([0.0, 0.0, 0.0])

        # Si se detecta agitación y no hay animación en curso
        if shake["shakeStatus"] and not animation_active:
            direction = np.array(shake["shakeDirection"], dtype=float)
            mag = np.linalg.norm(direction)
            if mag > 0:
                direction /= mag  # normalizar dirección
                animation_direction = direction
                animation_start = time.time()
                animation_active = True
                if logs:
                    print(f"Animación iniciada hacia: {direction}")

        # Si hay animación activa
        if animation_active:
            elapsed = time.time() - animation_start
            t = elapsed / animation_duration

            if t >= 1.0:
                # Termina la animación
                animation_active = False
                acc = np.array([0.0, 0.0, 0.0])
            else:
                # Movimiento suave de ida y vuelta (forma de media onda)
                phase = np.sin(np.pi * t)
                distance = 0.5  # escala de desplazamiento (ajustable)
                acc = animation_direction * distance * phase

        win.set_transform(acc, q)

    # Timer de actualización (~90 FPS)
    timer = QTimer()
    timer.timeout.connect(animate)
    timer.start(11)

    sys.exit(app.exec_())