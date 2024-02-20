import torch
import torch.nn as nn
import numpy as np
import cv2
from torch.autograd import Variable
from torchvision import transforms

class Model(nn.Module):
    def __init__(self, num_classes=36, num_chars=4):
        super(Model, self).__init__()
        # image size = 90 * 25
        # batch * 1 * 90 * 25

        self.conv = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=(1, 1)), # batch * 32 * 90 * 25
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Dropout2d(0.25),
            nn.Conv2d(32, 128, 3, padding=(1, 1)), # batch * 128 * 90 * 25
            nn.MaxPool2d(2, 2), # batch * 128 * 45 * 12
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Dropout2d(0.25),
            nn.Conv2d(128, 256, 3, padding=(1, 1)), # batch * 256 * 45 * 12
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.Dropout2d(0.5),
            nn.Conv2d(256, 256, 3, padding=(1, 1)),
            nn.MaxPool2d(2, 2), # batch * 256 * 22 * 6
            nn.BatchNorm2d(256),
            nn.Dropout2d(0.25),
            nn.ReLU(),
        )

        self.fc = nn.Linear(256 * 22 * 6, num_classes * num_chars)
        
    def forward(self, x):
        x = self.conv(x)
        x = x.view(-1, 256 * 22 * 6)
        x = self.fc(x)
        return x

class CaptchaRecognizer:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = Model()
        self.model.load_state_dict(torch.load('CaptchaRecognition/model_state_dict.pth', map_location=self.device))
        self.model.eval()
        self.model.to(self.device)
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Lambda(self.rpt)
        ])
        self.charset = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.charset_dict = {char: i for i, char in enumerate(self.charset)}

    def rpt(self, x):
        return x.repeat(1, 1, 1)

    def _preprocess_img(self, img: cv2.Mat) -> cv2.Mat:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        img = np.expand_dims(img, axis=2)
        img = cv2.resize(img, (90, 25))
        # show img
        #cv2.imshow('img', img)
        #cv2.waitKey(0)
        return self.transform(img)

    def _transform(self, img: cv2.Mat) -> torch.Tensor:
        img = self._preprocess_img(img)
        img = self.transform(img)
        return img

    def recognize(self, img: cv2.Mat):
        img = self._preprocess_img(img)
        with torch.no_grad():
            inputs = torch.tensor(img, dtype=torch.float32)
            inputs = inputs.unsqueeze(0)
            inputs = Variable(inputs.to(self.device))
            outputs = self.model(inputs)
            outputs = outputs.view(-1, 36)
            outputs = nn.functional.softmax(outputs, dim=1)
            outputs = torch.argmax(outputs, dim=1)
            outputs = outputs.view(-1, 4)
        
        return ''.join([self.charset[i] for i in outputs[0]])