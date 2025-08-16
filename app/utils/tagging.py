from PIL import Image
from torchvision import models, transforms
from torchvision.models import ResNet18_Weights
import torch
import json

# Load ImageNet labels
with open('imagenet_class_index.json') as f:
    idx_to_label = {int(key): value[1] for key, value in json.load(f).items()}

model = models.resnet18(weights=ResNet18_Weights.DEFAULT)
model.eval()

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def get_image_tags(img: Image):
    img_t = preprocess(img).unsqueeze(0)
    with torch.no_grad():
        out = model(img_t)
    _, indices = torch.topk(out, 3)
    if img.mode != "RGB":
        img = img.convert("RGB")
    print("Keys available:", list(idx_to_label.keys())[:20], "...", list(idx_to_label.keys())[-20:])
    print("Trying to access:", [str(idx.item()) for idx in indices[0]])
    tags = []
    for idx in indices[0]:
        key = str(idx.item())
        if key in idx_to_label:
            tags.append(idx_to_label[key])
        else:
            print(f"Warning: Key {key} not found in imagenet_class_index.json")
            tags.append(("unknown", "unknown"))
    return tags
