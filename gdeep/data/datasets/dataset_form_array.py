import json
import os
import shutil
import warnings
from abc import ABC, abstractmethod
from os.path import join
from typing import Any, Callable, Dict, Optional, Tuple, TypeVar, Union

import numpy as np
import pandas as pd
import torch
from PIL import Image, UnidentifiedImageError
from sympy import false
from torch.utils.data import DataLoader, Dataset
from torchtext import datasets as textds
from torchvision import datasets
from torchvision.transforms import Resize, ToTensor
from tqdm import tqdm


from ..transforming_dataset import TransformingDataset

Tensor = torch.Tensor
T = TypeVar('T')

class FromArray(Dataset):
    """This class is useful to build dataloaders
    from a array of X and y. Tensors are also supported.

    Args:
        X (np.array or torch.Tensor):
            The data. The first dimension is the datum index
        y (np.array or torch.Tensor):
            The labels, need to match the first dimension
            with the data

    """
    def __init__(self, X: Union[Tensor, np.ndarray],
                 y: Union[Tensor, np.ndarray]
                 ) -> None:
        self.X = self._from_numpy(X)
        y = self._from_numpy(y)
        self.y = self._long_or_float(y)

    @staticmethod
    def _from_numpy(X):
        """this is torch.from_numpy() that also allows
        for tensors"""
        if isinstance(X, torch.Tensor):
            return X
        return torch.from_numpy(X)

    @staticmethod
    def _long_or_float(y):
        if isinstance(y, torch.Tensor):
            return y
        if isinstance(y, np.float16) or isinstance(y, np.float32) or isinstance(y, np.float64):
            return torch.tensor(y).float()
        return torch.tensor(y).long()

    def __len__(self):
        return self.y.shape[0]

    def __getitem__(self, idx:int) -> Tuple[Tensor, Tensor]:
        X, y = (self.X[idx], self.y[idx])
        return X, y
