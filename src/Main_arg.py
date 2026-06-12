#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Version BETA

from math import sin
import re
import os
import io
import sys
import clr
import pythonnet
pythonnet.load("netfx")
import time
import argparse
import subprocess
import psutil
import base64
import importlib
from threading import Thread
from System import Action, Array, AppDomain, String, Console 
from System.IO import StringWriter # NOQA
from System.Reflection import Assembly # NOQA
base_dir = os.path.dirname(os.path.abspath(__file__))
dll_path = os.path.join(base_dir, "MuxServerHelper", "MuxServerHelper.dll")
clr.AddReference(dll_path)
asm = Assembly.LoadFile(dll_path)
program_type = asm.GetType("MuxServerHelper.Program")
from datetime import datetime
from ecq import aut
from times import args_parser
from readpes import sin
from mhz_ms_ues import args_parser_value
from bxml import maked_clip, maked_playlist, maked_fsdescriptor, maked_indextable, maked_movieobject, maked_projectdefinition
from pgtc_ms_ues import pg
from aacs import hxd_bin # NOQA
# from btFy13pd5uf4WC4h18 import lSfgApatkdxsVcGcrktoFd

def value_mhz(tc_start_timecode, timecode, timecode_dv, ves_path):

    stdout = sys.stdout

    sys.stdout = io.StringIO()

    result_mhz = args_parser_value(single_timecode=timecode, ves_path=ves_path, tc_start_timecode=tc_start_timecode)

    result_mhz_dv = args_parser_value(single_timecode=timecode_dv, ves_path=ves_path, tc_start_timecode=tc_start_timecode)

    sys.stdout = stdout

    if not result_mhz:
        print("Error: No Result")
        return None

    for line in result_mhz:
        if '=' in line:
            parts = line.split('=')
            if len(parts) == 2:
                return parts[1].strip()
    
    return None

def chapter(tc_start_timecode, file_path, ves_path, dv_ves_file, avf_file, avf_files, ssf_file):

    if file_path:
        stdout = sys.stdout

        sys.stdout = io.StringIO()

        ext = os.path.splitext(file_path)[1].lower()

        result_mhz_chap = args_parser_value(file_path=file_path, ves_path=ves_path, tc_start_timecode=tc_start_timecode)
        
        sys.stdout = stdout

        if not result_mhz_chap:
            print(f"Error: No Result, Check {file_path}...")
            return None

        output_text = '\n'.join(result_mhz_chap)
        print("Chapters TimeCode:")
        for line in result_mhz_chap:
            if '=' in line:
                print(f"                  {line.split('=')[0].strip()}\n")
            else:
                sys.exit(1)
          
    if not parse_duration_from_ves_file(file_path, ves_path, dv_ves_file, avf_file, avf_files, ssf_file):
        return None

    return value_mhz_chap_output(output_text)

def parse_duration_from_ves_file(file_path, ves_file, dv_ves_file, avf_file, avf_files, ssf_file):
    fps_value = []
   
    if file_path:
        ext = os.path.splitext(args.t)[1].lower()
        if ext == ".txt":
            fps_value = None
        elif ext != ".csv":
            print(f"Error: {file_path}, File must be .csv or .txt")
            sys.exit(1)

        try:
            if args.t is not None and isinstance(args.t, list) and len(args.t) > 1:
                print(f"Error: Max 1 Chapters CSV file can only be used once")
                sys.exit(1)

            with open(file_path, 'r', encoding='utf-8') as f_csv:
                first_line = f_csv.readline().strip()

                if re.match(r'^\d{2}(\.\d+)?', first_line):
                    fps_value = first_line.split(',')[0]

        except FileNotFoundError:
               print("Error: -t CSV File not found! Please check VES file path.")
               sys.exit(1)

    try:
        ext = os.path.splitext(args.f)[1].lower()
        if ext != ".ves":
            print(f"{args.f}, Error: File must be .ves")
            sys.exit(1)

        if args.fdv:
            ext = os.path.splitext(args.fdv)[1].lower()
            if ext != ".ves":
                print(f"{args.fdv}, Error: File must be .ves")
                sys.exit(1)

        if args.a:
            for i, audio_file in enumerate(args.a, start=1):
                ext = os.path.splitext(audio_file)[1].lower()
                if ext != ".ves":
                    print(f"{audio_file}, Error: File must be .ves")
                    sys.exit(1)

        if args.s:
            for i, sub_file in enumerate(args.s, start=1):
                ext = os.path.splitext(sub_file)[1].lower()
                if ext != ".pes":
                    print(f"{sub_file}, Error: File must be .pes")
                    sys.exit(1)

        if args.f is not None and isinstance(args.f, list) and len(args.f) > 1:
            print(f"Error: Max 1 Primary Video VES file can only be used once")
            sys.exit(1)

        if args.fdv is not None and isinstance(args.fdv, list) and len(args.fdv) > 1:
            print(f"Error: Max 1 Dolby Vision Enhancement Layer Video VES file can only be used once")
            sys.exit(1)

        if args.a is not None and len(args.a) > 32:
            print(f"Error: Max 32 Audio VES files can be used at once")
            sys.exit(1)

        if args.s is not None and len(args.s) > 32:
            print(f"Error: Max 32 Subtitle VES files can be used at once")
            sys.exit(1)

        with open(ves_file, 'r', encoding='utf-8') as f_ves:
            content = f_ves.read()
            d_value_bl = None
            API_value = None
            li_value = None
            fmof_value = None
            lg_value = None
            cpf_value_mode = None
            dynamic_range_type = None
            color_space = None
            colorspec_value_mode = 'SDR'
            hdr10pf_value_mode = None
            dm_value = None
            dp_x0_value = None
            dp_y0_value = None
            dp_x1_value = None
            dp_y1_value = None
            dp_x2_value = None
            dp_y2_value = None
            wp_x_value = None
            wp_y_value = None
            max_dml_value = None
            min_dml_value = None
            maxCLL_value = None
            maxFALL_value = None

            ast_value = None
            src_value = None
            bsid_value = None
            brc_value = None
            dsurmod_value = None
            bsmod_value = None
            nc_value = None
            full_svc_value = None
            langcod_value = None
            langcod2_value = None
            mainid_value = None
            asvcflags_value = None
            tcflag_value = None
            text_value = None

            dts_stream_type_value = None
            dts_stream_type_value_list = None
            mlp_sampling_rate_value = None
            mlp_sampling_rate_value_list = None

            fps_match = re.search(r'XML\.frame_rate=(\d+)', content)
            if fps_match:
                fps_code_0 = str(fps_match.group(1))
            else:
                print("Error: VES file invalid. Please check VES file")
                sys.exit(1)

            video_format = re.search(r'XML\.video_format=(\d+)', content)
            if video_format:
                video_format_code = str(video_format.group(1))
            else:
                print("Error: XML.video_format not found in VES file.")
                sys.exit(1)

            stream_coding_type = re.search(r'XML\.stream_coding_type=([A-Za-z0-9]+)', content)
            if stream_coding_type:
                sct_value = str(stream_coding_type.group(1))
            else:
                print("Error: XML.stream_coding_type not found in VES file.")
                sys.exit(1)

            if sct_value =='1B':
                API = re.search(r'XML\.AVC.profile_idc=(\d+)', content)
                if API:
                    API_value = str(API.group(1))
                else:
                    print("Error: AVC_profile_idc not found is VES file.")
                    sys.exit(1)

                li = re.search(r'XML\.AVC.level_idc=(\d+)', content)
                if li:
                    li_value = str(li.group(1))
                else:
                    print("Error: XML.AVC.level_idc not found is VES file.")
                    sys.exit(1)

                fmof = re.search(r'XML\.AVC.frame_mbs_only_flag=([A-Za-z0-9]+)', content)
                if fmof:
                    fmof_value = str(fmof.group(1))
                else:
                    print("Error: XML.AVC.frame_mbs_only_flag not found is VES file.")
                    sys.exit(1)

                lg = re.search(r'XML\.AVC.long_GOP=([A-Za-z0-9]+)', content)
                if lg:
                    lg_value = str(lg.group(1))
                else:
                    print("Error: XML.AVC.long_GOP not found is VES file.")
                    sys.exit(1)

            elif sct_value == '24':

                d = re.search(r'FrameCount[0]=(\d+)', content)
                if d:
                    d_value_bl = str(d.group(1))

                cpf = re.search(r'HEVC_cri_present_flag=(\d+)', content)
                if cpf:
                    cpf_value = str(cpf.group(1))

                    if cpf_value == '0':
                        cpf_value_mode = 'false'
                    elif cpf_value == '1':
                        cpf_value_mode = 'true'

                else:
                    print("Error: HEVC_cri_present_flag not found is VES file.")
                    sys.exit(1)

                colorspec = re.search(r'HEVC_colour_primaries=(\d+)', content)
                if colorspec:
                    colorspec_value = str(colorspec.group(1))

                    if colorspec_value == '1':
                        color_space = '1'
                        colorspec_value_mode = 'BT.709'
                        dynamic_range_type = '0'
                    elif colorspec_value == '9':
                        color_space = '2' 
                        colorspec_value_mode = 'BT.2020'
                        dynamic_range_type = '1'

                else:
                    print("Error: HEVC_colour_primaries not found is VES file.")
                    sys.exit(1)

                hdr10pf = re.search(r'HEVC_HDR10plus_present_flag=(\d+)', content)
                if hdr10pf:
                    hdr10pf_value = str(hdr10pf.group(1))

                    if hdr10pf_value == '0':
                        hdr10pf_value_mode = 'false'
                    elif hdr10pf_value == '1':
                        hdr10pf_value_mode = 'true'

                else:
                    print("Error: HEVC_HDR10plus_present_flag not found is VES file.")
                    sys.exit(1)

                dp_x0 = re.search(r'HEVC_display_primaries_x0=(\d+)', content)
                if dp_x0:
                    dp_x0_value = str(dp_x0.group(1))

                dp_y0 = re.search(r'HEVC_display_primaries_y0=(\d+)', content)
                if dp_y0:
                    dp_y0_value = str(dp_y0.group(1))

                dp_x1 = re.search(r'HEVC_display_primaries_x1=(\d+)', content)
                if dp_x1:
                    dp_x1_value = str(dp_x1.group(1))

                dp_y1 = re.search(r'HEVC_display_primaries_y1=(\d+)', content)
                if dp_y1:
                    dp_y1_value = str(dp_y1.group(1))

                dp_x2 = re.search(r'HEVC_display_primaries_x2=(\d+)', content)
                if dp_x2:
                    dp_x2_value = str(dp_x2.group(1))

                dp_y2 = re.search(r'HEVC_display_primaries_y2=(\d+)', content)
                if dp_y2:
                    dp_y2_value = str(dp_y2.group(1))

                wp_x = re.search(r'HEVC_white_point_x=(\d+)', content)
                if wp_x:
                    wp_x_value = str(wp_x.group(1))

                wp_y = re.search(r'HEVC_white_point_y=(\d+)', content)
                if wp_y:
                    wp_y_value = str(wp_y.group(1))

                max_dml = re.search(r'HEVC_max_display_mastering_luminance=(\d+)', content)
                if max_dml:
                    max_dml_value = max_dml.group(1)
                    if max_dml_value.endswith("0000"):
                        max_dml_value = max_dml_value[:-4]
                    else:
                        max_dml_value = max_dml_value

                min_dml = re.search(r'HEVC_min_display_mastering_luminance=(\d+)', content)
                if min_dml:
                    min_dml_value = min_dml.group(1)
                    if min_dml_value.endswith("0000"):
                        min_dml_value = min_dml_value[:-4]
                    else:
                        min_dml_value = min_dml_value

                maxCLL = re.search(r'HEVC_maxCLL=(\d+)', content)
                if maxCLL:
                    maxCLL_value = str(maxCLL.group(1))
                
                maxFALL = re.search(r'HEVC_maxFALL=(\d+)', content)
                if maxFALL:
                    maxFALL_value = str(maxFALL.group(1))

            if fps_code_0 == '1':
                fps_mode_0 = '23.976'
            elif fps_code_0 == '2':
                fps_mode_0 = '24'
            else:
                print(f"Error: Unsupported frame rate: {fps_code_0}")
                sys.exit(1)

            if video_format_code == '5':
                video_format_mode = '720p'
            elif video_format_code == '6':
                video_format_mode = '1080p'
            elif video_format_code == '8':
                video_format_mode = '2160p'
            else:
                print(f"Error: Unsupported video format: {video_format_code}")
                sys.exit(1)

            if sct_value == '1B':
                stream_coding_type_mode = 'MPEG-4 AVC'
            elif sct_value == '24':
                stream_coding_type_mode = 'HEVC'
            else:
                print(f"Error: Unsupported Video stream coding type: {sct_value}")
                sys.exit(1)

            if not fps_value:
                fps_value = fps_mode_0
            elif file_path.endswith(".txt"):
                fps_value = fps_mode_0

            if fps_value != fps_mode_0:
                print(f"Error: Frame Rate Mismatched!")
                sys.exit(1)

            sct_mode_value = stream_coding_type_mode
            vfc_mode_value = video_format_mode
            HEVC_cri_present_flag = cpf_value_mode
            dynamic_range_type = dynamic_range_type

            HEVC_colour_primaries = color_space

            if sct_value == '1B':
                color_space = ''
            elif sct_value == '24':
                color_space = colorspec_value_mode
              
            main_cp = colorspec_value_mode

            HEVC_HDR10plus_present_flag = hdr10pf_value_mode

    except FileNotFoundError:
           print("Error: -f VES File not found! Please check VES file path.")
           sys.exit(1)

    d_value_el = None
    sct_dv_value = None
    sct_dv_value_mode = None
    video_dv_format_code = None
    video_dv_format_code_mode = None
    fps_code_0_dv = None
    fps_dv = None
    cpf_value_mode_dv = None
    color_space_dv = None
    colorspec_value_mode_dv = None
    dynamic_range_type_dv = None
    hdr10pf_value_mode_dv = None

    if args.fdv:
        try:
            with open(dv_ves_file, 'r', encoding='utf-8') as f_dv_ves:
                content = f_dv_ves.read()

                d_value_el = None
                sct_dv_value_mode = None
                video_dv_format_code_mode = None
                fps_dv = None
                colorspec_value_mode_dv = None

                d = re.search(r'Duration=(\d+)', content)
                if d:
                    d_value_el = str(d.group(1))

                stream_coding_type = re.search(r'XML\.stream_coding_type=([A-Za-z0-9]+)', content)
                if stream_coding_type:
                    sct_dv_value = str(stream_coding_type.group(1))
                    sct_dv_value_mode = 'HEVC'
                else:
                    print("Error: XML.stream_coding_type not found in VES file.")
                    sys.exit(1)

                video_format = re.search(r'XML\.video_format=(\d+)', content)
                if video_format:
                    video_dv_format_code = str(video_format.group(1))
                    video_dv_format_code_mode = '1080p'
                else:
                    print("Error: XML.video_format not found in VES file.")
                    sys.exit(1)

                fps_match = re.search(r'XML\.frame_rate=(\d+)', content)
                if fps_match:
                    fps_code_0_dv = str(fps_match.group(1))
                    if fps_code_0_dv == '1':
                        fps_dv = '23.976'
                    elif fps_code_0_dv == '2':
                        fps_dv = '24'

                else:
                    print("Error: XML.frame_rate not found in VES file.")
                    sys.exit(1)

                dm = re.search(r'HEVC_dolby_meta=(\d+)', content)
                if dm:
                    dm_value = str(dm.group(1))
                else:
                    print("Error: Not is Dolby Vision (Enhancement Layer)")
                    sys.exit(1)

                cpf = re.search(r'HEVC_cri_present_flag=(\d+)', content)
                if cpf:
                    cpf_value = str(cpf.group(1))

                    if cpf_value == '0':
                        cpf_value_mode_dv = 'false'
                    elif cpf_value == '1':
                        cpf_value_mode_dv = 'true'

                else:
                    print("Error: HEVC_cri_present_flag not found is VES file.")
                    sys.exit(1)

                colorspec = re.search(r'HEVC_colour_primaries=(\d+)', content)
                if colorspec:
                    colorspec_value = str(colorspec.group(1))

                    if colorspec_value == '1':
                        color_space_dv = '1'
                        colorspec_value_mode_dv = 'BT.709'
                        dynamic_range_type_dv = '0'
                    elif colorspec_value == '9' and dm_value:
                        color_space_dv = '2' 
                        colorspec_value_mode_dv = 'BT.2020'
                        dynamic_range_type_dv = '2'

                else:
                    print("Error: HEVC_colour_primaries not found is VES file.")
                    sys.exit(1)

                hdr10pf = re.search(r'HEVC_HDR10plus_present_flag=(\d+)', content)
                if hdr10pf:
                    hdr10pf_value = str(hdr10pf.group(1))

                    if hdr10pf_value == '0':
                        hdr10pf_value_mode_dv = 'false'
                    elif hdr10pf_value == '1':
                        hdr10pf_value_mode_dv = 'true'

                else:
                    print("Error: HEVC_HDR10plus_present_flag not found is VES file.")
                    sys.exit(1)

                if fps_code_0_dv != fps_code_0:
                    print(f"Error: Frame Rate Mismatched in DV VES file!")
                    sys.exit(1)

            sct_dv_value_mode = sct_dv_value_mode
            video_dv_format_code_mode = video_dv_format_code_mode
            fps_dv = fps_dv
            colorspec_value_mode_dv = colorspec_value_mode_dv

        except FileNotFoundError:
            print("Error: -f_dv VES File not found! Please check VES file path.")
            sys.exit(1)

    aci_list = []
    apt_list = []
    sf_list = []
    adps_list = []
    ca_list = []
    bps_list = []
    audio_infos = []
    dts_stream_type_value_list = []
    ast_value_list = []
    src_value_list = []
    bsid_value_list = []
    brc_value_list = []
    dsurmod_value_list = []
    bsmod_value_list = []
    nc_value_list = []
    full_svc_value_list = []
    langcod_value_list = []
    langcod2_value_list = []
    mainid_value_list = []
    asvcflags_value_list = []
    tcflag_value_list = [] 
    mlp_sampling_rate_value_list = []

    if sct_value == "1B" and args.fdv:
        print("Error: H.264 codec don't want ues -fdv")
        sys.exit(1)

    if avf_files is None:
        avf_files = []
    if ssf_file is None:
        ssf_file = []

    for idx, avf_file in enumerate(avf_files):
        try:
            with open(avf_file, 'r', encoding='utf-8') as f_avf:
                avf_content = f_avf.read()

        except FileNotFoundError:
            print("Error: -a VES file not found! Please check VES file path.")
            sys.exit(1)

        aci_match = re.search(r'XML\.stream_coding_type=(\d+)', avf_content)
        if aci_match:
            aci_code = aci_match.group(1)
            aci_list.append(aci_code)
            aci_mode = {
                '80': 'LPCM',
                '81': 'Dolby Digital(AC3)',
                '82': 'DTS',
                '83': 'Dolby Lossless',
                '84': 'Dolby Digital Plus',
                '85': 'DTS-HD HRA',
                '86': 'DTS-HD'
            }.get(aci_code, f"Unsupported({aci_code})")
            audio_info = f"Codec: {aci_mode}"
        else:
            aci_list.append("Unknown")
            audio_info = "Codec: Unknown"

        apt_match = re.search(r'XML\.audio_presentation_type=(\d+)', avf_content)
        if apt_match:
            apt_value = apt_match.group(1)
            apt_list.append(f"{apt_value}")
        else:
            print("Unknown")

        sf = re.search(r'XML\.sampling_frequency=(\d+)', avf_content)
        if sf:
            sf_value = sf.group(1)
            sf_list.append(f"{sf_value}")
        else:
            print("Unknown")

        if aci_code == '80':
                    
            adps = re.search(r'XML\.LPCM.audio_data_payload_size=(\d+)', avf_content)
            ca = re.search(r'XML\.LPCM.channel_assignment=(\d+)', avf_content)
            bps = re.search(r'XML\.LPCM.bits_per_sample=(\d+)', avf_content)

            if adps or ca or bps:

                if adps:
                    adps_value = adps.group(1)
                    adps_value_fianl = int(adps_value) * 2
                    adps_list.append(f"{adps_value_fianl}")
        
                if ca:
                    ca_value = ca.group(1)
                    ca_list.append(f"{ca_value}")

                if bps:
                    bps_value = bps.group(1)
                    bps_list.append(f"{bps_value}")

            else:
                if aci_code == '81':
                    continue
                elif aci_code == '82':
                    continue
                elif aci_code == '83':
                    continue
                elif aci_code == '84':
                    continue
                elif aci_code == '85':
                    continue
                elif aci_code == '86':
                    continue
                else:
                    sys.exit(1)

        if aci_code in ['81', '83', '84']:

            ast = re.search(r'XML\.AC-3.ac3_stream_type=(\w+)', avf_content)
            src = re.search(r'XML\.AC-3.sample_rate_code=(\d+)', avf_content)
            bsid = re.search(r'XML\.AC-3.bsid=(\d+)', avf_content)
            brc = re.search(r'XML\.AC-3.bit_rate_code=(\d+)', avf_content)
            dsurmod = re.search(r'XML\.AC-3.dsurmod=(\d+)', avf_content)
            bsmod = re.search(r'XML\.AC-3.bsmod=(\d+)', avf_content)
            nc = re.search(r'XML\.AC-3.num_channels=(\d+)', avf_content)
            full_svc = re.search(r'XML\.AC-3.full_svc=([A-Za-z0-9]+)', avf_content)
            langcod = re.search(r'XML\.AC-3.langcod=(\d+)', avf_content)
            langcod2 = re.search(r'XML\.AC-3.langcod2=(\d+)', avf_content)
            mainid = re.search(r'XML\.AC-3.mainid=(\d+)', avf_content)
            asvcflags = re.search(r'XML\.AC-3.asvcflags=(\d+)', avf_content)
            tcflag = re.search(r'XML\.AC-3.text_code=([A-Za-z0-9]+)', avf_content)

            mlp_sampling_rate = re.search(r'XML\.AC-3.mlp_sampling_rate=(\w+)', avf_content)

            if aci_code == '83':
                mlp_sampling_rate_value = mlp_sampling_rate.group(1)
                mlp_sampling_rate_value_list.append(mlp_sampling_rate_value)
                
            if ast or src or bsid or brc or bsmod or nc or full_svc or langcod or langcod2 or mainid or asvcflags or tcflag:

                if ast:
                    ast_value = str(ast.group(1))
                    ast_value_list.append(ast_value)

                if src:
                    src_value = src.group(1)
                    src_value_list.append(src_value)

                if bsid:
                    bsid_value = bsid.group(1)
                    bsid_value_list.append(bsid_value)

                if brc:
                    brc_value = brc.group(1)
                    brc_value_list.append(brc_value)

                if dsurmod:
                    dsurmod_value = dsurmod.group(1)
                    dsurmod_value_list.append(dsurmod_value)

                if bsmod:
                    bsmod_value = bsmod.group(1)
                    bsmod_value_list.append(bsmod_value)

                if nc:
                    nc_value = nc.group(1)
                    nc_value_list.append(nc_value)

                if full_svc:
                    full_svc_value = str(full_svc.group(1))
                    full_svc_value_list.append(full_svc_value)

                if langcod:
                    langcod_value = langcod.group(1)
                    langcod_value_list.append(langcod_value)

                if langcod2:
                    langcod2_value = langcod2.group(1)
                    langcod2_value_list.append(langcod2_value)

                if mainid:
                    mainid_value = mainid.group(1)
                    mainid_value_list.append(mainid_value)

                if asvcflags:
                    asvcflags_value = asvcflags.group(1)
                    asvcflags_value_list.append(asvcflags_value)

                if tcflag:
                    tcflag_value = str(tcflag.group(1))
                    tcflag_value_list.append(tcflag_value)

            else:
                if aci_code == '80':
                    continue
                elif aci_code == '82':
                    continue
                elif aci_code == '85':
                    continue
                elif aci_code == '86':
                    continue
                else:
                    sys.exit(1)
                            
        if aci_code in ['82', '85', '86']:

            dts_stream_type = re.search(r'XML\.DTS\.dts_stream_type=(\w+)', avf_content)

            if dts_stream_type:
                dts_stream_type_value = dts_stream_type.group(1)
                dts_stream_type_value_list.append(dts_stream_type_value)

            else:
                if aci_code == '80':
                    continue
                elif aci_code == '81':
                    continue
                elif aci_code == '83':
                    continue
                elif aci_code == '84':
                    continue
                else:
                    sys.exit(1)

        audio_infos.append(audio_info)

    return video_format_code, video_format_mode, sct_value, stream_coding_type_mode, aci_list, apt_list, sf_list, adps_list, ca_list, bps_list, audio_infos, API_value, li_value, fmof_value, lg_value, dts_stream_type_value_list, ast_value_list, src_value_list, bsid_value_list, brc_value_list, dsurmod_value_list, bsmod_value_list, nc_value_list, full_svc_value_list, langcod_value_list, langcod2_value_list, mainid_value_list, asvcflags_value_list, tcflag_value_list, mlp_sampling_rate_value_list, HEVC_cri_present_flag, dynamic_range_type, HEVC_colour_primaries, main_cp, HEVC_HDR10plus_present_flag, dp_x0_value, dp_y0_value, dp_x1_value, dp_y1_value, dp_x2_value, dp_y2_value, wp_x_value, wp_y_value, max_dml_value, min_dml_value, maxCLL_value, maxFALL_value, sct_dv_value_mode, video_dv_format_code_mode, fps_dv, colorspec_value_mode_dv, sct_dv_value, video_dv_format_code, fps_code_0_dv, dm_value, cpf_value_mode_dv, color_space_dv, dynamic_range_type_dv, hdr10pf_value_mode_dv

def pes_file_check_path(pes_paths):
    for pes_file in pes_paths:
        try:
            with open(pes_file, 'rb'):
                pass
        except FileNotFoundError:
            print(f"Error: -s PES file not found! Please check PES file")
            sys.exit(1)

def value_mhz_chap_output(output_text):
    pattern = r'=\s*(\d+)\s*$'
    matches = re.findall(pattern, output_text, re.MULTILINE)
    return list(dict.fromkeys(matches))

def process_preid(preid_values, num_audios: int, num_subtitles: int):

    parts = preid_values.split(":")
    if len(parts) != 2:
        print("-preid x:x ")
        sys.exit(1)

    ida_1, ids_2 = map(int, parts)

    # Only validate audio id when audio tracks are present
    if num_audios > 0:
        if not (1 <= ida_1 <= 32):
            print("Error: Max 32 Audio")
            sys.exit(1)
        if ida_1 == 0:
            print("Error: The Audio id cannot start from 0")
            sys.exit(1)
        if ida_1 > num_audios:
            print(f"Error: The Audio id must be Audio track equal. audio id: {ida_1} audio quantity: {num_audios}")
            sys.exit(1)

    # Only validate subtitle id when subtitle tracks are present
    if num_subtitles > 0:
        if not (1 <= ids_2 <= 32):
            print("Error: Max 32 Subtitle")
            sys.exit(1)
        if ids_2 == 0:
            print("Error: The Subtitle id cannot start from 0")
            sys.exit(1)
        if ids_2 > num_subtitles:
            print(f"Error: The Subtitle id must be Subtitle track equal. subtitle id: {ids_2} Subtitle quantity: {num_subtitles}")
            sys.exit(1)

    ida_1, ids_2 = map(int, preid_values.split(':'))

    id_1 = f"8{ida_1:03X}" if num_audios > 0 else "8001"

    id_2 = f"{ids_2:03X}" if num_subtitles > 0 else "001"

    audio_idx = ida_1 - 1 if num_audios > 0 else 0
    sub_idx = ids_2 - 1 if num_subtitles > 0 else 0

    return audio_idx, sub_idx, id_1, id_2

def log_callback(msg):
    print(f"{msg}")

if __name__ == "__main__":
    # Handle --config FIRST: load JSON and build command line arguments
    if '--config' in sys.argv:
        config_idx = sys.argv.index('--config')
        if config_idx + 1 < len(sys.argv):
            config_file = sys.argv[config_idx + 1]
            import json
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Build new sys.argv from config
            new_argv = [sys.argv[0]]
            
            # Add main arguments
            new_argv.extend(['-f', config['main']['video']])
            if config['main'].get('audio'):
                new_argv.extend(['-a', config['main']['audio']])
            if config['main'].get('subtitle'):
                new_argv.extend(['-s', config['main']['subtitle']])
            
            # Add append groups
            for group in config['append_groups']:
                new_argv.append('-append')
                new_argv.extend(['-f', group['video']])
                if group.get('audio'):
                    new_argv.extend(['-a', group['audio']])
                if group.get('subtitle'):
                    new_argv.extend(['-s', group['subtitle']])
            
            # Add other arguments from original command line (excluding --config and its value)
            skip_next = False
            for i, arg in enumerate(sys.argv):
                if skip_next:
                    skip_next = False
                    continue
                if arg == '--config':
                    skip_next = True
                    continue
                if arg.startswith('-') and arg not in ['-f', '-a', '-s', '-append']:
                    new_argv.append(arg)
                    # Handle -muxserver which takes 4 arguments
                    if arg == '-muxserver':
                        for j in range(1, 5):
                            if i + j < len(sys.argv):
                                new_argv.append(sys.argv[i + j])
                        skip_next = True
                    elif i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith('-'):
                        new_argv.append(sys.argv[i + 1])
                        skip_next = True
            
            sys.argv = new_argv
    
    # Now manually parse append groups from sys.argv before argparse processes them
    append_groups = []
    # Find positions of -append in sys.argv
    append_indices = [i for i, arg in enumerate(sys.argv) if arg == '-append']
    
    if append_indices:
        # Parse command line to group parameters by -append
        # Parameters before first -append are the main group
        # Parameters after each -append are append groups
        for idx, append_idx in enumerate(append_indices):
            current_group = {'f': None, 'fdv': None, 'a': [], 'alang': [], 's': [], 'slang': []}
            i = append_idx + 1  # Start after -append
            
            # Determine the end index for this group (next -append or mux parameters or end of argv)
            if idx + 1 < len(append_indices):
                end_idx = append_indices[idx + 1]
            else:
                # Last group, find mux parameters or end of argv
                end_idx = len(sys.argv)
                for j in range(i, len(sys.argv)):
                    if sys.argv[j] in ['-mux', '-hypermux', '-muxserver', 'exe', 'port']:
                        end_idx = j
                        break
            
            # Parse parameters from i to end_idx
            while i < end_idx:
                arg = sys.argv[i]
                
                if arg == '-f' and i + 1 < len(sys.argv):
                    current_group['f'] = sys.argv[i + 1]
                    i += 2
                elif arg == '-fdv' and i + 1 < len(sys.argv):
                    current_group['fdv'] = sys.argv[i + 1]
                    i += 2
                elif arg == '-a' and i + 1 < len(sys.argv):
                    current_group['a'].append(sys.argv[i + 1])
                    i += 2
                elif arg == '-alang' and i + 1 < len(sys.argv):
                    current_group['alang'].append(sys.argv[i + 1])
                    i += 2
                elif arg == '-s' and i + 1 < len(sys.argv):
                    current_group['s'].append(sys.argv[i + 1])
                    i += 2
                elif arg == '-slang' and i + 1 < len(sys.argv):
                    current_group['slang'].append(sys.argv[i + 1])
                    i += 2
                elif arg == '-ain' and i + 1 < len(sys.argv):
                    current_group['ain'] = sys.argv[i + 1]
                    i += 2
                elif arg == '-sin' and i + 1 < len(sys.argv):
                    current_group['sin'] = sys.argv[i + 1]
                    i += 2
                else:
                    i += 1
            
            # Only add group if it has at least one file
            if current_group['f'] or current_group['a'] or current_group['s']:
                append_groups.append(current_group)
    
    
    # Remove append groups from sys.argv before argparse processes
    if append_indices:
        # Build new sys.argv without append groups
        new_argv = [sys.argv[0]]  # Keep script name
        i = 1
        while i < len(sys.argv):
            if sys.argv[i] == '-append':
                # Skip this -append and all its parameters until next -append or mux
                i += 1
                while i < len(sys.argv) and sys.argv[i] not in ['-append', '-mux', '-hypermux', '-muxserver', 'exe', 'port']:
                    # Skip parameter and its value
                    if sys.argv[i].startswith('-'):
                        i += 2  # Skip flag and its value
                    else:
                        i += 1
            else:
                new_argv.append(sys.argv[i])
                i += 1
        sys.argv = new_argv
    
    class CustomArgumentParser(argparse.ArgumentParser):
        def error(self, message):
            self.print_usage(sys.stderr)
            # If argparse sees tokens it does not recognise, those are almost
            # always words that belong to a path containing spaces or special
            # characters (e.g. Chinese) that the user forgot to quote in CMD.
            sys.stderr.write(f"Error: {message}\n")
            self.exit(1)

        def format_help(self):
            help_text = super().format_help()
            if help_text.startswith("usage:"):
                help_text = "Usage:" + help_text[len("usage:"):]
            custom_epilog = (
                "muxserver options:\n-muxserver   Startup MUXRemotingServer. Example: exe Exe Path port Port Number\n"
                "exe          Exe Path\n"
                "port         Port Number\n"
            )
            return help_text + "\n" + custom_epilog

        def print_usage(self, file=None):
            usage = self.format_usage()
            if usage.startswith("usage:"):
                usage = "Usage:" + usage[len("usage:"):]
            self._print_message(usage, file)

    parser = CustomArgumentParser(
        add_help=False,
        usage="tsSCB.exe -f <Input Video VES File> -a <Input Audio VES File> -s <Input Subtitles VES File> -sin <Set IN Time Subtitles> -mux <Output MUX Folder> | More options -h",
        epilog=""
        )
    parser.add_argument('-f', type=str, metavar='', required=True, help="Input Video VES File ( Supported videocodecs: H.264/AVC, H.265/HEVC )")
    parser.add_argument('-fdv', type=str, metavar='', help="Input Dolby Vision Enhancement Layer VES File ( Supported videocodecs: H.265/HEVC )")
    parser.add_argument('-a', type=str, metavar='', action='append', help="Input Audio VES File ( Supported audiocodecs: AC3/E-AC3(DD+), Dolby TrueHD, DTS/DTS-HD, LPCM )")
    parser.add_argument('-ain', type=str, metavar='', help="Set Audio IN Time, Set Delay relative to video; Support: Milliseconds and TimeCode (0 (ms) or 00:00:00:00)")
    parser.add_argument('-alang', type=str, metavar='', action='append', help="Set Audio Language, Default=und")
    parser.add_argument('-s', type=str, metavar='', action='append', help="Input Subtitles VES File ( Supported Subtitlecodecs: Presentation Graphic Stream (.sup))")
    parser.add_argument('-sin', type=str, metavar='', action='append', help=" Set IN Time Subtitles, Set Delay relative to video; Support: Milliseconds and TimeCode (0 (ms) or 00:00:00:00)")
    parser.add_argument('-slang', type=str, metavar='', action='append', help="Set Subtitles Language, Default=und")
    parser.add_argument('-preid', type=str, metavar='', default='1:1', help="Set Audio and Subtitle ID Default Track. Example: 1:1 (a:s)")
    parser.add_argument('-t', type=str, metavar='', help="Input CSV File ( Chapters Timecode ), default=00:00:00:00")
    parser.add_argument('-intime', type=str, metavar='', default='00:00:00:00', help="Set Video IN Time")
    parser.add_argument('-outtime', type=str, metavar='', help="Set Video OUT Time")
    parser.add_argument('-off', choices=['tc'], help="Off Video Start TimeCode", metavar='')
    parser.add_argument('-tc', type=str, metavar='', help="Specify Video Start TimeCode")
    parser.add_argument('-append', action="store_true", help="Append Files (separator for multiple file groups)")
    parser.add_argument('-mux', type=str, metavar='', required=True, help="Output MUX Folder")
    parser.add_argument('-hypermux', action="store_true", help="HyperMUXing Uses Metadata That References The Original Assets To Create a virtual BDMV volume and image")
    parser.add_argument('-muxserver', nargs=4, metavar=('EXE_TAG', 'EXE', 'PORT_TAG', 'PORT'), help=argparse.SUPPRESS)
    parser.add_argument('--config', type=str, metavar='', help="Load parameters from JSON config file")
    # btFy13pd5uf4WC4h18 = lSfgApatkdxsVcGcrktoFd()
    
    if '-h' in sys.argv or '--help' in sys.argv:
        parser.print_help()
        sys.exit()

    # -----------------------------------------------------------------------
    # Pre-parse: auto-reconstruct space-split paths + detect CJK characters
    # Runs BEFORE parse_args() so argparse receives clean, whole tokens.
    #
    # Problem: CMD splits unquoted paths on spaces, e.g.
    #   -f H:\VIDEO\28.Years#00800 PID 4117.hevc.ves
    # becomes three tokens: ["H:\\VIDEO\\28.Years#00800", "PID", "4117.hevc.ves"]
    #
    # Fix: for every known path flag, greedily join the following non-flag
    # tokens with spaces until os.path.exists() returns True.
    # After reconstruction, any path containing CJK characters is rejected.
    # -----------------------------------------------------------------------
    _PATH_FLAGS = {'-f', '-fdv', '-a', '-s', '-t', '-mux'}

    def _has_cjk(s):
        return any(
            '\u4e00' <= ch <= '\u9fff' or
            '\u3400' <= ch <= '\u4dbf' or
            '\uf900' <= ch <= '\ufaff'
            for ch in s
        )

    def _reconstruct_argv_paths(argv):
        result = []
        i = 0
        while i < len(argv):
            token = argv[i]
            if token in _PATH_FLAGS and i + 1 < len(argv):
                result.append(token)
                i += 1
                # Seed with the first token after the flag
                candidate = argv[i]
                i += 1
                # Greedily absorb following non-flag tokens while the
                # candidate path does not yet exist on disk.
                while i < len(argv) and not argv[i].startswith('-'):
                    if os.path.exists(candidate):
                        break
                    candidate += ' ' + argv[i]
                    i += 1
                # CJK check — error immediately
                if _has_cjk(candidate):
                    print(
                        f"Error: Path contains Chinese (CJK) characters.\n"
                        f"       Paths with Chinese characters are not supported.\n"
                        f"       Please rename the file/folder to ASCII-only characters:\n"
                        f"         {candidate}"
                    )
                    sys.exit(1)
                result.append(candidate)
            else:
                result.append(token)
                i += 1
        return result

    sys.argv = _reconstruct_argv_paths(sys.argv)

    args = parser.parse_args()

    # -----------------------------------------------------------------------
    # Pre-execution path validation
    # Detects missing files caused by unquoted paths that contain spaces,
    # Chinese characters, or other special characters in CMD.
    # Must run BEFORE any further processing so the error is clear and early.
    # -----------------------------------------------------------------------
    def _validate_path(flag, path, must_exist=True):
        if path is None:
            return
        # CJK check (safety net — _reconstruct_argv_paths already caught most)
        if _has_cjk(path):
            print(
                f"Error: Path contains Chinese (CJK) characters.\n"
                f"       Please rename to ASCII-only:\n"
                f"         {flag} {path}"
            )
            sys.exit(1)
        if must_exist and not os.path.exists(path):
            hint = (
                f'\n         If the path contains spaces, wrap it in double quotes:\n'
                f'           {flag} "{path}"'
            )
            print(f"Error: File not found: {path}{hint}")
            sys.exit(1)

    # Validate all path arguments before any processing begins
    _validate_path('-f',   args.f,   must_exist=True)
    _validate_path('-fdv', args.fdv, must_exist=True)
    if args.a:
        for _ap in (args.a if isinstance(args.a, list) else [args.a]):
            _validate_path('-a', _ap, must_exist=True)
    if args.s:
        for _sp in (args.s if isinstance(args.s, list) else [args.s]):
            _validate_path('-s', _sp, must_exist=True)
    # -mux: parent directory must already exist (subdirs are created by the tool)
    if args.mux and not os.path.exists(os.path.dirname(os.path.abspath(args.mux)) or args.mux):
        _validate_path('-mux', args.mux, must_exist=False)

    if len(sys.argv) > 1:
        encoded = aut()
        print(base64.b64decode(encoded).decode("utf-8"), end="\n\n")
    if args.s:
        pes_file_check_path(args.s)

    # Calculate count for main group only (since append groups were removed from sys.argv)
    count = 0
    for flag in ['-f', '-fdv', '-a', '-s']:
        count += sys.argv.count(flag)

    f_count = sys.argv.count('-f')
    fdv_count = sys.argv.count('-fdv')
    a_count = sys.argv.count('-a')
    s_count = sys.argv.count('-s')
    
    file_path, ves_file, dv_ves_file, avf_file, ssf_file, preid_values = args.t, args.f, args.fdv, args.a, args.s, args.preid

    (audio_idx, sub_idx, id_1, id_2) = process_preid(preid_values, len(args.a) if args.a else 0, len(args.s) if args.s else 0)

    # MAIN CLIP: Parse timecodes first (original source logic)
    stdout = sys.stdout
    sys.stdout = io.StringIO()
    result = args_parser(args.f, args.fdv)
    sys.stdout = stdout

    if not result:
        print("Not values")
        sys.exit(1)

    tc_start_timecode = result.get("tc_start_timecode", "00:00:00:00")
    timecode = result.get("timecode", "")
    fps = result.get("fps", "")
    fps_code = result.get("fps_code", "")

    if args.off == 'tc':
        tc_start_timecode = "00:00:00:00"
    elif args.tc:
        tc_start_timecode = args.tc

    tc_start_timecode_dv = result.get("tc_start_timecode_dv")
    timecode_dv = result.get("timecode_dv")
    fps_dv = result.get("fps_dv")
    fps_code_dv = result.get("fps_code_dv")

    if tc_start_timecode_dv:
        if args.off == 'tc':
            tc_start_timecode_dv = "00:00:00:00"
        elif args.tc:
            tc_start_timecode_dv = args.tc

    # MAIN CLIP: Compute in_tc, out_tc BEFORE parse_duration_from_ves_file
    # (value_mhz must be called before parse_duration to get correct relative values)
    in_tc = value_mhz(tc_start_timecode, args.intime, None, args.f)
    out_tc = value_mhz(tc_start_timecode, timecode, None, args.f)

    # -outtime: override the auto-detected OUT point with a user-specified timecode
    if args.outtime:
        _stdout = sys.stdout
        sys.stdout = io.StringIO()
        _out_tc_override = value_mhz(tc_start_timecode, args.outtime, None, args.f)
        sys.stdout = _stdout
        if _out_tc_override is not None:
            out_tc = _out_tc_override

    if in_tc is None or out_tc is None:
        print("Error: value_mhz returned None for main clip")
        sys.exit(1)

    main_presentation_start_time = str(in_tc)
    main_presentation_end_time = str(out_tc)
    accumulated_time = int(out_tc)

    # -----------------------------------------------------------------------
    # MAIN CLIP: Parse codec info from VES files (AFTER value_mhz calls)
    # sys.argv is already clean (append groups stripped), so args only has main
    # -----------------------------------------------------------------------
    (video_format_code, vfc_mode_value, sct_value, sct_mode_value, aci_list, apt_list, sf_list,
     adps_list, ca_list, bps_list, audio_infos, API_value, li_value, fmof_value, lg_value,
     dts_stream_type_value_list, ast_value_list, src_value_list, bsid_value_list, brc_value_list,
     dsurmod_value_list, bsmod_value_list, nc_value_list, full_svc_value_list, langcod_value_list,
     langcod2_value_list, mainid_value_list, asvcflags_value_list, tcflag_value_list,
     mlp_sampling_rate_value_list, HEVC_cri_present_flag, dynamic_range_type, colour_primaries,
     main_cp, HDR10plus_present_flag, dp_x0_value, dp_y0_value, dp_x1_value, dp_y1_value,
     dp_x2_value, dp_y2_value, wp_x_value, wp_y_value, max_dml_value, min_dml_value,
     maxCLL_value, maxFALL_value, sct_dv_value_mode, video_dv_format_code_mode, fps_dv,
     colorspec_value_mode_dv, sct_dv_value, video_dv_format_code, fps_code_0_dv, dm_value,
     cpf_value_mode_dv, color_space_dv, dynamic_range_type_dv, hdr10pf_value_mode_dv
    ) = parse_duration_from_ves_file(file_path, ves_file, dv_ves_file, avf_file, avf_file, ssf_file)

    # -----------------------------------------------------------------------
    # APPEND GROUPS: Each group parsed independently, fully separate data
    # -----------------------------------------------------------------------
    all_group_results = []

    for group in append_groups:
        group_ves_file   = group['f']   if group['f']   else None
        group_dv_ves_file = group['fdv'] if group['fdv'] else None
        group_avf_file   = group['a']   if group['a']   else []
        group_ssf_file   = group['s']   if group['s']   else []

        # Each group gets its own parse_duration_from_ves_file result
        group_result = parse_duration_from_ves_file(
            None, group_ves_file, group_dv_ves_file,
            group_avf_file, group_avf_file, group_ssf_file
        )

        # Each group gets its own timecode from args_parser
        group_tc_start_timecode = "00:00:00:00"
        group_timecode = "00:00:00:00"
        group_encoding_info = {}
        if group_ves_file:
            _stdout = sys.stdout
            sys.stdout = io.StringIO()
            group_tc_result = args_parser(group_ves_file, group_dv_ves_file)
            sys.stdout = _stdout
            if group_tc_result and isinstance(group_tc_result, dict):
                group_tc_start_timecode = group_tc_result.get("tc_start_timecode", "00:00:00:00")
                group_timecode          = group_tc_result.get("timecode", "00:00:00:00")
                group_encoding_info     = group_tc_result

        # Each CLPI independently uses its own absolute STC values from the VES file
        # (NOT accumulated — all CLPIs with same source get same values)
        g_in_tc  = value_mhz(group_tc_start_timecode, "00:00:00:00", None, group_ves_file)
        g_out_tc = value_mhz(group_tc_start_timecode, group_timecode, None, group_ves_file)
        group_presentation_start_time = str(g_in_tc)
        group_presentation_end_time   = str(g_out_tc)

        # Subtitle pg_all_value_list for this group
        # Each group computes its own pg_value from its subtitle MUI file (same as main clip)
        group_pg_all_value_list = []
        group_subtitle_langs = group.get('slang', [])
        group_fps_val = group_encoding_info.get('fps', fps)
        pid = 4608
        for i, s_path in enumerate(group_ssf_file):
            lang = group_subtitle_langs[i] if i < len(group_subtitle_langs) else 'und'
            # Try to get sin_timecode from MUI file (same as main clip logic)
            sin_timecode_g = "00:00:00:00"
            sin_value_g = 0
            base_s, _ = os.path.splitext(s_path)
            mui_path_g = base_s + ".pes.mui"
            if os.path.exists(mui_path_g):
                sin_timecode_g, sin_value_g = sin(mui_path_g, s_path, fps=group_fps_val)
            # Compute pg_value using pg() like the main clip
            _so = sys.stdout
            sys.stdout = io.StringIO()
            result_sin_g = pg(sin_timecode_g, group_tc_start_timecode, ves_path=group_ves_file)
            sys.stdout = _so
            if result_sin_g:
                pg_value_g = result_sin_g["value"]
            else:
                pg_value_g = "0"
            group_pg_all_value_list.append((pid, s_path, lang, sin_timecode_g, pg_value_g, sin_value_g))
            pid += 1

        # Unpack audio encoding info from group_result
        (group_aci_list, group_apt_list, group_sf_list, group_adps_list, group_ca_list, group_bps_list,
         group_audio_infos, group_ast_list, group_src_list, group_bsid_list, group_brc_list, group_dsurmod_list,
         group_bsmod_list, group_nc_list, group_full_svc_list, group_langcod_list, group_langcod2_list,
         group_mainid_list, group_asvcflags_list, group_tcflag_list, group_mlp_sr_list, group_dts_stream_type_list) = (
            group_result[4], group_result[5], group_result[6], group_result[7], group_result[8], group_result[9],
            group_result[10], group_result[17], group_result[18], group_result[19], group_result[20], group_result[21],
            group_result[22], group_result[23], group_result[24], group_result[25], group_result[26],
            group_result[27], group_result[28], group_result[29], group_result[30], group_result[16]
        )
        
        # Ensure lists are not None
        if group_adps_list is None: group_adps_list = []
        if group_ca_list is None: group_ca_list = []
        if group_bps_list is None: group_bps_list = []

        all_group_results.append({
            'group':                    group,
            'result':                   group_result,
            'pg_all_value_list':        group_pg_all_value_list,
            'presentation_start_time':  group_presentation_start_time,
            'presentation_end_time':    group_presentation_end_time,
            'encoding_info':            group_encoding_info,
            'a_ves_paths':              group_avf_file,
            'a_langs':                  group.get('alang', []),
            's_pes_paths':              group_ssf_file,
            's_langs':                  group_subtitle_langs,
            'in_tc':                    g_in_tc,
            'out_tc':                   g_out_tc,
            'ain':                      group.get('ain', None),
            'sin':                      group.get('sin', None),
            'audio_encoding_info': {
                'aci_list': group_aci_list,
                'apt_list': group_apt_list,
                'sf_list': group_sf_list,
                'adps_list': group_adps_list,
                'ca_list': group_ca_list,
                'bps_list': group_bps_list,
                'audio_infos': group_audio_infos,
                'ast_list': group_ast_list,
                'src_list': group_src_list,
                'bsid_list': group_bsid_list,
                'brc_list': group_brc_list,
                'dsurmod_list': group_dsurmod_list,
                'bsmod_list': group_bsmod_list,
                'nc_list': group_nc_list,
                'full_svc_list': group_full_svc_list,
                'langcod_list': group_langcod_list,
                'langcod2_list': group_langcod2_list,
                'mainid_list': group_mainid_list,
                'asvcflags_list': group_asvcflags_list,
                'tcflag_list': group_tcflag_list,
                'mlp_sr_list': group_mlp_sr_list,
                'dts_stream_type_list': group_dts_stream_type_list,
            },
        })

    fu = "\\"

    hypermux_flags = args.hypermux

    if hypermux_flags:
        hypermux_flags_value = "enabled"
    else:
        hypermux_flags_value = "disabled"

    hypermux_final = hypermux_flags_value

    mux_path = args.mux

    hxd_bin(mp=mux_path)

    if mux_path.endswith(f"\\"):
        print(f"Error: mux path dont can {fu}")
        sys.exit(1)

    # -----------------------------------------------------------------------
    # MAIN CLIP: Audio / Subtitle paths
    # sys.argv is clean — args.a / args.s contain ONLY the main clip's files
    # -----------------------------------------------------------------------
    a_ves_path = args.a if isinstance(args.a, list) else ([args.a] if args.a else [])
    s_pes_path = args.s if isinstance(args.s, list) else ([args.s] if args.s else [])
    audio_langs = []

    if isinstance(args.sin, str):
        sin_list = [args.sin]
    elif args.sin is not None and isinstance(args.sin, list):
        sin_list = args.sin
    else:
        sin_list = ["00:00:00:00"] * len(s_pes_path) if s_pes_path else []

    if isinstance(args.slang, str):
        subtitle_langs = [args.slang]
    elif isinstance(args.slang, list):
        subtitle_langs = args.slang
    else:
        subtitle_langs = []

    if args.alang:
        if len(a_ves_path) != len(args.alang):
            print("Error: The quantities of -a and -alang are inconsistent. Please ensure that each audio path has a corresponding language.")
            sys.exit(1)
        audio_langs = args.alang if isinstance(args.alang, list) else [args.alang]
    else:
        audio_langs = ["und"] * len(a_ves_path) if a_ves_path else []

    if args.slang:
        if len(s_pes_path) != len(args.slang):
            print("Error: The quantities of -s and -slang are inconsistent. Please ensure that each subtitles path has a corresponding language.")
            sys.exit(1)
        subtitles_langs = subtitle_langs
    else:
        subtitles_langs = ["und"] * len(s_pes_path) if s_pes_path else []

    # Order check on clean sys.argv
    a_index    = [i for i, arg in enumerate(sys.argv) if arg == '-a']
    alang_index = [i for i, arg in enumerate(sys.argv) if arg == '-alang']
    s_index    = [i for i, arg in enumerate(sys.argv) if arg == '-s']
    sin_index  = [i for i, arg in enumerate(sys.argv) if arg == '-sin']

    if alang_index and a_index and alang_index[0] < a_index[0]:
        print("Error: Please place -a before -alang (order must be correct)")
        sys.exit(1)

    # Build sin_map from clean sys.argv (original source logic)
    sin_map = {}
    for i, arg in enumerate(sys.argv):
        if arg == '-sin' and i + 1 < len(sys.argv):
            prev_s_positions = [idx for idx in range(i) if sys.argv[idx] == '-s']
            if prev_s_positions:
                sin_map[prev_s_positions[-1]] = sys.argv[i + 1]

    sin_list_built = []
    sin_value_list_built = []
    for idx, pes in enumerate(s_pes_path):
        base, _ = os.path.splitext(pes)
        mui_path = base + ".pes.mui"
        sin_value = sin_map.get(s_index[idx], None) if idx < len(s_index) else None
        sin_ms_value = 0
        if not sin_value:
            if os.path.exists(mui_path):
                sin_value, sin_ms_value = sin(mui_path, pes, fps=fps, tc_start_timecode=tc_start_timecode)
            else:
                sin_value = "00:00:00:00"
        sin_list_built.append(sin_value)
        sin_value_list_built.append(sin_ms_value)
    # Prefer explicit -sin values, fallback to auto-detected
    if any(v != "00:00:00:00" for v in sin_list):
        pass  # user specified -sin, keep sin_list
    else:
        sin_list = sin_list_built

    subtitles_lang_pairs = list(zip(s_pes_path, subtitle_langs, sin_list, sin_value_list_built))

    pg_all_value_list = []

    # -----------------------------------------------------------------------
    # Compute Audio IN Time value from -ain argument (HH:MM:SS:FF timecode)
    # Same calculation logic as subtitle stream_presentation_start_time
    # -----------------------------------------------------------------------
    ain_value = None
    if args.ain:
        ain_timecode = args.ain
        _stdout = sys.stdout
        sys.stdout = io.StringIO()
        result_ain = pg(ain_timecode, tc_start_timecode, ves_path=args.f)
        sys.stdout = _stdout
        if result_ain:
            ain_value = result_ain["value"]

    audio_lang_pairs = list(zip(a_ves_path, audio_langs))
    dv_final_Warning = ''

    print("Primary Video Info:")
    print(f"                   PID: 4113 | Name: {os.path.basename(args.f)}")
    print(f"                   Codec: {sct_mode_value}\n                   Format: {vfc_mode_value}\n                   Frame Rate: {fps}\n                   Color Primaries: {main_cp}")
    print(f"                   Time code of first frame: {tc_start_timecode}")
    print(f"                   IN TimeCode: {args.intime}")
    print(f"                   OUT TimeCode: {timecode}\n")
    if args.fdv:
        print("Dolby Vision Enhancement Layer Video Info:")
        print(f"                                          PID: 4117 | Name: {os.path.basename(args.fdv)}")
        print(f"                                          Codec: {sct_dv_value_mode}\n                                          Format: {video_dv_format_code_mode}\n                                          Frame Rate: {fps_dv}\n                                          Color Primaries: {colorspec_value_mode_dv}")
        print(f"                                          Time code of first frame: {tc_start_timecode_dv}")
        print(f"                                          IN TimeCode: {args.intime}")
        print(f"                                          OUT TimeCode: {timecode_dv}\n")
        if timecode != timecode_dv:
            dv_final_Warning = (
                f"                                          Warning: The Primary Video and Dolby Vision Enhancement Layer Video files do not have the same duration. Primary Video file duration: {timecode}, Dolby Vision Enhancement Layer Video file duration: {timecode_dv}\n"
            )
            print(dv_final_Warning)
    if all_group_results:
        for gi, gd in enumerate(all_group_results, start=1):
            g_enc = gd['encoding_info']
            g_f   = gd['group'].get('f', '')
            print(f"                   Append Track {gi}:")
            print(f"                                  PID: 4113 | Name: {os.path.basename(g_f)}")
            print(f"                                  Codec: {g_enc.get('sct_mode_value', 'MPEG-4 AVC')}")
            print(f"                                  Format: {g_enc.get('vfc_mode_value', '1080p')}")
            print(f"                                  Frame Rate: {g_enc.get('fps', '23.976')}")
            print(f"                                  Color Primaries: {g_enc.get('main_cp', 'SDR')}")
            print(f"                                  Time code of first frame: {g_enc.get('tc_start_timecode', '00:00:00:00')}")
            print(f"                                  IN TimeCode: 00:00:00:00")
            print(f"                                  OUT TimeCode: {g_enc.get('timecode', '00:00:00:00')}")
    print("Primary Audio Info:")
    start_pid = int('4352')
    a_ves_pid_list = []
    if audio_lang_pairs and audio_infos:
        for idx, ((a_ves_path, lang), info) in enumerate(zip(audio_lang_pairs, audio_infos)):
            pid = start_pid + idx
            is_default = (idx == audio_idx)
            if args.ain:
                try:
                    int(args.ain)
                    ain_display = f"{args.ain} ms"
                except (ValueError, TypeError):
                    ain_display = args.ain
            else:
                ain_display = "00:00:00:00"
            print(f"                   PID: {pid} | Name: {os.path.basename(args.a[idx])} | {info} | File Path: {a_ves_path} | Language: {lang} | IN TimeCode: {ain_display} | Default Track: {is_default}\n")
            a_ves_pid_list.append((pid, a_ves_path, lang))
            aci_list.append(info)
    else:
        print("                   N/A\n")
    if all_group_results:
        for gi, gd in enumerate(all_group_results, start=1):
            print(f"                   Append Track {gi}:")
            if gd['a_ves_paths']:
                # Get ain for this group
                group_ain = gd.get('ain', None)
                if group_ain:
                    try:
                        int(group_ain)
                        ain_display = f"{group_ain} ms"
                    except (ValueError, TypeError):
                        ain_display = group_ain
                else:
                    ain_display = "00:00:00:00"
                for i, audio_file in enumerate(gd['a_ves_paths']):
                    lang = gd['a_langs'][i] if i < len(gd['a_langs']) else 'und'
                    print(f"                                  PID: 4352 | Name: {os.path.basename(audio_file)} | File Path: {audio_file} | Language: {lang} | IN TimeCode: {ain_display} | Default Track: True")
            else:
                print("                                  N/A")
    print("Subtitle Info:")
    for idx, (s_path, lang, sin_timecode, sin_value) in enumerate(subtitles_lang_pairs):
        start_pid = int('4608')
        pid = start_pid + idx

        is_default = (idx == sub_idx)

        stdout = sys.stdout

        sys.stdout = io.StringIO()

        result_sin = pg(sin_timecode, tc_start_timecode, ves_path=args.f)

        sys.stdout = sys.__stdout__

        if not result_sin:
            print("Error: No Result")
            sys.exit(1)

        pg_value = result_sin["value"]
        pgtc_raw = result_sin["sin"]

        try:
            int(pgtc_raw)
            pgtc = f"{pgtc_raw} ms"
        except (ValueError, TypeError):
            pgtc = pgtc_raw

        try:
            int(sin_value)
            sin_display = f"{sin_value} ms"
        except (ValueError, TypeError):
            sin_display = sin_timecode

        print(f"              PID: {pid} | Name: {os.path.basename(s_path)} | Codec: PGS | File Path: {s_path} | Language: {lang} | IN TimeCode: {sin_display} | Default Track: {is_default}\n")

        pg_all_value_list.append((pid, s_path, lang, sin_timecode, pg_value))
    if not subtitles_lang_pairs:
        print("              N/A\n")

    if all_group_results:
        for gi, gd in enumerate(all_group_results, start=1):
            print(f"              Append Track {gi}:")
            if gd['s_pes_paths']:
                for i, sub_file in enumerate(gd['s_pes_paths']):
                    lang = gd['s_langs'][i] if i < len(gd['s_langs']) else 'und'
                    pg_entry = gd['pg_all_value_list'][i] if i < len(gd['pg_all_value_list']) else None
                    sin_tc_display = pg_entry[3] if pg_entry else '00:00:00:00'
                    sin_value_display = pg_entry[5] if pg_entry else 0
                    try:
                        int(sin_value_display)
                        sin_display = f"{sin_value_display} ms"
                    except (ValueError, TypeError):
                        sin_display = sin_tc_display
                    print(f"                             PID: 4608 | Name: {os.path.basename(sub_file)} | Codec: PGS | File Path: {sub_file} | Language: {lang} | IN TimeCode: {sin_display} | Default Track: True")
            else:
                print("                             N/A")

    out_tc_dv = value_mhz(tc_start_timecode, timecode_dv, None, args.fdv)

    # -outtime: also override DV out time when a DV layer is present
    if args.outtime and args.fdv and out_tc_dv is not None:
        _dv_tc_start = tc_start_timecode_dv if tc_start_timecode_dv else tc_start_timecode
        _stdout = sys.stdout
        sys.stdout = io.StringIO()
        _out_tc_dv_override = value_mhz(_dv_tc_start, args.outtime, None, args.fdv)
        sys.stdout = _stdout
        if _out_tc_dv_override is not None:
            out_tc_dv = _out_tc_dv_override

    if args.t:

        chapters = chapter(tc_start_timecode, args.t, args.f, args.fdv, args.a or [], args.a or [], args.s or [])

    else:

        chapters = [in_tc]
        print("Chapters TimeCode:")
        print(f"                  00:00:00:00\n")

    if not chapters:
        print("Error: No Chapters Timecode")
        sys.exit(1)

    if in_tc and out_tc:
        timestamps = [in_tc]

        # Call maked_clip separately to get tuple return value
        clip, clpi_append_blocks = maked_clip(fu, in_tc, out_tc, timestamps, v_ves_path=args.f, dv_ves_path=args.fdv, sct=sct_value, vfv=video_format_code, vfps=fps_code, a_ves_paths=args.a, a_ves_pid_list=a_ves_pid_list, pg_all_value_list=pg_all_value_list, aci_list=aci_list, apt_list=apt_list, sf_list=sf_list, adps_list=adps_list, ca_list=ca_list, bps_list=bps_list, v_idc=API_value, lidc=li_value, frame_mbs_only_flag=fmof_value, long_GOP=lg_value, ast_value_list=ast_value_list, src_value_list=src_value_list, bsid_value_list=bsid_value_list, brc_value_list=brc_value_list, dsurmod_value_list=dsurmod_value_list, bsmod_value_list=bsmod_value_list, nc_value_list=nc_value_list, full_svc_value_list=full_svc_value_list, langcod_value_list=langcod_value_list, langcod2_value_list=langcod2_value_list, mainid_value_list=mainid_value_list, asvcflags_value_list=asvcflags_value_list, tcflag_value_list=tcflag_value_list, mlp_sampling_rate_value_list=mlp_sampling_rate_value_list, dts_stream_type_value_list=dts_stream_type_value_list, cri_present_flag=HEVC_cri_present_flag, dynamic_range_type=dynamic_range_type, colour_primaries=colour_primaries, HDR10plus_present_flag=HDR10plus_present_flag, sct_dv_value=sct_dv_value, video_dv_format_code=video_dv_format_code, fps_code_0_dv=fps_code_0_dv, cpf_value_mode_dv=cpf_value_mode_dv, color_space_dv=color_space_dv, dynamic_range_type_dv=dynamic_range_type_dv, hdr10pf_value_mode_dv=hdr10pf_value_mode_dv, s_pes_paths=args.s, nosip=count, all_group_results=all_group_results, mp=args.mux, ain_value=ain_value)

        playlist, fsdescriptor, indextable, movieobject, projectdefinition = maked_playlist(in_tc, out_tc, out_tc_dv, chapters, timestamps, sct=sct_value, vfv=video_format_code, vfps=fps_code, a_ves_pid_list=a_ves_pid_list, pg_all_value_list=pg_all_value_list, video=args.f, a_ves_paths=args.a, s_pes_paths=args.s, aci_list=aci_list, apt_list=apt_list, sf_list=sf_list, f_count=f_count, fdv_count=fdv_count, a_count=a_count, s_count=s_count, dp_x0_value=dp_x0_value, dp_y0_value=dp_y0_value, dp_x1_value=dp_x1_value, dp_y1_value=dp_y1_value, dp_x2_value=dp_x2_value, dp_y2_value=dp_y2_value, wp_x_value=wp_x_value, wp_y_value=wp_y_value, max_dml_value=max_dml_value, min_dml_value=min_dml_value, maxCLL_value=maxCLL_value, maxFALL_value=maxFALL_value, dynamic_range_type=dynamic_range_type, sct_dv_value=sct_dv_value, video_dv_format_code=video_dv_format_code, fps_code_0_dv=fps_code_0_dv, dm_value=dm_value, cpf_value_mode_dv=cpf_value_mode_dv, color_space_dv=color_space_dv, dynamic_range_type_dv=dynamic_range_type_dv, hdr10pf_value_mode_dv=hdr10pf_value_mode_dv, all_group_results=all_group_results), maked_fsdescriptor(fu, mp=args.mux, all_group_results=all_group_results), maked_indextable(), maked_movieobject(id_1, id_2), maked_projectdefinition(hypermux_final, fu, mp=args.mux, all_group_results=all_group_results)

        xml_dir = os.path.join(args.mux, "Output", "MUX", "BDROM")

        print("Waiting...", end='', flush=True)
        time.sleep(3)

        sys.stdout.write('\r' + ' ' * len("Waiting...") + '\r')
        sys.stdout.flush()

        with open(os.path.join(xml_dir, "MoviePlayList.xml"), "w", encoding="utf-8") as f:
            f.write(playlist) 

        with open(os.path.join(xml_dir, "CLIPDescriptor.xml"), "w", encoding="utf-8") as f:
            f.write(clip)

        with open(os.path.join(xml_dir, "FSDescriptor.xml"), "w", encoding="utf-8") as f:
            f.write(fsdescriptor)

        with open(os.path.join(xml_dir, "IndexTable.xml"), "w", encoding="utf-8") as f:
            f.write(indextable)

        with open(os.path.join(xml_dir, "MovieObject.xml"), "w", encoding="utf-8") as f:
            f.write(movieobject)

        with open(os.path.join(xml_dir, "ProjectDefinition.xml"), "w", encoding="utf-8") as f:
            f.write(projectdefinition)

        if f.write:
            print("Log Info:\n         XML Save as MoviePlayList.xml\n         XML Save as CLIPDescriptor.xml\n         XML Save as FSDescriptor.xml\n         XML Save as IndexTable.xml\n         XML Save as MovieObject.xml\n         XML Save as ProjectDefinition.xml\n         XML Version: 2.0.0\n")
        elif not f.write:
            print(f"Error!")
            sys.exit(1)

        muxserver_flags = args.muxserver

        if muxserver_flags:

            base_dir = os.path.dirname(os.path.abspath(__file__))

            muxserver_path = os.path.join(base_dir, 'MuxServerHelper', 'MuxServerHelper.dll')

            if not os.path.exists(muxserver_path):
                print(f"MuxServerHelper.dll File Not Found.")
                sys.exit(1)

            xml_dir = os.path.join(args.mux, "Output", "MUX", "BDROM")

            projectdefinition = os.path.join(xml_dir, 'ProjectDefinition.xml')
                   
            server_tag, server, port_tag, port = args.muxserver

            if server_tag.lower() != 'exe' or port_tag.lower() != 'port':
                print("Error: have to -muxserver exe <File_Path> port <Port_Number>")
                sys.exit(1)

            args_list = [
                muxserver_path,
                "--project", projectdefinition,
                "--clip", str(len(all_group_results) + 1),
                "--server", server,
                "--port", port
            ]

            callback_delegate = Action[String](log_callback)
            init_method = program_type.GetMethod("InitConsoleRedirect")
            init_method.Invoke(None, [callback_delegate])

            args_array = Array[String](args_list)
            params = [args_array]

            print("MuxServer Info:")

            result = program_type.GetMethod("Run").Invoke(None, params)