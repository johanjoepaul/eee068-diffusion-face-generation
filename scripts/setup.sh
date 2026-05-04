#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python scripts/setup_celeba.py

python -m ipykernel install --user --name diffusion-celeb --display-name "diffusion-celeb"

echo "Setup complete!"