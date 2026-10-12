"""KingBlap Kodi build installer for Kodi 21 Omega and Kodi 22 Piers."""
import json
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
PUBLIC_BUILD_ID = "kingblap-public-1.0.19"
PUBLIC_BUILD_NAME = "Public KingBlap Kodi Build 1.0.19"
KODI21_PUBLIC_BUILD_ID = "kingblap-public-kodi21.3-1.0.20"
KODI21_PRIVATE_BUILD_ID = "kingblap-private-kodi21.3-1.0.20"
KODI21_PUBLIC_BUILD_NAME = "Public KingBlap Build for Kodi 21.3 (choose ZIP)"
KODI21_PRIVATE_BUILD_NAME = "Private KingBlap Build for Kodi 21.3 (choose ZIP)"
KODI22_PUBLIC_BUILD_ID = "kingblap-public-kodi22-1.0.21"
KODI22_PRIVATE_BUILD_ID = "kingblap-private-kodi22-1.0.21"
KODI22_PUBLIC_BUILD_NAME = "Public KingBlap Build for Kodi 22 (choose ZIP)"
KODI22_PRIVATE_BUILD_NAME = "Private KingBlap Build for Kodi 22 (choose ZIP)"
PUBLIC_BUILD_PARTS = (
    ("https://kingblap.github.io/builds/public/KingBlapKodiPublicBuild-1.0.19.zip.part001", 83886080),
    ("https://kingblap.github.io/builds/public/KingBlapKodiPublicBuild-1.0.19.zip.part002", 83886080),
    ("https://kingblap.github.io/builds/public/KingBlapKodiPublicBuild-1.0.19.zip.part003", 10645365),
)
WEATHER_VERSION = "0.6.4+matrix.1"
SKIN_SETTINGS_ARCHIVE_PATH = "userdata/addon_data/{}/settings.xml".format(SKIN_ID)
LEGACY_SKIN_ID = "skin.estuary.modv2"
ONEPLAY_REPO_ID = "One.repo"
WEATHER_ID = "weather.gismeteo"
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
ACCESS_CODE_PATTERN = re.compile(r"[0-9]{16}\Z")
CHUNK_SIZE = 1024 * 1024
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
        "User-Agent": "KingBlap-Wizard/1.0.32 Kodi",
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
    if KODI_MAJOR in (21, 22):
        if KODI_MAJOR == 21:
            build = (KODI21_PUBLIC_BUILD_ID, KODI21_PUBLIC_BUILD_NAME) if public_build else (KODI21_PRIVATE_BUILD_ID, KODI21_PRIVATE_BUILD_NAME)
        else:
            build = (KODI22_PUBLIC_BUILD_ID, KODI22_PUBLIC_BUILD_NAME) if public_build else (KODI22_PRIVATE_BUILD_ID, KODI22_PRIVATE_BUILD_NAME)
        return [build]
    if public_build:
        return [(PUBLIC_BUILD_ID, PUBLIC_BUILD_NAME)]
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


def _remove_child(root, name):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
        raise ValueError("Refusing to remove an invalid add-on path.")
    root_real = os.path.realpath(root)
    target = os.path.abspath(os.path.join(root_real, name))
    if os.path.commonpath((root_real, target)) != root_real or target == root_real:
        raise ValueError("Refusing to remove a path outside Kodi's profile.")
    _remove_path(target)


def _swap_child(root, name, staged, backup, changes):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
        raise ValueError("The build contains an invalid add-on ID.")
    root_real = os.path.realpath(root)
    target = os.path.abspath(os.path.join(root_real, name))
    if os.path.commonpath((root_real, target)) != root_real or target == root_real:
        raise ValueError("Refusing to replace a path outside Kodi's profile.")
    saved = None
    if os.path.lexists(target):
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
    if packages.get("plugin.video.giptv") != "3.1.0":
        raise ValueError("The build archive does not contain the expected GIPTV package.")
    if packages.get(SKIN_ID) != SKIN_VERSION:
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
    return (
        total,
        packages,
        sorted(set(platform_addons)),
        sorted(set(removed_addons)),
        profile_mode,
        sorted(profile_addon_data_ids) if profile_mode == PROFILE_DATA_MODE else [],
    )


def _download_public_archive(destination, progress):
    total_expected = sum(size for _, size in PUBLIC_BUILD_PARTS)
    total_written = 0
    with open(destination, "wb") as output:
        for part_index, (url, expected_part_size) in enumerate(PUBLIC_BUILD_PARTS):
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "KingBlap-Wizard/1.0.32 Kodi",
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
                                part_index + 1, len(PUBLIC_BUILD_PARTS)
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


def _download_archive(build_id, destination, progress, access_code=None, public_build=False):
    if public_build:
        if build_id != PUBLIC_BUILD_ID:
            raise ValueError("The selected public build is not valid.")
        _download_public_archive(destination, progress)
        return
    route = "/v1/builds"
    url = _api_url(
        "{}/{}/download".format(route, urllib.parse.quote(build_id, safe=""))
    )
    headers = {
        "User-Agent": "KingBlap-Wizard/1.0.32 Kodi",
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
        for addon_id in tuple(pending):
            try:
                details = _jsonrpc("Addons.GetAddonDetails", {
                    "addonid": addon_id,
                    "properties": ["version"],
                }).get("addon", {})
            except RuntimeError:
                continue
            if details.get("version"):
                pending.remove(addon_id)
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


def _enable_build_addons(addon_ids, progress):
    addon_ids = sorted(set(addon_ids))
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


def _ensure_kodi_managed_addon(addon_id, progress):
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
    _enable_addon(addon_id)


def _texture_source_path(url):
    """Resolve a cached texture URL to a local path when it refers to an add-on file."""
    value = str(url or "").strip()
    if not value:
        return None

    if value.lower().startswith("special://"):
        value = _path(value)
    elif value.lower().startswith("file://"):
        value = urllib.parse.unquote(urllib.parse.urlsplit(value).path)
    elif value.lower().startswith("image://"):
        value = urllib.parse.unquote(value[8:]).rstrip("/")
        if value.lower().startswith(("http://", "https://", "plugin://")):
            return None
    elif value.lower().startswith(("http://", "https://", "plugin://")):
        return None
    else:
        value = urllib.parse.unquote(value)

    if not os.path.isabs(value):
        return None
    return os.path.realpath(value)


def _refresh_addon_art_cache(addon_root, addon_ids):
    """Drop stale texture records for add-on files that this build replaced."""
    addon_root = os.path.realpath(addon_root)
    roots = []
    for addon_id in addon_ids:
        candidate = os.path.realpath(os.path.join(addon_root, addon_id))
        try:
            if os.path.commonpath((addon_root, candidate)) == addon_root and candidate != addon_root:
                roots.append(candidate)
        except ValueError:
            continue
    if not roots:
        return 0

    try:
        result = _jsonrpc("Textures.GetTextures", {"properties": ["url", "textureid"]})
    except (RuntimeError, ValueError, TypeError) as exc:
        _log("Could not inspect the add-on artwork cache: {}".format(exc), xbmc.LOGWARNING)
        return 0

    entries = result.get("textures", []) if isinstance(result, dict) else []
    stale_ids = set()
    for entry in entries:
        source = _texture_source_path(entry.get("url"))
        texture_id = entry.get("textureid")
        if source is None or texture_id is None:
            continue
        for root in roots:
            try:
                if os.path.commonpath((root, source)) == root and source != root:
                    stale_ids.add(int(texture_id))
                    break
            except ValueError:
                continue

    removed = 0
    for texture_id in stale_ids:
        try:
            _jsonrpc("Textures.RemoveTexture", {"textureid": texture_id})
            removed += 1
        except (RuntimeError, ValueError, TypeError):
            continue
    return removed


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


def _install(name, build_id, access_code, public_build=False, local_archive=None):
    if public_build:
        profile_notice = (
            "This public build contains no saved add-on profile data, API keys, or account credentials from the backup. "
            "It leaves other add-on profile data on this device in place."
        )
    else:
        profile_notice = (
            "Saved settings and login data for add-ons included in this private build may replace the matching add-on data on this device."
        )
        if local_archive:
            profile_notice += " The selected private ZIP is not encrypted; keep it in private storage and delete any extra copies after transfer."
    if not xbmcgui.Dialog().yesno(
        "Install {}?".format(name),
        "This installs and enables all packaged add-ons, fetches device-compatible "
        "native components through Kodi, replaces matching add-on files, and installs the Xonfluence skin for Kodi {}. ".format(KODI_MAJOR) +
        "It also sets Gismeteo to Thomasville, North Carolina, installs the Xonfluence skin settings, and removes Estuary MOD V2 and the OnePlay repository.\n\n"
        "It also removes XStream Player and its saved settings from this Kodi profile.\n\n" +
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
    transaction = os.path.join(
        wizard_temp,
        "transactions",
        "{}-{}".format(time.strftime("%Y%m%d-%H%M%S"), uuid.uuid4().hex[:8]),
    )
    staged_addons = os.path.join(transaction, "staged", "addons")
    staged_userdata = os.path.join(transaction, "staged", "userdata")
    rollback_root = os.path.join(transaction, "rollback")
    os.makedirs(downloads, exist_ok=True)
    os.makedirs(addon_root, exist_ok=True)

    progress = xbmcgui.DialogProgress()
    progress.create("KingBlap Wizard", "Downloading build…")
    changes = []
    original_skin = None
    original_weather_settings = None
    original_weather_addon_settings = None
    committed = False
    rollback_complete = True
    preserve_transaction = False
    try:
        if local_archive:
            allowed_build_ids = {
                21: (KODI21_PUBLIC_BUILD_ID, KODI21_PRIVATE_BUILD_ID),
                22: (KODI22_PUBLIC_BUILD_ID, KODI22_PRIVATE_BUILD_ID),
            }.get(KODI_MAJOR, ())
            if build_id not in allowed_build_ids:
                raise ValueError("This local archive is not an available build for this Kodi release.")
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
            ) = _validate_archive(archive, expected_public=public_build)
            required_dependencies = _required_external_dependencies(archive, packages)
            free_space = shutil.disk_usage(home).free
            if free_space < expanded_size + os.path.getsize(archive_path) + 64 * 1024 * 1024:
                raise OSError("There is not enough free storage to unpack this build safely.")
            if progress.iscanceled():
                raise InterruptedError("Build installation was cancelled.")
            progress.close()
            progress = xbmcgui.DialogProgressBG()
            progress.create("KingBlap Wizard", "Preparing add-ons…")

            count = 0
            last_percent = -1
            files = [info for info in archive.infolist() if not info.is_dir()]
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
                if percent != last_percent:
                    progress.update(
                        percent,
                        "KingBlap Wizard",
                        "Preparing add-ons without changing the current installation…",
                    )
                    last_percent = percent

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

        for addon_id, version in packages.items():
            manifest_path = _safe_target(staged_addons, "{}/addon.xml".format(addon_id))
            if not os.path.isfile(manifest_path):
                raise ValueError("The staged {} add-on is missing addon.xml.".format(addon_id))
            with open(manifest_path, "rb") as manifest_file:
                manifest = ET.parse(manifest_file).getroot()
            if manifest.get("id") != addon_id or manifest.get("version") != version:
                raise ValueError("The staged {} add-on failed its manifest check.".format(addon_id))
        original_skin = _get_setting("lookandfeel.skin")
        original_weather_settings = {
            "weather.addon": _get_setting("weather.addon"),
            "weather.currentlocation": _get_setting("weather.currentlocation"),
        }
        original_weather_addon_settings = _read_weather_addon_settings()

        if original_skin in (SKIN_ID, LEGACY_SKIN_ID):
            # Unload either skin before replacing or removing its files.
            _activate_skin("skin.estuary")

        progress.update(92, "KingBlap Wizard", "Replacing add-ons safely…")
        removed_addons = set(removed_addons) | {"plugin.video.xstream-player", LEGACY_SKIN_ID}
        for addon_id in sorted(set(packages) | removed_addons):
            staged = os.path.join(staged_addons, addon_id) if addon_id in packages else None
            backup = os.path.join(rollback_root, "addons", addon_id)
            _swap_child(addon_root, addon_id, staged, backup, changes)
        if profile_mode == PROFILE_DATA_MODE:
            for addon_id in profile_addon_data_ids:
                _swap_child(
                    data_root,
                    addon_id,
                    os.path.join(staged_userdata, "addon_data", addon_id),
                    os.path.join(rollback_root, "addon-data", addon_id),
                    changes,
                )
        else:
            _swap_child(
                os.path.join(data_root, SKIN_ID),
                "settings.xml",
                staged_skin_settings,
                os.path.join(rollback_root, "addon-data", SKIN_ID, "settings.xml"),
                changes,
            )
        _swap_child(
            data_root,
            "plugin.video.xstream-player",
            None,
            os.path.join(rollback_root, "addon-data", "plugin.video.xstream-player"),
            changes,
        )
        _swap_child(
            data_root,
            ONEPLAY_REPO_ID,
            None,
            os.path.join(rollback_root, "addon-data", ONEPLAY_REPO_ID),
            changes,
        )
        if profile_mode != PROFILE_DATA_MODE:
            _swap_child(
                os.path.join(data_root, WEATHER_ID),
                "settings.xml",
                staged_weather_settings,
                os.path.join(rollback_root, "addon-data", WEATHER_ID, "settings.xml"),
                changes,
            )
        xbmc.executebuiltin("UpdateLocalAddons", True)
        xbmc.executebuiltin("UpdateAddonRepos", True)
        kodi_managed_addons = sorted(set(required_dependencies) | set(platform_addons))
        for addon_id in kodi_managed_addons:
            _ensure_kodi_managed_addon(addon_id, progress)
        xbmc.executebuiltin("UpdateLocalAddons", True)
        _wait_for_addon_registration(packages.keys(), progress)
        _enable_build_addons(packages.keys(), progress)
        _write_weather_addon_settings(WEATHER_ADDON_SETTINGS)
        _set_setting("weather.addon", WEATHER_ID)
        _set_setting("weather.currentlocation", 1)
        # Select the configured first location through Kodi's weather manager
        # and refresh its cached forecast. Otherwise an earlier IP-based
        # location can remain active even after Gismeteo's settings change.
        xbmc.executebuiltin("Weather.LocationSet(1)", True)
        xbmc.executebuiltin("Weather.Refresh", True)
        if _get_setting("weather.currentlocation") != 1:
            raise RuntimeError("Kodi did not select Thomasville as its current weather location.")
        _write_weather_addon_settings(WEATHER_ADDON_SETTINGS)
        _log("Selected Gismeteo location 1 (Thomasville, North Carolina) and refreshed weather.")
        try:
            installed_skin_version = xbmcaddon.Addon(SKIN_ID).getAddonInfo("version")
        except RuntimeError:
            installed_skin_version = ""
        if installed_skin_version != packages[SKIN_ID]:
            raise RuntimeError("Kodi did not register the installed Xonfluence {} skin.".format(SKIN_VERSION))

        progress.update(97, "KingBlap Wizard", "Loading Xonfluence…")
        _apply_skin_settings()
        committed = True
        try:
            refreshed_art = _refresh_addon_art_cache(
                addon_root, set(packages) | removed_addons
            )
        except Exception as cache_exc:
            refreshed_art = 0
            _log("Could not refresh the add-on artwork cache: {}".format(cache_exc), xbmc.LOGWARNING)
        progress.close()
        success_message = (
            "Kodi registered and enabled all {} add-ons in the build and checked {} "
            "platform-specific add-ons through Kodi's add-on manager. It also refreshed "
            "{} cached add-on images. After you close this message, the wizard will "
            "finish applying Xonfluence.\n\n"
            "Kodi will recreate add-on logos and skin artwork when it displays them.\n"
            "Show and channel thumbnails need each add-on's own data and account settings.\n"
            "Keep Kodi's official repository enabled so Kodi can install native dependencies for {}.\n"
            "Gismeteo is set to Thomasville, North Carolina. The OnePlay repository was removed.\n"
            "{} The Wizard access code remains saved locally."
        ).format(
            len(packages),
            len(platform_addons),
            refreshed_art,
            _platform_name(),
            (
                "No saved add-on API keys or account credentials were imported."
                if public_build
                else "Saved profile data for add-ons in this private build has been restored."
            ),
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
            if changes:
                try:
                    _activate_skin("skin.estuary")
                except Exception:
                    pass
            rollback_complete = _restore_children(changes) and rollback_complete
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
        if not committed and rollback_complete and not preserve_transaction:
            try:
                _remove_path(transaction)
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
            _remove_path(transaction)
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
        "Public build: no saved add-on profile data or account credentials from the backup. On Kodi 21.3, select the public build ZIP copied to this device."
        if public_build
        else "Private build: contains saved add-on profile data. On Kodi 21.3, select the private ZIP copied to this device; keep that ZIP private."
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
            if KODI_MAJOR in (21, 22):
                kodi_label = "21.3" if KODI_MAJOR == 21 else "22"
                local_archive = xbmcgui.Dialog().browse(
                    1,
                    "Select the {} Kodi {} build ZIP".format(
                        "Public" if public_build else "Private", kodi_label
                    ),
                    "files",
                    ".zip",
                )
                if not local_archive:
                    xbmcplugin.endOfDirectory(handle, succeeded=True, cacheToDisc=False)
                    return
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
            xbmcgui.Dialog().ok(
                "KingBlap Wizard",
                "No {} builds are listed right now.".format(category),
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
