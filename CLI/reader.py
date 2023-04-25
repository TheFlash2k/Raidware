try:
    import gnureadline as readline
except ImportError:
    import readline
import os

class TabComplete:
    def __init__(self, commands : list):
        self.options = commands
        readline.set_completer(self.__complete__)
        readline.parse_and_bind('tab: complete')

    def __complete__(self, text, state):
        response = None
        if state == 0:
            if text:
                self.matches = [
                    s
                    for s in self.options
                    if s and s.startswith(text.upper())
                ]
            else:
                self.matches = self.options[:]
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response