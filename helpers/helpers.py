import pathlib


class Helper:
    """Helper class with sorta random helper methods
    """

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

    @classmethod
    def get_location(cls) -> str:
        return cls._get_backup_location() + cls._get_profile_data()

