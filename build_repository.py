#!/usr/bin/env python3
"""Regenerate repo/zips/addons.xml and its MD5 from published add-on ZIPs."""
import hashlib
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ZIP_ROOT = ROOT / "repo" / "zips"

def version_key(value):
    return tuple((0, int(part)) if part.isdigit() else (1, part.casefold()) for part in re.findall(r"\d+|[A-Za-z]+", value))

def main():
    latest = {}
    for addon_dir in sorted(ZIP_ROOT.iterdir()):
        if not addon_dir.is_dir():
            continue
        for archive in sorted(addon_dir.glob("*.zip")):
            with zipfile.ZipFile(archive) as zf:
                candidates = [name for name in zf.namelist()
                              if name.count("/") == 1 and name.endswith("/addon.xml")]
                if len(candidates) != 1:
                    continue
                addon = ET.fromstring(zf.read(candidates[0]))
            addon_id = addon.get("id")
            if not addon_id:
                continue
            if addon_id == "service.upnext":
                # The upstream XML contains indentation-only text nodes that
                # produce trailing whitespace in the generated catalog.
                for element in addon.iter():
                    if element.text is not None and not element.text.strip():
                        element.text = None
                    if element.tail is not None and not element.tail.strip():
                        element.tail = None
            current = latest.get(addon_id)
            if current is None or version_key(addon.get("version", "")) > version_key(current.get("version", "")):
                latest[addon_id] = addon
    root = ET.Element("addons")
    for addon_id in sorted(latest, key=str.casefold):
        root.append(latest[addon_id])
    payload = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    (ZIP_ROOT / "addons.xml").write_bytes(payload)
    (ZIP_ROOT / "addons.xml.md5").write_text(hashlib.md5(payload).hexdigest(), encoding="ascii")
    print(f"Updated catalog for {len(latest)} add-ons.")

if __name__ == "__main__":
    main()
