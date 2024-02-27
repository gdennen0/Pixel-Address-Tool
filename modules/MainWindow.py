from PyQt5.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QMainWindow, QWidget


class MainWindow(QMainWindow):
    """
    Main window class for the Pixel Address Finder application.

    This class sets up the main window and its layout, including input fields for channel offset,
    pixel count, and channels per pixel, as well as buttons for selecting files and running the program.
    """

    def __init__(self, main_controller):
        """
        Initializes the main window.

        Args:
            main_controller: The main controller instance to handle logic and events.
        """
        super().__init__()
        self.setWindowTitle("Pixel Address Finder")
        self.setGeometry(100, 100, 280, 100)  # Set window position and size

        # Setup the central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Setup input fields and buttons, and add them to the layout
        self.setup_input_fields(layout, main_controller)
        self.setup_buttons(layout, main_controller)

    def setup_input_fields(self, layout, main_controller):
        """
        Creates and adds input fields to the layout.

        Args:
            layout: The layout to add the input fields to.
            main_controller: The main controller instance for event handling.
        """
        # Channel Offset Input
        self.channel_offset_input = QLineEdit(self)
        self.channel_offset_input.setPlaceholderText("Enter Channel Offset")
        self.channel_offset_input.textChanged.connect(
            main_controller.validate_and_process_channel_offset
        )
        layout.addWidget(self.channel_offset_input)

        # Pixel Count Input
        self.pixel_count_input = QLineEdit(self)
        self.pixel_count_input.setPlaceholderText("Enter Pixel Count")
        self.pixel_count_input.textChanged.connect(
            main_controller.validate_and_process_pixel_count
        )
        layout.addWidget(self.pixel_count_input)

        # Channels Per Pixel Input
        self.channels_per_pixel_input = QLineEdit(self)
        self.channels_per_pixel_input.setPlaceholderText("Enter Pixel Channel Qty")
        self.channels_per_pixel_input.textChanged.connect(
            main_controller.validate_and_process_pixel_channel_count
        )
        layout.addWidget(self.channels_per_pixel_input)

    def setup_buttons(self, layout, main_controller):
        """
        Creates and adds buttons to the layout.

        Args:
            layout: The layout to add the buttons to.
            main_controller: The main controller instance for event handling.
        """
        # Select XML File Button
        self.select_file_btn = QPushButton("Select XML File", self)
        self.select_file_btn.clicked.connect(main_controller.select_file_path)
        layout.addWidget(self.select_file_btn)

        # Select Export Path Button
        self.select_export_btn = QPushButton("Select Export Path", self)
        self.select_export_btn.clicked.connect(main_controller.select_export_path)
        layout.addWidget(self.select_export_btn)

        # Run Program Button
        self.run_btn = QPushButton("Run Program", self)
        self.run_btn.clicked.connect(main_controller.run)
        layout.addWidget(self.run_btn)
