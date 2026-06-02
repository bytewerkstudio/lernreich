import json
import calendar as cal
import csv
import ctypes
import math
import os
import random
import sys
import threading
from datetime import date, datetime, timedelta
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

try:
    import pystray
    from PIL import Image, ImageDraw
except ImportError:
    pystray = None
    Image = None
    ImageDraw = None


APP_NAME = "Lernreich"
LEGACY_APP_NAMES = ["Avalon", "Lerndorf", "Studiumsstadt"]
DISPLAY_NAME = "Lernreich"
APP_VERSION = "1.3"
APP_COMPANY = "Bytewerk Studio"
APP_PUBLISHER = "Hijratullah Haqmal"
APP_USER_MODEL_ID = "Lernreich.FocusTimer"
DEFAULT_TARGET_MINUTES = 60
MAX_SESSION_MINUTES = 150
MAX_SESSION_SECONDS = MAX_SESSION_MINUTES * 60
XP_PER_HOUR = 100
XP_RATE_ID = "100_xp_per_hour"
MAX_UPGRADE_LEVEL = 100
BASE_UPGRADE_COST = 300
UPGRADE_COST_STEP = 20
BREAK_SECONDS = 5 * 60
BREAK_BONUS_XP = 5
STREAK_MIN_SECONDS = 10 * 60
STREAK_BONUS_BASE_XP = 10
STREAK_BONUS_STEP_XP = 2
STREAK_BONUS_CAP_XP = 30
MAX_STORED_SESSIONS = 5000

UPGRADE_CATEGORIES = [
    {"key": "houses", "name": "Haeuser", "max": 22},
    {"key": "bridge", "name": "Bruecke", "max": 10},
    {"key": "mill", "name": "Muehle", "max": 12},
    {"key": "fields", "name": "Felder", "max": 16},
    {"key": "castle", "name": "Burg", "max": 14},
    {"key": "mage_tower", "name": "Magierturm", "max": 12},
    {"key": "library", "name": "Bibliothek", "max": 14},
]

MONTH_NAMES = [
    "",
    "Januar",
    "Februar",
    "Maerz",
    "April",
    "Mai",
    "Juni",
    "Juli",
    "August",
    "September",
    "Oktober",
    "November",
    "Dezember",
]
WEEKDAY_NAMES = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

LANGUAGE_LABELS = {"de": "Deutsch", "en": "English"}
LANGUAGE_CODES = {label: code for code, label in LANGUAGE_LABELS.items()}

TEXT = {
    "de": {
        "ready": "Bereit fuer die naechste Lernsession.",
        "subtitle": "Focus Timer",
        "hourglass_title": "Timer",
        "hourglass_desc": "Die Sanduhr zeigt dein Ziel. Lernreich laeuft bis maximal 2,5 Stunden.",
        "start": "Start",
        "running": "Laeuft...",
        "settings": "Einstellungen",
        "study_goal": "Lernziel",
        "subject": "Fach",
        "goal": "Ziel",
        "minutes": "Minuten",
        "popup": "Popup",
        "daily_goal": "Tagesziel",
        "hours_short": "Std",
        "aware_abort": "Bewusst abbrechen",
        "finish_goal": "Ziel beenden",
        "reset_all": "Alles zuruecksetzen",
        "break_after_focus": "Pause nach Fokus",
        "avalon_valley": "Statistik-Zentrale",
        "avalon_tab": "Statistik",
        "calendar": "Kalender",
        "notes_tab": "Notizen",
        "open_notes_folder": "Ordner oeffnen",
        "notes_title": "Lernjournal",
        "notes_hint": "Hier siehst du deine gemerkten Lernziele und Notizen.",
        "notes_empty": "Noch keine gespeicherten Notizen. Schreibe unten eine Notiz und klicke auf Notiz merken.",
        "active_note": "laufend",
        "daily_plan": "Tagesplanung",
        "week_report": "Wochenbericht",
        "reviews": "Wiederholen",
        "focus_checklist": "Fokus-Checkliste",
        "tray_running": "Lernreich laeuft im Hintergrund.",
        "start_ready": "Ich bin startklar.",
        "plan_saved": "Tagesplanung gespeichert.",
        "abort_reason": "Abbruchgrund",
        "abort_note": "Kurzer Grund",
        "upgrade_tree": "Lernanalyse",
        "learned": "Was gelernt?",
        "save_note": "Notiz merken",
        "last_sessions": "Letzte Sessions",
        "language": "Sprache",
        "save": "Speichern",
        "close": "Schliessen",
        "reset_warning": "Moechtest du wirklich alle Lernzeiten und Lernreich loeschen?",
        "language_saved": "Sprache gespeichert. Beim naechsten Start ist alles umgestellt.",
        "export_csv": "Sessions als CSV exportieren",
        "export_empty": "Noch keine Sessions zum Exportieren vorhanden.",
        "export_failed": "Export fehlgeschlagen:",
        "export_done": "{count} Sessions als CSV gespeichert.",
    },
    "en": {
        "ready": "Ready for the next focus session.",
        "subtitle": "Focus Timer",
        "hourglass_title": "Timer",
        "hourglass_desc": "The hourglass shows your target. Lernreich runs up to 2.5 hours.",
        "start": "Start",
        "running": "Running...",
        "settings": "Settings",
        "study_goal": "Goal",
        "subject": "Subject",
        "goal": "Target",
        "minutes": "Minutes",
        "popup": "Popup",
        "daily_goal": "Daily goal",
        "hours_short": "h",
        "aware_abort": "Conscious abort",
        "finish_goal": "Finish goal",
        "reset_all": "Reset everything",
        "break_after_focus": "Break after focus",
        "avalon_valley": "Stats Center",
        "avalon_tab": "Stats",
        "calendar": "Calendar",
        "notes_tab": "Notes",
        "open_notes_folder": "Open folder",
        "notes_title": "Learning journal",
        "notes_hint": "Your saved goals and notes appear here.",
        "notes_empty": "No saved notes yet. Write a note below and click Save note.",
        "active_note": "active",
        "daily_plan": "Daily plan",
        "week_report": "Weekly report",
        "reviews": "Review",
        "focus_checklist": "Focus checklist",
        "tray_running": "Lernreich is running in the background.",
        "start_ready": "I am ready.",
        "plan_saved": "Daily plan saved.",
        "abort_reason": "Abort reason",
        "abort_note": "Short reason",
        "upgrade_tree": "Learning analysis",
        "learned": "What did you learn?",
        "save_note": "Save note",
        "last_sessions": "Recent sessions",
        "language": "Language",
        "save": "Save",
        "close": "Close",
        "reset_warning": "Do you really want to delete all learning time and Lernreich?",
        "language_saved": "Language saved. Everything will switch on the next start.",
        "export_csv": "Export sessions as CSV",
        "export_empty": "No sessions to export yet.",
        "export_failed": "Export failed:",
        "export_done": "{count} sessions saved as CSV.",
    },
}


LIGHT_COLORS = {
    "ink": "#111215",        # Deep obsidian charcoal
    "muted": "#5e616c",      # Sleek muted gray
    "paper": "#fbfbfa",      # Warm, minimalist airy background
    "paper_dark": "#f1f1ed", # Slightly darker warm-gray
    "navy": "#111215",        # Matches ink
    "navy_light": "#1e2025",  # Soft dark gray for hover
    "gold": "#3b52e2",        # Exquisite brand indigo
    "gold_dark": "#2a3db6",   # Darker brand color
    "sage": "#16a34a",
    "brick": "#d97706",
    "clay": "#ea580c",
    "slate": "#4b5563",
    "cream": "#ffffff",
    "line": "#e6e6e2",
    "success": "#16a34a",
    "danger": "#dc2626",
    "shadow": "#eaeae6",
}

DARK_COLORS = {
    "ink": "#fbfbfa",        # Light text
    "muted": "#9ca3af",      # Muted gray text
    "paper": "#090a0c",      # Deep dark obsidian background
    "paper_dark": "#121317", # Slightly lighter dark gray for sidebar
    "navy": "#fbfbfa",        # Light text for primary buttons
    "navy_light": "#e5e7eb",  # Active button bg
    "gold": "#3b52e2",        # Exquisite brand indigo
    "gold_dark": "#5c6fff",   # Lighter brand indigo for dark mode contrast
    "sage": "#22c55e",
    "brick": "#f59e0b",
    "clay": "#f97316",
    "slate": "#9ca3af",
    "cream": "#18191e",       # Dark card color
    "line": "#262930",        # Dark border line
    "success": "#22c55e",
    "danger": "#ef4444",
    "shadow": "#050507",
}

COLORS = dict(LIGHT_COLORS)


REMINDER_MESSAGES = [
    "Fokus-Check: Ist dein naechster Lernschritt noch klar?",
    "Kurzer Blick nach innen: Haltung lockern, Wasser trinken, weiter mit Ruhe.",
    "Deine Statistik waechst. Markiere eine Sache, die du gerade verstanden hast.",
    "Atme einmal tief durch. Dann zurueck zur wichtigsten Aufgabe.",
    "Fokus-Glocke: eine klare Sache festhalten, dann ruhig weiterlernen.",
]

ABORT_REASONS = [
    "Ablenkung",
    "Muedigkeit",
    "Zu schwer",
    "Aufgabe fertig",
    "Falsches Ziel",
    "Notfall / anderer Grund",
]

DEFAULT_SUBJECT = "Allgemein"

FOCUS_CHECKLIST_ITEMS = [
    "Handy weggelegt",
    "Wasser bereit",
    "Aufgabe klar",
    "Ablenkende Tabs geschlossen",
]

REVIEW_OPTIONS = [
    ("Morgen", 1),
    ("In 3 Tagen", 3),
    ("In 7 Tagen", 7),
]


def resource_path(relative_path: str) -> Path:
    base_path = getattr(sys, "_MEIPASS", None)
    if base_path:
        return Path(base_path) / relative_path
    return Path(__file__).resolve().parent / relative_path


def app_data_dir() -> Path:
    base = os.environ.get("APPDATA")
    if base:
        path = Path(base) / APP_NAME
    else:
        path = Path.home() / f".{APP_NAME.lower()}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def app_data_path() -> Path:
    path = app_data_dir()
    return path / "progress.json"


def notes_root_path() -> Path:
    path = app_data_dir() / "Notizen"
    path.mkdir(parents=True, exist_ok=True)
    return path


def notes_day_path(day_key: str | None = None) -> Path:
    day = day_key or date.today().isoformat()
    path = notes_root_path() / day
    path.mkdir(parents=True, exist_ok=True)
    return path


def active_note_path() -> Path:
    return notes_day_path() / "laufende_session.md"


def legacy_app_data_paths() -> list[Path]:
    base = os.environ.get("APPDATA")
    paths = []
    if base:
        for name in LEGACY_APP_NAMES:
            paths.append(Path(base) / name / "progress.json")
        return paths
    for name in LEGACY_APP_NAMES:
        paths.append(Path.home() / f".{name.lower()}" / "progress.json")
    return paths


def load_progress() -> dict:
    path = app_data_path()
    if not path.exists():
        for legacy_path in legacy_app_data_paths():
            if legacy_path.exists():
                path = legacy_path
                break
    if not path.exists():
        return {"total_seconds": 0, "sessions": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"total_seconds": 0, "sessions": []}
    data.setdefault("total_seconds", 0)
    data.setdefault("sessions", [])
    if "total_xp" not in data:
        data["total_xp"] = (int(data.get("total_seconds", 0)) * XP_PER_HOUR) // 3600
        stored_hourly_rate = XP_PER_HOUR
    else:
        stored_hourly_rate = int(data.get("xp_per_hour", 0))
        if not stored_hourly_rate:
            try:
                old_per_minute = int(data.get("xp_rate", 1))
            except (TypeError, ValueError):
                old_per_minute = 0
            if data.get("xp_rate") == XP_RATE_ID:
                stored_hourly_rate = XP_PER_HOUR
            else:
                stored_hourly_rate = max(1, old_per_minute) * 60
    if stored_hourly_rate != XP_PER_HOUR:
        factor = XP_PER_HOUR / max(1, stored_hourly_rate)
        data["total_xp"] = int(round(int(data.get("total_xp", 0)) * factor))
        if "available_xp" in data:
            data["available_xp"] = int(round(int(data.get("available_xp", 0)) * factor))
        if "spent_xp" in data:
            data["spent_xp"] = int(round(int(data.get("spent_xp", 0)) * factor))
        for session in data.get("sessions", []):
            for key in ("xp", "lost_xp"):
                if key in session:
                    session[key] = int(round(int(session.get(key, 0)) * factor))
    data.setdefault("spent_xp", 0)
    data.setdefault("available_xp", max(0, int(data.get("total_xp", 0)) - int(data.get("spent_xp", 0))))
    data["village_level"] = min(MAX_UPGRADE_LEVEL, max(1, int(data.get("village_level", 1))))
    data.setdefault("upgrades", [])
    data.setdefault("break_bonuses", [])
    data.setdefault("streak_bonuses", [])
    data.setdefault("streak_bonus_days", [])
    data.setdefault("current_streak", 0)
    data.setdefault("best_streak", 0)
    data.setdefault("daily_goal_hours", 2.0)
    data.setdefault("daily_plans", {})
    data.setdefault("reviews", [])
    data.setdefault("active_subject", DEFAULT_SUBJECT)
    data.setdefault("language", "de")
    levels = default_category_levels()
    saved_levels = data.get("category_levels")
    if isinstance(saved_levels, dict):
        for category in UPGRADE_CATEGORIES:
            levels[category["key"]] = min(
                int(category["max"]),
                max(0, int(saved_levels.get(category["key"], 0))),
            )
    elif data["village_level"]:
        levels["houses"] = min(int(UPGRADE_CATEGORIES[0]["max"]), data["village_level"])
    data["category_levels"] = levels
    data["xp_per_hour"] = XP_PER_HOUR
    data["xp_rate"] = XP_RATE_ID
    return data


def save_progress(data: dict) -> None:
    path = app_data_path()
    tmp = path.with_suffix(".tmp")
    data["xp_per_hour"] = XP_PER_HOUR
    data["xp_rate"] = XP_RATE_ID
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def format_seconds(seconds: int) -> str:
    seconds = max(0, int(seconds))
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    sec = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{sec:02d}"


def minutes_text(seconds: int) -> str:
    minutes = int(seconds // 60)
    hours = minutes // 60
    mins = minutes % 60
    if hours and mins:
        return f"{hours} h {mins} min"
    if hours:
        return f"{hours} h"
    return f"{mins} min"


def category_names() -> list[str]:
    return [category["name"] for category in UPGRADE_CATEGORIES]


def category_by_name(name: str) -> dict:
    for category in UPGRADE_CATEGORIES:
        if category["name"] == name:
            return category
    return UPGRADE_CATEGORIES[0]


def default_category_levels() -> dict:
    return {category["key"]: 0 for category in UPGRADE_CATEGORIES}


def upgrade_cost_for_level(current_level: int) -> int:
    return BASE_UPGRADE_COST + max(0, int(current_level) - 1) * UPGRADE_COST_STEP


class StudyCityApp:
    def __init__(self) -> None:
        self._set_windows_app_id()
        self.root = tk.Tk()
        self.root.title(DISPLAY_NAME)
        self._apply_window_icon()
        self.root.geometry("960x600")
        self.root.minsize(900, 560)
        self.root.configure(bg=COLORS["paper"])

        self.data = load_progress()
        self.running = False
        self.break_running = False
        self.break_available = False
        self.break_seconds = 0.0
        self.session_seconds = int(self.data.get("active_session_seconds", 0))
        self.session_started_at = self._parse_datetime(self.data.get("active_session_started_at"))
        if self.session_seconds > 0 and self.session_started_at is None:
            self.session_started_at = datetime.now() - timedelta(seconds=self.session_seconds)
        self._last_tick = None
        self._save_checkpoint = 0
        self._reminder_checkpoint = 0
        self._hourglass_phase = 0.0
        self._last_city_minute = -1
        self._active_learned = str(self.data.get("active_learned", ""))
        self._review_popup_shown = False
        self._last_completed_session = None
        self.tray_icon = None
        self.tray_thread = None
        self._quit_requested = False

        saved_target = self.data.get(
            "active_target_minutes",
            self.data.get("target_minutes", DEFAULT_TARGET_MINUTES),
        )
        self.target_minutes = tk.IntVar(
            value=self._clamp_minutes_value(saved_target, DEFAULT_TARGET_MINUTES, 1, MAX_SESSION_MINUTES)
        )
        self.reminder_minutes = tk.IntVar(
            value=self._clamp_minutes_value(self.data.get("reminder_minutes", 15), 15, 1, MAX_SESSION_MINUTES)
        )
        self.daily_goal_hours = tk.DoubleVar(value=float(self.data.get("daily_goal_hours", 2.0)))
        self.upgrade_category = tk.StringVar(value=category_names()[0])
        self.current_view = tk.StringVar(value="stats")
        saved_subject = str(self.data.get("active_subject", DEFAULT_SUBJECT)).strip()
        self.subject_text = tk.StringVar(value=saved_subject or DEFAULT_SUBJECT)
        language = str(self.data.get("language", "de"))
        self.language = tk.StringVar(value=language if language in TEXT else "de")
        self.break_duration_minutes = tk.IntVar(
            value=self._clamp_minutes_value(self.data.get("break_duration_minutes", 5), 5, 5, 15)
        )
        theme_mode = str(self.data.get("theme_mode", "dark"))
        self.theme_mode = tk.StringVar(value=theme_mode if theme_mode in ("light", "dark") else "dark")
        today = date.today()
        self.calendar_year = today.year
        self.calendar_month = today.month
        self.goal_text = tk.StringVar(
            value=str(self.data.get("active_goal") or "Kapitel lesen, Notizen ordnen")
        )
        self.status_text = tk.StringVar(value=self.t("ready"))
        self._target_reached_popup_shown = self.session_seconds >= self._target_seconds()

        self._build_styles()
        self._build_layout()
        self._apply_theme()
        self._restore_active_learning_note()
        self._bind_events()
        self._render_all()
        self._tick()
        self.root.after(550, self._show_start_toast)
        self.root.after(1800, self._show_due_reviews_once)

    @staticmethod
    def _parse_datetime(value) -> datetime | None:
        if not value:
            return None
        try:
            return datetime.fromisoformat(str(value))
        except ValueError:
            return None

    @staticmethod
    def _clamp_minutes_value(value, fallback: int, minimum: int, maximum: int) -> int:
        try:
            minutes = int(float(value))
        except (TypeError, ValueError):
            minutes = fallback
        return max(minimum, min(maximum, minutes))

    @property
    def total_visible_seconds(self) -> int:
        return int(self.data.get("total_seconds", 0) + self.session_seconds)

    @property
    def break_limit_seconds(self) -> int:
        return self.break_duration_minutes.get() * 60

    @property
    def break_bonus_xp(self) -> int:
        return self.break_duration_minutes.get()

    @property
    def total_visible_xp(self) -> int:
        return int(self.data.get("total_xp", 0) + self._xp_for_seconds(self.session_seconds))

    @property
    def saved_available_xp(self) -> int:
        return int(self.data.get("available_xp", 0))

    @property
    def village_level(self) -> int:
        return min(MAX_UPGRADE_LEVEL, max(1, int(self.data.get("village_level", 1))))

    @property
    def category_levels(self) -> dict:
        levels = default_category_levels()
        saved = self.data.get("category_levels", {})
        if isinstance(saved, dict):
            for category in UPGRADE_CATEGORIES:
                levels[category["key"]] = min(
                    int(category["max"]),
                    max(0, int(saved.get(category["key"], 0))),
                )
        return levels

    def _player_level_info(self, total_xp: int) -> tuple[int, int, int]:
        total_xp = max(0, int(total_xp))
        level = int(math.floor((1.0 + math.sqrt(1.0 + 0.08 * total_xp)) / 2.0))
        level = max(1, level)
        xp_for_current_level = 50 * level * (level - 1)
        cost = level * 100
        current_xp_in_level = total_xp - xp_for_current_level
        return level, current_xp_in_level, cost

    def run(self) -> None:
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._setup_tray_icon()
        self.root.mainloop()
        self._stop_tray_icon()

    def t(self, key: str) -> str:
        lang = self.language.get() if hasattr(self, "language") else "de"
        return TEXT.get(lang, TEXT["de"]).get(key, TEXT["de"].get(key, key))

    def _set_windows_app_id(self) -> None:
        if sys.platform != "win32":
            return
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_USER_MODEL_ID)
        except Exception:
            pass

    def _apply_window_icon(self) -> None:
        icon_path = resource_path("assets/lernreich.ico")
        if not icon_path.exists():
            return
        try:
            self.root.iconbitmap(default=str(icon_path))
        except tk.TclError:
            try:
                self.root.iconbitmap(str(icon_path))
            except tk.TclError:
                pass

    def _create_tray_image(self):
        if Image is None or ImageDraw is None:
            return None
        icon_path = resource_path("assets/lernreich.ico")
        if icon_path.exists():
            try:
                return Image.open(icon_path).resize((64, 64))
            except Exception:
                pass
        image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((5, 5, 59, 59), fill=(25, 47, 76, 255), outline=(224, 185, 90, 255), width=3)
        draw.polygon((46, 14, 32, 10, 18, 23, 34, 27), fill=(248, 246, 230, 255))
        draw.polygon((39, 24, 22, 23, 11, 36, 29, 34), fill=(248, 246, 230, 255))
        draw.polygon((34, 27, 43, 42, 30, 53, 25, 34), fill=(232, 238, 224, 255))
        draw.line((16, 50, 47, 13), fill=(92, 55, 35, 255), width=4)
        draw.line((18, 48, 45, 15), fill=(252, 234, 176, 255), width=2)
        draw.polygon((15, 50, 7, 57, 12, 45, 21, 41), fill=(245, 220, 152, 255))
        return image

    def _setup_tray_icon(self) -> None:
        if pystray is None or self.tray_icon is not None:
            return
        image = self._create_tray_image()
        if image is None:
            return
        menu = pystray.Menu(
            pystray.MenuItem("Lernreich oeffnen", lambda _icon, _item: self.root.after(0, self._show_from_tray)),
            pystray.MenuItem("Wirklich beenden", lambda _icon, _item: self.root.after(0, self._quit_from_tray)),
        )
        self.tray_icon = pystray.Icon(APP_NAME, image, "Lernreich laeuft", menu)
        self.tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
        self.tray_thread.start()

    def _stop_tray_icon(self) -> None:
        if self.tray_icon is None:
            return
        try:
            self.tray_icon.stop()
        except Exception:
            pass
        self.tray_icon = None

    def _show_from_tray(self) -> None:
        self.root.deiconify()
        self.root.state("normal")
        self.root.lift()
        self.root.focus_force()
        self.status_text.set("Lernreich ist wieder sichtbar.")

    def _hide_to_tray(self) -> None:
        self._save_current_session()
        if self.tray_icon is None:
            self.root.iconify()
            self.status_text.set(self.t("tray_running"))
            return
        self.root.withdraw()
        self.status_text.set(self.t("tray_running"))
        try:
            self.tray_icon.notify("Lernreich laeuft weiter. Oeffne es ueber das Tray-Menue.", "Lernreich")
        except Exception:
            pass

    def _quit_from_tray(self) -> None:
        self._quit_requested = True
        self._save_current_session()
        self._stop_tray_icon()
        self.root.destroy()

    def _show_start_toast(self) -> None:
        if not self.root.winfo_exists():
            return
        toast = tk.Toplevel(self.root)
        toast.overrideredirect(True)
        toast.attributes("-topmost", True)
        toast.configure(bg=COLORS["navy"])

        width, height = 330, 104
        screen_w = toast.winfo_screenwidth()
        screen_h = toast.winfo_screenheight()
        x = max(12, screen_w - width - 22)
        y = max(12, screen_h - height - 62)
        toast.geometry(f"{width}x{height}+{x}+{y}")

        frame = tk.Frame(toast, bg=COLORS["navy"], padx=16, pady=12)
        frame.pack(fill="both", expand=True)
        tk.Label(
            frame,
            text="Lernreich",
            bg=COLORS["navy"],
            fg="#ffffff",
            font=("Segoe UI", 15, "bold"),
        ).pack(anchor="w")
        tk.Label(
            frame,
            text=f"Heute: {date.today().strftime('%d.%m.%Y')}",
            bg=COLORS["navy"],
            fg="#e7d7aa",
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(3, 0))
        tk.Label(
            frame,
            text=f"{self.t('start_ready')} Lernreich laeuft.",
            bg=COLORS["navy"],
            fg="#ffffff",
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(7, 0))
        toast.after(6500, toast.destroy)

    def _build_styles(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "App.TFrame",
            background=COLORS["paper"],
        )
        style.configure(
            "Panel.TFrame",
            background=COLORS["cream"],
            relief="flat",
            borderwidth=0,
        )
        style.configure(
            "Title.TLabel",
            background=COLORS["paper"],
            foreground=COLORS["ink"],
            font=("Bahnschrift SemiBold", 30),
        )
        style.configure(
            "Eyebrow.TLabel",
            background=COLORS["paper"],
            foreground=COLORS["gold"],
            font=("Segoe UI Semibold", 9),
        )
        style.configure(
            "Subtitle.TLabel",
            background=COLORS["paper"],
            foreground=COLORS["muted"],
            font=("Segoe UI", 10),
        )
        style.configure(
            "PanelTitle.TLabel",
            background=COLORS["cream"],
            foreground=COLORS["ink"],
            font=("Segoe UI", 16, "bold"),
        )
        style.configure(
            "Body.TLabel",
            background=COLORS["cream"],
            foreground=COLORS["ink"],
            font=("Segoe UI", 10),
        )
        style.configure(
            "Muted.TLabel",
            background=COLORS["cream"],
            foreground=COLORS["muted"],
            font=("Segoe UI", 9),
        )
        style.configure(
            "Timer.TLabel",
            background=COLORS["cream"],
            foreground=COLORS["navy"],
            font=("Consolas", 42, "bold"),
        )
        style.configure(
            "Primary.TButton",
            background=COLORS["navy"],
            foreground=COLORS["cream"],
            borderwidth=0,
            focusthickness=0,
            padding=(18, 12),
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Primary.TButton",
            background=[("active", COLORS["navy_light"]), ("disabled", COLORS["line"])],
            foreground=[("disabled", COLORS["muted"])],
        )
        style.configure(
            "Secondary.TButton",
            background=COLORS["paper_dark"],
            foreground=COLORS["ink"],
            borderwidth=0,
            padding=(16, 11),
            font=("Segoe UI", 10),
        )
        style.map(
            "Secondary.TButton",
            background=[("active", COLORS["line"]), ("disabled", COLORS["paper_dark"])],
        )
        style.configure(
            "Danger.TButton",
            background="#f6eaea",
            foreground=COLORS["danger"],
            borderwidth=0,
            padding=(16, 11),
            font=("Segoe UI", 10),
        )
        style.map("Danger.TButton", background=[("active", "#eedede")])
        style.configure(
            "TSpinbox",
            arrowsize=14,
            padding=5,
            fieldbackground=COLORS["cream"],
            background=COLORS["paper_dark"],
            foreground=COLORS["ink"],
        )
        style.configure(
            "TEntry",
            fieldbackground=COLORS["cream"],
            foreground=COLORS["ink"],
            insertcolor=COLORS["ink"],
            padding=7,
        )

    def _build_layout(self) -> None:
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # 1. Left Sidebar (Warm Gray Background)
        self.sidebar_frame = tk.Frame(self.root, bg=COLORS["paper_dark"], width=230)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)
        self._build_sidebar(self.sidebar_frame)

        # 2. Right Content Pane Container
        self.content_container = tk.Frame(self.root, bg=COLORS["paper"])
        self.content_container.grid(row=0, column=1, sticky="nsew")
        self.content_container.grid_columnconfigure(0, weight=1)
        self.content_container.grid_rowconfigure(0, weight=1)

        # Tab A: Fokus-Timer Pane
        self.timer_pane = RoundedPanel(self.content_container, bg=COLORS["paper"], fill=COLORS["cream"])
        self.timer_pane.inner.grid_columnconfigure(0, weight=1)
        self._build_timer_panel(self.timer_pane.inner)

        # Tab B/C/D: City Panel Pane (Stadt, Kalender, Journal)
        self.city_pane = RoundedPanel(self.content_container, bg=COLORS["paper"], fill=COLORS["cream"])
        self.city_pane.inner.grid_rowconfigure(1, weight=1)
        self.city_pane.inner.grid_columnconfigure(0, weight=1)
        self._build_city_panel(self.city_pane.inner)

        # Set default active tab
        self.current_view.set("timer")
        self._build_native_menus()

    def _build_sidebar(self, parent: tk.Frame) -> None:
        parent.grid_columnconfigure(0, weight=1)

        # Profile Area
        profile = tk.Frame(parent, bg=COLORS["paper_dark"])
        profile.grid(row=0, column=0, sticky="ew", padx=20, pady=(24, 20))
        
        avatar_lbl = tk.Label(profile, text="🔥", font=("Segoe UI", 22), bg=COLORS["paper_dark"])
        avatar_lbl.grid(row=0, column=0, rowspan=3, padx=(0, 10))
        
        user_lbl = tk.Label(profile, text="Lernzeit-Profi", font=("Segoe UI", 10, "bold"), fg=COLORS["ink"], bg=COLORS["paper_dark"])
        user_lbl.grid(row=0, column=1, sticky="w")
        
        self.sidebar_streak_lbl = tk.Label(profile, text="Streak: 0 Tage", font=("Segoe UI", 8), fg=COLORS["muted"], bg=COLORS["paper_dark"])
        self.sidebar_streak_lbl.grid(row=1, column=1, sticky="w")

        # Visual preview of the streak status (last 7 days)
        self.streak_preview_canvas = tk.Canvas(
            profile,
            width=100,
            height=14,
            bg=COLORS["paper_dark"],
            bd=0,
            highlightthickness=0
        )
        self.streak_preview_canvas.grid(row=2, column=1, sticky="w", pady=(2, 0))

        # Nav Area
        self.nav_frame = tk.Frame(parent, bg=COLORS["paper_dark"])
        self.nav_frame.grid(row=1, column=0, sticky="new", padx=12)
        parent.grid_rowconfigure(1, weight=1)

        # Create sidebar buttons with custom styling
        self.nav_buttons = {}
        nav_items = [
            ("timer", "⏱  Fokus-Timer"),
            ("stats", "📊  Statistiken"),
            ("calendar", "📅  Lern-Kalender"),
            ("notes", "📝  Lernjournal"),
        ]
        for idx, (view_id, label) in enumerate(nav_items):
            btn = tk.Button(
                self.nav_frame,
                text=label,
                font=("Segoe UI", 10, "normal"),
                anchor="w",
                padx=16,
                pady=10,
                bg=COLORS["paper_dark"],
                fg=COLORS["muted"],
                relief="flat",
                bd=0,
                cursor="hand2",
                activebackground="#eef0fe",
                activeforeground="#3b52e2"
            )
            btn.pack(fill="x", pady=3)
            btn.configure(command=lambda v=view_id: self.switch_view(v))
            self.nav_buttons[view_id] = btn

        # Gear/Settings button at the bottom of nav
        settings_btn = tk.Button(
            self.nav_frame,
            text="⚙  Einstellungen",
            font=("Segoe UI", 10),
            anchor="w",
            padx=16,
            pady=10,
            relief="flat",
            bd=0,
            cursor="hand2",
            bg=COLORS["paper_dark"],
            fg=COLORS["muted"],
            activebackground="#eef0fe",
            activeforeground="#3b52e2",
            command=self.open_settings
        )
        settings_btn.pack(fill="x", pady=(20, 0))

        # Bottom XP Progress Area
        self.xp_sidebar_frame = tk.Frame(parent, bg=COLORS["paper_dark"])
        self.xp_sidebar_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=24)
        parent.grid_rowconfigure(2, weight=0)

        self.xp_sidebar_frame.grid_columnconfigure(0, weight=1)
        self.sidebar_lvl_lbl = tk.Label(self.xp_sidebar_frame, text="Level 1", font=("Segoe UI", 8, "bold"), fg=COLORS["ink"], bg=COLORS["paper_dark"])
        self.sidebar_lvl_lbl.grid(row=0, column=0, sticky="w")

        self.sidebar_xp_lbl = tk.Label(self.xp_sidebar_frame, text="0 / 100 XP", font=("Segoe UI", 8), fg=COLORS["muted"], bg=COLORS["paper_dark"])
        self.sidebar_xp_lbl.grid(row=0, column=1, sticky="e")

        self.xp_sidebar_canvas = tk.Canvas(self.xp_sidebar_frame, height=8, bg=COLORS["paper_dark"], bd=0, highlightthickness=0)
        self.xp_sidebar_canvas.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(6, 0))

        # Version label directly under the XP Progress Area, right-aligned
        self.sidebar_version_lbl = tk.Label(
            self.xp_sidebar_frame,
            text=f"Version {APP_VERSION}",
            font=("Segoe UI", 7),
            fg=COLORS["muted"],
            bg=COLORS["paper_dark"]
        )
        self.sidebar_version_lbl.grid(row=2, column=0, columnspan=2, sticky="e", pady=(4, 0))

    def _draw_streak_preview(self) -> None:
        c = self.streak_preview_canvas
        if not c.winfo_exists():
            return
        c.delete("all")
        
        dot_r = 3.5
        gap = 4.5
        start_x = 4
        y = 7
        
        qualifying = self._qualifying_streak_days(include_active=True)
        today = date.today()
        
        for i in range(7):
            day = today - timedelta(days=6-i)
            day_str = day.isoformat()
            
            x = start_x + i * (dot_r * 2 + gap)
            is_active = day_str in qualifying
            color = "#3b52e2" if is_active else "#e6e6e2"
            outline_color = "#3b52e2" if is_active else "#b0b0a8"
            
            c.create_oval(
                x - dot_r, y - dot_r, x + dot_r, y + dot_r,
                fill=color, outline=outline_color, width=1
            )

    def _draw_sidebar_xp(self) -> None:
        c = self.xp_sidebar_canvas
        if not c.winfo_exists():
            return
        c.delete("all")
        w = max(100, c.winfo_width())
        h = 8
        
        total_xp = self.total_visible_xp
        level, current_xp_in_level, cost = self._player_level_info(total_xp)
        
        self.sidebar_lvl_lbl.configure(text=f"Level {level}")
        self.sidebar_xp_lbl.configure(text=f"{current_xp_in_level} / {cost} XP")
        
        c.create_rectangle(0, 0, w, h, fill="#e6e6e2", outline="", width=0)
        
        percent = min(1.0, max(0.0, current_xp_in_level / cost))
        fill_w = w * percent
        if fill_w > 0:
            c.create_rectangle(0, 0, fill_w, h, fill="#3b52e2", outline="", width=0)

    def _update_sidebar_nav(self) -> None:
        view = self.current_view.get()
        for key, btn in self.nav_buttons.items():
            if key == view:
                btn.configure(bg="#eef0fe", fg="#3b52e2", font=("Segoe UI", 10, "bold"))
            else:
                btn.configure(bg=COLORS["paper_dark"], fg=COLORS["muted"], font=("Segoe UI", 10, "normal"))

    def _build_native_menus(self) -> None:
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # "Lernreich" / Main menu
        main_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Menü", menu=main_menu)
        main_menu.add_command(label="⏱  Fokus-Timer", command=lambda: self.switch_view("timer"))
        main_menu.add_command(label="📊  Statistiken", command=lambda: self.switch_view("stats"))
        main_menu.add_command(label="📅  Lern-Kalender", command=lambda: self.switch_view("calendar"))
        main_menu.add_command(label="📝  Lernjournal", command=lambda: self.switch_view("notes"))
        main_menu.add_separator()
        main_menu.add_command(label="⚙️  Einstellungen", command=self.open_settings)
        main_menu.add_command(label="📤  Sessions als CSV exportieren", command=self.export_sessions_csv)
        main_menu.add_separator()
        main_menu.add_command(label="❌  Beenden", command=self._quit_from_tray)

        # Tools Menu
        tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="📋  Tagesplanung", command=self.open_daily_plan)
        tools_menu.add_command(label="📊  Wochenbericht", command=self.open_week_report)
        tools_menu.add_command(label="🔄  Wiederholen (Spaced Repetition)", command=self.open_review_reminders)

    def _build_timer_panel(self, parent: ttk.Frame) -> None:
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)

        # 1. Setup Frame Container
        self.timer_setup_frame = tk.Frame(parent, bg=COLORS["cream"])
        self._build_timer_setup_frame(self.timer_setup_frame)

        # 2. Active Frame Container
        self.timer_active_frame = tk.Frame(parent, bg=COLORS["cream"])
        self._build_timer_active_frame(self.timer_active_frame)

    def _build_timer_setup_frame(self, parent: tk.Frame) -> None:
        # Wrap everything in a container to enforce professional padding
        container = tk.Frame(parent, bg=COLORS["cream"])
        container.pack(fill="both", expand=True, padx=30, pady=(12, 10))

        title_lbl = tk.Label(
            container,
            text="Fokus-Sitzung einrichten",
            font=("Segoe UI", 16, "bold"),
            fg=COLORS["ink"],
            bg=COLORS["cream"]
        )
        title_lbl.pack(anchor="w", pady=(5, 2))
        
        subtitle_lbl = tk.Label(
            container,
            text="Bereite deinen Kopf vor und schließe alle Ablenkungen aus.",
            font=("Segoe UI", 9),
            fg=COLORS["muted"],
            bg=COLORS["cream"]
        )
        subtitle_lbl.pack(anchor="w", pady=(0, 15))

        input_container = tk.Frame(container, bg=COLORS["cream"])
        input_container.pack(fill="x", pady=5)
        
        tk.Label(
            input_container,
            text="Was möchtest du lernen? (Fach)",
            font=("Segoe UI", 9, "bold"),
            fg=COLORS["muted"],
            bg=COLORS["cream"]
        ).pack(anchor="w", pady=(4, 4))
        
        subject_bg = RoundedPanel(input_container, bg=COLORS["cream"], fill=COLORS["cream"], radius=8, height=36)
        subject_bg.pack(fill="x", pady=(0, 8))
        self.subject_entry = tk.Entry(
            subject_bg.inner,
            textvariable=self.subject_text,
            font=("Segoe UI", 10),
            bg=COLORS["cream"],
            fg=COLORS["ink"],
            bd=0,
            relief="flat",
            insertbackground=COLORS["ink"]
        )
        self.subject_entry.pack(fill="both", expand=True, padx=10, pady=6)
        self.subject_entry.bind("<FocusOut>", lambda _event: self._save_current_session())
        self.subject_entry.bind("<Return>", lambda _event: self._save_current_session())

        tk.Label(
            input_container,
            text="Was ist dein konkretes Lernziel? (Ziel)",
            font=("Segoe UI", 9, "bold"),
            fg=COLORS["muted"],
            bg=COLORS["cream"]
        ).pack(anchor="w", pady=(4, 4))
        
        goal_bg = RoundedPanel(input_container, bg=COLORS["cream"], fill=COLORS["cream"], radius=8, height=36)
        goal_bg.pack(fill="x", pady=(0, 10))
        self.goal_entry = tk.Entry(
            goal_bg.inner,
            textvariable=self.goal_text,
            font=("Segoe UI", 10),
            bg=COLORS["cream"],
            fg=COLORS["ink"],
            bd=0,
            relief="flat",
            insertbackground=COLORS["ink"]
        )
        self.goal_entry.pack(fill="both", expand=True, padx=10, pady=6)
        self.goal_entry.bind("<FocusOut>", lambda _event: self._save_current_session())
        self.goal_entry.bind("<Return>", lambda _event: self._save_current_session())

        # Beautiful vertical stack of sliders with clean labels and live HSL-harmony styles
        sliders_container = tk.Frame(container, bg=COLORS["cream"])
        sliders_container.pack(fill="x", pady=(5, 10))

        # 1. Slider: Duration (Dauer)
        dur_row = tk.Frame(sliders_container, bg=COLORS["cream"])
        dur_row.pack(fill="x", pady=6)

        dur_hdr = tk.Frame(dur_row, bg=COLORS["cream"])
        dur_hdr.pack(fill="x")

        dur_lbl = tk.Label(
            dur_hdr,
            text="Fokus-Dauer",
            font=("Segoe UI", 9, "bold"),
            fg=COLORS["muted"],
            bg=COLORS["cream"]
        )
        dur_lbl.pack(side="left")

        self.dur_value_lbl = tk.Label(
            dur_hdr,
            text=f"{self.target_minutes.get()} Min",
            font=("Segoe UI", 10, "bold"),
            fg=COLORS["gold"],
            bg=COLORS["cream"]
        )
        self.dur_value_lbl.pack(side="right")

        self.dur_scale = tk.Scale(
            dur_row,
            from_=5,
            to=MAX_SESSION_MINUTES,
            resolution=5,
            orient="horizontal",
            showvalue=False,
            variable=self.target_minutes,
            command=self._on_duration_slider_changed,
            bg="#ffffff",
            troughcolor=COLORS["gold"],
            activebackground="#ffffff",
            highlightthickness=0,
            bd=0,
            width=8,
            sliderlength=24,
            length=450,
            sliderrelief="flat",
            cursor="hand2"
        )
        self.dur_scale.pack(fill="x", pady=(4, 0))

        # 2. Slider: Popup Reminder (Popup)
        pop_row = tk.Frame(sliders_container, bg=COLORS["cream"])
        pop_row.pack(fill="x", pady=6)

        pop_hdr = tk.Frame(pop_row, bg=COLORS["cream"])
        pop_hdr.pack(fill="x")

        pop_lbl = tk.Label(
            pop_hdr,
            text="Erinnerungs-Intervall (Popup)",
            font=("Segoe UI", 9, "bold"),
            fg=COLORS["muted"],
            bg=COLORS["cream"]
        )
        pop_lbl.pack(side="left")

        self.pop_value_lbl = tk.Label(
            pop_hdr,
            text=f"{self.reminder_minutes.get()} Min",
            font=("Segoe UI", 10, "bold"),
            fg=COLORS["gold"],
            bg=COLORS["cream"]
        )
        self.pop_value_lbl.pack(side="right")

        self.pop_scale = tk.Scale(
            pop_row,
            from_=5,
            to=90,
            resolution=5,
            orient="horizontal",
            showvalue=False,
            variable=self.reminder_minutes,
            command=self._on_popup_slider_changed,
            bg="#ffffff",
            troughcolor=COLORS["gold"],
            activebackground="#ffffff",
            highlightthickness=0,
            bd=0,
            width=8,
            sliderlength=24,
            length=450,
            sliderrelief="flat",
            cursor="hand2"
        )
        self.pop_scale.pack(fill="x", pady=(4, 0))

        # 3. Slider: Daily Goal (Tagesziel)
        goal_row = tk.Frame(sliders_container, bg=COLORS["cream"])
        goal_row.pack(fill="x", pady=6)

        goal_hdr = tk.Frame(goal_row, bg=COLORS["cream"])
        goal_hdr.pack(fill="x")

        goal_lbl = tk.Label(
            goal_hdr,
            text="Tägliches Lernziel",
            font=("Segoe UI", 9, "bold"),
            fg=COLORS["muted"],
            bg=COLORS["cream"]
        )
        goal_lbl.pack(side="left")

        self.goal_value_lbl = tk.Label(
            goal_hdr,
            text=f"{self.daily_goal_hours.get():.1f} Std",
            font=("Segoe UI", 10, "bold"),
            fg=COLORS["gold"],
            bg=COLORS["cream"]
        )
        self.goal_value_lbl.pack(side="right")

        self.goal_scale = tk.Scale(
            goal_row,
            from_=0.5,
            to=12.0,
            resolution=0.5,
            orient="horizontal",
            showvalue=False,
            variable=self.daily_goal_hours,
            command=self._on_goal_slider_changed,
            bg="#ffffff",
            troughcolor=COLORS["gold"],
            activebackground="#ffffff",
            highlightthickness=0,
            bd=0,
            width=8,
            sliderlength=24,
            length=450,
            sliderrelief="flat",
            cursor="hand2"
        )
        self.goal_scale.pack(fill="x", pady=(4, 0))

        self.chk_box = RoundedPanel(container, bg=COLORS["cream"], fill=COLORS["paper_dark"], radius=8)
        self.chk_box.pack(fill="x", pady=12)
        self.chk_box.inner.configure(padx=16, pady=10)
        
        tk.Label(
            self.chk_box.inner,
            text="FOKUS-VORBEREITUNG",
            font=("Segoe UI", 8, "bold"),
            fg=COLORS["muted"],
            bg=COLORS["paper_dark"]
        ).pack(anchor="w", pady=(0, 6))

        self.checklist_vars = []
        for item in FOCUS_CHECKLIST_ITEMS:
            var = tk.BooleanVar(value=False)
            chk = tk.Checkbutton(
                self.chk_box.inner,
                text=item,
                variable=var,
                command=self._on_checklist_changed,
                bg=COLORS["paper_dark"],
                activebackground=COLORS["paper_dark"],
                selectcolor="#ffffff",
                fg=COLORS["ink"],
                activeforeground=COLORS["ink"],
                font=("Segoe UI", 9),
                bd=0,
                relief="flat",
                cursor="hand2"
            )
            chk.pack(anchor="w", pady=2)
            self.checklist_vars.append(var)

        # Setup buttons action frame
        setup_buttons = tk.Frame(container, bg=COLORS["cream"])
        setup_buttons.pack(fill="x", pady=(12, 5))
        setup_buttons.columnconfigure((0, 1), weight=1)

        self.start_timer_btn = tk.Button(
            setup_buttons,
            text="⏱  Fokus starten",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["navy"],
            fg=COLORS["cream"],
            activebackground=COLORS["navy_light"],
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            cursor="hand2",
            state="normal",
            command=self.start_new_session_action,
            pady=10
        )
        self.start_timer_btn.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        self.resume_timer_btn = tk.Button(
            setup_buttons,
            text="🔄  Sitzung fortsetzen",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["paper_dark"],
            fg=COLORS["ink"],
            activebackground=COLORS["line"],
            activeforeground=COLORS["ink"],
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.resume_session_action,
            pady=10
        )
        self.resume_timer_btn.grid(row=0, column=1, sticky="ew", padx=(6, 0))

    def _on_checklist_changed(self) -> None:
        pass

    def _on_duration_slider_changed(self, value) -> None:
        self.dur_value_lbl.configure(text=f"{int(float(value))} Min")
        self._target_changed()

    def _on_popup_slider_changed(self, value) -> None:
        self.pop_value_lbl.configure(text=f"{int(float(value))} Min")
        self.save_preferences()

    def _on_goal_slider_changed(self, value) -> None:
        self.goal_value_lbl.configure(text=f"{float(value):.1f} Std")
        self.save_preferences()

    def _build_timer_active_frame(self, parent: tk.Frame) -> None:
        container = tk.Frame(parent, bg=COLORS["cream"])
        container.pack(fill="both", expand=True, padx=30, pady=(8, 8))
        container.grid_columnconfigure(0, weight=1)

        self.active_phase_lbl = tk.Label(
            container,
            text="FOKUS-PHASE LÄUFT",
            font=("Segoe UI", 9, "bold"),
            fg=COLORS["gold"],
            bg=COLORS["cream"]
        )
        self.active_phase_lbl.grid(row=0, column=0, pady=(2, 1))
        
        self.active_subject_lbl = tk.Label(
            container,
            text="Mathematik & Algorithmen",
            font=("Segoe UI", 14, "bold"),
            fg=COLORS["ink"],
            bg=COLORS["cream"]
        )
        self.active_subject_lbl.grid(row=1, column=0, pady=(0, 2))

        self.timer_label = ttk.Label(container, text="00:00:00", style="Timer.TLabel", anchor="center")
        self.timer_label.grid(row=2, column=0, pady=(2, 2))

        self.hourglass_canvas = tk.Canvas(
            container,
            width=214,
            height=200,
            bg=COLORS["cream"],
            bd=0,
            highlightthickness=0,
        )
        self.hourglass_canvas.grid(row=3, column=0, pady=(2, 2))

        self.progress_canvas = tk.Canvas(
            container,
            height=38,
            bg=COLORS["cream"],
            bd=0,
            highlightthickness=0,
        )
        self.progress_canvas.grid(row=4, column=0, sticky="ew", pady=2)

        buttons = tk.Frame(container, bg=COLORS["cream"])
        buttons.grid(row=5, column=0, sticky="ew", pady=3)
        buttons.grid_columnconfigure((0, 1), weight=1)
        
        self.start_button = tk.Button(
            buttons,
            text=self.t("start"),
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["navy"],
            fg=COLORS["cream"],
            activebackground=COLORS["navy_light"],
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.toggle_running,
            pady=8
        )
        self.start_button.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        
        self.abort_button = tk.Button(
            buttons,
            text=self.t("aware_abort"),
            font=("Segoe UI", 10),
            bg=COLORS["paper_dark"],
            fg=COLORS["ink"],
            activebackground=COLORS["line"],
            activeforeground=COLORS["ink"],
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.request_abort_session,
            pady=8
        )
        self.abort_button.grid(row=0, column=1, sticky="ew", padx=(6, 0))

        bottom = tk.Frame(container, bg=COLORS["cream"])
        bottom.grid(row=6, column=0, sticky="ew", pady=(3, 3))
        bottom.grid_columnconfigure(0, weight=1)
        
        self.break_button = tk.Button(
            bottom,
            text=self.t("break_after_focus"),
            font=("Segoe UI", 10),
            bg=COLORS["paper_dark"],
            fg=COLORS["ink"],
            activebackground=COLORS["line"],
            activeforeground=COLORS["ink"],
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.toggle_break,
            pady=8
        )
        self.break_button.grid(row=0, column=0, sticky="ew")

        self.status_label = tk.Label(
            container,
            textvariable=self.status_text,
            font=("Segoe UI", 9),
            fg=COLORS["muted"],
            bg=COLORS["cream"],
            wraplength=400,
            justify="center"
        )
        self.status_label.grid(row=7, column=0, pady=(4, 2))

        self.penalty_label = tk.Label(
            container,
            text="",
            font=("Segoe UI", 8, "bold"),
            fg=COLORS["danger"],
            bg=COLORS["cream"],
            wraplength=400,
            justify="center"
        )
        self.penalty_label.grid(row=8, column=0, pady=(2, 2))

        # Dummy hidden stats labels to prevent AttributeError crashes
        hidden_frame = tk.Frame(parent)
        self.total_label = tk.Label(hidden_frame)
        self.xp_label = tk.Label(hidden_frame)
        self.today_label = tk.Label(hidden_frame)
        self.streak_label = tk.Label(hidden_frame)
        self.next_label = tk.Label(hidden_frame)

    def _build_city_panel(self, parent: ttk.Frame) -> None:
        top = ttk.Frame(parent, style="Panel.TFrame")
        top.grid(row=0, column=0, sticky="ew", padx=22, pady=(22, 10))
        top.grid_columnconfigure(0, weight=1)
        top.grid_columnconfigure(1, weight=0)
        top.grid_columnconfigure(2, weight=0)
        ttk.Label(top, text=self.t("avalon_valley"), style="PanelTitle.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        self.city_summary = ttk.Label(top, text="", style="Muted.TLabel")
        self.city_summary.grid(row=1, column=0, sticky="w", pady=(2, 0))

        view_switch = ttk.Frame(top, style="Panel.TFrame")
        view_switch.grid(row=0, column=1, rowspan=2, sticky="e", padx=(12, 0))
        self.tal_button = ttk.Button(
            view_switch,
            text=self.t("avalon_tab"),
            style="Primary.TButton",
            command=lambda: self.switch_view("stats"),
        )
        self.tal_button.grid(row=0, column=0, padx=(0, 6))
        self.calendar_button = ttk.Button(
            view_switch,
            text=self.t("calendar"),
            style="Secondary.TButton",
            command=lambda: self.switch_view("calendar"),
        )
        self.calendar_button.grid(row=0, column=1, padx=(0, 6))
        self.notes_button = ttk.Button(
            view_switch,
            text=self.t("notes_tab"),
            style="Secondary.TButton",
            command=lambda: self.switch_view("notes"),
        )
        self.notes_button.grid(row=0, column=2)

        stats_wrap = ttk.Frame(top, style="Panel.TFrame")
        stats_wrap.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(12, 0))
        stats_wrap.grid_columnconfigure(0, weight=1)
        self.focus_summary_label = ttk.Label(stats_wrap, text="", style="Muted.TLabel")
        self.focus_summary_label.grid(row=0, column=0, sticky="w")
        self.prev_month_button = ttk.Button(
            stats_wrap,
            text="<",
            style="Secondary.TButton",
            command=lambda: self.shift_calendar_month(-1),
        )
        self.prev_month_button.grid(row=0, column=1, padx=(12, 4))
        self.next_month_button = ttk.Button(
            stats_wrap,
            text=">",
            style="Secondary.TButton",
            command=lambda: self.shift_calendar_month(1),
        )
        self.next_month_button.grid(row=0, column=2)
        self.open_notes_button = ttk.Button(
            stats_wrap,
            text=self.t("open_notes_folder"),
            style="Secondary.TButton",
            command=self.open_notes_folder,
        )
        self.open_notes_button.grid(row=0, column=3, padx=(10, 0))
        self.daily_plan_button = ttk.Button(
            stats_wrap,
            text=self.t("daily_plan"),
            style="Secondary.TButton",
            command=self.open_daily_plan,
        )
        self.daily_plan_button.grid(row=0, column=4, padx=(10, 0))
        self.week_report_button = ttk.Button(
            stats_wrap,
            text=self.t("week_report"),
            style="Secondary.TButton",
            command=self.open_week_report,
        )
        self.week_report_button.grid(row=0, column=5, padx=(8, 0))
        self.review_button = ttk.Button(
            stats_wrap,
            text=self.t("reviews"),
            style="Secondary.TButton",
            command=self.open_review_reminders,
        )
        self.review_button.grid(row=0, column=6, padx=(8, 0))

        self.city_canvas = tk.Canvas(
            parent,
            bg=COLORS["cream"],
            bd=0,
            highlightthickness=0,
        )
        self.city_canvas.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))

        journal = ttk.Frame(parent, style="Panel.TFrame")
        journal.grid(row=2, column=0, sticky="ew", padx=22, pady=(0, 22))
        journal.grid_columnconfigure(0, weight=1)
        journal.grid_columnconfigure(1, weight=1)

        learned = ttk.Frame(journal, style="Panel.TFrame")
        learned.grid(row=0, column=0, sticky="nsew", padx=(0, 16))
        learned.grid_columnconfigure(0, weight=1)
        ttk.Label(learned, text=self.t("learned"), style="Body.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        self.learned_text = tk.Text(
            learned,
            height=4,
            wrap="word",
            bg=COLORS["cream"],
            fg=COLORS["ink"],
            insertbackground=COLORS["ink"],
            relief="solid",
            bd=1,
            highlightthickness=0,
            font=("Segoe UI", 9),
        )
        self.learned_text.grid(row=1, column=0, sticky="ew", pady=(4, 8))
        ttk.Button(
            learned,
            text=self.t("save_note"),
            style="Secondary.TButton",
            command=self.save_learning_note,
        ).grid(row=2, column=0, sticky="w")

        history = ttk.Frame(journal, style="Panel.TFrame")
        history.grid(row=0, column=1, sticky="nsew")
        history.grid_columnconfigure(0, weight=1)
        ttk.Label(history, text=self.t("upgrade_tree"), style="Body.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        self.tree_label = ttk.Label(history, text="", style="Muted.TLabel", wraplength=330)
        self.tree_label.grid(row=1, column=0, sticky="w", pady=(4, 8))
        ttk.Label(history, text=self.t("last_sessions"), style="Body.TLabel").grid(
            row=2, column=0, sticky="w"
        )
        self.journal_label = ttk.Label(history, text="", style="Muted.TLabel", wraplength=330)
        self.journal_label.grid(row=3, column=0, sticky="w", pady=(4, 0))

    def _bind_events(self) -> None:
        self.root.bind("<space>", lambda _event: self.toggle_running())
        self.root.bind("<Configure>", self._on_resize)

    def _on_resize(self, _event=None) -> None:
        self.root.after_idle(self._render_all)

    def _restore_active_learning_note(self) -> None:
        if self._active_learned:
            self.learned_text.insert("1.0", self._active_learned)

    def save_learning_note(self) -> None:
        self._save_current_session()
        self.current_view.set("notes")
        self.status_text.set("Lernnotiz gemerkt und im Tagesordner gespeichert.")
        self._render_all()

    def save_preferences(self) -> None:
        self.data["daily_goal_hours"] = self._daily_goal_hours()
        self.data["language"] = self.language.get()
        self.data["active_subject"] = self._current_subject()
        self.data["target_minutes"] = self._clamped_target_minutes()
        self.data["reminder_minutes"] = self._clamped_reminder_minutes()
        self._save_current_session()
        self._render_all()

    def _target_changed(self) -> None:
        minutes = self._clamped_target_minutes()
        self.data["target_minutes"] = minutes
        if minutes >= MAX_SESSION_MINUTES:
            self.status_text.set("Zielzeit auf maximal 2,5 Stunden begrenzt.")
        if self.session_seconds > 0:
            self.data["active_target_minutes"] = minutes
            self._target_reached_popup_shown = self.session_seconds >= self._target_seconds()
            self._save_current_session()
        else:
            save_progress(self.data)
        self._render_all()

    def _clamped_target_minutes(self) -> int:
        minutes = self._clamp_minutes_value(
            self.target_minutes.get(),
            DEFAULT_TARGET_MINUTES,
            1,
            MAX_SESSION_MINUTES,
        )
        try:
            if int(self.target_minutes.get()) != minutes:
                self.target_minutes.set(minutes)
        except (tk.TclError, ValueError):
            self.target_minutes.set(minutes)
        return minutes

    def _clamped_reminder_minutes(self) -> int:
        minutes = self._clamp_minutes_value(self.reminder_minutes.get(), 15, 1, 90)
        try:
            if int(self.reminder_minutes.get()) != minutes:
                self.reminder_minutes.set(minutes)
        except (tk.TclError, ValueError):
            self.reminder_minutes.set(minutes)
        return minutes

    def open_notes_folder(self) -> None:
        path = notes_root_path()
        try:
            os.startfile(path)
            self.status_text.set(f"Notizen-Ordner geoeffnet: {path}")
        except OSError:
            messagebox.showerror(
                "Notizen",
                f"Der Notizen-Ordner konnte nicht geoeffnet werden:\n{path}",
                parent=self.root,
            )

    def _plan_for_day(self, day: date) -> list[dict]:
        plans = self.data.setdefault("daily_plans", {})
        raw_plan = plans.get(day.isoformat(), {})
        raw_items = raw_plan.get("items", []) if isinstance(raw_plan, dict) else []
        items = []
        for item in raw_items[:3]:
            if not isinstance(item, dict):
                continue
            text = " ".join(str(item.get("text", "")).split())
            if text:
                items.append({"text": text, "done": bool(item.get("done", False))})
        return items

    def _save_plan_for_day(self, day: date, items: list[dict]) -> None:
        plans = self.data.setdefault("daily_plans", {})
        plans[day.isoformat()] = {
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "items": items[:3],
        }
        save_progress(self.data)

    def open_daily_plan(self) -> None:
        today = date.today()
        items = self._plan_for_day(today)

        popup = tk.Toplevel(self.root)
        popup.title(self.t("daily_plan"))
        popup.configure(bg=COLORS["paper"])
        popup.resizable(False, False)
        popup.transient(self.root)

        x = self.root.winfo_rootx() + max(120, self.root.winfo_width() // 2 - 230)
        y = self.root.winfo_rooty() + max(80, self.root.winfo_height() // 2 - 180)
        popup.geometry(f"460x360+{x}+{y}")

        frame = tk.Frame(popup, bg=COLORS["cream"], padx=22, pady=20)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        tk.Label(
            frame,
            text="Tagesplanung",
            bg=COLORS["cream"],
            fg=COLORS["ink"],
            font=("Segoe UI", 16, "bold"),
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 4))
        tk.Label(
            frame,
            text="Lege 1-3 klare Lernziele fuer heute fest.",
            bg=COLORS["cream"],
            fg=COLORS["muted"],
            font=("Segoe UI", 10),
        ).grid(row=1, column=0, columnspan=3, sticky="w", pady=(0, 14))

        rows = []
        for index in range(3):
            text_var = tk.StringVar(value=items[index]["text"] if index < len(items) else "")
            done_var = tk.BooleanVar(value=items[index]["done"] if index < len(items) else False)
            ttk.Checkbutton(frame, variable=done_var).grid(row=2 + index, column=0, sticky="w", pady=5)
            entry = ttk.Entry(frame, textvariable=text_var)
            entry.grid(row=2 + index, column=1, columnspan=2, sticky="ew", padx=(8, 0), pady=5)
            rows.append((text_var, done_var))
        frame.grid_columnconfigure(1, weight=1)

        def save_plan() -> None:
            plan_items = []
            for text_var, done_var in rows:
                text = " ".join(text_var.get().split())
                if text:
                    plan_items.append({"text": text, "done": bool(done_var.get())})
            self._save_plan_for_day(today, plan_items)
            self.status_text.set(self.t("plan_saved"))
            popup.destroy()
            self._render_all()

        ttk.Button(
            frame,
            text=self.t("save"),
            style="Primary.TButton",
            command=save_plan,
        ).grid(row=6, column=0, columnspan=3, sticky="ew", pady=(18, 8))
        ttk.Button(
            frame,
            text=self.t("close"),
            style="Secondary.TButton",
            command=popup.destroy,
        ).grid(row=7, column=0, columnspan=3, sticky="ew")

    def open_week_report(self) -> None:
        report = self._week_report()
        popup = tk.Toplevel(self.root)
        popup.title(self.t("week_report"))
        popup.configure(bg=COLORS["paper"])
        popup.resizable(True, True)
        popup.transient(self.root)

        x = self.root.winfo_rootx() + max(80, self.root.winfo_width() // 2 - 280)
        y = self.root.winfo_rooty() + max(40, self.root.winfo_height() // 2 - 280)
        popup.geometry(f"560x560+{x}+{y}")
        popup.minsize(520, 520)

        frame = tk.Frame(popup, bg=COLORS["cream"], padx=22, pady=16)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        tk.Label(
            frame,
            text="Wochenbericht",
            bg=COLORS["cream"],
            fg=COLORS["ink"],
            font=("Segoe UI", 17, "bold"),
        ).pack(anchor="w")
        tk.Label(
            frame,
            text=report["range"],
            bg=COLORS["cream"],
            fg=COLORS["muted"],
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(2, 12))

        for title, value in report["lines"]:
            row = tk.Frame(frame, bg=COLORS["cream"])
            row.pack(fill="x", pady=3)
            tk.Label(
                row,
                text=title,
                bg=COLORS["cream"],
                fg=COLORS["muted"],
                font=("Segoe UI", 10),
                width=18,
                anchor="w",
            ).pack(side="left")
            tk.Label(
                row,
                text=value,
                bg=COLORS["cream"],
                fg=COLORS["ink"],
                font=("Segoe UI", 10, "bold"),
                anchor="w",
                justify="left",
            ).pack(side="left", fill="x", expand=True)

        tk.Label(
            frame,
            text=report["note"],
            bg=COLORS["cream"],
            fg=COLORS["muted"],
            font=("Segoe UI", 9),
            justify="left",
            wraplength=490,
        ).pack(anchor="w", pady=(12, 12))
        ttk.Button(
            frame,
            text=self.t("close"),
            style="Primary.TButton",
            command=popup.destroy,
        ).pack(fill="x")

    def open_review_reminders(self) -> None:
        due_reviews = self._due_reviews()
        if not due_reviews:
            messagebox.showinfo(
                "Wiederholen",
                "Heute sind keine Wiederholungen faellig.",
                parent=self.root,
            )
            return

        popup = tk.Toplevel(self.root)
        popup.title(self.t("reviews"))
        popup.configure(bg=COLORS["paper"])
        popup.resizable(True, True)
        popup.transient(self.root)

        x = self.root.winfo_rootx() + max(80, self.root.winfo_width() // 2 - 260)
        y = self.root.winfo_rooty() + max(50, self.root.winfo_height() // 2 - 230)
        popup.geometry(f"520x460+{x}+{y}")
        popup.minsize(500, 420)

        frame = tk.Frame(popup, bg=COLORS["cream"], padx=22, pady=18)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        tk.Label(
            frame,
            text="Faellige Wiederholungen",
            bg=COLORS["cream"],
            fg=COLORS["ink"],
            font=("Segoe UI", 17, "bold"),
        ).pack(anchor="w")
        tk.Label(
            frame,
            text="Markiere die Themen, die du heute wiederholt hast.",
            bg=COLORS["cream"],
            fg=COLORS["muted"],
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(2, 14))

        checks = []
        for index, review in due_reviews[:8]:
            done_var = tk.BooleanVar(value=False)
            row = tk.Frame(frame, bg=COLORS["cream"])
            row.pack(fill="x", pady=5)
            ttk.Checkbutton(row, variable=done_var).pack(side="left")
            text = (
                f"{review.get('due', '')} · {review.get('subject', DEFAULT_SUBJECT)} · "
                f"{self._short_text(str(review.get('goal', 'Lernsession')), 52)}"
            )
            tk.Label(
                row,
                text=text,
                bg=COLORS["cream"],
                fg=COLORS["ink"],
                font=("Segoe UI", 10),
                anchor="w",
                justify="left",
                wraplength=410,
            ).pack(side="left", fill="x", expand=True, padx=(8, 0))
            checks.append((index, done_var))

        hidden = max(0, len(due_reviews) - 8)
        if hidden:
            tk.Label(
                frame,
                text=f"+{hidden} weitere faellige Wiederholungen.",
                bg=COLORS["cream"],
                fg=COLORS["muted"],
                font=("Segoe UI", 9),
            ).pack(anchor="w", pady=(8, 0))

        def save_done() -> None:
            reviews = list(self.data.get("reviews", []))
            changed = 0
            now_text = datetime.now().strftime("%Y-%m-%d %H:%M")
            for index, done_var in checks:
                if done_var.get() and 0 <= index < len(reviews):
                    reviews[index]["status"] = "erledigt"
                    reviews[index]["completed"] = now_text
                    changed += 1
            self.data["reviews"] = reviews
            save_progress(self.data)
            self.status_text.set(f"{changed} Wiederholung(en) erledigt.")
            popup.destroy()
            self._render_all()

        ttk.Button(
            frame,
            text="Erledigte speichern",
            style="Primary.TButton",
            command=save_done,
        ).pack(fill="x", pady=(16, 8))
        ttk.Button(
            frame,
            text=self.t("close"),
            style="Secondary.TButton",
            command=popup.destroy,
        ).pack(fill="x")

    def _due_reviews(self) -> list[tuple[int, dict]]:
        today_key = date.today().isoformat()
        due = []
        for index, review in enumerate(self.data.get("reviews", [])):
            if str(review.get("status", "offen")) == "erledigt":
                continue
            due_key = str(review.get("due", ""))
            if len(due_key) == 10 and due_key <= today_key:
                due.append((index, review))
        return due

    def _review_counts(self) -> tuple[int, int]:
        today_key = date.today().isoformat()
        due = 0
        upcoming = 0
        for review in self.data.get("reviews", []):
            if str(review.get("status", "offen")) == "erledigt":
                continue
            due_key = str(review.get("due", ""))
            if len(due_key) != 10:
                continue
            if due_key <= today_key:
                due += 1
            else:
                upcoming += 1
        return due, upcoming

    def _show_due_reviews_once(self) -> None:
        if self._review_popup_shown:
            return
        self._review_popup_shown = True
        if self._due_reviews():
            self.open_review_reminders()

    def _schedule_review(self, session: dict, days: int) -> None:
        due_day = date.today() + timedelta(days=days)
        reviews = list(self.data.get("reviews", []))
        reviews.append(
            {
                "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "due": due_day.isoformat(),
                "status": "offen",
                "subject": str(session.get("subject", DEFAULT_SUBJECT)).strip() or DEFAULT_SUBJECT,
                "goal": str(session.get("goal", "Lernsession")),
                "learned": str(session.get("learned", "")),
                "source_date": str(session.get("date", "")),
            }
        )
        self.data["reviews"] = reviews[-300:]
        save_progress(self.data)
        self.status_text.set(f"Wiederholung gespeichert: {due_day.strftime('%d.%m.%Y')}.")
        self._render_all()

    def _ask_review_schedule(self, session: dict | None) -> None:
        if not session:
            return
        popup = tk.Toplevel(self.root)
        popup.title("Wiederholung planen")
        popup.configure(bg=COLORS["paper"])
        popup.resizable(False, False)
        popup.transient(self.root)

        x = self.root.winfo_rootx() + max(120, self.root.winfo_width() // 2 - 220)
        y = self.root.winfo_rooty() + max(90, self.root.winfo_height() // 2 - 150)
        popup.geometry(f"440x300+{x}+{y}")

        frame = tk.Frame(popup, bg=COLORS["cream"], padx=22, pady=20)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        tk.Label(
            frame,
            text="Wiederholung planen?",
            bg=COLORS["cream"],
            fg=COLORS["ink"],
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w")
        tk.Label(
            frame,
            text=(
                f"{session.get('subject', DEFAULT_SUBJECT)} · "
                f"{self._short_text(str(session.get('goal', 'Lernsession')), 58)}"
            ),
            bg=COLORS["cream"],
            fg=COLORS["muted"],
            font=("Segoe UI", 10),
            justify="left",
            wraplength=380,
        ).pack(anchor="w", pady=(8, 14))

        for label, days in REVIEW_OPTIONS:
            ttk.Button(
                frame,
                text=label,
                style="Secondary.TButton",
                command=lambda d=days: (self._schedule_review(session, d), popup.destroy()),
            ).pack(fill="x", pady=3)

        ttk.Button(
            frame,
            text="Nicht planen",
            style="Primary.TButton",
            command=popup.destroy,
        ).pack(fill="x", pady=(10, 0))

    def open_settings(self) -> None:
        popup = tk.Toplevel(self.root)
        popup.title(self.t("settings"))
        popup.configure(bg=COLORS["paper"])
        popup.resizable(False, False)
        popup.transient(self.root)

        x = self.root.winfo_rootx() + max(120, self.root.winfo_width() // 2 - 180)
        y = self.root.winfo_rooty() + max(90, self.root.winfo_height() // 2 - 130)
        popup.geometry(f"360x350+{x}+{y}")

        frame = tk.Frame(popup, bg=COLORS["cream"], padx=22, pady=20)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        tk.Label(
            frame,
            text=self.t("settings"),
            bg=COLORS["cream"],
            fg=COLORS["ink"],
            font=("Segoe UI", 16, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 16))

        tk.Label(
            frame,
            text=self.t("language"),
            bg=COLORS["cream"],
            fg=COLORS["ink"],
            font=("Segoe UI", 10),
        ).grid(row=1, column=0, sticky="w", pady=(0, 10))

        language_label = tk.StringVar(value=LANGUAGE_LABELS.get(self.language.get(), "Deutsch"))
        language_combo = ttk.Combobox(
            frame,
            textvariable=language_label,
            values=list(LANGUAGE_LABELS.values()),
            state="readonly",
            width=18,
        )
        language_combo.grid(row=1, column=1, sticky="ew", pady=(0, 10))

        # Break Duration Setting
        tk.Label(
            frame,
            text="Pausenlänge",
            bg=COLORS["cream"],
            fg=COLORS["ink"],
            font=("Segoe UI", 10),
        ).grid(row=2, column=0, sticky="w", pady=(0, 10))

        break_duration_label = tk.StringVar(value=f"{self.break_duration_minutes.get()} Min")
        break_duration_combo = ttk.Combobox(
            frame,
            textvariable=break_duration_label,
            values=["5 Min", "10 Min", "15 Min"],
            state="readonly",
            width=18,
        )
        break_duration_combo.grid(row=2, column=1, sticky="ew", pady=(0, 10))

        # Theme Setting
        tk.Label(
            frame,
            text="Farbschema",
            bg=COLORS["cream"],
            fg=COLORS["ink"],
            font=("Segoe UI", 10),
        ).grid(row=3, column=0, sticky="w", pady=(0, 10))

        theme_label = tk.StringVar(value="Dunkel" if self.theme_mode.get() == "dark" else "Hell")
        theme_combo = ttk.Combobox(
            frame,
            textvariable=theme_label,
            values=["Hell", "Dunkel"],
            state="readonly",
            width=18,
        )
        theme_combo.grid(row=3, column=1, sticky="ew", pady=(0, 10))
        frame.grid_columnconfigure(1, weight=1)

        def save_settings() -> None:
            code = LANGUAGE_CODES.get(language_label.get(), "de")
            self.language.set(code)
            self.data["language"] = code

            try:
                mins = int(break_duration_label.get().split()[0])
            except (ValueError, IndexError):
                mins = 5
            self.break_duration_minutes.set(mins)
            self.data["break_duration_minutes"] = mins

            theme_mode = "dark" if theme_label.get() == "Dunkel" else "light"
            self.theme_mode.set(theme_mode)
            self.data["theme_mode"] = theme_mode
            self._apply_theme()

            self.data["daily_goal_hours"] = self._daily_goal_hours()
            self.data["active_subject"] = self._current_subject()
            self._save_current_session()
            self.status_text.set(self.t("language_saved"))
            popup.destroy()

        ttk.Button(
            frame,
            text=self.t("save"),
            style="Primary.TButton",
            command=save_settings,
        ).grid(row=4, column=0, columnspan=2, sticky="ew", pady=(4, 10))

        ttk.Button(
            frame,
            text=self.t("export_csv"),
            style="Secondary.TButton",
            command=lambda: self.export_sessions_csv(parent=popup),
        ).grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        ttk.Button(
            frame,
            text=self.t("reset_all"),
            style="Danger.TButton",
            command=lambda: self.reset_all(parent=popup),
        ).grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        ttk.Button(
            frame,
            text=self.t("close"),
            style="Secondary.TButton",
            command=popup.destroy,
        ).grid(row=7, column=0, columnspan=2, sticky="ew")

        tk.Label(
            frame,
            text=f"{APP_COMPANY} · {DISPLAY_NAME} v{APP_VERSION} · © {APP_PUBLISHER}",
            bg=COLORS["cream"],
            fg=COLORS["muted"],
            font=("Segoe UI", 8),
        ).grid(row=8, column=0, columnspan=2, sticky="w", pady=(14, 0))

    def export_sessions_csv(self, parent=None) -> None:
        sessions = list(self.data.get("sessions", []))
        if not sessions:
            messagebox.showinfo(self.t("export_csv"), self.t("export_empty"), parent=parent or self.root)
            return
        default_name = f"lernreich_sessions_{date.today().isoformat()}.csv"
        path_str = filedialog.asksaveasfilename(
            parent=parent or self.root,
            title=self.t("export_csv"),
            defaultextension=".csv",
            initialfile=default_name,
            filetypes=[("CSV", "*.csv"), ("*", "*.*")],
        )
        if not path_str:
            return
        if self.language.get() == "en":
            headers = ["Date", "Start", "Subject", "Target", "Minutes", "XP", "Status", "Note"]
        else:
            headers = ["Datum", "Start", "Fach", "Ziel", "Minuten", "XP", "Status", "Notiz"]
        try:
            with open(path_str, "w", encoding="utf-8-sig", newline="") as handle:
                writer = csv.writer(handle, delimiter=";")
                writer.writerow(headers)
                for session in sessions:
                    minutes = int(session.get("seconds", 0)) // 60
                    writer.writerow([
                        session.get("date", ""),
                        session.get("started_at", ""),
                        session.get("subject", ""),
                        session.get("goal", ""),
                        minutes,
                        int(session.get("xp", 0)),
                        session.get("status", ""),
                        str(session.get("learned", "")).replace("\n", " ").strip(),
                    ])
        except OSError as exc:
            messagebox.showerror(
                self.t("export_csv"),
                f"{self.t('export_failed')}\n{exc}",
                parent=parent or self.root,
            )
            return
        messagebox.showinfo(
            self.t("export_csv"),
            self.t("export_done").format(count=len(sessions)),
            parent=parent or self.root,
        )

    def switch_view(self, view: str) -> None:
        self.current_view.set(view)
        self._render_all()

    def shift_calendar_month(self, offset: int) -> None:
        month = self.calendar_month + offset
        year = self.calendar_year
        while month < 1:
            month += 12
            year -= 1
        while month > 12:
            month -= 12
            year += 1
        self.calendar_month = month
        self.calendar_year = year
        self.current_view.set("calendar")
        self._render_all()

    def _daily_goal_hours(self) -> float:
        try:
            return max(0.5, min(12.0, float(self.daily_goal_hours.get())))
        except (tk.TclError, ValueError):
            return 2.0

    def _current_learned_text(self) -> str:
        text = self.learned_text.get("1.0", "end").strip()
        return " ".join(text.split())

    def _current_subject(self) -> str:
        subject = " ".join(self.subject_text.get().split())
        return subject or DEFAULT_SUBJECT

    def _clear_learning_note(self) -> None:
        self.learned_text.delete("1.0", "end")

    def _note_file_name(self, timestamp: datetime, status: str) -> str:
        clean_status = "".join(
            char if char.isalnum() or char in ("-", "_") else "_"
            for char in status.lower()
        ).strip("_") or "session"
        return f"{timestamp.strftime('%H-%M-%S')}_{clean_status}.md"

    def _write_learning_note_file(
        self,
        path: Path,
        timestamp: datetime,
        status: str,
        seconds: int,
        xp: int,
        lost_xp: int,
        penalty_percent: int,
        goal: str,
        learned: str,
        subject: str = "",
        abort_reason: str = "",
        abort_note: str = "",
        started_at: datetime | None = None,
        target_minutes: int | None = None,
    ) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "# Lernreich Lernnotiz",
            "",
            f"Datum: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Status: {status}",
            f"Fach: {subject or DEFAULT_SUBJECT}",
            f"Startzeit: {(started_at or timestamp - timedelta(seconds=seconds)).strftime('%Y-%m-%d %H:%M:%S')}",
            f"Zielzeit: {target_minutes or self._clamped_target_minutes()} Minuten",
            f"Dauer: {format_seconds(seconds)}",
            f"XP erhalten: {xp}",
        ]
        if lost_xp:
            lines.append(f"XP verloren: {lost_xp}")
            lines.append(f"Abbruchstrafe: {penalty_percent}%")
        if abort_reason or abort_note:
            lines.extend(["", "## Fokus-Sperre"])
            if abort_reason:
                lines.append(f"Grund: {abort_reason}")
            if abort_note:
                lines.append(f"Notiz: {abort_note}")
        lines.extend(
            [
                "",
                "## Lernziel",
                goal or "-",
                "",
                "## Notizen",
                learned or "-",
                "",
            ]
        )
        path.write_text("\n".join(lines), encoding="utf-8")
        return path

    def _save_active_note_file(self, goal: str, learned: str) -> Path | None:
        if self.session_seconds <= 0 and not learned:
            return None
        timestamp = datetime.now()
        subject = self._current_subject()
        return self._write_learning_note_file(
            active_note_path(),
            timestamp,
            "laufend",
            int(self.session_seconds),
            self._xp_for_seconds(self.session_seconds),
            0,
            0,
            goal,
            learned,
            subject,
            started_at=self.session_started_at,
            target_minutes=self._clamped_target_minutes(),
        )

    def _clear_active_note_file(self) -> None:
        paths = [self.data.get("active_note_file"), str(active_note_path())]
        seen = set()
        for raw_path in paths:
            if not raw_path or raw_path in seen:
                continue
            seen.add(raw_path)
            try:
                Path(raw_path).unlink()
            except FileNotFoundError:
                continue
            except OSError:
                continue

    def _confirm_focus_checklist(self) -> bool:
        popup = tk.Toplevel(self.root)
        popup.title(self.t("focus_checklist"))
        popup.configure(bg=COLORS["paper"])
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()

        x = self.root.winfo_rootx() + max(120, self.root.winfo_width() // 2 - 230)
        y = self.root.winfo_rooty() + max(80, self.root.winfo_height() // 2 - 190)
        popup.geometry(f"460x380+{x}+{y}")

        frame = tk.Frame(popup, bg=COLORS["cream"], padx=22, pady=20)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        tk.Label(
            frame,
            text="Bereit fuer Fokus?",
            bg=COLORS["cream"],
            fg=COLORS["ink"],
            font=("Segoe UI", 17, "bold"),
        ).pack(anchor="w")
        tk.Label(
            frame,
            text=(
                f"{self._current_subject()} · "
                f"{self._short_text(self.goal_text.get().strip() or 'Lernsession', 52)}"
            ),
            bg=COLORS["cream"],
            fg=COLORS["muted"],
            font=("Segoe UI", 10),
            wraplength=390,
            justify="left",
        ).pack(anchor="w", pady=(4, 16))

        checks = []
        for item in FOCUS_CHECKLIST_ITEMS:
            var = tk.BooleanVar(value=False)
            ttk.Checkbutton(frame, text=item, variable=var).pack(anchor="w", pady=5)
            checks.append(var)

        result = {"start": False}

        def start_focus() -> None:
            if not all(var.get() for var in checks):
                self.status_text.set("Bitte erst alle Fokus-Punkte abhaken.")
                return
            result["start"] = True
            popup.destroy()

        buttons = ttk.Frame(frame, style="Panel.TFrame")
        buttons.pack(fill="x", pady=(18, 0))
        buttons.grid_columnconfigure((0, 1), weight=1)
        ttk.Button(
            buttons,
            text="Fokus starten",
            style="Primary.TButton",
            command=start_focus,
        ).grid(row=0, column=0, sticky="ew", padx=(0, 7))
        ttk.Button(
            buttons,
            text=self.t("close"),
            style="Secondary.TButton",
            command=popup.destroy,
        ).grid(row=0, column=1, sticky="ew", padx=(7, 0))

        popup.protocol("WM_DELETE_WINDOW", popup.destroy)
        self.root.wait_window(popup)
        return result["start"]

    def start_new_session_action(self) -> None:
        self.session_seconds = 0
        self.session_started_at = datetime.now()
        self._target_reached_popup_shown = False
        self.toggle_running()

    def resume_session_action(self) -> None:
        self.toggle_running()

    def toggle_running(self) -> None:
        if self.running:
            if self._has_reached_target():
                self.finish_session(automatic=False)
                return
            self.status_text.set(
                "Lernreich haelt dich im Fokus: Ziel erreichen oder bewusst abbrechen."
            )
            self._save_current_session()
            return

        self._clamped_target_minutes()
        if hasattr(self, "checklist_vars"):
            for var in self.checklist_vars:
                var.set(False)
        if hasattr(self, "start_timer_btn"):
            self.start_timer_btn.configure(state="disabled", bg=COLORS["line"], fg=COLORS["muted"])

        now = datetime.now()
        self.running = True
        self.break_available = False
        self.break_running = False
        self.break_seconds = 0.0
        if self.session_seconds <= 0:
            self.session_started_at = now
            self._reminder_checkpoint = 0
            self._target_reached_popup_shown = False
        elif self.session_started_at is None:
            self.session_started_at = now - timedelta(seconds=self.session_seconds)
        self._last_tick = now
        self.status_text.set(
            f"Lernreich laeuft seit {self.session_started_at.strftime('%H:%M')}. "
            f"Ziel: {self._clamped_target_minutes()} min, Maximum: 2 h 30 min."
        )
        self._save_current_session()
        self._render_all()

    def finish_session(self, automatic: bool = False) -> None:
        if self.session_seconds < 10:
            self.status_text.set("Noch zu kurz fuer eine gespeicherte Session.")
            return
        self.running = False
        self.start_button.configure(text=self.t("start"))
        completed_seconds = int(self.session_seconds)
        streak_bonus = self._commit_session()
        mins = self.break_duration_minutes.get()
        bonus = self.break_bonus_xp
        if completed_seconds >= 25 * 60:
            self.break_available = True
            if automatic:
                message = f"Maximale Fokuszeit erreicht: Lernzeit gespeichert. Halte jetzt {mins} Minuten Pause fuer +{bonus} XP."
            else:
                message = f"Ziel beendet: volle XP gespeichert. Halte jetzt {mins} Minuten Pause fuer +{bonus} XP."
        else:
            message = "Ziel beendet: Lernnotiz und volle XP gespeichert."
        if streak_bonus:
            message += f" Streak-Bonus: +{streak_bonus} XP."
        self.status_text.set(message)
        self._render_all()
        self._ask_review_schedule(self._last_completed_session)

    def reset_session(self) -> None:
        self.request_abort_session()

    def request_abort_session(self) -> None:
        if self.session_seconds <= 0 and not self._current_learned_text():
            self.status_text.set("Keine laufende Session zum Abbrechen.")
            return
        if self._has_reached_target():
            self.finish_session(automatic=False)
            return
        self._confirm_abandon_session()

    def _reset_active_session_fields(self) -> None:
        if self.running:
            self.running = False
        self.break_running = False
        self.break_available = False
        self.break_seconds = 0.0
        self.session_seconds = 0
        self.session_started_at = None
        self._target_reached_popup_shown = False
        self._reminder_checkpoint = 0
        self._save_checkpoint = 0
        self._clear_learning_note()
        self.start_button.configure(text=self.t("start"))

    def toggle_break(self) -> None:
        if self.running:
            self.status_text.set("Pause gibt es erst nach einer beendeten Session.")
            return
        if self.break_running:
            self.status_text.set("Pause laeuft. Halte sie bis zum Ende fuer den Bonus.")
            return
        if not self.break_available:
            self.status_text.set("Nach einer Fokus-Session ab 25 Minuten gibt es Pausenbonus.")
            return
        self.break_running = True
        self.break_seconds = 0.0
        self._last_tick = datetime.now()
        mins = self.break_duration_minutes.get()
        self.status_text.set(f"Pause gestartet. {mins} Minuten ruhig bleiben fuer +{mins} XP.")
        self._render_all()

    def _complete_break_bonus(self) -> None:
        self.break_running = False
        self.break_available = False
        self.break_seconds = 0.0
        bonus_xp = self.break_bonus_xp
        self.data["total_xp"] = int(self.data.get("total_xp", 0)) + bonus_xp
        self.data["available_xp"] = int(self.data.get("available_xp", 0)) + bonus_xp
        bonuses = list(self.data.get("break_bonuses", []))
        bonuses.append({"date": datetime.now().strftime("%Y-%m-%d %H:%M"), "xp": bonus_xp})
        self.data["break_bonuses"] = bonuses[-100:]
        save_progress(self.data)
        self.status_text.set(f"Pause eingehalten: +{bonus_xp} XP Bonus.")
        self._render_all()

    def _abandon_penalty(self) -> tuple[int, int, int]:
        raw_xp = self._xp_for_seconds(self.session_seconds)
        if self._has_reached_target():
            return raw_xp, 0, 0
        if self.session_seconds < 180:
            loss_percent = 100
        elif self.session_seconds <= 300:
            loss_percent = 10
        else:
            loss_percent = 80
        lost_xp = min(raw_xp, math.ceil(raw_xp * loss_percent / 100))
        kept_xp = max(0, raw_xp - lost_xp)
        return kept_xp, lost_xp, loss_percent

    def _confirm_abandon_session(self, close_after: bool = False) -> bool:
        kept_xp, lost_xp, loss_percent = self._abandon_penalty()
        raw_xp = self._xp_for_seconds(self.session_seconds)
        minutes = self.session_seconds / 60

        popup = tk.Toplevel(self.root)
        popup.title("Lernreich: bewusst abbrechen")
        popup.configure(bg=COLORS["paper"])
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()

        x = self.root.winfo_rootx() + max(120, self.root.winfo_width() // 2 - 240)
        y = self.root.winfo_rooty() + max(70, self.root.winfo_height() // 2 - 215)
        popup.geometry(f"480x430+{x}+{y}")

        frame = tk.Frame(popup, bg=COLORS["cream"], padx=22, pady=20)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(
            frame,
            text="Lernreich schuetzt deinen Fokus",
            bg=COLORS["cream"],
            fg=COLORS["ink"],
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w")

        message = (
            f"Du hast gerade {minutes:.1f} Minuten gelernt und {raw_xp} XP aufgebaut.\n"
            f"Wenn du jetzt abbrichst, verlierst du {loss_percent}%: "
            f"{lost_xp} XP weg, {kept_xp} XP bleiben."
        )
        tk.Label(
            frame,
            text=message,
            bg=COLORS["cream"],
            fg=COLORS["muted"],
            font=("Segoe UI", 10),
            justify="left",
            wraplength=420,
        ).pack(anchor="w", pady=(12, 10))

        tk.Label(
            frame,
            text="Warum willst du abbrechen?",
            bg=COLORS["cream"],
            fg=COLORS["ink"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")
        reason_var = tk.StringVar(value="")
        reason_combo = ttk.Combobox(
            frame,
            textvariable=reason_var,
            values=ABORT_REASONS,
            state="readonly",
        )
        reason_combo.pack(fill="x", pady=(6, 10))

        tk.Label(
            frame,
            text="Kurzer Grund oder naechster Schritt",
            bg=COLORS["cream"],
            fg=COLORS["ink"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")
        reason_note = tk.StringVar()
        note_entry = ttk.Entry(frame, textvariable=reason_note)
        note_entry.pack(fill="x", pady=(6, 12))

        tk.Label(
            frame,
            text='Tippe "ABBRECHEN", wenn du das bewusst willst.',
            bg=COLORS["cream"],
            fg=COLORS["ink"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")

        phrase = tk.StringVar()
        entry = ttk.Entry(frame, textvariable=phrase)
        entry.pack(fill="x", pady=(6, 14))
        result = {"abandoned": False}

        def keep_learning() -> None:
            popup.destroy()
            self.status_text.set("Gute Entscheidung: Lernreich laeuft weiter.")

        def abandon() -> None:
            abort_reason = reason_var.get().strip()
            if not abort_reason:
                self.status_text.set("Waehle erst einen Abbruchgrund aus.")
                return
            if phrase.get().strip().upper() != "ABBRECHEN":
                self.status_text.set('Zum Abbrechen musst du bewusst "ABBRECHEN" tippen.')
                return
            result["abandoned"] = True
            self._abandon_session(
                kept_xp,
                lost_xp,
                loss_percent,
                abort_reason,
                reason_note.get().strip(),
            )
            popup.destroy()
            if close_after:
                self.root.destroy()

        buttons = ttk.Frame(frame, style="Panel.TFrame")
        buttons.pack(fill="x")
        buttons.grid_columnconfigure((0, 1), weight=1)
        ttk.Button(buttons, text="Weiterlernen", style="Primary.TButton", command=keep_learning).grid(
            row=0, column=0, sticky="ew", padx=(0, 7)
        )
        ttk.Button(buttons, text="XP verlieren", style="Danger.TButton", command=abandon).grid(
            row=0, column=1, sticky="ew", padx=(7, 0)
        )
        entry.focus_set()
        popup.protocol("WM_DELETE_WINDOW", keep_learning)
        self.root.wait_window(popup)
        return result["abandoned"]

    def _abandon_session(
        self,
        kept_xp: int,
        lost_xp: int,
        loss_percent: int,
        abort_reason: str = "",
        abort_note: str = "",
    ) -> None:
        session_length = int(self.session_seconds)
        goal = self.goal_text.get().strip() or "Lernsession"
        learned = self._current_learned_text()
        subject = self._current_subject()
        timestamp = datetime.now()
        started_at = self.session_started_at or timestamp - timedelta(seconds=session_length)
        target_minutes = self._clamped_target_minutes()
        note_path = self._write_learning_note_file(
            notes_day_path(timestamp.date().isoformat())
            / self._note_file_name(timestamp, "bewusst_abgebrochen"),
            timestamp,
            "bewusst abgebrochen",
            session_length,
            kept_xp,
            lost_xp,
            loss_percent,
            goal,
            learned,
            subject,
            abort_reason,
            abort_note,
            started_at=started_at,
            target_minutes=target_minutes,
        )
        self.running = False
        self.data["total_seconds"] = int(self.data.get("total_seconds", 0)) + session_length
        self.data["total_xp"] = int(self.data.get("total_xp", 0)) + kept_xp
        self.data["available_xp"] = int(self.data.get("available_xp", 0)) + kept_xp
        self.data["xp_per_hour"] = XP_PER_HOUR
        self.data["xp_rate"] = XP_RATE_ID
        sessions = list(self.data.get("sessions", []))
        sessions.append(
            {
                "date": timestamp.strftime("%Y-%m-%d %H:%M"),
                "seconds": session_length,
                "xp": kept_xp,
                "lost_xp": lost_xp,
                "penalty_percent": loss_percent,
                "status": "abgebrochen",
                "started_at": started_at.strftime("%Y-%m-%d %H:%M"),
                "target_minutes": target_minutes,
                "subject": subject,
                "goal": goal,
                "learned": learned,
                "abort_reason": abort_reason,
                "abort_note": abort_note,
                "note_file": str(note_path),
            }
        )
        self.data["sessions"] = sessions[-MAX_STORED_SESSIONS:]
        self._clear_active_note_file()
        self.data.pop("active_session_seconds", None)
        self.data.pop("active_session_started_at", None)
        self.data.pop("active_target_minutes", None)
        self.data.pop("active_goal", None)
        self.data.pop("active_learned", None)
        self.data["active_subject"] = subject
        self.data.pop("active_note_file", None)
        save_progress(self.data)
        self._reset_active_session_fields()
        self.status_text.set(
            f"Bewusst abgebrochen ({abort_reason}): {lost_xp} XP verloren, {kept_xp} XP behalten."
        )
        self._render_all()

    def reset_all(self, parent=None) -> None:
        confirmed = messagebox.askyesno(
            "Fortschritt zuruecksetzen",
            self.t("reset_warning"),
            parent=parent or self.root,
        )
        if not confirmed:
            return
        self.running = False
        self.session_seconds = 0
        self._clear_active_note_file()
        self.data = {
            "total_seconds": 0,
            "total_xp": 0,
            "available_xp": 0,
            "spent_xp": 0,
            "village_level": 1,
            "category_levels": default_category_levels(),
            "upgrades": [],
            "break_bonuses": [],
            "streak_bonuses": [],
            "streak_bonus_days": [],
            "current_streak": 0,
            "best_streak": 0,
            "daily_goal_hours": self._daily_goal_hours(),
            "daily_plans": {},
            "reviews": [],
            "active_subject": self._current_subject(),
            "language": self.language.get(),
            "xp_per_hour": XP_PER_HOUR,
            "xp_rate": XP_RATE_ID,
            "sessions": [],
        }
        self._clear_learning_note()
        save_progress(self.data)
        self.start_button.configure(text=self.t("start"))
        self.status_text.set("Alles zurueckgesetzt. Lernreich wartet neu.")
        if parent is not None:
            parent.destroy()
        self._render_all()

    def _next_upgrade_cost(self) -> int | None:
        if self.village_level >= MAX_UPGRADE_LEVEL:
            return None
        return upgrade_cost_for_level(self.village_level)

    def _selected_category(self) -> dict:
        return category_by_name(self.upgrade_category.get())

    def _category_level(self, key: str) -> int:
        return int(self.category_levels.get(key, 0))

    def buy_next_upgrade(self) -> None:
        self.buy_selected_upgrade()

    def buy_selected_upgrade(self) -> None:
        if self.running:
            self.status_text.set("Erst das Fokusziel erreichen, dann Lernreich ausbauen.")
            return
        if self.break_running:
            self.status_text.set("Erst die Pause fertig einhalten, dann ausbauen.")
            return
        cost = self._next_upgrade_cost()
        if cost is None:
            self.status_text.set("Lernreich ist bis Ausbau 100 vollstaendig ausgebaut.")
            return
        category = self._selected_category()
        levels = self.category_levels
        current_category_level = int(levels.get(category["key"], 0))
        if current_category_level >= int(category["max"]):
            self.status_text.set(f"{category['name']} ist in diesem Baum voll ausgebaut.")
            return
        if self.saved_available_xp < cost:
            missing = cost - self.saved_available_xp
            self.status_text.set(f"Noch {missing} XP bis zum naechsten {category['name']}-Upgrade.")
            return

        self.data["available_xp"] = self.saved_available_xp - cost
        self.data["spent_xp"] = int(self.data.get("spent_xp", 0)) + cost
        self.data["village_level"] = self.village_level + 1
        levels[category["key"]] = current_category_level + 1
        self.data["category_levels"] = levels
        upgrades = list(self.data.get("upgrades", []))
        upgrades.append(
            {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "name": category["name"],
                "category": category["key"],
                "category_level": current_category_level + 1,
                "total_level": self.village_level,
                "cost": cost,
            }
        )
        self.data["upgrades"] = upgrades
        save_progress(self.data)
        self.status_text.set(f"{category['name']} ausgebaut: Stufe {current_category_level + 1} fuer {cost} XP.")
        self._render_all()

    def _refresh_upgrade_button(self) -> None:
        cost = self._next_upgrade_cost()
        category = self._selected_category()
        category_level = self._category_level(category["key"])
        if cost is None:
            self.upgrade_button.configure(text="Maximal", state="disabled")
            self.upgrade_info.configure(text="Ausbau 100 erreicht.")
            return
        full = category_level >= int(category["max"])
        state = "normal" if self.saved_available_xp >= cost and not self.running and not self.break_running and not full else "disabled"
        self.upgrade_button.configure(text=f"Upgrade {cost} XP", state=state)
        missing = max(0, cost - self.saved_available_xp)
        self.upgrade_info.configure(
            text=f"{category['name']}: {category_level}/{category['max']} · Ausbau {self.village_level}/{MAX_UPGRADE_LEVEL} · noch {missing} XP"
        )

    def _refresh_view_buttons(self) -> None:
        view = self.current_view.get()
        self.tal_button.configure(style="Primary.TButton" if view == "stats" else "Secondary.TButton")
        self.calendar_button.configure(style="Primary.TButton" if view == "calendar" else "Secondary.TButton")
        self.notes_button.configure(style="Primary.TButton" if view == "notes" else "Secondary.TButton")
        month_state = "normal" if view == "calendar" else "disabled"
        self.prev_month_button.configure(state=month_state)
        self.next_month_button.configure(state=month_state)

    def _refresh_break_button(self) -> None:
        if self.break_running:
            left = max(0, int(self.break_limit_seconds - self.break_seconds))
            self.break_button.configure(text=f"Pause {format_seconds(left)}", state="disabled", bg=COLORS["paper_dark"], fg=COLORS["muted"])
        elif self.break_available:
            self.break_button.configure(text=f"Pause starten (+{self.break_bonus_xp} XP)", state="normal", bg=COLORS["navy"], fg=COLORS["cream"])
        else:
            self.break_button.configure(text=self.t("break_after_focus"), state="disabled", bg=COLORS["paper_dark"], fg=COLORS["muted"])

    def _tick(self) -> None:
        now = datetime.now()
        if self.break_running:
            if self._last_tick is None:
                self._last_tick = now
            delta = (now - self._last_tick).total_seconds()
            if delta > 0:
                self.break_seconds += delta
            self._last_tick = now
            if self.break_seconds >= self.break_limit_seconds:
                self._complete_break_bonus()
        elif self.running:
            if self._last_tick is None:
                self._last_tick = now
            delta = (now - self._last_tick).total_seconds()
            if delta > 0:
                self.session_seconds = min(MAX_SESSION_SECONDS, self.session_seconds + delta)
                self._hourglass_phase += delta
            self._last_tick = now
            if self.session_seconds >= MAX_SESSION_SECONDS:
                self.finish_session(automatic=True)
            else:
                target_popup_shown = self._check_target_reached()
                if not target_popup_shown:
                    self._check_reminders()
                self._auto_save()
        else:
            self._last_tick = now
            self._hourglass_phase += 0.03

        self._render_dynamic()
        visible_minute = self.total_visible_seconds // 60
        if visible_minute != self._last_city_minute:
            self._draw_current_view()
        self.root.after(250, self._tick)

    def _target_seconds(self) -> int:
        return self._clamped_target_minutes() * 60

    def _has_reached_target(self) -> bool:
        return self.session_seconds >= self._target_seconds()

    def _check_target_reached(self) -> bool:
        if self._target_reached_popup_shown or not self._has_reached_target():
            return False
        self._target_reached_popup_shown = True
        self._show_focus_popup(
            "Ziel geschafft",
            (
                f"Du hast {minutes_text(int(self.session_seconds))} gelernt. "
                "Du kannst jetzt Ziel beenden ohne XP-Verlust oder weiterlernen, "
                f"maximal bis {minutes_text(MAX_SESSION_SECONDS)}."
            ),
        )
        return True

    def _auto_save(self) -> None:
        seconds = int(self.session_seconds)
        if seconds - self._save_checkpoint >= 60:
            self._save_checkpoint = seconds
            self._save_current_session()

    def _save_current_session(self) -> None:
        goal = self.goal_text.get().strip()
        learned = self._current_learned_text()
        subject = self._current_subject()
        target_minutes = self._clamped_target_minutes()
        reminder_minutes = self._clamped_reminder_minutes()
        note_path = self._save_active_note_file(goal, learned)
        self.data["active_session_seconds"] = int(self.session_seconds)
        self.data["active_target_minutes"] = target_minutes
        self.data["target_minutes"] = target_minutes
        self.data["reminder_minutes"] = reminder_minutes
        self.data["active_goal"] = goal
        self.data["active_learned"] = learned
        self.data["active_subject"] = subject
        if self.session_started_at is not None:
            self.data["active_session_started_at"] = self.session_started_at.isoformat()
        else:
            self.data.pop("active_session_started_at", None)
        if note_path is not None:
            self.data["active_note_file"] = str(note_path)
        elif "active_note_file" in self.data:
            self.data.pop("active_note_file", None)
        save_progress(self.data)

    def _commit_session(self) -> int:
        session_length = int(self.session_seconds)
        goal = self.goal_text.get().strip() or "Lernsession"
        learned = self._current_learned_text()
        subject = self._current_subject()
        earned_xp = self._xp_for_seconds(session_length)
        timestamp = datetime.now()
        started_at = self.session_started_at or timestamp - timedelta(seconds=session_length)
        target_minutes = self._clamped_target_minutes()
        note_path = self._write_learning_note_file(
            notes_day_path(timestamp.date().isoformat()) / self._note_file_name(timestamp, "beendet"),
            timestamp,
            "beendet",
            session_length,
            earned_xp,
            0,
            0,
            goal,
            learned,
            subject,
            started_at=started_at,
            target_minutes=target_minutes,
        )
        self.data["total_seconds"] = int(self.data.get("total_seconds", 0)) + session_length
        self.data["total_xp"] = int(self.data.get("total_xp", 0)) + earned_xp
        self.data["available_xp"] = int(self.data.get("available_xp", 0)) + earned_xp
        self.data["xp_per_hour"] = XP_PER_HOUR
        self.data["xp_rate"] = XP_RATE_ID
        sessions = list(self.data.get("sessions", []))
        session_record = {
            "date": timestamp.strftime("%Y-%m-%d %H:%M"),
            "seconds": session_length,
            "xp": earned_xp,
            "lost_xp": 0,
            "penalty_percent": 0,
            "status": "beendet",
            "started_at": started_at.strftime("%Y-%m-%d %H:%M"),
            "target_minutes": target_minutes,
            "subject": subject,
            "goal": goal,
            "learned": learned,
            "note_file": str(note_path),
        }
        sessions.append(session_record)
        self._last_completed_session = session_record
        self.data["sessions"] = sessions[-MAX_STORED_SESSIONS:]
        streak_bonus = self._award_streak_bonus_if_earned()
        self._clear_active_note_file()
        self.data.pop("active_session_seconds", None)
        self.data.pop("active_session_started_at", None)
        self.data.pop("active_target_minutes", None)
        self.data.pop("active_goal", None)
        self.data.pop("active_learned", None)
        self.data["active_subject"] = subject
        self.data.pop("active_note_file", None)
        save_progress(self.data)
        self.session_seconds = 0
        self.session_started_at = None
        self._target_reached_popup_shown = False
        self._reminder_checkpoint = 0
        self._save_checkpoint = 0
        self._clear_learning_note()
        return streak_bonus

    def _check_reminders(self) -> None:
        interval = self._clamped_reminder_minutes() * 60
        if self.session_seconds < interval:
            return
        checkpoint = int(self.session_seconds // interval)
        if checkpoint <= self._reminder_checkpoint:
            return
        self._reminder_checkpoint = checkpoint
        self._show_reminder(checkpoint)

    def _show_focus_popup(self, title: str, message: str) -> None:
        popup = tk.Toplevel(self.root)
        popup.title("Fokus-Check")
        popup.configure(bg=COLORS["paper"])
        popup.resizable(False, False)
        popup.attributes("-topmost", True)
        popup.transient(self.root)

        x = self.root.winfo_rootx() + max(120, self.root.winfo_width() // 2 - 190)
        y = self.root.winfo_rooty() + max(100, self.root.winfo_height() // 2 - 90)
        popup.geometry(f"380x190+{x}+{y}")

        frame = tk.Frame(popup, bg=COLORS["cream"], padx=22, pady=20)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(
            frame,
            text=title,
            bg=COLORS["cream"],
            fg=COLORS["ink"],
            font=("Segoe UI", 15, "bold"),
        ).pack(anchor="w")

        tk.Label(
            frame,
            text=message,
            bg=COLORS["cream"],
            fg=COLORS["muted"],
            font=("Segoe UI", 10),
            wraplength=320,
            justify="left",
        ).pack(anchor="w", pady=(10, 16))

        ttk.Button(
            frame,
            text="Weiterlernen",
            style="Primary.TButton",
            command=popup.destroy,
        ).pack(anchor="e")
        popup.after(18000, popup.destroy)

    def _show_reminder(self, checkpoint: int) -> None:
        elapsed_seconds = int(self.session_seconds)
        target_seconds = self._target_seconds()
        remaining_seconds = max(0, target_seconds - elapsed_seconds)
        elapsed = minutes_text(elapsed_seconds)
        start_text = self.session_started_at.strftime("%H:%M") if self.session_started_at else "jetzt"
        if remaining_seconds > 0:
            message = (
                f"Wir sind jetzt bei {elapsed}. "
                f"Es bleiben noch {minutes_text(remaining_seconds)} bis zum Ziel. "
                f"Startzeit: {start_text}."
            )
        else:
            message = (
                f"Geschafft: {elapsed}. Du bist ueber deinem Ziel und kannst ohne XP-Verlust beenden."
            )
        extra = REMINDER_MESSAGES[(checkpoint - 1) % len(REMINDER_MESSAGES)]
        self._show_focus_popup(f"Geschafft: {elapsed}", f"{message}\n\n{extra}")

    def _render_all(self) -> None:
        self._render_dynamic()
        self._draw_current_view()
        self._draw_journal()

    def _draw_current_view(self) -> None:
        view = self.current_view.get()
        self._update_sidebar_nav()
        if view == "timer":
            self.city_pane.grid_remove()
            self.timer_pane.grid(row=0, column=0, sticky="nsew", padx=22, pady=(16, 12))
            
            # Switch between Setup and Active frames dynamically based on running state only
            if self.running or self.break_running:
                self.timer_setup_frame.grid_remove()
                self.timer_active_frame.grid(row=0, column=0, sticky="nsew")
                self.active_subject_lbl.configure(text=self._current_subject())
            else:
                self.timer_active_frame.grid_remove()
                self.timer_setup_frame.grid(row=0, column=0, sticky="nsew")
        else:
            self.timer_pane.grid_remove()
            self.city_pane.grid(row=0, column=0, sticky="nsew", padx=22, pady=(16, 12))
            if view == "calendar":
                self._draw_calendar()
            elif view == "notes":
                self._draw_notes_center()
            else:
                self._draw_stats_center()

    def _render_dynamic(self) -> None:
        self._update_session_buttons()
        self.timer_label.configure(text=format_seconds(self.session_seconds))
        total_seconds = self.total_visible_seconds
        self.total_label.configure(text=f"Gesamt: {minutes_text(total_seconds)}")
        total_xp = self.total_visible_xp
        self.xp_label.configure(text=f"XP: {self.saved_available_xp} frei")
        today_seconds = self._seconds_for_day(date.today())
        self.today_label.configure(text=f"Heute: {minutes_text(today_seconds)} / {self._daily_goal_hours():g} Std")
        current_streak, best_streak = self._streak_counts(include_active=True)
        stored_best = max(best_streak, int(self.data.get("best_streak", 0)))
        self.streak_label.configure(
            text=f"Streak: {current_streak} Tage · Rekord {stored_best} · ab 10 min/Tag"
        )
        if hasattr(self, "sidebar_streak_lbl"):
            self.sidebar_streak_lbl.configure(text=f"Streak: {current_streak} Tage")
            self._draw_streak_preview()
        if hasattr(self, "xp_sidebar_canvas"):
            self._draw_sidebar_xp()

        target_seconds = self._target_seconds()
        target_percent = min(1.0, self.session_seconds / target_seconds)
        self._draw_progress(target_percent)
        self._draw_hourglass(target_percent)

        week_seconds = self._week_seconds(date.today())
        week_goal_seconds = int(self._daily_goal_hours() * 3600 * 7)
        week_percent = 0 if week_goal_seconds <= 0 else min(100, int(week_seconds / week_goal_seconds * 100))
        self.next_label.configure(
            text=f"Diese Woche: {minutes_text(week_seconds)} / {minutes_text(week_goal_seconds)} ({week_percent}%)"
        )
        kept_xp, lost_xp, loss_percent = self._abandon_penalty()
        if self._has_reached_target() and self.session_seconds >= 10:
            self.penalty_label.configure(text="Ziel erreicht: Beenden ist jetzt ohne XP-Verlust moeglich.")
        elif self.session_seconds >= 10:
            self.penalty_label.configure(
                text=f"Lernreich-Regel bei Abbruch: -{loss_percent}% ({lost_xp} XP weg, {kept_xp} XP bleiben)"
            )
        else:
            self.penalty_label.configure(text="Lernreich-Regel: 3-5 min -10%, danach -80% bei Abbruch.")
        note_count = len(self._note_entries(include_active=False))
        if self.current_view.get() == "notes":
            self.city_summary.configure(
                text=f"{note_count} gespeicherte Notizen · Tagesordner: {notes_day_path()}"
            )
            self.focus_summary_label.configure(
                text="Notizen werden automatisch beim Merken, Beenden oder Abbrechen gespeichert."
            )
        else:
            self.city_summary.configure(
                text=(
                    f"Heute {minutes_text(today_seconds)} · Woche {minutes_text(week_seconds)} · "
                    f"{total_xp} XP gesamt · {self.saved_available_xp} XP frei · Fach {self._current_subject()}"
                )
            )
            self.focus_summary_label.configure(
                text=f"Tagesziel {self._daily_goal_hours():g} Std · Wochenfortschritt {week_percent}% · Streak {current_streak} Tage · Rekord {stored_best}"
            )

    def _update_session_buttons(self) -> None:
        if not hasattr(self, "start_button"):
            return
        if self.running:
            if self._has_reached_target():
                self.start_button.configure(text=self.t("finish_goal"), bg=COLORS["success"], fg=COLORS["cream"])
                if hasattr(self, "abort_button"):
                    self.abort_button.configure(text=self.t("finish_goal"), bg=COLORS["success"], fg=COLORS["cream"])
            else:
                self.start_button.configure(text=self.t("running"), bg=COLORS["navy"], fg=COLORS["cream"])
                if hasattr(self, "abort_button"):
                    self.abort_button.configure(text=self.t("aware_abort"), bg=COLORS["paper_dark"], fg=COLORS["ink"])
        else:
            self.start_button.configure(text=self.t("start"), bg=COLORS["navy"], fg=COLORS["cream"])
            if hasattr(self, "abort_button"):
                self.abort_button.configure(text=self.t("aware_abort"), bg=COLORS["paper_dark"], fg=COLORS["ink"])
            if hasattr(self, "start_timer_btn"):
                self.start_timer_btn.configure(state="normal", bg=COLORS["navy"], fg=COLORS["cream"])
        
        # Dual-action buttons: show resume button dynamically if there is a leftover session
        if hasattr(self, "resume_timer_btn") and hasattr(self, "start_timer_btn"):
            if self.session_seconds > 0 and not self.running:
                self.resume_timer_btn.grid(row=0, column=1, sticky="ew", padx=(6, 0))
                self.start_timer_btn.grid(row=0, column=0, sticky="ew", padx=(0, 6), columnspan=1)
                formatted_time = format_seconds(self.session_seconds)
                self.resume_timer_btn.configure(text=f"🔄  Sitzung fortsetzen ({formatted_time})")
            else:
                self.resume_timer_btn.grid_remove()
                self.start_timer_btn.grid(row=0, column=0, sticky="ew", padx=0, columnspan=2)

        self._refresh_view_buttons()
        self._refresh_break_button()

    def _draw_progress(self, percent: float) -> None:
        canvas = self.progress_canvas
        canvas.delete("all")
        width = max(260, canvas.winfo_width())
        height = max(46, canvas.winfo_height())
        x0, y0 = 4, 15
        x1, y1 = width - 4, 31
        canvas.create_rectangle(x0, y0, x1, y1, fill=COLORS["paper_dark"], outline=COLORS["line"])
        canvas.create_rectangle(
            x0,
            y0,
            x0 + (x1 - x0) * percent,
            y1,
            fill=COLORS["gold"],
            outline=COLORS["gold"],
        )
        target = self._clamped_target_minutes()
        label = "Ziel erreicht - frei beenden" if percent >= 1.0 else f"Sitzungsziel: {target} min"
        canvas.create_text(
            x0,
            5,
            text=label,
            anchor="w",
            fill=COLORS["muted"],
            font=("Segoe UI", 8),
        )
        canvas.create_text(
            x1,
            40,
            text=f"{int(percent * 100)}%",
            anchor="e",
            fill=COLORS["muted"],
            font=("Segoe UI", 8),
        )

    def _draw_hourglass(self, percent: float) -> None:
        c = self.hourglass_canvas
        c.delete("all")
        w = int(c.winfo_width() or 214)
        h = int(c.winfo_height() or 200)
        cx = w / 2
        top_y = 15
        bottom_y = h - 25
        neck_y = h / 2
        
        # Glossy metallic/glass shades
        glass_border = "#94a3b8"  # Slate metal
        glass_shadow = "#e2e8f0"  # Subtle reflection
        glass_glow = "#f8fafc"    # Light refraction
        glass_glow_2 = "#f1f5f9"  # Inner light
        
        # Exquisite glowing Indigo/Violet sand palette
        sand_glow = "#3b52e2"     # Glowing royal Indigo
        sand_core = "#3144be"     # Deep core shadow
        sand_sparkle = "#818cf8"  # Sparkling violet highlight
        sand_glare = "#ffffff"    # Glaring bright sand particle
        
        wood = "#111215"          # Charcoal plates
        
        top_wide = 48
        neck_half = 6
        top_glass_y = top_y + 12
        bottom_glass_y = bottom_y - 12

        # 1. Soft layered drop shadow
        c.create_oval(cx - 65, bottom_y + 8, cx + 65, bottom_y + 16, fill="#eaeae6", outline="")
        c.create_oval(cx - 50, bottom_y + 10, cx + 50, bottom_y + 15, fill="#deded9", outline="")

        # 2. Sleek metal side columns with chrome bases & caps
        for side in (-1, 1):
            x_col = cx + side * 62
            # Chrome column caps
            c.create_rectangle(x_col - 5, top_y + 8, x_col + 5, top_y + 14, fill="#cbd5e1", outline="#94a3b8")
            c.create_rectangle(x_col - 5, bottom_y - 14, x_col + 5, bottom_y - 8, fill="#cbd5e1", outline="#94a3b8")
            # Sleek dark steel cylinders
            c.create_rectangle(x_col - 3, top_y + 14, x_col + 3, bottom_y - 14, fill="#1e2025", outline="")
            c.create_rectangle(x_col - 1, top_y + 14, x_col + 1, bottom_y - 14, fill="#475569", outline="")

        # 3. Premium Charcoal wooden endplates (rounded 3D bevels)
        c.create_oval(cx - 68, top_y, cx + 68, top_y + 10, fill=wood, outline="")
        c.create_rectangle(cx - 68, top_y + 5, cx + 68, top_y + 10, fill=wood, outline="")
        c.create_oval(cx - 68, bottom_y - 10, cx + 68, bottom_y, fill=wood, outline="")
        c.create_rectangle(cx - 68, bottom_y - 10, cx + 68, bottom_y - 5, fill=wood, outline="")

        # 4. Premium three-dimensional glass bulbs (glowing polygon refractions)
        c.create_polygon(
            cx - top_wide, top_glass_y,
            cx + top_wide, top_glass_y,
            cx + neck_half, neck_y,
            cx - neck_half, neck_y,
            fill=glass_glow, outline=""
        )
        c.create_polygon(
            cx - neck_half, neck_y,
            cx + neck_half, neck_y,
            cx + top_wide, bottom_glass_y,
            cx - top_wide, bottom_glass_y,
            fill=glass_glow_2, outline=""
        )
        
        # 5. Smooth curved glass bulb outlines
        c.create_line(
            cx - top_wide, top_glass_y,
            cx - 36, top_glass_y + 25,
            cx - 15, neck_y - 15,
            cx - neck_half, neck_y,
            fill=glass_border, width=3, smooth=True
        )
        c.create_line(
            cx + top_wide, top_glass_y,
            cx + 36, top_glass_y + 25,
            cx + 15, neck_y - 15,
            cx + neck_half, neck_y,
            fill=glass_border, width=3, smooth=True
        )
        c.create_line(
            cx - neck_half, neck_y,
            cx - 15, neck_y + 15,
            cx - 36, bottom_glass_y - 25,
            cx - top_wide, bottom_glass_y,
            fill=glass_border, width=3, smooth=True
        )
        c.create_line(
            cx + neck_half, neck_y,
            cx + 15, neck_y + 15,
            cx + 36, bottom_glass_y - 25,
            cx + top_wide, bottom_glass_y,
            fill=glass_border, width=3, smooth=True
        )
        
        # 6. Glowing glass glare curves
        c.create_line(cx - 32, top_glass_y + 10, cx - 12, neck_y - 12, fill="#ffffff", width=2, smooth=True)
        c.create_line(cx + 28, bottom_glass_y - 10, cx + 12, neck_y + 12, fill="#ffffff", width=2, smooth=True)
        c.create_line(cx - 24, top_glass_y + 24, cx - 14, neck_y - 20, fill=glass_shadow, width=1, smooth=True)

        upper_fill = max(0.0, min(1.0, 1.0 - percent))
        lower_fill = max(0.0, min(1.0, percent))

        # 7. Upper chamber sand (with rippling surface physics)
        upper_chamber_h = neck_y - top_glass_y - 6
        surface_y = neck_y - upper_chamber_h * upper_fill
        surface_half = neck_half + (top_wide - neck_half) * upper_fill
        
        if upper_fill > 0.015:
            # Active organic surface wave
            slope = 3 * math.sin(self._hourglass_phase * 2.2) if self.running else 0
            c.create_polygon(
                cx - surface_half, surface_y + slope,
                cx + surface_half, surface_y - slope,
                cx + neck_half - 1, neck_y - 4,
                cx - neck_half + 1, neck_y - 4,
                fill=sand_glow, outline=""
            )
            # Surface core shadow
            c.create_polygon(
                cx - surface_half + 4, surface_y + slope + 2,
                cx + surface_half - 4, surface_y - slope + 2,
                cx + neck_half - 1, neck_y - 4,
                cx - neck_half + 1, neck_y - 4,
                fill=sand_core, outline=""
            )
            # Glowing ripple highlight line
            c.create_line(
                cx - surface_half + 2, surface_y + slope,
                cx + surface_half - 2, surface_y - slope,
                fill=sand_sparkle, width=2
            )
            # Sparkling falling grains inside upper chamber
            rng = random.Random(888 + int(percent * 500))
            for _ in range(8):
                gx = rng.uniform(cx - surface_half * 0.7, cx + surface_half * 0.7)
                gy = rng.uniform(surface_y + 4, neck_y - 8)
                c.create_oval(gx - 1, gy - 1, gx + 1, gy + 1, fill=sand_glare, outline="")

        # 8. Lower chamber sand (beautiful organic growing dome)
        pile_base_y = bottom_glass_y - 4
        lower_chamber_h = bottom_glass_y - neck_y - 6
        pile_h = lower_chamber_h * 0.8 * lower_fill
        pile_half = neck_half + (top_wide - neck_half) * lower_fill
        
        if lower_fill > 0.015:
            # Organic rounded dome
            c.create_oval(
                cx - pile_half, pile_base_y - pile_h * 0.5 - 4,
                cx + pile_half, pile_base_y + 4,
                fill=sand_glow, outline=""
            )
            c.create_polygon(
                cx - pile_half, pile_base_y,
                cx + pile_half, pile_base_y,
                cx, pile_base_y - pile_h,
                fill=sand_glow, outline=""
            )
            # Dome core shadow
            c.create_polygon(
                cx - pile_half * 0.7, pile_base_y - 1,
                cx + pile_half * 0.7, pile_base_y - 1,
                cx, pile_base_y - pile_h + 3,
                fill=sand_core, outline=""
            )
            # Top-glowing highlight arc
            c.create_arc(
                cx - pile_half, pile_base_y - pile_h * 0.5 - 4,
                cx + pile_half, pile_base_y + 4,
                start=0, extent=180,
                fill=sand_sparkle, outline=""
            )
            # Sparkle overlay inside the lower dome
            rng = random.Random(777 + int(percent * 500))
            for _ in range(int(3 + lower_fill * 12)):
                gx = rng.uniform(cx - pile_half * 0.6, cx + pile_half * 0.6)
                max_gy = pile_base_y - (pile_h * (1.0 - abs(gx - cx) / (pile_half + 0.1)))
                gy = rng.uniform(max_gy, pile_base_y)
                c.create_oval(gx - 1, gy - 1, gx + 1, gy + 1, fill=sand_glare, outline="")

        # 9. Ultra cascading falling sand stream (with ripples & particles)
        if self.running and upper_fill > 0.01:
            stream_top = neck_y - 4
            stream_bottom = max(stream_top + 10, pile_base_y - pile_h - 2)
            # Glowing core line
            c.create_line(cx, stream_top, cx, stream_bottom, fill=sand_glow, width=3)
            c.create_line(cx, stream_top + 4, cx, stream_bottom - 2, fill=sand_sparkle, width=1)
            
            # Spark particles with realistic gravitational wobble
            span = max(10, stream_bottom - stream_top)
            phase = (self._hourglass_phase * 60) % span
            for i in range(12):
                dot_y = stream_top + ((phase + i * 8) % span)
                wobble = math.sin((self._hourglass_phase * 5.0) + i * 0.8) * 1.5
                color = sand_glare if i % 2 == 0 else sand_sparkle
                c.create_oval(cx + wobble - 1, dot_y - 1, cx + wobble + 1, dot_y + 1, fill=color, outline="")
        elif upper_fill <= 0.01:
            c.create_oval(cx - 2, neck_y - 2, cx + 2, neck_y + 2, fill=sand_sparkle, outline="")

        target_seconds = self._target_seconds()
        remaining_seconds = max(0, target_seconds - int(self.session_seconds))
        footer = "Ziel erreicht" if remaining_seconds <= 0 else f"Bis Ziel: {minutes_text(remaining_seconds)}"
        c.create_text(
            cx,
            h - 9,
            text=footer,
            fill=COLORS["muted"],
            font=("Segoe UI", 9),
        )

    def _note_entries(self, include_active: bool = True) -> list[dict]:
        entries = []
        if include_active:
            learned = self._current_learned_text()
            goal = self.goal_text.get().strip()
            if learned or self.session_seconds > 0:
                entries.append(
                    {
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "seconds": int(self.session_seconds),
                        "xp": self._xp_for_seconds(self.session_seconds),
                        "status": self.t("active_note"),
                        "subject": self._current_subject(),
                        "goal": goal or "Lernsession",
                        "learned": learned or "Noch keine Notiz geschrieben.",
                        "note_file": str(self.data.get("active_note_file") or active_note_path()),
                    }
                )

        for session in reversed(list(self.data.get("sessions", []))):
            learned = str(session.get("learned", "")).strip()
            goal = str(session.get("goal", "")).strip()
            note_file = str(session.get("note_file", "")).strip()
            if not learned and not goal and not note_file:
                continue
            entries.append(
                {
                    "date": str(session.get("date", "")),
                    "seconds": int(session.get("seconds", 0)),
                    "xp": int(session.get("xp", 0)),
                    "lost_xp": int(session.get("lost_xp", 0)),
                    "status": str(session.get("status", "beendet")),
                    "subject": str(session.get("subject", DEFAULT_SUBJECT)).strip() or DEFAULT_SUBJECT,
                    "goal": goal or "Lernsession",
                    "learned": learned or "-",
                    "abort_reason": str(session.get("abort_reason", "")).strip(),
                    "abort_note": str(session.get("abort_note", "")).strip(),
                    "note_file": note_file,
                }
            )
        return entries

    def _draw_notes_center(self) -> None:
        c = self.city_canvas
        c.delete("all")
        width = max(600, int(c.winfo_width()))
        height = max(360, int(c.winfo_height()))
        self._last_city_minute = self.total_visible_seconds // 60
        bg_fill = COLORS["paper"]
        c.create_rectangle(0, 0, width, height, fill=bg_fill, outline="")

        margin = 24
        c.create_text(
            margin,
            26,
            text=self.t("notes_title"),
            anchor="w",
            fill=COLORS["ink"],
            font=("Segoe UI", 18, "bold"),
        )
        c.create_text(
            margin,
            52,
            text=self.t("notes_hint"),
            anchor="w",
            fill=COLORS["muted"],
            font=("Segoe UI", 10),
        )
        folder = str(notes_day_path())
        folder_text = folder if len(folder) <= 86 else "..." + folder[-83:]
        c.create_text(
            margin,
            76,
            text=f"Tagesordner: {folder_text}",
            anchor="w",
            fill=COLORS["muted"],
            font=("Segoe UI", 8),
        )

        entries = self._note_entries()
        if not entries:
            c.create_rectangle(margin, 108, width - margin, 214, fill="#ffffff", outline="#e3e6eb")
            c.create_text(
                margin + 18,
                154,
                text=self.t("notes_empty"),
                anchor="w",
                width=width - margin * 2 - 36,
                fill=COLORS["muted"],
                font=("Segoe UI", 11),
            )
            return

        top = 106
        gap = 12
        card_h = 92
        max_cards = max(2, min(6, int((height - top - 18) // (card_h + gap))))
        for index, entry in enumerate(entries[:max_cards]):
            y = top + index * (card_h + gap)
            x1 = margin
            x2 = width - margin
            accent = COLORS["gold"] if entry.get("status") == self.t("active_note") else COLORS["success"]
            if str(entry.get("status")) == "abgebrochen":
                accent = COLORS["brick"]
            c.create_rectangle(x1, y, x2, y + card_h, fill="#ffffff", outline="#e3e6eb")
            c.create_rectangle(x1, y, x1 + 5, y + card_h, fill=accent, outline=accent)
            meta = (
                f"{entry.get('date', '')} · {entry.get('subject', DEFAULT_SUBJECT)} · "
                f"{minutes_text(int(entry.get('seconds', 0)))} · "
                f"+{int(entry.get('xp', 0))} XP"
            )
            lost_xp = int(entry.get("lost_xp", 0) or 0)
            if lost_xp:
                meta += f" · -{lost_xp} XP"
            c.create_text(x1 + 16, y + 17, text=meta, anchor="w", fill=COLORS["muted"], font=("Segoe UI", 8))
            c.create_text(
                x2 - 16,
                y + 17,
                text=str(entry.get("status", "")),
                anchor="e",
                fill=accent,
                font=("Segoe UI", 8, "bold"),
            )
            c.create_text(
                x1 + 16,
                y + 42,
                text=f"Ziel: {self._short_text(str(entry.get('goal', 'Lernsession')), 78)}",
                anchor="w",
                width=x2 - x1 - 32,
                fill=COLORS["ink"],
                font=("Segoe UI", 10, "bold"),
            )
            c.create_text(
                x1 + 16,
                y + 70,
                text=(
                    f"Grund: {entry.get('abort_reason')} · " if entry.get("abort_reason") else ""
                )
                + f"Notiz: {self._short_text(str(entry.get('learned', '-')), 140)}",
                anchor="w",
                width=x2 - x1 - 32,
                fill=COLORS["muted"],
                font=("Segoe UI", 9),
            )

        hidden_count = max(0, len(entries) - max_cards)
        if hidden_count:
            c.create_text(
                width - margin,
                height - 12,
                text=f"+{hidden_count} weitere Notizen im Ordner",
                anchor="e",
                fill=COLORS["muted"],
                font=("Segoe UI", 8),
            )

    def _draw_stats_center(self) -> None:
        c = self.city_canvas
        c.delete("all")
        width = max(600, int(c.winfo_width()))
        height = max(360, int(c.winfo_height()))
        self._last_city_minute = self.total_visible_seconds // 60

        c.create_rectangle(0, 0, width, height, fill=COLORS["paper"], outline="")
        today = date.today()
        totals = self._daily_totals()
        today_key = today.isoformat()
        today_seconds = int(totals.get(today_key, {}).get("seconds", 0))
        today_xp = int(totals.get(today_key, {}).get("xp", 0))
        week_start = self._week_start(today)
        week_days = [week_start + timedelta(days=i) for i in range(7)]
        week_seconds = sum(int(totals.get(day.isoformat(), {}).get("seconds", 0)) for day in week_days)
        daily_goal_seconds = max(1, int(self._daily_goal_hours() * 3600))
        current_streak, best_streak = self._streak_counts(include_active=True)
        best_streak = max(best_streak, int(self.data.get("best_streak", 0)))
        total_seconds = self.total_visible_seconds

        margin = 26
        gap = 14
        tile_w = (width - margin * 2 - gap * 3) / 4
        tile_y = 22
        tile_h = 80

        def draw_tile(index: int, title: str, value: str, sub: str, accent: str) -> None:
            x = margin + index * (tile_w + gap)
            c.create_rectangle(x, tile_y, x + tile_w, tile_y + tile_h, fill=COLORS["cream"], outline=COLORS["line"], width=1)
            c.create_oval(x + 16, tile_y + 20, x + 25, tile_y + 29, fill=accent, outline="")
            c.create_text(x + 33, tile_y + 25, text=title, anchor="w", fill=COLORS["muted"], font=("Segoe UI", 9))
            c.create_text(x + 16, tile_y + 51, text=value, anchor="w", fill=COLORS["ink"], font=("Segoe UI", 19, "bold"))
            c.create_text(x + 16, tile_y + 69, text=sub, anchor="w", fill=COLORS["muted"], font=("Segoe UI", 8))

        today_percent = min(100, int(today_seconds / daily_goal_seconds * 100))
        draw_tile(0, "HEUTE", minutes_text(today_seconds), f"{today_percent}% vom Tagesziel", COLORS["gold"])
        draw_tile(1, "DIESE WOCHE", minutes_text(week_seconds), f"+{today_xp} XP heute", COLORS["success"])
        draw_tile(2, "STREAK", f"{current_streak} Tage", f"Rekord {best_streak} Tage", COLORS["brick"])
        draw_tile(3, "GESAMT", minutes_text(total_seconds), f"{self.saved_available_xp} XP frei", COLORS["slate"])

        chart_y = tile_y + tile_h + 18
        panel_w = width - margin * 2
        bottom_fits = height >= chart_y + 158 + 104
        if bottom_fits:
            chart_h = max(150, height - chart_y - 120)
        else:
            chart_h = max(150, height - chart_y - 20)
        c.create_rectangle(margin, chart_y, margin + panel_w, chart_y + chart_h, fill=COLORS["cream"], outline=COLORS["line"], width=1)
        c.create_text(margin + 18, chart_y + 22, text="Lern-Aktivitaet", anchor="w", fill=COLORS["ink"], font=("Segoe UI", 13, "bold"))
        c.create_text(margin + panel_w - 18, chart_y + 22, text=f"{minutes_text(week_seconds)} diese Woche", anchor="e", fill=COLORS["muted"], font=("Segoe UI", 9))

        weeks = 18
        grid_left = margin + 18 + 24
        grid_top = chart_y + 46
        grid_right = margin + panel_w - 18
        grid_bottom = chart_y + chart_h - 28
        cell = min((grid_right - grid_left - (weeks - 1) * 3) / weeks, (grid_bottom - grid_top - 6 * 3) / 7)
        cell = max(8.0, min(17.0, cell))
        cgap = 3
        heat = ["#eceef2", "#cdebd6", "#93d7ac", "#4fb37e", "#1f9d57"]
        start_day = week_start - timedelta(weeks=weeks - 1)
        for row, lbl in ((0, "Mo"), (2, "Mi"), (4, "Fr")):
            ly = grid_top + row * (cell + cgap) + cell / 2
            c.create_text(grid_left - 7, ly, text=lbl, anchor="e", fill=COLORS["muted"], font=("Segoe UI", 8))
        last_month = None
        for col in range(weeks):
            first = start_day + timedelta(days=col * 7)
            if first.month != last_month and first.day <= 7:
                c.create_text(grid_left + col * (cell + cgap), grid_top - 12, text=MONTH_NAMES[first.month][:3], anchor="w", fill=COLORS["muted"], font=("Segoe UI", 8))
                last_month = first.month
            for row in range(7):
                day = start_day + timedelta(days=col * 7 + row)
                if day > today:
                    continue
                seconds = int(totals.get(day.isoformat(), {}).get("seconds", 0))
                if seconds <= 0:
                    level = 0
                else:
                    frac = seconds / daily_goal_seconds
                    level = 4 if frac >= 1.0 else 3 if frac >= 0.6 else 2 if frac >= 0.25 else 1
                x1 = grid_left + col * (cell + cgap)
                y1 = grid_top + row * (cell + cgap)
                c.create_rectangle(x1, y1, x1 + cell, y1 + cell, fill=heat[level], outline="")
        legend_x = margin + panel_w - 18 - (5 * 15) - 36
        legend_y = grid_bottom + 16
        c.create_text(legend_x - 8, legend_y, text="weniger", anchor="e", fill=COLORS["muted"], font=("Segoe UI", 8))
        for i, col_color in enumerate(heat):
            lxx = legend_x + i * 15
            c.create_rectangle(lxx, legend_y - 6, lxx + 11, legend_y + 6, fill=col_color, outline="")
        c.create_text(legend_x + 5 * 15 + 2, legend_y, text="mehr", anchor="w", fill=COLORS["muted"], font=("Segoe UI", 8))

        bottom_y = chart_y + chart_h + 14
        if bottom_y + 72 <= height:
            sessions = list(self.data.get("sessions", []))
            finished = sum(1 for session in sessions if session.get("status") != "abgebrochen")
            aborted = sum(1 for session in sessions if session.get("status") == "abgebrochen")
            due_reviews, upcoming_reviews = self._review_counts()
            note_count = sum(1 for session in sessions if str(session.get("learned", "")).strip())
            avg_seconds = 0
            if sessions:
                avg_seconds = sum(int(session.get("seconds", 0)) for session in sessions) // max(1, len(sessions))
            left_x1 = margin
            left_x2 = width * 0.52
            right_x1 = left_x2 + 12
            right_x2 = width - margin
            c.create_rectangle(left_x1, bottom_y, left_x2, height - 20, fill="#ffffff", outline="#e3e6eb")
            c.create_text(left_x1 + 16, bottom_y + 22, text="Session-Auswertung", anchor="w", fill=COLORS["ink"], font=("Segoe UI", 13, "bold"))
            summary = (
                f"{finished} beendet · {aborted} bewusst abgebrochen · "
                f"{note_count} Notizen · {due_reviews} Wdh. faellig · Schnitt {minutes_text(avg_seconds)}"
            )
            c.create_text(left_x1 + 16, bottom_y + 50, text=summary, anchor="w", width=left_x2 - left_x1 - 32, fill=COLORS["muted"], font=("Segoe UI", 10))

            plan_items = self._plan_for_day(today)
            done_count = sum(1 for item in plan_items if item.get("done"))
            c.create_rectangle(right_x1, bottom_y, right_x2, height - 20, fill="#ffffff", outline="#e3e6eb")
            c.create_text(right_x1 + 16, bottom_y + 22, text="Tagesplanung", anchor="w", fill=COLORS["ink"], font=("Segoe UI", 13, "bold"))
            if plan_items:
                c.create_text(
                    right_x2 - 16,
                    bottom_y + 22,
                    text=f"{done_count}/{len(plan_items)}",
                    anchor="e",
                    fill=COLORS["success"] if done_count == len(plan_items) else COLORS["gold_dark"],
                    font=("Segoe UI", 9, "bold"),
                )
                plan_text = " · ".join(
                    f"{'OK' if item.get('done') else 'offen'}: {self._short_text(item.get('text', ''), 24)}"
                    for item in plan_items
                )
            else:
                plan_text = "Noch keine Ziele fuer heute. Klick auf Tagesplanung."
            c.create_text(right_x1 + 16, bottom_y + 50, text=plan_text, anchor="w", width=right_x2 - right_x1 - 32, fill=COLORS["muted"], font=("Segoe UI", 10))

    def _draw_city(self) -> None:
        c = self.city_canvas
        c.delete("all")
        width = max(600, int(c.winfo_width()))
        height = max(360, int(c.winfo_height()))
        seconds = self.total_visible_seconds
        minutes = int(seconds // 60)
        xp = self.total_visible_xp
        upgrade_level = self.village_level
        levels = self.category_levels
        self._last_city_minute = minutes

        self._draw_map_ground(c, width, height, upgrade_level)
        self._draw_mountains(c, width, height, upgrade_level)
        self._draw_fields(c, width, height, levels["fields"])
        self._draw_rivers(c, width, height, levels["bridge"])
        self._draw_village_paths(c, width, height, minutes)

        plots = self._topdown_plots(width, height)
        building_count = min(len(plots), max(1, 1 + levels["houses"] // 2))
        for i, plot in enumerate(plots[:building_count]):
            self._draw_village_house(c, i, plot, levels["houses"], xp)

        if levels["mill"] > 0:
            self._draw_watermill(c, width, height, levels["mill"])
        if levels["library"] > 0:
            self._draw_library_marker(c, width, height, levels["library"])
        if levels["mage_tower"] > 0:
            self._draw_mage_tower(c, width, height, levels["mage_tower"])
        if levels["castle"] > 0:
            self._draw_keep(c, width, height, levels["castle"])

        self._draw_village_square(c, width, height, minutes)
        self._draw_topdown_trees(c, width, height, minutes + upgrade_level * 6)
        self._draw_villagers(c, width, height, upgrade_level)
        self._draw_map_badge(c, xp, minutes)

    def _draw_map_ground(self, c: tk.Canvas, width: int, height: int, level: int) -> None:
        c.create_rectangle(0, 0, width, height, fill="#b8d98d", outline="")
        for y in range(0, height, 42):
            color = "#c5e29b" if (y // 42) % 2 == 0 else "#b9d98d"
            c.create_rectangle(0, y, width, y + 42, fill=color, outline="")

        rng = random.Random(4200 + level)
        for _ in range(42):
            x = rng.randint(0, width)
            y = rng.randint(0, height)
            if y < height * 0.20:
                continue
            blade = rng.choice(["#8fbd6b", "#a8ce7c", "#d3e6a5"])
            c.create_line(x, y, x + rng.randint(-2, 2), y - rng.randint(3, 6), fill=blade, width=1)

    def _draw_mountains(self, c: tk.Canvas, width: int, height: int, level: int) -> None:
        base_y = max(82, height * 0.20)
        peaks = [
            (-32, base_y, width * 0.13, 20, width * 0.30),
            (width * 0.20, base_y + 3, width * 0.36, 16, width * 0.52),
            (width * 0.48, base_y + 1, width * 0.66, 10, width * 0.86),
            (width * 0.76, base_y + 5, width * 0.90, 28, width + 42),
        ]
        for i, (x1, by, px, py, x2) in enumerate(peaks):
            shade = ["#627861", "#6f856f", "#5f775f", "#78906f"][i]
            c.create_polygon(x1, by, px, py, x2, by, fill=shade, outline="#4d624f")
            snow = max(18, 34 - level * 2)
            c.create_polygon(
                px,
                py,
                px - snow,
                py + snow * 1.25,
                px - 3,
                py + snow * 0.82,
                px + snow * 0.42,
                py + snow * 1.35,
                fill="#efe8d5",
                outline="",
            )
        c.create_rectangle(0, base_y - 1, width, base_y + 22, fill="#90b574", outline="")

    def _draw_rivers(self, c: tk.Canvas, width: int, height: int, level: int) -> None:
        main = [
            -20,
            height * 0.70,
            width * 0.16,
            height * 0.66,
            width * 0.30,
            height * 0.72,
            width * 0.48,
            height * 0.69,
            width * 0.66,
            height * 0.74,
            width * 0.82,
            height * 0.72,
            width + 26,
            height * 0.78,
        ]
        c.create_line(*main, fill="#6fa7bb", width=30, smooth=True, capstyle="round")
        c.create_line(*main, fill="#9fd0da", width=20, smooth=True, capstyle="round")
        c.create_line(*main, fill="#d4eef0", width=3, smooth=True, dash=(12, 18))

        if level >= 7:
            side = [
                width * 0.86,
                height * 0.20,
                width * 0.80,
                height * 0.34,
                width * 0.76,
                height * 0.49,
                width * 0.70,
                height * 0.64,
            ]
            c.create_line(*side, fill="#78b0c0", width=16, smooth=True, capstyle="round")
            c.create_line(*side, fill="#b8dfe6", width=8, smooth=True, capstyle="round")

        if level >= 1:
            bridge_x = width * 0.48
            bridge_y = height * 0.69
            c.create_rectangle(bridge_x - 34, bridge_y - 11, bridge_x + 34, bridge_y + 11, fill="#9b714b", outline="#5a3d2b", width=2)
            for offset in range(-24, 28, 12):
                c.create_line(bridge_x + offset, bridge_y - 12, bridge_x + offset + 7, bridge_y + 12, fill="#5a3d2b")

    def _draw_village_paths(self, c: tk.Canvas, width: int, height: int, minutes: int) -> None:
        path = "#c7a979"
        light = "#ead7ad"
        cx = width / 2
        cy = height * 0.50
        roads = [
            [width * 0.12, height * 0.58, width * 0.30, height * 0.52, cx, cy, width * 0.76, height * 0.44],
            [cx, height * 0.26, cx, cy, width * 0.50, height * 0.66],
        ]
        for road in roads:
            c.create_line(*road, fill=path, width=11, smooth=True, capstyle="round")
            c.create_line(*road, fill=light, width=3, smooth=True, capstyle="round")

    def _draw_village_square(self, c: tk.Canvas, width: int, height: int, minutes: int) -> None:
        cx = width / 2
        cy = height * 0.50
        plaza_w = min(132, width * 0.18)
        plaza_h = min(86, height * 0.18)
        x1 = cx - plaza_w / 2
        y1 = cy - plaza_h / 2
        x2 = cx + plaza_w / 2
        y2 = cy + plaza_h / 2
        c.create_oval(x1 - 5, y1 - 5, x2 + 5, y2 + 5, fill="#c8a978", outline="#896a42", width=2)
        c.create_oval(x1 + 12, y1 + 10, x2 - 12, y2 - 10, fill="#e5cea1", outline="#a17b4f")
        c.create_oval(cx - 13, cy - 8, cx + 13, cy + 18, fill="#78aabb", outline="#4f7d8a", width=2)
        c.create_rectangle(cx - 4, y1 + 8, cx + 4, cy - 8, fill="#704a32", outline="#3d281e")
        c.create_polygon(cx - 17, y1 + 18, cx, y1 + 2, cx + 17, y1 + 18, fill="#b84f3c", outline="#6e332b")

    def _topdown_plots(self, width: int, height: int) -> list[tuple[float, float, float, float]]:
        cx = width / 2
        cy = height * 0.50
        specs = [
            (-120, -48, 56, 42),
            (92, -50, 58, 42),
            (-92, 42, 54, 40),
            (104, 40, 56, 40),
            (-190, -12, 58, 42),
            (180, -10, 58, 42),
            (-150, 88, 56, 40),
            (140, 86, 54, 40),
            (-238, 72, 58, 42),
            (230, 68, 58, 42),
            (-245, -72, 56, 40),
            (246, -70, 56, 40),
        ]
        plots = []
        for dx, dy, w, h in specs:
            x = min(max(28, cx + dx - w / 2), width - w - 28)
            y = min(max(height * 0.24, cy + dy - h / 2), height * 0.64)
            plots.append((x, y, w, h))
        return plots

    def _draw_village_house(
        self,
        c: tk.Canvas,
        index: int,
        plot: tuple[float, float, float, float],
        level: int,
        xp: int,
    ) -> None:
        x, y, w, h = plot
        walls = "#d7bc86" if index % 4 else "#c7a879"
        roof = ["#874734", "#9d5c35", "#704c34", "#a84f3d"][index % 4]
        trim = "#402c22"
        c.create_rectangle(x + 4, y + 5, x + w + 4, y + h + 5, fill="#7e8f61", outline="")
        c.create_rectangle(x, y + h * 0.22, x + w, y + h, fill=walls, outline=trim, width=2)
        c.create_polygon(
            x - 5,
            y + h * 0.24,
            x + w / 2,
            y - h * 0.12,
            x + w + 5,
            y + h * 0.24,
            fill=roof,
            outline=trim,
            width=2,
        )
        c.create_line(x + 5, y + h * 0.25, x + w - 5, y + h * 0.25, fill="#d99b62", width=2)
        c.create_rectangle(x + w * 0.42, y + h * 0.62, x + w * 0.58, y + h, fill="#5c3d2b", outline=trim)
        c.create_rectangle(x + 8, y + h * 0.42, x + 18, y + h * 0.55, fill="#f5d98b", outline=trim)
        if w > 52:
            c.create_rectangle(x + w - 20, y + h * 0.42, x + w - 10, y + h * 0.55, fill="#f5d98b", outline=trim)
        if xp + index * 2 >= 18:
            c.create_rectangle(x + w - 13, y - 18, x + w - 6, y + 3, fill="#5b4030", outline=trim)
            c.create_rectangle(x + w - 16, y - 23, x + w - 3, y - 17, fill="#d6c7a5", outline=trim)
        if level >= 3 and index % 5 == 0:
            c.create_rectangle(x - 8, y + h + 3, x + w + 8, y + h + 8, fill="#8a5e3b", outline="")

    def _draw_watermill(self, c: tk.Canvas, width: int, height: int, level: int) -> None:
        x = width * 0.26
        y = height * 0.61
        w = 84
        h = 54
        c.create_rectangle(x + 4, y + 5, x + w + 4, y + h + 5, fill="#6b8b68", outline="")
        c.create_rectangle(x, y + 18, x + w, y + h, fill="#c9a978", outline="#412d22", width=2)
        c.create_polygon(x - 6, y + 20, x + w / 2, y - 8, x + w + 6, y + 20, fill="#8c4c36", outline="#412d22", width=2)
        wheel_cx = x - 10
        wheel_cy = y + 35
        c.create_oval(wheel_cx - 18, wheel_cy - 18, wheel_cx + 18, wheel_cy + 18, outline="#5a3b28", width=4)
        for angle in range(0, 180, 45):
            dx = math.cos(math.radians(angle)) * 17
            dy = math.sin(math.radians(angle)) * 17
            c.create_line(wheel_cx - dx, wheel_cy - dy, wheel_cx + dx, wheel_cy + dy, fill="#5a3b28", width=2)
        if level >= 3:
            c.create_rectangle(x + 12, y + h + 4, x + w - 12, y + h + 11, fill="#9e7148", outline="#5a3b28")

    def _draw_market(self, c: tk.Canvas, width: int, height: int) -> None:
        cx = width * 0.63
        cy = height * 0.47
        colors = ["#b84f3c", "#e0c56d", "#6a8f71"]
        for i, dx in enumerate([-36, 36, 0]):
            x = cx + dx
            y = cy + (26 if dx else -30)
            c.create_rectangle(x - 22, y - 8, x + 22, y + 18, fill="#d7bc86", outline="#5b4030")
            c.create_polygon(x - 26, y - 8, x, y - 28, x + 26, y - 8, fill=colors[i], outline="#5b4030")
            c.create_line(x - 17, y + 18, x - 17, y + 30, fill="#5b4030", width=2)
            c.create_line(x + 17, y + 18, x + 17, y + 30, fill="#5b4030", width=2)

    def _draw_library_marker(self, c: tk.Canvas, width: int, height: int, level: int) -> None:
        x = width * 0.61
        y = height * 0.57
        w = 74 + min(28, level * 2)
        h = 44
        c.create_rectangle(x + 4, y + 5, x + w + 4, y + h + 5, fill="#7c8c62", outline="")
        c.create_rectangle(x, y + 12, x + w, y + h, fill="#d8bd86", outline="#4d3528", width=2)
        c.create_polygon(x - 5, y + 13, x + w / 2, y - 10, x + w + 5, y + 13, fill="#6b4634", outline="#4d3528", width=2)
        for i in range(3):
            bx = x + 16 + i * 18
            c.create_rectangle(bx, y + 22, bx + 8, y + 34, fill="#eef1f5", outline="#4d3528")

    def _draw_mage_tower(self, c: tk.Canvas, width: int, height: int, level: int) -> None:
        x = width * 0.36
        y = height * 0.29
        h = 58 + min(34, level * 3)
        w = 34
        c.create_rectangle(x + 4, y + 5, x + w + 4, y + h + 5, fill="#71845f", outline="")
        c.create_rectangle(x, y + 18, x + w, y + h, fill="#8a8f92", outline="#3f3d35", width=2)
        c.create_polygon(x - 8, y + 19, x + w / 2, y - 12, x + w + 8, y + 19, fill="#4d5f84", outline="#303a55", width=2)
        c.create_oval(x + 10, y + 34, x + 24, y + 48, fill="#d9edf0", outline="#3f3d35")

    def _draw_keep(self, c: tk.Canvas, width: int, height: int, level: int) -> None:
        x = width * 0.75
        y = height * 0.31
        size = 78
        c.create_rectangle(x + 5, y + 6, x + size + 5, y + size + 6, fill="#7a866c", outline="")
        c.create_rectangle(x, y, x + size, y + size, fill="#9f9a88", outline="#3f3d35", width=2)
        for px in [x, x + size - 17]:
            c.create_rectangle(px, y - 14, px + 17, y + 8, fill="#8b8677", outline="#3f3d35")
        c.create_rectangle(x + size * 0.42, y + size * 0.55, x + size * 0.58, y + size, fill="#4b3b30", outline="#2e261f")
        if level >= 5:
            c.create_polygon(x + size * 0.28, y, x + size * 0.50, y - 28, x + size * 0.72, y, fill="#8c4c36", outline="#3f3d35")

    def _draw_fields(self, c: tk.Canvas, width: int, height: int, field_level: int) -> None:
        if field_level < 1:
            return
        fields = [
            (24, height * 0.70, width * 0.18, height * 0.18),
            (width * 0.78, height * 0.73, width * 0.17, height * 0.16),
        ]
        visible_fields = fields[: 1 if field_level < 8 else 2]
        for idx, (x, y, w, h) in enumerate(visible_fields):
            c.create_rectangle(x, y, x + w, y + h, fill="#d1b86d" if idx == 0 else "#a9c879", outline="#7d7042", width=2)
            step = 12
            for offset in range(6, int(w + h), step):
                c.create_line(x + offset, y, x, y + offset, fill="#8f7d46")
            c.create_rectangle(x - 6, y - 6, x + w + 6, y + h + 6, outline="#8a5e3b", width=2)

    def _draw_topdown_trees(self, c: tk.Canvas, width: int, height: int, minutes: int) -> None:
        tree_count = min(38, 12 + minutes // 4)
        for i in range(tree_count):
            rng = random.Random(7000 + i)
            x = rng.randint(22, max(24, width - 24))
            y = rng.randint(22, max(24, height - 24))
            if y < height * 0.22:
                continue
            if height * 0.64 < y < height * 0.80 and width * 0.08 < x < width * 0.92:
                continue
            if abs(x - width / 2) < width * 0.20 and abs(y - height * 0.50) < height * 0.20:
                continue
            r = rng.randint(7, 13)
            c.create_oval(x - r, y - r, x + r, y + r, fill="#4f8a43", outline="#3d6e35")
            c.create_oval(x - r * 0.6, y - r * 1.2, x + r * 0.8, y + r * 0.2, fill="#6aa653", outline="")
            c.create_oval(x - 3, y - 3, x + 3, y + 3, fill="#6b452e", outline="")

    def _draw_villagers(self, c: tk.Canvas, width: int, height: int, upgrade_level: int) -> None:
        people = min(10, upgrade_level + 1)
        for i in range(people):
            rng = random.Random(9000 + i)
            x = width / 2 + rng.randint(-120, 120)
            y = height * 0.50 + rng.randint(-64, 64)
            color = ["#315d85", "#8a4f46", "#6a8f71", "#a67b36"][i % 4]
            c.create_oval(x - 4, y - 4, x + 4, y + 4, fill=color, outline=COLORS["ink"])
            c.create_line(x, y + 4, x, y + 11, fill=COLORS["ink"], width=1)

    def _draw_map_badge(self, c: tk.Canvas, xp: int, minutes: int) -> None:
        c.create_rectangle(16, 14, 172, 60, fill="#fff7df", outline="#9f8556")
        c.create_text(28, 27, text=f"{self.saved_available_xp} XP frei", anchor="w", fill=COLORS["ink"], font=("Segoe UI", 12, "bold"))
        c.create_text(28, 46, text=f"{minutes} Lernmin. · Ausbau {self.village_level}/{MAX_UPGRADE_LEVEL}", anchor="w", fill=COLORS["muted"], font=("Segoe UI", 8))

    def _daily_totals(self, include_active: bool = True, completed_only: bool = False) -> dict[str, dict[str, int]]:
        totals: dict[str, dict[str, int]] = {}
        for session in self.data.get("sessions", []):
            if completed_only and session.get("status") == "abgebrochen":
                continue
            day = str(session.get("date", ""))[:10]
            if len(day) != 10:
                continue
            totals.setdefault(day, {"seconds": 0, "xp": 0, "bonus": 0})
            totals[day]["seconds"] += int(session.get("seconds", 0))
            totals[day]["xp"] += int(session.get("xp", 0))
        if not completed_only:
            for bonus in self.data.get("break_bonuses", []):
                day = str(bonus.get("date", ""))[:10]
                if len(day) != 10:
                    continue
                totals.setdefault(day, {"seconds": 0, "xp": 0, "bonus": 0, "streak_bonus": 0})
                totals[day].setdefault("bonus", 0)
                totals[day]["xp"] += int(bonus.get("xp", 0))
                totals[day]["bonus"] += int(bonus.get("xp", 0))
            for bonus in self.data.get("streak_bonuses", []):
                day = str(bonus.get("date", ""))[:10]
                if len(day) != 10:
                    continue
                totals.setdefault(day, {"seconds": 0, "xp": 0, "bonus": 0, "streak_bonus": 0})
                totals[day].setdefault("streak_bonus", 0)
                totals[day]["xp"] += int(bonus.get("xp", 0))
                totals[day]["streak_bonus"] += int(bonus.get("xp", 0))
        if include_active and self.session_seconds > 0:
            day = date.today().isoformat()
            totals.setdefault(day, {"seconds": 0, "xp": 0, "bonus": 0, "streak_bonus": 0})
            totals[day]["seconds"] += int(self.session_seconds)
            totals[day]["xp"] += self._xp_for_seconds(int(self.session_seconds))
        return totals

    def _subject_totals(self, day_keys: set[str] | None = None, include_active: bool = True) -> dict[str, dict[str, int]]:
        totals: dict[str, dict[str, int]] = {}
        for session in self.data.get("sessions", []):
            day = str(session.get("date", ""))[:10]
            if day_keys is not None and day not in day_keys:
                continue
            subject = str(session.get("subject", DEFAULT_SUBJECT)).strip() or DEFAULT_SUBJECT
            totals.setdefault(subject, {"seconds": 0, "xp": 0, "sessions": 0})
            totals[subject]["seconds"] += int(session.get("seconds", 0))
            totals[subject]["xp"] += int(session.get("xp", 0))
            totals[subject]["sessions"] += 1
        if include_active and self.session_seconds > 0:
            day = date.today().isoformat()
            if day_keys is None or day in day_keys:
                subject = self._current_subject()
                totals.setdefault(subject, {"seconds": 0, "xp": 0, "sessions": 0})
                totals[subject]["seconds"] += int(self.session_seconds)
                totals[subject]["xp"] += self._xp_for_seconds(int(self.session_seconds))
                totals[subject]["sessions"] += 1
        return totals

    def _top_subject_text(self, day_keys: set[str] | None = None, include_active: bool = True) -> str:
        totals = self._subject_totals(day_keys=day_keys, include_active=include_active)
        if not totals:
            return "noch kein Fach"
        subject, info = max(totals.items(), key=lambda item: (item[1].get("seconds", 0), item[1].get("xp", 0)))
        return f"{subject} ({minutes_text(int(info.get('seconds', 0)))})"

    def _seconds_for_day(self, day: date) -> int:
        return int(self._daily_totals().get(day.isoformat(), {}).get("seconds", 0))

    def _week_start(self, day: date) -> date:
        return day - timedelta(days=day.weekday())

    def _week_seconds(self, day: date) -> int:
        totals = self._daily_totals()
        start = self._week_start(day)
        return sum(
            int(totals.get((start + timedelta(days=i)).isoformat(), {}).get("seconds", 0))
            for i in range(7)
        )

    def _week_report(self) -> dict:
        today = date.today()
        start = self._week_start(today)
        days = [start + timedelta(days=i) for i in range(7)]
        day_keys = {day.isoformat() for day in days}
        totals = self._daily_totals()
        daily_goal_seconds = int(self._daily_goal_hours() * 3600)
        week_goal_seconds = max(1, daily_goal_seconds * 7)
        week_seconds = sum(int(totals.get(day.isoformat(), {}).get("seconds", 0)) for day in days)
        week_xp = sum(int(totals.get(day.isoformat(), {}).get("xp", 0)) for day in days)
        goal_days = sum(1 for day in days if int(totals.get(day.isoformat(), {}).get("seconds", 0)) >= daily_goal_seconds)
        best_day = max(days, key=lambda day: int(totals.get(day.isoformat(), {}).get("seconds", 0)))
        best_day_seconds = int(totals.get(best_day.isoformat(), {}).get("seconds", 0))
        sessions = [
            session
            for session in self.data.get("sessions", [])
            if str(session.get("date", ""))[:10] in day_keys
        ]
        top_subject = self._top_subject_text(day_keys=day_keys, include_active=True)
        finished = [session for session in sessions if session.get("status") != "abgebrochen"]
        aborted = [session for session in sessions if session.get("status") == "abgebrochen"]
        note_count = sum(1 for session in sessions if str(session.get("learned", "")).strip())
        avg_seconds = 0
        if sessions:
            avg_seconds = sum(int(session.get("seconds", 0)) for session in sessions) // len(sessions)

        reasons: dict[str, int] = {}
        for session in aborted:
            reason = str(session.get("abort_reason", "")).strip()
            if reason:
                reasons[reason] = reasons.get(reason, 0) + 1
        top_reason = "keiner" if not reasons else max(reasons.items(), key=lambda item: item[1])[0]

        plan_total = 0
        plan_done = 0
        for day in days:
            for item in self._plan_for_day(day):
                plan_total += 1
                if item.get("done"):
                    plan_done += 1
        due_reviews, upcoming_reviews = self._review_counts()

        week_percent = min(100, int(week_seconds / week_goal_seconds * 100))
        return {
            "range": f"{start.strftime('%d.%m.%Y')} bis {(start + timedelta(days=6)).strftime('%d.%m.%Y')}",
            "lines": [
                ("Lernzeit", f"{minutes_text(week_seconds)} von {minutes_text(week_goal_seconds)} ({week_percent}%)"),
                ("XP", f"{week_xp} XP diese Woche"),
                ("Top-Fach", top_subject),
                ("Tagesziele", f"{goal_days}/7 Tage erreicht"),
                ("Bester Tag", f"{WEEKDAY_NAMES[best_day.weekday()]} mit {minutes_text(best_day_seconds)}"),
                ("Sessions", f"{len(finished)} beendet, {len(aborted)} abgebrochen"),
                ("Schnitt", minutes_text(avg_seconds)),
                ("Notizen", f"{note_count} gespeicherte Lernnotizen"),
                ("Planung", f"{plan_done}/{plan_total} Tagesziele erledigt" if plan_total else "noch keine Tagesplanung"),
                ("Wiederholen", f"{due_reviews} faellig, {upcoming_reviews} geplant"),
                ("Abbruchgrund", top_reason),
            ],
            "note": "Tipp: Plane vor dem Start 1-3 Ziele. Wenn du abbrechen willst, waehle bewusst einen Grund aus. So siehst du spaeter, was deinen Fokus wirklich stoert.",
        }

    def _qualifying_streak_days(self, include_active: bool = False) -> set[str]:
        totals = self._daily_totals(include_active=include_active, completed_only=True)
        return {
            day
            for day, info in totals.items()
            if int(info.get("seconds", 0)) >= STREAK_MIN_SECONDS
        }

    def _streak_counts(self, include_active: bool = False) -> tuple[int, int]:
        qualifying = self._qualifying_streak_days(include_active=include_active)
        if not qualifying:
            return 0, 0

        today = date.today()
        if today.isoformat() in qualifying:
            anchor = today
        elif (today - timedelta(days=1)).isoformat() in qualifying:
            anchor = today - timedelta(days=1)
        else:
            anchor = None

        current = 0
        if anchor is not None:
            cursor = anchor
            while cursor.isoformat() in qualifying:
                current += 1
                cursor -= timedelta(days=1)

        best = 0
        run = 0
        previous = None
        for day_text in sorted(qualifying):
            current_day = date.fromisoformat(day_text)
            if previous is not None and current_day == previous + timedelta(days=1):
                run += 1
            else:
                run = 1
            best = max(best, run)
            previous = current_day
        return current, best

    def _award_streak_bonus_if_earned(self) -> int:
        today_key = date.today().isoformat()
        awarded_days = set(self.data.get("streak_bonus_days", []))
        current, best = self._streak_counts(include_active=False)
        self.data["current_streak"] = current
        self.data["best_streak"] = max(int(self.data.get("best_streak", 0)), best)

        if today_key in awarded_days or today_key not in self._qualifying_streak_days(include_active=False):
            return 0

        bonus = min(STREAK_BONUS_CAP_XP, STREAK_BONUS_BASE_XP + max(0, current - 1) * STREAK_BONUS_STEP_XP)
        self.data["total_xp"] = int(self.data.get("total_xp", 0)) + bonus
        self.data["available_xp"] = int(self.data.get("available_xp", 0)) + bonus
        awarded_days.add(today_key)
        self.data["streak_bonus_days"] = sorted(awarded_days)[-400:]
        bonuses = list(self.data.get("streak_bonuses", []))
        bonuses.append(
            {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "xp": bonus,
                "streak": current,
            }
        )
        self.data["streak_bonuses"] = bonuses[-400:]
        return bonus

    def _draw_calendar(self) -> None:
        c = self.city_canvas
        c.delete("all")
        width = max(320, int(c.winfo_width() or 600))
        height = int(c.winfo_height() or 360)
        bg_fill = COLORS["paper"]
        c.create_rectangle(0, 0, width, height, fill=bg_fill, outline="")

        compact = height < 430
        tiny = height < 330
        title = f"{MONTH_NAMES[self.calendar_month]} {self.calendar_year}"
        title_y = 16 if tiny else (20 if compact else 26)
        left = 14 if tiny else (18 if compact else 26)
        c.create_text(
            left,
            title_y,
            text=title,
            anchor="w",
            fill=COLORS["ink"],
            font=("Segoe UI", 14 if tiny else (16 if compact else 20), "bold"),
        )
        goal_hours = self._daily_goal_hours()
        c.create_text(
            left,
            34 if tiny else (42 if compact else 52),
            text=f"Ziel: {goal_hours:g} Std · Gruen=geschafft · S=Streak · Gold=Bonus",
            anchor="w",
            fill=COLORS["muted"],
            font=("Segoe UI", 8 if compact else 9),
        )

        totals = self._daily_totals()
        streak_days = self._qualifying_streak_days(include_active=True)
        goal_seconds = max(1, int(goal_hours * 3600))
        month_days = cal.Calendar(firstweekday=0).monthdatescalendar(self.calendar_year, self.calendar_month)
        top = 58 if tiny else (70 if compact else 86)
        gap = 3 if tiny else (4 if compact else 8)
        rows = max(1, len(month_days))
        cell_w = (width - left * 2 - gap * 6) / 7
        cell_h = max(22, (height - top - 10 - gap * (rows - 1)) / rows)
        very_compact = cell_h < 48

        for i, name in enumerate(WEEKDAY_NAMES):
            x = left + i * (cell_w + gap)
            c.create_text(
                x + 5,
                top - 12,
                text=name,
                anchor="w",
                fill=COLORS["muted"],
                font=("Segoe UI", 8 if compact else 9, "bold"),
            )

        today = date.today()
        for row, week in enumerate(month_days):
            for col, day in enumerate(week):
                x1 = left + col * (cell_w + gap)
                y1 = top + row * (cell_h + gap)
                x2 = x1 + cell_w
                y2 = y1 + cell_h
                key = day.isoformat()
                info = totals.get(key, {"seconds": 0, "xp": 0, "bonus": 0})
                in_month = day.month == self.calendar_month
                complete = info["seconds"] >= goal_seconds
                
                if self.theme_mode.get() == "dark":
                    fill = "#1a3a22" if complete else "#1e1f24"
                    if not in_month:
                        fill = "#121316"
                else:
                    fill = "#dbecc6" if complete else "#ffffff"
                    if not in_month:
                        fill = "#eee6d6"
                        
                outline = COLORS["gold"] if day == today else COLORS["line"]
                c.create_rectangle(x1, y1, x2, y2, fill=fill, outline=outline, width=2 if day == today else 1)
                c.create_text(
                    x1 + 6,
                    y1 + 8,
                    text=str(day.day),
                    anchor="w",
                    fill=COLORS["ink"],
                    font=("Segoe UI", 9 if compact else 11, "bold"),
                )
                if info["seconds"]:
                    if very_compact:
                        c.create_text(
                            x1 + 6,
                            y1 + max(17, cell_h - 7),
                            text=f"{int(info['seconds'] // 60)}m",
                            anchor="w",
                            fill=COLORS["muted"],
                            font=("Segoe UI", 7),
                        )
                    else:
                        c.create_text(
                            x1 + 7,
                            y1 + 27,
                            text=f"{int(info['seconds'] // 60)} min",
                            anchor="w",
                            fill=COLORS["muted"],
                            font=("Segoe UI", 8),
                        )
                        c.create_text(
                            x1 + 7,
                            y1 + min(cell_h - 10, 43),
                            text=f"{info['xp']} XP",
                            anchor="w",
                            fill=COLORS["success"] if complete else COLORS["gold_dark"],
                            font=("Segoe UI", 8, "bold"),
                        )
                if key in streak_days:
                    c.create_text(
                        x2 - 12,
                        y1 + 12,
                        text="S",
                        fill=COLORS["danger"],
                        font=("Segoe UI", 8 if compact else 9, "bold"),
                    )
                if info.get("bonus", 0):
                    c.create_oval(x2 - 18, y1 + 8, x2 - 9, y1 + 17, fill=COLORS["gold"], outline="")
                if info.get("streak_bonus", 0):
                    c.create_rectangle(x2 - 18, y2 - 13, x2 - 8, y2 - 5, fill=COLORS["danger"], outline="")

    def _draw_sky(self, c: tk.Canvas, width: int, height: int) -> None:
        for i in range(18):
            ratio = i / 17
            r = int(248 - ratio * 20)
            g = int(242 - ratio * 22)
            b = int(232 - ratio * 25)
            color = f"#{r:02x}{g:02x}{b:02x}"
            y0 = int(height * ratio * 0.75)
            y1 = int(height * (i + 1) / 17 * 0.75)
            c.create_rectangle(0, y0, width, y1, fill=color, outline=color)
        c.create_oval(width - 100, 34, width - 42, 92, fill="#f4d37f", outline="")
        for x, y, w in [(62, 72, 86), (240, 44, 112), (width - 280, 104, 96)]:
            c.create_oval(x, y, x + w, y + 22, fill="#f7f8fa", outline="")
            c.create_oval(x + 32, y - 10, x + w + 24, y + 18, fill="#f7f8fa", outline="")

    def _draw_old_lawn(self, c: tk.Canvas, width: int, height: int, ground_y: int) -> None:
        c.create_rectangle(0, ground_y, width, height, fill="#dfe8d6", outline="")
        c.create_polygon(
            0,
            ground_y + 20,
            width,
            ground_y - 8,
            width,
            ground_y + 44,
            0,
            ground_y + 70,
            fill="#c7d8bf",
            outline="",
        )
        c.create_rectangle(0, ground_y + 82, width, height, fill="#d7ccb6", outline="")
        c.create_polygon(
            width * 0.43,
            ground_y + 16,
            width * 0.57,
            ground_y + 16,
            width * 0.64,
            height,
            width * 0.36,
            height,
            fill="#c2ad8d",
            outline="",
        )
        for line in range(6):
            y = ground_y + 96 + line * 26
            c.create_line(0, y, width, y - 28, fill="#b9aa91", width=1)

    def _city_plots(self, width: int, ground_y: int, count: int) -> list[tuple[float, float]]:
        usable = width - 60
        base_w = max(38, min(70, usable / max(count, 1)))
        plots = []
        for i in range(count):
            x = 30 + i * (usable / max(count, 1)) + 3
            plot_w = base_w * (0.82 + (i % 3) * 0.08)
            if abs((x + plot_w / 2) - width * 0.50) < width * 0.13:
                continue
            plots.append((x, plot_w))
        return plots

    def _draw_building(
        self,
        c: tk.Canvas,
        index: int,
        x: float,
        y: float,
        w: float,
        h: float,
        rng: random.Random,
        minutes: int,
    ) -> None:
        palette = [COLORS["slate"], COLORS["brick"], COLORS["clay"], COLORS["sage"], COLORS["navy_light"]]
        fill = palette[index % len(palette)]
        outline = COLORS["ink"]
        c.create_rectangle(x + 5, y + 8, x + w + 5, y + h + 8, fill=COLORS["shadow"], outline="")

        roof_type = index % 4
        if roof_type == 0:
            c.create_rectangle(x, y, x + w, y + h, fill=fill, outline=outline, width=1)
            c.create_polygon(x - 2, y, x + w / 2, y - 22, x + w + 2, y, fill="#794f42", outline=outline)
        elif roof_type == 1:
            c.create_rectangle(x, y, x + w, y + h, fill=fill, outline=outline, width=1)
            c.create_rectangle(x - 4, y - 10, x + w + 4, y, fill=COLORS["gold_dark"], outline=outline)
        elif roof_type == 2:
            c.create_rectangle(x, y + 14, x + w, y + h, fill=fill, outline=outline, width=1)
            c.create_arc(x, y - 20, x + w, y + 48, start=0, extent=180, fill=fill, outline=outline)
        else:
            c.create_rectangle(x, y, x + w, y + h, fill=fill, outline=outline, width=1)
            c.create_polygon(x, y, x + w * 0.72, y - 16, x + w, y, fill="#6e4d3e", outline=outline)

        rows = max(2, int(h // 32))
        cols = max(2, int(w // 20))
        light_seed = minutes + index * 7
        for row in range(rows):
            for col in range(cols):
                wx = x + 9 + col * ((w - 18) / max(cols, 1))
                wy = y + 22 + row * ((h - 42) / max(rows - 1, 1))
                lit = (row + col + light_seed) % 3 != 0
                color = "#f5d98b" if lit else "#d9d1bd"
                c.create_rectangle(wx, wy, wx + 8, wy + 11, fill=color, outline="#2d3544")

        door_w = min(18, w * 0.32)
        c.create_rectangle(
            x + w / 2 - door_w / 2,
            y + h - 28,
            x + w / 2 + door_w / 2,
            y + h,
            fill="#4b352e",
            outline=outline,
        )

    def _draw_library(self, c: tk.Canvas, center_x: float, bottom: float, width: float, level: int) -> None:
        x = center_x - width / 2
        y = bottom - 126 - min(level * 3, 24)
        c.create_rectangle(x + 12, y + 36, x + width + 12, bottom + 10, fill=COLORS["shadow"], outline="")
        c.create_rectangle(x, y + 44, x + width, bottom, fill="#eef1f5", outline=COLORS["ink"], width=2)
        c.create_polygon(
            x - 10,
            y + 44,
            center_x,
            y,
            x + width + 10,
            y + 44,
            fill=COLORS["navy"],
            outline=COLORS["ink"],
            width=2,
        )
        c.create_rectangle(x - 12, bottom - 8, x + width + 12, bottom, fill=COLORS["gold_dark"], outline=COLORS["ink"])
        column_count = 5
        for i in range(column_count):
            cx = x + width * (i + 1) / (column_count + 1)
            c.create_rectangle(cx - 7, y + 56, cx + 7, bottom - 12, fill="#fff6df", outline=COLORS["ink"])
            c.create_rectangle(cx - 11, y + 52, cx + 11, y + 58, fill=COLORS["gold"], outline=COLORS["ink"])
        c.create_text(center_x, y + 30, text="BIBLIOTHEK", fill=COLORS["cream"], font=("Segoe UI", 10, "bold"))

    def _draw_clock_tower(self, c: tk.Canvas, x: float, bottom: float, level: int) -> None:
        h = 178 + min(level * 4, 34)
        y = bottom - h
        w = 58
        c.create_rectangle(x + 8, y + 8, x + w + 8, bottom + 8, fill=COLORS["shadow"], outline="")
        c.create_rectangle(x, y + 28, x + w, bottom, fill="#b66d57", outline=COLORS["ink"], width=2)
        c.create_polygon(x - 8, y + 28, x + w / 2, y - 10, x + w + 8, y + 28, fill=COLORS["navy"], outline=COLORS["ink"])
        c.create_oval(x + 13, y + 44, x + w - 13, y + 78, fill=COLORS["cream"], outline=COLORS["ink"], width=2)
        cx, cy = x + w / 2, y + 61
        c.create_line(cx, cy, cx, cy - 11, fill=COLORS["ink"], width=2)
        c.create_line(cx, cy, cx + 10, cy + 5, fill=COLORS["ink"], width=2)
        for yy in range(int(y + 92), int(bottom - 24), 28):
            c.create_rectangle(x + 17, yy, x + 41, yy + 13, fill="#f5d98b", outline=COLORS["ink"])

    def _draw_observatory(self, c: tk.Canvas, x: float, bottom: float, level: int) -> None:
        w = 96
        h = 108 + min(level * 3, 24)
        y = bottom - h
        c.create_rectangle(x + 8, y + 28, x + w + 8, bottom + 8, fill=COLORS["shadow"], outline="")
        c.create_rectangle(x, y + 38, x + w, bottom, fill="#d4ddcf", outline=COLORS["ink"], width=2)
        c.create_arc(x, y - 8, x + w, y + 86, start=0, extent=180, fill=COLORS["slate"], outline=COLORS["ink"], width=2)
        c.create_rectangle(x + w * 0.47, y + 2, x + w * 0.56, y + 41, fill=COLORS["cream"], outline=COLORS["ink"])
        c.create_oval(x + 26, y + 58, x + 70, y + 90, fill="#f5d98b", outline=COLORS["ink"])
        c.create_text(x + w / 2, bottom - 16, text="OBS", fill=COLORS["ink"], font=("Segoe UI", 9, "bold"))

    def _draw_foreground(self, c: tk.Canvas, width: int, height: int, ground_y: int, minutes: int) -> None:
        c.create_rectangle(0, height - 28, width, height, fill="#bda983", outline="")
        tree_count = min(12, 3 + minutes // 12)
        for i in range(tree_count):
            rng = random.Random(8000 + i)
            x = rng.randint(20, max(24, int(width - 24)))
            y = rng.randint(ground_y + 34, max(ground_y + 36, height - 62))
            c.create_rectangle(x - 3, y, x + 3, y + 24, fill="#7b573f", outline="")
            c.create_oval(x - 17, y - 18, x + 17, y + 14, fill="#6e976e", outline="")
            c.create_oval(x - 9, y - 29, x + 21, y + 4, fill="#789f76", outline="")

        if minutes >= 10:
            c.create_rectangle(width * 0.44, height - 78, width * 0.56, height - 68, fill=COLORS["navy"], outline=COLORS["ink"])
            c.create_rectangle(width * 0.455, height - 68, width * 0.545, height - 58, fill=COLORS["navy_light"], outline=COLORS["ink"])
        if minutes >= 35:
            self._draw_student(c, width * 0.30, height - 58, "#315d85")
            self._draw_student(c, width * 0.68, height - 60, "#8a4f46")
        if minutes >= 90:
            c.create_arc(width * 0.43, height - 112, width * 0.57, height - 34, start=0, extent=180, fill="", outline=COLORS["gold_dark"], width=5)

    def _draw_student(self, c: tk.Canvas, x: float, y: float, color: str) -> None:
        c.create_oval(x - 7, y - 28, x + 7, y - 14, fill="#d7a276", outline=COLORS["ink"])
        c.create_rectangle(x - 8, y - 14, x + 8, y + 9, fill=color, outline=COLORS["ink"])
        c.create_line(x - 5, y + 9, x - 12, y + 24, fill=COLORS["ink"], width=2)
        c.create_line(x + 5, y + 9, x + 13, y + 24, fill=COLORS["ink"], width=2)
        c.create_rectangle(x + 10, y - 8, x + 24, y + 2, fill=COLORS["paper"], outline=COLORS["ink"])

    def _draw_journal(self) -> None:
        self._draw_learning_analysis_summary()
        sessions = list(self.data.get("sessions", []))[-3:]
        if not sessions:
            self.journal_label.configure(text="Noch keine gespeicherten Sessions.")
            return
        parts = []
        for session in reversed(sessions):
            learned = self._short_text(str(session.get("learned", "")), 80)
            learned_part = f" | gelernt: {learned}" if learned else ""
            xp = int(session.get("xp", self._xp_for_seconds(int(session.get("seconds", 0)))))
            lost_xp = int(session.get("lost_xp", 0))
            status = str(session.get("status", "beendet"))
            xp_part = f"+{xp} XP"
            if lost_xp:
                xp_part += f", -{lost_xp} XP"
            reason = str(session.get("abort_reason", "")).strip()
            reason_part = f" | Grund: {reason}" if reason else ""
            subject = str(session.get("subject", DEFAULT_SUBJECT)).strip() or DEFAULT_SUBJECT
            parts.append(
                f"{session.get('date', '')}: {minutes_text(int(session.get('seconds', 0)))} "
                f"{xp_part} ({status}) · {subject} - {session.get('goal', 'Lernsession')}{learned_part}{reason_part}"
            )
        self.journal_label.configure(text="\n".join(parts))

    def _draw_learning_analysis_summary(self) -> None:
        sessions = list(self.data.get("sessions", []))
        finished = [session for session in sessions if session.get("status") != "abgebrochen"]
        aborted = [session for session in sessions if session.get("status") == "abgebrochen"]
        week_seconds = self._week_seconds(date.today())
        today_seconds = self._seconds_for_day(date.today())
        note_count = sum(1 for session in sessions if str(session.get("learned", "")).strip())
        avg_seconds = 0
        if finished:
            avg_seconds = sum(int(session.get("seconds", 0)) for session in finished) // len(finished)
        current_streak, best_streak = self._streak_counts(include_active=True)
        best_streak = max(best_streak, int(self.data.get("best_streak", 0)))
        top_subject = self._top_subject_text()
        due_reviews, upcoming_reviews = self._review_counts()
        goals = [
            self._short_text(str(session.get("goal", "")).strip(), 24)
            for session in reversed(sessions[-8:])
            if str(session.get("goal", "")).strip()
        ]
        goal_line = "Letzte Ziele: " + " | ".join(goals[:3]) if goals else "Letzte Ziele: noch keine"
        self.tree_label.configure(
            text=(
                f"Heute {minutes_text(today_seconds)} · Woche {minutes_text(week_seconds)}\n"
                f"Streak {current_streak} Tage · Rekord {best_streak} · Schnitt {minutes_text(avg_seconds)}\n"
                f"Top-Fach {top_subject} · {note_count} Notizen · {due_reviews} Wdh. faellig\n"
                f"Sessions {len(finished)} beendet · {len(aborted)} abgebrochen\n"
                f"{goal_line}"
            )
        )

    def _short_text(self, text: str, limit: int) -> str:
        clean = " ".join(text.split())
        if len(clean) <= limit:
            return clean
        return clean[: limit - 3].rstrip() + "..."

    def _xp_for_seconds(self, seconds: int) -> int:
        return max(0, (int(seconds) * XP_PER_HOUR) // 3600)

    def _city_level(self, seconds: int) -> int:
        minutes = seconds // 60
        if minutes < 25:
            return 1
        if minutes < 60:
            return 2
        if minutes < 120:
            return 3
        if minutes < 240:
            return 4
        return 5

    def _city_title(self, level: int) -> str:
        titles = {
            1: "Gruene Wiese",
            2: "Kleines Dorf",
            3: "Flussdorf",
            4: "Marktflecken",
            5: "Bergtal-Siedlung",
        }
        return titles.get(level, "Bergtal-Siedlung")

    def _apply_theme(self) -> None:
        mode = self.theme_mode.get()
        palette = DARK_COLORS if mode == "dark" else LIGHT_COLORS
        for k, v in palette.items():
            COLORS[k] = v
            
        # Re-build styles
        self._build_styles()
        
        # Recursively update standard Tkinter widgets
        self._update_widget_colors(self.root)
        
        # Re-draw canvasses and active panes
        self._render_all()

    def _update_widget_colors(self, widget) -> None:
        try:
            w_class = widget.winfo_class()
        except Exception:
            return

        bg = None
        fg = None

        if isinstance(widget, RoundedPanel):
            bg = COLORS["paper"]
            fill = COLORS["cream"]
            curr_bg = widget.cget("bg")
            if curr_bg == LIGHT_COLORS["paper_dark"] or curr_bg == DARK_COLORS["paper_dark"]:
                bg = COLORS["paper_dark"]
            widget.update_colors(bg, fill)
            for child in widget.winfo_children():
                if child != widget.canvas:
                    self._update_widget_colors(child)
            return

        if w_class in ("Frame", "Labelframe"):
            curr_bg = widget.cget("bg")
            if curr_bg == LIGHT_COLORS["paper_dark"] or curr_bg == DARK_COLORS["paper_dark"]:
                bg = COLORS["paper_dark"]
            elif curr_bg == LIGHT_COLORS["paper"] or curr_bg == DARK_COLORS["paper"]:
                bg = COLORS["paper"]
            elif curr_bg == LIGHT_COLORS["cream"] or curr_bg == DARK_COLORS["cream"]:
                bg = COLORS["cream"]
            else:
                bg = COLORS["paper"]
            widget.configure(bg=bg)
            
        elif w_class == "Label":
            curr_bg = widget.cget("bg")
            curr_fg = widget.cget("fg")
            
            if curr_bg == LIGHT_COLORS["paper_dark"] or curr_bg == DARK_COLORS["paper_dark"]:
                bg = COLORS["paper_dark"]
            elif curr_bg == LIGHT_COLORS["paper"] or curr_bg == DARK_COLORS["paper"]:
                bg = COLORS["paper"]
            elif curr_bg == LIGHT_COLORS["cream"] or curr_bg == DARK_COLORS["cream"]:
                bg = COLORS["cream"]
            elif curr_bg == LIGHT_COLORS["navy"] or curr_bg == DARK_COLORS["navy"]:
                bg = COLORS["navy"]
            else:
                bg = COLORS["paper"]
                
            if curr_fg == LIGHT_COLORS["ink"] or curr_fg == DARK_COLORS["ink"]:
                fg = COLORS["ink"]
            elif curr_fg == LIGHT_COLORS["muted"] or curr_fg == DARK_COLORS["muted"]:
                fg = COLORS["muted"]
            elif curr_fg == LIGHT_COLORS["gold"] or curr_fg == DARK_COLORS["gold"]:
                fg = COLORS["gold"]
            elif curr_fg == "#ffffff" or curr_fg == "#ffffff":
                fg = "#ffffff"
            else:
                fg = COLORS["ink"]
                
            widget.configure(bg=bg, fg=fg)
            
        elif w_class == "Button":
            curr_bg = widget.cget("bg")
            curr_fg = widget.cget("fg")
            
            if curr_bg == LIGHT_COLORS["paper_dark"] or curr_bg == DARK_COLORS["paper_dark"]:
                bg = COLORS["paper_dark"]
                fg = COLORS["muted"]
                widget.configure(bg=bg, fg=fg, activebackground="#eef0fe" if self.theme_mode.get() == "light" else "#1e2030")
            elif curr_bg == LIGHT_COLORS["navy"] or curr_bg == DARK_COLORS["navy"]:
                bg = COLORS["navy"]
                fg = COLORS["cream"]
                widget.configure(bg=bg, fg=fg, activebackground=COLORS["navy_light"])
            elif curr_bg == LIGHT_COLORS["paper_dark"] or curr_bg == DARK_COLORS["paper_dark"] or curr_bg == "#fbfbfa":
                bg = COLORS["paper_dark"]
                fg = COLORS["ink"]
                widget.configure(bg=bg, fg=fg)
            else:
                bg = COLORS["paper_dark"]
                fg = COLORS["ink"]
                widget.configure(bg=bg, fg=fg)
                
        elif w_class == "Entry":
            widget.configure(bg=COLORS["cream"], fg=COLORS["ink"], insertbackground=COLORS["ink"])
            
        elif w_class == "Spinbox":
            widget.configure(bg=COLORS["cream"], fg=COLORS["ink"])
            
        elif w_class == "Canvas":
            curr_bg = widget.cget("bg")
            if curr_bg == LIGHT_COLORS["paper_dark"] or curr_bg == DARK_COLORS["paper_dark"]:
                bg = COLORS["paper_dark"]
            elif curr_bg == LIGHT_COLORS["paper"] or curr_bg == DARK_COLORS["paper"]:
                bg = COLORS["paper"]
            elif curr_bg == LIGHT_COLORS["cream"] or curr_bg == DARK_COLORS["cream"]:
                bg = COLORS["cream"]
            else:
                bg = COLORS["paper"]
            widget.configure(bg=bg)

        elif w_class == "Toplevel":
            widget.configure(bg=COLORS["paper"])
            
        elif w_class == "Checkbutton":
            curr_bg = widget.cget("bg")
            if curr_bg == LIGHT_COLORS["paper_dark"] or curr_bg == DARK_COLORS["paper_dark"]:
                bg = COLORS["paper_dark"]
            else:
                bg = COLORS["cream"]
            widget.configure(
                bg=bg,
                fg=COLORS["ink"],
                activebackground=bg,
                activeforeground=COLORS["ink"],
                selectcolor=COLORS["cream"]
            )

        elif w_class == "Scale":
            widget.configure(
                bg="#ffffff",
                highlightbackground=COLORS["cream"],
                fg=COLORS["ink"],
                troughcolor=COLORS["gold"],
                activebackground="#ffffff"
            )

        for child in widget.winfo_children():
            self._update_widget_colors(child)

    def _on_close(self) -> None:
        if self._quit_requested:
            self._save_current_session()
            self.root.destroy()
            return
        self._hide_to_tray()


class RoundedPanel(tk.Frame):
    def __init__(self, master, bg: str, fill: str, radius: int = 14, **kwargs) -> None:
        super().__init__(master, bg=bg, **kwargs)
        self.fill = fill
        self.radius = radius
        self.canvas = tk.Canvas(self, bg=bg, bd=0, highlightthickness=0)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Use tk.Frame instead of ttk.Frame for direct background color control
        self.inner = tk.Frame(self, bg=fill, bd=0, relief="flat")
        self.bind("<Configure>", self._draw)

    def update_colors(self, bg: str, fill: str) -> None:
        self.fill = fill
        self.configure(bg=bg)
        self.canvas.configure(bg=bg)
        self.inner.configure(bg=fill)
        self._draw()

    def _draw(self, _event=None) -> None:
        self.canvas.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w <= 10 or h <= 10:
            return
        r = min(self.radius, max(1, w // 2), max(1, h // 2))
        
        # Draw the main filled rounded rectangle with line border
        self._rounded_rectangle(1, 1, w - 1, h - 1, r, fill=self.fill, outline=COLORS["line"])
        
        # Inset the inner frame slightly so it does not draw over the rounded border
        inset = 2
        self.inner.place(x=inset, y=inset, width=w - 2 * inset, height=h - 2 * inset)

    def _rounded_rectangle(self, x1, y1, x2, y2, r, **kwargs) -> None:
        points = [
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1
        ]
        self.canvas.create_polygon(points, smooth=True, **kwargs)


if __name__ == "__main__":
    StudyCityApp().run()
