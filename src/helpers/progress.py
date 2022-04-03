import dataclasses
import os

from src.logger import config_logger #type: ignore


@dataclasses.dataclass
class ProgressBar(config_logger.Logger):
    """Tiny progressbar display in the terminal
    """

    amount: int

    counter: int = 0

    @property
    def percent_done(self):
        return '{:05.2f}'.format(self.counter / self.amount * 100)

    def update(self):
        self._update_counter()
        self._clear_line()
        self._update_screen()

    def progress_done(self):
        print()

    def _update_counter(self):
        self.counter += 1

    def _update_screen(self):
        bar = self._get_bar()
        info = self._get_info()
        print('{} {}'.format(bar, info), end='\r')

    def _get_bar(self):
        line_amount = int(float(self.percent_done)/2.5)
        lines = '=' * line_amount
        space = ' ' * (40 - line_amount)

        return '[{}{}]'.format(lines, space)

    def _get_info(self):
        return '{}%\t({}/{})'.format(self.percent_done, self.counter, self.amount)

    def _clear_line(self):
        size = os.get_terminal_size().columns
        print(' ' * size, end='\r')
