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
REPLACED_ADDON = "plugin.video.xstream-player"
GIPTV_ID = "plugin.video.giptv"
GIPTV_VERSION = "3.1.0"
BUILD_VERSION = "1.0.3"
REPO_ID = "repository.kingblap"
NATIVE_SUFFIXES = {".dll", ".so", ".dylib", ".pyd"}
SECRET_ID = re.compile(
    r"(?i)(?:^|[._-])(?:password|passwd|token|secret|api[_-]?key|credential|auth|email|username)(?:$|[._-])"
)
SECRET_VALUE = re.compile(
    r"(?i)(?:bearer\s+[A-Za-z0-9._~-]{12,}|(?:password|passwd|token|secret|api[_-]?key)\s*[:=]\s*\S+|https?://[^/\s:@]+:[^/\s@]+@)"
)
LOCAL_PATH = re.compile(r"(?i)(?:[a-z]:\\|\\\\|/storage/|/home/|/users/|special://profile)")
ADDON_PATH = re.compile(r"(?i)(?:plugin://|runaddon\(|runscript\()")


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
    if addon_id == REPLACED_ADDON:
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


def portable_addon_icon(setting_id, value, packages, chosen):
    """Translate a saved Windows add-on logo path to Kodi's portable path."""
    if not setting_id.casefold().startswith("addonset") or not setting_id.casefold().endswith(".icon"):
        return None

    match = re.search(
        r"(?i)(?:^|[\\/])addons[\\/](?P<addon>[A-Za-z0-9_.-]+)[\\/](?P<member>.+)$",
        value,
    )
    if not match:
        return None

    addon_id = match.group("addon").casefold()
    if addon_id not in chosen or addon_id not in packages:
        return None
    relative = PurePosixPath(match.group("member").replace("\\", "/"))
    if relative.is_absolute() or not relative.parts or any(part in ("", ".", "..") for part in relative.parts):
        return None

    try:
        with zipfile.ZipFile(packages[addon_id][2]) as archive:
            root_entry, _ = addon_xml_from_zip(archive)
            if root_entry is None:
                return None
            prefix = root_entry.split("/", 1)[0] + "/"
            members = {
                name[len(prefix):].casefold(): name[len(prefix):]
                for name in archive.namelist()
                if name.startswith(prefix) and not name.endswith("/")
            }
    except (OSError, zipfile.BadZipFile):
        return None

    packaged_member = members.get(relative.as_posix().casefold())
    if packaged_member is None:
        return None
    return "special://home/addons/{}/{}".format(addon_id, packaged_member)


def skin_settings(snapshot, packages, chosen):
    path = snapshot / "addon_data" / SKIN_ID / "settings.xml"
    root = ET.parse(path).getroot()
    sanitized = ET.Element("settings")
    for element in root.findall("setting"):
        setting_id = element.get("id", "")
        value = "".join(element.itertext()).strip()
        if SECRET_ID.search(setting_id) or SECRET_VALUE.search(value):
            continue
        portable_icon = portable_addon_icon(setting_id, value, packages, chosen)
        if portable_icon is not None:
            value = portable_icon
        elif LOCAL_PATH.search(value) or ("http://" in value.lower()) or ("https://" in value.lower()):
            continue
        value = re.sub(re.escape(REPLACED_ADDON), GIPTV_ID, value, flags=re.IGNORECASE)
        value = re.sub(r"(?i)xstream\s+player", "GIPTV", value)
        setting = ET.SubElement(sanitized, "setting", dict(element.attrib))
        setting.text = value
    return ET.tostring(sanitized, encoding="utf-8", xml_declaration=True)


def package_dependencies(addon):
    requires = addon.find("requires")
    if requires is None:
        return []
    return [
        item.get("addon", "")
        for item in requires.findall("import")
        if item.get("addon") and item.get("optional", "false").casefold() != "true"
    ]


def build(snapshot, output):
    if not (snapshot / "xbmcbackup.val").is_file():
        raise ValueError("The selected folder is not a Kodi backup snapshot (xbmcbackup.val is missing).")
    packages = package_index()
    installed = installed_ids(snapshot)
    chosen = set()
    excluded_platform = set()
    pending = list(installed | {REPO_ID, GIPTV_ID, SKIN_ID})

    while pending:
        addon_id = pending.pop()
        if addon_id in chosen or addon_id == REPLACED_ADDON:
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
    if SKIN_ID not in chosen:
        raise ValueError("The backup's Xonfluence skin package is missing from the repository.")

    info = {
        "name": "KingBlap Kodi Build",
        "version": BUILD_VERSION,
        "kodi_major": 22,
        "skin": SKIN_ID,
        "addons": sorted(chosen),
        "replaced_addon": REPLACED_ADDON,
        "excluded_platform_addons": sorted(excluded_platform),
        "excluded_user_data": [
            "add-on accounts and credentials",
            "Kodi databases and media libraries",
            "provider playlists, EPG, and source paths",
            "add-on caches and thumbnails",
            "Windows-only native add-ons",
        ],
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9, allowZip64=True) as build_zip:
        build_zip.writestr("build_info.json", json.dumps(info, indent=2) + "\n")
        build_zip.writestr(
            "userdata/addon_data/{}/settings.xml".format(SKIN_ID),
            skin_settings(snapshot, packages, chosen),
        )
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
