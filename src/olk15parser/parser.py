from typing import Tuple
import re
import base64

from src.logger import config_logger #type: ignore


class OLK15Parser(config_logger.Logger):
    """Read olk15 formated files
    """

    def get_mail_content(self, olk15message_location: str, subject: str) -> bytes:

        with open(olk15message_location, 'rb') as mail_file:
            message = mail_file.read()
            sliced_message = self._slice_message(message, subject)

            return sliced_message

    def get_file_content(self, olk15attachment_location: str) -> Tuple:
        with open(olk15attachment_location, 'rb') as mail_attachment:
            message = mail_attachment.read()
            attachment_name = self._get_attachment_name(message)
            attachment_content = self._decode_attachment_content(message)

            return (attachment_content, attachment_name)

    def _decode_attachment_content(self, message: bytes) -> bytes:
        try:
            attachment_content_b64 = re.search('base64(.*)', str(message)).group(1)[:-1] #type: ignore
        except:
            return b''

        attachment_content_b64 =  attachment_content_b64.replace('\\r','')

        try:
            attachment_content = base64.b64decode(attachment_content_b64)
        except:
            return b''

        return attachment_content

    def _get_attachment_name(self, message: bytes) -> str:
        try:
            attachment_name = re.search('name="(.*?)";', str(message)).group(1) #type: ignore
        except:
            attachment_name = ''

        attachment_name = self._decode_name(attachment_name)
        return attachment_name

    def _decode_name(self, name: str) -> str:
        name = name.replace('\\r','')
        reg_matches = re.findall('=\?UTF-8\?B\?(.*?)\?=', name) #type: ignore

        for reg_match in reg_matches:
            name = name.replace('=?UTF-8?B?{}?='.format(reg_match),
                                base64.b64decode(reg_match).decode('utf-8'))

        return name.strip()

    def _slice_message(self, message: bytes, subject: str) -> bytes:
        first_index = self._get_first_index(message, subject)
        last_index = self._get_last_index(message)
        return message[first_index:last_index]

    def _get_first_index(self, message: bytes, subject: str) -> int:
        try:
            return message.index('<html'.encode('utf-16-le'))
        except:
            self.logger.debug('[FirstIndex] Missing html tag, trying subject.')

        try:
            return message.index(subject.encode('utf-16-le'))
        except:
            self.logger.debug('[FirstIndex] Missing subject, going with default 0')

        self.logger.debug('[FirstIndex] default 0')
        return 0

    def _get_last_index(self, message: bytes) -> int:
        try:
            return len(message) - message[::-1].index('</html>'.encode('utf-16-le')[::-1])
        except:
            self.logger.debug('[LastIndex] Missing ending html tag, trying newline.')

        try:
            return len(message) - message[::-1].index('\r\n'.encode('utf-16-le')[::-1]) - 2
        except:
            self.logger.debug('[LastIndex] Missing ending newline, trying newline.')

        try:
            return len(message) - message[::-1].index(b'\x03\x00\x00\x00\x00\x00\x00\x00'[::-1]) - 8
        except:
            self.logger.debug('[LastIndex] Missing ending newline, trying newline.')

        self.logger.debug('[LastIndex] default -1')
        return -1

