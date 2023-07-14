import numpy as np
from time import time_ns

from generators.gnpcl import GNPCL


class ExpGen:
    def __init__(self, param_lambda) -> None:
        self.gnpcl = GNPCL(time_ns())
        self.param_lambda = param_lambda

    def generate(self):
        return (-1 / self.param_lambda) * np.log(self.gnpcl.generate())
