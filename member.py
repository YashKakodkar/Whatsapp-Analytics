import os
from collections import OrderedDict


class Member:

    def __init__(self, name, date_added):
        self.name = name
        self.date_added = date_added
        self.messages_sent = 0
        self.times_added = 1
        self.times_removed = 0
        self.times_left = 0
        self.active = True
        self.chat_log = OrderedDict()

    def to_string(self):
        info = self.name + "\n"
        info += "Messages Sent: {}\n".format(self.messages_sent)
        info += "Status: {}\n".format(self.active)
        info += "Date Added: {}\n".format(self.date_added)
        info += "Times Added: {}\n".format(self.times_added)
        info += "Times Left: {}\n".format(self.times_left)
        info += "Times Removed: {}\n".format(self.times_removed)
        return info
