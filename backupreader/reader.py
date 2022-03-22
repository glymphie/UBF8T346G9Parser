import sqlite3
import dataclasses

from helpers.helpers import Helper

@dataclasses.dataclass
class backupreader:
    """Read data from Outlook 2016 Backup folder.

    Attributes:
      backup_location: A string of backup folder location.
      profile_data_location: A string of data folder location based on user.
    """

    profile_data_location: str

    filter_hidden = '/.'

    def get_mails_from_database(self):
        sqlitedb = 'Outlook.sqlite'
        try:
            db_location = Helper.test_location(
                self.profile_data_location + sqlitedb, 'file')
        except FileNotFoundError:
            raise FileNotFoundError('Missing {sqlitedb}, is the database missing?')

        db_connection = self._connect_to_database(db_location)
        mails = self._get_mails(db_connection)
        while True:
            first_row = mails.fetchone()
            if first_row['Message_HasAttachment'] == 1:
                for key, col in zip(first_row.keys(), list(first_row)):
                    print(key, col)
                return


    def _connect_to_database(self, db_location):
        db_connection = sqlite3.connect(db_location)
        db_connection.row_factory = sqlite3.Row
        return db_connection.cursor()

    def _get_mails(self, db_connection):
        return db_connection.execute('SELECT * FROM Mail')


