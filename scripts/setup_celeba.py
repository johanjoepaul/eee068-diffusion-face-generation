from pathlib import Path
import shutil
import kagglehub

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TARGET = PROJECT_ROOT / "celeba_hq_256"

print("Downloading CelebA-HQ 256x256 dataset...")
download_path = Path(kagglehub.dataset_download("badasstechie/celebahq-resized-256x256"))
print("Downloaded to:", download_path)

image_extensions = {".jpg", ".jpeg", ".png"}

candidate_dirs = []
for folder in [download_path] + [p for p in download_path.rglob("*") if p.is_dir()]:
    images = [p for p in folder.iterdir() if p.suffix.lower() in image_extensions]
    if len(images) >= 3000:
        candidate_dirs.append((folder, len(images)))

if not candidate_dirs:
    raise RuntimeError("No folder with at least 3000 images was found in the downloaded dataset.")

source_dir, image_count = max(candidate_dirs, key=lambda item: item[1])

print("Using image folder:", source_dir)
print("Images found:", image_count)

if TARGET.exists():
    print("celeba_hq_256 already exists. Leaving it unchanged.")
else:
    try:
        TARGET.symlink_to(source_dir, target_is_directory=True)
        print(f"Created symlink: {TARGET} -> {source_dir}")
    except Exception:
        print("Symlink failed. Copying first 3000 images instead.")
        TARGET.mkdir(parents=True, exist_ok=True)

        images = sorted(
            [p for p in source_dir.iterdir() if p.suffix.lower() in image_extensions]
        )[:3000]

        for image_path in images:
            shutil.copy2(image_path, TARGET / image_path.name)

        print(f"Copied {len(images)} images to {TARGET}")

print("CelebA-HQ setup complete.")
print("Dataset folder ready at:", TARGET)