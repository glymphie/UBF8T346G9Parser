import re


class olk15parser:
    """Read olk15 formated files
    """

    re_full_message = re.compile(r'<head>[(\r\n)\w\W]*</html>')

    def get_mail_content(self, olk15message_location: str) -> str:

        with open(olk15message_location, 'rb') as mail_file:
            message = mail_file.read().decode('utf-16-be', 'ignore')
            rmatch = self.re_full_message.search(message)
            return rmatch.group(0) # type: ignore

