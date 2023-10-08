import torch
from dataset import *
from modules import *
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import torchvision
import numpy as np
from torch.utils.data import random_split


#-------------
# Device Configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
if torch.cuda.is_available():
    print("Using GPU")
else:
    print("Warning, CUDA not found. Using CPU.")
print()

#---------------
# Hyper Parameters
learning_rate = 0.0005
num_epochs = 1

#-----------------
# Data configuration
batch_size = 50
train_set_proportion = 0.9

# Path parameters must be changed depending on where the dataset is located on the machine
path = r"c:\Users\Jackie Mann\Documents\Jarrod_Python\AD_NC"
save_path = r"c:\Users\Jackie Mann\Documents\Jarrod_Python\PatternAnalysis-2023\recognition\super_resolution_network_s4696612\saved_model.pth"
train_path = path + "\\train\\AD"
test_path = path + "\\test\\AD"

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(0.5, 0.5),
])

# Datasets and validation split
data = ImageDataset(directory=train_path,
                          transform=transform)
train_size = int(train_set_proportion * len(data))
valid_size = len(data) - train_size
train_data, validation_data = random_split(data, [train_size, valid_size])
test_data = ImageDataset(directory=test_path,
                         transform=transform)

# Data Loaders
train_loader = torch.utils.data.DataLoader(train_data,
                                           batch_size=batch_size,
                                           shuffle=True)
test_loader = torch.utils.data.DataLoader(test_data,
                                          batch_size=batch_size,
                                          shuffle=True)
valid_loader = torch.utils.data.DataLoader(validation_data,
                                           batch_size=batch_size,
                                           shuffle=True)
n_total_steps = len(train_loader)
batch = next(iter(train_loader))

#----------------------------
#Training
model = SuperResolution()
model.to(device)
model.train()

# Adam optimiser used for learning
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Mean squared error loss used for image comparisons
criterion = nn.MSELoss()

print("> Training.")
losses = []
validation_losses = []

# Training loop
for epoch in range(num_epochs):
    for i, (images, labels) in enumerate(train_loader):
        images = images.to(device)
        labels = labels.to(device)

        outputs = model(images)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        losses.append(loss.item())
        
        # Check validation set for overfitting
        with torch.no_grad():
            worst_loss = 0
            for j, (photos, names) in enumerate(valid_loader):
                photos = photos.to(device)
                names = names.to(device)

                out = model(photos)
                lose = criterion(out, names)
                if lose.item() > worst_loss:
                    worst_loss = lose.item()
            validation_losses.append(worst_loss)
        
        if (i + 1) % 10 == 0:
            print(f"Epoch [{epoch + 1}/{num_epochs}], Step [{i+1}/{n_total_steps}], Loss: {loss.item()}, Validation Loss: {lose.item()}")



#-------------------
# Model Finalisation
model.eval()

# Save trained pytorch model
torch.save(model.state_dict(), save_path)

# Show sample of model images
x = batch[0].to(device)[0]
y = model(x)
plt.figure(figsize=(8,8))
plt.axis('off')
plt.title('Model Images')
plt.imshow(np.transpose(torchvision.utils.make_grid(y, padding=2,normalize=True).cpu(), (1,2,0)))
plt.show()

# Show sample of goal images
plt.figure(figsize=(8,8))
plt.axis('off')
plt.title('Goal Images')
plt.imshow(np.transpose(torchvision.utils.make_grid(batch[1].to(device)[:64], padding=2,normalize=True).cpu(), (1,2,0)))
plt.show()

plt.figure()
plt.title('Training Loss')
plt.xlabel('Iterations')
plt.ylabel('Mean Squared Error Loss')
plt.plot(losses)
plt.plot(validation_losses)
plt.savefig('training_loss.png')
plt.show()