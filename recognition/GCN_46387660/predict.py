import torch
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import dataset
import modules

transform = TSNE


PATH = "model.pt"

data = dataset.dataset


# show untrained nodes
model_new = modules.GCN(in_channels=128, num_classes=4)
model_new.eval()
out = model_new(data.x, data.edge_index)

z_untrained = TSNE(n_components=2).fit_transform(out.detach().cpu().numpy())
print("computed untrained")

# show trained nodes
model_load = torch.load(PATH)

model_load.eval()

out = model_load(data.x, data.edge_index)

z_trained = TSNE(n_components=2).fit_transform(out.detach().cpu().numpy())
print("computed trained")

figure, axis = plt.subplots(1,2)

axis[0].scatter(z_untrained[:,0], z_untrained[:, 1], s=60, c=data.y, marker=".",cmap="Set2", alpha=0.5)
axis[0].set_title("Untrained GCN")

axis[1].scatter(z_trained[:,0], z_trained[:, 1], s=60, c=data.y, marker=".",cmap="Set2", alpha=0.5)
axis[1].set_title("Trained GCN")

plt.setp(plt.gcf().get_axes(), xticks=[], yticks=[])

plt.show()