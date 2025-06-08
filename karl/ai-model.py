import cv2
import torch
from torchvision import transforms
from PIL import Image

# 1. Load model
model = torch.hub.load('pytorch/vision', 'fasterrcnn_resnet50_fpn', pretrained=True)
model.eval()

# 2. Preprocess frame
def preprocess(frame):
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    return transforms.ToTensor()(img)

# 3. Run inference & count people
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret: break
    input_tensor = preprocess(frame).unsqueeze(0)  # batch of 1
    with torch.no_grad():
        outputs = model(input_tensor)[0]
    # Filter for ‘person’ (COCO class 1) above a confidence threshold
    person_scores = [
        s.item() for lbl, s in zip(outputs['labels'], outputs['scores'])
        if lbl.item() == 1 and s.item() > 0.5
    ]
    count = len(person_scores)
    cv2.putText(frame, f'People: {count}', (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
