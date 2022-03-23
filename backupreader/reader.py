import sqlite3
import dataclasses
from typing import Generator, List

from helpers.helpers import Helper # type: ignore


@dataclasses.dataclass
class backupreader:
    """Read data from Outlook 2016 Backup folder.

    Attributes:
      backup_location: A string of backup folder location.
      profile_data_location: A string of data folder location based on user.
    """

    profile_data_location: str
    filter_hidden = '/.'

    def get_mails_from_database(self) -> Generator:
        sqlitedb = 'Outlook.sqlite'
        try:
            db_location = Helper.test_location(
                self.profile_data_location + sqlitedb, 'file')
        except FileNotFoundError:
            raise FileNotFoundError('Missing {sqlitedb}, is the database missing?')

        db_connection = self._connect_to_database(db_location)
        mails = self._get_mails(db_connection)
        for mail in mails:
            yield self._get_info_from_email(dict(mail))

    def _get_info_from_email(self, mail: dict) -> dict:
        return {
            'content_path' : mail.get('PathToDataFile'),
            'subject' : mail.get('Message_ThreadTopic'),
            'time' : mail.get('Message_TimeReceived'),
            'sender' : {'email': mail.get('Message_SenderAddressList'),
                        'name': mail.get('Message_SenderList')},
            'recipients' : self._merge_recipients(
                mail.get('Message_ToRecipientAddressList'),
                mail.get('Message_RecipientList')),
            'cc' : mail.get('Message_CCRecipientAddressList'),
            'type' : mail.get('Message_type'),
        }

    def _merge_recipients(self, emails: str, names: str) -> List:
        try:
            emails_split = emails.split(';')
            names_split = names.split(';')
        except AttributeError:
            return [None]

        recipients = []

        for email, name in zip(emails_split, names_split):
            recipients.append({
                'email': email,
                'name': name
            })

        return recipients

    def _connect_to_database(self, db_location):
        db_connection = sqlite3.connect(db_location)
        db_connection.row_factory = sqlite3.Row
        return db_connection.cursor()

    def _get_mails(self, db_connection):
        return db_connection.execute('SELECT * FROM Mail')

    def _get_tables(self, db_connection):
        return db_connection.execute("SELECT * FROM sqlite_schema WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%' ")

