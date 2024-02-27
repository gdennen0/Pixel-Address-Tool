class MainModel:
    """
    A model class to store application settings and data paths.

    Attributes:
        xml_file_path (str): Path to the input XML file. Default is None.
        export_file_path (str): Path where the export file will be saved. Default is None.
        channel_offset (int): The offset for channel numbering. Default is None.
        pixel_count (int): The number of pixels to process. Default is None.
        pixel_channel_count (int): The number of channels per pixel. Default is None.
    """

    def __init__(self):
        """
        Initializes the MainModel with default values for its attributes.
        """
        self.xml_file_path = None
        self.export_file_path = None
        self.channel_offset = None
        self.pixel_count = None
        self.pixel_channel_count = None
