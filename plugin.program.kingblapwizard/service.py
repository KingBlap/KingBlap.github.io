"""Finish applying Xonfluence after the installer window closes and on Kodi startup."""
import json
import os
import time

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


def main():
    monitor = xbmc.Monitor()
    last_marker_time = None
    while not monitor.abortRequested():
        try:
            marker_time = os.path.getmtime(MARKER_PATH)
        except OSError:
            marker_time = None
        if marker_time is not None and marker_time != last_marker_time:
            last_marker_time = marker_time
            if _load_requested_skin():
                _apply_pending_skin(monitor)
        if monitor.waitForAbort(2):
            break


if __name__ == "__main__":
    main()
