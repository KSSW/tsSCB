# -*- coding: utf-8 -*-

import os
from pgtc_ms_ues import pg

def maked_playlist(in_time, out_time, out_tc_dv, value_chap, timestamps, sct, vfv, vfps, a_ves_pid_list, pg_all_value_list, video, a_ves_paths, s_pes_paths, aci_list, apt_list, sf_list, f_count, fdv_count, a_count, s_count, dp_x0_value, dp_y0_value, dp_x1_value, dp_y1_value, dp_x2_value, dp_y2_value, wp_x_value, wp_y_value, max_dml_value, min_dml_value, maxCLL_value, maxFALL_value, dynamic_range_type, sct_dv_value, video_dv_format_code, fps_code_0_dv, dm_value, cpf_value_mode_dv, color_space_dv, dynamic_range_type_dv, hdr10pf_value_mode_dv, all_group_results=None):
    # Guard against None for optional tracks
    if a_ves_pid_list is None:
        a_ves_pid_list = []
    if pg_all_value_list is None:
        pg_all_value_list = []
    if a_ves_paths is None:
        a_ves_paths = []
    if s_pes_paths is None:
        s_pes_paths = []
    if aci_list is None:
        aci_list = []
    if apt_list is None:
        apt_list = []
    if sf_list is None:
        sf_list = []
    if video:
        primary_video_stream = f"""
              <primary_video_stream>
                <stream_entry>
                  <type>1</type>
                  <Select_type>
                    <type_1>
                      <ref_to_stream_PID_of_mainClip>4113</ref_to_stream_PID_of_mainClip>
                    </type_1>
                  </Select_type>
                </stream_entry>
                <stream_attributes>
                  <stream_coding_type>{sct}</stream_coding_type>
                  <Select_stream_coding_type>
                    <video_stream>
                      <video_format>{vfv}</video_format>
                      <frame_rate>{vfps}</frame_rate>
                    </video_stream>
                  </Select_stream_coding_type>
                </stream_attributes>
              </primary_video_stream>
            """.strip()

        primary_audio_streams = []
        nodess = []
        nodes_not = []
        dv_noss = []
        dv_noss_final = []
        dv_noss_not_values = []
        number_of_SubPaths = []
        nos_numbers = []
        lp_dvs = []
        all_info_number_of_SubPaths_final = []
        append_play_items = []
        
        if sct == '24':
                
            nodes = (
                f"          <static_metadata>\n"
                f"            <number_of_data_entries>1</number_of_data_entries>\n"
                f"            <Loop_static_metadata_entries>\n"
                f"              <static_metadata_entry>\n"
                f"                <dynamic_range_type_ref>{dynamic_range_type}</dynamic_range_type_ref>\n"
                f"                <number_of_display_primaries>3</number_of_display_primaries>\n"
                f"                <Loop_display_primaries>\n"
                f"                  <display_primaries>\n"
                f"                    <display_primaries_x>{dp_x0_value}</display_primaries_x>\n"
                f"                    <display_primaries_y>{dp_y0_value}</display_primaries_y>\n"
                f"                  </display_primaries>\n"
                f"                  <display_primaries>\n"
                f"                    <display_primaries_x>{dp_x1_value}</display_primaries_x>\n"
                f"                    <display_primaries_y>{dp_y1_value}</display_primaries_y>\n"
                f"                  </display_primaries>\n"
                f"                  <display_primaries>\n"
                f"                    <display_primaries_x>{dp_x2_value}</display_primaries_x>\n"
                f"                    <display_primaries_y>{dp_y2_value}</display_primaries_y>\n"
                f"                  </display_primaries>\n"
                f"                </Loop_display_primaries>\n"
                f"                <white_point_x>{wp_x_value}</white_point_x>\n"
                f"                <white_point_y>{wp_y_value}</white_point_y>\n"
                f"                <max_display_mastering_luminance>{max_dml_value}</max_display_mastering_luminance>\n"
                f"                <min_display_mastering_luminance>{min_dml_value}</min_display_mastering_luminance>\n"
                f"                <MaxCLL>{maxCLL_value}</MaxCLL>\n"
                f"                <MaxFALL>{maxFALL_value}</MaxFALL>\n"
                f"              </static_metadata_entry>\n"
                f"            </Loop_static_metadata_entries>\n"
                f"          </static_metadata>"
            )
            nodess.append(nodes)
            
        if dm_value:

            dv_nos = (

                f'            <Loop_enhancement_layer_video_stream>\n'
                f'              <enhancement_layer_video_stream>\n'
                f'                <stream_entry>\n'
                f'                  <type>4</type>\n'
                f'                  <Select_type>\n'
                f'                    <type_4>\n'
                f'                      <ref_to_SubPath_id>0</ref_to_SubPath_id>\n'
                f'                      <ref_to_stream_PID_of_mainClip>4117</ref_to_stream_PID_of_mainClip>\n'
                f'                    </type_4>\n'
                f'                  </Select_type>\n'
                f'                </stream_entry>\n'
                f'                <stream_attributes>\n'
                f'                  <stream_coding_type>{sct_dv_value}</stream_coding_type>\n'
                f'                  <Select_stream_coding_type>\n'
                f'                    <video_stream>\n'
                f'                      <video_format>{video_dv_format_code}</video_format>\n'
                f'                      <frame_rate>1</frame_rate>\n'
                f'                      <dynamic_range_type>{dynamic_range_type_dv}</dynamic_range_type>\n'
                f'                      <color_space>{color_space_dv}</color_space>\n'
                f'                      <cri_usage_flag>{cpf_value_mode_dv}</cri_usage_flag>\n'
                f'                    </video_stream>\n'
                f'                  </Select_stream_coding_type>\n'
                f'                </stream_attributes>\n'
                f'              </enhancement_layer_video_stream>\n'
                f'            </Loop_enhancement_layer_video_stream>'
            )

            dv_noss.append(dv_nos)

            number_of_SubPaths = (
                f'      <number_of_SubPaths>1</number_of_SubPaths>'

            )

            nos_numbers.append(number_of_SubPaths)

            lp_dv = (

                f'      </Loop_PlayItem>\n'
                f'      <Loop_SubPath>\n'
                f'        <SubPath>\n'
                f'          <SubPath_type>10</SubPath_type>\n'
                f'          <is_repeat_SubPath>false</is_repeat_SubPath>\n'
                f'          <number_of_SubPlayItems>1</number_of_SubPlayItems>\n'
                f'          <Loop_SubPlayItem>\n'
                f'            <SubPlayItem>\n'
                f'              <Clip_Information_file_name>88888</Clip_Information_file_name>\n'
                f'              <Clip_codec_identifier>M2TS</Clip_codec_identifier>\n'
                f'              <sp_connection_condition>1</sp_connection_condition>\n'
                f'              <is_multi_Clip_entries>false</is_multi_Clip_entries>\n'
                f'              <ref_to_STC_id>0</ref_to_STC_id>\n'
                f'              <SubPlayItem_IN_time>{in_time}</SubPlayItem_IN_time>\n'
                f'              <SubPlayItem_OUT_time>{out_tc_dv}</SubPlayItem_OUT_time>\n'
                f'              <sync_PlayItem_id>0</sync_PlayItem_id>\n'
                f'              <sync_start_PTS_of_PlayItem>{in_time}</sync_start_PTS_of_PlayItem>\n'
                f'              <Select_is_multi_Clip_entries />\n'
                f'            </SubPlayItem>\n'
                f'          </Loop_SubPlayItem>\n'
                f'        </SubPath>\n'
                f'      </Loop_SubPath>'          
            )

            lp_dvs.append(lp_dv)
                            
        else:
            
            nodes_not = (
                f"          <static_metadata>\n"
                f"            <number_of_data_entries>0</number_of_data_entries>\n"
                f"            <Loop_static_metadata_entries />\n"
                f"          </static_metadata>"
            )

            nodess.append(nodes_not)

            number_of_SubPaths = (
                f'      <number_of_SubPaths>0</number_of_SubPaths>'

            )

            nos_numbers.append(number_of_SubPaths)

            dv_noss_not_value = (
                f'            <Loop_enhancement_layer_video_stream />'
            )

            dv_noss.append(dv_noss_not_value)

            number_of_SubPaths_not = (
                    f'      </Loop_PlayItem>\n'
                    f'      <Loop_SubPath />'
            )

            lp_dvs.append(number_of_SubPaths_not)

    nodess_final = "\n".join(nodess)
    dv_noss_final = "\n".join(dv_noss)
    nos_numbers_final = "\n".join(nos_numbers)
    all_info_number_of_SubPaths_final = "\n".join(lp_dvs)

    if all_info_number_of_SubPaths_final:
      all_info_number_of_SubPaths_final = "\n" + all_info_number_of_SubPaths_final

    for idx, (pid, a_path, lang), in enumerate(a_ves_pid_list):
        aci_code = aci_list[idx]
        apt_value = apt_list[idx]
        sf_value = sf_list[idx]
        final_stream = []
                
        if a_ves_paths:
            audio_stream_block = (
                               f"              <primary_audio_stream>\n"
                               f"                <stream_entry>\n"
                               f"                  <type>1</type>\n"
                               f"                  <Select_type>\n"
                               f"                    <type_1>\n"
                               f"                      <ref_to_stream_PID_of_mainClip>{pid}</ref_to_stream_PID_of_mainClip>\n"
                               f"                    </type_1>\n"
                               f"                  </Select_type>\n"
                               f"                </stream_entry>\n"
                               f"                <stream_attributes>\n"
                               f"                  <stream_coding_type>{aci_code}</stream_coding_type>\n"
                               f"                  <Select_stream_coding_type>\n"
                               f"                    <audio_stream>\n"
                               f"                      <audio_presentation_type>{apt_value}</audio_presentation_type>\n"
                               f"                      <sampling_frequency>{sf_value}</sampling_frequency>\n"
                               f"                      <audio_language_code>{lang}</audio_language_code>\n"
                               f"                    </audio_stream>\n"
                               f"                  </Select_stream_coding_type>\n"
                               f"                </stream_attributes>\n"
                               f"              </primary_audio_stream>"
            )
            primary_audio_streams.append(audio_stream_block)

    final_stream = []
    for s_pid, s_path, s_lang, sin_timecode, pg_value in pg_all_value_list:

        if s_pes_paths:
            subtitles = (
                f"            <Loop_PG_textST_stream>\n"
                f"              <PG_textST_stream>\n"
                f"                <stream_entry>\n"
                f"                  <type>1</type>\n"
                f"                  <Select_type>\n"
                f"                    <type_1>\n"
                f"                      <ref_to_stream_PID_of_mainClip>{s_pid}</ref_to_stream_PID_of_mainClip>\n"
                f"                    </type_1>\n"
                f"                  </Select_type>\n"
                f"                </stream_entry>\n"
                f"                <stream_attributes>\n"
                f"                  <stream_coding_type>90</stream_coding_type>\n"
                f"                  <Select_stream_coding_type>\n"
                f"                    <PG_stream>\n"
                f"                      <PG_language_code>{s_lang}</PG_language_code>\n"
                f"                    </PG_stream>\n"
                f"                  </Select_stream_coding_type>\n"
                f"                </stream_attributes>\n"
                f"              </PG_textST_stream>\n"
                f"            </Loop_PG_textST_stream>"
            )
            final_stream.append(subtitles)

    all_audio_streams_final = "\n".join(primary_audio_streams)
    all_sub_streams_final = "\n".join(final_stream)

    if not all_audio_streams_final:
      all_audio_streams_final = f"            <Loop_primary_audio_stream />"

    if not all_sub_streams_final:
      all_sub_streams_final = f"            <Loop_PG_textST_stream />"

    if not append_play_items:
      append_play_items = f"        </PlayItem>"

    if not all_info_number_of_SubPaths_final:
      all_info_number_of_SubPaths_final = f"        </PlayItem>"

    # Build append PlayItems block BEFORE the f-string template (backslash not allowed inside f-string)
    _nl = "\n"
    if all_group_results:
        _append_items_raw = "".join([f'''        <PlayItem>
          <Clip_Information_file_name>{88889 + i}</Clip_Information_file_name>
          <Clip_codec_identifier>M2TS</Clip_codec_identifier>
          <is_multi_angle>false</is_multi_angle>
          <connection_condition>1</connection_condition>
          <ref_to_STC_id>0</ref_to_STC_id>
          <IN_time>{group.get('presentation_start_time', in_time)}</IN_time>
          <OUT_time>{group.get('presentation_end_time', out_time)}</OUT_time>
          <UO_mask_table>
            <reserved_for_menu_call_mask>false</reserved_for_menu_call_mask>
            <reserved_for_title_search_mask>false</reserved_for_title_search_mask>
            <chapter_search_mask>false</chapter_search_mask>
            <time_search_mask>false</time_search_mask>
            <skip_to_next_point_mask>false</skip_to_next_point_mask>
            <skip_back_to_previous_point_mask>false</skip_back_to_previous_point_mask>
            <stop_mask>false</stop_mask>
            <pause_on_mask>false</pause_on_mask>
            <still_off_mask>false</still_off_mask>
            <forward_play_mask>false</forward_play_mask>
            <backward_play_mask>false</backward_play_mask>
            <resume_mask>false</resume_mask>
            <move_up_selected_button_mask>false</move_up_selected_button_mask>
            <move_down_selected_button_mask>false</move_down_selected_button_mask>
            <move_left_selected_button_mask>false</move_left_selected_button_mask>
            <move_right_selected_button_mask>false</move_right_selected_button_mask>
            <select_button_mask>false</select_button_mask>
            <activate_button_mask>false</activate_button_mask>
            <select_button_and_activate_mask>false</select_button_and_activate_mask>
            <primary_audio_stream_number_change_mask>false</primary_audio_stream_number_change_mask>
            <angle_number_change_mask>false</angle_number_change_mask>
            <popup_on_mask>false</popup_on_mask>
            <popup_off_mask>false</popup_off_mask>
            <PG_textST_enable_disable_mask>false</PG_textST_enable_disable_mask>
            <PG_textST_stream_number_change_mask>false</PG_textST_stream_number_change_mask>
            <secondary_video_enable_disable_mask>true</secondary_video_enable_disable_mask>
            <secondary_video_stream_number_change_mask>true</secondary_video_stream_number_change_mask>
            <secondary_audio_enable_disable_mask>true</secondary_audio_enable_disable_mask>
            <secondary_audio_stream_number_change_mask>true</secondary_audio_stream_number_change_mask>
            <PiP_PG_textST_stream_number_change_mask>true</PiP_PG_textST_stream_number_change_mask>
          </UO_mask_table>
          <PlayItem_random_access_flag>false</PlayItem_random_access_flag>
          <still_mode>00</still_mode>
          <Select_still_mode />
          <Select_is_multi_angle />
          <STN_table>
            <number_of_primary_video_stream_entries>1</number_of_primary_video_stream_entries>
            <number_of_primary_audio_stream_entries>{a_count}</number_of_primary_audio_stream_entries>
            <number_of_PG_textST_stream_entries>{s_count}</number_of_PG_textST_stream_entries>
            <number_of_IG_stream_entries>0</number_of_IG_stream_entries>
            <number_of_secondary_audio_stream_entries>0</number_of_secondary_audio_stream_entries>
            <number_of_secondary_video_stream_entries>0</number_of_secondary_video_stream_entries>
            <number_of_PiP_PG_textST_stream_entries_plus>0</number_of_PiP_PG_textST_stream_entries_plus>
            <number_of_enhancement_layer_video_stream_entries>0</number_of_enhancement_layer_video_stream_entries>
            <Loop_primary_video_stream>
              <primary_video_stream>
                <stream_entry>
                  <type>1</type>
                  <Select_type>
                    <type_1>
                      <ref_to_stream_PID_of_mainClip>4113</ref_to_stream_PID_of_mainClip>
                    </type_1>
                  </Select_type>
                </stream_entry>
                <stream_attributes>
                  <stream_coding_type>{sct}</stream_coding_type>
                  <Select_stream_coding_type>
                    <video_stream>
                      <video_format>{vfv}</video_format>
                      <frame_rate>{vfps}</frame_rate>
                    </video_stream>
                  </Select_stream_coding_type>
                </stream_attributes>
              </primary_video_stream>
            </Loop_primary_video_stream>
            <Loop_primary_audio_stream>
{all_audio_streams_final}
            </Loop_primary_audio_stream>
{all_sub_streams_final}
            <Loop_IG_stream />
            <Loop_secondary_audio_stream />
            <Loop_secondary_video_stream />
            <Loop_enhancement_layer_video_stream />
          </STN_table>
        </PlayItem>
''' for i, group in enumerate(all_group_results)])
        append_play_items = "\n" + _append_items_raw.rstrip('\n')
    else:
        append_play_items = ""

    pl_marks = ""
    for ts in value_chap:
        pl_marks = "".join(f"""
        <PL_Mark>
          <mark_type>01</mark_type>
          <ref_to_PlayItem_id>0</ref_to_PlayItem_id>
          <mark_time_stamp>{ts}</mark_time_stamp>
          <entry_ES_PID>65535</entry_ES_PID>
          <duration>0</duration>
        </PL_Mark>""" for ts in value_chap)

    xml_template = f"""
<?xml version="1.0" encoding="UTF-8"?>
<MoviePlayListFile Version="0099" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="MoviePlayList.xsd">
  <MPLS FileName="00000">
    <type_indicator>MPLS</type_indicator>
    <version_number>0300</version_number>
    <AppInfoPlayList>
      <PlayList_playback_type>1</PlayList_playback_type>
      <Select_PlayList_playback_type />
      <UO_mask_table>
        <reserved_for_menu_call_mask>false</reserved_for_menu_call_mask>
        <reserved_for_title_search_mask>false</reserved_for_title_search_mask>
        <chapter_search_mask>false</chapter_search_mask>
        <time_search_mask>false</time_search_mask>
        <skip_to_next_point_mask>false</skip_to_next_point_mask>
        <skip_back_to_previous_point_mask>false</skip_back_to_previous_point_mask>
        <stop_mask>false</stop_mask>
        <pause_on_mask>false</pause_on_mask>
        <still_off_mask>false</still_off_mask>
        <forward_play_mask>false</forward_play_mask>
        <backward_play_mask>false</backward_play_mask>
        <resume_mask>false</resume_mask>
        <move_up_selected_button_mask>false</move_up_selected_button_mask>
        <move_down_selected_button_mask>false</move_down_selected_button_mask>
        <move_left_selected_button_mask>false</move_left_selected_button_mask>
        <move_right_selected_button_mask>false</move_right_selected_button_mask>
        <select_button_mask>false</select_button_mask>
        <activate_button_mask>false</activate_button_mask>
        <select_button_and_activate_mask>false</select_button_and_activate_mask>
        <primary_audio_stream_number_change_mask>false</primary_audio_stream_number_change_mask>
        <angle_number_change_mask>false</angle_number_change_mask>
        <popup_on_mask>false</popup_on_mask>
        <popup_off_mask>false</popup_off_mask>
        <PG_textST_enable_disable_mask>false</PG_textST_enable_disable_mask>
        <PG_textST_stream_number_change_mask>false</PG_textST_stream_number_change_mask>
        <secondary_video_enable_disable_mask>true</secondary_video_enable_disable_mask>
        <secondary_video_stream_number_change_mask>true</secondary_video_stream_number_change_mask>
        <secondary_audio_enable_disable_mask>true</secondary_audio_enable_disable_mask>
        <secondary_audio_stream_number_change_mask>true</secondary_audio_stream_number_change_mask>
        <PiP_PG_textST_stream_number_change_mask>true</PiP_PG_textST_stream_number_change_mask>
      </UO_mask_table>
      <PlayList_random_access_flag>false</PlayList_random_access_flag>
      <audio_mix_app_flag>true</audio_mix_app_flag>
      <lossless_may_bypass_mixer_flag>false</lossless_may_bypass_mixer_flag>
      <MVC_Base_view_R_flag>false</MVC_Base_view_R_flag>
      <SDR_conversion_notification_flag>false</SDR_conversion_notification_flag>
    </AppInfoPlayList>
    <Loop_padding_word_1 />
    <PlayList>
      <number_of_PlayItems>{1 + len(all_group_results) if all_group_results else 1}</number_of_PlayItems>
{nos_numbers_final}
      <Loop_PlayItem>
        <PlayItem>
          <Clip_Information_file_name>88888</Clip_Information_file_name>
          <Clip_codec_identifier>M2TS</Clip_codec_identifier>
          <is_multi_angle>false</is_multi_angle>
          <connection_condition>1</connection_condition>
          <ref_to_STC_id>0</ref_to_STC_id>
          <IN_time>{in_time}</IN_time>
          <OUT_time>{out_time}</OUT_time>
          <UO_mask_table>
            <reserved_for_menu_call_mask>false</reserved_for_menu_call_mask>
            <reserved_for_title_search_mask>false</reserved_for_title_search_mask>
            <chapter_search_mask>false</chapter_search_mask>
            <time_search_mask>false</time_search_mask>
            <skip_to_next_point_mask>false</skip_to_next_point_mask>
            <skip_back_to_previous_point_mask>false</skip_back_to_previous_point_mask>
            <stop_mask>false</stop_mask>
            <pause_on_mask>false</pause_on_mask>
            <still_off_mask>false</still_off_mask>
            <forward_play_mask>false</forward_play_mask>
            <backward_play_mask>false</backward_play_mask>
            <resume_mask>false</resume_mask>
            <move_up_selected_button_mask>false</move_up_selected_button_mask>
            <move_down_selected_button_mask>false</move_down_selected_button_mask>
            <move_left_selected_button_mask>false</move_left_selected_button_mask>
            <move_right_selected_button_mask>false</move_right_selected_button_mask>
            <select_button_mask>false</select_button_mask>
            <activate_button_mask>false</activate_button_mask>
            <select_button_and_activate_mask>false</select_button_and_activate_mask>
            <primary_audio_stream_number_change_mask>false</primary_audio_stream_number_change_mask>
            <angle_number_change_mask>false</angle_number_change_mask>
            <popup_on_mask>false</popup_on_mask>
            <popup_off_mask>false</popup_off_mask>
            <PG_textST_enable_disable_mask>false</PG_textST_enable_disable_mask>
            <PG_textST_stream_number_change_mask>false</PG_textST_stream_number_change_mask>
            <secondary_video_enable_disable_mask>true</secondary_video_enable_disable_mask>
            <secondary_video_stream_number_change_mask>true</secondary_video_stream_number_change_mask>
            <secondary_audio_enable_disable_mask>true</secondary_audio_enable_disable_mask>
            <secondary_audio_stream_number_change_mask>true</secondary_audio_stream_number_change_mask>
            <PiP_PG_textST_stream_number_change_mask>true</PiP_PG_textST_stream_number_change_mask>
          </UO_mask_table>
          <PlayItem_random_access_flag>false</PlayItem_random_access_flag>
          <still_mode>00</still_mode>
          <Select_still_mode />
          <Select_is_multi_angle />
          <STN_table>
            <number_of_primary_video_stream_entries>{f_count}</number_of_primary_video_stream_entries>
            <number_of_primary_audio_stream_entries>{a_count}</number_of_primary_audio_stream_entries>
            <number_of_PG_textST_stream_entries>{s_count}</number_of_PG_textST_stream_entries>
            <number_of_IG_stream_entries>0</number_of_IG_stream_entries>
            <number_of_secondary_audio_stream_entries>0</number_of_secondary_audio_stream_entries>
            <number_of_secondary_video_stream_entries>0</number_of_secondary_video_stream_entries>
            <number_of_PiP_PG_textST_stream_entries_plus>0</number_of_PiP_PG_textST_stream_entries_plus>
            <number_of_enhancement_layer_video_stream_entries>{fdv_count}</number_of_enhancement_layer_video_stream_entries>
            <Loop_primary_video_stream>
              {primary_video_stream}
            </Loop_primary_video_stream>
            <Loop_primary_audio_stream>
{all_audio_streams_final}
            </Loop_primary_audio_stream>
{all_sub_streams_final}
            <Loop_IG_stream />
            <Loop_secondary_audio_stream />
            <Loop_secondary_video_stream />
{dv_noss_final}
          </STN_table>
        </PlayItem>{append_play_items}{all_info_number_of_SubPaths_final}
    </PlayList>
    <Loop_padding_word_2 />
    <PlayListMark>
      <number_of_PlayList_marks>{len(value_chap)}</number_of_PlayList_marks>
      <Loop_PL_Mark>{pl_marks}
      </Loop_PL_Mark>
    </PlayListMark>
    <Loop_padding_word_3 />
    <ExtensionData>
      <number_of_ext_data_entries>1</number_of_ext_data_entries>
      <Loop_ext_data_entries>
        <ext_data_entry>
          <ID1>3</ID1>
          <ID2>5</ID2>
        </ext_data_entry>
      </Loop_ext_data_entries>
      <Loop_padding_word />
      <Loop_data_block>
        <data_block>
{nodess_final}
        </data_block>
      </Loop_data_block>
    </ExtensionData>
    <Loop_padding_word_4 />
  </MPLS>
</MoviePlayListFile>
    """.strip()

    return xml_template.strip()

def maked_clip(fu, in_time, out_time, timestamps, v_ves_path, dv_ves_path, sct, vfv, vfps, a_ves_paths, s_pes_paths, aci_list, apt_list, sf_list, adps_list, ca_list, bps_list, v_idc, lidc, frame_mbs_only_flag, long_GOP,
               dts_stream_type_value_list, ast_value_list, src_value_list, bsid_value_list, brc_value_list, dsurmod_value_list, bsmod_value_list, nc_value_list, full_svc_value_list, langcod_value_list, langcod2_value_list, mainid_value_list, asvcflags_value_list, tcflag_value_list, mlp_sampling_rate_value_list,
               a_ves_pid_list, pg_all_value_list, cri_present_flag, dynamic_range_type, colour_primaries, HDR10plus_present_flag, sct_dv_value, video_dv_format_code, fps_code_0_dv, cpf_value_mode_dv, color_space_dv, dynamic_range_type_dv, hdr10pf_value_mode_dv, nosip, all_group_results, mp, ain_value=None):

    # Output
    TSIntermediate = r"Output\MUX\BDROM\TSIntermediate\88888"
    STREAM = r"Output\MUX\BDROM\DB\BDMV\STREAM"
    TSmediate = os.path.join(mp, TSIntermediate)
    m2ts = os.path.join(mp, STREAM)
    os.makedirs(TSmediate, exist_ok=True)
    os.makedirs(m2ts, exist_ok=True)
    # Also create TSIntermediate directories for all append clip groups
    if all_group_results:
        for append_idx in range(len(all_group_results)):
            append_clip_id = 88889 + append_idx
            append_ts_dir = os.path.join(mp, r"Output\MUX\BDROM\TSIntermediate", str(append_clip_id))
            os.makedirs(append_ts_dir, exist_ok=True)

    # Guard against None for optional tracks
    if a_ves_paths is None:
        a_ves_paths = []
    if s_pes_paths is None:
        s_pes_paths = []
    if a_ves_pid_list is None:
        a_ves_pid_list = []
    if pg_all_value_list is None:
        pg_all_value_list = []

    a_pid = ""
    s_pid = ""
    blocks_a = []
    blocks_s = []
    pmss = []
    spsts = []
    spstss = []
    total_a = len(a_ves_paths)
    total_s = len(s_pes_paths)
    sin_timecode = []

    for (a_pid, a_ves_path, a_lang) in (a_ves_pid_list):
        a, _ = os.path.splitext(a_ves_path)
        a_mui_path = a + ".mui"

        ain_psts = (
            f"                <stream_presentation_start_time>{ain_value}</stream_presentation_start_time>\n"
            if ain_value is not None else ""
        )

        block_a = (
              f"              <ESData_TS>\n"
              f"                <stream_PID>{a_pid}</stream_PID>\n"
              f"{ain_psts}"
              f"                <VES_InputFilename>{a_ves_path}</VES_InputFilename>\n"
              f"                <MUI_InputFilename>{a_mui_path}</MUI_InputFilename>\n"
              f"                <ESData_RwBufferSize>10240</ESData_RwBufferSize>\n"
              f"              </ESData_TS>"
        )
        blocks_a.append(block_a)
        
    for (s_pid, s_path, s_lang, sin_timecode, pg_value) in (pg_all_value_list):

        if sin_timecode:
            spsts = (
                f"                <stream_presentation_start_time>{pg_value}</stream_presentation_start_time>\n"
        )
            spstss.append(spsts)
        else:
            if sin_timecode != "00:00:00:00":
                spsts = ""

        s_mui_path = s_path + ".mui"
        
        # Check if .mui file exists
        if not os.path.exists(s_mui_path):
            raise FileNotFoundError(f"MUI file not found: {s_mui_path}")

        block_s = (
              f"              <ESData_TS>\n"
              f"                <stream_PID>{s_pid}</stream_PID>\n"
              f"{spsts}"
              f"                <VES_InputFilename>{s_path}</VES_InputFilename>\n"
              f"                <MUI_InputFilename>{s_mui_path}</MUI_InputFilename>\n"
              f"                <ESData_RwBufferSize>10240</ESData_RwBufferSize>\n"
              f"              </ESData_TS>"
        )
        blocks_s.append(block_s)

        if s_path:
            pms = (
            f"            <streams_in_ps>\n"
            f"              <stream_PID>{s_pid}</stream_PID>\n"
            f"              <StreamCodingInfo>\n"
            f"                <stream_coding_type>90</stream_coding_type>\n"
            f"                <Select_stream_coding_type>\n"
            f"                  <PG_stream>\n"
            f"                    <PG_language_code>{s_lang}</PG_language_code>\n"
            f"                    <ISRC>\n"
            f"                      <country_code />\n"
            f"                      <copyright_holder />\n"
            f"                      <recording_year />\n"
            f"                      <recording_number />\n"
            f"                    </ISRC>\n"
            f"                  </PG_stream>\n"
            f"                </Select_stream_coding_type>\n"
            f"              </StreamCodingInfo>\n"
            f"            </streams_in_ps>"
            )
            pmss.append(pms)

    apid = "\n".join(blocks_a + blocks_s)
    all_streams_in_ps = "\n".join(pmss)

    v, _ = os.path.splitext(v_ves_path)
    v_mui_path = v + ".mui"

    if dv_ves_path:
        dv, _= os.path.splitext(dv_ves_path)
        dv_mui_path = dv + ".mui"

    video_stream_avc = f"""  <MPEG4_video_stream>
                        <profile_idc>{v_idc}</profile_idc>
                        <level_idc>{lidc}</level_idc>
                        <frame_mbs_only_flag>{frame_mbs_only_flag}</frame_mbs_only_flag>
                        <long_GOP>{long_GOP}</long_GOP>
                      </MPEG4_video_stream>"""

    video_stream_hevc = f"""  <HEVC_video_stream>
                        <cri_present_flag>{cri_present_flag}</cri_present_flag>
                        <dynamic_range_type>{dynamic_range_type}</dynamic_range_type>
                        <color_space>{colour_primaries}</color_space>
                        <HDR10plus_present_flag>{HDR10plus_present_flag}</HDR10plus_present_flag>
                      </HEVC_video_stream>"""

    if sct == '1B':
        video_stream = video_stream_avc
    elif sct == '24':
        video_stream = video_stream_hevc

    syyqs = []
    dv_ves = ''
    dv_ves_block = ''
    dv_ves_all_info = ''

    if v_ves_path:
        syys = (
              f"<ESData_TS>\n"
                f"                <stream_PID>4113</stream_PID>\n"
                f"                <VES_InputFilename>{v_ves_path}</VES_InputFilename>\n"
                f"                <MUI_InputFilename>{v_mui_path}</MUI_InputFilename>\n"
                f"                <ESData_RwBufferSize>10240</ESData_RwBufferSize>\n"
              f"              </ESData_TS>\n"
         )


        sip_v = f"""  <streams_in_ps>
              <stream_PID>4113</stream_PID>
              <StreamCodingInfo>
                <stream_coding_type>{sct}</stream_coding_type>
                <Select_stream_coding_type>
                  <Video_stream>
                    <video_format>{vfv}</video_format>
                    <frame_rate>{vfps}</frame_rate>
                    <aspect_ratio>3</aspect_ratio>
                    <cc_flag>false</cc_flag>
                    <ISRC>
                      <country_code />
                      <copyright_holder />
                      <recording_year />
                      <recording_number />
                    </ISRC>
                    <Select_Video_stream>
                    {video_stream}
                    </Select_Video_stream>
                  </Video_stream>
                </Select_stream_coding_type>
              </StreamCodingInfo>
            </streams_in_ps>"""

    if dv_ves_path:
        syyq = (
            f'              <ESData_TS>\n'
            f'                <stream_PID>4117</stream_PID>\n'
            f'                <VES_InputFilename>{dv_ves_path}</VES_InputFilename>\n'
            f'                <MUI_InputFilename>{dv_mui_path}</MUI_InputFilename>\n'
            f'                <ESData_RwBufferSize>10240</ESData_RwBufferSize>\n'    
            f'              </ESData_TS>' 
         )
        syyqs.append(syyq)
              
        f_dv_value = "\n".join(syyqs)
        dv_ves_block = f"\n{f_dv_value}" if f_dv_value else ""


        sip_dv = f"""            <streams_in_ps>
              <stream_PID>4117</stream_PID>
              <StreamCodingInfo>
                <stream_coding_type>{sct_dv_value}</stream_coding_type>
                <Select_stream_coding_type>
                  <Video_stream>
                    <video_format>{video_dv_format_code}</video_format>
                    <frame_rate>{fps_code_0_dv}</frame_rate>
                    <aspect_ratio>3</aspect_ratio>
                    <cc_flag>false</cc_flag>
                    <ISRC>
                      <country_code />
                      <copyright_holder />
                      <recording_year />
                      <recording_number />
                    </ISRC>
                    <Select_Video_stream>
                      <HEVC_video_stream>
                        <cri_present_flag>{cpf_value_mode_dv}</cri_present_flag>
                        <dynamic_range_type>{dynamic_range_type_dv}</dynamic_range_type>
                        <color_space>{color_space_dv}</color_space>
                        <HDR10plus_present_flag>{hdr10pf_value_mode_dv}</HDR10plus_present_flag>
                      </HEVC_video_stream>
                    </Select_Video_stream>
                  </Video_stream>
                </Select_stream_coding_type>
              </StreamCodingInfo>
            </streams_in_ps>"""

        dv_ves_all_info = f"\n{sip_dv}" if sip_dv else ""
    
    audio_stream = ""
    blocks = []
    blocks_80 = []
    blocks_816 = []
    blocks_8256 = []
    dts_index = 0
    dolby_index = 0

    for idx, (pid, a_path, lang) in enumerate(a_ves_pid_list):
        aci_code = aci_list[idx]
        apt_value = apt_list[idx]
        sf_value = sf_list[idx]

        if idx < len(adps_list) and idx < len(ca_list) and idx < len(bps_list) and apt_list[idx] and ca_list[idx] and bps_list[idx]:
            adps_value= adps_list[idx]
            ca_value = ca_list[idx]
            bps_value = bps_list[idx]
        else:
            adps_value = None
            ca_value = None
            bps_value = None

        if a_ves_paths:
            if aci_code == '80':
                block_80 = (
                    f"            <streams_in_ps>\n"
                    f"              <stream_PID>{pid}</stream_PID>\n"
                    f"              <StreamCodingInfo>\n"
                    f"                <stream_coding_type>{aci_code}</stream_coding_type>\n"
                    f"                <Select_stream_coding_type>\n"
                    f"                  <Audio_stream>\n"
                    f"                    <audio_presentation_type>{apt_value}</audio_presentation_type>\n"
                    f"                    <sampling_frequency>{sf_value}</sampling_frequency>\n"
                    f"                    <audio_language_code>{lang}</audio_language_code>\n"
                    f"                    <ISRC>\n"
                    f"                      <country_code />\n"
                    f"                      <copyright_holder />\n"
                    f"                      <recording_year />\n"
                    f"                      <recording_number />\n"
                    f"                    </ISRC>\n"
                    f"                    <Select_Audio_stream>\n"
                    f"                      <LPCM_audio>\n"
                    f"                        <audio_data_payload_size>{adps_value}</audio_data_payload_size>\n"
                    f"                        <channel_assignment>{ca_value}</channel_assignment>\n"
                    f"                        <bits_per_sample>{bps_value}</bits_per_sample>\n"
                    f"                      </LPCM_audio>\n"
                    f"                    </Select_Audio_stream>\n"
                    f"                  </Audio_stream>\n"
                    f"                </Select_stream_coding_type>\n"
                    f"              </StreamCodingInfo>\n"
                    f"            </streams_in_ps>"
                )
                blocks_80.append(block_80)

            elif aci_code in ['81', '83', '84']:

                    if dolby_index < len(ast_value_list) and dolby_index < len(src_value_list) and dolby_index < len(bsid_value_list) and dolby_index < len(brc_value_list) and dolby_index < len(dsurmod_value_list) and dolby_index < len(bsmod_value_list) and \
                        dolby_index < len(nc_value_list) and dolby_index < len(full_svc_value_list) and dolby_index < len(langcod_value_list) and dolby_index < len(langcod2_value_list) and dolby_index < len(mainid_value_list) and dolby_index < len(asvcflags_value_list) and dolby_index < len(tcflag_value_list):
                        
                        ast_types = ast_value_list[dolby_index]
                        src_types = src_value_list[dolby_index]
                        bsid_types = bsid_value_list[dolby_index]
                        brc_types = brc_value_list[dolby_index]
                        dsurmod_types = dsurmod_value_list[dolby_index]
                        bsmod_types = bsmod_value_list[dolby_index]
                        nc_types = nc_value_list[dolby_index]
                        full_svc_types = full_svc_value_list[dolby_index]
                        langcod_types = langcod_value_list[dolby_index]
                        langcod2_types = langcod2_value_list[dolby_index]
                        mainid_types = mainid_value_list[dolby_index]
                        asvcflags_types = asvcflags_value_list[dolby_index]
                        tcflag_types = tcflag_value_list[dolby_index]

                        if aci_code == '83':
                            if dolby_index < len(mlp_sampling_rate_value_list):
                                mlp_sampling_rate_value_types = mlp_sampling_rate_value_list[dolby_index]

                            else:
                                mlp_sampling_rate_value_types = ""
                        
                    else:
                        ast_types = ""
                        src_types = ""
                        bsid_types = ""
                        brc_types = ""
                        dsurmod_types = ""
                        bsmod_types = ""
                        nc_types = ""
                        full_svc_types = ""
                        langcod_types = ""
                        langcod2_types = ""
                        mainid_types = ""
                        asvcflags_types = ""
                        tcflag_types = ""
                        
                    mlp = ""
                    if aci_code == '83' and mlp_sampling_rate_value_types:
                        mlp = f"                        <mlp_sampling_rate>{mlp_sampling_rate_value_types}</mlp_sampling_rate>\n"
                                                
                    dolby_index += 1

                    block_816 = (
                        f"            <streams_in_ps>\n"
                        f"              <stream_PID>{pid}</stream_PID>\n"
                        f"              <StreamCodingInfo>\n"
                        f"                <stream_coding_type>{aci_code}</stream_coding_type>\n"
                        f"                <Select_stream_coding_type>\n"
                        f"                  <Audio_stream>\n"
                        f"                    <audio_presentation_type>{apt_value}</audio_presentation_type>\n"
                        f"                    <sampling_frequency>{sf_value}</sampling_frequency>\n"
                        f"                    <audio_language_code>{lang}</audio_language_code>\n"
                        f"                    <ISRC>\n"
                        f"                      <country_code />\n"
                        f"                      <copyright_holder />\n"
                        f"                      <recording_year />\n"
                        f"                      <recording_number />\n"
                        f"                    </ISRC>\n"
                        f"                    <Select_Audio_stream>\n"
                        f"                      <AC3_audio>\n"
                        f"                        <ac3_stream_type>{ast_types}</ac3_stream_type>\n"
                        f"                        <sample_rate_code>{src_types}</sample_rate_code>\n"
                        f"                        <bsid>{bsid_types}</bsid>\n"
                        f"                        <bit_rate_code>{brc_types}</bit_rate_code>\n"
                        f"                        <dsurmod>{dsurmod_types}</dsurmod>\n"
                        f"                        <bsmod>{bsmod_types}</bsmod>\n"
                        f"                        <num_channels>{nc_types}</num_channels>\n"
                        f"                        <full_svc>{full_svc_types}</full_svc>\n"
                        f"                        <langcod>{langcod_types}</langcod>\n"
                        f"                        <langcod2>{langcod2_types}</langcod2>\n"
                        f"                        <mainid>{mainid_types}</mainid>\n"
                        f"                        <asvcflags>{asvcflags_types}</asvcflags>\n"
                        f"                        <text_code>{tcflag_types}</text_code>\n"
                        f"                        <text />\n"
                        f"{mlp}"
                        f"                      </AC3_audio>\n"
                        f"                    </Select_Audio_stream>\n"
                        f"                  </Audio_stream>\n"
                        f"                </Select_stream_coding_type>\n"
                        f"              </StreamCodingInfo>\n"
                        f"            </streams_in_ps>"
                    )
                    blocks_816.append(block_816)

            elif aci_code in ['82', '85', '86']:

                if dts_index < len(dts_stream_type_value_list):
                    dts_types = dts_stream_type_value_list[dts_index]
                else:
                    dts_types = ""
                dts_index += 1
                     
                block_8256 = (
                    f"            <streams_in_ps>\n"
                    f"              <stream_PID>{pid}</stream_PID>\n"
                    f"              <StreamCodingInfo>\n"
                    f"                <stream_coding_type>{aci_code}</stream_coding_type>\n"
                    f"                <Select_stream_coding_type>\n"
                    f"                  <Audio_stream>\n"
                    f"                    <audio_presentation_type>{apt_value}</audio_presentation_type>\n"
                    f"                    <sampling_frequency>{sf_value}</sampling_frequency>\n"
                    f"                    <audio_language_code>{lang}</audio_language_code>\n"
                    f"                    <ISRC>\n"
                    f"                      <country_code />\n"
                    f"                      <copyright_holder />\n"
                    f"                      <recording_year />\n"
                    f"                      <recording_number />\n"
                    f"                    </ISRC>\n"
                    f"                    <Select_Audio_stream>\n"
                    f"                      <DTS_audio>\n"
                    f"                        <dts_stream_type>{dts_types}</dts_stream_type>\n"
                    f"                      </DTS_audio>\n"
                    f"                    </Select_Audio_stream>\n"
                    f"                  </Audio_stream>\n"
                    f"                </Select_stream_coding_type>\n"
                    f"              </StreamCodingInfo>\n"
                    f"            </streams_in_ps>"
                )
                blocks_8256.append(block_8256)

        audio_stream = "\n".join(blocks_80 + blocks_816 + blocks_8256)

    # Generate CLPI append blocks for each append group
    clpi_append_blocks = []
    if all_group_results:  # Process if there are any append groups
        for idx, group_data in enumerate(all_group_results, start=88889):  # Start from 88889
            group = group_data['group']
            group_result = group_data['result']
            group_pg_all_value_list = group_data.get('pg_all_value_list', [])
            group_presentation_start_time = group_data.get('presentation_start_time', '0')
            group_presentation_end_time = group_data.get('presentation_end_time', '0')
            group_encoding_info = group_data.get('encoding_info', {})
            group_audio_encoding_info = group_data.get('audio_encoding_info', {})
            group_ain = group_data.get('ain', None)
            group_sin = group_data.get('sin', None)
            
            # Extract encoding info from group result
            group_f = group.get('f', '')
            group_a = group.get('a', [])
            group_s = group.get('s', [])
            group_alang = group.get('alang', [])
            group_slang = group.get('slang', [])
            
            # Skip this group if it doesn't have its own files
            if not group_f and not group_a and not group_s:
                continue
            
            # Use encoding_info from group if available, otherwise unpack from result
            if group_encoding_info:
                # Use the encoding info from args_parser for this specific group
                # The key names from args_parser are different from the tuple names
                group_vfc = group_encoding_info.get('video_format_code', '6')
                group_sct = group_encoding_info.get('stream_coding_type', '1B')
                group_API = group_encoding_info.get('profile_idc', '100')
                group_li = group_encoding_info.get('level_idc', '41')
                group_fmof = group_encoding_info.get('frame_mbs_only_flag', True)
                group_lg = group_encoding_info.get('long_GOP', False)
                group_cri = group_encoding_info.get('cri_present_flag', 'false')
                group_dynamic_range = group_encoding_info.get('dynamic_range_type', '0')
                group_colour_primaries = group_encoding_info.get('colour_primaries', '1')
                group_HDR10plus = group_encoding_info.get('HDR10plus_present_flag', 'false')
                # For audio, use the actual encoding info from audio_encoding_info
                group_aci = group_audio_encoding_info.get('aci_list') if group_audio_encoding_info else ['83']
                group_apt = group_audio_encoding_info.get('apt_list') if group_audio_encoding_info else ['6']
                group_sf = group_audio_encoding_info.get('sf_list') if group_audio_encoding_info else ['1']
                group_adps = group_audio_encoding_info.get('adps_list') if group_audio_encoding_info and group_a else []
                group_ca = group_audio_encoding_info.get('ca_list') if group_audio_encoding_info and group_a else []
                group_bps = group_audio_encoding_info.get('bps_list') if group_audio_encoding_info and group_a else []
                group_bsid = group_audio_encoding_info.get('bsid_list') if group_audio_encoding_info and group_a else [6]
                group_brc = group_audio_encoding_info.get('brc_list') if group_audio_encoding_info and group_a else [18]
                group_dsurmod = group_audio_encoding_info.get('dsurmod_list') if group_audio_encoding_info and group_a else [0]
                group_bsmod = group_audio_encoding_info.get('bsmod_list') if group_audio_encoding_info and group_a else [0]
                group_nc = group_audio_encoding_info.get('nc_list') if group_audio_encoding_info and group_a else [7]
                group_full_svc = group_audio_encoding_info.get('full_svc_list') if group_audio_encoding_info and group_a else [False]
                group_langcod = group_audio_encoding_info.get('langcod_list') if group_audio_encoding_info and group_a else [0]
                group_langcod2 = group_audio_encoding_info.get('langcod2_list') if group_audio_encoding_info and group_a else [0]
                group_mainid = group_audio_encoding_info.get('mainid_list') if group_audio_encoding_info and group_a else [0]
                group_asvcflags = group_audio_encoding_info.get('asvcflags_list') if group_audio_encoding_info and group_a else [0]
                group_mlp_sr = group_audio_encoding_info.get('mlp_sr_list') if group_audio_encoding_info and group_a else ['MLP_48KHZ']
                group_ast = group_audio_encoding_info.get('ast_list') if group_audio_encoding_info and group_a else ['DLL_PRI']
                group_src = group_audio_encoding_info.get('src_list') if group_audio_encoding_info and group_a else [0]
                group_dts_stream_type = group_audio_encoding_info.get('dts_stream_type_list') if group_audio_encoding_info and group_a else ['']
                # Ensure lists are not None
                if group_aci is None: group_aci = ['83']
                if group_apt is None: group_apt = ['6']
                if group_sf is None: group_sf = ['1']
                if group_adps is None: group_adps = []
                if group_ca is None: group_ca = []
                if group_bps is None: group_bps = []
                if group_bsid is None: group_bsid = [6]
                if group_brc is None: group_brc = [18]
                if group_dsurmod is None: group_dsurmod = [0]
                if group_bsmod is None: group_bsmod = [0]
                if group_nc is None: group_nc = [7]
                if group_full_svc is None: group_full_svc = [False]
                if group_langcod is None: group_langcod = [0]
                if group_langcod2 is None: group_langcod2 = [0]
                if group_mainid is None: group_mainid = [0]
                if group_asvcflags is None: group_asvcflags = [0]
                if group_mlp_sr is None: group_mlp_sr = ['MLP_48KHZ']
                if group_ast is None: group_ast = ['DLL_PRI']
                if group_src is None: group_src = [0]
                if group_dts_stream_type is None: group_dts_stream_type = ['']
                # HEVC/DV related
                group_sct_dv = group_encoding_info.get('sct_dv_value', '24')
                group_video_dv_format = group_encoding_info.get('video_dv_format_code', '6')
                group_fps_code_0_dv = group_encoding_info.get('fps_code_0_dv', '1')
                group_cpf_mode_dv = group_encoding_info.get('cpf_value_mode_dv', 'false')
                group_color_space_dv = group_encoding_info.get('color_space_dv', '1')
                group_dynamic_range_dv = group_encoding_info.get('dynamic_range_type_dv', '0')
                group_hdr10pf_mode_dv = group_encoding_info.get('hdr10pf_value_mode_dv', 'false')
            else:
                # Fallback to unpacking from result tuple
                (group_vfc, group_vfc_mode, group_sct, group_sct_mode, group_aci, group_apt, group_sf, 
                 group_adps, group_ca, group_bps, group_audio_infos, group_API, group_li, 
                 group_fmof, group_lg, group_dts_stream_type, group_ast, group_src, group_bsid, 
                 group_brc, group_dsurmod, group_bsmod, group_nc, group_full_svc, group_langcod, 
                 group_langcod2, group_mainid, group_asvcflags, group_tcflag, group_mlp_sr, 
                 group_cri, group_dynamic_range, group_colour_primaries, group_main_cp, 
                 group_hdr10pf, group_dp_x0, group_dp_y0, group_dp_x1, group_dp_y1, 
                 group_dp_x2, group_dp_y2, group_wp_x, group_wp_y, group_max_dml, 
                 group_min_dml, group_maxCLL, group_maxFALL, group_sct_dv_mode, 
                 group_video_dv_format_mode, group_fps_dv, group_colorspec_mode_dv, 
                 group_sct_dv, group_video_dv_format, group_fps_code_0_dv, group_dm, 
                 group_cpf_mode_dv, group_color_space_dv, group_dynamic_range_dv, 
                 group_hdr10pf_mode_dv) = group_result
            
            # Build ESData_TS blocks for this group
            esdata_blocks = []
            if group_f:
                esdata_blocks.append(
                    f"              <ESData_TS>\n"
                    f"                <stream_PID>4113</stream_PID>\n"
                    f"                <VES_InputFilename>{group_f}</VES_InputFilename>\n"
                    f"                <MUI_InputFilename>{group_f.replace('.ves', '.mui')}</MUI_InputFilename>\n"
                    f"                <ESData_RwBufferSize>10240</ESData_RwBufferSize>\n"
                    f"              </ESData_TS>"
                )
            
            # Convert ain to stream_presentation_start_time if available
            group_tc_starttimecode = group_data.get('encoding_info', {}).get('tc_start_timecode', '00:00:00:00')
            group_ain_value = None
            if group_ain:
                ain_timecode = group_ain
                ain_result = pg(ain_timecode, group_tc_starttimecode, ves_path=group_f)
                if ain_result:
                    group_ain_value = ain_result.get('value', None)
            
            audio_pid_es = 4352
            for audio_file in group_a:
                esdata_blocks.append(
                    f"              <ESData_TS>\n"
                    f"                <stream_PID>{audio_pid_es}</stream_PID>\n"
                    f"                <stream_presentation_start_time>{group_ain_value}</stream_presentation_start_time>\n"
                    f"                <VES_InputFilename>{audio_file}</VES_InputFilename>\n"
                    f"                <MUI_InputFilename>{audio_file.replace('.ves', '.mui')}</MUI_InputFilename>\n"
                    f"                <ESData_RwBufferSize>10240</ESData_RwBufferSize>\n"
                    f"              </ESData_TS>"
                )
                audio_pid_es += 1
            
            # Generate subtitle PIDs for this group (starting from 4608)
            sub_pid = 4608
            for sub_file in group_s:
                # Get pg_value from pg_all_value_list
                pg_value = "54000000"
                for (s_pid, s_path, lang, sin_timecode, pg_val) in group_pg_all_value_list:
                    if s_path == sub_file:
                        pg_value = pg_val
                        break
                
                # Generate .mui path and check if it exists
                s_mui_path = sub_file + ".mui"
                if not os.path.exists(s_mui_path):
                    raise FileNotFoundError(f"MUI file not found: {s_mui_path}")

                esdata_blocks.append(
                    f"              <ESData_TS>\n"
                    f"                <stream_PID>{sub_pid}</stream_PID>\n"
                    f"                <stream_presentation_start_time>{pg_value}</stream_presentation_start_time>\n"
                    f"                <VES_InputFilename>{sub_file}</VES_InputFilename>\n"
                    f"                <MUI_InputFilename>{s_mui_path}</MUI_InputFilename>\n"
                    f"                <ESData_RwBufferSize>10240</ESData_RwBufferSize>\n"
                    f"              </ESData_TS>"
                )
                sub_pid += 1
            
            esdata_section = "\n".join(esdata_blocks) if esdata_blocks else ""
            
            # Build StreamCodingInfo blocks dynamically based on actual encoding info
            stream_coding_blocks = []
            
            # Video stream coding info - choose format based on stream_coding_type
            if group_f:
                if group_sct == '24':
                    # HEVC video stream
                    video_stream_content = f'''<HEVC_video_stream>
                        <cri_present_flag>{group_cri}</cri_present_flag>
                        <dynamic_range_type>{group_dynamic_range}</dynamic_range_type>
                        <color_space>{group_colour_primaries}</color_space>
                        <HDR10plus_present_flag>{group_HDR10plus}</HDR10plus_present_flag>
                      </HEVC_video_stream>'''
                else:
                    # MPEG4/AVC video stream (default for '1B' or other)
                    video_stream_content = f'''<MPEG4_video_stream>
                        <profile_idc>{group_API}</profile_idc>
                        <level_idc>{group_li}</level_idc>
                        <frame_mbs_only_flag>{str(group_fmof).lower()}</frame_mbs_only_flag>
                        <long_GOP>{str(group_lg).lower()}</long_GOP>
                      </MPEG4_video_stream>'''
                
                stream_coding_blocks.append(f'''            <streams_in_ps>
              <stream_PID>4113</stream_PID>
              <StreamCodingInfo>
                <stream_coding_type>{group_sct}</stream_coding_type>
                <Select_stream_coding_type>
                  <Video_stream>
                    <video_format>{group_vfc}</video_format>
                    <frame_rate>{vfps}</frame_rate>
                    <aspect_ratio>3</aspect_ratio>
                    <cc_flag>false</cc_flag>
                    <ISRC>
                      <country_code />
                      <copyright_holder />
                      <recording_year />
                      <recording_number />
                    </ISRC>
                    <Select_Video_stream>
                    {video_stream_content}
                    </Select_Video_stream>
                  </Video_stream>
                </Select_stream_coding_type>
              </StreamCodingInfo>
            </streams_in_ps>''')
            
            # Audio stream coding info
            audio_pid = 4352
            for i, audio_file in enumerate(group_a):
                audio_lang = group_alang[i] if i < len(group_alang) else 'und'
                aci_code = group_aci[i] if i < len(group_aci) else '83'
                apt_val = group_apt[i] if i < len(group_apt) else '6'
                sf_val = group_sf[i] if i < len(group_sf) else '1'
                
                # Build audio stream content based on audio coding type
                if aci_code == '80':
                    # LPCM audio
                    adps_val = group_adps[i] if i < len(group_adps) else 1920
                    ca_val = group_ca[i] if i < len(group_ca) else 1
                    bps_val = group_bps[i] if i < len(group_bps) else 1
                    audio_stream_content = f'''<LPCM_audio>
                        <audio_data_payload_size>{adps_val}</audio_data_payload_size>
                        <channel_assignment>{ca_val}</channel_assignment>
                        <bits_per_sample>{bps_val}</bits_per_sample>
                      </LPCM_audio>'''
                elif aci_code in ['82', '85', '86']:
                    # DTS audio
                    dts_type = group_dts_stream_type[i] if i < len(group_dts_stream_type) else ''
                    audio_stream_content = f'''<DTS_audio>
                        <dts_stream_type>{dts_type}</dts_stream_type>
                      </DTS_audio>'''
                elif aci_code in ['81', '83', '84']:
                    # AC3 audio (81, 83, 84)
                    ast_val = group_ast[i] if i < len(group_ast) else 'DLL_PRI'
                    src_val = group_src[i] if i < len(group_src) else '0'
                    bsid_val = group_bsid[i] if i < len(group_bsid) else 6
                    brc_val = group_brc[i] if i < len(group_brc) else 18
                    dsurmod_val = group_dsurmod[i] if i < len(group_dsurmod) else 0
                    bsmod_val = group_bsmod[i] if i < len(group_bsmod) else 0
                    nc_val = group_nc[i] if i < len(group_nc) else 7
                    full_svc_val = str(group_full_svc[i] if i < len(group_full_svc) else False).lower()
                    langcod_val = group_langcod[i] if i < len(group_langcod) else 0
                    langcod2_val = group_langcod2[i] if i < len(group_langcod2) else 0
                    mainid_val = group_mainid[i] if i < len(group_mainid) else 0
                    asvcflags_val = group_asvcflags[i] if i < len(group_asvcflags) else 0
                    mlp_val = group_mlp_sr[i] if i < len(group_mlp_sr) else 'MLP_48KHZ'
                    
                    mlp_tag = f'\n                        <mlp_sampling_rate>{mlp_val}</mlp_sampling_rate>' if aci_code == '83' else ''
                    
                    audio_stream_content = f'''<AC3_audio>
                        <ac3_stream_type>{ast_val}</ac3_stream_type>
                        <sample_rate_code>{src_val}</sample_rate_code>
                        <bsid>{bsid_val}</bsid>
                        <bit_rate_code>{brc_val}</bit_rate_code>
                        <dsurmod>{dsurmod_val}</dsurmod>
                        <bsmod>{bsmod_val}</bsmod>
                        <num_channels>{nc_val}</num_channels>
                        <full_svc>{full_svc_val}</full_svc>
                        <langcod>{langcod_val}</langcod>
                        <langcod2>{langcod2_val}</langcod2>
                        <mainid>{mainid_val}</mainid>
                        <asvcflags>{asvcflags_val}</asvcflags>
                        <text_code>false</text_code>
                        <text />{mlp_tag}
                      </AC3_audio>'''
                else:
                    # Unknown audio type, use AC3 as fallback
                    audio_stream_content = ''
                
                stream_coding_blocks.append(f'''            <streams_in_ps>
              <stream_PID>{audio_pid}</stream_PID>
              <StreamCodingInfo>
                <stream_coding_type>{aci_code}</stream_coding_type>
                <Select_stream_coding_type>
                  <Audio_stream>
                    <audio_presentation_type>{apt_val}</audio_presentation_type>
                    <sampling_frequency>{sf_val}</sampling_frequency>
                    <audio_language_code>{audio_lang}</audio_language_code>
                    <ISRC>
                      <country_code />
                      <copyright_holder />
                      <recording_year />
                      <recording_number />
                    </ISRC>
                    <Select_Audio_stream>
                    {audio_stream_content}
                    </Select_Audio_stream>
                  </Audio_stream>
                </Select_stream_coding_type>
              </StreamCodingInfo>
            </streams_in_ps>''')
                audio_pid += 1
            
            # Subtitle stream coding info
            sub_pid = 4608
            for i, sub_file in enumerate(group_s):
                sub_lang = group_slang[i] if i < len(group_slang) else 'und'
                stream_coding_blocks.append(f'''            <streams_in_ps>
              <stream_PID>{sub_pid}</stream_PID>
              <StreamCodingInfo>
                <stream_coding_type>90</stream_coding_type>
                <Select_stream_coding_type>
                  <PG_stream>
                    <PG_language_code>{sub_lang}</PG_language_code>
                    <ISRC>
                      <country_code />
                      <copyright_holder />
                      <recording_year />
                      <recording_number />
                    </ISRC>
                  </PG_stream>
                </Select_stream_coding_type>
              </StreamCodingInfo>
            </streams_in_ps>''')
                sub_pid += 1
            
            stream_coding_section = "\n".join(stream_coding_blocks) if stream_coding_blocks else ""
            
            clpi_block = f"""  <CLPI FileName="{idx}">
    <type_indicator>HDMV</type_indicator>
    <version_number>0300</version_number>
    <ClipInfo>
      <Clip_stream_type>1</Clip_stream_type>
      <application_type>1</application_type>
      <is_ATC_delta>false</is_ATC_delta>
      <TS_type_info_block>
        <Validity_flags>80</Validity_flags>
        <Format_identifier>48444D56</Format_identifier>
        <Network_information>000000000000000000</Network_information>
        <Stream_format_name>00000000000000000000000000000000</Stream_format_name>
      </TS_type_info_block>
      <Select_is_ATC_delta />
      <Select_application_type />
    </ClipInfo>
    <Loop_padding_word_1 />
    <SequenceInfo>
      <number_of_ATC_sequences>1</number_of_ATC_sequences>
      <Loop_ATC_sequence>
        <ATC_sequence>
          <number_of_STC_sequences>1</number_of_STC_sequences>
          <Loop_STC_sequence>
            <STC_sequence>
              <presentation_start_time>{group_presentation_start_time}</presentation_start_time>
              <presentation_end_time>{group_presentation_end_time}</presentation_end_time>
{esdata_section}
            </STC_sequence>
          </Loop_STC_sequence>
        </ATC_sequence>
      </Loop_ATC_sequence>
    </SequenceInfo>
    <Loop_padding_word_2 />
    <ProgramInfo>
      <number_of_program_sequences>1</number_of_program_sequences>
      <Loop_program_sequences>
        <program_sequences>
          <SPN_program_sequence_start>0</SPN_program_sequence_start>
          <program_map_PID>256</program_map_PID>
          <number_of_streams_in_ps>{len(stream_coding_blocks)}</number_of_streams_in_ps>
          <Loop_stream_in_ps>
{stream_coding_section}
          </Loop_stream_in_ps>
        </program_sequences>
      </Loop_program_sequences>
    </ProgramInfo>
    <Loop_padding_word_3 />
    <CPI>
      <Select_CPI_data />
    </CPI>
    <Loop_padding_word_4 />
    <ClipMark>
      <length>0</length>
    </ClipMark>
    <Loop_padding_word_5 />
    <Loop_padding_word_6 />
    <HDMV_TS_Descriptor>
      <HDMV_copy_control_descriptor>
        <private_data_byte1>
          <Reserved>01</Reserved>
          <RetentionMoveMode>01</RetentionMoveMode>
          <RetentionState>07</RetentionState>
          <EPN>01</EPN>
          <CCI>03</CCI>
        </private_data_byte1>
        <private_data_byte2>
          <Reserved2>1F</Reserved2>
          <ImageConstraintToken>00</ImageConstraintToken>
          <APS>00</APS>
        </private_data_byte2>
      </HDMV_copy_control_descriptor>
    </HDMV_TS_Descriptor>
    <TP_extra_header>
      <copy_permission_indicator>3</copy_permission_indicator>
    </TP_extra_header>
    <M2TSDirectoryList>
      <TS_Intermediatefile_dir>{mp}{fu}Output{fu}MUX{fu}BDROM{fu}TSIntermediate{fu}{idx}</TS_Intermediatefile_dir>
      <TS_Intermediatefile_RwBufferSize>10240</TS_Intermediatefile_RwBufferSize>
      <TS_M2TS_output_dir>{mp}{fu}Output{fu}MUX{fu}BDROM{fu}DB{fu}BDMV{fu}STREAM</TS_M2TS_output_dir>
      <TS_M2TS_output_RwBufferSize>10240</TS_M2TS_output_RwBufferSize>
    </M2TSDirectoryList>
  </CLPI>"""

            clpi_append_blocks.append(clpi_block)
    
    clpi_append = "\n".join(clpi_append_blocks)

    if not clpi_append:
      clpi_append = ""
    else:
      clpi_append = "\n" + clpi_append.rstrip('\n')
    
    stream_parts = [sip_v, audio_stream, all_streams_in_ps, dv_ves_all_info]
    stream_parts = [p.rstrip() for p in stream_parts if p and p.strip()]
    stream_content = "\n".join(stream_parts)
    
    xml_template = f"""
<?xml version="1.0" encoding="UTF-8"?>
<CLIPDescriptorFile Version="0099" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="CLIPDescriptor.xsd">
  <CLPI FileName="88888">
    <type_indicator>HDMV</type_indicator>
    <version_number>0300</version_number>
    <ClipInfo>
      <Clip_stream_type>1</Clip_stream_type>
      <application_type>1</application_type>
      <is_ATC_delta>false</is_ATC_delta>
      <TS_type_info_block>
        <Validity_flags>80</Validity_flags>
        <Format_identifier>48444D56</Format_identifier>
        <Network_information>000000000000000000</Network_information>
        <Stream_format_name>00000000000000000000000000000000</Stream_format_name>
      </TS_type_info_block>
      <Select_is_ATC_delta />
      <Select_application_type />
    </ClipInfo>
    <Loop_padding_word_1 />
    <SequenceInfo>
      <number_of_ATC_sequences>1</number_of_ATC_sequences>
      <Loop_ATC_sequence>
        <ATC_sequence>
          <number_of_STC_sequences>1</number_of_STC_sequences>
          <Loop_STC_sequence>
            <STC_sequence>
              <presentation_start_time>{in_time}</presentation_start_time>
              <presentation_end_time>{out_time}</presentation_end_time>
              {syys}{apid}{dv_ves_block}
            </STC_sequence>
          </Loop_STC_sequence>
        </ATC_sequence>
      </Loop_ATC_sequence>
    </SequenceInfo>
    <Loop_padding_word_2 />
    <ProgramInfo>
      <number_of_program_sequences>1</number_of_program_sequences>
      <Loop_program_sequences>
        <program_sequences>
          <SPN_program_sequence_start>0</SPN_program_sequence_start>
          <program_map_PID>256</program_map_PID>
          <number_of_streams_in_ps>{nosip}</number_of_streams_in_ps>
          <Loop_stream_in_ps>
          {stream_content}
          </Loop_stream_in_ps>
        </program_sequences>
      </Loop_program_sequences>
    </ProgramInfo>
    <Loop_padding_word_3 />
    <CPI>
      <Select_CPI_data />
    </CPI>
    <Loop_padding_word_4 />
    <ClipMark>
      <length>0</length>
    </ClipMark>
    <Loop_padding_word_5 />
    <Loop_padding_word_6 />
    <HDMV_TS_Descriptor>
      <HDMV_copy_control_descriptor>
        <private_data_byte1>
          <Reserved>01</Reserved>
          <RetentionMoveMode>01</RetentionMoveMode>
          <RetentionState>07</RetentionState>
          <EPN>01</EPN>
          <CCI>03</CCI>
        </private_data_byte1>
        <private_data_byte2>
          <Reserved2>1F</Reserved2>
          <ImageConstraintToken>00</ImageConstraintToken>
          <APS>00</APS>
        </private_data_byte2>
      </HDMV_copy_control_descriptor>
    </HDMV_TS_Descriptor>
    <TP_extra_header>
      <copy_permission_indicator>3</copy_permission_indicator>
    </TP_extra_header>
    <M2TSDirectoryList>
      <TS_Intermediatefile_dir>{mp}{fu}{TSIntermediate}</TS_Intermediatefile_dir>
      <TS_Intermediatefile_RwBufferSize>10240</TS_Intermediatefile_RwBufferSize>
      <TS_M2TS_output_dir>{mp}{fu}{STREAM}</TS_M2TS_output_dir>
      <TS_M2TS_output_RwBufferSize>10240</TS_M2TS_output_RwBufferSize>
    </M2TSDirectoryList>
  </CLPI>{clpi_append}
</CLIPDescriptorFile>""".strip()

    # Validate XML template before returning
    import re
    start_match = re.search(r'<presentation_start_time>([^<]+)</presentation_start_time>', xml_template)
    end_match = re.search(r'<presentation_end_time>([^<]+)</presentation_end_time>', xml_template)

    if not start_match or not end_match:
        if not start_match:
            print(f"    - presentation_start_time is missing")
        if not end_match:
            print(f"    - presentation_end_time is missing")
    

    # Return main CLPI content and append CLPI blocks separately
    return xml_template.strip(), clpi_append_blocks

def maked_fsdescriptor(fu, mp, all_group_results=None):
    # Output
    if all_group_results is None:
        all_group_results = []
    
    # Generate CLPI and m2ts file IDs based on number of groups
    # Main group: 88888, Append groups: 88889, 88890, etc.
    num_groups = len(all_group_results)
    clip_ids = [88888 + i for i in range(num_groups + 1)]  # +1 for main group
    
    # Calculate File_ID offset based on number of CLPI files
    # Single CLPI (88888 only): offset = 0
    # Multiple CLPIs (88888 + append): offset = num_append_groups
    num_clpi = len(clip_ids)
    offset = num_clpi - 1  # 0 for single CLPI, 1+ for multiple

    # Calculate precise dynamic File_IDs based on mathematically proven formulas
    # Fixed BDMV IDs
    BDMV_id = 1
    index_bdmv_id = 2
    MovieObject_bdmv_id = 3
    mpls_id = 4
    PLAYLIST_id = 5

    # CLPI IDs (sequential from 6)
    clpi_fids = [6 + i for i in range(num_clpi)]
    clpi_fids_rev = list(reversed(clpi_fids))
    CLIPINF_id = 6 + num_clpi

    # M2TS IDs (sequential starting after CLIPINF)
    m2ts_fids = [8 + offset + i for i in range(num_clpi)]
    m2ts_fids_rev = list(reversed(m2ts_fids))
    STREAM_id = 9 + 2 * offset

    # Other subdirectories under BDMV (sequential starting after STREAM)
    AUXDATA_id = 10 + 2 * offset
    META_id = 11 + 2 * offset
    BDJO_id = 12 + 2 * offset
    JAR_id = 13 + 2 * offset
    BACKUP_id = 14 + 2 * offset

    # BACKUP subfolder file IDs (sequential starting after BACKUP)
    index_bdmv_backup_id = 15 + 2 * offset
    MovieObject_bdmv_backup_id = 16 + 2 * offset
    mpls_backup_id = 17 + 2 * offset
    PLAYLIST_backup_id = 18 + 2 * offset

    # CLPI backup IDs (sequential starting after PLAYLIST_backup)
    backup_clpi_fids = [19 + 2 * offset + i for i in range(num_clpi)]
    backup_clpi_fids_rev = list(reversed(backup_clpi_fids))
    CLIPINF_backup_id = 20 + 3 * offset

    # Other directories under CERTIFICATE / BACKUP (sequential starting after CLIPINF_backup)
    BDJO_backup_id = 21 + 3 * offset
    JAR_backup_id = 22 + 3 * offset
    CERTIFICATE_id = 23 + 3 * offset
    id_bdmv_id = 24 + 3 * offset
    id_bdmv_backup_id = 25 + 3 * offset
    BACKUP_cert_id = 26 + 3 * offset
    AACS_id = 27 + 3 * offset

    # AACS file IDs
    Content001_cer_id = 29 + 3 * offset
    Content002_cer_id = 30 + 3 * offset
    Content000_cer_id = 31 + 3 * offset
    DH_Pairing_Server_cer_id = 32 + 3 * offset
    MKB_RO_inf_id = 33 + 3 * offset
    Unit_Key_RO_inf_id = 34 + 3 * offset
    CPSUnit00001_cci_id = 35 + 3 * offset
    ContentRevocation_lst_id = 36 + 3 * offset
    DUPLICATE_id = 46 + 3 * offset

    # DUPLICATE file IDs
    Content001_cer_dup_id = 38 + 3 * offset
    Content002_cer_dup_id = 39 + 3 * offset
    Content000_cer_dup_id = 40 + 3 * offset
    DH_Pairing_Server_cer_dup_id = 41 + 3 * offset
    MKB_RO_inf_dup_id = 42 + 3 * offset
    Unit_Key_RO_inf_dup_id = 43 + 3 * offset
    CPSUnit00001_cci_dup_id = 44 + 3 * offset
    ContentRevocation_lst_dup_id = 45 + 3 * offset

    def make_seq_ids(ids):
        return '\n'.join([f'      <Sequence_File_ID>{fid}</Sequence_File_ID>' for fid in ids])

    phys_seqs = []
    # Layer 0 certificates
    phys_seqs.append(f'    <Sequence_unit RequiredLayer="0">\n{make_seq_ids([Content000_cer_id])}\n    </Sequence_unit>')
    # AACS key files
    phys_seqs.append(f'    <Sequence_unit>\n{make_seq_ids([ContentRevocation_lst_id, CPSUnit00001_cci_id, DH_Pairing_Server_cer_id, MKB_RO_inf_id, Unit_Key_RO_inf_id])}\n    </Sequence_unit>')
    # BDMV files (including CLPIs) and id.bdmv
    phys_seqs.append(f'    <Sequence_unit>\n{make_seq_ids([index_bdmv_id, MovieObject_bdmv_id, mpls_id] + clpi_fids_rev + [id_bdmv_id])}\n    </Sequence_unit>')
    # Main clip m2ts ALONE (before DUPLICATE section) — m2ts_fids[-1] is the highest fid = main clip (88888)
    phys_seqs.append(f'    <Sequence_unit>\n{make_seq_ids([m2ts_fids[-1]])}\n    </Sequence_unit>')
    # DUPLICATE key files
    phys_seqs.append(f'    <Sequence_unit>\n{make_seq_ids([ContentRevocation_lst_dup_id, CPSUnit00001_cci_dup_id, DH_Pairing_Server_cer_dup_id, MKB_RO_inf_dup_id, Unit_Key_RO_inf_dup_id])}\n    </Sequence_unit>')
    # BACKUP files (including CLPI backups) and id.bdmv backup
    phys_seqs.append(f'    <Sequence_unit>\n{make_seq_ids([index_bdmv_backup_id, MovieObject_bdmv_backup_id, mpls_backup_id] + backup_clpi_fids_rev + [id_bdmv_backup_id])}\n    </Sequence_unit>')
    # Layer 0 duplicate certificate
    phys_seqs.append(f'    <Sequence_unit RequiredLayer="0">\n{make_seq_ids([Content000_cer_dup_id])}\n    </Sequence_unit>')
    # Append clips m2ts together (after Layer 0 duplicate) — only when there are append groups
    if len(m2ts_fids) > 1:
        phys_seqs.append(f'    <Sequence_unit>\n{make_seq_ids(list(reversed(m2ts_fids[:-1])))}\n    </Sequence_unit>')
    # Layer 1 duplicate certificate
    phys_seqs.append(f'    <Sequence_unit RequiredLayer="1">\n{make_seq_ids([Content001_cer_dup_id])}\n    </Sequence_unit>')
    # Layer 1 certificate
    phys_seqs.append(f'    <Sequence_unit RequiredLayer="1">\n{make_seq_ids([Content001_cer_id])}\n    </Sequence_unit>')
    
    # Layer 2 duplicate certificate and Layer 2 certificate (only added if BD100 triple layer is used)
    # Check if Content002.cer exists on disk to decide if we should output Layer 2 Sequence_units
    import os
    aacs_dir = os.path.join(mp, r"Output\MUX\BDROM\DB\AACS")
    if os.path.exists(os.path.join(aacs_dir, "Content002.cer")):
        phys_seqs.append(f'    <Sequence_unit RequiredLayer="2">\n{make_seq_ids([Content002_cer_dup_id])}\n    </Sequence_unit>')
        phys_seqs.append(f'    <Sequence_unit RequiredLayer="2">\n{make_seq_ids([Content002_cer_id])}\n    </Sequence_unit>')

    physical_dir_struct = '  <Physical_dir_struct>\n' + '\n'.join(phys_seqs) + '\n  </Physical_dir_struct>'
    
    TSIntermediate = r"Output\MUX\BDROM\TSIntermediate"
    FSIntermediate = r"Output\MUX\BDROM\FSIntermediate"
    DBIntermediate = r"Output\MUX\BDROM\DBIntermediate"
    STREAM = r"Output\MUX\BDROM\DB\BDMV\STREAM"
    BDMV = r"Output\MUX\BDROM\DB\BDMV"
    PLAYLIST = r"Output\MUX\BDROM\DB\BDMV\PLAYLIST"
    CLIPINF = r"Output\MUX\BDROM\DB\BDMV\CLIPINF"
    CERTIFICATE = r"Output\MUX\BDROM\DB\CERTIFICATE"
    BACKUP = r"Output\MUX\BDROM\DB\CERTIFICATE\BACKUP"
    AACS = r"Output\MUX\BDROM\DB\AACS"
    DUPLICATE = r"Output\MUX\BDROM\DB\AACS\DUPLICATE"
    image = r"image\BDROM"
    FSIntermediate = r"Output\MUX\BDROM\FSIntermediate"
    BACKUP_CLIPINF = r"Output\MUX\BDROM\DB\BDMV\BACKUP\CLIPINF"
    BACKUP_PLAYLIST = r"Output\MUX\BDROM\DB\BDMV\BACKUP\PLAYLIST"
    META = r"Output\MUX\BDROM\DB\BDMV\META"
    AACS = r"Output\MUX\BDROM\DB\AACS"
    AACS_DUPLICATE = r"Output\MUX\BDROM\DB\AACS\DUPLICATE"

    image = os.path.join(mp, image)
    PLAYLIST = os.path.join(mp, PLAYLIST)
    CLIPINF = os.path.join(mp, CLIPINF)
    BACKUP_CLIPINF = os.path.join(mp, BACKUP_CLIPINF)
    BACKUP_PLAYLIST = os.path.join(mp, BACKUP_PLAYLIST)
    META = os.path.join(mp, META)
    FSIntermediate = os.path.join(mp, FSIntermediate)
    DBIntermediate = os.path.join(mp, DBIntermediate)
    os.makedirs(image, exist_ok=True)
    os.makedirs(PLAYLIST, exist_ok=True)
    os.makedirs(CLIPINF, exist_ok=True)
    os.makedirs(BACKUP_CLIPINF, exist_ok=True)
    os.makedirs(BACKUP_PLAYLIST, exist_ok=True)
    os.makedirs(META, exist_ok=True)
    os.makedirs(FSIntermediate, exist_ok=True)
    os.makedirs(DBIntermediate, exist_ok=True)

    # Conditionally add Content002.cer if it exists
    content002_entry = ""
    if os.path.exists(os.path.join(aacs_dir, "Content002.cer")):
        content002_entry = f"""      <File_entry File_ID="{Content002_cer_id}">
        <Filename>Content002.cer</Filename>
        <Sourcepath>{mp}{fu}{AACS}{fu}Content002.cer</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>"""

    content002_dup_entry = ""
    if os.path.exists(os.path.join(aacs_dir, "DUPLICATE", "Content002.cer")):
        content002_dup_entry = f"""      <File_entry File_ID="{Content002_cer_dup_id}">
        <Filename>Content002.cer</Filename>
        <Sourcepath>{mp}{fu}{AACS_DUPLICATE}{fu}Content002.cer</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>"""

    xml_template = f"""
<?xml version="1.0" encoding="UTF-8"?>
<FSDescriptor Version="0099" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="FSDescriptor.xsd">
  <ForBDCMFCreator>
    <ApplicationInfo>
      <Software>N{fu}A</Software>
      <Version>N{fu}A</Version>
    </ApplicationInfo>
  </ForBDCMFCreator>
  <Volume>
    <Volume_ID>BLURAY_DISC</Volume_ID>
    <Volume_Set_ID>045AF019        BLURAY_DISC</Volume_Set_ID>
    <Application_ID>*N{fu}A</Application_ID>
    <Implementation_ID>*N{fu}A</Implementation_ID>
    <Implementation_Use>*N{fu}A</Implementation_Use>
    <Logical_Volume_ID>BLURAY_DISC</Logical_Volume_ID>
    <File_Set_ID>BLURAY_DISC</File_Set_ID>
  </Volume>
  <Logical_dir_struct>
    <directory File_ID="0">
      <File_entry File_ID="{BDMV_id}">
        <Filename>BDMV</Filename>
        <is_dir>true</is_dir>
      </File_entry>
      <File_entry File_ID="{CERTIFICATE_id}">
        <Filename>CERTIFICATE</Filename>
        <is_dir>true</is_dir>
      </File_entry>
      <File_entry File_ID="{AACS_id}">
        <Filename>AACS</Filename>
        <is_dir>true</is_dir>
      </File_entry>
    </directory>
    <directory File_ID="{BDMV_id}">
      <File_entry File_ID="{index_bdmv_id}">
        <Filename>index.bdmv</Filename>
        <Sourcepath>{mp}{fu}{BDMV}{fu}index.bdmv</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>
      <File_entry File_ID="{MovieObject_bdmv_id}">
        <Filename>MovieObject.bdmv</Filename>
        <Sourcepath>{mp}{fu}{BDMV}{fu}MovieObject.bdmv</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>
      <File_entry File_ID="{PLAYLIST_id}">
        <Filename>PLAYLIST</Filename>
        <is_dir>true</is_dir>
      </File_entry>
      <File_entry File_ID="{CLIPINF_id}">
        <Filename>CLIPINF</Filename>
        <is_dir>true</is_dir>
      </File_entry>
      <File_entry File_ID="{STREAM_id}">
        <Filename>STREAM</Filename>
        <is_dir>true</is_dir>
      </File_entry>
      <File_entry File_ID="{AUXDATA_id}">
        <Filename>AUXDATA</Filename>
        <is_dir>true</is_dir>
      </File_entry>
      <File_entry File_ID="{META_id}">
        <Filename>META</Filename>
        <is_dir>true</is_dir>
      </File_entry>
      <File_entry File_ID="{BDJO_id}">
        <Filename>BDJO</Filename>
        <is_dir>true</is_dir>
      </File_entry>
      <File_entry File_ID="{JAR_id}">
        <Filename>JAR</Filename>
        <is_dir>true</is_dir>
      </File_entry>
      <File_entry File_ID="{BACKUP_id}">
        <Filename>BACKUP</Filename>
        <is_dir>true</is_dir>
      </File_entry>
    </directory>
    <directory File_ID="{PLAYLIST_id}">
      <File_entry File_ID="{mpls_id}">
        <Filename>00000.mpls</Filename>
        <Sourcepath>{PLAYLIST}{fu}00000.mpls</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>
    </directory>
    <directory File_ID="{CLIPINF_id}">
{"".join([f'''      <File_entry File_ID="{fid}">
        <Filename>{clip_id}.clpi</Filename>
        <Sourcepath>{CLIPINF}{fu}{clip_id}.clpi</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>
''' if idx < len(clip_ids) - 1 else f'''      <File_entry File_ID="{fid}">
        <Filename>{clip_id}.clpi</Filename>
        <Sourcepath>{CLIPINF}{fu}{clip_id}.clpi</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>''' for idx, (fid, clip_id) in enumerate(zip(clpi_fids, reversed(clip_ids)))])}
    </directory>
    <directory File_ID="{STREAM_id}">
{"".join([f'''      <File_entry File_ID="{fid}">
        <Filename>{clip_id}.m2ts</Filename>
        <Sourcepath>{mp}{fu}{STREAM}{fu}{clip_id}.m2ts</Sourcepath>
        <is_dir>false</is_dir>
        <TS_Intermediatefile_dir>{mp}{fu}{TSIntermediate}{fu}{clip_id}</TS_Intermediatefile_dir>
      </File_entry>
''' if idx < len(clip_ids) - 1 else f'''      <File_entry File_ID="{fid}">
        <Filename>{clip_id}.m2ts</Filename>
        <Sourcepath>{mp}{fu}{STREAM}{fu}{clip_id}.m2ts</Sourcepath>
        <is_dir>false</is_dir>
        <TS_Intermediatefile_dir>{mp}{fu}{TSIntermediate}{fu}{clip_id}</TS_Intermediatefile_dir>
      </File_entry>''' for idx, (fid, clip_id) in enumerate(zip(m2ts_fids, reversed(clip_ids)))])}
    </directory>
    <directory File_ID="{BACKUP_id}">
      <File_entry File_ID="{index_bdmv_backup_id}">
        <Filename>index.bdmv</Filename>
        <Sourcepath>{mp}{fu}{BDMV}{fu}index.bdmv</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>
      <File_entry File_ID="{MovieObject_bdmv_backup_id}">
        <Filename>MovieObject.bdmv</Filename>
        <Sourcepath>{mp}{fu}{BDMV}{fu}MovieObject.bdmv</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>
      <File_entry File_ID="{PLAYLIST_backup_id}">
        <Filename>PLAYLIST</Filename>
        <is_dir>true</is_dir>
      </File_entry>
      <File_entry File_ID="{CLIPINF_backup_id}">
        <Filename>CLIPINF</Filename>
        <is_dir>true</is_dir>
      </File_entry>
      <File_entry File_ID="{BDJO_backup_id}">
        <Filename>BDJO</Filename>
        <is_dir>true</is_dir>
      </File_entry>
      <File_entry File_ID="{JAR_backup_id}">
        <Filename>JAR</Filename>
        <is_dir>true</is_dir>
      </File_entry>
    </directory>
    <directory File_ID="{PLAYLIST_backup_id}">
      <File_entry File_ID="{mpls_backup_id}">
        <Filename>00000.mpls</Filename>
        <Sourcepath>{PLAYLIST}{fu}00000.mpls</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>
    </directory>
    <directory File_ID="{CLIPINF_backup_id}">
{"".join([f'''      <File_entry File_ID="{fid}">
        <Filename>{clip_id}.clpi</Filename>
        <Sourcepath>{CLIPINF}{fu}{clip_id}.clpi</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>
''' if idx < len(clip_ids) - 1 else f'''      <File_entry File_ID="{fid}">
        <Filename>{clip_id}.clpi</Filename>
        <Sourcepath>{CLIPINF}{fu}{clip_id}.clpi</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>''' for idx, (fid, clip_id) in enumerate(zip(backup_clpi_fids, reversed(clip_ids)))])}
    </directory>
    <directory File_ID="{CERTIFICATE_id}">
      <File_entry File_ID="{id_bdmv_id}">
        <Filename>id.bdmv</Filename>
        <Sourcepath>{mp}{fu}{CERTIFICATE}{fu}id.bdmv</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>
      <File_entry File_ID="{BACKUP_cert_id}">
        <Filename>BACKUP</Filename>
        <is_dir>true</is_dir>
      </File_entry>
    </directory>
    <directory File_ID="{BACKUP_cert_id}">
      <File_entry File_ID="{id_bdmv_backup_id}">
        <Filename>id.bdmv</Filename>
        <Sourcepath>{mp}{fu}{BACKUP}{fu}id.bdmv</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>
    </directory>
    <directory File_ID="{AACS_id}">
      <File_entry File_ID="{Content001_cer_id}">
        <Filename>Content001.cer</Filename>
        <Sourcepath>{mp}{fu}{AACS}{fu}Content001.cer</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>
{content002_entry}
      <File_entry File_ID="{Content000_cer_id}">
        <Filename>Content000.cer</Filename>
        <Sourcepath>{mp}{fu}{AACS}{fu}Content000.cer</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>
      <File_entry File_ID="{DH_Pairing_Server_cer_id}">
        <Filename>DH_Pairing_Server.cer</Filename>
        <Sourcepath>{mp}{fu}{AACS}{fu}DH_Pairing_Server.cer</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>
      <File_entry File_ID="{MKB_RO_inf_id}">
        <Filename>MKB_RO.inf</Filename>
        <Sourcepath>{mp}{fu}{AACS}{fu}MKB_RO.inf</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>
      <File_entry File_ID="{Unit_Key_RO_inf_id}">
        <Filename>Unit_Key_RO.inf</Filename>
        <Sourcepath>{mp}{fu}{AACS}{fu}Unit_Key_RO.inf</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>
      <File_entry File_ID="{CPSUnit00001_cci_id}">
        <Filename>CPSUnit00001.cci</Filename>
        <Sourcepath>{mp}{fu}{AACS}{fu}CPSUnit00001.cci</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>
      <File_entry File_ID="{ContentRevocation_lst_id}">
        <Filename>ContentRevocation.lst</Filename>
        <Sourcepath>{mp}{fu}{AACS}{fu}ContentRevocation.lst</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>
      <File_entry File_ID="{DUPLICATE_id}">
        <Filename>DUPLICATE</Filename>
        <is_dir>true</is_dir>
      </File_entry>
    </directory>
    <directory File_ID="{DUPLICATE_id}">
      <File_entry File_ID="{Content001_cer_dup_id}">
        <Filename>Content001.cer</Filename>
        <Sourcepath>{mp}{fu}{AACS_DUPLICATE}{fu}Content001.cer</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>
{content002_dup_entry}
      <File_entry File_ID="{Content000_cer_dup_id}">
        <Filename>Content000.cer</Filename>
        <Sourcepath>{mp}{fu}{AACS_DUPLICATE}{fu}Content000.cer</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>
      <File_entry File_ID="{DH_Pairing_Server_cer_dup_id}">
        <Filename>DH_Pairing_Server.cer</Filename>
        <Sourcepath>{mp}{fu}{AACS_DUPLICATE}{fu}DH_Pairing_Server.cer</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>
      <File_entry File_ID="{MKB_RO_inf_dup_id}">
        <Filename>MKB_RO.inf</Filename>
        <Sourcepath>{mp}{fu}{AACS_DUPLICATE}{fu}MKB_RO.inf</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>
      <File_entry File_ID="{Unit_Key_RO_inf_dup_id}">
        <Filename>Unit_Key_RO.inf</Filename>
        <Sourcepath>{mp}{fu}{AACS_DUPLICATE}{fu}Unit_Key_RO.inf</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>
      <File_entry File_ID="{CPSUnit00001_cci_dup_id}">
        <Filename>CPSUnit00001.cci</Filename>
        <Sourcepath>{mp}{fu}{AACS_DUPLICATE}{fu}CPSUnit00001.cci</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>
      <File_entry File_ID="{ContentRevocation_lst_dup_id}">
        <Filename>ContentRevocation.lst</Filename>
        <Sourcepath>{mp}{fu}{AACS_DUPLICATE}{fu}ContentRevocation.lst</Sourcepath>
        <is_dir>false</is_dir>
      </File_entry>
    </directory>
  </Logical_dir_struct>
{physical_dir_struct}
  <FS_OutputFilename>
    <Is_Output_CMF>false</Is_Output_CMF>
    <IMAGE>{image}{fu}FSImage0.img</IMAGE>
    <MDC_IMAGE>{image}{fu}MDC_Image0.dat</MDC_IMAGE>
    <UCD>{image}{fu}ucd0.dat</UCD>
    <BDCMF_Filename>
      <BDCMF />
      <FAI>{image}{fu}FAI.DAT</FAI>
      <FMTSMap />
    </BDCMF_Filename>
    <PIC_info_mux>{image}{fu}Pic_info_mux.dat</PIC_info_mux>
    <File_addr_map>{image}{fu}file_addr.map</File_addr_map>
    <FS_Intermediatefile_dir>{FSIntermediate}{fu}</FS_Intermediatefile_dir>
  </FS_OutputFilename>
</FSDescriptor>
"""

    return xml_template.strip()

def maked_indextable():
    xml_template = f"""
<?xml version="1.0" encoding="UTF-8"?>
<IndexTableFile Version="0099" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="IndexTable.xsd">
  <type_indicator>INDX</type_indicator>
  <version_number>0300</version_number>
  <AppInfoBDMV>
    <initial_output_mode_preference>0</initial_output_mode_preference>
    <SS_content_exist_flag>0</SS_content_exist_flag>
    <initial_dynamic_range_type>0</initial_dynamic_range_type>
    <video_format>0</video_format>
    <frame_rate>0</frame_rate>
    <content_provider_user_data>Not</content_provider_user_data>
  </AppInfoBDMV>
  <Loop_padding_word_1 />
  <Indexes>
    <FirstPlayback>
      <FirstPlayback_object_type>01</FirstPlayback_object_type>
      <Select_FirstPlayback_object>
        <FirstPlayback_mobj>
          <HDMV_Title_playback_type>00</HDMV_Title_playback_type>
          <FirstPlayback_mobj_id_ref>0</FirstPlayback_mobj_id_ref>
        </FirstPlayback_mobj>
      </Select_FirstPlayback_object>
    </FirstPlayback>
    <TopMenu>
      <TopMenu_object_type>01</TopMenu_object_type>
      <Select_TopMenu_object>
        <TopMenu_mobj>
          <HDMV_Title_playback_type>01</HDMV_Title_playback_type>
          <TopMenu_mobj_id_ref>1</TopMenu_mobj_id_ref>
        </TopMenu_mobj>
      </Select_TopMenu_object>
    </TopMenu>
    <number_of_Titles>1</number_of_Titles>
    <Loop_Title>
      <Title>
        <Title_object_type>01</Title_object_type>
        <Title_access_type>00</Title_access_type>
        <Select_Title_object>
          <Title_mobj>
            <HDMV_Title_playback_type>00</HDMV_Title_playback_type>
            <Title_mobj_id_ref>2</Title_mobj_id_ref>
          </Title_mobj>
        </Select_Title_object>
      </Title>
    </Loop_Title>
  </Indexes>
  <Loop_padding_word_2 />
  <ExtensionData>
    <number_of_ext_data_entries>1</number_of_ext_data_entries>
    <Loop_ext_data_entries>
      <ext_data_entry>
        <ID1>3</ID1>
        <ID2>1</ID2>
      </ext_data_entry>
    </Loop_ext_data_entries>
    <Loop_padding_word />
    <Loop_data_block>
      <data_block>
        <Disc_Info>
          <disc_type>5</disc_type>
          <is_4K_content_exist>false</is_4K_content_exist>
          <HDR_content_exist_flags>0</HDR_content_exist_flags>
        </Disc_Info>
      </data_block>
    </Loop_data_block>
  </ExtensionData>
  <Loop_padding_word_3 />
</IndexTableFile>
""".strip()

    return xml_template.strip()

def maked_movieobject(id_1, id_2):
    xml_template = f"""
<?xml version="1.0" encoding="UTF-8"?>
<MovieObjectFile Version="0099" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="MovieObject.xsd">
  <type_indicator>MOBJ</type_indicator>
  <version_number>0300</version_number>
  <MovieObjects>
    <number_of_mobjs>3</number_of_mobjs>
    <Loop_MovieObject>
      <MovieObject>
        <TerminalInfo>
          <resume_intention_flag>true</resume_intention_flag>
          <menu_call_mask>true</menu_call_mask>
          <title_search_mask>true</title_search_mask>
        </TerminalInfo>
        <number_of_navigation_commands>5</number_of_navigation_commands>
        <Loop_navigation_command>
          <navigation_command>504000010000000000000000</navigation_command>
          <navigation_command>504000010000000200000001</navigation_command>
          <navigation_command>50400001000000030000FFFF</navigation_command>
          <navigation_command>504000010000000400000000</navigation_command>
          <navigation_command>218100000000000000000000</navigation_command>
        </Loop_navigation_command>
      </MovieObject>
      <MovieObject>
        <TerminalInfo>
          <resume_intention_flag>true</resume_intention_flag>
          <menu_call_mask>true</menu_call_mask>
          <title_search_mask>true</title_search_mask>
        </TerminalInfo>
        <number_of_navigation_commands>9</number_of_navigation_commands>
        <Loop_navigation_command>
          <navigation_command>500000010000000A00000003</navigation_command>
          <navigation_command>50400001000000030000FFFF</navigation_command>
          <navigation_command>484003000000000A0000FFFF</navigation_command>
          <navigation_command>220000000000000A00000000</navigation_command>
          <navigation_command>500000010000000A00000004</navigation_command>
          <navigation_command>504000010000000400000000</navigation_command>
          <navigation_command>484003000000000A00000000</navigation_command>
          <navigation_command>210100000000000A00000000</navigation_command>
          <navigation_command>218100000000000100000000</navigation_command>
        </Loop_navigation_command>
      </MovieObject>
      <MovieObject>
        <TerminalInfo>
          <resume_intention_flag>true</resume_intention_flag>
          <menu_call_mask>true</menu_call_mask>
          <title_search_mask>true</title_search_mask>
        </TerminalInfo>
        <number_of_navigation_commands>6</number_of_navigation_commands>
        <Loop_navigation_command>
          <navigation_command>500000010000000A00000000</navigation_command>
          <navigation_command>504000010000000000000000</navigation_command>
          <navigation_command>51C00001{id_1}C{id_2}00000000</navigation_command>
          <navigation_command>504000010000000000000000</navigation_command>
          <navigation_command>42820000000000000000000A</navigation_command>
          <navigation_command>000200000000000000000000</navigation_command>
        </Loop_navigation_command>
      </MovieObject>
    </Loop_MovieObject>
  </MovieObjects>
  <Loop_padding_word_1 />
  <Loop_padding_word_2 />
</MovieObjectFile>
""".strip()

    return xml_template.strip()

def maked_projectdefinition(hypermux_final, fu, mp, all_group_results=None):
    xml_dir = os.path.join(mp, "Output", "MUX", "BDROM")
    DBIntermediate = r"Output\MUX\BDROM\DBIntermediate"
    BDMV = r"Output\MUX\BDROM\DB\BDMV"
    
    # Generate CLIP IDs based on number of groups
    if all_group_results is None:
        all_group_results = []
    num_groups = len(all_group_results)
    clip_ids = [88888 + i for i in range(num_groups + 1)]  # +1 for main group
    
    # Generate M2TS_List and CLPI_List
    m2ts_list = "\n".join([f'        <mstns:CLIP_id>{clip_id}</mstns:CLIP_id>' for clip_id in clip_ids])
    clpi_list = "\n".join([f'        <mstns:CLIP_id>{clip_id}</mstns:CLIP_id>' for clip_id in clip_ids])

    xml_template = f"""
<?xml version="1.0" encoding="UTF-8"?>
<mstns:ProjectDefinition Version="0099" xmlns:mstns="http://tempuri.org/ProjectDefinition.xsd" xmlns:msdata="urn:schemas-microsoft-com:xml-msdata" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://tempuri.org/ProjectDefinition.xsd ProjectDefinition.xsd">
  <mstns:Information>
    <mstns:ProjectName />
    <mstns:Author />
    <mstns:Manufacturer />
    <mstns:DriveType>BD66/100_TR_122</mstns:DriveType>
  </mstns:Information>
  <mstns:XML_List>
    <mstns:IndexTableFile>{xml_dir}{fu}IndexTable.xml</mstns:IndexTableFile>
    <mstns:MovieObjectFile>{xml_dir}{fu}MovieObject.xml</mstns:MovieObjectFile>
    <mstns:MoviePlayListFile>{xml_dir}{fu}MoviePlayList.xml</mstns:MoviePlayListFile>
    <mstns:CLIPDescriptorFile>{xml_dir}{fu}CLIPDescriptor.xml</mstns:CLIPDescriptorFile>
    <mstns:FSDescriptorFile>{xml_dir}{fu}FSDescriptor.xml</mstns:FSDescriptorFile>
  </mstns:XML_List>
  <mstns:Transaction>
    <mstns:TS_process mstns:hypermux="{hypermux_final}">
      <mstns:M2TS_List mstns:All_M2TS="false">
{m2ts_list}
      </mstns:M2TS_List>
      <mstns:TP_extra_header>
        <mstns:copy_permission_indicator>3</mstns:copy_permission_indicator>
      </mstns:TP_extra_header>
    </mstns:TS_process>
    <mstns:DB_Allocate_process>
      <mstns:Execute_process>true</mstns:Execute_process>
      <mstns:Execute_Allocate>true</mstns:Execute_Allocate>
      <mstns:IndexTable_process>true</mstns:IndexTable_process>
      <mstns:MovieObject_process>true</mstns:MovieObject_process>
      <mstns:MoviePlayList_List mstns:All_PlayLists="false">
        <mstns:Playlist_id>00000</mstns:Playlist_id>
      </mstns:MoviePlayList_List>
      <mstns:CLPI_List mstns:All_CLPI="false">
{clpi_list}
      </mstns:CLPI_List>
      <mstns:DB_dirs>
        <mstns:DB_Intermediatefile_dir>{mp}{fu}{DBIntermediate}{fu}</mstns:DB_Intermediatefile_dir>
        <mstns:DB_output_dir>{mp}{fu}{BDMV}{fu}</mstns:DB_output_dir>
      </mstns:DB_dirs>
    </mstns:DB_Allocate_process>
    <mstns:FS_process>true</mstns:FS_process>
  </mstns:Transaction>
</mstns:ProjectDefinition>
""".strip()

    return xml_template.strip()
