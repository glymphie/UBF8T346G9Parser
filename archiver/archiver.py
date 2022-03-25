from datetime import datetime
from typing import Dict

class MailArchiver:
    """Archives emails
    """

    def archive_mail(self, mail: Dict, message: bytes):

        mail_times = self._get_date(mail)



        if mail.get('id') == 7038:
            print(mail.get('time'), datetime.fromtimestamp(mail.get('time')))
#            message = olk15parser_app.get_mail_content(mail_path, mail.get('subject'))
#            with open('test.html', 'a') as f:
#                f.write(message.decode('utf-16-le'))
#                f.write('\n\n' + 200 * '@' + '\n\n')

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

