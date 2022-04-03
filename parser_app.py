#!/usr/bin/env python
from src.backupreader import reader
from src.olk15parser import parser
from src.archiver import archiver
from src.helpers import helpers
from src.helpers import progress
from src.logger import config_logger

logger = config_logger.Logger()

if __name__ == "__main__":
    profile_data_location = helpers.Helper.get_location()
    backupreader_app = reader.BackupReader(profile_data_location)
    olk15parser_app = parser.OLK15Parser()
    archiver_app = archiver.MailArchiver()

    mails_amount = backupreader_app.get_mails_amount()
    progressbar = progress.ProgressBar(mails_amount)

    mails = backupreader_app.get_mails_from_database()

    logger.logger.info('Getting email content and writing to files')
    for mail in mails:
        progressbar.update()
        mail_path = profile_data_location + mail.get('content_path')
        message = olk15parser_app.get_mail_content(mail_path, mail.get('subject'))
        archiver_app.archive_mail(mail, message)

    progressbar.progress_done()

    logger.logger.info('Done getting emails, updating index')
