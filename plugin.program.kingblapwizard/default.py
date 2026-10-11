"""KingBlap Kodi build installer for Kodi 22 and Android-based Kodi devices."""
import json
import os
import re
import shutil
import sys
import time
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
BUILDS_URL = "https://kingblap.github.io/builds.txt"
SKIN_ID = "skin.xonfluence"
SKIN_VERSION = "6.0.6"
SKIN_SETTINGS_ARCHIVE_PATH = "userdata/addon_data/{}/settings.xml".format(SKIN_ID)
LEGACY_SKIN_ID = "skin.estuary.modv2"
BUILD_LIMIT = 1024 * 1024 * 1024
DOWNLOAD_LIMIT = 512 * 1024 * 1024
CHUNK_SIZE = 1024 * 1024


def _log(message, level=xbmc.LOGINFO):
    xbmc.log("[{}] {}".format(ADDON_ID, message), level)


def _path(special):
    return os.path.abspath(xbmcvfs.translatePath(special))


def _fetch(url, max_bytes):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "KingBlap-Wizard/1.0.8 Kodi"},
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        length = response.headers.get("Content-Length")
        if length and int(length) > max_bytes:
            raise ValueError("The download is larger than the wizard limit.")
        data = response.read(max_bytes + 1)
    if len(data) > max_bytes:
        raise ValueError("The download is larger than the wizard limit.")
    return data


def _get_builds():
    content = _fetch(BUILDS_URL, 1024 * 1024).decode("utf-8-sig")
    builds = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "|" in line:
            name, url = [part.strip() for part in line.split("|", 1)]
        else:
            url = line
            name = os.path.basename(urllib.parse.urlparse(url).path) or "Kodi Build"
        if name and url.startswith("https://"):
            builds.append((name, url))
    return builds


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
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with archive.open(info, "r") as source, open(destination, "wb") as output:
        shutil.copyfileobj(source, output, CHUNK_SIZE)


def _validate_archive(archive):
    total = 0
    packages = {}
    skin_settings_found = False
    seen_names = set()
    for info in archive.infolist():
        if info.is_dir():
            continue
        name = info.filename
        if name in seen_names:
            raise ValueError("The build archive contains a duplicate file path.")
        seen_names.add(name)
        if name == "build_info.json":
            pass
        elif name == SKIN_SETTINGS_ARCHIVE_PATH:
            try:
                settings = ET.fromstring(archive.read(info))
            except ET.ParseError:
                raise ValueError("The build archive's Xonfluence skin settings are not valid XML.")
            if settings.tag != "settings" or not settings.findall("setting"):
                raise ValueError("The build archive's Xonfluence skin settings are empty or invalid.")
            skin_settings_found = True
        elif name.startswith("addons/"):
            relative = name[len("addons/"):]
            parts = relative.split("/")
            if len(parts) < 2 or not re.fullmatch(r"[A-Za-z0-9_.-]+", parts[0]):
                raise ValueError("The build archive contains an invalid add-on path.")
            if parts[0] == "plugin.video.xstream-player":
                raise ValueError("The build archive still contains XStream Player.")
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
    if packages.get("plugin.video.giptv") != "3.1.0":
        raise ValueError("The build archive does not contain the expected GIPTV package.")
    if packages.get(SKIN_ID) != SKIN_VERSION:
        raise ValueError("The build archive does not contain Xonfluence 6.0.6 for Kodi 22.")
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
    if "build_info.json" not in archive.namelist():
        raise ValueError("The build archive is missing its build information.")
    if not skin_settings_found:
        raise ValueError("The build archive is missing its Xonfluence skin settings file.")
    return total, packages


def _download_archive(url, destination, progress):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "KingBlap-Wizard/1.0.8 Kodi"},
    )
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


def _enable_addon(addon_id):
    result = _jsonrpc("Addons.SetAddonEnabled", {
        "addonid": addon_id,
        "enabled": True,
    })
    if result not in (True, "OK"):
        raise RuntimeError("Kodi could not enable the {} add-on.".format(addon_id))


def _activate_skin(skin_id):
    _set_setting("lookandfeel.skin", skin_id)
    xbmc.executebuiltin("ReloadSkin", True)
    stable_reads = 0
    for unused in range(24):
        xbmc.sleep(500)
        if (
            _get_setting("lookandfeel.skin") == skin_id
            and xbmc.getSkinDir() == skin_id
        ):
            stable_reads += 1
            if stable_reads >= 3:
                return
        else:
            stable_reads = 0
    raise RuntimeError(
        "Kodi could not load the {} skin. The previous skin will be restored.".format(skin_id)
    )


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


def _install(name, url):
    if not xbmcgui.Dialog().yesno(
        "Install {}?".format(name),
        "This replaces matching add-on files, installs Xonfluence 6.0.6 for Kodi 22, "
        "installs the build's sanitized Xonfluence skin settings, and removes the previous Estuary MOD V2 skin.\n\n"
        "It also removes XStream Player and its saved settings from this Kodi profile.\n\n"
        "Your provider accounts, other add-on data, libraries, and databases are not in the build.",
        yeslabel="Install build",
        nolabel="Cancel",
    ):
        return

    home = _path("special://home")
    addon_root = _path("special://home/addons")
    data_root = _path("special://profile/addon_data")
    wizard_data = _path("special://profile/addon_data/{}".format(ADDON_ID))
    downloads = os.path.join(wizard_data, "downloads")
    archive_path = os.path.join(downloads, "KingBlapKodiBuild.zip")
    transaction = os.path.join(
        wizard_data,
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
    committed = False
    rollback_complete = True
    try:
        _download_archive(url, archive_path, progress)
        with zipfile.ZipFile(archive_path, "r") as archive:
            expanded_size, packages = _validate_archive(archive)
            free_space = shutil.disk_usage(home).free
            if free_space < expanded_size + os.path.getsize(archive_path) + 64 * 1024 * 1024:
                raise OSError("There is not enough free storage to unpack this build safely.")
            if progress.iscanceled():
                raise InterruptedError("Build installation was cancelled.")
            progress.close()
            progress = xbmcgui.DialogProgressBG()
            progress.create("KingBlap Wizard", "Preparing add-ons…")

            count = 0
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
                _write_member(archive, info, destination)
                count += 1
                progress.update(
                    int(count * 90 / max(1, len(files))),
                    "KingBlap Wizard",
                    "Preparing add-ons without changing the current installation…",
                )

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

        for addon_id, version in packages.items():
            manifest_path = _safe_target(staged_addons, "{}/addon.xml".format(addon_id))
            if not os.path.isfile(manifest_path):
                raise ValueError("The staged {} add-on is missing addon.xml.".format(addon_id))
            with open(manifest_path, "rb") as manifest_file:
                manifest = ET.parse(manifest_file).getroot()
            if manifest.get("id") != addon_id or manifest.get("version") != version:
                raise ValueError("The staged {} add-on failed its manifest check.".format(addon_id))
        original_skin = _get_setting("lookandfeel.skin")

        if original_skin in (SKIN_ID, LEGACY_SKIN_ID):
            # Unload either skin before replacing or removing its files.
            _activate_skin("skin.estuary")

        progress.update(92, "KingBlap Wizard", "Replacing add-ons safely…")
        for addon_id in sorted(set(packages) | {"plugin.video.xstream-player", LEGACY_SKIN_ID}):
            staged = os.path.join(staged_addons, addon_id) if addon_id in packages else None
            backup = os.path.join(rollback_root, "addons", addon_id)
            _swap_child(addon_root, addon_id, staged, backup, changes)
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
        xbmc.executebuiltin("UpdateLocalAddons", True)
        xbmc.sleep(1500)
        _enable_addon("script.favourites")
        _enable_addon("script.image.resource.select")
        _enable_addon(SKIN_ID)
        try:
            installed_skin_version = xbmcaddon.Addon(SKIN_ID).getAddonInfo("version")
        except RuntimeError:
            installed_skin_version = ""
        if installed_skin_version != packages[SKIN_ID]:
            raise RuntimeError("Kodi did not register the installed Xonfluence 6.0.6 skin.")

        progress.update(97, "KingBlap Wizard", "Loading Xonfluence…")
        _apply_skin_settings()
        committed = True
        try:
            refreshed_art = _refresh_addon_art_cache(
                addon_root, set(packages) | {"plugin.video.xstream-player", LEGACY_SKIN_ID}
            )
        except Exception as cache_exc:
            refreshed_art = 0
            _log("Could not refresh the add-on artwork cache: {}".format(cache_exc), xbmc.LOGWARNING)
        progress.close()
        success_message = (
            "Kodi found {} portable add-ons and refreshed {} cached add-on images. "
            "Restart Kodi to finish applying the build.\n\n"
            "Kodi will recreate add-on logos and skin artwork when it displays them.\n"
            "Show and channel thumbnails need each add-on's own data and account settings.\n"
            "Keep Kodi's official repository enabled for Android-specific binary dependencies.\n"
            "Open GIPTV and enter your own provider details."
        ).format(len(packages), refreshed_art)
        xbmcgui.Dialog().ok(
            "KingBlap build installed",
            success_message,
        )
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
            try:
                xbmc.executebuiltin("UpdateLocalAddons", True)
            except Exception as restore_exc:
                rollback_complete = False
                _log("Could not refresh Kodi's add-on list during rollback: {}".format(
                    restore_exc
                ), xbmc.LOGERROR)
            if original_skin:
                try:
                    _activate_skin(original_skin)
                except Exception as restore_exc:
                    rollback_complete = False
                    _log("Could not restore the previous skin: {}".format(
                        restore_exc
                    ), xbmc.LOGERROR)
        if not committed and rollback_complete:
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
            xbmcgui.Dialog().ok(
                "KingBlap build", "The build was not installed.\n\n{}".format(exc)
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


def _add_directory_item(handle, name, url):
    item = xbmcgui.ListItem(label=name)
    item.setInfo("video", {"title": name, "plot": "Install the portable KingBlap Kodi build."})
    xbmcplugin.addDirectoryItem(handle, url, item, isFolder=False)


def main():
    handle = int(sys.argv[1])
    query = urllib.parse.parse_qs(sys.argv[2][1:]) if len(sys.argv) > 2 and sys.argv[2].startswith("?") else {}
    if query.get("action") == ["install"]:
        name = query.get("name", ["KingBlap Kodi Build"])[0]
        url = query.get("url", [""])[0]
        if not url.startswith("https://"):
            xbmcgui.Dialog().ok("KingBlap Wizard", "The build link is invalid.")
        else:
            _install(name, url)
        xbmcplugin.endOfDirectory(handle, succeeded=True, cacheToDisc=False)
        return

    xbmcplugin.setContent(handle, "files")
    try:
        builds = _get_builds()
        for name, url in builds:
            item_url = "{}?action=install&name={}&url={}".format(
                sys.argv[0], urllib.parse.quote(name), urllib.parse.quote(url, safe="")
            )
            _add_directory_item(handle, name, item_url)
        if not builds:
            xbmcgui.Dialog().ok("KingBlap Wizard", "No builds are listed right now.")
    except (OSError, ValueError, urllib.error.URLError) as exc:
        _log("Could not load build list: {}".format(exc), xbmc.LOGERROR)
        xbmcgui.Dialog().ok(
            "KingBlap Wizard", "Could not load the build list.\n\n{}".format(exc)
        )
    xbmcplugin.endOfDirectory(handle, succeeded=True, cacheToDisc=False)


if __name__ == "__main__":
    main()
