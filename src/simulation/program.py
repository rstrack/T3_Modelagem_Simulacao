import random

from util.colors import COLORS


class Program:
    def __init__(self, number, processing_time):
        self.number = number
        self.processing_time = processing_time
        self.start_time = 0
        self.finish_time = 0
        self.color = random.choice(COLORS)

    def execute(self, current_time):
        if self.start_time == 0:
            self.start_time = current_time
        if current_time - self.start_time >= self.processing_time:
            self.finish_time = current_time
