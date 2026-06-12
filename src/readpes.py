#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import struct
import statistics
from pgtc_ms_ues import pg, mstovalue
from pathlib import Path
from typing import List, Optional
from fractions import Fraction

CLOCK = 90000.0
TSOFFSET_MUIES = 54000000

FRAME_RATES= {
    1: Fraction(23.976),
    2: Fraction(24),       
    3: Fraction(25),       
    4: Fraction(29.97), 
    7: Fraction(59.94), 
    8: Fraction(60),        
}

DROP_FRAME = {29.97, 59.94}

def format_fps(fps) -> str:
    fps = float(fps)
    if fps.is_integer():
        return str(int(fps))
    else:
        return str(fps)

def ticks_to_ms(ticks: int) -> int:
    if ticks < 0:
        ticks = 0
    return round(ticks / 90.0)

def ms_to_smpte(ms: int, fps: float, df: bool = False) -> str:
    neg = ms < 0
    ms = abs(int(ms))
    ms = ms % 86_400_000

    if df and fps not in (29.97, 59.94):
        raise ValueError("Drop-frame only supports 29.97 and 59.94 fps")

    if df and fps in (29.97, 59.94):
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

class TSContext:
    def __init__(self):
        self.carry = 0
        self.prev_dts = -1 * CLOCK

    def get_full_range(self, pts, dts):
        self.carry += (self.prev_dts > dts)
        self.prev_dts = dts
        return (self.carry * (1 << 33)) + dts, (self.carry * (1 << 33)) + pts

class MuiDecoder:
    def __init__(self, mui_file: str, pes_file: str, fps: float, drop_frame: bool = False, tc_start_timecode=None):
        self.mui_file = Path(mui_file)
        self.pes_file = Path(pes_file)
        self.fps = float(fps)
        self.drop_frame = drop_frame
        self.tc_start_timecode = tc_start_timecode

        code = self.read_pes_code()
        self.code = code 
        fps_val = self.code_to_fps(code)
        self.detected_fps = fps_val

        if self.detected_fps:
            self.fps = self.detected_fps
        else:
            self.fps = float(fps)

    def read_pes_code(self) -> int:
        try:
            with open(self.pes_file, "rb") as f:
                data = f.read(12)
            if len(data) < 8:
                print(f"Error : An error occurred when reading the ES file. (readed size is incorrect): {self.mui_file}")
                sys.exit(1)
            b7 = data[7]
            code = (b7 >> 4) & 0x0F
            return int(code)
        except Exception as e:
            print("Error : Decode failed.")
            sys.exit(1)

    def code_to_fps(self, code: int):
        frac = FRAME_RATES.get(code)
        return frac

    def get_first_time(self, smpte: bool = True) -> tuple:
        with open(self.mui_file, "rb") as f:
            f.read(4)

            entry = f.read(14)
            if len(entry) < 14:
                print("Error: The file does not contain a valid segment.")
                sys.exit(1)

            num = ((entry[9] & 0x7F) << 26) \
                | (entry[10] << 18) \
                | (entry[11] << 10) \
                | (entry[12] << 2) \
                | (entry[13] >> 6)

            pts = num - TSOFFSET_MUIES
            ms = ticks_to_ms(pts)
            value = mstovalue(ms, self.tc_start_timecode)

            if smpte:
                tc_str = ms_to_smpte(ms, self.fps, self.drop_frame)
            else:
                h, r = divmod(ms, 3600_000)
                m, r = divmod(r, 60_000)
                s, ms = divmod(r, 1000)
                tc_str = f"{h:02}:{m:02}:{s:02},{ms:03}"

            return tc_str, ms

def sin(mui_path: str, pes_path: str, fps: float, drop_frame: bool = False, tc_start_timecode=None) -> tuple:
    return_tc = MuiDecoder(mui_path, pes_path, fps=float(fps), drop_frame=drop_frame, tc_start_timecode=tc_start_timecode)
    return return_tc.get_first_time()