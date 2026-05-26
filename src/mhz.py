#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import csv

def parse_duration_from_ves_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    with open(file_path, 'r', encoding='utf-8') as file:
        if ext == '.csv':
            first_line = file.readline().strip()

            if re.match(r'^\d{2}(\.\d+)?', first_line):
                fps_value = first_line.split(',')[0]
                if fps_value in ['23.976', '24']:
                    return fps_value
                else:
                    print(f"Error: Unsupported Frame Rate: {fps_value}")

        elif ext == '.ves':
            file.seek(0)
            content = file.read()
            fps_match = re.search(r'XML\.frame_rate=(\d+)', content)

            if not fps_match:
                raise ValueError("XML.frame_rate not found in VES file.")

            fps_code_0 = int(fps_match.group(1))

            if fps_code_0 == 1:
                fps_mode_0 = '23.976'
            elif fps_code_0 == 2:
                fps_mode_0 = '24'
            else:
                print(f"Error: Unsupported Frame Rate Code: {fps_code_0}")
        else:
             return None
     
        return fps_mode_0

def correct_offset_generator_24():
    current = 1
    while True:
        for _ in range(8):
            yield current, "Odd"
            current += 1

        current = current - 1 + 1
        for _ in range(3):
            yield current, "Median"
            current += 1

        for _ in range(5):
            yield current, "Even"
            current += 1

        current = current - 1 + 1
        for _ in range(3):
            yield current, "Median"
            current += 1

        for _ in range(5):
            yield current, "Odd"
            current += 1

        while True:
            current = current - 1 + 1
            for _ in range(3):
                yield current, "Median"
                current += 1

            for _ in range(5):
                yield current, "Even"
                current += 1

def correct_offset_generator_23_98():
    current = 1
    while True:
        for _ in range(8):
            yield current, "Odd"
            current += 2

        current = current - 2 + 1
        for _ in range(3):
            yield current, "Median"
            current += 2

        for _ in range(5):
            yield current, "Even"
            current += 2

        current = current - 2 + 1
        for _ in range(3):
            yield current, "Median"
            current += 2

        for _ in range(5):
            yield current, "Odd"
            current += 2

        while True:
            current = current - 2 + 1
            for _ in range(3):
                yield current, "Median"
                current += 2

            for _ in range(5):
                yield current, "Even"
                current += 2

def correct_offset_generator_tc():
    current = 1
    while True:
        for _ in range(8):
            yield current, "Odd"
            current += 1

        current = current - 1 + 1
        for _ in range(3):
            yield current, "Median"
            current += 1

        for _ in range(5):
            yield current, "Even"
            current += 1

        current = current - 1 + 1
        for _ in range(3):
            yield current, "Median"
            current += 1

        for _ in range(5):
            yield current, "Odd"
            current += 1

        while True:
            current = current - 1 + 1
            for _ in range(3):
                yield current, "Median"
                current += 1

            for _ in range(5):
                yield current, "Even"
                current += 1

def timecode_to_value_verbose_tc(timecode, fps=24, base=27000000, per_frame=1874, verbose=True):
    hh, mm, ss, ff = map(int, timecode.strip().split(":"))
    total_frames = ((hh * 3600 + mm * 60 + ss) * fps + ff)

    gen = correct_offset_generator_tc()
    offset = (0, "no offset")

    for _ in range(total_frames):
        offset = next(gen)

    extra, offset_type = offset
    result = base + total_frames * per_frame + extra
    if verbose:
        print(f"[TC Start]{timecode} = {base} + {per_frame} * {total_frames} + offset{extra}（{offset_type}）= {result}")
    return result

def timecode_to_value_verbose(timecode, tc_start="00:00:00:00", fps=24, base=27000000, per_frame_24=1874 , per_frame_23_98=1875, fps_mode_value=None):
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
           base_tc = timecode_to_value_verbose_tc(tc_start, verbose=False)
           result_23_98 = base_tc + total_frames_23_98 * per_frame_23_98 + extra_23_98
           print(f"[23.976fps][TC]{timecode} = {base_tc} + {per_frame_23_98} * {total_frames_23_98} + offset{extra_23_98}（{offset_type_23_98}）= {result_23_98}")
       else:
           result_23_98 = base + total_frames_23_98 * per_frame_23_98 + extra_23_98
           print(f"[23.976fps]{timecode} = {base} + {per_frame_23_98} * {total_frames_23_98} + offset{extra_23_98}（{offset_type_23_98}）= {result_23_98}")

    elif fps_mode_value == '24':
         extra_24, offset_type_24 = offset_24

         if tc_start != "00:00:00:00":
             base_tc = timecode_to_value_verbose_tc(tc_start, verbose=False)
             result_24 = base_tc + total_frames_24 * per_frame_24 + extra_24
             print(f"[24fps][TC]{timecode} = {base_tc} + {per_frame_24} * {total_frames_24} + offset{extra_24}（{offset_type_24}）= {result_24}")
         else:
             result_24 = base + total_frames_24 * per_frame_24 + extra_24
             print(f"[24fps]{timecode} = {base} + {per_frame_24} * {total_frames_24} + offset{extra_24}（{offset_type_24}）= {result_24}")
    else:
        print(f"fps_mode_value: Invalid value")

    return result_23_98, result_24

def is_valid_timecode(start_tc):
    return re.match(r'^\d{2}:\d{2}:\d{2}:\d{2}$', start_tc) is not None

def args_parser_value(*, file_path=None, single_timecode=None, ves_path=None, tc_start_timecode=None):
    results = []

    def log_output(tc, value, fps_mode):
        if fps_mode == '23.976':
            results.append(f"{tc} = {value[0]}")
        elif fps_mode == '24':
            results.append(f"{tc} = {value[1]}")
        else:
            results.append(f"{tc} = Unsupported FPS Mode")

    if file_path and ves_path:
        fps_mode = parse_duration_from_ves_file(ves_path)
        if fps_mode is None:
            print(f"Erro: Unknown Frame Rate: {fps_mode}")
            return results

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if not row or len(row) <= 2:
                    continue

                for tc in row[2:]:
                    tc = tc.strip()
                    if is_valid_timecode(tc):
                        value = timecode_to_value_verbose(tc, tc_start=tc_start_timecode, fps_mode_value=fps_mode)
                        log_output(tc, value, fps_mode)
                    else:
                        print(f"Invalid timecode format: {tc}")

    elif single_timecode and ves_path:
        fps_mode = parse_duration_from_ves_file(ves_path)
        if fps_mode is None:
            print(f"Unable Parse Frame Rate")
            return results

        if is_valid_timecode(single_timecode):
            value = timecode_to_value_verbose(single_timecode, tc_start=tc_start_timecode, fps_mode_value=fps_mode)
            log_output(single_timecode, value, fps_mode)
        else:
            print(f"Invalid Timecode Format：{single_timecode}")
    else:
        results.append("least arguments: -t and -d; If ues -d then is -f required")

    return results
