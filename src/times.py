#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys

def parse_duration_from_ves_file(file_path, dv_file_path=None):
    duration_value_0 = fps_mode_1 = fps_code_1 = tc_start_timecode_2 = None
    duration_value_dv = fps_mode_dv = fps_code_dv = tc_start_timecode_dv = None
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

            duration_match = re.search(r'Duration\[0]=(\d+)', content)
            fps_match = re.search(r'XML\.frame_rate=(\d+)', content)
            match = re.search(
                r'TC_StartTime_Hours=(\d+).*?TC_StartTime_Minutes=(\d+).*?TC_StartTime_Seconds=(\d+).*?TC_StartTime_Frames=(\d+)',
                content,
                re.DOTALL
            )

            if not duration_match:
                raise ValueError("Duration[0] not found in VES file.")
            if not fps_match:
                raise ValueError("XML.frame_rate not found in VES file.")
            if not match:
                raise ValueError("XML.TC_StartTime... not found in VES file.")

            duration_value_0 = int(duration_match.group(1))
            fps_code_1 = int(fps_match.group(1))
            h, m, s, f = match.groups()
            tc_start_timecode_2 = f"{h.zfill(2)}:{m.zfill(2)}:{s.zfill(2)}:{f.zfill(2)}"

            if fps_code_1 == 1:
                fps_mode_1 = '23.976'
            elif fps_code_1 == 2:
                fps_mode_1 = '24'
            else:
                print(f"Error: Unsupported frame rate code: {fps_code_1}")

    except FileNotFoundError:
        print(f"Error: File not found: {dv_file_path}")
        sys.exit(1)
    if dv_file_path:
        try:
            with open(dv_file_path, 'r', encoding='utf-8') as dv_file:
                content = dv_file.read()

                duration_match = re.search(r'Duration\[0]=(\d+)', content)
                fps_match = re.search(r'XML\.frame_rate=(\d+)', content)
                match = re.search(
                    r'TC_StartTime_Hours=(\d+).*?TC_StartTime_Minutes=(\d+).*?TC_StartTime_Seconds=(\d+).*?TC_StartTime_Frames=(\d+)',
                    content,
                    re.DOTALL
                )

                if not duration_match:
                    raise ValueError("Duration[0] not found in VES file.")
                if not fps_match:
                    raise ValueError("XML.frame_rate not found in VES file.")
                if not match:
                    raise ValueError("XML.TC_StartTime... not found in VES file.")

                duration_value_dv = int(duration_match.group(1))
                fps_code_dv = int(fps_match.group(1))
                h, m, s, f = match.groups()
                tc_start_timecode_dv = f"{h.zfill(2)}:{m.zfill(2)}:{s.zfill(2)}:{f.zfill(2)}"

                if fps_code_dv == 1:
                    fps_mode_dv = '23.976'
                elif fps_code_dv == 2:
                    fps_mode_dv = '24'
                else:
                    print(f"Error: Unsupported frame rate code: {fps_code_dv}")

        except FileNotFoundError:
            print(f"Error: File not found: {dv_file_path}")
            sys.exit(1)

    return (
    duration_value_0, fps_mode_1, fps_code_1, tc_start_timecode_2,
    duration_value_dv, fps_code_dv, fps_mode_dv, tc_start_timecode_dv
)

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

def timecode_to_value_verbose(timecode_main, fps=24, per_frame_24=3749, per_frame_23_98=3752):
    hh, mm, ss, ff = map(int, timecode_main.strip().split(":"))
    total_frames_23_98 = ((hh * 3600 + mm * 60 + ss) * fps + ff)
    total_frames_24 = ((hh * 3600 + mm * 60 + ss) * fps + ff)

    gen_23_98 = correct_offset_generator_23_98()
    offset_23_98 = (0, "no offset")

    gen_24 = correct_offset_generator_24()
    offset_24 = (0, "no offset")

    for _ in range(total_frames_23_98):
        offset_23_98 = next(gen_23_98)

    for _ in range(total_frames_24):
        offset_24 = next(gen_24)

    extra_23_98, offset_type_23_98 = offset_23_98
    result_23_98 = total_frames_23_98 * per_frame_23_98 + extra_23_98
    print(
        f"[23.976fps]{timecode_main} = {per_frame_23_98} * {total_frames_23_98} + offset{extra_23_98}（{offset_type_23_98}）= {result_23_98}")

    extra_24, offset_type_24 = offset_24
    result_24 = total_frames_24 * per_frame_24 + extra_24
    print(
        f"[24fps]{timecode_main} = {per_frame_24} * {total_frames_24} + offset{extra_24}（{offset_type_24}）= {result_24}")

    return result_23_98, result_24

def value_to_timecode(result_value, fps_mode_value='', label=''):
    if fps_mode_value == '23.976':
        per_frame = 3752
        fps = 24
        gen = correct_offset_generator_23_98()
    elif fps_mode_value == '24':
        per_frame = 3749
        fps = 24
        gen = correct_offset_generator_24()
    else:
        print("fps_mode_value must be 23.976、24")
        return None
    frame_index = 1

    while True:
        extra_offset, offset_type = next(gen)
        test_value = frame_index * per_frame + extra_offset

        if test_value >= result_value:
            print(f"[{label}] {test_value}，result: {result_value}，Error: {abs(test_value - result_value)}")
            print(f"[{label} {fps_mode_value}fps] ≈ frame({frame_index}) * {per_frame} + offset({extra_offset})（{offset_type}）")
            break

        frame_index += 1

    hh = frame_index // (3600 * fps)
    mm = (frame_index % (3600 * fps)) // (60 * fps)
    ss = (frame_index % (60 * fps)) // fps
    ff = frame_index % fps

    return f"{hh:02d}:{mm:02d}:{ss:02d}:{ff:02d}"

def args_parser(file_path, dv_file_path=None):
    
    result = {}
    try:
        parsed = parse_duration_from_ves_file(file_path, dv_file_path)
        if parsed:
            duration_value, fps_mode, fps_code, tc_start_timecode, \
            duration_value_dv, fps_code_dv, fps_mode_dv, tc_start_timecode_dv = parsed

        if duration_value and fps_mode:
            timecode = value_to_timecode(duration_value, fps_mode, label='Main')
            result["tc_start_timecode"] = tc_start_timecode
            result["timecode"] = timecode
            result["fps"] = str(fps_mode)
            result["fps_code"] = fps_code

        if dv_file_path and duration_value_dv and fps_mode_dv:
                timecode_dv = value_to_timecode(duration_value_dv, fps_mode_dv, label='DV')
                result["tc_start_timecode_dv"] = tc_start_timecode_dv
                result["timecode_dv"] = timecode_dv
                result["fps_dv"] = str(fps_mode_dv)
                result["fps_code_dv"] = fps_code_dv

        return result if result else None

    except Exception as e:
        print(f"Error: {e}")
        return None