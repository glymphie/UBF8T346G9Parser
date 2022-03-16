import pathlib

class backupreader:
    """Read data from Outlook 2016 Backup folder.

    Attributes:
      backup_location: A string of backup folder location.
      profile_data_location: A string of data folder location based on user.
    """

    filter_hidden = '/.'

    def __init__(self) -> None:
        self.backup_location = self._test_location(
            self._get_backup_location(), 'folder')
        self.profile_data_location = self._test_location(
            self.backup_location + self._get_profile_data(), 'folder')

    def _get_backup_location(self):
        default = './UBF8T346G9.Office/'
        userinput = input(
            f'Please provide backup folder location [Default: {default}]: ')
        if userinput:
            return userinput
        return default

    def _get_profile_data(self):
        static_path = '/Outlook/Outlook 15 Profiles/{}/Data/'
        default = 'Main Profile'
        userinput = input(
            f'Please provide user profile [Default: {default}]: ')
        if userinput:
            return static_path.format(userinput)
        return static_path.format(default)

    def _test_location(self, location: str, location_type: str) -> str:
        location_path = pathlib.Path(location)
        if location_type == 'folder' and not location_path.is_dir():
            raise NotADirectoryError(f'{location} is not a directory')
        if location_type == 'file' and not location_path.is_file():
            raise FileNotFoundError(f'{location} is not a file')
        return location

    def iterate_over_messages(self):
        messages_folder = 'Messages/'
        messages_path = pathlib.Path(
            self.profile_data_location + messages_folder)
        for num_folder in messages_path.iterdir():
            if self.filter_hidden in str(num_folder):
                continue

            iter_folder = pathlib.Path(num_folder)
            for message in iter_folder.iterdir():
                if self.filter_hidden in str(message):
                    continue

                yield message


    def get_file_content(self):
        pass


