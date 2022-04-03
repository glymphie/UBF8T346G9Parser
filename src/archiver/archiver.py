import pathlib
import shutil
from datetime import datetime
from typing import Dict

from src.helpers import helpers #type: ignore
from src.logger import config_logger #type: ignore

class MailArchiver(config_logger.Logger):
    """Archive email
    """

    def __init__(self) -> None:
        self.mailsdir = 'MailArchive/Mails'
        self._check_mailsdir(self.mailsdir)

    def archive_mail(self, mail: Dict, message: bytes) -> None:
        mail_times = self._get_date(mail)
        mail_path = self._get_mail_path(mail, mail_times)

        with helpers.Helper.open_file(mail_path) as f:
            f.write('\n<frame>\n')
            f.write(message.decode('utf-16-le','ignore'))
            f.write('\n</frame>\n')

    def _get_date(self, mail: Dict) -> Dict:
        mail_date = datetime.fromtimestamp(mail.get('time'))
        return {
            'year': mail_date.strftime("%Y"),
            'month': mail_date.strftime("%m"),
            'day': mail_date.strftime("%d"),
            'hours': mail_date.strftime("%H"),
            'minutes': mail_date.strftime("%M"),
            'seconds': mail_date.strftime("%S"),
        }

    def _get_mail_path(self, mail: Dict, mail_times: Dict) -> str:
        mail_dir = self._create_mail_dirs(mail_times)
        return '{}/{}.html'.format(mail_dir, mail.get('id'))

    def _create_mail_dirs(self, mail_times: Dict) -> str:
        mail_dir = '{mailsdir}/{year}/{month}/{day}'.format(
            mailsdir=self.mailsdir,
            year=mail_times.get('year'),
            month=mail_times.get('month'),
            day=mail_times.get('day')
        )

        pathlib.Path(mail_dir).mkdir(parents=True, exist_ok=True)
        return mail_dir

    def _check_mailsdir(self, mailsdir: str):
        mails_dir = pathlib.Path(mailsdir)
        if mails_dir.is_dir():
            userinput = input('The Mails directory already exists, do you want '
                              'to start over? [Y/n]: ')

            if 'n' == userinput.lower() or 'no' == userinput.lower():
                self.logger.info('Exiting.')
                exit(0)
            else:
                self.logger.info(f'Removing {mails_dir}')
                shutil.rmtree(mails_dir)

