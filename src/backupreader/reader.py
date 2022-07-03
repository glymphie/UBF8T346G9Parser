import sqlite3
import dataclasses
import pathlib
from typing import Generator, List

from src.helpers import helpers # type: ignore
from src.logger import config_logger #type: ignore


@dataclasses.dataclass
class BackupReader(config_logger.Logger):
    """Read data from Outlook 2016 Backup folder.

    Attributes:
      backup_location: A string of backup folder location.
      profile_data_location: A string of data folder location based on user.
    """

    profile_data_location: str
    filter_hidden = '/.'

    @property
    def db_location(self):
        sqlitedb = 'Outlook.sqlite'
        try:
            return helpers.Helper.test_location(
                self.profile_data_location + sqlitedb, 'file')
        except FileNotFoundError:
            self.logger.warning(f'Missing {sqlitedb}, is the database missing?')
            raise FileNotFoundError

    def get_mails_from_database(self) -> Generator:
        self.logger.info('Getting emails from database')
        db_connection = self._connect_to_database(self.db_location)
        mails = self._get_mails(db_connection)
        for mail in mails:
            yield self._get_info_from_email(dict(mail))

    def get_mails_amount(self) -> int:
        db_connection = self._connect_to_database(self.db_location)
        mails = self._get_mails(db_connection)
        return len(list(mails))

    def get_attachments_from_folder(self) -> Generator:
        self.logger.info('Getting attachments from folders')
        message_attachments = 'Message Attachments/'
        attachments_location = pathlib.Path(self.profile_data_location +
            message_attachments)
        attachments_directories = [directory for directory
                                   in attachments_location.iterdir()
                                   if directory.is_dir()]
        for attachment_directory in attachments_directories:
            for attachments_location in attachment_directory.iterdir():
                if '._' not in str(attachments_location):
                    yield attachments_location

    def get_attachments_amount(self) -> int:
        return len(list(self.get_attachments_from_folder()))


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
            'id': mail.get('Threads_ThreadID'),
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

