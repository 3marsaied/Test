import socket
import json
import requests
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from collections import deque
from threading import Thread
from pyqtgraph.dockarea import *


class MedicalDataServer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.temperature_values = deque(maxlen=500)
        self.received_data = {"patient_id": "1", "heart_rate": []}
        self.searchId = QLineEdit("1")
        self.searchId.setPlaceholderText("Patient ID")

        self.figure = Figure(facecolor='black')
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111, facecolor='black')
        self.ax.set_xlabel('Time', color='white')
        self.ax.set_title('Real-time Heart Rate (BPM) Plot', color='white')
        self.ax.grid()
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.tick_params(axis='x', colors='white', labelsize=6.5)
        self.ax.tick_params(axis='y', colors='white', labelsize=6.5)
        self.figure.subplots_adjust(
            left=0.1, right=0.99, top=0.92, bottom=0.1)

        # setting title
        self.setWindowTitle("ICU monitor")

        # UI contents

        self.initUI()

    def initUI(self):
        """Window GUI contents"""
        wid = QWidget(self)
        self.setGeometry(120, 80, 800, 600)
        self.setStyleSheet("background-color:#B6D0E2")
        self.setCentralWidget(wid)

        # big Layout
        outerLayout = QVBoxLayout()
        # Create a layout for the plots

        graphsLayout = QHBoxLayout()

        # Create an empty line for the plot
        self.line, = self.ax.plot([], [], color='#7CFC00')

        # Initialize empty lists for x and y data
        self.x_data = []
        self.y_data = []

        # Read and plot temperature values continuously
        self.timer = self.canvas.new_timer(interval=2020)
        self.timer.add_callback(self.update_plot)
        self.timer.start()

        graphsLayout.addWidget(self.canvas)

        outerLayout.addLayout(graphsLayout)
        outerLayout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Expanding))

        # Create a layout for the main buttons
        mainButtonsLayout = QHBoxLayout()
        name = QLabel("Patient Name: ")
        name.setStyleSheet(
            "color: black; font-size: 18px;"
        )

        mainButtonsLayout.addSpacerItem(
            QSpacerItem(200, 10, QSizePolicy.Expanding))

        # mainButtonsLayout.addWidget(downSpeedBtn,2)
        mainButtonsLayout.addSpacerItem(
            QSpacerItem(200, 10, QSizePolicy.Expanding))

        mainButtonsLayout.addWidget(self.searchId)
        # give this dock the minimum possible size
        plotArea = Dock("Plot", size=(1, 1))

        plotArea.hideTitleBar()
        outerLayout.addLayout(mainButtonsLayout, 1)

        wid.setLayout(outerLayout)

    def update_plot(self):
        # Fetch data from the database based on patient_id
        patient_id = int(self.searchId.text())
        received_data = self.fetch_data_from_database(patient_id)

        # Extract heart rate data from received data
        heart_rates = received_data["heart_rate"]
        if heart_rates:
            heart_rate = heart_rates[-1]  # Get the last value from the array
        else:
            heart_rate = 0

        # Update deque with new heart rate value
        self.temperature_values.append(heart_rate)

        # Update x and y data for the plot
        self.x_data = list(range(len(self.temperature_values)))
        self.y_data = list(self.temperature_values)

        # Update the plot
        self.line.set_xdata(self.x_data)
        self.line.set_ydata(self.y_data)

        x_range = 50
        if len(self.x_data) < x_range:
            self.ax.set_xlim(0, x_range)
        else:
            self.ax.set_xlim(
                min(self.x_data[-x_range:]), max(self.x_data[-x_range:]))

        self.ax.relim()
        self.ax.autoscale_view()

        # Draw the plot
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def fetch_data_from_database(self, patient_id):
        url = f"https://test-bjyo.onrender.com/get_data/{patient_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching data: {e}")
            return {"patient_id": patient_id, "heart_rate": []}

    def exit(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Exit the application")
        dlg.setText("Are you sure you want to exit the application ?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        button = dlg.exec()

        if button == QMessageBox.Yes:
            sys.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    server = MedicalDataServer()
    server.show()
    sys.exit(app.exec_())
