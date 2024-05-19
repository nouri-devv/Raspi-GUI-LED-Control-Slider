from gpiozero import PWMLED
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QLabel
from PyQt5.QtCore import Qt

# Define the LED pins and initialize PWMLED objects
LED_PINS = {
    'green': 17,  # GPIO pin for the green LED
    'red': 27,    # GPIO pin for the red LED
    'blue': 22    # GPIO pin for the blue LED
}
# Create a dictionary of PWMLED objects for each color linked to its respective GPIO pin
leds = {color: PWMLED(pin) for color, pin in LED_PINS.items()}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 400, 300)  # Set the window size and position
        self.setWindowTitle("LED Brightness Control")  # Set the window title
        self.initUI()  # Initialize the user interface

    def initUI(self):
        y_position = 50  # Starting position for the first slider
        for color in LED_PINS.keys():
            slider = QSlider(Qt.Horizontal, self)
            slider.setGeometry(100, y_position, 200, 30)  # Position and size of the slider
            slider.setMinimum(0)  # Minimum value of the slider
            slider.setMaximum(100)  # Maximum value of the slider
            slider.setValue(0)  # Initial value of the slider
            
            # Connect the slider's valueChanged signal to a lambda function that updates LED intensity
            slider.valueChanged.connect(lambda value, col=color: self.update_led_intensity(col, value / 100.0))

            label = QLabel(self)
            label.setText(f"{color.capitalize()} LED:")  # Set the label text for each LED
            label.move(10, y_position)  # Position the label

            y_position += 50  # Increment the position for the next slider

    def update_led_intensity(self, color, value):
        leds[color].value = value  # Update the LED intensity

    def closeEvent(self, event):
        # Turn off all LEDs when the application is closed
        for led in leds.values():
            led.close()
        event.accept()

def main():
    app = QApplication(sys.argv)  # Create a QApplication instance
    window = MainWindow()  # Create the main window
    window.show()  # Show the main window
    sys.exit(app.exec_())  # Start the application event loop

if __name__ == '__main__':
    main()
