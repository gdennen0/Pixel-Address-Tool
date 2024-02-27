import os
from DialogWindow import DialogWindow
from XMLProcessor import XMLProcessor
from MainModel import MainModel


class MainController:
    """
    MainController class handles the interaction between the user interface and the model.
    It is responsible for processing user inputs, validating them, and executing the main
    functionality of the application.
    """

    def __init__(self):
        """
        Initializes the MainController with a MainModel instance.
        """
        self.main_model = MainModel()

    def select_file_path(self):
        """
        Opens a dialog for the user to select an XML file path.
        """
        self.main_model.xml_file_path = DialogWindow.open_file(
            "Select File", "Select file to open"
        )

    def select_export_path(self):
        """
        Opens a dialog for the user to select a file path for exporting results.
        """
        self.main_model.export_file_path = DialogWindow.save_file("Save Location")

    def validate_and_process_channel_offset(self, channel_offset_input):
        """
        Validates and processes the channel offset input from the user.

        Args:
            channel_offset_input (str): The channel offset input from the user.
        """
        try:
            if channel_offset_input and channel_offset_input.isdigit():
                self.main_model.channel_offset = int(channel_offset_input)
                print(f"Updated channel offset to {channel_offset_input}")
            else:
                raise ValueError("Channel offset input must be a digit.")
        except ValueError as e:
            print(f"Error: {e}")

    def validate_and_process_pixel_count(self, pixel_count_input):
        """
        Validates and processes the pixel count input from the user.

        Args:
            pixel_count_input (str): The pixel count input from the user.
        """
        try:
            if pixel_count_input and pixel_count_input.isdigit():
                self.main_model.pixel_count = int(pixel_count_input)
                print(f"Updated Pixel count to {pixel_count_input}")
            else:
                raise ValueError("Pixel count input must be a digit")
        except ValueError as e:
            print(f"Error: {e}")

    def validate_and_process_pixel_channel_count(self, pixel_channel_count):
        """
        Validates and processes the pixel channel count input from the user.

        Args:
            pixel_channel_count (str): The pixel channel count input from the user.
        """
        try:
            if pixel_channel_count and pixel_channel_count.isdigit():
                self.main_model.pixel_channel_count = int(pixel_channel_count)
                print(f"Updated channel per pixel count to {pixel_channel_count}")
            else:
                raise ValueError("Channel per pixel input must be a digit")
        except ValueError as e:
            print(f"Error: {e}")

    def run(self):
        """
        Executes the main functionality of the application. It validates the user inputs,
        processes the XML file, and exports the results to a specified file path.
        """
        try:
            # Validate file paths and parameters
            self._validate_inputs()

            # Process XML file and export results
            self._process_and_export()

            print(f"Export Complete!")
        except ValueError as e:
            print(f"Validation Error: {e}")

    def _validate_inputs(self):
        """
        Validates the inputs provided by the user.
        """
        if not self.main_model.xml_file_path or not os.path.isfile(
            self.main_model.xml_file_path
        ):
            raise ValueError("Invalid or missing XML file path.")
        if not self.main_model.export_file_path or not os.path.isdir(
            os.path.dirname(self.main_model.export_file_path)
        ):
            raise ValueError("Invalid or missing export file path.")
        for attr in ["channel_offset", "pixel_count", "pixel_channel_count"]:
            if (
                getattr(self.main_model, attr) is None
                or not str(getattr(self.main_model, attr)).isdigit()
            ):
                raise ValueError(
                    f"{attr.replace('_', ' ').capitalize()} must be a digit and cannot be empty."
                )

    def _process_and_export(self):
        """
        Processes the XML file and exports the results to the specified file path.
        """
        xml_processor = XMLProcessor()
        xml_processor.set_channel_offset(self.main_model.channel_offset)
        xml_processor.set_pixel_channel_count(self.main_model.pixel_channel_count)

        fixture_data = xml_processor.run(self.main_model.xml_file_path)
        if fixture_data:
            export_file_path = f"{self.main_model.export_file_path}.txt"
            with open(export_file_path, "w") as file:
                for fixture in fixture_data:
                    for key, value in fixture.items():
                        if key != "Pixels":
                            file.write(f"{key}: {value}\n")
                        else:
                            for pixel_index, pixel in enumerate(
                                value[: self.main_model.pixel_count], start=1
                            ):
                                pixel_info = f"Pixel {pixel_index} start: {pixel['Universe']}.{pixel['Address']}"
                                file.write(f"{pixel_info}\n")
                    file.write("\n")
