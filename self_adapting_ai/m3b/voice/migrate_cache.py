#!/usr/bin/env python3
"""Copy an index-named phrase cache (chNN_SSS.wav) to content-named files (chNN_<hash>.wav).
usage: migrate_cache.py <direction .md that PRODUCED the cache> <cache dir>   (originals are kept)"""
import os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from direction import direction_chapters
from generate_v3 import seg_key
D = direction_chapters(sys.argv[1]); cache = sys.argv[2]; n = miss = 0
for ch, segs in D.items():
    for i, seg in enumerate(segs):
        old = os.path.join(cache, f"ch{ch:02d}_{i:03d}.wav")
        if os.path.exists(old):
            shutil.copy2(old, os.path.join(cache, f"ch{ch:02d}_{seg_key(seg)}.wav")); n += 1
        else:
            miss += 1
print(f"migrated {n} phrases ({miss} had no cache file)")
