import torch
import torch.nn as nn

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

if __name__ == '__main__':
    BATCH_SIZE = 4
    x = torch.randn(BATCH_SIZE, 1, 90, 25)
    print(x)
    #model = Model()
    #out = model(x)
    #print(out)