tsSCB
=============

# How Use？
# Step 1:
Required for [MuxServerHelper](https://github.com/KSSW/MuxServerHelper/releases)\
Put the MuxServerHelper in the same directory\
Double click Run a Run_Tool.bat

# Step 2:
The cmd window displays:

tsSCB Command Tool\
Command args(Don't add exe):

Enter Command args

# Options:
```bash
  -f         Input Video VES File ( Supported videocodecs: H.264/AVC, H.265/HEVC )
  -fdv       Input Dolby Vision Enhancement Layer VES File ( Supported videocodecs: H.265/HEVC )
  -a         Input Audio VES File ( Supported audiocodecs: AC3 / E-AC3(DD+), Dolby TrueHD, DTS/ DTS-HD, LPCM )
  -alang     Set Audio Language, default=und
  -s         Input Subtitles VES File ( Supported Subtitlecodecs: Presentation Graphic Stream (.sup))
  -sin       Set IN Time Subtitles
  -slang     Set Subtitles Language, default=und
  -preid     Set Audio and Subtitle ID Default Track. Example: 1:1 (a:s)
  -t         Input CSV File ( Chapters Timecode ), default=00:00:00:00
  -intime    Set Video IN Time
  -off       off Video Start TimeCode
  -tc        Specify Video Start TimeCode
  -mux       Output MUX Folder
  -hypermux  HyperMUXing Uses Metadata That References The Original Assets To Create a virtual BDMV volume and image

muxserver options:
-muxserver   Startup MUXRemotingServer. Example: exe Exe Path port Port Number
exe          Exe Path
port         Port Number