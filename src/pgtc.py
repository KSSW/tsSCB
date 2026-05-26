#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import sys

def correct_offset_generator_23_98():
    current = 1
    while True:
        for _ in range(4):
            yield current, "Odd"
            current += 2

        current = current - 2 + 1
        for _ in range(2):
            yield current, "Median"
            current += 2

        current = current - 1 + 1
        for _ in range(1):
            yield current, "Median"
            current += 2

        for _ in range(1):
            yield current, "Odd"
            current += 1

        for _ in range(1):
            yield current, "Odd"
            current += 2
        
        current = current - 1 + 1
        for _ in range(2):
            yield current, "Median"
            current += 2
        
        for _ in range(1):
            yield current, "Odd"
            current += 1

        for _ in range(1):
            yield current, "Odd"
            current += 2
            
        while True:
            current = current - 1 + 1
            for _ in range(2):
                yield current, "Median"
                current += 2

            for _ in range(1):
                yield current, "Odd"
                current += 1
                
            for _ in range(1):
                yield current, "Odd"
                current += 2
                
def correct_offset_generator_24():
    current = 1
    while True:
        for _ in range(4):
            yield current, "Odd"
            current += 1

        current = current - 1 + 1
        for _ in range(2):
            yield current, "Median"
            current += 1

        current = current - 1 + 1
        for _ in range(1):
            yield current, "Median"
            current += 1

        for _ in range(1):
            yield current, "Odd"
            current += 1

        for _ in range(1):
            yield current, "Odd"
            current += 1
        
        current = current - 1 + 1
        for _ in range(2):
            yield current, "Median"
            current += 1
        
        for _ in range(1):
            yield current, "Odd"
            current += 1

        for _ in range(1):
            yield current, "Odd"
            current += 1
            
        while True:
            current = current - 1 + 1
            for _ in range(2):
                yield current, "Median"
                current += 1

            for _ in range(1):
                yield current, "Odd"
                current += 1
                
            for _ in range(1):
                yield current, "Odd"
                current += 1

def correct_offset_generator_TC():
    current = 1
    while True:
        for _ in range(4):
            yield current, "Odd"
            current += 1

        current = current - 1 + 1
        for _ in range(2):
            yield current, "Median"
            current += 1

        current = current - 1 + 1
        for _ in range(1):
            yield current, "Median"
            current += 1

        for _ in range(1):
            yield current, "Odd"
            current += 1

        for _ in range(1):
            yield current, "Odd"
            current += 1

        current = current - 1 + 1
        for _ in range(2):
            yield current, "Median"
            current += 1

        for _ in range(1):
            yield current, "Odd"
            current += 1

        for _ in range(1):
            yield current, "Odd"
            current += 1

        while True:
            current = current - 1 + 1
            for _ in range(2):
                yield current, "Median"
                current += 1

            for _ in range(1):
                yield current, "Odd"
                current += 1

            for _ in range(1):
                yield current, "Odd"
                current += 1

def timecode_to_value_verbose_TC(timecode, fps=24, base=54000000, per_frame=3749, verbose=True):
    hh, mm, ss, ff = map(int, timecode.strip().split(":"))
    total_frames = ((hh * 3600 + mm * 60 + ss) * fps + ff)

    gen = correct_offset_generator_24()
    offset = (0, "no offset")

    for _ in range(total_frames):
        offset = next(gen)

    extra, offset_type = offset
    result = base + total_frames * per_frame + extra
    if verbose:
        print(f"[TC Start]{timecode} = {base} + {per_frame} * {total_frames} + offset{extra}（{offset_type}）= {result}")
    return result

def timecode_to_value_verbose(timecode, tc_start="00:00:00:00", fps=24, base=54000000, per_frame_24=3749, per_frame_23_98=3752, fps_mode_value=None):
    hh, mm, ss, ff = map(int, timecode.strip().split(":"))
    total_frames_23_98 = ((hh * 3600 + mm * 60 + ss) * fps + ff)
    total_frames_24 = ((hh * 3600 + mm * 60 + ss) * fps + ff)

    result_23_98 = None
    result_24 = None

    gen_23_98 = correct_offset_generator_23_98()
    offset_23_98 = (0, "no offset")

    gen_24 = correct_offset_generator_24()
    offset_24 = (0, "no offset")

    for _ in range(total_frames_23_98):
        offset_23_98 = next(gen_23_98)
        
    for _ in range(total_frames_24):
        offset_24 = next(gen_24)

    if fps_mode_value == '23.976':
        extra_23_98, offset_type_23_98 = offset_23_98
        if tc_start != "00:00:00:00":
            base_TC = timecode_to_value_verbose_TC(tc_start, verbose=False)
            result_23_98 = base_TC + total_frames_23_98 * per_frame_23_98 + extra_23_98
            print(f"[23.976fps][TC]{timecode} = {base_TC} + {per_frame_23_98} * {total_frames_23_98} + offset{extra_23_98}（{offset_type_23_98}）= {result_23_98}")
        else:
            result_23_98 = base + total_frames_23_98 * per_frame_23_98 + extra_23_98
            print(f"[23.976fps]{timecode} = {base} + {per_frame_23_98} * {total_frames_23_98} + offset{extra_23_98}（{offset_type_23_98}）= {result_23_98}")

    elif fps_mode_value == '24':    
        extra_24, offset_type_24 = offset_24
        if tc_start != "00:00:00:00":
            base_TC = timecode_to_value_verbose_TC(tc_start, verbose=False)
            result_24 = base_TC + total_frames_24 * per_frame_24 + extra_24
            print(f"[24fps][TC]{timecode} = {base_TC} + {per_frame_24} * {total_frames_24} + offset{extra_24}（{offset_type_24}）= {result_24}")
        else:
            result_24 = base + total_frames_24 * per_frame_24 + extra_24
            print(f"[24fps]{timecode} = {base} + {per_frame_24} * {total_frames_24} + offset{extra_24}（{offset_type_24}）= {result_24}")
    
    return result_23_98, result_24

def pg(sin=None, tc_start_timecode=None, file_path=None, ves_path=None):
    from mhz import parse_duration_from_ves_file, is_valid_timecode

    results_sin = []

    def log_output(sin, value, fps_mode):
        if fps_mode == '23.976':
            final_value = value[0]
            results_sin.append(f"{sin} = {value[0]}")
        elif fps_mode == '24':
            final_value = value[1]
            results_sin.append(f"{sin} = {value[1]}")
        else:
            print(f"{sin} = Unsupported FPS Mode")
            sys.exit(1)

        return final_value

    if ves_path:
        fps_mode = parse_duration_from_ves_file(ves_path)
        if fps_mode is None:
            print(f"Error: Unknown Frame Rate：{fps_mode}")
            sys.exit(1)
    else:
        return results_sin

    if is_valid_timecode(sin):
        value = timecode_to_value_verbose(sin, tc_start_timecode, fps_mode_value=fps_mode)
        final_value = log_output(sin, value, fps_mode)
    else:
        print(f"Error: Invalid Timecode Format：{sin}")
        sys.exit(1)

    return {"sin": sin, "value": final_value}