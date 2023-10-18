import torch
import torch.nn as nn
import modules
import dataset
import time

NUM_EPOCHS = 100
# Placeholder for now
PATH = "model.pt"

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
if not torch.cuda.is_available():
    print("Warning CUDA not Found. Using CPU")

# get model (GCN)
model = modules.GCN(in_channels=128, num_classes=4)
model = model.to(device)

# get dataset
data = dataset.dataset

print('starting test')

# Set optimizer and criterion
optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
criterion = torch.nn.CrossEntropyLoss()

# Train the model
model.train()
start = time.time()
for epoch in range(NUM_EPOCHS):
    optimizer.zero_grad()
    out = model(data.x, data.edge_index)
    loss = criterion(out[data.train_mask], data.y[data.train_mask])
    loss.backward()
    optimizer.step()

    if (epoch % 10 == 0):
        print(f'Epoch {epoch:>3} | Loss: {loss:.2f}\n', flush=True)
        

end = time.time()
elapsed = end - start
print("Training took " + str(elapsed) + " secs or " + str(elapsed/60) + " mins in total")

# Test the model
model.eval()
start = time.time()

out = model(data.x, data.edge_index)
pred = out.argmax(dim=1)
test_correct = (pred[data.test_mask] == data.y[data.test_mask]).sum()
test_acc = int(test_correct) / int(data.test_mask.sum().item()) 
print("Test Accuracy: " + str(test_acc))
    
# Save the model to model.pt
torch.save(model,PATH)


