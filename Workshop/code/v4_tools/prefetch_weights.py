"""Download only the three V4 weights explicitly approved by the user."""
import hashlib
import json
from pathlib import Path
import socket
import time

import torch
from torchvision.models import MobileNet_V3_Small_Weights
from torchvision.models.detection import SSDLite320_MobileNet_V3_Large_Weights
from torchvision.models.segmentation import LRASPP_MobileNet_V3_Large_Weights


def main():
    socket.setdefaulttimeout(30)
    cache = Path(torch.hub.get_dir()) / "checkpoints"
    cache.mkdir(parents=True, exist_ok=True)
    evidence = []
    for weights in (
        MobileNet_V3_Small_Weights.IMAGENET1K_V1,
        SSDLite320_MobileNet_V3_Large_Weights.COCO_V1,
        LRASPP_MobileNet_V3_Large_Weights.COCO_WITH_VOC_LABELS_V1,
    ):
        filename = weights.url.rsplit("/", 1)[-1]
        dest = cache / filename
        prefix = filename.rsplit("-", 1)[-1].split(".")[0]
        if not dest.is_file():
            for attempt in range(3):
                try:
                    torch.hub.download_url_to_file(
                        weights.url, str(dest), hash_prefix=prefix, progress=False
                    )
                    break
                except Exception as exc:
                    print(f"{filename}: attempt {attempt + 1} failed: {exc}", flush=True)
                    if attempt == 2:
                        raise
                    time.sleep(2 * (attempt + 1))
        digest = hashlib.sha256(dest.read_bytes()).hexdigest()
        if not digest.startswith(prefix):
            raise RuntimeError(f"Checkpoint hash mismatch: {filename}")
        evidence.append({"weights": str(weights), "file": filename, "sha256": digest})
        print(f"Verified {filename}: {dest.stat().st_size} bytes", flush=True)
    out = Path(__file__).resolve().parents[1] / "v4_outputs"
    out.mkdir(exist_ok=True)
    (out / "download_manifest.json").write_text(json.dumps(evidence, indent=2))


if __name__ == "__main__":
    main()
