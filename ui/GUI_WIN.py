from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QPushButton, QVBoxLayout,
    QFileDialog, QTableWidget, QTableWidgetItem, QLabel,
    QComboBox, QTextEdit, QHBoxLayout, QLineEdit, QMenu, QDialog, QCheckBox, QMessageBox, QListWidget, QAbstractItemView
)
from PyQt6.QtCore import Qt, QSettings, QProcess, QTimer, QStandardPaths, QCoreApplication, QEvent, QByteArray
from PyQt6.QtGui import QIntValidator, QStandardItemModel, QStandardItem, QIcon
from pathlib import Path
from datetime import datetime
import os
import sys
import pycountry
import subprocess
import re

def build_lang_list():
    lang_list = []

    lang_list.append(("und (Undetermined)", "und"))

    lang_list.append(("———— Common ————", None))

    common_langs = ["eng", "zho", "jpn", "nld", "kor", "fra", "fin", "ita", "nor", "deu", "spa", "swe", "rus"]
    for code in common_langs:
        lang = pycountry.languages.get(alpha_3=code)
        if lang:
            lang_list.append((f"{lang.alpha_3} ({lang.name})", lang.alpha_3))

    lang_list.append(("———— All ————", None))

    for lang in pycountry.languages:
        if hasattr(lang, "alpha_3"):
            lang_list.append((f"{lang.alpha_3} ({lang.name})", lang.alpha_3))

    return lang_list

def get_base_dir() -> Path:
    return Path(sys.executable).parent

def _geom_settings() -> QSettings:
    return QSettings("Setup", "WindowGeometry")

def find_run_tool_bat() -> Path | None:
    candidates = [
        Path(sys.executable).resolve().parent / "Run_Tool.bat",
        Path(sys.argv[0]).resolve().parent / "Run_Tool.bat",
        Path(__file__).resolve().parent / "Run_Tool.bat",
        Path.cwd() / "Run_Tool.bat",
    ]
    for p in candidates:
        try:
            if p.exists():
                return p
        except Exception:
            continue
    return None

def has_window_geometry(name: str) -> bool:
    s = _geom_settings()
    return s.contains(f"{name}/geometry")

def restore_window_geometry(widget, name: str) -> bool:
    s = _geom_settings()
    geo = s.value(f"{name}/geometry", None)
    if isinstance(geo, QByteArray):
        return widget.restoreGeometry(geo)
    elif isinstance(geo, (bytes, bytearray)):
        return widget.restoreGeometry(QByteArray(geo))
    return False

def save_window_geometry(widget, name: str):
    s = _geom_settings()
    s.setValue(f"{name}/geometry", widget.saveGeometry())

LANG_CODES = build_lang_list()

SCT_TO_CODEC: dict[str, str] = {
    "1B": "MPEG-4 AVC",
    "24": "HEVC",
    "80": "LPCM",
    "81": "Dolby Digital(AC3)",
    "82": "DTS",
    "83": "Dolby Lossless",
    "84": "Dolby Digital Plus",
    "85": "DTS-HD HRA",
    "86": "DTS-HD",
}

CODEC_TO_CLI_TYPE: dict[str, str] = {
    "MPEG-4 AVC": "MPEG-4 AVC",
    "HEVC": "HEVC",
    "LPCM": "LPCM(WAV)",
    "Dolby Digital(AC3)": "Dolby Digital(AC3)",
    "DTS": "DTS",
    "Dolby Lossless": "Dolby Lossless",
    "Dolby Digital Plus": "Dolby Digital Plus",
    "DTS-HD HRA": "DTS-HD",
    "DTS-HD": "DTS-HD",
}

EXT_TO_CODEC: dict[str, str] = {
    ".avc": "MPEG-4 AVC",
    ".bsf": "MPEG-4 AVC",
    ".264": "MPEG-4 AVC",
    ".h264": "MPEG-4 AVC",
    ".hevc": "HEVC",
    ".265": "HEVC",
    ".h265": "HEVC",
    ".wav": "LPCM",
    ".pcm": "LPCM",
    ".w64": "LPCM",
    ".ac3": "Dolby Digital(AC3)",
    ".mlp": "Dolby Lossless",
    ".dts": "DTS",
    ".cpt": "DTS",
    ".ec3": "Dolby Digital Plus",
    ".eb3": "Dolby Digital Plus",
    ".cptl": "DTS-HD",
    ".dtshd": "DTS-HD",
}

def parse_ves_sct(ves_path: Path) -> str | None:
    try:
        content = ves_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None
    m = re.search(r"XML\.stream_coding_type=([A-Za-z0-9]+)", content)
    return m.group(1) if m else None

def is_dolby_vision_el_from_ves(ves_path: Path) -> bool:
    try:
        content = ves_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return False
    dm = re.search(r"HEVC_dolby_meta=(\d+)", content)
    if not dm:
        return False
    try:
        return int(dm.group(1)) > 0
    except Exception:
        return False

def get_codec_from_ves(ves_path: Path) -> str:
    sct = parse_ves_sct(ves_path)
    if not sct:
        return ""
    return SCT_TO_CODEC.get(sct.upper(), "")

def guess_filetype_from_codec(codec: str) -> str:
    if codec in ("MPEG-4 AVC", "HEVC"):
        return "Video VES File"
    if codec:
        return "Audio VES File"
    return "Audio VES File"

def find_muigenerator_cli() -> Path | None:
    candidates = [
        Path(__file__).resolve().parent / "MUI Generator" / "MUIGenerator_CLI.exe",
        get_base_dir() / "MUI Generator" / "MUIGenerator_CLI.exe",
    ]
    for p in candidates:
        if p.exists():
            return p
    return None

def ensure_ves_for_input(input_path: Path, codec: str, parent=None) -> Path:
    if input_path.suffix.lower() == ".ves":
        return input_path
    target = input_path.with_name(input_path.name + ".ves")
    if target.exists():
        choice = QMessageBox.question(
            parent,
            "Replace .ves?",
            f"{target.name} already exists.\nDo you want to replace it?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if choice == QMessageBox.StandardButton.No:
            return target

    cli = find_muigenerator_cli()
    if not cli:
        raise FileNotFoundError(
            "MUIGenerator_CLI.exe Not found.\n"
            "MUI Generator/MUIGenerator_CLI.exe Please check."
        )

    cli_type = CODEC_TO_CLI_TYPE.get(codec, "")
    if not cli_type:
        raise ValueError(f"Unsupported codec type: {codec}")

    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    result = subprocess.run(
        [str(cli), str(input_path), str(target), "--type", cli_type, "--force"],
        capture_output=True,
        text=True,
        creationflags=creationflags,
    )
    if result.returncode != 0:
        msg = (result.stdout or "") + "\n" + (result.stderr or "")
        raise RuntimeError(msg.strip() or f"MUIGenerator_CLI failed: {result.returncode}")

    return target

class Project:
    def __init__(self):
        self.video: Path | None = None
        self.dolby: Path | None = None
        self.chapter: Path | None = None
        self.audios: list[tuple[Path, str]] = []
        self.subs: list[tuple[Path, str, str, str]] = []
        self.codecs: dict[Path, str] = {}
        self.mux_output: Path | None = None
        self.use_hypermux: bool = False
        self.use_muxserver: bool = False
        self.muxserver_exe: str = ""
        self.muxserver_port: str = ""

    def save_settings(self):
        s = QSettings("Setup", "More_Options")
        s.setValue("use_hypermux", self.use_hypermux)
        s.setValue("use_muxserver", self.use_muxserver)
        s.setValue("muxserver_exe", str(self.muxserver_exe) if self.muxserver_exe else "")
        s.setValue("muxserver_port", self.muxserver_port if self.muxserver_port else "")

    def load_settings(self):
        s = QSettings("Setup", "More_Options")
        self.use_hypermux = s.value("use_hypermux", False, bool)
        self.use_muxserver = s.value("use_muxserver", False, bool)
        exe = s.value("muxserver_exe", "", str)
        self.muxserver_exe = Path(exe) if exe else None
        port = s.value("muxserver_port", "", str)
        self.muxserver_port = int(port) if port else None

    def validate(self, parent=None) -> bool:
        if not self.video or not self.audios or not self.subs:
            if parent:
                QMessageBox.information(parent, "INFO", "A Video, Audio, Subtitle is required")
            return False

        if not self.mux_output:
            if parent:
                QMessageBox.information(parent, "INFO", "Please specify the output mux path")
            return False

        if not self.use_muxserver:
            if parent:
                QMessageBox.information(parent, "INFO", "Must Enable -muxserver")
            return False

        if self.use_muxserver:
            if not self.muxserver_exe or not str(self.muxserver_exe).strip():
                if parent:
                    QMessageBox.information(parent, "INFO", "Must Enable -muxserver exe")
                return False
            if not self.muxserver_port or not str(self.muxserver_port).strip():
                if parent:
                    QMessageBox.information(parent, "INFO", "Must Enable -muxserver port")
                return False

        return True

    def build_cmd(self, file_table=None) -> str:
        parts = []

        if self.chapter:
            parts += ["-t", str(self.chapter)]

        if self.video:
            parts += ["-f", str(self.video)]

        if self.dolby:
            parts += ["-fdv", str(self.dolby)]

        if file_table:
            for row in range(file_table.rowCount()):
                fname_item = file_table.item(row, 0)
                path_item = file_table.item(row, 4)
                if not fname_item or not path_item:
                    continue
                path = path_item.text()
                meta = fname_item.data(Qt.ItemDataRole.UserRole)
                filetype = meta.get("filetype", "") if isinstance(meta, dict) else meta

                if filetype == "Audio VES File":
                    combo = file_table.cellWidget(row, 2)
                    lang = combo.currentData() if combo else "eng"
                    parts += ["-a", path, "-alang", lang]

                elif filetype == "Subtitle PES File":
                    combo = file_table.cellWidget(row, 2)
                    lang = combo.currentData() if combo else "eng"

                    widget = file_table.cellWidget(row, 3)
                    if widget:
                        combo_time = widget.findChild(QComboBox)
                        line_edit = widget.findChild(QLineEdit)
                        if combo_time.currentText() == "Auto":
                            start_time = "auto"
                        else:
                            start_time = line_edit.text().strip()
                    else:
                        start_time = "00:00:00:00"

                    if start_time != "auto":
                        parts += ["-s", path, "-slang", lang, "-sin", start_time]
                    else:
                        parts += ["-s", path, "-slang", lang]

        if self.mux_output:
            parts += ["-mux", str(self.mux_output)]

        if self.use_hypermux:
            parts.append("-hypermux")

        if self.use_muxserver and self.muxserver_exe and self.muxserver_port:
            parts += ["-muxserver", "exe", f"\"{self.muxserver_exe}\"", "port", str(self.muxserver_port)]

        return " ".join(parts)

class TaskWindow(QWidget):
    def __init__(self, project: Project, file_table=None):
        super().__init__()
        self.project = project
        self.file_table = file_table
        self.setWindowTitle("Code Preview")
        self.resize(900, 100)

        self.setWindowFlags(
            Qt.WindowType.Tool |
            Qt.WindowType.WindowStaysOnTopHint
        )

        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
        self.setWindowOpacity(0.85)
        layout = QVBoxLayout()
        self.cmd_view = QTextEdit()
        self.cmd_view.setReadOnly(True)
        layout.addWidget(QLabel("CMD:"))
        layout.addWidget(self.cmd_view)
        self.setLayout(layout)
        restore_window_geometry(self, "TaskWindow")
        self.refresh()

    def refresh(self):
        cmd = self.project.build_cmd(self.file_table)
        self.cmd_view.setPlainText(cmd)

    def closeEvent(self, event):
        save_window_geometry(self, "TaskWindow")
        super().closeEvent(event)

class OptionsWindow(QDialog):
    def __init__(self, project: Project, task_win: TaskWindow):
        super().__init__()
        self.project = project
        self.task_win = task_win
        self.setWindowTitle("MuxServer Settings")
        self.setWindowIcon(QIcon("C:\\build\\ICO.ico"))
        self.resize(480, 200)

        layout = QVBoxLayout()

        self.cb_hypermux  = QCheckBox("-hypermux")
        self.cb_hypermux.setChecked(self.project.use_hypermux)
        self.cb_hypermux.stateChanged.connect(self.toggle_hypermux)
        layout.addWidget(self.cb_hypermux)

        self.cb_muxserver = QCheckBox("-muxserver")
        self.cb_muxserver.setChecked(self.project.use_muxserver)
        self.cb_muxserver.stateChanged.connect(self.toggle_muxserver)
        layout.addWidget(self.cb_muxserver)

        exe_layout = QHBoxLayout()
        self.le_exe = QLineEdit(str(self.project.muxserver_exe) if self.project.muxserver_exe else "")
        self.le_exe.setPlaceholderText("Specify exe Path")
        btn_exe = QPushButton("Path")
        btn_exe.clicked.connect(self.choose_exe)
        exe_layout.addWidget(QLabel("exe:"))
        exe_layout.addWidget(self.le_exe)
        exe_layout.addWidget(btn_exe)
        layout.addLayout(exe_layout)

        port_layout = QHBoxLayout()
        self.le_port = QLineEdit(str(self.project.muxserver_port) if self.project.muxserver_port else "")
        self.le_port.setPlaceholderText("Port Number")
        self.le_port.setValidator(QIntValidator(1, 2147483647, self))
        port_layout.addWidget(QLabel("port:"))
        port_layout.addWidget(self.le_port)
        layout.addLayout(port_layout)

        self.set_muxserver_controls_enabled(self.cb_muxserver.isChecked())

        self.le_exe.textChanged.connect(self.update_muxserver)
        self.le_port.textChanged.connect(self.update_muxserver)

        self.setLayout(layout)

    def toggle_hypermux(self, state):
        self.project.use_hypermux = self.cb_hypermux.isChecked()
        self.task_win.refresh()

    def toggle_muxserver(self, state):
        enabled = self.cb_muxserver.isChecked()
        self.project.use_muxserver = enabled
        self.set_muxserver_controls_enabled(enabled)
        self.task_win.refresh()

    def set_muxserver_controls_enabled(self, enabled: bool):
        self.le_exe.setEnabled(enabled)
        self.le_port.setEnabled(enabled)

    def choose_exe(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select UHDMuxRemotingServer.exe File", filter="UHDMuxRemotingServer.exe (*UHDMuxRemotingServer.exe);")
        if path:
            self.le_exe.setText(path)
            self.update_muxserver()

    def update_muxserver(self):
        self.project.muxserver_exe = self.le_exe.text().strip()
        self.project.muxserver_port = self.le_port.text().strip()
        self.task_win.refresh()

class JobQueueWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Job Queue")
        self.resize(700, 400)

        layout = QVBoxLayout(self)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        btn_layout = QHBoxLayout()
        self.btn_process = QPushButton("Process")
        self.btn_close = QPushButton("Cancel")

        btn_layout.addWidget(self.btn_process)
        btn_layout.addWidget(self.btn_close)
        layout.addLayout(btn_layout)

        self.btn_close.clicked.connect(self.close)
        self.btn_process.clicked.connect(self.process_selected)

        self.load_queue_files()

    def load_queue_files(self):
        base_dir = Path(__file__).resolve().parent
        files = sorted(base_dir.glob("queue_*.txt"))

        for f in files:
            self.list_widget.addItem(f.name)

    def process_selected(self):
        item = self.list_widget.currentItem()
        if not item:
            QMessageBox.warning(self, "Tip", "Please select a job files")
            return

        file_name = item.text()
        base_dir = Path(__file__).resolve().parent
        job_file = base_dir / file_name

        try:
            with open(job_file, "r", encoding="utf-8") as f:
                cmd = f.read().strip()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        self.parent().run_job_command(cmd)

        self.close()

class MainWindow(QMainWindow):
    def __init__(self, project: Project, task_win: TaskWindow):
        super().__init__()
        self.setWindowTitle("tsSCB GUI")
        self.resize(900, 600)
        self.project = project
        self.setWindowIcon(QIcon("C:\\build\\ICO.ico"))
        self.task_win = task_win
        self.setAcceptDrops(True)
        self._muigen_warned = False
        self._mlp_warned = False

        central = QWidget()
        layout = QVBoxLayout()
        top_layout = QHBoxLayout()

        about_layout = QHBoxLayout()
        self.about_btn = QPushButton("About")
        self.about_btn.setFixedSize(60, 30)
        self.about_btn.clicked.connect(self.show_about)
        top_layout.addWidget(self.about_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        job_queue = QHBoxLayout()
        self.queue_btn = QPushButton("Queue")
        self.queue_btn.setFixedSize(60, 30)
        self.queue_btn.clicked.connect(self.show_job)
        top_layout.addWidget(self.queue_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        top_layout.addStretch()
        layout.addLayout(top_layout)

        self.file_table = QTableWidget(0, 5)
        self.file_table.setHorizontalHeaderLabels(["File Name", "Codec", "Lang", "Start Time", "File Path"])
        self.file_table.setAcceptDrops(True)
        self.file_table.viewport().setAcceptDrops(True)
        self.file_table.setDragDropMode(QAbstractItemView.DragDropMode.DropOnly)
        self.file_table.setDefaultDropAction(Qt.DropAction.CopyAction)
        self.file_table.installEventFilter(self)
        self.file_table.viewport().installEventFilter(self)
        layout.addWidget(QLabel("File List:"))
        layout.addWidget(self.file_table)
        btn_open = QPushButton("Open File")
        menu = QMenu()
        menu.addAction("Video VES File").triggered.connect(lambda: self.open_files("Video VES File"))
        menu.addAction("Dolby Vision Enhancement Layer Video VES File").triggered.connect(lambda: self.open_files("Dolby Vision Enhancement Layer Video VES File"))
        menu.addAction("Audio VES File").triggered.connect(lambda: self.open_files("Audio VES File"))
        menu.addAction("Subtitle PES File").triggered.connect(lambda: self.open_files("Subtitle PES File"))
        menu.addAction("Chapter CSV File").triggered.connect(lambda: self.open_files("Chapter CSV File"))
        btn_open.setMenu(menu)

        btn_up = QPushButton("Up")
        btn_up.clicked.connect(self.move_up)
        btn_down = QPushButton("Down")
        btn_down.clicked.connect(self.move_down)
        btn_remove = QPushButton("Remove...")
        remove_menu = QMenu()
        remove_menu.addAction("Remove", self.remove_selected)
        remove_menu.addAction("All Remove", self.remove_all_files)
        btn_remove.setMenu(remove_menu)
        btn_save = QPushButton("Disc Root Path")
        btn_save.clicked.connect(self.choose_mux)
        btn_more = QPushButton("Options")
        btn_more.clicked.connect(self.show_options)
        self.btu_start_mux = QPushButton("Mux...")
        job_queue = QMenu()
        job_queue.addAction("Process", self.start_muxing)
        job_queue.addAction("Add To Queue", self.job_queue)
        self.btu_start_mux.setMenu(job_queue)
        
        for btn in [btn_open, btn_up, btn_down, btn_remove, btn_save, btn_more, self.btu_start_mux]:
            layout.addWidget(btn)

        central.setLayout(layout)
        self.setCentralWidget(central)

        self.task_win.file_table = self.file_table
        restore_window_geometry(self, "MainWindow")

    def eventFilter(self, obj, event):
        if obj in (self.file_table, self.file_table.viewport()):
            if event.type() in (QEvent.Type.DragEnter, QEvent.Type.DragMove):
                if event.mimeData().hasUrls():
                    event.acceptProposedAction()
                    return True
            elif event.type() == QEvent.Type.Drop:
                if event.mimeData().hasUrls():
                    paths: list[Path] = []
                    for url in event.mimeData().urls():
                        local = url.toLocalFile()
                        if local:
                            paths.append(Path(local))
                    if paths:
                        self.import_dropped_paths(paths)
                    event.acceptProposedAction()
                    return True
        return super().eventFilter(obj, event)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if not event.mimeData().hasUrls():
            event.ignore()
            return
        paths = []
        for url in event.mimeData().urls():
            local = url.toLocalFile()
            if local:
                paths.append(Path(local))
        if paths:
            self.import_dropped_paths(paths)
        event.acceptProposedAction()

    def import_dropped_paths(self, paths: list[Path]):
        expanded: list[Path] = []
        for p in paths:
            if p.is_dir():
                expanded.extend([x for x in p.rglob("*") if x.is_file()])
            else:
                expanded.append(p)

        cli_missing = find_muigenerator_cli() is None
        if cli_missing:
            need = [
                x for x in expanded
                if x.suffix.lower() in EXT_TO_CODEC and not x.with_suffix(".ves").exists()
            ]
            if need and not self._muigen_warned:
                preview = "\n".join(str(x) for x in need[:8])
                more = "" if len(need) <= 8 else f"\n... (+{len(need) - 8})"
                QMessageBox.warning(
                    self,
                    "Missing MUI Generator",
                    "MUI Generator/MUIGenerator_CLI.exe\n"
                    f"{preview}{more}",
                )
                self._muigen_warned = True

        for p in expanded:
            self.import_one_path(p)

        self.refresh_all()

    def import_one_path(self, path: Path):
        try:
            path = path.resolve()
        except Exception:
            pass
        suffix = path.suffix.lower()
        forced_codec = ""

        if suffix == ".mlp":
            alt = path.with_suffix(".ac3")
            if not alt.exists():
                if not self._mlp_warned:
                    QMessageBox.warning(
                        self,
                        "Missing .ac3",
                        f"Requires paired substream .ac3 file with same base name：\n{alt}",
                    )
                    self._mlp_warned = True
                return
            forced_codec = "Dolby Lossless"
            path = alt
            suffix = path.suffix.lower()

        if suffix == ".ves":
            codec = get_codec_from_ves(path)
            if codec:
                self.project.codecs[path] = codec
                if codec == "HEVC" and is_dolby_vision_el_from_ves(path):
                    filetype = "Dolby Vision Enhancement Layer Video VES File"
                else:
                    filetype = guess_filetype_from_codec(codec)
            else:
                filetype = "Audio VES File"

            if filetype == "Dolby Vision Enhancement Layer Video VES File":
                self.project.dolby = path
            elif filetype == "Video VES File":
                self.project.video = path
            else:
                self.project.audios.append((path, "eng"))
            return

        if suffix == ".pes":
            self.project.subs.append((path, "eng", "Auto", "00:00:00:00"))
            return

        if suffix == ".csv":
            if self.project.chapter == path:
                return
            self.project.chapter = path
            return

        codec = forced_codec or EXT_TO_CODEC.get(suffix, "")
        if not codec:
            return

        if find_muigenerator_cli() is None and not path.with_suffix(".ves").exists():
            if not self._muigen_warned:
                QMessageBox.warning(
                    self,
                    "Missing MUI Generator",
                    "MUI Generator/MUIGenerator_CLI.exe Please check.",
                )
                self._muigen_warned = True
            return

        try:
            ves_path = ensure_ves_for_input(path, codec, parent=self)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        ves_codec = get_codec_from_ves(ves_path) or codec
        if ves_codec:
            self.project.codecs[ves_path] = ves_codec

        if ves_codec == "HEVC" and is_dolby_vision_el_from_ves(ves_path):
            filetype = "Dolby Vision Enhancement Layer Video VES File"
        else:
            filetype = guess_filetype_from_codec(ves_codec)

        if filetype == "Dolby Vision Enhancement Layer Video VES File":
            self.project.dolby = ves_path
        elif filetype == "Video VES File":
            self.project.video = ves_path
        else:
            self.project.audios.append((ves_path, "eng"))

    def open_files(self, filetype):
        filters = {
            "Video VES File": "Video VES File (*.ves)",
            "Dolby Vision Enhancement Layer Video VES File": "Dolby Vision Enhancement Layer Video VES File (*.ves)",
            "Audio VES File": "Audio VES File (*.ves)",
            "Subtitle PES File": "Subtitle PES File (*.pes)",
            "Chapter CSV File": "Chapter CSV File(*.csv)"
        }

        paths, _ = QFileDialog.getOpenFileNames(
            self, f"Select {filetype}",
            filter=filters[filetype]
        )
        if not paths:
            return

        for path in paths:
            path = Path(path)
            if filetype == "Video VES File":
                codec = get_codec_from_ves(path)
                if codec:
                    self.project.codecs[path] = codec
                if codec == "HEVC" and is_dolby_vision_el_from_ves(path):
                    self.project.dolby = path
                else:
                    self.project.video = path
            elif filetype == "Dolby Vision Enhancement Layer Video VES File":
                self.project.dolby = path
                codec = get_codec_from_ves(path)
                if codec:
                    self.project.codecs[path] = codec
            elif filetype == "Audio VES File":
                self.project.audios.append((path, "eng"))
                codec = get_codec_from_ves(path)
                if codec:
                    self.project.codecs[path] = codec
            elif filetype == "Subtitle PES File":
                self.project.subs.append((path, "eng", "Auto", "00:00:00:00"))
            elif filetype == "Chapter CSV File":
                self.project.chapter = path

        self.refresh_all()

    def show_options(self):
        self.options_win = OptionsWindow(self.project, self.task_win)
        self.options_win.exec()

    def refresh_all(self):
        for row in range(self.file_table.rowCount()):
            fname_item = self.file_table.item(row, 0)
            if not fname_item:
                continue
            meta = fname_item.data(Qt.ItemDataRole.UserRole)
            if not isinstance(meta, dict):
                continue
            kind = meta.get("kind", "")
            idx = meta.get("index", None)

            if kind == "audio" and isinstance(idx, int) and 0 <= idx < len(self.project.audios):
                combo = self.file_table.cellWidget(row, 2)
                if combo:
                    lang = combo.currentData()
                    p, _ = self.project.audios[idx]
                    self.project.audios[idx] = (p, lang)

            elif kind == "sub" and isinstance(idx, int) and 0 <= idx < len(self.project.subs):
                combo = self.file_table.cellWidget(row, 2)
                if combo:
                    lang = combo.currentData()
                    entry = self.project.subs[idx]
                    p = entry[0]
                    mode = entry[2] if len(entry) > 2 else "Auto"
                    start = entry[3] if len(entry) > 3 else "00:00:00:00"
                    widget = self.file_table.cellWidget(row, 3)
                    if widget:
                        combo_time = widget.findChild(QComboBox)
                        line_edit = widget.findChild(QLineEdit)
                        if combo_time:
                            mode = combo_time.currentText()
                        if line_edit:
                            start = line_edit.text().strip()
                    self.project.subs[idx] = (p, lang, mode, start)

        self.file_table.setRowCount(0)

        def add_row(meta: dict, codec: str, lang: str, path: Path, sub_mode: str = "Auto", sub_start: str = "00:00:00:00"):
            filetype = meta.get("filetype", "")
            row = self.file_table.rowCount()
            self.file_table.insertRow(row)

            item_name = QTableWidgetItem(path.name)
            item_name.setFlags(item_name.flags() & ~Qt.ItemFlag.ItemIsEditable)
            item_name.setData(Qt.ItemDataRole.UserRole, meta)
            self.file_table.setItem(row, 0, item_name)

            item_codec = QTableWidgetItem(codec or "")
            item_codec.setFlags(item_codec.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.file_table.setItem(row, 1, item_codec)

            if filetype in ["Audio VES File", "Subtitle PES File"]:
                combo = QComboBox()
                for display, code in LANG_CODES:
                    combo.addItem(display, code)
                    if code is None:
                        index = combo.count() - 1
                        model = combo.model()
                        item = model.item(index)
                        if item:
                            item.setFlags(Qt.ItemFlag.NoItemFlags)
            if lang:
                idx = next((i for i, (_, code) in enumerate(LANG_CODES) if code == lang), -1)
                if idx >= 0:
                    combo.setCurrentIndex(idx)

                combo.currentIndexChanged.connect(self.task_win.refresh)
                self.file_table.setCellWidget(row, 2, combo)
            else:
                item_lang = QTableWidgetItem("")
                item_lang.setFlags(item_lang.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.file_table.setItem(row, 2, item_lang)

            if filetype == "Subtitle PES File":
                widget = QWidget()
                hbox = QHBoxLayout()
                hbox.setContentsMargins(0, 0, 0, 0)

                combo_time = QComboBox()
                combo_time.addItems(["Auto", "Custom"])
                combo_time.setCurrentText(sub_mode if sub_mode in ("Auto", "Custom") else "Auto")
                line_edit = QLineEdit(sub_start or "00:00:00:00")
                line_edit.setEnabled(combo_time.currentText() != "Auto")

                def on_time_mode_changed(idx):
                    if combo_time.currentText() == "Auto":
                        line_edit.setEnabled(False)
                    else:
                        line_edit.setEnabled(True)
                    self.task_win.refresh()

                combo_time.currentIndexChanged.connect(on_time_mode_changed)
                line_edit.textChanged.connect(self.task_win.refresh)

                hbox.addWidget(combo_time)
                hbox.addWidget(line_edit)
                widget.setLayout(hbox)
                self.file_table.setCellWidget(row, 3, widget)
            else:
                item_time = QTableWidgetItem("00:00:00:00")
                item_time.setFlags(item_time.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.file_table.setItem(row, 3, item_time)

            item_path = QTableWidgetItem(str(path))
            item_path.setFlags(item_path.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.file_table.setItem(row, 4, item_path)

            self.file_table.resizeColumnsToContents()
            self.file_table.horizontalHeader().setStretchLastSection(True)

        if self.project.video:
            add_row({"kind": "video", "filetype": "Video VES File"}, self.project.codecs.get(self.project.video, ""), "", self.project.video)
        if self.project.dolby:
            add_row({"kind": "dolby", "filetype": "Dolby Vision Enhancement Layer Video VES File"}, self.project.codecs.get(self.project.dolby, ""), "", self.project.dolby)
        for i, (a, lang) in enumerate(self.project.audios):
            add_row({"kind": "audio", "index": i, "filetype": "Audio VES File"}, self.project.codecs.get(a, ""), lang, a)
        for i, entry in enumerate(self.project.subs):
            if len(entry) == 2:
                s, lang = entry
                mode = "Auto"
                start = "00:00:00:00"
            else:
                s, lang, mode, start = entry
            add_row({"kind": "sub", "index": i, "filetype": "Subtitle PES File"}, "PGS", lang, s, mode, start)

        self.task_win.refresh()

    def is_path_used(self, path: Path) -> bool:
        if self.project.video == path or self.project.dolby == path or self.project.chapter == path:
            return True
        for p, _ in self.project.audios:
            if p == path:
                return True
        for entry in self.project.subs:
            if entry[0] == path:
                return True
        return False

    def remove_selected(self):
        row = self.file_table.currentRow()
        if row < 0:
            return
        item = self.file_table.item(row, 0)
        if not item:
            return
        meta = item.data(Qt.ItemDataRole.UserRole)
        if not isinstance(meta, dict):
            return
        kind = meta.get("kind", "")
        idx = meta.get("index", None)
        path = Path(self.file_table.item(row, 4).text())

        if kind == "video" and self.project.video == path:
            self.project.video = None
        elif kind == "dolby" and self.project.dolby == path:
            self.project.dolby = None
        elif kind == "chapter" and self.project.chapter == path:
            self.project.chapter = None
        elif kind == "audio" and isinstance(idx, int) and 0 <= idx < len(self.project.audios):
            self.project.audios.pop(idx)
        elif kind == "sub" and isinstance(idx, int) and 0 <= idx < len(self.project.subs):
            self.project.subs.pop(idx)

        if not self.is_path_used(path):
            self.project.codecs.pop(path, None)
        self.refresh_all()

    def remove_all_files(self):
        self.project.video = None
        self.project.dolby = None
        self.project.chapter = None
        self.project.audios.clear()
        self.project.subs.clear()
        self.project.codecs.clear()

        self.refresh_all()

    def job_queue(self):
        if not self.project.validate(parent=self):
            return

        cmd = self.project.build_cmd(self.file_table)
        if not cmd:
            QMessageBox.warning(self, "Tip", "No cmd generated, unable to add to queue")
            return

        base_dir = Path(__file__).resolve().parent
        # base_dir = Path(sys.executable).parent

        base_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        queue_file = base_dir / f"queue_{timestamp}.txt"

        with open(queue_file, "a", encoding="utf-8") as f:
            f.write(cmd + "\n")

    def move_up(self):
        row = self.file_table.currentRow()
        if row <= 0:
            return

        item = self.file_table.item(row, 0)
        if not item:
            return
        meta = item.data(Qt.ItemDataRole.UserRole)
        if not isinstance(meta, dict):
            return
        kind = meta.get("kind", "")
        idx = meta.get("index", None)

        moved = False
        if kind == "audio" and isinstance(idx, int) and idx > 0:
            self.project.audios[idx - 1], self.project.audios[idx] = self.project.audios[idx], self.project.audios[idx - 1]
            moved = True
        elif kind == "sub" and isinstance(idx, int) and idx > 0:
            self.project.subs[idx - 1], self.project.subs[idx] = self.project.subs[idx], self.project.subs[idx - 1]
            moved = True
        if not moved:
            return

        self.refresh_all()
        self.file_table.selectRow(row - 1)

    def move_down(self):
        row = self.file_table.currentRow()
        if row < 0 or row >= self.file_table.rowCount() - 1:
            return

        item = self.file_table.item(row, 0)
        if not item:
            return
        meta = item.data(Qt.ItemDataRole.UserRole)
        if not isinstance(meta, dict):
            return
        kind = meta.get("kind", "")
        idx = meta.get("index", None)

        moved = False
        if kind == "audio" and isinstance(idx, int) and idx < len(self.project.audios) - 1:
            self.project.audios[idx], self.project.audios[idx + 1] = self.project.audios[idx + 1], self.project.audios[idx]
            moved = True
        elif kind == "sub" and isinstance(idx, int) and idx < len(self.project.subs) - 1:
            self.project.subs[idx], self.project.subs[idx + 1] = self.project.subs[idx + 1], self.project.subs[idx]
            moved = True
        if not moved:
            return

        self.refresh_all()
        self.file_table.selectRow(row + 1)

    def choose_mux(self):
        path = QFileDialog.getExistingDirectory(self, "Browse Folders")
        if not path:
            return
        self.project.mux_output = Path(path)
        self.task_win.refresh()

    def start_muxing(self, parent=None):

        if not self.project.validate(parent=self):
            return

        cmd = self.project.build_cmd(self.file_table)
        if not cmd:
            QMessageBox.warning(self, "Tip", "No cmd generated, unable to start muxing")
            return

        bat_path = find_run_tool_bat()
        if not bat_path:
            QMessageBox.critical(self, "Error", "Not Found File: Run_Tool.bat")
            return
        base_dir = bat_path.parent
        info_path = base_dir / "args.txt"
        self.flag_path = base_dir / "light.flag"

        if not bat_path.exists():
            QMessageBox.critical(self, "Error", f"Not Found File: {bat_path}")
            return

        with open(info_path, "w", encoding="utf-8") as f:
            f.write(cmd)

        if self.flag_path.exists():
            self.flag_path.unlink()

        self.btu_start_mux.setEnabled(False)

        os.startfile(str(bat_path))

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_process)
        self.timer.start(1000)

    def check_process(self):
        if self.flag_path.exists():
            try:
                with open(self.flag_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "Execution Completed" in content:
                        self.timer.stop()
                        self.btu_start_mux.setEnabled(True)
            except Exception:
                pass

    def closeEvent(self, event):
        save_window_geometry(self, "MainWindow")
        save_window_geometry(self.task_win, "TaskWindow")
        self.project.save_settings()
        self.task_win.close()
        super().closeEvent(event)

    def show_about(self):
        QMessageBox.information(
            self,
            "About",
            "tsSCB GUI\n\n"
            "Author: KSSW\n"
            "Version: v1.1"
        )

    def show_job(self):
        dlg = JobQueueWindow(self)
        dlg.exec()

    def run_job_command(self, cmd: str):
        bat_path = find_run_tool_bat()
        if not bat_path:
            QMessageBox.critical(self, "Error", "Not Found File: Run_Tool.bat")
            return
        base_dir = bat_path.parent
        info_path = base_dir / "args.txt"
        self.flag_path = base_dir / "light.flag"

        if not bat_path.exists():
            QMessageBox.critical(self, "Error", f"Not Found File: {bat_path}")
            return

        with open(info_path, "w", encoding="utf-8") as f:
            f.write(cmd)

        if self.flag_path.exists():
            self.flag_path.unlink()

        self.btu_start_mux.setEnabled(False)
        os.startfile(str(bat_path))

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_process)
        self.timer.start(1000)

def main():
    app = QApplication(sys.argv)
    project = Project()
    project.load_settings()
    task_win = TaskWindow(project)
    w = MainWindow(project, task_win)

    if not has_window_geometry("MainWindow"):
        screen = app.primaryScreen().availableGeometry()
        size = w.frameGeometry()
        center_point = screen.center()
        size.moveCenter(center_point)
        w.move(size.topLeft())
    if not has_window_geometry("TaskWindow"):
        task_win.move(1020, 895)

    task_win.show()
    w.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
