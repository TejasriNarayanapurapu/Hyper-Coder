from dataset import load_data
from utils import preprocess

def train():
    data = load_data()
    data = preprocess(data)
    for epoch in range(3):
        print(f"Epoch {epoch+1}: Training with {len(data)} samples")

if __name__ == "__main__":
    train()
