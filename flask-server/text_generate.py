import torch
import os
import json
from transformers import pipeline
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import torchvision.transforms as transforms

class ImageDataset(Dataset):
    def __init__(self, img_paths, transform=None):
        self.img_paths = img_paths
        self.transform = transform

    def __len__(self):
        return len(self.img_paths)

    def __getitem__(self, idx):
        img_path = self.img_paths[idx]
        image = Image.open(img_path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image, img_path


transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

model = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large", device="cuda")
def generate(path, query):
    img_paths = [os.path.join(path, img) for img in os.listdir(path)]
    dataset = ImageDataset(img_paths, transform=transform)
    dataloader = DataLoader(dataset, batch_size=8, shuffle=False)
    texts = []
    for batch_images, batch_paths in dataloader:
        batch_texts = model([img_path for img_path in batch_paths])
        for text_dict in batch_texts:
            generated_text = text_dict[0]['generated_text']
            print(generated_text)
            texts.append(generated_text)
    return texts
