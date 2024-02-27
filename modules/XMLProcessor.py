import xml.etree.ElementTree as ET  # Import for XML parsing
import re  # Import for regular expression operations


class XMLProcessor:
    """
    A class to process XML files for extracting fixture and pixel information.

    Attributes:
        channel_offset (int): The offset to start counting channels from.
        pixel_channel_count (int): The number of channels per pixel.

    Methods:
        set_channel_offset(offset): Sets the channel offset.
        set_pixel_channel_count(pixel_channel_count): Sets the pixel channel count.
        run(xml_path): Processes the XML file and extracts fixture and pixel information.
        calculate_universe_address(absolute_address): Calculates the universe and address from an absolute address.
        remove_namespaces(xml): Removes namespaces from XML tags.
    """

    def __init__(self):
        """Initializes the XMLProcessor with default values for its attributes."""
        self.channel_offset = None
        self.pixel_channel_count = None

    def set_channel_offset(self, offset):
        """Sets the channel offset.

        Args:
            offset (int): The offset to start counting channels from.
        """
        self.channel_offset = offset

    def set_pixel_channel_count(self, pixel_channel_count):
        """Sets the number of channels per pixel.

        Args:
            pixel_channel_count (int): The number of channels per pixel.
        """
        self.pixel_channel_count = pixel_channel_count

    def run(self, xml_path):
        """Processes the XML file and extracts fixture and pixel information.

        Args:
            xml_path (str): The path to the XML file to be processed.

        Returns:
            list: A list of dictionaries containing fixture and pixel information.
        """
        fixtures_info = []  # List to store fixture information
        try:
            tree = ET.parse(xml_path)  # Parse the XML file
            root = tree.getroot()  # Get the root element of the XML tree

            for elem in root.iter():  # Remove namespaces from tags
                elem.tag = self.remove_namespaces(elem.tag)

            for layer in root.findall(".//Layer"):  # Process each Layer element
                for fixture in layer.findall(
                    ".//Fixture"
                ):  # Process each Fixture element within Layer
                    fixture_info = self._process_fixture(fixture)
                    fixtures_info.append(
                        fixture_info
                    )  # Append fixture information to the list

            return fixtures_info
        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        return fixtures_info  # Return list even in case of an exception

    def _process_fixture(self, fixture):
        """Processes a single fixture element and extracts its information.

        Args:
            fixture (xml.etree.ElementTree.Element): The fixture element to process.

        Returns:
            dict: A dictionary containing the processed fixture information.
        """
        name = fixture.attrib.get("name", "Unknown Name")
        fixture_id = fixture.attrib.get("fixture_id", "Unknown FixtureID")
        address_element = fixture.find(".//Address")
        address = (
            address_element.text if address_element is not None else "Unknown Address"
        )
        universe, fixture_address = self.calculate_universe_address(int(address))
        converted_address = f"{universe}.{fixture_address}"
        pixels_info = self._process_pixels(int(address))

        return {
            "Name": name,
            "Fixture Absolute Address": address,
            "Fixture Address": converted_address,
            "FixtureID": fixture_id,
            "Pixels": pixels_info,
        }

    def _process_pixels(self, start_address):
        """Processes pixel information starting from a given address.

        Args:
            start_address (int): The starting address for pixel processing.

        Returns:
            list: A list of dictionaries containing pixel information.
        """
        pixels_info = []
        pixel_start_address = start_address + self.channel_offset
        for channel_offset in range(0, 512, self.pixel_channel_count):
            pixel_address = pixel_start_address + channel_offset
            pixel_universe, pixel_address = self.calculate_universe_address(
                pixel_address
            )
            pixels_info.append(
                {
                    "Pixel Start Channel": pixel_address,
                    "Universe": pixel_universe,
                    "Address": pixel_address,
                }
            )
        return pixels_info

    def calculate_universe_address(self, absolute_address):
        """Calculates the universe and address from an absolute address.

        Args:
            absolute_address (int): The absolute address to calculate from.

        Returns:
            tuple: A tuple containing the universe and address.
        """
        universe = (absolute_address - 1) // 512 + 1
        address = (absolute_address - 1) % 512 + 1
        return universe, address

    def remove_namespaces(self, xml):
        """Removes namespaces from XML tags.

        Args:
            xml (str): The XML tag to remove namespaces from.

        Returns:
            str: The XML tag without namespaces.
        """
        return re.sub(r"\{.*?\}", "", xml)
