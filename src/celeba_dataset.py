from pathlib import Path
from PIL import Image
from torch.utils.data import Dataset


class CelebAHQDataset(Dataset):
    
    def __init__(self, data_dir, transform=None):
        self.data_dir = Path(data_dir)
        self.transform = transform

        if not self.data_dir.exists():
            raise FileNotFoundError(f"Dataset directory not found: {self.data_dir}")

        self.image_paths = sorted(
            list(self.data_dir.glob("*.jpg")) +
            list(self.data_dir.glob("*.jpeg")) +
            list(self.data_dir.glob("*.png"))
        )

        if len(self.image_paths) == 0:
            raise ValueError(f"No images found in {self.data_dir}")

        print(f"Loaded {len(self.image_paths)} images from {self.data_dir}")

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = Image.open(self.image_paths[idx]).convert("RGB")

        if self.transform:
            image = self.transform(image)

        return {"images": image}