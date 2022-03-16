import pathlib
import sqlite3

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
        sqlitedb = 'Outlook.sqlite'
        try:
            db_location = self._test_location(
                self.profile_data_location + sqlitedb, 'file')
        except FileNotFoundError:
            raise FileNotFoundError('Missing {sqlitedb}, is the database missing?')

        db_connection = self._connect_to_database(db_location)
#        db_connection.execute('SELECT name FROM sqlite_master WHERE type=\'table\';')
        for table in db_connection.fetchall():
            print(list(table))
        mails = self._get_mails(db_connection)
        first_row = mails.fetchone()
#        for key, col in zip(first_row.keys(), list(first_row)):
#            print(key, col)

        print(first_row['Message_MessageListData'].decode('utf-8','ignore'))
        print(first_row['Message_MessageListData'].decode('utf-16-be','ignore'))


    def _connect_to_database(self, db_location):
        db_connection = sqlite3.connect(db_location)
        db_connection.row_factory = sqlite3.Row
        return db_connection.cursor()

    def _get_mails(self, db_connection):
        return db_connection.execute('SELECT * FROM Mail')





