"""KingBlap Kodi build installer for Kodi 21 Omega and Kodi 22 Piers."""
import json
import hashlib
import html
import os
import re
import shutil
import sys
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
import uuid
import xml.etree.ElementTree as ET
import zipfile

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs


ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo("id")
DEFAULT_API_URL = "https://kingblap-api.tyshawncalvin243.workers.dev"
BUILDS_PATH = "/v1/builds"
BUILTIN_DIM_SCREENSAVER_ID = "screensaver.xbmc.builtin.dim"
def _detect_kodi_major():
    """Read Kodi's major version without relying on platform-specific paths."""
    try:
        match = re.match(r"\s*(\d+)", xbmc.getInfoLabel("System.BuildVersion"))
        return int(match.group(1)) if match else 0
    except (AttributeError, TypeError, ValueError):
        return 0


KODI_MAJOR = _detect_kodi_major()
if KODI_MAJOR == 21:
    SKIN_ID = "skin.xonfluence.skinbase"
    SKIN_VERSION = "5"
    PREVIOUS_SKIN_ID = "skin.xonfluence"
elif KODI_MAJOR == 22:
    SKIN_ID = "skin.xonfluence"
    SKIN_VERSION = "6.0.7"
    PREVIOUS_SKIN_ID = None
else:
    SKIN_ID = "skin.xonfluence"
    SKIN_VERSION = "6.0.7"
    PREVIOUS_SKIN_ID = None
KODI21_PUBLIC_BUILD_ID = "kingblap-public-kodi21.3-1.0.23"
KODI21_PRIVATE_BUILD_ID = "kingblap-private-kodi21.3-1.0.21"
KODI21_PRIVATE_BUILD_PREFIX = "kingblap-private-kodi21.3-"
KODI21_PUBLIC_BUILD_NAME = "Public KingBlap Build for Kodi 21.3 1.0.23 (download)"
KODI21_PRIVATE_BUILD_NAME = "Private KingBlap Build for Kodi 21.3 (download)"
KODI22_PUBLIC_BUILD_ID = "kingblap-public-kodi22-1.0.23"
KODI22_PRIVATE_BUILD_ID = "kingblap-private-kodi22-1.0.26"
KODI22_PUBLIC_BUILD_NAME = "Public KingBlap Build for Kodi 22 1.0.23 (download)"
KODI22_PRIVATE_BUILD_NAME = "Private KingBlap Build for Kodi 22 1.0.28 (download)"
KODI22_PRIVATE_BUILD_PREFIX = "kingblap-private-kodi22-"
KODI21_PUBLIC_BUILD_PARTS = (
    ("https://kingblap.github.io/builds/public/KingBlapKodiPublicBuild-21.3-1.0.23.zip.part001", 82948762),
)
KODI21_PUBLIC_BUILD_SHA256 = "A03171BA07AA8E427530EEB06F0ACDB2542988D01D31E60FB03AEC6D1FCB309A"
KODI22_PUBLIC_BUILD_PARTS = (
    ("https://kingblap.github.io/builds/public/KingBlapKodiPublicBuild-22-1.0.23.zip.part001", 69831690),
)
KODI22_PUBLIC_BUILD_SHA256 = "A2548B1BD2C746D1AC1701A8314352EDDBC68DE64136102403F50D59C51D8FAA"
WEATHER_VERSION = "0.6.4+matrix.1"
SKIN_SETTINGS_ARCHIVE_PATH = "userdata/addon_data/{}/settings.xml".format(SKIN_ID)
LEGACY_SKIN_ID = "skin.estuary.modv2"
ONEPLAY_REPO_ID = "One.repo"
WEATHER_ID = "weather.gismeteo"
PVR_ADDON_ID = "pvr.iptvsimple"
OPTIKLEAN_ID = "program.optiklean"
WEATHER_LOCATION = "Thomasville"
WEATHER_LOCATION_ID = "8771"
WEATHER_ADDON_SETTINGS = {
    "CurrentLocation": "false",
    "Location1": WEATHER_LOCATION,
    "Location1ID": WEATHER_LOCATION_ID,
}
WEATHER_SETTINGS_ARCHIVE_PATH = "userdata/addon_data/{}/settings.xml".format(WEATHER_ID)
PROFILE_DATA_MODE = "replace-addon-data-except-wizard"
BUILD_LIMIT = 1024 * 1024 * 1024
DOWNLOAD_LIMIT = 512 * 1024 * 1024
PRE_DOWNLOAD_EXPANSION_RESERVE = 512 * 1024 * 1024
INSTALL_SAFETY_RESERVE = 64 * 1024 * 1024
ACCESS_CODE_PATTERN = re.compile(r"[0-9]{16}\Z")
CHUNK_SIZE = 256 * 1024
ADDON_REGISTRATION_TIMEOUT = 600
SKIN_LOAD_TIMEOUT = 120
SKIN_CONFIRMATION_GRACE = 13


def _platform_name():
    """Return the platform Kodi is running on for install guidance."""
    checks = (
        ("Android (phones / Android TV / Fire TV)", "System.Platform.Android"),
        ("Windows", "System.Platform.Windows"),
        ("macOS", "System.Platform.OSX"),
        ("iOS / tvOS", "System.Platform.IOS"),
        ("Linux / LibreELEC", "System.Platform.Linux"),
    )
    for name, condition in checks:
        try:
            if xbmc.getCondVisibility(condition):
                return name
        except Exception:
            pass
    if sys.platform.startswith("win"):
        return "Windows"
    if sys.platform == "darwin":
        return "macOS"
    if sys.platform.startswith("linux"):
        return "Linux"
    return "this Kodi device"


class AccessDenied(ValueError):
    """The private KingBlap API rejected the configured access code."""


def _log(message, level=xbmc.LOGINFO):
    xbmc.log("[{}] {}".format(ADDON_ID, message), level)


def _path(special):
    return os.path.abspath(xbmcvfs.translatePath(special))


def _installed_addon_version(addon_root, addon_id):
    manifest_path = os.path.join(addon_root, addon_id, "addon.xml")
    try:
        with open(manifest_path, "rb") as manifest_file:
            manifest = ET.parse(manifest_file).getroot()
    except (OSError, ET.ParseError):
        return None
    if manifest.get("id") != addon_id:
        return None
    return manifest.get("version")


def _addon_directory_fingerprint(path):
    """Return a content signature for an add-on tree, or None if it is incomplete."""
    if not os.path.isdir(path) or os.path.islink(path):
        return None
    files = {}

    def raise_walk_error(error):
        raise error

    try:
        for current, directories, filenames in os.walk(path, onerror=raise_walk_error):
            if any(os.path.islink(os.path.join(current, name)) for name in directories):
                return None
            for filename in filenames:
                file_path = os.path.join(current, filename)
                if os.path.islink(file_path) or not os.path.isfile(file_path):
                    return None
                relative = os.path.relpath(file_path, path).replace(os.sep, "/")
                digest = hashlib.sha256()
                with open(file_path, "rb") as source:
                    while True:
                        block = source.read(CHUNK_SIZE)
                        if not block:
                            break
                        digest.update(block)
                files[relative] = (os.path.getsize(file_path), digest.hexdigest())
    except OSError:
        return None
    return files or None


def _addon_directories_match(first, second):
    """Check all packaged add-on files and contents before keeping an active skin."""
    first_files = _addon_directory_fingerprint(first)
    second_files = _addon_directory_fingerprint(second)
    return first_files is not None and first_files == second_files


def _api_url(path):
    base = ADDON.getSetting("api_url").strip() or DEFAULT_API_URL
    parsed = urllib.parse.urlsplit(base)
    if (
        parsed.scheme.casefold() != "https"
        or not parsed.netloc
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("Set the Worker URL to a valid HTTPS address in KingBlap Wizard settings.")
    return base.rstrip("/") + path


def _fetch(url, max_bytes, access_code=None):
    headers = {
        "User-Agent": "KingBlap-Wizard/1.0.66 Kodi",
        "Accept": "application/json",
    }
    if access_code:
        headers["Authorization"] = "Bearer {}".format(access_code)
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            length = response.headers.get("Content-Length")
            if length and int(length) > max_bytes:
                raise ValueError("The download is larger than the wizard limit.")
            data = response.read(max_bytes + 1)
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            raise AccessDenied("The access code was not accepted.")
        raise
    if len(data) > max_bytes:
        raise ValueError("The download is larger than the wizard limit.")
    return data


def _get_builds(access_code=None, public_build=False):
    if KODI_MAJOR == 21 and public_build:
        return [(KODI21_PUBLIC_BUILD_ID, KODI21_PUBLIC_BUILD_NAME)]
    if KODI_MAJOR == 22 and public_build:
        return [(KODI22_PUBLIC_BUILD_ID, KODI22_PUBLIC_BUILD_NAME)]
    if KODI_MAJOR not in (21, 22) and public_build:
        return []
    label = "public" if public_build else "private"
    content = _fetch(_api_url(BUILDS_PATH), 1024 * 1024, access_code).decode("utf-8-sig")
    payload = json.loads(content)
    if not isinstance(payload, dict) or not isinstance(payload.get("builds"), list):
        raise ValueError("The {} build list is not valid JSON.".format(label))
    builds = []
    seen = set()
    for entry in payload["builds"]:
        if not isinstance(entry, dict):
            raise ValueError("The {} build list contains an invalid entry.".format(label))
        build_id = entry.get("id")
        name = entry.get("name")
        if (
            not isinstance(build_id, str)
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}", build_id)
            or build_id in seen
            or not isinstance(name, str)
            or not name.strip()
            or len(name) > 120
            or any(ord(character) < 32 for character in name)
        ):
            raise ValueError("The {} build list contains an invalid entry.".format(label))
        seen.add(build_id)
        builds.append((build_id, name.strip()))
    return builds


def _valid_access_code(access_code):
    return bool(ACCESS_CODE_PATTERN.fullmatch(access_code))


def _private_build_kodi_major(build_id):
    if not isinstance(build_id, str):
        return None
    if build_id.startswith(KODI21_PRIVATE_BUILD_PREFIX):
        return 21
    if build_id.startswith(KODI22_PRIVATE_BUILD_PREFIX):
        return 22
    return None


def _safe_target(root, relative):
    if "\\" in relative or relative.startswith("/"):
        raise ValueError("The build archive contains an invalid path.")
    parts = relative.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise ValueError("The build archive contains an invalid path.")
    root = os.path.realpath(root)
    target = os.path.realpath(os.path.join(root, *parts))
    if os.path.commonpath((root, target)) != root or target == root:
        raise ValueError("The build archive contains an invalid path.")
    return target


def _remove_path(path):
    if os.path.islink(path) or os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)


def _format_storage_size(size):
    if size >= 1024 * 1024 * 1024:
        return "{:.1f} GB".format(size / float(1024 * 1024 * 1024))
    return "{} MB".format(max(1, int(size / float(1024 * 1024) + 0.5)))


def _check_pre_download_space(archive_bytes, local_archive=False):
    """Fail before writing a large archive when Kodi's storage is too full."""
    archive_bytes = max(0, int(archive_bytes))
    archive_copies = 3 if local_archive else 2
    required = (
        archive_copies * archive_bytes
        + PRE_DOWNLOAD_EXPANSION_RESERVE
        + INSTALL_SAFETY_RESERVE
    )
    free_space = shutil.disk_usage(_path("special://home")).free
    if free_space < required:
        raise OSError(
            "This device has {} free, but the installer needs about {} free to install safely. "
            "Free storage on the TV, then try again. No build files were downloaded.".format(
                _format_storage_size(free_space), _format_storage_size(required)
            )
        )


def _remove_stale_download(path):
    """Remove only the Wizard's own interrupted build archive before measuring space."""
    if not os.path.lexists(path):
        return
    if os.path.islink(path) or os.path.isfile(path):
        os.remove(path)
        _log("Removed an incomplete build archive left in the Wizard download folder.")
        return
    raise OSError("The Wizard download path is not a regular file; it was left untouched.")


def _remove_child(root, name):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
        raise ValueError("Refusing to remove an invalid add-on path.")
    root_real = os.path.realpath(root)
    target = os.path.abspath(os.path.join(root_real, name))
    if os.path.commonpath((root_real, target)) != root_real or target == root_real:
        raise ValueError("Refusing to remove a path outside Kodi's profile.")
    _remove_path(target)


def _write_transaction_journal(
    transaction, phase, operations, addon_states=None, post_commit_enable=None
):
    journal = os.path.join(transaction, "journal.json")
    temporary = journal + ".tmp"
    with open(temporary, "w", encoding="utf-8") as journal_file:
        json.dump({
            "version": 2,
            "phase": phase,
            "operations": operations,
            "addon_states": addon_states or {},
            "post_commit_enable": post_commit_enable or [],
        }, journal_file)
        journal_file.flush()
        os.fsync(journal_file.fileno())
    os.replace(temporary, journal)


def _write_transaction_commit_marker(transaction):
    marker = transaction + ".committed"
    temporary = marker + ".tmp"
    with open(temporary, "w", encoding="utf-8") as marker_file:
        marker_file.write("KingBlap build transaction committed\n")
        marker_file.flush()
        os.fsync(marker_file.fileno())
    os.replace(temporary, marker)


def _cleanup_transaction(transaction):
    _remove_path(transaction)
    _remove_path(transaction + ".committed")


def _swap_child(root, name, staged, backup, changes, journal_state=None, location=None):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
        raise ValueError("The build contains an invalid add-on ID.")
    root_real = os.path.realpath(root)
    target = os.path.abspath(os.path.join(root_real, name))
    if os.path.commonpath((root_real, target)) != root_real or target == root_real:
        raise ValueError("Refusing to replace a path outside Kodi's profile.")
    saved = None
    had_target = os.path.lexists(target)
    if journal_state is not None:
        if location not in ("addons", "addon_data", "skin_data", "weather_data"):
            raise ValueError("Refusing to journal an unknown Kodi profile location.")
        backup_relative = os.path.relpath(backup, journal_state["transaction"])
        if backup_relative.startswith("..") or os.path.isabs(backup_relative):
            raise ValueError("Refusing to journal a rollback path outside the transaction.")
        journal_state["operations"].append({
            "location": location,
            "parent": os.path.basename(root_real)
            if location in ("skin_data", "weather_data")
            else "",
            "name": name,
            "had_target": had_target,
            "backup": backup_relative.replace(os.sep, "/"),
        })
        _write_transaction_journal(
            journal_state["transaction"],
            "swapping",
            journal_state["operations"],
            journal_state.get("addon_states"),
            journal_state.get("post_commit_enable"),
        )
    if had_target:
        os.makedirs(os.path.dirname(backup), exist_ok=True)
        os.replace(target, backup)
        saved = backup
    changes.append((root_real, name, saved))
    if staged is not None:
        os.makedirs(os.path.dirname(target), exist_ok=True)
        os.replace(staged, target)


def _restore_children(changes):
    restored = True
    for root, name, backup in reversed(changes):
        try:
            _remove_child(root, name)
            if backup and os.path.lexists(backup):
                os.replace(backup, os.path.join(root, name))
        except OSError as exc:
            restored = False
            _log("Could not restore add-on {}: {}".format(name, exc), xbmc.LOGERROR)
    return restored


def _write_member(archive, info, destination):
    parent = os.path.dirname(destination)
    if not xbmcvfs.mkdirs(parent) and not os.path.isdir(parent):
        raise OSError("Kodi could not create the staged folder for {}.".format(info.filename))

    def remove_directory_conflict():
        if os.path.isdir(destination):
            shutil.rmtree(destination)
            return True
        if xbmcvfs.exists(destination.rstrip("/\\") + "/"):
            if xbmcvfs.rmdir(destination.rstrip("/\\") + "/", True):
                return True
            raise OSError("Kodi could not remove a staged folder that conflicts with {}.".format(
                info.filename
            ))
        return False

    remove_directory_conflict()
    with archive.open(info, "r") as source:
        for attempt in range(3):
            output = None
            try:
                output = xbmcvfs.File(destination, "w")
                bytes_written = 0
                while True:
                    block = source.read(CHUNK_SIZE)
                    if not block:
                        break
                    if not output.write(block):
                        raise IOError("Kodi could not write {}.".format(info.filename))
                    bytes_written += len(block)
                if bytes_written != info.file_size:
                    raise IOError("Kodi wrote an incomplete staged file: {}.".format(info.filename))
            except Exception:
                if output is not None:
                    output.close()
                if attempt == 2:
                    raise
                remove_directory_conflict()
                source.seek(0)
                time.sleep(0.1)
            else:
                output.close()
                return


def _required_external_dependencies(archive, packages):
    dependencies = set()
    for addon_id in packages:
        manifest_path = "addons/{}/addon.xml".format(addon_id)
        root = ET.fromstring(archive.read(manifest_path))
        for dependency in root.findall("requires/import"):
            dependency_id = dependency.get("addon", "")
            if (
                dependency_id
                and dependency.get("optional", "false").lower() != "true"
                and not dependency_id.startswith(("xbmc.", "kodi."))
                and dependency_id not in packages
            ):
                dependencies.add(dependency_id)
    return sorted(dependencies)


def _validate_archive(archive, expected_public=None):
    total = 0
    packages = {}
    build_info = None
    profile_addon_data_ids = set()
    skin_settings_found = False
    weather_settings_found = False
    seen_names = set()
    folded_paths = set()
    file_paths = set()
    for info in archive.infolist():
        if info.is_dir():
            continue
        name = info.filename
        if name in seen_names:
            raise ValueError("The build archive contains a duplicate file path.")
        seen_names.add(name)
        portable = "/".join(
            part.rstrip(" .").casefold() for part in name.split("/")
        )
        if portable in folded_paths:
            raise ValueError("The build archive contains paths that collide on case-insensitive filesystems.")
        folded_paths.add(portable)
        parts = portable.split("/")
        if any("/".join(parts[:index]) in file_paths for index in range(1, len(parts))):
            raise ValueError("The build archive uses a file as a directory.")
        if any(
            "/".join(parts[:index]) in folded_paths
            for index in range(1, len(parts))
        ):
            raise ValueError("The build archive uses a file as a directory.")
        file_paths.add(portable)
        if name == "build_info.json":
            try:
                build_info = json.loads(archive.read(info).decode("utf-8-sig"))
            except (UnicodeDecodeError, ValueError) as exc:
                raise ValueError("The build information file is not valid JSON: {}".format(exc))
            if not isinstance(build_info, dict):
                raise ValueError("The build information file must contain a JSON object.")
        elif name == SKIN_SETTINGS_ARCHIVE_PATH:
            try:
                settings = ET.fromstring(archive.read(info))
            except ET.ParseError:
                raise ValueError("The build archive's Xonfluence skin settings are not valid XML.")
            if settings.tag != "settings" or not settings.findall("setting"):
                raise ValueError("The build archive's Xonfluence skin settings are empty or invalid.")
            skin_settings_found = True
            profile_addon_data_ids.add(SKIN_ID)
        elif name == WEATHER_SETTINGS_ARCHIVE_PATH:
            try:
                settings = ET.fromstring(archive.read(info))
            except ET.ParseError:
                raise ValueError("The build archive's Gismeteo settings are not valid XML.")
            values = {
                setting.get("id"): setting.text or ""
                for setting in settings.findall("setting")
            } if settings.tag == "settings" else {}
            if (
                values.get("CurrentLocation", "").casefold() != "false"
                or values.get("Location1") != WEATHER_LOCATION
                or values.get("Location1ID") != WEATHER_LOCATION_ID
            ):
                raise ValueError("The build archive does not select Thomasville, North Carolina in Gismeteo.")
            weather_settings_found = True
            profile_addon_data_ids.add(WEATHER_ID)
        elif name.startswith("userdata/addon_data/"):
            relative = name[len("userdata/addon_data/"):]
            parts = relative.split("/")
            if (
                len(parts) < 2
                or not re.fullmatch(r"[A-Za-z0-9_.-]+", parts[0])
        or parts[0] in (
            ADDON_ID,
            "plugin.video.xstream-player",
            ONEPLAY_REPO_ID,
            LEGACY_SKIN_ID,
            PREVIOUS_SKIN_ID,
        )
            ):
                raise ValueError("The build archive contains an invalid add-on profile path.")
            _safe_target("/build/userdata/addon_data", relative)
            profile_addon_data_ids.add(parts[0])
        elif name.startswith("addons/"):
            relative = name[len("addons/"):]
            parts = relative.split("/")
            if len(parts) < 2 or not re.fullmatch(r"[A-Za-z0-9_.-]+", parts[0]):
                raise ValueError("The build archive contains an invalid add-on path.")
            if parts[0] in ("plugin.video.xstream-player", ONEPLAY_REPO_ID):
                raise ValueError("The build archive contains an add-on that should be removed.")
            _safe_target("/build/addons", relative)
            if parts[-1] == "addon.xml" and len(parts) == 2:
                root = ET.fromstring(archive.read(info))
                addon_id = root.get("id", "")
                if addon_id != parts[0]:
                    raise ValueError("An add-on folder does not match its add-on ID.")
                packages[addon_id] = root.get("version", "")
        else:
            raise ValueError("The build archive contains an unexpected file.")
        total += info.file_size
        if total > BUILD_LIMIT:
            raise ValueError("The expanded build is larger than the wizard limit.")
        mode = (info.external_attr >> 16) & 0xFFFF
        if mode & 0o170000 == 0o120000:
            raise ValueError("Symbolic links are not accepted in the build archive.")
    for path in file_paths:
        parts = path.split("/")
        if any("/".join(parts[:index]) in file_paths for index in range(1, len(parts))):
            raise ValueError("The build archive uses a file as a directory.")
    if (
        packages.get("plugin.video.giptv") not in ("3.1.0", "3.1.1", "3.1.2", "3.1.3")
        and packages.get("plugin.video.xstream-pro") not in ("1.1.2", "1.1.4")
    ):
        raise ValueError("The build archive does not contain a supported IPTV add-on.")
    expected_skin_version = SKIN_VERSION
    if (
        build_info
        and build_info.get("distribution") == "private"
        and build_info.get("pvr_channel_view") == "preview-list"
    ):
        expected_skin_version = {21: "5.1", 22: "6.0.8"}.get(KODI_MAJOR, SKIN_VERSION)
    if packages.get(SKIN_ID) != expected_skin_version:
        raise ValueError("The build archive does not contain the Xonfluence skin for Kodi {}.".format(KODI_MAJOR))
    if packages.get(WEATHER_ID) != WEATHER_VERSION:
        raise ValueError("The build archive is missing the Gismeteo weather add-on.")
    if LEGACY_SKIN_ID in packages:
        raise ValueError("The build archive still contains Estuary MOD V2.")
    for addon_id in (
        "script.favourites",
        "script.image.resource.select",
        "script.module.requests",
    ):
        if addon_id not in packages:
            raise ValueError("The build archive is missing a required add-on: {}.".format(addon_id))
    skin_manifest = ET.fromstring(archive.read("addons/{}/addon.xml".format(SKIN_ID)))
    for dependency in skin_manifest.findall("requires/import"):
        dependency_id = dependency.get("addon", "")
        if dependency_id and not dependency_id.startswith("xbmc.") and dependency_id not in packages:
            raise ValueError("The build archive is missing the skin dependency: {}.".format(dependency_id))
    if build_info is None:
        raise ValueError("The build archive is missing its build information.")
    if build_info.get("kodi_major") != KODI_MAJOR:
        raise ValueError(
            "This build is for Kodi {}, but this device is running Kodi {}.".format(
                build_info.get("kodi_major", "unknown"), KODI_MAJOR
            )
        )
    if build_info.get("skin") != SKIN_ID:
        raise ValueError("The build archive selects a skin that does not match this Kodi release.")
    distribution = build_info.get("distribution")
    if expected_public is True and (
        distribution != "public"
        or build_info.get("profile_data_mode") != "settings-only"
    ):
        raise ValueError("The public download contains private profile data or has no public marker.")
    if expected_public is False and distribution == "public":
        raise ValueError("The selected private route returned a public build.")
    declared_addons = build_info.get("addons")
    if (
        not isinstance(declared_addons, list)
        or any(
            not isinstance(addon_id, str)
            or not re.fullmatch(r"[A-Za-z0-9_.-]+", addon_id)
            for addon_id in declared_addons
        )
        or set(declared_addons) != set(packages)
    ):
        raise ValueError("The build information does not match the packaged add-ons.")
    platform_addons = build_info.get("excluded_platform_addons", [])
    if not isinstance(platform_addons, list) or any(
        not isinstance(addon_id, str)
        or not re.fullmatch(r"[A-Za-z0-9_.-]+", addon_id)
        for addon_id in platform_addons
    ):
        raise ValueError("The build information contains an invalid platform-specific add-on ID.")
    removed_addons = build_info.get("removed_addons", [])
    if not isinstance(removed_addons, list) or any(
        not isinstance(addon_id, str)
        or not re.fullmatch(r"[A-Za-z0-9_.-]+", addon_id)
        for addon_id in removed_addons
    ):
        raise ValueError("The build information contains an invalid removed add-on ID.")
    if ONEPLAY_REPO_ID not in removed_addons or set(removed_addons) & set(packages):
        raise ValueError("The build must remove the OnePlay repository and cannot package removed add-ons.")
    if not skin_settings_found:
        raise ValueError("The build archive is missing its Xonfluence skin settings file.")
    if not weather_settings_found:
        raise ValueError("The build archive is missing its Thomasville Gismeteo settings.")
    if (
        build_info.get("weather_addon") != WEATHER_ID
        or build_info.get("weather_location") != "Thomasville, North Carolina"
        or build_info.get("weather_location_id") != WEATHER_LOCATION_ID
    ):
        raise ValueError("The build information does not identify the Thomasville, North Carolina weather setup.")
    skin_colors = build_info.get("skin_colors")
    skin_font = build_info.get("skin_font")
    screensaver_addon = build_info.get("screensaver_addon")
    builtin_dim_screensaver = screensaver_addon == BUILTIN_DIM_SCREENSAVER_ID
    if screensaver_addon is not None and (
        not isinstance(screensaver_addon, str)
        or not re.fullmatch(r"[A-Za-z0-9_.-]+", screensaver_addon)
        or (screensaver_addon not in packages and not builtin_dim_screensaver)
        or (builtin_dim_screensaver and expected_public)
    ):
        raise ValueError("The build information selects a screensaver that is not packaged.")
    if screensaver_addon is not None and not builtin_dim_screensaver:
        screensaver_manifest = ET.fromstring(
            archive.read("addons/{}/addon.xml".format(screensaver_addon))
        )
        if not any(
            extension.get("point") == "xbmc.ui.screensaver"
            for extension in screensaver_manifest.findall("extension")
        ):
            raise ValueError("The build's selected add-on is not a Kodi screensaver.")
    auto_update_addons = build_info.get("auto_update_addons")
    if auto_update_addons is not None and not isinstance(auto_update_addons, bool):
        raise ValueError("The build information contains an invalid add-on update setting.")
    appearance_declared = skin_colors is not None or skin_font is not None
    if distribution == "private" or appearance_declared:
        if (
            not isinstance(skin_colors, str)
            or not re.fullmatch(r"[A-Za-z0-9_. -]+", skin_colors)
            or "addons/{}/colors/{}.xml".format(SKIN_ID, skin_colors).casefold() not in file_paths
        ):
            raise ValueError("The build does not include its selected Xonfluence color palette.")
        if not isinstance(skin_font, str) or not re.fullmatch(r"[A-Za-z0-9_. -]+", skin_font):
            raise ValueError("The build does not identify a valid Xonfluence font.")
        try:
            font_xml = ET.fromstring(archive.read("addons/{}/xml/Font.xml".format(SKIN_ID)))
        except (KeyError, ET.ParseError):
            raise ValueError("The build is missing its Xonfluence font definitions.")
        font_ids = {
            fontset.get("id")
            for fontset in font_xml.findall("fontset")
            if fontset.get("id")
        } if font_xml.tag == "fonts" else set()
        if skin_font not in font_ids:
            raise ValueError("The build's selected font is not defined by Xonfluence.")
    profile_mode = build_info.get("profile_data_mode", "settings-only")
    if profile_mode not in ("settings-only", PROFILE_DATA_MODE):
        raise ValueError("The build information contains an unsupported add-on profile mode.")
    declared_profile_ids = build_info.get("profile_addon_data_ids", [])
    if not isinstance(declared_profile_ids, list) or any(
        not isinstance(addon_id, str)
        or not re.fullmatch(r"[A-Za-z0-9_.-]+", addon_id)
        or addon_id in (
            ADDON_ID,
            "plugin.video.xstream-player",
            ONEPLAY_REPO_ID,
            LEGACY_SKIN_ID,
            PREVIOUS_SKIN_ID,
        )
        for addon_id in declared_profile_ids
    ):
        raise ValueError("The build information contains an invalid profile add-on ID.")
    if profile_mode == PROFILE_DATA_MODE:
        if (
            set(declared_profile_ids) != profile_addon_data_ids
            or SKIN_ID not in profile_addon_data_ids
            or WEATHER_ID not in profile_addon_data_ids
        ):
            raise ValueError("The build profile data list does not match the archived add-on data.")
    elif profile_addon_data_ids != {SKIN_ID, WEATHER_ID} or declared_profile_ids:
        raise ValueError("The settings-only build contains unexpected add-on profile data.")
    reset_addon_data_ids = build_info.get("reset_addon_data_ids", [])
    if (
        not isinstance(reset_addon_data_ids, list)
        or any(
            not isinstance(addon_id, str)
            or not re.fullmatch(r"[A-Za-z0-9_.-]+", addon_id)
            or addon_id in (
                ADDON_ID,
                "plugin.video.xstream-player",
                ONEPLAY_REPO_ID,
                LEGACY_SKIN_ID,
                PREVIOUS_SKIN_ID,
            )
            for addon_id in reset_addon_data_ids
        )
        or len(reset_addon_data_ids) != len(set(reset_addon_data_ids))
        or set(reset_addon_data_ids) & profile_addon_data_ids
        or not set(reset_addon_data_ids).issubset(packages)
        or (reset_addon_data_ids and profile_mode != PROFILE_DATA_MODE)
        or (expected_public is True and reset_addon_data_ids)
    ):
        raise ValueError("The build information contains invalid add-on profile reset IDs.")
    giptv_id = "plugin.video.giptv"
    if (
        build_info.get("distribution") == "private"
        and profile_mode == PROFILE_DATA_MODE
        and giptv_id in packages
    ):
        if PVR_ADDON_ID not in profile_addon_data_ids or PVR_ADDON_ID not in platform_addons:
            raise ValueError("The private GIPTV build is missing IPTV Simple profile or platform data.")
        pvr_prefix = "userdata/addon_data/{}/".format(PVR_ADDON_ID)
        pvr_instances = [
            name for name in archive.namelist()
            if re.fullmatch(re.escape(pvr_prefix) + r"instance-settings-\d+\.xml", name)
        ]
        if len(pvr_instances) != 1:
            raise ValueError("The private build must contain one IPTV Simple GIPTV instance.")
        try:
            pvr_settings = ET.fromstring(archive.read(pvr_instances[0]))
        except ET.ParseError:
            raise ValueError("The private IPTV Simple settings are not valid XML.")
        pvr_values = {
            setting.get("id"): (setting.text or "").strip()
            for setting in pvr_settings.findall("setting")
        } if pvr_settings.tag == "settings" else {}
        expected_playlist_path = (
            "special://profile/addon_data/{}/iptv_simple/playlist.m3u8".format(giptv_id)
        )
        if (
            pvr_values.get("kodi_addon_instance_name") != "GIPTV"
            or pvr_values.get("kodi_addon_instance_enabled", "true").casefold() != "true"
            or pvr_values.get("m3uPathType") != "0"
            or pvr_values.get("m3uPath") != expected_playlist_path
        ):
            raise ValueError("The private IPTV Simple instance does not use GIPTV's local playlist.")
        export_prefix = "userdata/addon_data/{}/iptv_simple/".format(giptv_id)
        export_paths = {
            "playlist": export_prefix + "playlist.m3u8",
            "epg": export_prefix + "epg.xml",
            "state": export_prefix + "sync_state.json",
        }
        if any(path not in seen_names for path in export_paths.values()):
            raise ValueError("The private build is missing a GIPTV startup export file.")
        try:
            playlist_text = archive.read(export_paths["playlist"]).decode("utf-8")
            epg_text = archive.read(export_paths["epg"]).decode("utf-8")
            sync_state = json.loads(archive.read(export_paths["state"]).decode("utf-8-sig"))
            epg_root = ET.fromstring(epg_text)
        except (UnicodeDecodeError, ValueError, ET.ParseError):
            raise ValueError("The private GIPTV startup exports are not valid text data.")
        group_titles = re.findall(
            r'(?im)^#EXTINF:[^\r\n]*?group-title="([^"]*)"', playlist_text
        )
        playlist_entries = len(re.findall(r"(?im)^#EXTINF:", playlist_text))
        playlist_epg_ids = {
            html.unescape(value).strip()
            for value in re.findall(r'(?im)^#EXTINF:[^\r\n]*?tvg-id="([^"]*)"', playlist_text)
            if value.strip()
        }
        guide_entries_valid = epg_root.tag == "tv"
        if guide_entries_valid:
            for element in epg_root:
                element_name = element.tag.rsplit("}", 1)[-1]
                if element_name == "channel":
                    guide_id = (element.get("id") or "").strip()
                elif element_name == "programme":
                    guide_id = (element.get("channel") or "").strip()
                else:
                    guide_entries_valid = False
                    break
                if not guide_id or guide_id not in playlist_epg_ids:
                    guide_entries_valid = False
                    break
        if (
            playlist_entries < 1
            or len(group_titles) != playlist_entries
            or len(playlist_epg_ids) < 1
            or any(
                not re.match(r"^(usa|24/7)\s*\|", title.strip(), re.I)
                for title in group_titles
            )
            or not guide_entries_valid
        ):
            raise ValueError("The private GIPTV exports must contain only USA/24/7 groups and a guide limited to those channels.")
        if (
            not isinstance(sync_state, dict)
            or sync_state.get("playlist_sha256") != hashlib.sha256(playlist_text.encode("utf-8")).hexdigest()
            or sync_state.get("epg_sha256") != hashlib.sha256(epg_text.encode("utf-8")).hexdigest()
            or not isinstance(sync_state.get("last_sync"), int)
        ):
            raise ValueError("The private GIPTV sync state does not match its packaged playlist and guide.")
    if (
        build_info.get("kodi_major") == 22
        and build_info.get("distribution") == "private"
        and build_info.get("version") in ("1.0.26", "1.0.28")
    ):
        xstream_id = "plugin.video.xstream-pro"
        giptv_id = "plugin.video.giptv"
        expected_xstream_version = {
            "1.0.26": "1.1.2",
            "1.0.28": "1.1.4",
        }.get(build_info.get("version"))
        if (
            packages.get(xstream_id) != expected_xstream_version
            or giptv_id in packages
            or giptv_id not in removed_addons
            or xstream_id not in profile_addon_data_ids
            or giptv_id in profile_addon_data_ids
        ):
            raise ValueError("The private build does not contain the expected XStream Pro package and migration.")
        try:
            xstream_settings = ET.fromstring(
                archive.read("userdata/addon_data/{}/settings.xml".format(xstream_id))
            )
        except (KeyError, ET.ParseError):
            raise ValueError("The private build is missing valid XStream Pro settings.")
        xstream_values = {
            setting.get("id"): (setting.text or "").strip()
            for setting in xstream_settings.findall("setting")
        } if xstream_settings.tag == "settings" else {}
        if not all(xstream_values.get(setting) for setting in (
            "profile_1_xtream_url",
            "profile_1_xtream_username",
            "profile_1_xtream_password",
        )) or xstream_values.get("profile_1_source_type") != "Xtream Codes":
            raise ValueError("The private build is missing its migrated Xtream Profile 1 credentials.")
    return (
        total,
        packages,
        sorted(set(platform_addons)),
        sorted(set(removed_addons)),
        profile_mode,
        sorted(profile_addon_data_ids) if profile_mode == PROFILE_DATA_MODE else [],
        sorted(reset_addon_data_ids),
        skin_colors,
        skin_font,
        screensaver_addon,
        auto_update_addons is True,
    )


def _prime_giptv_startup_state(staged_userdata):
    """Use packaged exports unless an empty guide needs its first background sync."""
    giptv_data = os.path.join(staged_userdata, "addon_data", "plugin.video.giptv", "iptv_simple")
    playlist_path = os.path.join(giptv_data, "playlist.m3u8")
    epg_path = os.path.join(giptv_data, "epg.xml")
    state_path = os.path.join(giptv_data, "sync_state.json")
    with open(playlist_path, "rb") as source:
        playlist_text = source.read().decode("utf-8")
    with open(epg_path, "rb") as source:
        epg_text = source.read().decode("utf-8")
    has_programmes = False
    try:
        for _, element in ET.iterparse(epg_path, events=("end",)):
            if element.tag.rsplit("}", 1)[-1] == "programme":
                has_programmes = True
                break
    except (OSError, ET.ParseError):
        has_programmes = False
    state = {
        "last_sync": int(time.time()) if has_programmes else 0,
        "playlist_sha256": hashlib.sha256(playlist_text.encode("utf-8")).hexdigest(),
        "epg_sha256": hashlib.sha256(epg_text.encode("utf-8")).hexdigest(),
    }
    with open(state_path, "w", encoding="utf-8") as destination:
        json.dump(state, destination, separators=(",", ":"))
        destination.write("\n")


def _download_public_archive(destination, progress, build_id):
    if build_id == KODI21_PUBLIC_BUILD_ID:
        parts = KODI21_PUBLIC_BUILD_PARTS
        expected_sha256 = KODI21_PUBLIC_BUILD_SHA256
        build_label = "Kodi 21.3"
    elif build_id == KODI22_PUBLIC_BUILD_ID:
        parts = KODI22_PUBLIC_BUILD_PARTS
        expected_sha256 = KODI22_PUBLIC_BUILD_SHA256
        build_label = "Kodi 22"
    else:
        raise ValueError("The selected public build is not valid.")
    total_expected = sum(size for _, size in parts)
    _check_pre_download_space(total_expected)
    total_written = 0
    with open(destination, "wb") as output:
        for part_index, (url, expected_part_size) in enumerate(parts):
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "KingBlap-Wizard/1.0.66 Kodi",
                    "Accept": "application/octet-stream",
                },
            )
            part_written = 0
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    length = response.headers.get("Content-Length")
                    if length and int(length) != expected_part_size:
                        raise IOError("A public build part has an unexpected size.")
                    while True:
                        if progress.iscanceled():
                            raise InterruptedError("Build installation was cancelled.")
                        block = response.read(CHUNK_SIZE)
                        if not block:
                            break
                        part_written += len(block)
                        total_written += len(block)
                        if part_written > expected_part_size or total_written > DOWNLOAD_LIMIT:
                            raise ValueError("The public build download is larger than expected.")
                        output.write(block)
                        percent = int(total_written * 100 / total_expected)
                        progress.update(
                            min(percent, 99),
                            "Downloading public build part {} of {}…".format(
                                part_index + 1, len(parts)
                            ),
                        )
            except urllib.error.HTTPError as exc:
                if exc.code == 404:
                    raise ValueError("A public build part is not available yet.")
                raise
            if part_written != expected_part_size:
                raise IOError("A public build part was incomplete.")
    if total_written != total_expected:
        raise IOError("The public build download was incomplete.")
    if expected_sha256:
        digest = hashlib.sha256()
        with open(destination, "rb") as downloaded:
            while True:
                block = downloaded.read(CHUNK_SIZE)
                if not block:
                    break
                digest.update(block)
        if digest.hexdigest().upper() != expected_sha256:
            raise IOError("The {} public build download failed its integrity check.".format(build_label))


def _download_archive(build_id, destination, progress, access_code=None, public_build=False):
    if public_build:
        if build_id not in (KODI21_PUBLIC_BUILD_ID, KODI22_PUBLIC_BUILD_ID):
            raise ValueError("The selected public build is not valid.")
        _download_public_archive(destination, progress, build_id)
        return
    route = "/v1/builds"
    url = _api_url(
        "{}/{}/download".format(route, urllib.parse.quote(build_id, safe=""))
    )
    headers = {
        "User-Agent": "KingBlap-Wizard/1.0.66 Kodi",
        "Accept": "application/zip",
    }
    if access_code:
        headers["Authorization"] = "Bearer {}".format(access_code)
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            length = response.headers.get("Content-Length")
            expected = int(length) if length else None
            if expected and expected > DOWNLOAD_LIMIT:
                raise ValueError("The build download is larger than the wizard limit.")
            _check_pre_download_space(expected if expected is not None else DOWNLOAD_LIMIT)
            written = 0
            with open(destination, "wb") as output:
                while True:
                    if progress.iscanceled():
                        raise InterruptedError("Build installation was cancelled.")
                    block = response.read(CHUNK_SIZE)
                    if not block:
                        break
                    written += len(block)
                    if written > DOWNLOAD_LIMIT:
                        raise ValueError("The build download is larger than the wizard limit.")
                    output.write(block)
                    percent = int(written * 100 / expected) if expected else 0
                    progress.update(min(percent, 99), "Downloading build…")
            if expected and written != expected:
                raise IOError("The build download was incomplete.")
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            raise AccessDenied("The access code was not accepted.")
        if exc.code == 404:
            raise ValueError("The selected build is not available.")
        raise


def _jsonrpc(method, params):
    request = json.dumps({
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1,
    })
    response = json.loads(xbmc.executeJSONRPC(request))
    if "error" in response:
        error = response["error"]
        detail = error.get("data", {})
        stack = detail.get("stack", {}) if isinstance(detail, dict) else {}
        explanation = stack.get("message") if isinstance(stack, dict) else None
        if not explanation and isinstance(detail, dict):
            explanation = detail.get("message")
        message = "{} failed: {}".format(
            method,
            error.get("message", "Kodi could not complete the request."),
        )
        if explanation:
            message += " ({})".format(explanation)
        if error.get("code") is not None:
            message += " [Kodi error {}]".format(error["code"])
        raise RuntimeError(message)
    return response.get("result")


def _get_setting(setting):
    result = _jsonrpc("Settings.GetSettingValue", {"setting": setting})
    if not isinstance(result, dict) or "value" not in result:
        raise RuntimeError("Kodi could not read the {} setting.".format(setting))
    return result["value"]


def _set_setting(setting, value):
    result = _jsonrpc("Settings.SetSettingValue", {"setting": setting, "value": value})
    if result is not True:
        raise RuntimeError("Kodi could not apply the {} setting.".format(setting))


def _read_weather_addon_settings():
    try:
        addon = xbmcaddon.Addon(WEATHER_ID)
    except RuntimeError:
        return None
    return {
        setting: addon.getSetting(setting)
        for setting in WEATHER_ADDON_SETTINGS
    }


def _write_weather_addon_settings(values):
    addon = xbmcaddon.Addon(WEATHER_ID)
    for setting, value in values.items():
        addon.setSetting(setting, value)
    for setting, value in values.items():
        if addon.getSetting(setting) != value:
            raise RuntimeError("Kodi could not apply the {} Gismeteo setting.".format(setting))


def _enable_addon(addon_id):
    result = _jsonrpc("Addons.SetAddonEnabled", {
        "addonid": addon_id,
        "enabled": True,
    })
    if result not in (True, "OK"):
        raise RuntimeError("Kodi could not enable the {} add-on.".format(addon_id))
    details = _jsonrpc("Addons.GetAddonDetails", {
        "addonid": addon_id,
        "properties": ["enabled"],
    }).get("addon", {})
    if details.get("enabled") is not True:
        raise RuntimeError("Kodi did not confirm that the {} add-on is enabled.".format(addon_id))


def _get_addon_enabled(addon_id):
    result = _jsonrpc("Addons.GetAddons", {
        "properties": ["enabled"],
        "enabled": "all",
    })
    for addon in result.get("addons", []):
        if addon.get("addonid") == addon_id:
            enabled = addon.get("enabled")
            if isinstance(enabled, bool):
                return enabled
            raise RuntimeError("Kodi could not read the {} add-on state.".format(addon_id))
    return None


def _set_addon_enabled(addon_id, enabled):
    result = _jsonrpc("Addons.SetAddonEnabled", {
        "addonid": addon_id,
        "enabled": enabled,
    })
    action = "enable" if enabled else "disable"
    if result not in (True, "OK"):
        raise RuntimeError("Kodi could not {} the {} add-on.".format(action, addon_id))
    state = _get_addon_enabled(addon_id)
    if state is not enabled:
        action = "enabled" if enabled else "disabled"
        raise RuntimeError("Kodi did not confirm that the {} add-on is {}.".format(addon_id, action))


def _pause_install_addon(addon_id, journal_state, original_states):
    """Pause a heavy background add-on and save its prior state before changing it."""
    enabled = _get_addon_enabled(addon_id)
    if not isinstance(enabled, bool):
        return None
    original_states[addon_id] = enabled
    journal_state["addon_states"][addon_id] = enabled
    _write_transaction_journal(
        journal_state["transaction"],
        "staging",
        journal_state["operations"],
        journal_state["addon_states"],
        journal_state.get("post_commit_enable"),
    )
    if enabled:
        _set_addon_enabled(addon_id, False)
        xbmc.sleep(1500)
    return enabled


def _confirm_skin_keep_prompt():
    if xbmcgui.getCurrentWindowDialogId() != 10100:
        return False
    try:
        dialog = xbmcgui.Window(10100)
        heading = dialog.getControl(1).getLabel().strip().casefold()
        message = dialog.getControl(9).getText().strip().casefold()
    except (AttributeError, RuntimeError, TypeError):
        return False
    prompt_text = "{} {}".format(heading, message)
    if "keep" not in prompt_text or not (
        "skin" in heading or "keep this change" in message or "keep this skin" in prompt_text
    ):
        return False
    xbmc.executebuiltin("SendClick(10100,11)", True)
    _log("Confirmed Kodi's keep-skin prompt: {}".format(heading))
    return True


def _activate_skin(skin_id):
    previous_skin = _get_setting("lookandfeel.skin")
    _set_setting("lookandfeel.skin", skin_id)
    if previous_skin == skin_id and xbmc.getSkinDir() != skin_id:
        xbmc.executebuiltin("ReloadSkin", True)
    stable_reads = 0
    stable_since = None
    for unused in range(SKIN_LOAD_TIMEOUT * 2):
        xbmc.sleep(500)
        _confirm_skin_keep_prompt()
        if (
            _get_setting("lookandfeel.skin") == skin_id
            and xbmc.getSkinDir() == skin_id
        ):
            stable_reads += 1
            if stable_since is None:
                stable_since = time.time()
            if (
                stable_reads >= 3
                and time.time() - stable_since >= SKIN_CONFIRMATION_GRACE
            ):
                return
        else:
            stable_reads = 0
            stable_since = None
    raise RuntimeError(
        "Kodi could not load the {} skin. The previous skin will be restored.".format(skin_id)
    )


def _confirm_kodi_addon_prompt(addon_id, progress):
    if xbmcgui.getCurrentWindowDialogId() != 10100:
        return False
    try:
        dialog = xbmcgui.Window(10100)
        heading = dialog.getControl(1).getLabel().strip().casefold()
        message = dialog.getControl(9).getText().strip().casefold()
    except (AttributeError, RuntimeError, TypeError):
        return False
    if heading != "add-on required" or "would you like to download this add-on?" not in message:
        return False
    progress.update(
        93,
        "KingBlap Wizard",
        "Confirming Kodi's compatible component for {}…".format(addon_id),
    )
    xbmc.executebuiltin("SendClick(10100,11)", True)
    _log("Accepted Kodi's required add-on prompt for {}.".format(addon_id))
    return True


def _wait_for_addon_registration(addon_ids, progress, confirm_required_addon=False):
    pending = set(addon_ids)
    started = time.monotonic()
    deadline = started + ADDON_REGISTRATION_TIMEOUT
    while pending and time.monotonic() < deadline:
        # Handle Kodi's confirmation dialog before querying JSON-RPC. A modal
        # dialog can block Kodi's add-on work while the wizard waits here.
        if confirm_required_addon:
            _confirm_kodi_addon_prompt(sorted(pending)[0], progress)
        start_index = 0
        page_size = 250
        while pending:
            try:
                result = _jsonrpc("Addons.GetAddons", {
                    "enabled": "all",
                    "properties": ["version"],
                    "limits": {"start": start_index, "end": start_index + page_size},
                })
            except RuntimeError:
                break
            addons = result.get("addons", []) if isinstance(result, dict) else []
            limits = result.get("limits", {}) if isinstance(result, dict) else {}
            total = limits.get("total") if isinstance(limits, dict) else None
            for addon in addons:
                if addon.get("addonid") in pending and addon.get("version"):
                    pending.discard(addon["addonid"])
            if (
                not pending
                or not addons
                or (
                    isinstance(total, int)
                    and start_index + len(addons) >= total
                )
                or (total is None and len(addons) < page_size)
            ):
                break
            start_index += len(addons)
        if pending:
            elapsed = int(time.monotonic() - started)
            progress.update(
                94 + min(2, elapsed // 15),
                "KingBlap Wizard",
                "Waiting for Kodi to register required add-ons ({}s): {}".format(
                    elapsed, ", ".join(sorted(pending))
                ),
            )
            xbmc.sleep(1000)
    if pending:
        raise RuntimeError(
            "Kodi did not finish registering these required add-ons after {} minutes: {}. "
            "The build files were rolled back; restart Kodi and try again.".format(
                ADDON_REGISTRATION_TIMEOUT // 60, ", ".join(sorted(pending))
            )
        )


def _enable_build_addons(addon_ids, progress, deferred=()):
    addon_ids = sorted(set(addon_ids) - set(deferred))
    failures = []
    total = max(1, len(addon_ids))
    for index, addon_id in enumerate(addon_ids, 1):
        try:
            _enable_addon(addon_id)
        except Exception as exc:
            failures.append((addon_id, str(exc)))
        if index == total or index % 4 == 0:
            progress.update(
                96 + int(index * 1 / total),
                "KingBlap Wizard",
                "Enabling add-ons ({}/{}): {}".format(index, total, addon_id),
            )
    if failures:
        details = "; ".join("{}: {}".format(addon_id, reason) for addon_id, reason in failures[:8])
        if len(failures) > 8:
            details += "; and {} more".format(len(failures) - 8)
        raise RuntimeError("Kodi could not enable every packaged add-on. {}".format(details))


def _ensure_kodi_managed_addon(addon_id, progress, enable=True):
    try:
        _jsonrpc("Addons.GetAddonDetails", {
            "addonid": addon_id,
            "properties": ["version", "enabled"],
        })
    except RuntimeError:
        _log("Installing required Kodi repository dependency {}.".format(addon_id))
        progress.update(
            93,
            "KingBlap Wizard",
            "Requesting a {} compatible component: {}".format(_platform_name(), addon_id),
        )
        # Do not wait inside InstallAddon: Kodi can present a required-add-on
        # prompt, and the wizard must keep polling to recognize and confirm it.
        xbmc.executebuiltin("InstallAddon({})".format(addon_id), False)
        _wait_for_addon_registration((addon_id,), progress, confirm_required_addon=True)
    if enable:
        _enable_addon(addon_id)
    elif _get_addon_enabled(addon_id) is True:
        _set_addon_enabled(addon_id, False)
        xbmc.sleep(1500)


def _apply_skin_settings():
    # Preserve the device's Kodi display preferences while activating its new skin.
    _activate_skin(SKIN_ID)


def _request_skin_reapply():
    marker_dir = os.path.join(_path("special://profile/addon_data"), ADDON_ID)
    os.makedirs(marker_dir, exist_ok=True)
    marker = os.path.join(marker_dir, "skin-reapply.json")
    temporary = marker + ".tmp"
    with open(temporary, "w", encoding="utf-8") as marker_file:
        json.dump({"skin": SKIN_ID, "requested": time.time()}, marker_file)
    os.replace(temporary, marker)


def _copy_local_archive(source_path, destination, progress):
    """Copy a user-selected build ZIP from a local path or Kodi VFS source."""
    source_path = (source_path or "").strip()
    if not source_path.lower().endswith(".zip"):
        raise ValueError("Choose a Kodi build .zip archive.")
    translated = xbmcvfs.translatePath(source_path)
    if os.path.isfile(translated):
        size = os.path.getsize(translated)
        if size > DOWNLOAD_LIMIT:
            raise ValueError("The selected build archive is larger than the wizard limit.")
        shutil.copyfile(translated, destination)
        progress.update(5, "Reading the selected build archive…")
        return
    source = xbmcvfs.File(source_path)
    if not source:
        raise OSError("Kodi could not read the selected build archive.")
    written = 0
    try:
        expected = source.size()
        if expected and expected > DOWNLOAD_LIMIT:
            raise ValueError("The selected build archive is larger than the wizard limit.")
        with open(destination, "wb") as output:
            while True:
                block = source.read(CHUNK_SIZE)
                if not block:
                    break
                if isinstance(block, str):
                    block = block.encode("utf-8")
                written += len(block)
                if written > DOWNLOAD_LIMIT:
                    raise ValueError("The selected build archive is larger than the wizard limit.")
                output.write(block)
        if expected and written != expected:
            raise IOError("Kodi copied an incomplete build archive.")
    finally:
        source.close()
    progress.update(5, "Reading the selected build archive…")


def _stop_playback_for_install():
    """Do not unpack a large build while Kodi is decoding an active stream."""
    player = xbmc.Player()
    if not player.isPlaying():
        return
    _log("Stopping active playback before build preparation.")
    player.stop()
    deadline = time.monotonic() + 10
    while player.isPlaying() and time.monotonic() < deadline:
        xbmc.sleep(250)
    if player.isPlaying():
        raise RuntimeError("Kodi is still playing video. Stop playback, then retry the build install.")
    _log("Playback stopped; build preparation can begin.")


def _install(name, build_id, access_code, public_build=False, local_archive=None):
    target_kodi_major = _private_build_kodi_major(build_id) if not public_build else None
    if target_kodi_major is not None and target_kodi_major != KODI_MAJOR:
        target_version = "21.3" if target_kodi_major == 21 else str(target_kodi_major)
        device_version = "21.3" if KODI_MAJOR == 21 else str(KODI_MAJOR)
        xbmcgui.Dialog().ok(
            "Kodi version mismatch",
            "This build is for Kodi {}. Install it on a device running Kodi {}, not Kodi {}.".format(
                target_version, target_version, device_version
            ),
        )
        return
    if public_build:
        profile_notice = (
            "This public build contains no saved personal account profiles, API keys, or credentials from the backup. "
            "The new public release removes older add-ons absent from the selected backup, including Forge, Gears, "
            "and Zoro, together with their saved settings. Back up this device before installing. "
            "Settings for other add-ons stay in place."
        )
    else:
        profile_notice = (
            "Saved settings and login data for add-ons included in this private build may replace the matching add-on data on this device."
        )
        if local_archive:
            profile_notice += " The selected private ZIP is not encrypted; keep it in private storage and delete any extra copies after transfer."
    if not xbmcgui.Dialog().yesno(
        "Install {}?".format(name),
        "This stops active playback, pauses IPTV during the large file preparation, installs and enables all packaged add-ons, fetches device-compatible "
        "native components through Kodi, replaces matching add-on files, and installs the Xonfluence skin for Kodi {}. ".format(KODI_MAJOR) +
        "It also sets Gismeteo to Thomasville, North Carolina, installs the Xonfluence skin settings, and removes Aeon Nox: SiLVO, Estuary MOD V2, and the OnePlay repository.\n\n"
        "It also removes XStream Pro, XStream Player, and their saved settings when the selected build marks them for removal.\n\n" +
        profile_notice + " The KingBlap Wizard's own settings and access code will stay saved here. "
        "Libraries and Kodi databases are not in the build.",
        yeslabel="Install build",
        nolabel="Cancel",
    ):
        return

    home = _path("special://home")
    addon_root = _path("special://home/addons")
    data_root = _path("special://profile/addon_data")
    wizard_temp = os.path.join(_path("special://temp"), ADDON_ID)
    downloads = os.path.join(wizard_temp, "downloads")
    archive_path = os.path.join(downloads, "KingBlapKodiBuild.zip")
    # Keep the rollback journal on persistent profile storage, but avoid a deep
    # addon_data path: Kodi's VFS can fail to write long staged member paths.
    transaction_root = _path("special://profile/.kbw-transactions")
    transaction = os.path.join(
        transaction_root,
        "{}-{}".format(time.strftime("%Y%m%d-%H%M%S"), uuid.uuid4().hex[:8]),
    )
    staged_addons = os.path.join(transaction, "s", "a")
    staged_userdata = os.path.join(transaction, "s", "u")
    rollback_root = os.path.join(transaction, "rollback")
    os.makedirs(downloads, exist_ok=True)
    os.makedirs(addon_root, exist_ok=True)
    _remove_stale_download(archive_path)

    progress = xbmcgui.DialogProgress()
    progress.create("KingBlap Wizard", "Downloading build…")
    changes = []
    original_skin = None
    original_pvr_enabled = None
    original_weather_settings = None
    original_weather_addon_settings = None
    original_skin_appearance = None
    original_screensaver_mode = None
    original_addon_update_mode = None
    original_stream_buffer_memory = None
    original_service_states = {}
    service_addon_ids = set()
    optiklean_enable_warning = None
    committed = False
    rollback_complete = True
    preserve_transaction = False
    packages = {}
    try:
        _stop_playback_for_install()
        if not public_build:
            previous_buffer_memory = _get_setting("filecache.memorysize")
            if type(previous_buffer_memory) is int and previous_buffer_memory > 16:
                original_stream_buffer_memory = previous_buffer_memory
                _set_setting("filecache.memorysize", 16)
                _log(
                    "Reduced Kodi's stream-buffer memory from {} MB to 16 MB for this private install.".format(
                        previous_buffer_memory
                    )
                )
        os.makedirs(transaction, exist_ok=True)
        journal_state = {
            "transaction": transaction,
            "operations": [],
            "addon_states": {},
            "post_commit_enable": [],
        }
        _write_transaction_journal(
            transaction,
            "staging",
            journal_state["operations"],
            journal_state["addon_states"],
            journal_state["post_commit_enable"],
        )
        if local_archive:
            allowed_build_ids = {
                21: (KODI21_PUBLIC_BUILD_ID, KODI21_PRIVATE_BUILD_ID),
                22: (KODI22_PUBLIC_BUILD_ID, KODI22_PRIVATE_BUILD_ID),
            }.get(KODI_MAJOR, ())
            kodi22_private_release = (
                KODI_MAJOR == 22
                and isinstance(build_id, str)
                and build_id.startswith(KODI22_PRIVATE_BUILD_PREFIX)
            )
            kodi21_private_release = (
                KODI_MAJOR == 21
                and isinstance(build_id, str)
                and build_id.startswith(KODI21_PRIVATE_BUILD_PREFIX)
            )
            if (
                build_id not in allowed_build_ids
                and not kodi21_private_release
                and not kodi22_private_release
            ):
                raise ValueError("This local archive is not an available build for this Kodi release.")
            _check_pre_download_space(os.path.getsize(local_archive), local_archive=True)
            _copy_local_archive(local_archive, archive_path, progress)
        else:
            _download_archive(
                build_id, archive_path, progress, access_code, public_build=public_build
            )
        with zipfile.ZipFile(archive_path, "r") as archive:
            (
                expanded_size,
                packages,
                platform_addons,
                removed_addons,
                profile_mode,
                profile_addon_data_ids,
                reset_addon_data_ids,
                skin_colors,
                skin_font,
                screensaver_addon,
                auto_update_addons,
            ) = _validate_archive(archive, expected_public=public_build)
            required_dependencies = _required_external_dependencies(archive, packages)
            free_space = shutil.disk_usage(home).free
            if free_space < expanded_size + os.path.getsize(archive_path) + 64 * 1024 * 1024:
                raise OSError("There is not enough free storage to unpack this build safely.")
            if progress.iscanceled():
                raise InterruptedError("Build installation was cancelled.")
            if not public_build and "plugin.video.giptv" in packages:
                progress.update(5, "Pausing IPTV while the build is prepared…")
                if PVR_ADDON_ID in profile_addon_data_ids:
                    original_pvr_enabled = _pause_install_addon(
                        PVR_ADDON_ID, journal_state, original_service_states
                    )
                original_service_states["plugin.video.giptv"] = _pause_install_addon(
                    "plugin.video.giptv", journal_state, original_service_states
                )
            progress.close()
            progress = xbmcgui.DialogProgressBG()
            progress.create("KingBlap Wizard", "Preparing add-ons…")

            count = 0
            last_percent = -1
            files = [info for info in archive.infolist() if not info.is_dir()]
            _log("Preparing {} build files ({} add-ons, {} expanded bytes).".format(
                len(files), len(packages), expanded_size
            ))
            for info in files:
                if info.filename.startswith("addons/"):
                    relative = info.filename[len("addons/"):]
                    destination = _safe_target(staged_addons, relative)
                elif info.filename.startswith("userdata/"):
                    relative = info.filename[len("userdata/"):]
                    destination = _safe_target(staged_userdata, relative)
                elif info.filename == "build_info.json":
                    continue
                else:
                    continue
                try:
                    _write_member(archive, info, destination)
                except OSError as exc:
                    preserve_transaction = True
                    try:
                        destination_state = "lexists={}, islink={}, isdir={}, parent_isdir={}".format(
                            os.path.lexists(destination),
                            os.path.islink(destination),
                            os.path.isdir(destination),
                            os.path.isdir(os.path.dirname(destination)),
                        )
                        destination_state += ", parent_entries={!r}".format(
                            os.listdir(os.path.dirname(destination))[:30]
                        )
                    except OSError as state_exc:
                        destination_state = "state check failed: {}".format(state_exc)
                    _log(
                        "Archive member staging failed: member={!r}, destination={!r}, "
                        "error={!r}, state={}, traceback={}".format(
                            info.filename,
                            destination,
                            exc,
                            destination_state,
                            traceback.format_exc(),
                        ),
                        xbmc.LOGERROR,
                    )
                    raise
                count += 1
                percent = int(count * 90 / max(1, len(files)))
                if percent != last_percent or count % 50 == 0 or count == len(files):
                    progress.update(
                        percent,
                        "KingBlap Wizard",
                        "Preparing files ({:,} of {:,}); your current setup is unchanged…".format(
                            count, len(files)
                        ),
                    )
                    last_percent = percent
                if count % 50 == 0:
                    xbmc.sleep(1)

        staged_skin_settings = os.path.join(
            staged_userdata,
            "addon_data",
            SKIN_ID,
            "settings.xml",
        )
        if not os.path.isfile(staged_skin_settings):
            raise ValueError("The staged build is missing its Xonfluence skin settings file.")
        try:
            staged_settings = ET.parse(staged_skin_settings).getroot()
        except ET.ParseError:
            raise ValueError("The staged Xonfluence skin settings are not valid XML.")
        if staged_settings.tag != "settings" or not staged_settings.findall("setting"):
            raise ValueError("The staged Xonfluence skin settings are empty or invalid.")
        staged_weather_settings = os.path.join(
            staged_userdata,
            "addon_data",
            WEATHER_ID,
            "settings.xml",
        )
        if not os.path.isfile(staged_weather_settings):
            raise ValueError("The staged build is missing its Gismeteo settings file.")
        if profile_mode == PROFILE_DATA_MODE:
            staged_profile_root = os.path.join(staged_userdata, "addon_data")
            for addon_id in profile_addon_data_ids:
                if not os.path.isdir(os.path.join(staged_profile_root, addon_id)):
                    raise ValueError("The staged build is missing profile data for {}.".format(addon_id))
            if "plugin.video.giptv" in packages:
                _prime_giptv_startup_state(staged_userdata)

        for addon_id, version in packages.items():
            manifest_path = _safe_target(staged_addons, "{}/addon.xml".format(addon_id))
            if not os.path.isfile(manifest_path):
                raise ValueError("The staged {} add-on is missing addon.xml.".format(addon_id))
            with open(manifest_path, "rb") as manifest_file:
                manifest = ET.parse(manifest_file).getroot()
            if manifest.get("id") != addon_id or manifest.get("version") != version:
                raise ValueError("The staged {} add-on failed its manifest check.".format(addon_id))
            if any(
                extension.get("point") == "xbmc.service"
                for extension in manifest.findall("extension")
            ):
                service_addon_ids.add(addon_id)
        original_skin = _get_setting("lookandfeel.skin")
        if skin_colors is not None or skin_font is not None:
            original_skin_appearance = {}
            if skin_colors is not None:
                original_skin_appearance["lookandfeel.skincolors"] = _get_setting(
                    "lookandfeel.skincolors"
                )
            if skin_font is not None:
                original_skin_appearance["lookandfeel.font"] = _get_setting(
                    "lookandfeel.font"
                )
        if screensaver_addon is not None:
            original_screensaver_mode = _get_setting("screensaver.mode")
        if auto_update_addons:
            original_addon_update_mode = _get_setting("general.addonupdates")
        original_weather_settings = {
            "weather.addon": _get_setting("weather.addon"),
            "weather.currentlocation": _get_setting("weather.currentlocation"),
        }
        original_weather_addon_settings = _read_weather_addon_settings()
        same_skin_version = (
            original_skin == SKIN_ID
            and _installed_addon_version(addon_root, SKIN_ID) == packages.get(SKIN_ID)
        )
        keep_active_skin = same_skin_version and _addon_directories_match(
            os.path.join(addon_root, SKIN_ID),
            os.path.join(staged_addons, SKIN_ID),
        )
        if keep_active_skin:
            _log(
                "Keeping the active {} skin in place because its installed files and build package match ({}).".format(
                    SKIN_ID, packages[SKIN_ID]
                )
            )
        elif same_skin_version:
            _log(
                "Replacing the active {} skin because installed files differ from the staged build package.".format(
                    SKIN_ID
                ),
                xbmc.LOGWARNING,
            )
        giptv_id = "plugin.video.giptv"
        for service_addon_id in sorted(service_addon_ids):
            enabled_state = _get_addon_enabled(service_addon_id)
            original_service_states.setdefault(service_addon_id, enabled_state)
            if enabled_state is True:
                # Keep background services from changing profiles while the build is
                # being swapped. IPTV and cleanup services get a little more time to stop.
                _set_addon_enabled(service_addon_id, False)
                xbmc.sleep(1500 if service_addon_id in (giptv_id, OPTIKLEAN_ID) else 300)
        for removed_addon_id in sorted(set(removed_addons) - set(packages)):
            enabled_state = _get_addon_enabled(removed_addon_id)
            original_service_states[removed_addon_id] = enabled_state
            if enabled_state is True:
                # Stop removed add-on services before replacing their files and profile data.
                _set_addon_enabled(removed_addon_id, False)
                xbmc.sleep(1200 if removed_addon_id == "plugin.video.xstream-pro" else 300)
        if PVR_ADDON_ID in profile_addon_data_ids:
            if original_pvr_enabled is None:
                original_pvr_enabled = _get_addon_enabled(PVR_ADDON_ID)
            if original_pvr_enabled is True and _get_addon_enabled(PVR_ADDON_ID) is True:
                # Unload every IPTV Simple instance before replacing its settings directory.
                _set_addon_enabled(PVR_ADDON_ID, False)
                xbmc.sleep(1500)
        if original_skin in (SKIN_ID, LEGACY_SKIN_ID) and not keep_active_skin:
            # Unload either skin before replacing or removing its files.
            _activate_skin("skin.estuary")

        progress.update(92, "KingBlap Wizard", "Replacing add-ons safely…")
        removed_addons = set(removed_addons) | {"plugin.video.xstream-player", LEGACY_SKIN_ID}
        addon_ids_to_replace = set(packages) | removed_addons
        if keep_active_skin:
            # Keep Kodi's currently rendered skin loaded when the build already has that version.
            addon_ids_to_replace.discard(SKIN_ID)
        for addon_id in sorted(addon_ids_to_replace):
            staged = os.path.join(staged_addons, addon_id) if addon_id in packages else None
            backup = os.path.join(rollback_root, "addons", addon_id)
            _swap_child(addon_root, addon_id, staged, backup, changes, journal_state, "addons")
        if profile_mode == PROFILE_DATA_MODE:
            for addon_id in profile_addon_data_ids:
                _swap_child(
                    data_root,
                    addon_id,
                    os.path.join(staged_userdata, "addon_data", addon_id),
                    os.path.join(rollback_root, "addon-data", addon_id),
                    changes,
                    journal_state,
                    "addon_data",
                )
        else:
            _swap_child(
                os.path.join(data_root, SKIN_ID),
                "settings.xml",
                staged_skin_settings,
                os.path.join(rollback_root, "addon-data", SKIN_ID, "settings.xml"),
                changes,
                journal_state,
                "skin_data",
            )
        for addon_id in reset_addon_data_ids:
            _swap_child(
                data_root,
                addon_id,
                None,
                os.path.join(rollback_root, "addon-data", addon_id),
                changes,
                journal_state,
                "addon_data",
            )
        for addon_id in removed_addons:
            _swap_child(
                data_root,
                addon_id,
                None,
                os.path.join(rollback_root, "addon-data", addon_id),
                changes,
                journal_state,
                "addon_data",
            )
        if profile_mode != PROFILE_DATA_MODE:
            _swap_child(
                os.path.join(data_root, WEATHER_ID),
                "settings.xml",
                staged_weather_settings,
                os.path.join(rollback_root, "addon-data", WEATHER_ID, "settings.xml"),
                changes,
                journal_state,
                "weather_data",
            )
        xbmc.executebuiltin("UpdateLocalAddons", True)
        xbmc.executebuiltin("UpdateAddonRepos", True)
        kodi_managed_addons = set(required_dependencies) | set(platform_addons)
        if PVR_ADDON_ID in profile_addon_data_ids:
            # Do not start importing thousands of IPTV channels while Kodi is
            # still registering and enabling the rest of the build.
            kodi_managed_addons.discard(PVR_ADDON_ID)
        kodi_managed_addons = sorted(kodi_managed_addons)
        for addon_id in kodi_managed_addons:
            _ensure_kodi_managed_addon(addon_id, progress)
        # Kodi automatically enables a newly installed IPTV Simple dependency.
        # Installing it here starts a large channel import while the skin is
        # changing, even when _ensure_kodi_managed_addon(enable=False) is used.
        # Wait until after the file swap and skin activation have committed.
        xbmc.executebuiltin("UpdateLocalAddons", True)
        _wait_for_addon_registration(packages.keys(), progress)
        deferred_addons = service_addon_ids
        _enable_build_addons(packages.keys(), progress, deferred=deferred_addons)
        _log(
            "Verified {} packaged add-ons are enabled; Kodi services stay paused until the file swap commits.".format(
                len(packages) - len(deferred_addons)
            )
        )
        _log("Weather activation deferred until after the build transaction commits.")
        _log("Checking the packaged Xonfluence skin registration.")
        try:
            installed_skin_version = xbmcaddon.Addon(SKIN_ID).getAddonInfo("version")
        except RuntimeError:
            installed_skin_version = ""
        if installed_skin_version != packages[SKIN_ID]:
            raise RuntimeError("Kodi did not register the installed Xonfluence {} skin.".format(SKIN_VERSION))

        progress.update(97, "KingBlap Wizard", "Loading Xonfluence…")
        _apply_skin_settings()
        if skin_colors is not None:
            _set_setting("lookandfeel.skincolors", skin_colors)
            if _get_setting("lookandfeel.skincolors") != skin_colors:
                raise RuntimeError("Kodi did not apply the selected Xonfluence color palette.")
        if skin_font is not None:
            _set_setting("lookandfeel.font", skin_font)
            if _get_setting("lookandfeel.font") != skin_font:
                raise RuntimeError("Kodi did not apply the selected Xonfluence font.")
        if screensaver_addon is not None:
            _set_setting("screensaver.mode", screensaver_addon)
            if _get_setting("screensaver.mode") != screensaver_addon:
                raise RuntimeError("Kodi did not select the build's screensaver add-on.")
            _log("Selected the build's screensaver add-on {}.".format(screensaver_addon))
        if auto_update_addons:
            _set_setting("general.addonupdates", 0)
            if _get_setting("general.addonupdates") != 0:
                raise RuntimeError("Kodi did not enable automatic add-on updates.")
            _log("Enabled automatic updates for compatible add-ons from enabled repositories.")
        if skin_colors is not None or skin_font is not None:
            _log("Applied private Xonfluence appearance: colors={!r}, font={!r}.".format(
                skin_colors, skin_font
            ))
        journal_state["post_commit_enable"] = sorted(
            set(service_addon_ids)
            | ({PVR_ADDON_ID} if PVR_ADDON_ID in profile_addon_data_ids else set())
        )
        _write_transaction_journal(
            transaction,
            "swapping",
            journal_state["operations"],
            journal_state["addon_states"],
            journal_state["post_commit_enable"],
        )
        _write_transaction_commit_marker(transaction)
        committed = True
        _log("Build transaction committed; starting packaged services.")
        post_commit_failures = []
        if PVR_ADDON_ID in profile_addon_data_ids:
            progress.update(98, "KingBlap Wizard", "Starting IPTV Simple after setup…")
            try:
                _ensure_kodi_managed_addon(PVR_ADDON_ID, progress)
            except Exception as pvr_exc:
                post_commit_failures.append("IPTV Simple: {}".format(pvr_exc))
        for service_addon_id in sorted(service_addon_ids - {"plugin.video.giptv"}):
            try:
                _enable_addon(service_addon_id)
            except Exception as service_exc:
                post_commit_failures.append("{}: {}".format(service_addon_id, service_exc))
        if "plugin.video.giptv" in service_addon_ids:
            progress.update(99, "KingBlap Wizard", "Starting GIPTV after setup…")
            try:
                _enable_addon("plugin.video.giptv")
            except Exception as giptv_exc:
                post_commit_failures.append("GIPTV: {}".format(giptv_exc))
        if post_commit_failures:
            optiklean_enable_warning = "; ".join(post_commit_failures[:4])
            _log(
                "The build committed, but some background services could not start: {}".format(
                    optiklean_enable_warning
                ),
                xbmc.LOGWARNING,
            )
        else:
            _log("Verified all {} packaged add-ons are enabled.".format(len(packages)))
        weather_warning = None
        try:
            _log("Post-commit weather setup: applying Gismeteo settings.")
            _write_weather_addon_settings(WEATHER_ADDON_SETTINGS)
            _log("Post-commit weather setup: Gismeteo settings applied.")
            _log("Post-commit weather setup: selecting Gismeteo and location 1.")
            _set_setting("weather.addon", WEATHER_ID)
            _log("Post-commit weather setup: Gismeteo selected.")
            _set_setting("weather.currentlocation", 1)
            _log("Post-commit weather setup: location 1 selected.")
            if _get_setting("weather.currentlocation") != 1:
                raise RuntimeError("Kodi did not select Thomasville as its current weather location.")
            # Weather builtins may wait on the weather manager. Queue them so
            # forecast loading cannot block the build completion notice.
            _log("Post-commit weather setup: queuing location and forecast refresh.")
            xbmc.executebuiltin("Weather.LocationSet(1)", False)
            xbmc.executebuiltin("Weather.Refresh", False)
            _log("Selected Gismeteo location 1 (Thomasville, North Carolina); forecast refresh queued.")
        except Exception as weather_exc:
            weather_warning = str(weather_exc)
            _log("Build committed, but weather setup needs attention: {}".format(weather_exc), xbmc.LOGWARNING)
        progress.close()
        success_message = (
            "Kodi registered the {} add-ons in the build and checked {} "
            "platform-specific add-ons through Kodi's add-on manager. After you close this message, the wizard will "
            "finish applying Xonfluence.\n\n"
            "Kodi will recreate add-on logos and skin artwork when it displays them.\n"
            "Show and channel thumbnails need each add-on's own data and account settings.\n"
            "Keep Kodi's official repository enabled so Kodi can install native dependencies for {}.\n"
            "The OnePlay repository and build-marked add-ons were removed with their saved profile data.\n"
            "{} The Wizard access code remains saved locally."
        ).format(
            len(packages),
            len(platform_addons),
            _platform_name(),
            (
                "No saved add-on API keys or account credentials were imported."
                if public_build
                else "Saved profile data for add-ons in this private build has been restored."
            ),
        )
        if skin_colors is not None or skin_font is not None:
            success_message += "\nThe Xonfluence interface uses the {} color palette and {} font.".format(
                skin_colors or "current",
                skin_font or "current",
            )
        if screensaver_addon is not None:
            if screensaver_addon == BUILTIN_DIM_SCREENSAVER_ID:
                success_message += "\nKodi's built-in dim screensaver is selected."
            else:
                success_message += "\nThe {} screensaver is installed and selected.".format(
                    screensaver_addon
                )
        if auto_update_addons:
            success_message += "\nAutomatic add-on updates are enabled for compatible add-ons from enabled repositories."
        if weather_warning:
            success_message += "\nGismeteo needs attention: {}.".format(weather_warning)
        else:
            success_message += "\nGismeteo is set to Thomasville, North Carolina."
        if optiklean_enable_warning:
            success_message += "\nSome background add-ons did not start automatically: {}. You can enable them in Add-ons > My add-ons.".format(
                optiklean_enable_warning
            )
        xbmcgui.Dialog().ok(
            "KingBlap build installed",
            success_message,
        )
        try:
            _request_skin_reapply()
        except OSError as marker_exc:
            _log("Could not schedule the final Xonfluence apply: {}".format(marker_exc), xbmc.LOGWARNING)
        _log("Installed build {} with {} add-ons.".format(name, len(packages)))
    except Exception as exc:
        try:
            progress.close()
        except Exception:
            pass
        if not committed:
            for service_addon_id in sorted(service_addon_ids):
                try:
                    if _get_addon_enabled(service_addon_id) is True:
                        _set_addon_enabled(service_addon_id, False)
                        xbmc.sleep(1500 if service_addon_id in ("plugin.video.giptv", OPTIKLEAN_ID) else 300)
                except Exception as service_exc:
                    rollback_complete = False
                    _log(
                        "Could not pause {} before rollback: {}".format(service_addon_id, service_exc),
                        xbmc.LOGERROR,
                    )
            if changes:
                try:
                    _activate_skin("skin.estuary")
                except Exception:
                    pass
            rollback_complete = _restore_children(changes) and rollback_complete
            if original_stream_buffer_memory is not None:
                try:
                    _set_setting("filecache.memorysize", original_stream_buffer_memory)
                except Exception as restore_exc:
                    rollback_complete = False
                    _log("Could not restore Kodi's previous stream-buffer memory setting: {}".format(
                        restore_exc
                    ), xbmc.LOGERROR)
            if original_weather_settings is not None:
                for setting, value in original_weather_settings.items():
                    try:
                        _set_setting(setting, value)
                    except Exception as restore_exc:
                        rollback_complete = False
                        _log("Could not restore {}: {}".format(setting, restore_exc), xbmc.LOGERROR)
            try:
                xbmc.executebuiltin("UpdateLocalAddons", True)
            except Exception as restore_exc:
                rollback_complete = False
                _log("Could not refresh Kodi's add-on list during rollback: {}".format(
                    restore_exc
                ), xbmc.LOGERROR)
            if original_screensaver_mode is not None:
                try:
                    _set_setting("screensaver.mode", original_screensaver_mode)
                except Exception as restore_exc:
                    rollback_complete = False
                    _log("Could not restore the previous screensaver: {}".format(
                        restore_exc
                    ), xbmc.LOGERROR)
            if original_addon_update_mode is not None:
                try:
                    _set_setting("general.addonupdates", original_addon_update_mode)
                except Exception as restore_exc:
                    rollback_complete = False
                    _log("Could not restore the previous add-on update setting: {}".format(
                        restore_exc
                    ), xbmc.LOGERROR)
            if original_pvr_enabled is not None:
                try:
                    if _get_addon_enabled(PVR_ADDON_ID) is not None:
                        _set_addon_enabled(PVR_ADDON_ID, original_pvr_enabled)
                except Exception as restore_exc:
                    rollback_complete = False
                    _log("Could not restore the previous IPTV Simple enabled state: {}".format(
                        restore_exc
                    ), xbmc.LOGERROR)
            for service_addon_id, previous_state in original_service_states.items():
                if previous_state is None:
                    continue
                try:
                    if _get_addon_enabled(service_addon_id) is not previous_state:
                        _set_addon_enabled(service_addon_id, previous_state)
                except Exception as restore_exc:
                    rollback_complete = False
                    _log("Could not restore the previous {} enabled state: {}".format(
                        service_addon_id, restore_exc
                    ), xbmc.LOGERROR)
            if original_weather_addon_settings is not None:
                try:
                    _write_weather_addon_settings(original_weather_addon_settings)
                except Exception as restore_exc:
                    rollback_complete = False
                    _log("Could not restore Gismeteo settings: {}".format(restore_exc), xbmc.LOGERROR)
            if original_skin:
                try:
                    _activate_skin(original_skin)
                except Exception as restore_exc:
                    rollback_complete = False
                    _log("Could not restore the previous skin: {}".format(
                        restore_exc
                    ), xbmc.LOGERROR)
            if original_skin_appearance is not None:
                for setting, value in original_skin_appearance.items():
                    try:
                        _set_setting(setting, value)
                    except Exception as restore_exc:
                        rollback_complete = False
                        _log("Could not restore {}: {}".format(setting, restore_exc), xbmc.LOGERROR)
        if not committed and rollback_complete and not preserve_transaction:
            try:
                _cleanup_transaction(transaction)
            except OSError as cleanup_exc:
                _log("Could not remove installer staging files: {}".format(
                    cleanup_exc
                ), xbmc.LOGWARNING)
        if committed:
            _log("The build installed, but its completion notice failed: {}".format(
                exc
            ), xbmc.LOGWARNING)
        else:
            _log("Build install failed: {}".format(exc), xbmc.LOGERROR)
            if isinstance(exc, AccessDenied) and not public_build:
                ADDON.setSetting("access_code", "")
                message = "The access code was not accepted. Enter the correct code in KingBlap Wizard settings and try again."
            elif isinstance(exc, AccessDenied):
                message = "The public download was refused. Try again later."
            else:
                message = "The build was not installed.\n\n{}".format(exc)
            xbmcgui.Dialog().ok(
                "KingBlap build", message
            )
    finally:
        try:
            if os.path.exists(archive_path):
                os.remove(archive_path)
        except OSError:
            pass
    if committed:
        try:
            _cleanup_transaction(transaction)
        except OSError as cleanup_exc:
            _log("Could not remove installer rollback files: {}".format(
                cleanup_exc
            ), xbmc.LOGWARNING)


def _add_category_item(handle, name, category, description):
    item = xbmcgui.ListItem(label=name)
    item.setInfo("video", {"title": name, "plot": description})
    item_url = "{}?category={}".format(sys.argv[0], category)
    xbmcplugin.addDirectoryItem(handle, item_url, item, isFolder=True)


def _add_directory_item(handle, name, build_id, public_build=False):
    item = xbmcgui.ListItem(label=name)
    tier = "public" if public_build else "private"
    description = (
        "Public build: downloads directly in the Wizard; no saved add-on account profiles, API keys, credentials, IPTV playlists, or guide data from the backup are included."
        if public_build
        else "Private build: Kodi 21.3 and Kodi 22 builds are listed here. Choose the build matching this device; downloads use the access-code-protected service."
    )
    item.setInfo("video", {"title": name, "plot": description})
    item_url = "{}?action=install&name={}&build={}&tier={}".format(
        sys.argv[0],
        urllib.parse.quote(name),
        urllib.parse.quote(build_id, safe=""),
        tier,
    )
    xbmcplugin.addDirectoryItem(handle, item_url, item, isFolder=False)


def main():
    handle = int(sys.argv[1])
    query = urllib.parse.parse_qs(sys.argv[2][1:]) if len(sys.argv) > 2 and sys.argv[2].startswith("?") else {}
    access_code = ADDON.getSetting("access_code").strip()
    category = query.get("category", [""])[0]
    if query.get("action") == ["install"]:
        name = query.get("name", ["KingBlap Kodi Build"])[0]
        build_id = query.get("build", [""])[0]
        public_build = query.get("tier", [""])[0] == "public"
        if not public_build and not access_code:
            xbmcgui.Dialog().ok(
                "KingBlap Wizard",
                "Enter your access code in KingBlap Wizard settings before installing a build.",
            )
        elif not public_build and not _valid_access_code(access_code):
            xbmcgui.Dialog().ok(
                "KingBlap Wizard",
                "The access code must be exactly 16 digits.",
            )
        elif not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}", build_id):
            xbmcgui.Dialog().ok("KingBlap Wizard", "The selected build is invalid.")
        else:
            local_archive = None
            _install(
                name,
                build_id,
                access_code if not public_build else None,
                public_build=public_build,
                local_archive=local_archive,
            )
        xbmcplugin.endOfDirectory(handle, succeeded=True, cacheToDisc=False)
        return

    xbmcplugin.setContent(handle, "files")
    if category not in ("public", "private"):
        _add_category_item(
            handle,
            "Public Builds",
            "public",
            "Credential-free builds; no saved account settings from the backup are included.",
        )
        _add_category_item(
            handle,
            "Private Builds",
            "private",
            "Builds that include saved add-on profile data and require the private access code.",
        )
        xbmcplugin.endOfDirectory(handle, succeeded=True, cacheToDisc=False)
        return

    public_build = category == "public"
    if not public_build and not access_code:
        xbmcgui.Dialog().ok(
            "KingBlap Wizard",
            "Enter your access code in KingBlap Wizard settings, then open the wizard again.",
        )
        xbmcplugin.endOfDirectory(handle, succeeded=True, cacheToDisc=False)
        return
    if not public_build and not _valid_access_code(access_code):
        xbmcgui.Dialog().ok(
            "KingBlap Wizard",
            "The access code must be exactly 16 digits. Update it in KingBlap Wizard settings.",
        )
        xbmcplugin.endOfDirectory(handle, succeeded=True, cacheToDisc=False)
        return
    try:
        builds = _get_builds(
            access_code if not public_build else None,
            public_build=public_build,
        )
        for build_id, name in builds:
            _add_directory_item(handle, name, build_id, public_build=public_build)
        if not builds:
            message = (
                "Public builds are available for Kodi 21.3 and Kodi 22."
                if public_build and KODI_MAJOR not in (21, 22)
                else "No {} builds are listed right now.".format(category)
            )
            xbmcgui.Dialog().ok(
                "KingBlap Wizard",
                message,
            )
    except AccessDenied:
        if not public_build:
            ADDON.setSetting("access_code", "")
            message = "The access code was not accepted. Enter the correct code in KingBlap Wizard settings and try again."
        else:
            message = "The public build endpoint refused the request. Try again later."
        xbmcgui.Dialog().ok("KingBlap Wizard", message)
    except (OSError, ValueError, urllib.error.URLError) as exc:
        _log("Could not load build list: {}".format(exc), xbmc.LOGERROR)
        xbmcgui.Dialog().ok(
            "KingBlap Wizard", "Could not load the build list.\n\n{}".format(exc)
        )
    xbmcplugin.endOfDirectory(handle, succeeded=True, cacheToDisc=False)


if __name__ == "__main__":
    main()
