from fastapi import FastAPI, UploadFile, File
import torch
from torchvision import transforms
from PIL import Image
import io

from main import Net  # As the model is defined in main.py
app = FastAPI()
model = Net()
model.load_state_dict(torch.load("mnist_cnn.pt", map_location=torch.device('cpu')))
model.eval()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    img = Image.open(io.BytesIO(await file.read())).convert("L")
    transform = transforms.Compose([
        transforms.Resize((28, 28)),
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    img_tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        output = model(img_tensor)
        prediction = output.argmax(1).item()
    return {"prediction": prediction}