#!/usr/bin/env python
from src.backupreader import reader
from src.olk15parser import parser
from src.archiver import archiver
from src.helpers import helpers

if __name__ == "__main__":
    profile_data_location = helpers.Helper.get_location()
    backupreader_app = reader.BackupReader(profile_data_location)
    olk15parser_app = parser.OLK15Parser()
    htmlformater_app = archiver.MailArchiver()
    for mail in backupreader_app.get_mails_from_database():
        mail_path = profile_data_location + mail.get('content_path')
        message = olk15parser_app.get_mail_content(mail_path, mail.get('subject'))
        htmlformater_app.archive_mail(mail, message)

