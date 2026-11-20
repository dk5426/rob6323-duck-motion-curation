"""Load the motion clips and list them by split.

    python load_clips.py            # summary
    python load_clips.py <clip id>  # one clip's arrays and metadata
"""

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def load(root=os.path.join(HERE, "data")):
    """Returns (arrays, manifest). Clip c's frames are arrays[key][c["index"], :c["length"]]."""
    arrays = dict(np.load(os.path.join(root, "library.npz")))
    manifest = json.load(open(os.path.join(root, "manifest.json")))
    return arrays, manifest


def clip(arrays, entry):
    """The arrays of one clip, trimmed to its length."""
    i, n = entry["index"], entry["length"]
    return {k: v[i, :n] for k, v in arrays.items() if k != "length"}


def main():
    arrays, man = load()
    clips = man["clips"]
    if len(sys.argv) > 1:
        entry = next(c for c in clips if c["id"] == sys.argv[1])
        for k, v in clip(arrays, entry).items():
            print(f"{k:10s} {v.shape}")
        print(json.dumps({k: entry[k] for k in ("id", "category", "split", "params", "feasibility") if k in entry}, indent=1))
        return
    print(f"{len(clips)} clips at {man['fps']} Hz; joints: {', '.join(man['joints'])}")
    for split in ("train", "val", "test"):
        cs = [c for c in clips if c["split"] == split]
        broken = sum(c.get("feasibility", {}).get("corrupted", False) for c in cs)
        print(f"  {split:5s} {len(cs):3d} clips ({broken} broken)")


if __name__ == "__main__":
    main()
