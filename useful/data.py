"""
Data class

@date: 15/05/2019
@author: Quentin Lieumont
"""
import numpy as np
from useful.functions import nmap, title, generate, write_json


def _nmap_with_print(f: callable, t: iter):
    length = len(t)
    print_list = nmap(int, np.arange(100) * length / 100)
    out = np.array([])
    title(" Generation of {} data... ".format(length))
    for i in range(length):
        out = np.append(out, f(t[i]))
        if i in print_list:
            print("Building data : {}%".format(str(int(i * 100 / length)).zfill(2)))
    return out


class _LearningData:
    def __init__(self, tab: iter):
        self.data = tab
        self.training = np.array([])
        self.testing = np.array([])

    def __len__(self) -> int:
        return len(self.data)

    def split(self, index: int) -> None:
        self.training, self.testing = self.data[:index], self.data[index:]


class Data:
    def __init__(
        self,
        tab: iter = None,
        func: callable = None,
        expected: iter = None,
        debug: bool = False,
    ):
        if func:
            if tab is None:
                if "dim" in func.__dict__.keys():
                    tab = generate(dim=func.dim)
                else:
                    raise AttributeError("Can't extract dimension")
            self.func = func
            self.raw_data = tab
            self.question = _LearningData(self.raw_data)
            if debug:
                self.expected = _LearningData(
                    _nmap_with_print(self.func, self.question_data)
                )
            else:
                self.expected = _LearningData(nmap(self.func, self.question_data))
        elif expected is not None:
            self.raw_data = tab
            self.question = _LearningData(self.raw_data)
            self.expected = _LearningData(expected)
        else:
            raise AttributeError("func or awnsers needed")

    def __len__(self) -> int:
        return len(self.question)

    def split(self, learning_set_ratio: float = 0.5) -> None:
        split_at = int(learning_set_ratio * len(self))
        self.question.split(split_at)
        self.expected.split(split_at)

    def save(self, file_name: str) -> None:
        write_json(
            file_name,
            {
                "question": self.question_data.tolist(),
                "expected": self.expected_data.tolist(),
            },
        )

    @property
    def n_dim(self):
        return len(self.raw_data[0])

    @property
    def question_training(self):
        return self.question.training

    @property
    def expected_training(self):
        return self.expected.training

    @property
    def question_data(self):
        return self.question.data

    @property
    def expected_data(self):
        return self.expected.data

    @property
    def question_testing(self):
        return self.question.testing

    @property
    def expected_testing(self):
        return self.expected.testing
