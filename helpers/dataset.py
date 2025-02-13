# In summary, the NextTokenPredictionDataset class is a useful component for building a language model that can predict the next token in a sequence. The class leverages PyTorch tensors and the Tokenizer class to efficiently load and preprocess data for training.


import torch
from torch import Tensor

from model.tokenizer import Tokenizer

# Target sequences (labels) are constructed similarly by slicing the encoded data, but shifted by one position to predict the next token in the sequence.

class NextTokenPredictionDataset:
    def __init__(self, input_file: str, context_size: int, tokenizer: Tokenizer) -> None:
        super().__init__()

        self.input_file = input_file
        self.context_size = context_size

        # load data in memory
        with open(self.input_file) as f:
            data = f.read()

        self.data = tokenizer.encode(data)

    def get_batch(self, batch_size: int) -> tuple[Tensor]:
        # sample random starting index in the data and build a batch from there
        indices = torch.randint(self.data.size(0) - self.context_size, (batch_size,))
        inputs = torch.stack([self.data[i : i + self.context_size] for i in indices], dim=0)
        labels = torch.stack([self.data[i + 1 : i + 1 + self.context_size] for i in indices], dim=0).long()

        return inputs, labels