import io

import numpy as np
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
from PIL import Image
from torch import nn


class CDNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(
            in_channels=3, out_channels=16, kernel_size=(5, 5), stride=2, padding=1
        )
        self.conv2 = nn.Conv2d(
            in_channels=16, out_channels=32, kernel_size=(5, 5), stride=2, padding=1
        )
        self.conv3 = nn.Conv2d(
            in_channels=32, out_channels=64, kernel_size=(3, 3), padding=1
        )
        self.fc1 = nn.Linear(in_features=64 * 6 * 6, out_features=500)
        self.fc2 = nn.Linear(in_features=500, out_features=50)
        self.fc3 = nn.Linear(in_features=50, out_features=4)

    def forward(self, X):
        X = F.relu(self.conv1(X))
        X = F.max_pool2d(X, 2)
        X = F.relu(self.conv2(X))
        X = F.max_pool2d(X, 2)
        X = F.relu(self.conv3(X))
        X = F.max_pool2d(X, 2)
        #         print(X.shape)
        X = X.view(X.shape[0], -1)
        X = F.relu(self.fc1(X))
        X = F.relu(self.fc2(X))
        X = self.fc3(X)
        #         X = torch.sigmoid(X)
        return X


def transform_image(image_bytes):
    my_transforms = transforms.Compose(
        [
            transforms.Resize((256, 256)),
            transforms.CenterCrop((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize((0.5), (0.5)),
        ]
    )
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)


def get_prediction_MNIST(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    model = torch.load("covid_.pth")
    with torch.no_grad():
        logits = model.forward(tensor)
    prob = F.softmax(logits, dim=1)
    y = prob.detach()[0].numpy()
    x = [x for x in range(12)]
    dict = {}
    for a, b in zip(x, y):
        dict[a] = b
    return dict
