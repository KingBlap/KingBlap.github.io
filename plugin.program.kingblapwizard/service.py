"""Finish applying Xonfluence after the installer window closes and on Kodi startup."""
import json
import os
import re
import shutil
import time
import xml.etree.ElementTree as ET

import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs


ADDON_ID = "plugin.program.kingblapwizard"
SUPPORTED_SKINS = {"skin.xonfluence", "skin.xonfluence.skinbase"}
SKIN_ID = None
MARKER_PATH = xbmcvfs.translatePath(
    "special://profile/addon_data/{}/skin-reapply.json".format(ADDON_ID)
)
TRANSACTION_ROOT = xbmcvfs.translatePath(
    "special://profile/.kbw-transactions"
)
PREVIOUS_TRANSACTION_ROOT = xbmcvfs.translatePath(
    "special://profile/addon_data/{}/transactions".format(ADDON_ID)
)
LEGACY_TRANSACTION_ROOT = xbmcvfs.translatePath(
    "special://temp/{}/transactions".format(ADDON_ID)
)
OPTIKLEAN_ID = "program.optiklean"
WEATHER_ID = "weather.gismeteo"
PRIVATE_MEMORY_POLICY_PATH = xbmcvfs.translatePath(
    "special://profile/addon_data/plugin.video.giptv/.kingblap-low-memory.json"
)
PENDING_COMMIT_PATH = xbmcvfs.translatePath(
    "special://profile/addon_data/{}/pending-commit-addons.json".format(ADDON_ID)
)
LOAD_TIMEOUT = 60
CONFIRMATION_GRACE = 13


def _log(message, level=xbmc.LOGINFO):
    xbmc.log("[KingBlap Wizard] {}".format(message), level)


def _load_requested_skin():
    global SKIN_ID
    try:
        with open(MARKER_PATH, "r", encoding="utf-8") as marker_file:
            request = json.load(marker_file)
        skin_id = request.get("skin") if isinstance(request, dict) else None
        if skin_id in SUPPORTED_SKINS:
            SKIN_ID = skin_id
            return True
    except (OSError, TypeError, ValueError):
        pass
    _log("The skin reapply marker is missing a supported skin ID.", xbmc.LOGWARNING)
    return False


def _skin_selected():
    if SKIN_ID not in SUPPORTED_SKINS:
        return False
    request = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "Settings.GetSettingValue",
        "params": {"setting": "lookandfeel.skin"},
    })
    response = json.loads(xbmc.executeJSONRPC(request))
    if "error" in response:
        raise RuntimeError(response["error"].get("message", "Kodi could not read the skin setting."))
    return response.get("result", {}).get("value") == SKIN_ID


def _set_skin():
    if SKIN_ID not in SUPPORTED_SKINS:
        raise RuntimeError("The Wizard has no supported skin selected.")
    already_selected = _skin_selected()
    try:
        xbmcaddon.Addon(SKIN_ID)
    except RuntimeError:
        raise RuntimeError("Xonfluence is not registered in Kodi.")

    request = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "Settings.SetSettingValue",
        "params": {"setting": "lookandfeel.skin", "value": SKIN_ID},
    })
    response = json.loads(xbmc.executeJSONRPC(request))
    if response.get("result") is not True:
        raise RuntimeError("Kodi could not select Xonfluence.")
    if already_selected and xbmc.getSkinDir() != SKIN_ID:
        xbmc.executebuiltin("ReloadSkin", True)


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


def _wait_for_skin(monitor):
    stable = 0
    stable_since = None
    for unused in range(LOAD_TIMEOUT * 2):
        if monitor.waitForAbort(0.5):
            return False
        _confirm_skin_keep_prompt()
        try:
            selected = _skin_selected()
        except (RuntimeError, TypeError, ValueError):
            selected = False
        if selected and xbmc.getSkinDir() == SKIN_ID:
            stable += 1
            if stable_since is None:
                stable_since = time.time()
            if stable >= 6 and time.time() - stable_since >= CONFIRMATION_GRACE:
                return True
        else:
            stable = 0
            stable_since = None
    return False


def _skin_stays_loaded(monitor, seconds):
    for unused in range(seconds * 2):
        if monitor.waitForAbort(0.5):
            return False
        _confirm_skin_keep_prompt()
        try:
            if not _skin_selected() or xbmc.getSkinDir() != SKIN_ID:
                return False
        except (RuntimeError, TypeError, ValueError):
            return False
    return True


def _apply_pending_skin(monitor):
    # Let Kodi close the wizard's add-on window before changing the home skin.
    if monitor.waitForAbort(12):
        return False
    try:
        if (
            _skin_selected()
            and xbmc.getSkinDir() == SKIN_ID
            and _skin_stays_loaded(monitor, 10)
        ):
            _log("Xonfluence stayed selected after Kodi finished opening the build.")
            return True
        _set_skin()
        if _wait_for_skin(monitor) and _skin_stays_loaded(monitor, 10):
            _log("Xonfluence is loaded and selected.")
            return True
        _log("Kodi did not settle on Xonfluence after the first reload; retrying.", xbmc.LOGWARNING)
        _set_skin()
        if _wait_for_skin(monitor) and _skin_stays_loaded(monitor, 10):
            _log("Xonfluence is loaded and selected after retry.")
            return True
        _log("Kodi could not keep Xonfluence loaded; the saved preference will be checked next launch.", xbmc.LOGERROR)
    except (RuntimeError, TypeError, ValueError) as exc:
        _log("Could not apply Xonfluence: {}".format(exc), xbmc.LOGERROR)
    return False


def _jsonrpc(method, params):
    request = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params})
    response = json.loads(xbmc.executeJSONRPC(request))
    if "error" in response:
        raise RuntimeError(response["error"].get("message", "Kodi JSON-RPC request failed."))
    return response.get("result")


def _apply_private_memory_policy():
    try:
        with open(PRIVATE_MEMORY_POLICY_PATH, "r", encoding="utf-8") as policy_file:
            policy = json.load(policy_file)
        memory_limit = policy.get("stream_buffer_memory_mb") if isinstance(policy, dict) else None
        if type(memory_limit) is not int or memory_limit != 16:
            return
        current = _jsonrpc("Settings.GetSettingValue", {"setting": "filecache.memorysize"})
        current_size = current.get("value") if isinstance(current, dict) else None
        if type(current_size) is not int or current_size <= memory_limit:
            return
        _jsonrpc("Settings.SetSettingValue", {
            "setting": "filecache.memorysize",
            "value": memory_limit,
        })
        _log("Limited Kodi's stream-buffer memory to 16 MB for the private low-memory profile.")
    except (OSError, TypeError, ValueError, RuntimeError) as exc:
        _log("Could not apply the private low-memory setting: {}".format(exc), xbmc.LOGWARNING)


def _addon_enabled(addon_id):
    result = _jsonrpc("Addons.GetAddonDetails", {
        "addonid": addon_id,
        "properties": ["enabled"],
    })
    return result.get("addon", {}).get("enabled")


def _set_addon_enabled(addon_id, enabled):
    result = _jsonrpc("Addons.SetAddonEnabled", {"addonid": addon_id, "enabled": enabled})
    if result not in (True, "OK"):
        raise RuntimeError("Kodi could not change the {} add-on state.".format(addon_id))


def _safe_remove(path):
    if os.path.islink(path) or os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)


def _safe_join(root, parts):
    root = os.path.realpath(root)
    target = os.path.abspath(os.path.join(root, *parts))
    if target == root or os.path.commonpath((root, os.path.realpath(target))) != root:
        raise ValueError("The saved install transaction contains an unsafe path.")
    return target


def _journal_target(operation):
    location = operation.get("location")
    name = operation.get("name")
    if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
        raise ValueError("The saved install transaction contains an invalid add-on path.")
    home = xbmcvfs.translatePath("special://home")
    data = xbmcvfs.translatePath("special://profile/addon_data")
    if location == "addons":
        root = os.path.join(home, "addons")
    elif location == "addon_data":
        root = data
    elif location in ("skin_data", "weather_data"):
        parent = operation.get("parent")
        allowed = SUPPORTED_SKINS if location == "skin_data" else {WEATHER_ID}
        if parent not in allowed or name != "settings.xml":
            raise ValueError("The saved install transaction contains an invalid settings path.")
        root = os.path.join(data, parent)
    else:
        raise ValueError("The saved install transaction contains an unknown location.")
    return _safe_join(root, [name])


def _journal_backup(transaction, relative):
    if not isinstance(relative, str):
        raise ValueError("The saved install transaction has an invalid rollback path.")
    parts = relative.replace("\\", "/").split("/")
    if len(parts) < 2 or parts[0] != "rollback" or any(
        part in ("", ".", "..") for part in parts
    ):
        raise ValueError("The saved install transaction has an unsafe rollback path.")
    return _safe_join(transaction, parts)


def _restore_journal(transaction, journal):
    if journal.get("version") not in (1, 2) or not isinstance(journal.get("operations"), list):
        raise ValueError("The saved install transaction journal is not supported.")
    phase = journal.get("phase")
    if phase == "staging":
        return False
    if phase != "swapping":
        raise ValueError("The saved install transaction has an unknown state.")
    restored = False
    for operation in reversed(journal["operations"]):
        if not isinstance(operation, dict) or not isinstance(operation.get("had_target"), bool):
            raise ValueError("The saved install transaction has an invalid operation.")
        target = _journal_target(operation)
        backup = _journal_backup(transaction, operation.get("backup"))
        if operation["had_target"]:
            if os.path.lexists(backup):
                _safe_remove(target)
                os.makedirs(os.path.dirname(target), exist_ok=True)
                os.replace(backup, target)
                restored = True
        elif os.path.lexists(target):
            _safe_remove(target)
            restored = True
    return restored


def _restore_journal_addon_states(journal):
    states = journal.get("addon_states", {})
    if not isinstance(states, dict):
        raise ValueError("The saved install transaction has invalid add-on states.")
    for addon_id, enabled in states.items():
        if (
            not isinstance(addon_id, str)
            or not re.fullmatch(r"[A-Za-z0-9_.-]+", addon_id)
            or not isinstance(enabled, bool)
        ):
            raise ValueError("The saved install transaction has an invalid add-on state.")
        current = _addon_enabled(addon_id)
        if current is not enabled:
            _set_addon_enabled(addon_id, enabled)
            _log("Restored {} after an interrupted build install.".format(addon_id), xbmc.LOGWARNING)
    return True


def _save_pending_commit_addons(journal):
    addon_ids = journal.get("post_commit_enable", [])
    if not isinstance(addon_ids, list) or any(
        not isinstance(addon_id, str)
        or not re.fullmatch(r"[A-Za-z0-9_.-]+", addon_id)
        for addon_id in addon_ids
    ):
        raise ValueError("The committed build has an invalid service list.")
    if not addon_ids:
        return False
    os.makedirs(os.path.dirname(PENDING_COMMIT_PATH), exist_ok=True)
    temporary = PENDING_COMMIT_PATH + ".tmp"
    with open(temporary, "w", encoding="utf-8") as pending_file:
        json.dump(sorted(set(addon_ids)), pending_file)
        pending_file.flush()
        os.fsync(pending_file.fileno())
    os.replace(temporary, PENDING_COMMIT_PATH)
    return True


def _enable_pending_commit_addons():
    try:
        with open(PENDING_COMMIT_PATH, "r", encoding="utf-8") as pending_file:
            addon_ids = json.load(pending_file)
    except FileNotFoundError:
        return
    except (OSError, TypeError, ValueError) as exc:
        _log("Could not read the saved post-install service list: {}".format(exc), xbmc.LOGWARNING)
        return
    if not isinstance(addon_ids, list) or any(
        not isinstance(addon_id, str)
        or not re.fullmatch(r"[A-Za-z0-9_.-]+", addon_id)
        for addon_id in addon_ids
    ):
        _log("The saved post-install service list is invalid; it was left for inspection.", xbmc.LOGERROR)
        return
    failed = False
    for addon_id in addon_ids:
        try:
            details = _jsonrpc("Addons.GetAddonDetails", {
                "addonid": addon_id,
                "properties": ["enabled"],
            }).get("addon", {})
            if not details:
                raise RuntimeError("Kodi has not registered the add-on yet.")
            if details.get("enabled") is not True:
                _set_addon_enabled(addon_id, True)
            xbmc.sleep(500)
        except (RuntimeError, TypeError, ValueError) as exc:
            failed = True
            _log("Could not finish starting {} after build recovery: {}".format(addon_id, exc), xbmc.LOGWARNING)
    if not failed:
        try:
            os.remove(PENDING_COMMIT_PATH)
            _log("Finished starting the build services after Kodi restarted during installation.")
        except OSError:
            pass


def _restore_legacy_backups(transaction):
    rollback = os.path.join(transaction, "rollback")
    addon_root = os.path.join(xbmcvfs.translatePath("special://home"), "addons")
    data_root = xbmcvfs.translatePath("special://profile/addon_data")
    changed = False
    addon_backups = os.path.join(rollback, "addons")
    if os.path.isdir(addon_backups):
        for addon_id in os.listdir(addon_backups):
            if not re.fullmatch(r"[A-Za-z0-9_.-]+", addon_id):
                continue
            backup = _safe_join(addon_backups, [addon_id])
            target = _safe_join(addon_root, [addon_id])
            manifest = os.path.join(target, "addon.xml")
            valid_target = False
            try:
                ET.parse(manifest)
                valid_target = True
            except (OSError, ET.ParseError):
                pass
            if os.path.lexists(backup) and not valid_target:
                _safe_remove(target)
                os.makedirs(os.path.dirname(target), exist_ok=True)
                os.replace(backup, target)
                changed = True
    data_backups = os.path.join(rollback, "addon-data")
    if os.path.isdir(data_backups):
        for addon_id in os.listdir(data_backups):
            if not re.fullmatch(r"[A-Za-z0-9_.-]+", addon_id):
                continue
            backup = _safe_join(data_backups, [addon_id])
            target = _safe_join(data_root, [addon_id])
            if os.path.isdir(backup):
                if not os.path.lexists(target):
                    os.makedirs(os.path.dirname(target), exist_ok=True)
                    os.replace(backup, target)
                    changed = True
                elif os.path.isdir(target):
                    for entry in os.listdir(backup):
                        if not re.fullmatch(r"[A-Za-z0-9_.-]+", entry):
                            continue
                        saved = _safe_join(backup, [entry])
                        current = _safe_join(target, [entry])
                        if not os.path.lexists(current):
                            os.replace(saved, current)
                            changed = True
    return changed


def _cleanup_transaction(transaction):
    _safe_remove(transaction)
    _safe_remove(transaction + ".committed")


def _recover_transactions():
    roots = (TRANSACTION_ROOT, PREVIOUS_TRANSACTION_ROOT, LEGACY_TRANSACTION_ROOT)
    recovered = False
    for root in roots:
        if not os.path.isdir(root):
            continue
        for name in sorted(os.listdir(root)):
            if not re.fullmatch(r"\d{8}-\d{6}-[a-f0-9]{8}", name):
                continue
            transaction = _safe_join(root, [name])
            if not os.path.isdir(transaction):
                continue
            marker = transaction + ".committed"
            try:
                if os.path.isfile(marker):
                    journal_path = os.path.join(transaction, "journal.json")
                    if os.path.isfile(journal_path):
                        with open(journal_path, "r", encoding="utf-8") as journal_file:
                            journal = json.load(journal_file)
                        if _save_pending_commit_addons(journal):
                            recovered = True
                    _cleanup_transaction(transaction)
                    _log("Cleaned up a committed build transaction.")
                    continue
                journal_path = os.path.join(transaction, "journal.json")
                if os.path.isfile(journal_path):
                    with open(journal_path, "r", encoding="utf-8") as journal_file:
                        journal = json.load(journal_file)
                    if journal.get("phase") == "staging":
                        try:
                            _restore_journal_addon_states(journal)
                        except (RuntimeError, TypeError, ValueError) as state_exc:
                            _log(
                                "Could not restore paused add-ons after an interrupted build install: {}".format(state_exc),
                                xbmc.LOGERROR,
                            )
                            continue
                        _cleanup_transaction(transaction)
                        _log("Removed abandoned build staging files.", xbmc.LOGWARNING)
                        continue
                else:
                    journal = None

                previous_optiklean_state = None
                try:
                    previous_optiklean_state = _addon_enabled(OPTIKLEAN_ID)
                    if previous_optiklean_state is True:
                        _set_addon_enabled(OPTIKLEAN_ID, False)
                        xbmc.sleep(1500)
                except (RuntimeError, TypeError, ValueError):
                    previous_optiklean_state = None

                changed = (
                    _restore_journal(transaction, journal)
                    if journal is not None
                    else _restore_legacy_backups(transaction)
                )
                if changed:
                    xbmc.executebuiltin("UpdateLocalAddons", True)
                    xbmc.sleep(1000)
                    recovered = True
                    _log("Recovered Kodi add-ons and settings from an interrupted build install.", xbmc.LOGWARNING)
                try:
                    if journal is not None:
                        _restore_journal_addon_states(journal)
                except (RuntimeError, TypeError, ValueError) as state_exc:
                    _log(
                        "Could not restore paused add-ons after an interrupted build install: {}".format(state_exc),
                        xbmc.LOGERROR,
                    )
                    continue
                _cleanup_transaction(transaction)
                if previous_optiklean_state is True:
                    try:
                        _set_addon_enabled(OPTIKLEAN_ID, True)
                    except (RuntimeError, TypeError, ValueError) as exc:
                        _log("OptiKlean could not restart after transaction recovery: {}".format(exc), xbmc.LOGWARNING)
            except (OSError, RuntimeError, TypeError, ValueError, json.JSONDecodeError) as exc:
                _log("An interrupted build transaction still needs recovery: {}".format(exc), xbmc.LOGERROR)
    return recovered


def _configured_supported_skin():
    try:
        result = _jsonrpc("Settings.GetSettingValue", {"setting": "lookandfeel.skin"})
        skin_id = result.get("value") if isinstance(result, dict) else None
        return skin_id if skin_id in SUPPORTED_SKINS else None
    except (RuntimeError, TypeError, ValueError):
        return None


def main():
    global SKIN_ID
    monitor = xbmc.Monitor()
    _apply_private_memory_policy()
    last_marker_time = None
    if _recover_transactions():
        if os.path.isfile(MARKER_PATH) and _load_requested_skin():
            _apply_pending_skin(monitor)
        else:
            configured_skin = _configured_supported_skin()
            if configured_skin:
                SKIN_ID = configured_skin
                _apply_pending_skin(monitor)
        try:
            last_marker_time = os.path.getmtime(MARKER_PATH)
        except OSError:
            pass
    _enable_pending_commit_addons()
    last_pending_commit_check = time.monotonic()
    while not monitor.abortRequested():
        try:
            marker_time = os.path.getmtime(MARKER_PATH)
        except OSError:
            marker_time = None
        if marker_time is not None and marker_time != last_marker_time:
            last_marker_time = marker_time
            if _load_requested_skin():
                _apply_pending_skin(monitor)
        if time.monotonic() - last_pending_commit_check >= 15:
            _enable_pending_commit_addons()
            last_pending_commit_check = time.monotonic()
        if monitor.waitForAbort(2):
            break


if __name__ == "__main__":
    main()
