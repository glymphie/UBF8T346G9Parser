#!/usr/bin/env python
from backupreader import reader
from olk15parser import parser
from helpers.helpers import Helper

if __name__ == "__main__":
    profile_data_location = Helper.get_location()

    backupreader_app = reader.backupreader(profile_data_location)
    olk15parser_app = parser.olk15parser()


    for i, mail in enumerate(backupreader_app.get_mails_from_database()):
        mail_path = profile_data_location + mail.get('content_path')
        print(i, mail)
        message = olk15parser_app.get_mail_content(mail_path, mail.get('subject'))

