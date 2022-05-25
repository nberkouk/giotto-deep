# %%
import os
from shutil import rmtree
from typing import List
from sklearn.model_selection import train_test_split

import numpy as np
from torch.utils.data import DataLoader, Subset

from gdeep.data.datasets.persistence_diagrams_from_graphs_builder import PersistenceDiagramFromGraphBuilder
from gdeep.data.persistence_diagrams.one_hot_persistence_diagram import OneHotEncodedPersistenceDiagram
from gdeep.utility.utils import autoreload_if_notebook
from gdeep.utility import DEFAULT_GRAPH_DIR

autoreload_if_notebook()

# Parameters
name_graph_dataset: str = 'MUTAG'
diffusion_parameter: float = 0.1
num_homology_types: int = 4


# Create the persistence diagram dataset
pd_creator = PersistenceDiagramFromGraphBuilder(name_graph_dataset, diffusion_parameter)
pd_creator.create()

# %%
# Print sample extended persistence diagram
file_path: str = os.path.join(DEFAULT_GRAPH_DIR,
                              f"MUTAG_{diffusion_parameter}_extended_persistence", "diagrams")
graph_idx = 4
pd: OneHotEncodedPersistenceDiagram = \
    OneHotEncodedPersistenceDiagram.load(os.path.join(file_path, 
                                                      f"graph_{graph_idx}_persistence_diagram.npy"))
names = ["Ord0", "Ext0", "Rel1", "Ext1"]
pd.plot(names)
# %%

pd_mutag_ds: Dataset[Tuple[OneHotEncodedPersistenceDiagram, int]] = \
    PersistenceDiagramFromFiles(name_graph_dataset, 0.1)

pd: OneHotEncodedPersistenceDiagram = pd_mutag_ds[0][0]

pd.plot()


# Create the train/validation/test split

train_indices, test_indices = train_test_split(
    range(len(pd_mutag_ds)),
    test_size=0.2,
    random_state=42,
)

train_indices: List[int], validation_indices: List[int] = train_test_split(
    train_indices,
    test_size=0.2,
    random_state=42,
)

# Create the data loaders
train_dataset = Subset(pd_mutag_ds, train_indices)
validation_dataset = Subset(pd_mutag_ds, validation_indices)
test_dataset = Subset(pd_mutag_ds, test_indices)

# Preprocess the data
preprocessing_pipeline = PreprocessingPipeline(
    (ToTensorImage((32, 32)), Normalization()))
)

preprocessing_pipeline.fit_to_dataset(train_dataset)

train_dataset = preprocessing_pipeline.attach_transform_to_dataset(train_dataset)
validation_dataset = preprocessing_pipeline.attach_transform_to_dataset(validation_dataset)
test_dataset = preprocessing_pipeline.attach_transform_to_dataset(test_dataset)


# Build the data loaders
dl_builder = DataLoaderBuilder(train_dataset, validation_dataset, test_dataset)
dl_train ... = dl_builder.build

# Define the model
model_config = PersformerConfig(
    num_layers=6,
    num_heads=8,
    input_size=2 + num_homology_types,
)

model = Persformer(model_config)

writer = SummaryWriter()

loss_function = lambda logits, target: nn.CrossEntropyLoss()(logits, target)

trainer = Trainer(model, (train_dataset, validation_dataset, test_dataset), loss_function, writer)

trainer.train(SGD, 3, False, {"lr":0.01}, {"batch_size":16})

# %%
import numpy as np

# matrix of vectors of shape (num_vectors, dim_vector)
x = np.random.rand(10, 2)

# compute pairwise distances
dists = np.linalg.norm(x[:, np.newaxis, :] - x[np.newaxis, :, :], axis=-1)

 