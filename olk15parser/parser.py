import logging


class olk15parser:
    """Read olk15 formated files
    """

    def get_mail_content(self, olk15message_location: str, subject: str) -> bytes:

        with open(olk15message_location, 'rb') as mail_file:
            message = mail_file.read()
            sliced_message = self._slice_message(message, subject)

            return sliced_message

    def _slice_message(self, message: bytes, subject: str) -> bytes:
        first_index = self._get_first_index(message, subject)
        last_index = self._get_last_index(message)
        return message[first_index:last_index]

    def _get_first_index(self, message: bytes, subject: str) -> int:
        try:
            return message.index('<html'.encode('utf-16-le'))
        except:
            logging.debug('[FirstIndex] Missing html tag, trying subject.')

        try:
            return message.index(subject.encode('utf-16-le'))
        except:
            logging.debug('[FirstIndex] Missing subject, going with default 0')

        logging.debug('[FirstIndex] default 0')
        return 0

    def _get_last_index(self, message: bytes) -> int:
        try:
            return len(message) - message[::-1].index('</html>'.encode('utf-16-le')[::-1])
        except:
            logging.debug('[LastIndex] Missing ending html tag, trying newline.')

        try:
            return len(message) - message[::-1].index('\r\n'.encode('utf-16-le')[::-1]) - 2
        except:
            logging.debug('[LastIndex] Missing ending newline, trying newline.')

        try:
            return len(message) - message[::-1].index(b'\x03\x00\x00\x00\x00\x00\x00\x00'[::-1]) - 8
        except:
            logging.debug('[LastIndex] Missing ending newline, trying newline.')

        logging.debug('[LastIndex] default -1')
        return -1

