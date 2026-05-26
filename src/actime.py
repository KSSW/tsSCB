#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import argparse
import time
from typing import List

FRAME_RATES: List[float] = [
    23.976, 24, 25, 29.97,
    59.94, 60
]

# DROP_FRAME = {29.97, 59.94}

def format_fps(fps) -> str:
    fps = float(fps)
    if fps.is_integer():
        return str(int(fps))
    else:
        return str(fps)

def ms_to_smpte(ms: int, fps: float, df) -> str:
    neg = ms < 0
    ms = abs(int(ms))
    ms = ms % 86_400_000

    if df and fps not in (29.97, 59.94):
        print("Not Supported Frame Rate(Supported Frame Rate Only: 29.97, 59.94)")
        exit(1)

    if df and fps == 29.97 or fps == 59.94:
        fps_int = round(fps)

        minutes = ms // 60000
        tens = minutes // 10

        ms = int(0.999001 * ms + ((minutes - tens) * 2002 / fps_int))

        hours = ms // 3_600_000
        minutes = (ms % 3_600_000) // 60_000
        seconds = (ms % 60_000) // 1000
        frames = int(((ms % 1000) * fps) // 1000)

        s = f"{hours:02d}:{minutes:02d}:{seconds:02d};{frames:02d}"
        return f"-{s}" if neg else s

    else:
        if fps in (23.976, 29.97, 59.94):
            ms = int(0.999001 * ms + 1000.0 / fps)

        hours = ms // 3_600_000
        minutes = (ms % 3_600_000) // 60_000
        seconds = (ms % 60_000) // 1000
        frames = int(((ms % 1000) * fps) // 1000)

        s = f"{hours:02d}:{minutes:02d}:{seconds:02d}:{frames:02d}"
        return f"-{s}" if neg else s

def parse_srt(filepath: str) -> List[tuple[int, int]]:
    pattern = re.compile(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})")
    results = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            matches = pattern.findall(line)
            if len(matches) == 2:
                (h1, m1, s1, ms1), (h2, m2, s2, ms2) = matches
                start_ms = int(h1) * 3600_000 + int(m1) * 60_000 + int(s1) * 1000 + int(ms1)
                end_ms   = int(h2) * 3600_000 + int(m2) * 60_000 + int(s2) * 1000 + int(ms2)
                results.append((start_ms, end_ms))
    return results

def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-i", metavar='', type=str, required=True, help="Input SRT File")
    parser.add_argument("-fps", metavar='', type=float, choices=FRAME_RATES, required=True, help="Frame Rate (Supported: 23.976, 24, 25, 29.97/(Drop Frame), 59.94/(Drop Frame), 60)")
    parser.add_argument("-df", action='store_true', help="Enable Drop Frame (Supported Frame Rate Only: 29.97, 59.94)")
    args = parser.parse_args()

    entries = parse_srt(args.i)

    ff = format_fps(args.fps)

    smpte_events = []
    for idx, (start_ms, end_ms) in enumerate(entries, start=1):
        inTC = ms_to_smpte(start_ms, args.fps, args.df)
        outTC = ms_to_smpte(end_ms, args.fps, args.df)
        smpte_events.append((idx, inTC, outTC))

if __name__ == "__main__":
    main()