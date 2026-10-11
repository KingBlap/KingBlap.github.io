#!/usr/bin/env python3
"""Create the portable KingBlap Kodi build ZIP from a Kodi backup snapshot.

The backup's add-on account data, Kodi databases, media sources, thumbnails,
and platform-specific binary add-ons are intentionally excluded.
"""
import argparse
import json
import re
import shutil
import sqlite3
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
ZIP_ROOT = ROOT / "repo" / "zips"
SKIN_ID = "skin.xonfluence"
SKIN_VERSION = "6.0.7"
LEGACY_SKIN_ID = "skin.estuary.modv2"
ONEPLAY_REPO_ID = "One.repo"
REPLACED_ADDON = "plugin.video.xstream-player"
GIPTV_ID = "plugin.video.giptv"
GIPTV_VERSION = "3.1.0"
WEATHER_ID = "weather.gismeteo"
WEATHER_VERSION = "0.6.4+matrix.1"
WEATHER_LOCATION = "Thomasville"
WEATHER_LOCATION_ID = "8771"
WEATHER_SETTINGS_ARCHIVE_PATH = "userdata/addon_data/{}/settings.xml".format(WEATHER_ID)
BUILD_VERSION = "1.0.15"
REPO_ID = "repository.kingblap"
NATIVE_SUFFIXES = {".dll", ".so", ".dylib", ".pyd"}
SECRET_SETTING = re.compile(
    r"(?i)(?:^|[._-])(?:password|passwd|token|secret|api[_-]?key|credential|auth|email|username|client[_-]?id|refresh[_-]?token)(?:$|[._-])"
)
SECRET_VALUE = re.compile(
    r"(?i)(?:\bbearer\s+[A-Za-z0-9._~-]{12,}|"
    r"\b(?:password|passwd|token|secret|api[_-]?key|credential|auth|email|username)\s*[:=]\s*[^\s<&]+|"
    r"[?&](?:password|passwd|token|secret|api[_-]?key|credential|auth|email|username)=|"
    r"https?://[^/\s:@]+:[^/\s@]+@)"
)
LOCAL_PATH = re.compile(
    r"(?i)(?:[a-z]:[\\/]|\\\\|(?:^|[\\/])(?:storage|home|users|profiles)[\\/]|"
    r"special://(?:home|profile|temp|masterprofile)/)"
)
WEB_URL = re.compile(r"(?i)https?://")
ADDON_ICON_SETTING = re.compile(r"(?i)^addonset[^.]*\.[^.]+\.icon$")
ADDON_PATH = re.compile(
    r"(?i)(?:^|[\\/])addons[\\/](?P<addon_id>[A-Za-z0-9_.-]+)[\\/](?P<member>.+)$"
)


def version_key(value):
    return tuple(
        (0, int(part)) if part.isdigit() else (1, part.casefold())
        for part in re.findall(r"\d+|[A-Za-z]+", value)
    )


def addon_xml_from_zip(archive):
    candidates = [
        name for name in archive.namelist()
        if name.count("/") == 1 and name.endswith("/addon.xml")
    ]
    if len(candidates) != 1:
        return None, None
    return candidates[0], ET.fromstring(archive.read(candidates[0]))


def zip_has_native_binary(archive):
    return any(Path(name).suffix.casefold() in NATIVE_SUFFIXES for name in archive.namelist())


def package_index():
    latest = {}
    for path in sorted(ZIP_ROOT.glob("*/*.zip")):
        try:
            with zipfile.ZipFile(path) as archive:
                inner, addon = addon_xml_from_zip(archive)
                if addon is None:
                    continue
                addon_id = addon.get("id", "")
                version = addon.get("version", "")
                platform = (addon.findtext("extension[@point='xbmc.addon.metadata']/platform") or "").strip().casefold()
                record = (version, platform, path)
                current = latest.get(addon_id)
                if current is None or version_key(version) > version_key(current[0]):
                    latest[addon_id] = record
        except (OSError, zipfile.BadZipFile, ET.ParseError):
            continue
    return latest


def installed_ids(snapshot):
    database = snapshot / "database" / "Addons33.db"
    with sqlite3.connect("file:{}?mode=ro".format(database.as_posix()), uri=True) as connection:
        return {
            row[0]
            for row in connection.execute("SELECT DISTINCT addonID FROM installed WHERE enabled = 1")
        }


def portable_addon(addon_id, record):
    version, platform, path = record
    if addon_id in (REPLACED_ADDON, LEGACY_SKIN_ID, ONEPLAY_REPO_ID):
        return False
    if addon_id.startswith("repository.") and addon_id != REPO_ID:
        return False
    if platform not in ("", "all"):
        return False
    try:
        with zipfile.ZipFile(path) as archive:
            return not zip_has_native_binary(archive)
    except (OSError, zipfile.BadZipFile):
        return False


def package_dependencies(addon):
    requires = addon.find("requires")
    if requires is None:
        return []
    return [
        item.get("addon", "")
        for item in requires.findall("import")
        if item.get("addon") and item.get("optional", "false").casefold() != "true"
    ]


def portable_addon_icon(setting_id, value, packages, chosen):
    """Translate a snapshot-local add-on icon path into Kodi's portable path."""
    if not ADDON_ICON_SETTING.fullmatch(setting_id):
        return None
    match = ADDON_PATH.search(value)
    if match is None:
        return None
    addon_id = match.group("addon_id")
    member = PurePosixPath(match.group("member").replace("\\", "/"))
    if (
        addon_id not in chosen
        or member.is_absolute()
        or any(part in ("", ".", "..") for part in member.parts)
    ):
        return None
    record = packages.get(addon_id)
    if record is None:
        return None
    with zipfile.ZipFile(record[2]) as addon_zip:
        root, addon = addon_xml_from_zip(addon_zip)
        if addon is None or addon.get("id") != addon_id:
            return None
        expected = root.split("/", 1)[0] + "/" + member.as_posix()
        if expected not in addon_zip.namelist():
            return None
    return "special://home/addons/{}/{}".format(addon_id, member.as_posix())


def make_skin_settings(snapshot, packages, chosen):
    """Keep portable Xonfluence presentation settings and discard private/local values."""
    source = snapshot / "addon_data" / SKIN_ID / "settings.xml"
    if not source.is_file():
        raise ValueError("The Kodi snapshot is missing Xonfluence skin settings.xml.")
    original = ET.parse(source).getroot()
    if original.tag != "settings":
        raise ValueError("The snapshot's Xonfluence settings file is not valid Kodi settings XML.")

    sanitized = ET.Element("settings")
    kept = 0
    for setting in original.findall("setting"):
        setting_id = setting.get("id", "")
        value = setting.text or ""
        if (
            not setting_id
            or SECRET_SETTING.search(setting_id)
            or setting_id.casefold() == "lastvideoplayed"
        ):
            continue
        if SECRET_VALUE.search(value):
            continue
        if LOCAL_PATH.search(value) or WEB_URL.search(value):
            portable = portable_addon_icon(setting_id, value, packages, chosen)
            if portable is None:
                continue
            value = portable
        entry = ET.SubElement(sanitized, "setting", dict(setting.attrib))
        entry.text = value
        kept += 1
    if kept < 1:
        raise ValueError("No portable Xonfluence skin settings remained after sanitizing the snapshot.")

    # The background pictures ship inside the skin, so this path works on
    # Windows, Android phones, Android TV, and Fire TV without a profile path.
    required_settings = {
        "globalbackgroundpath": ("GlobalBackGroundPath", "string", "special://skin/extras/DemonWomen/"),
        "singleglobalbackground": ("singleglobalbackground", "bool", "true"),
        "globalliveweatherimage": ("globalliveweatherimage", "bool", "false"),
    }
    settings_by_id = {
        setting.get("id", "").casefold(): setting
        for setting in sanitized.findall("setting")
    }
    for setting_key, (setting_id, setting_type, value) in required_settings.items():
        entry = settings_by_id.get(setting_key)
        if entry is None:
            entry = ET.SubElement(sanitized, "setting", {"id": setting_id, "type": setting_type})
            settings_by_id[setting_key] = entry
            kept += 1
        else:
            entry.set("id", setting_id)
            entry.set("type", setting_type)
        entry.text = value
    return ET.tostring(sanitized, encoding="utf-8", xml_declaration=True), kept


def make_weather_settings():
    """Package the requested Gismeteo location without unrelated profile data."""
    settings = ET.Element("settings", {"version": "4"})
    for setting_id, value in (
        ("CurrentLocation", "false"),
        ("Location1", WEATHER_LOCATION),
        ("Location1ID", WEATHER_LOCATION_ID),
    ):
        ET.SubElement(settings, "setting", {"id": setting_id}).text = value
    return ET.tostring(settings, encoding="utf-8", xml_declaration=True)


def build(snapshot, output):
    if not (snapshot / "xbmcbackup.val").is_file():
        raise ValueError("The selected folder is not a Kodi backup snapshot (xbmcbackup.val is missing).")
    packages = package_index()
    installed = installed_ids(snapshot)
    chosen = set()
    excluded_platform = set()
    pending = list(installed | {REPO_ID, GIPTV_ID, SKIN_ID, WEATHER_ID})

    while pending:
        addon_id = pending.pop()
        if addon_id in chosen or addon_id in (REPLACED_ADDON, LEGACY_SKIN_ID, ONEPLAY_REPO_ID):
            continue
        record = packages.get(addon_id)
        if record is None:
            continue
        if not portable_addon(addon_id, record):
            if record[1] not in ("", "all"):
                excluded_platform.add(addon_id)
            continue
        chosen.add(addon_id)
        with zipfile.ZipFile(record[2]) as archive:
            _, addon = addon_xml_from_zip(archive)
            for dependency in package_dependencies(addon):
                if dependency in packages and dependency not in chosen:
                    pending.append(dependency)

    if GIPTV_ID not in chosen or packages.get(GIPTV_ID, (None,))[0] != GIPTV_VERSION:
        raise ValueError("GIPTV 3.1.0 must be present in the public Kodi repository first.")
    if SKIN_ID not in chosen or packages.get(SKIN_ID, (None,))[0] != SKIN_VERSION:
        raise ValueError("The fresh Kodi 22 Xonfluence 6.0.7 skin package is missing from the repository.")
    if WEATHER_ID not in chosen or packages.get(WEATHER_ID, (None,))[0] != WEATHER_VERSION:
        raise ValueError("The Gismeteo weather package is missing from the repository.")
    for addon_id in (
        "script.favourites",
        "script.image.resource.select",
    ):
        if addon_id not in chosen:
            raise ValueError("The Xonfluence dependency {} is missing.".format(addon_id))

    skin_settings, skin_setting_count = make_skin_settings(snapshot, packages, chosen)
    weather_settings = make_weather_settings()

    info = {
        "name": "KingBlap Kodi Build",
        "version": BUILD_VERSION,
        "kodi_major": 22,
        "skin": SKIN_ID,
        "addons": sorted(chosen),
        "replaced_addon": REPLACED_ADDON,
        "removed_addons": [LEGACY_SKIN_ID, ONEPLAY_REPO_ID],
        "weather_addon": WEATHER_ID,
        "weather_location": "Thomasville, North Carolina",
        "weather_location_id": WEATHER_LOCATION_ID,
        "excluded_platform_addons": sorted(excluded_platform),
        "excluded_user_data": [
            "add-on accounts and credentials",
            "Kodi databases and media libraries",
            "provider playlists, EPG, and source paths",
            "add-on caches and thumbnails",
            "platform-specific native add-ons",
        ],
        "included_user_data": [
            "sanitized Xonfluence skin settings ({} portable settings)".format(skin_setting_count),
            "Gismeteo weather configuration for Thomasville, North Carolina",
        ],
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9, allowZip64=True) as build_zip:
        build_zip.writestr("build_info.json", json.dumps(info, indent=2) + "\n")
        build_zip.writestr(
            "userdata/addon_data/{}/settings.xml".format(SKIN_ID),
            skin_settings,
        )
        build_zip.writestr(WEATHER_SETTINGS_ARCHIVE_PATH, weather_settings)
        for addon_id in sorted(chosen):
            record = packages[addon_id]
            with zipfile.ZipFile(record[2]) as addon_zip:
                root_entry, addon = addon_xml_from_zip(addon_zip)
                if addon.get("id") != addon_id:
                    raise ValueError("An add-on package ID does not match its file path.")
                source_root = root_entry.split("/", 1)[0] + "/"
                for member in addon_zip.infolist():
                    if member.is_dir() or not member.filename.startswith(source_root):
                        continue
                    relative = member.filename[len(source_root):]
                    if not relative or "__pycache__" in relative.split("/") or relative.endswith((".pyc", ".pyo")):
                        continue
                    target = "addons/{}/{}".format(addon_id, relative)
                    with addon_zip.open(member, "r") as source, build_zip.open(target, "w") as dest:
                        shutil.copyfileobj(source, dest, 1024 * 1024)

    print("Build: {}".format(output))
    print("Portable add-ons: {}".format(len(chosen)))
    print("Excluded platform-specific add-ons: {}".format(", ".join(sorted(excluded_platform)) or "none"))
    print("Archive bytes: {}".format(output.stat().st_size))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, required=True, help="Kodi backup snapshot root")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT.parent / "KingBlapKodiBuild-{}.zip".format(BUILD_VERSION),
        help="Output build archive path",
    )
    args = parser.parse_args()
    build(args.snapshot.resolve(), args.output.resolve())


if __name__ == "__main__":
    main()
