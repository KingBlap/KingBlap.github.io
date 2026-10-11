# KingBlap Kodi Repository

This project provides two ways to install its Kodi add-ons: the **KingBlap Kodi Repository** lets you choose add-ons individually, while **KingBlap Wizard** installs the complete portable build. The repository catalog currently lists **121 packages**. Build **1.0.16** installs and enables **77 add-ons**, selects Xonfluence 6.0.7, and configures and refreshes Gismeteo for Thomasville, North Carolina.

The build was assembled from a Kodi 22 backup snapshot dated October 4, 2026. It targets Kodi 22. Compatibility and available features vary by Kodi version, device, add-on, and service provider.

## Install in Kodi

1. In Kodi, open **Settings → System → Add-ons** and enable **Unknown sources** if needed.
2. Open **Settings → File Manager → Add source**. Select the path field (usually **<None>**), enter `https://kingblap.github.io/`, and select **OK**. Name the source `KingBlap Repo` and save it.
3. Return to Kodi's home screen and choose **Add-ons → Install from zip file → KingBlap Repo**.
4. Select `repository.kingblap-1.0.0.zip`. If Kodi asks to install dependencies, choose **OK** and keep Kodi's official repository enabled.
5. Choose **Install from repository → KingBlap Kodi Repository** to browse the add-ons. Open a category, select an add-on, and choose **Install**.

This File Manager method also works on Android phones, Android TV, and Fire TV Stick; Kodi fetches the repository ZIP over HTTPS from the source. If the source appears empty or Kodi says it cannot connect, check that the path is exactly `https://kingblap.github.io/` and open that address in a browser on the same device. As a fallback, download the [repository installer ZIP](https://kingblap.github.io/repository.kingblap-1.0.0.zip), then use **File Manager → Add source → Browse** to add the folder containing the downloaded ZIP. Choose that source in **Install from zip file**.

## Install the complete wizard build

1. Install or update **KingBlap Wizard 1.0.24** from **Install from repository → KingBlap Kodi Repository → Program add-ons**. If the update is not listed, select **Add-ons → Check for updates** or install the [Wizard 1.0.24 ZIP](https://kingblap.github.io/repo/zips/plugin.program.kingblapwizard/plugin.program.kingblapwizard-1.0.24.zip).
2. Open **KingBlap Wizard**, choose **KingBlap Kodi Build 1.0.16**, and confirm.
3. Let the download and installation finish. Close the completion notice, allow Kodi to finish loading add-ons and Xonfluence, then restart Kodi once.
4. Gismeteo is enabled and set to Thomasville, North Carolina. The wizard selects it as the active location and forces a weather refresh, replacing any prior IP-detected city. Open GIPTV and enter your own provider details. Sign in to any other services you use.

Make a Kodi backup before installing over an existing setup. The wizard replaces the add-on files included in the build, removes XStream Player, the prior Estuary MOD V2 skin, and the OnePlay repository from the build target, and enables the 77 packaged add-ons. It also replaces the Gismeteo location settings with Thomasville, North Carolina. It does not wipe unrelated add-ons or Kodi libraries. Existing add-on settings outside the build archive may remain on the device.

## What Build 1.0.16 includes

- **77 pre-enabled add-ons**, including 18 video add-ons, supporting modules, artwork tools, Up Next, Gismeteo, and the KingBlap repository. The full 121-package repository catalog and versions are listed below; the build archive's `build_info.json` records the exact 77 add-on IDs in the build.
- **GIPTV 3.1.0** in place of XStream Player. GIPTV needs your own provider details and any provider-required account or playlist setup.
- **Xonfluence 6.0.7** for Kodi 22, based on [BadIDMan/skin.xonfluence](https://github.com/BadIDMan/skin.xonfluence) at [commit 827ace3](https://github.com/BadIDMan/skin.xonfluence/commit/827ace3b3de32f28682fca7cf1c48ac4cd19a76b). Estuary MOD V2 is still available as an optional repository add-on, but is not the build's selected skin.
- Eight supplied Demon Women pictures, packaged with Xonfluence as a randomized, crossfading background slideshow. The images use a skin-relative location for portability across Windows, Android phones, Android TV, and Fire TV Stick; Xonfluence scales portrait images to fill the display.
- Sanitized Xonfluence skin settings from the supplied snapshot. The archive keeps portable presentation settings and removes local paths, web addresses, and secret-like values.
- Gismeteo weather add-on enabled and selected for Thomasville, North Carolina (location ID `8771`). The build disables Gismeteo's automatic IP location, selects location 1 in Kodi, and forces a weather refresh so an older IP-detected city such as Dallas is replaced.
- The OnePlay repository (`One.repo`) is excluded from the build and removed by the wizard, including its saved add-on data. It remains available as an optional package in the repository catalog.
- Wizard fixes for Kodi add-on registration delays, install dialogs, the skin confirmation prompt, and applying Xonfluence after Kodi starts. The wizard also asks Kodi's add-on manager to obtain compatible platform-specific components when available.

The public build does **not** contain service passwords, provider credentials, account tokens, other add-on profile data beyond the sanitized skin settings and Thomasville weather location, Kodi databases, personal libraries, media-source paths, provider playlists or EPG data, caches, thumbnails, or platform-specific native binaries. Configure accounts and sources on each device after installation.

The repository was assembled from a Windows Kodi 22 snapshot. Four native binary packages (`inputstream.adaptive`, `inputstream.ffmpegdirect`, `inputstream.rtmp`, and `pvr.iptvsimple`) are Windows x86-64 packages in the catalog and are omitted from the portable build. Leave Kodi's official repository enabled; Kodi may install a compatible Android ARM version where available. Other packages retain their upstream Kodi compatibility metadata, so availability and behavior can vary across devices.

## Current downloads

- Build list: [builds.txt](https://kingblap.github.io/builds.txt)
- Build 1.0.16: [download the ZIP](https://github.com/KingBlap/KingBlap.github.io/releases/download/kingblap-build-v1.0.16/KingBlapKodiBuild-1.0.16.zip)
- KingBlap repository installer: [download the ZIP](https://kingblap.github.io/repository.kingblap-1.0.0.zip)
- Kodi add-on catalog: [addons.xml](https://kingblap.github.io/repo/zips/addons.xml)
- Package inventory and versions: [addon_catalog.json](addon_catalog.json)

## Wizard build release history

| Build | Changes |
| --- | --- |
| **1.0.16** | Selects Gismeteo location 1 and forces a weather refresh so Thomasville replaces a previously active IP-detected city such as Dallas. |
| **1.0.15** | Enabled and selected Gismeteo for Thomasville, North Carolina; excluded and removed the OnePlay repository from the build; configured weather location during installation. |
| **1.0.14** | Updated the wizard's Xonfluence version check to match the packaged Kodi 22 skin, version 6.0.7. |
| **1.0.13** | Added the eight-image Demon Women Xonfluence slideshow. |
| **1.0.12** | Enabled all 78 packaged add-ons and improved automatic confirmation and persistent application of Xonfluence. |
| **1.0.11** | Improved installation on devices where Kodi registers add-ons slowly. |
| **1.0.10** | Avoided invalid Kodi settings calls during installation. |
| **1.0.9** | Added portable, sanitized Xonfluence skin settings to the build archive. |
| **1.0.8** | Returned the build to a fresh Kodi 22-compatible Xonfluence package (6.0.6 at that release). |
| **1.0.7** | Temporarily switched the build skin to Estuary MOD V2 and added its supporting packages. This skin was later removed from the build and remains optional in the repository. |
| **1.0.6** | Updated the Xonfluence package to 5.1.1. |
| **1.0.5** | Restored Xonfluence 5.1 as the build skin. |
| **1.0.4** | Updated Xonfluence for Kodi 22. |
| **1.0.3** | Fixed portable build logos. |
| **1.0.2** | Fixed Kodi 22 wizard installation dialogs. |
| **1.0.1** | Refreshed add-on artwork after build installation. |
| **1.0.0** | Initial wizard build release. |

The main add-on change was replacing XStream Player with GIPTV. The repository contains GIPTV 3.1.0; the build does not include the user's provider playlist or login. Individual packages retain their upstream metadata and licenses.

## Repository package inventory

The list below describes all **121 packages available in the repository**. Only 77 are bundled and enabled by Wizard Build 1.0.16; the rest can be installed individually from the repository. It includes add-ons, dependencies, skins, and upstream add-on repositories. Package versions are shown alongside their add-on IDs.

- **In Build 1.0.16** — context.otaku — 1.0.35
- **In Build 1.0.16** — context.prism — 4.0.2
- **In Build 1.0.16** — context.seren — 3.0.2
- **Repository only** — inputstream.adaptive — 22.3.22
- **Repository only** — inputstream.ffmpegdirect — 22.2.7
- **Repository only** — inputstream.rtmp — 22.1.3
- **In Build 1.0.16** — metadata.generic.albums — 1.0.20
- **In Build 1.0.16** — metadata.generic.artists — 1.0.20
- **In Build 1.0.16** — metadata.tvshows.themoviedb.org.python — 2.0.9
- **Repository only** — One.repo — 1.16
- **Repository only** — plugin.program.kingblapwizard — 1.0.24
- **In Build 1.0.16** — plugin.video.absolution — 4.4.1
- **In Build 1.0.16** — plugin.video.cosmos — 4.3.26
- **In Build 1.0.16** — plugin.video.dailymotion_com — 2.4.5
- **In Build 1.0.16** — plugin.video.forge — 0.2.13
- **In Build 1.0.16** — plugin.video.gears — 2.4.3
- **In Build 1.0.16** — plugin.video.genocide — 6.9.9
- **In Build 1.0.16** — plugin.video.giptv — 3.1.0
- **In Build 1.0.16** — plugin.video.homelander — 1.3.1
- **In Build 1.0.16** — plugin.video.jet_guide — 0.0.21
- **In Build 1.0.16** — plugin.video.loopguide — 3.8.2
- **In Build 1.0.16** — plugin.video.looptv — 26+matrix.2
- **In Build 1.0.16** — plugin.video.madtitansports — 2.0.44
- **In Build 1.0.16** — plugin.video.otaku — 5.3.3
- **In Build 1.0.16** — plugin.video.prism — 5.0.56
- **In Build 1.0.16** — plugin.video.tatv2 — 1.0.3
- **In Build 1.0.16** — plugin.video.thechains — 6.0.1
- **In Build 1.0.16** — plugin.video.watchnixtoons2 — 0.14.23
- **In Build 1.0.16** — plugin.video.zoro — 1.1.9
- **In Build 1.0.16** — program.easyplayerswitch — 1.1.0
- **In Build 1.0.16** — program.optiklean — 2.0.7
- **Repository only** — pvr.iptvsimple — 22.6.4
- **Repository only** — repository.709 — 1.0.2
- **Repository only** — repository.aliunde — 1.9.5
- **Repository only** — repository.autowidget — 1.1
- **Repository only** — repository.bugatsinho — 2.7
- **Repository only** — repository.butter — 2.2.0
- **Repository only** — repository.chainsrepo — 0.0.15
- **Repository only** — repository.cMaNWizard — 3.2
- **Repository only** — repository.cywteow — 1.1.1
- **Repository only** — repository.diggz — 28
- **Repository only** — repository.doomzday — 1.1.0
- **Repository only** — repository.enigmawiz — 2.1.6
- **Repository only** — repository.fenskeleton — 1.0.2
- **Repository only** — repository.forge — 0.1.0
- **Repository only** — repository.funstersplace — 0.3
- **Repository only** — repository.gaia.full — 8.0.0
- **Repository only** — repository.hooty — 1.0
- **Repository only** — repository.jewrepo — 1.6.0
- **Repository only** — repository.jmooremcc — 1.1.0
- **In Build 1.0.16** — repository.kingblap — 1.0.0
- **Repository only** — repository.kodifitzwell — 0.0.1
- **Repository only** — repository.loop — 3.0.4
- **Repository only** — repository.madforit — 1.6
- **Repository only** — repository.Magnetic — 1.1.0b
- **Repository only** — repository.mtr81 — 1.0
- **Repository only** — repository.nixgates — 2.2.0
- **Repository only** — repository.octopus — 0.7.0
- **Repository only** — repository.peno64 — 1.5
- **Repository only** — repository.prism — 1.0
- **Repository only** — repository.redwizard — 1.2.2
- **Repository only** — repository.swagotaku — 0.0.2
- **Repository only** — repository.the666mafia — 1.0
- **Repository only** — repository.thecrew — 0.3.8
- **Repository only** — repository.thelab — 25.3.27
- **Repository only** — repository.vanilla21 — 1.0.0
- **Repository only** — repository.zachmorris — 1.0.4
- **In Build 1.0.16** — resource.uisounds.appletv — 0.0.2
- **In Build 1.0.16** — script.absolution.artwork — 4.1.7
- **In Build 1.0.16** — script.ezmaintenanceplus — 2026.04.05.0
- **In Build 1.0.16** — script.favourites — 8.1.2
- **In Build 1.0.16** — script.homelander.artwork — 1.0.4
- **In Build 1.0.16** — script.image.resource.select — 3.0.2
- **In Build 1.0.16** — script.module.absolutionscrapers — 4.0.5
- **In Build 1.0.16** — script.module.acctmgr — 1.1.6
- **In Build 1.0.16** — script.module.acctvwr — 1.1.4
- **In Build 1.0.16** — script.module.backports.zoneinfo — 0.2.1
- **In Build 1.0.16** — script.module.beautifulsoup4 — 4.12.2
- **In Build 1.0.16** — script.module.certifi — 2023.5.7
- **In Build 1.0.16** — script.module.chainscrapers — 1.0.8
- **In Build 1.0.16** — script.module.chardet — 5.1.0
- **In Build 1.0.16** — script.module.cocoscrapers — 1.0.39
- **In Build 1.0.16** — script.module.dateutil — 2.8.2
- **In Build 1.0.16** — script.module.defusedxml — 0.6.0+matrix.1
- **In Build 1.0.16** — script.module.dropbox — 10.3.1+matrix.1
- **In Build 1.0.16** — script.module.fenomscrapers — 1.5.4
- **In Build 1.0.16** — script.module.future — 1.0.0+matrix.1
- **In Build 1.0.16** — script.module.gearsscrapers — 1.6.2
- **In Build 1.0.16** — script.module.homelanderscrapers — 2.0.4
- **In Build 1.0.16** — script.module.idna — 3.10.0
- **In Build 1.0.16** — script.module.inputstreamhelper — 0.8.6
- **In Build 1.0.16** — script.module.jetextractors — 3.3.26
- **In Build 1.0.16** — script.module.kodi-six — 0.1.3.1
- **In Build 1.0.16** — script.module.microjenscrapers — 1.4
- **In Build 1.0.16** — script.module.myaccounts — 1.1.3
- **In Build 1.0.16** — script.module.myconnpy — 8.0.33
- **Repository only** — script.module.pvr.artwork — 2.2.10
- **In Build 1.0.16** — script.module.pyamf — 0.8.10+matrix.4
- **In Build 1.0.16** — script.module.pyjsparser — 3.0.0
- **In Build 1.0.16** — script.module.pyqrcode — 1.2.1+matrix.4
- **In Build 1.0.16** — script.module.pytz — 2023.3.0+matrix.1
- **In Build 1.0.16** — script.module.requests — 2.31.0
- **In Build 1.0.16** — script.module.resolveurl — 5.1.210
- **In Build 1.0.16** — script.module.routing — 0.2.3+matrix.1
- **Repository only** — script.module.simplecache — 2.0.2
- **In Build 1.0.16** — script.module.simplejson — 3.19.1+matrix.1
- **In Build 1.0.16** — script.module.simpleplugin3 — 3.0.6+matrix.1
- **In Build 1.0.16** — script.module.six — 1.16.0+matrix.1
- **In Build 1.0.16** — script.module.soupsieve — 2.4.1
- **In Build 1.0.16** — script.module.tabulate — 0.9.1.2
- **In Build 1.0.16** — script.module.tzdata — 2023.3.0+matrix.1
- **In Build 1.0.16** — script.module.tzlocal — 5.0.1
- **In Build 1.0.16** — script.module.unidecode — 1.3.6
- **In Build 1.0.16** — script.module.urllib3 — 2.2.3
- **Repository only** — script.skinshortcuts — 3.0.4
- **In Build 1.0.16** — script.xbmcbackup — 1.7.3
- **In Build 1.0.16** — service.upnext — 1.1.9+matrix.1
- **In Build 1.0.16** — service.xbmc.versioncheck — 0.5.30+matrix.1
- **Repository only** — skin.estuary.modv2 — 22.0+piers
- **In Build 1.0.16** — skin.xonfluence — 6.0.7
- **In Build 1.0.16** — weather.gismeteo — 0.6.4+matrix.1

## Updating the catalog

Add or replace an add-on ZIP under repo/zips/<addon-id>/<addon-id>-<version>.zip, then run the following in the repository root:

    python build_repository.py

Commit the updated ZIP, repo/zips/addons.xml, and repo/zips/addons.xml.md5 together.

After editing this README, regenerate the GitHub Pages landing page with `python tools/render_readme_site.py`.
