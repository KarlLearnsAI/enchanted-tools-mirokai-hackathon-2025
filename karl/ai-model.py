import cv2
import torch
from torchvision import transforms
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from PIL import Image

# 1. Load model
model = fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

# 2. Preprocess function
def preprocess(frame):
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    return transforms.ToTensor()(img)

# 3. Load single image
path = "frames/exhibit_2162.png"
frame = cv2.imread(path)
if frame is None:
    raise FileNotFoundError(f"Image not found at: {path}")

# 4. Run inference
input_tensor = preprocess(frame).unsqueeze(0)
with torch.no_grad():
    outputs = model(input_tensor)[0]

# 5. Count people (label == 1 in COCO)
person_scores = [
    s.item() for lbl, s in zip(outputs['labels'], outputs['scores'])
    if lbl.item() == 1 and s.item() > 0.5
]
count = len(person_scores)

# 6. Draw results
cv2.putText(frame, f'People: {count}', (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# 7. Show image
cv2.imshow('frame', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()