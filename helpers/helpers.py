import pathlib
from typing import List

class Helper:
    @staticmethod
    def test_location(location: str, location_type: str) -> str:
        location_path = pathlib.Path(location)
        if location_type == 'folder' and not location_path.is_dir():
            raise NotADirectoryError(f'{location} is not a directory')
        if location_type == 'file' and not location_path.is_file():
            raise FileNotFoundError(f'{location} is not a file')
        return location

    @staticmethod
    def _get_backup_location():
        default = './UBF8T346G9.Office/'
        userinput = input(
            f'Please provide backup folder location [Default: {default}]: ')
        if userinput:
            return userinput
        return default

    @staticmethod
    def _get_profile_data():
        static_path = 'Outlook/Outlook 15 Profiles/{}/Data/'
        default = 'Main Profile'
        userinput = input(
            f'Please provide user profile [Default: {default}]: ')
        if userinput:
            return static_path.format(userinput)
        return static_path.format(default)

    @staticmethod
    def get_location() -> str:
        return __class__._get_backup_location() + __class__._get_profile_data()
