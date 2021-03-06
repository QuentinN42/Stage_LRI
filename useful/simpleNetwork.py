"""
A simple Dense network.

@date: 15/05/2019
@author: Quentin Lieumont
"""
from useful.network import Network
from useful.data import Data
from useful.functions import generate
from keras import layers, constraints
import numpy as np


class SimpleNetwork(Network):
    """
    Input : X n dim array
    Output : activation(X.W)
    with W the weights vector
    """

    def __init__(
        self,
        # Data initialisation
        data: Data = None,
        quiet: bool = False,
        func: callable = None,
        n_dim: int = 2,
        # Layer options
        use_bias: bool = False,
        activation: str = "linear",
        allow_neg: bool = True,
        max_norm: float = 1.0,
        # Training options
        loss_func: callable = None,
        split_ratio: float = 0.5,
        validate: bool = True,
        epochs: int = 1,
    ):
        self.n_dim = n_dim
        if func:
            if not data:
                d = generate(dim=self.n_dim)
                data = Data(d, func)
            else:
                data = Data(data.raw_data, func)
        else:
            if not data:
                raise AttributeError("Data generation need function")
        super().__init__(data, quiet)
        if allow_neg:
            self.model.add(
                layers.Dense(
                    1,
                    activation=activation,
                    input_dim=self.n_dim,
                    use_bias=use_bias,
                    kernel_constraint=constraints.max_norm(max_norm),
                )
            )
        else:
            self.model.add(
                layers.Dense(
                    1,
                    activation=activation,
                    input_dim=self.n_dim,
                    use_bias=use_bias,
                    kernel_constraint=constraints.NonNeg()
                )
            )
        if loss_func:
            self.build(loss_func)
        else:
            self.build()
        self.train(split_ratio, validate=validate, epochs=epochs)

    @property
    def weights(self) -> np.array:
        return np.array([w[0] for w in self.model.get_weights()[0]])
