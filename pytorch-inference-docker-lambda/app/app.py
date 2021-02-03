import urllib
import json
import os

import torch
from PIL import Image
from torchvision import transforms


transform_test = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])


def handler(event, context):
    print('Received event: ' + json.dumps(event, indent=2))
    url = event['url']

    img = Image.open(urllib.request.urlopen(url))
    scaled_img = transform_test(img)
    torch_image = scaled_img.unsqueeze(0)

    model = torch.jit.load('./resnet34.pt')
    predicted_class = model(torch_image).argmax().item()
    print('predicted_class: {}'.format(predicted_class))

    # Read the categories
    with open("imagenet_classes.txt", "r") as f:
        categories = [s.strip() for s in f.readlines()]

    print('Categories count: {}'.format(len(categories)))

    return json.dumps({
        "class": categories[predicted_class]
    })
