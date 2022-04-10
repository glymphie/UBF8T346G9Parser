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
        self.mails_info = {}

    def archive_mail(self, mail: Dict, message: bytes) -> None:
        mail_times = self._get_date(mail)
        mail_path = self._get_mail_path(mail, mail_times)
        self._update_mails_info(mail, mail_times)
        self._style_mails(mail, mail_path, message)

    def update_index(self) -> None:
        self.logger.info('Updating index')

        htmlstart = '<head>\n<link rel="stylesheet" href="./static/css/custom.css">\n</head>\n'
        htmltitle = '<h2>\nEmails found by the UBF8T346G9 Parser\n</h2>\n'
        htmlend = '</body>\n</html>'

        print(self.mails_info)

    def _update_mails_info(self, mail, mail_times):
        mail_info = {
            'path': 'Mails/{year}/{month}/{day}/{mailid}.html'.format(
                year=mail_times.get('year'),
                month=mail_times.get('month'),
                day=mail_times.get('day'),
                mailid=mail.get('id')
            ),
            'subject': mail.get('subject')
        }

    def _style_mails(self, mail: Dict, mail_path: str, message: bytes):

        with helpers.Helper.open_file(mail_path) as f:
            f.write('<head>\n<link rel="stylesheet" href="../../../../static/css/custom.css">\n</head>\n')
            self._write_meta_data(mail, f)
            f.write('\n<div class="bordermail">\n')
            f.write(message.decode('utf-16-le','ignore'))
            f.write('\n</div>\n')

    def _write_meta_data(self, mail: Dict, mail_file):
        meta_data = '''
<div class="bordermeta">
  <p>
    Subject: <b>{subject}</b>
  </p>
  <p>
    From: {sender}
  </p>
  <p>
    To: {recipients}
  </p>
  <p>
    CC: {cc}
  </p>
  <p>
    Date: {date}
  </p>
</div>
'''

        sendertext = self._get_sender(mail)
        recipientstext = self._get_recipients(mail)
        timetext = self._get_time(mail)

        meta_data = meta_data.format(
            subject=mail.get('subject'),
            sender=sendertext,
            recipients=' | '.join(recipientstext),
            cc=mail.get('cc'),
            date=timetext
        )

        mail_file.write(meta_data)

    def _get_time(self, mail):
        time = self._get_date(mail)
        timetext = '{hours}:{minutes}:{seconds} {day}/{month}/{year}'.format(
            year=time.get('year'),
            month=time.get('month'),
            day=time.get('day'),
            hours=time.get('hours'),
            minutes=time.get('minutes'),
            seconds=time.get('seconds'),
        )
        return timetext

    def _get_sender(self, mail):
        sender = mail.get('sender')
        sendertext = '<b>{name}</b> - <b>{email}</b>'.format(
            email=sender.get('email'), #type: ignore
            name=sender.get('name') #type: ignore
        )
        return sendertext

    def _get_recipients(self, mail):
        recipients = mail.get('recipients')
        recipientstext = []
        if recipients != [None]:
            for recipient in recipients: #type: ignore
                recipientstext.append('<b>{name}</b> - <b>{email}</b>'.format(
                    email=recipient.get('email'), #type: ignore
                    name=recipient.get('name') #type: ignore
                ))
        return recipientstext

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

