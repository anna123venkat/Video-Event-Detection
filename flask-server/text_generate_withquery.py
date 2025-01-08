import torch
import os
import json
from transformers import pipeline
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import torchvision.transforms as transforms
from transformers import BlipProcessor, BlipForConditionalGeneration


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

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to("cuda")
def generate(path, query):
    path = path
    img_paths = [os.path.join(path, img) for img in os.listdir(path)]
    dataset = ImageDataset(img_paths, transform=transform)
    dataloader = DataLoader(dataset, batch_size=8, shuffle=False)
    texts = []
    for batch_images, batch_paths in dataloader:
        for img_path in batch_paths:
            inputs = processor(Image.open(img_path).convert("RGB"), query, return_tensors="pt").to("cuda")
            out = model.generate(**inputs)
            text = processor.decode(out[0], skip_special_tokens=True)
            print(text)
            texts.append(text)
    return texts
