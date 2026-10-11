# KingBlap Kodi Repository

This project provides two ways to install its Kodi add-ons: the KingBlap Kodi Repository lets you choose add-ons individually, while KingBlap Wizard offers separate public and private complete builds. The repository catalog lists 121 packages. Public Build 1.0.19 and Private Build 1.0.18 install and enable 78 add-ons, including 18 video add-ons, select Xonfluence 6.0.7, and configure Gismeteo for Thomasville, North Carolina.

Build 1.0.18 uses the Kodi 22 backup snapshot dated October 11, 2026. Compatibility and available features vary by Kodi version, device, add-on, and service provider.

## Install in Kodi

1. In Kodi, open Settings → System → Add-ons and enable Unknown sources if needed.
2. Open Settings → File Manager → Add source. Select the path field, enter https://kingblap.github.io/, and name the source KingBlap Repo.
3. Choose Add-ons → Install from zip file → KingBlap Repo.
4. Select repository.kingblap-1.0.0.zip and confirm any dependency prompt. Keep Kodi's official repository enabled.
5. Choose Install from repository → KingBlap Kodi Repository to browse and install add-ons.

## Install the complete Wizard build

1. Install or update KingBlap Wizard 1.0.28 from Install from repository → KingBlap Kodi Repository → Program add-ons. If needed, install the Wizard 1.0.28 ZIP from https://kingblap.github.io/repo/zips/plugin.program.kingblapwizard/plugin.program.kingblapwizard-1.0.28.zip.
2. Open the Wizard. It shows separate **Public Builds** and **Private Builds** folders before listing a build. The public 1.0.19 build does not require an access code and excludes saved add-on profile data and credentials from the backup. The private 1.0.18 build requires the shared 16-digit numeric access code and restores saved profile data for 34 add-ons.
3. Select the intended build and review the confirmation message before installing. The private build can replace matching saved add-on settings and login data. The Wizard's own API URL and access code are excluded and remain saved locally.
4. Let the download and installation finish, close the completion notice, and restart Kodi once.

The public archive is built without add-on account profile data. Its only user-data files are the sanitized Xonfluence and Gismeteo preferences needed for the visual setup and weather location. It does not include the backup's saved API keys or service credentials. The private build restores saved add-on profile data from the October 11 backup for 34 add-ons, including credentials stored by those add-ons. Anyone with the shared access code can download that private profile data, so share the code and private build only with intended recipients.

Back up Kodi before installing over an existing setup. Both choices replace packaged add-on files and remove XStream Player, Estuary MOD V2, and the OnePlay repository, then enable 78 add-ons. The public choice leaves other add-on account profiles in place; the private choice replaces matching profile data for its 34 included add-ons. Kodi libraries remain on the device. Gismeteo is configured for Thomasville, North Carolina.

## What both builds include

- 78 pre-enabled add-ons, including 18 video add-ons, supporting modules, artwork tools, Up Next, Gismeteo, and the KingBlap repository. The build archive records the exact add-on IDs.
- GIPTV 3.1.0 in place of XStream Player.
- Xonfluence 6.0.7 for Kodi 22.
- Eight supplied Demon Women pictures packaged with Xonfluence as a randomized, crossfading background slideshow.
- Sanitized, portable Xonfluence presentation settings.
- Gismeteo set to Thomasville, North Carolina (location ID 8771), with the active location refreshed after installation.
- **Public Build 1.0.19:** sanitized Xonfluence and Gismeteo settings only. No saved API keys, account credentials, or other add-on profile data from the backup.
- **Private Build 1.0.18:** saved add-on profile data from 34 add-ons, including service credentials saved in those profiles.
- Both archives exclude the KingBlap Wizard settings and access code; the installer preserves the Wizard settings already on the device.

Both archives exclude Kodi databases and libraries, standalone Kodi playlists and EPG files, texture thumbnails, and platform-specific native binaries. Keep the shared access code private because it grants access to saved account data in Private Build 1.0.18.

The repository was assembled from Windows Kodi 22 files. Windows-specific native packages are omitted from the portable build. Keep Kodi's official repository enabled so Kodi can install compatible platform dependencies where available.

## Current downloads

- Build list: https://kingblap.github.io/builds.txt
- Public build 1.0.19: choose Public Builds in KingBlap Wizard; no access code is needed.
- Private build 1.0.18: choose Private Builds in KingBlap Wizard after entering the access code.
- KingBlap repository installer: https://kingblap.github.io/repository.kingblap-1.0.0.zip
- Kodi add-on catalog: https://kingblap.github.io/repo/zips/addons.xml
- Package inventory and versions: addon_catalog.json

## Wizard build release history

| Build | Changes |
| --- | --- |
| **Wizard 1.0.28** | Requires exactly 16 numeric digits for private build access codes. |
| **Wizard 1.0.27** | Adds separate Public Builds and Private Builds folders; public downloads do not send an access code and reject credential-bearing archives. |
| **Public Build 1.0.19** | Built without backup account profiles, API keys, or saved service credentials. |
| **Private Build 1.0.18** | Restores saved add-on profile data from the October 11 backup while preserving the local Wizard URL and access code. |
| **1.0.17** | Preserves Gismeteo's supported language, units, timezone, weekend, and provider-icon preferences while setting Thomasville as location 1. |
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

The list below describes all 121 packages available in the repository. 78 are bundled and enabled by Wizard Build 1.0.18; the rest can be installed individually. Package versions are shown with their add-on IDs.

- In Build 1.0.18 — context.otaku — 1.0.35
- In Build 1.0.18 — context.prism — 4.0.2
- In Build 1.0.18 — context.seren — 3.0.2
- Repository only — inputstream.adaptive — 22.3.22
- Repository only — inputstream.ffmpegdirect — 22.2.7
- Repository only — inputstream.rtmp — 22.1.3
- In Build 1.0.18 — metadata.generic.albums — 1.0.20
- In Build 1.0.18 — metadata.generic.artists — 1.0.20
- In Build 1.0.18 — metadata.tvshows.themoviedb.org.python — 2.0.9
- Repository only — One.repo — 1.16
- Repository only — plugin.program.kingblapwizard — 1.0.26
- In Build 1.0.18 — plugin.video.absolution — 4.4.1
- In Build 1.0.18 — plugin.video.cosmos — 4.3.26
- In Build 1.0.18 — plugin.video.dailymotion_com — 2.4.5
- In Build 1.0.18 — plugin.video.forge — 0.2.13
- In Build 1.0.18 — plugin.video.gears — 2.4.3
- In Build 1.0.18 — plugin.video.genocide — 6.9.9
- In Build 1.0.18 — plugin.video.giptv — 3.1.0
- In Build 1.0.18 — plugin.video.homelander — 1.3.1
- In Build 1.0.18 — plugin.video.jet_guide — 0.0.21
- In Build 1.0.18 — plugin.video.loopguide — 3.8.2
- In Build 1.0.18 — plugin.video.looptv — 26+matrix.2
- In Build 1.0.18 — plugin.video.madtitansports — 2.0.44
- In Build 1.0.18 — plugin.video.otaku — 5.3.3
- In Build 1.0.18 — plugin.video.prism — 5.0.56
- In Build 1.0.18 — plugin.video.tatv2 — 1.0.3
- In Build 1.0.18 — plugin.video.thechains — 6.0.1
- In Build 1.0.18 — plugin.video.watchnixtoons2 — 0.14.23
- In Build 1.0.18 — plugin.video.zoro — 1.1.9
- In Build 1.0.18 — program.easyplayerswitch — 1.1.0
- In Build 1.0.18 — program.optiklean — 2.0.7
- Repository only — pvr.iptvsimple — 22.6.4
- Repository only — repository.709 — 1.0.2
- Repository only — repository.aliunde — 1.9.5
- Repository only — repository.autowidget — 1.1
- Repository only — repository.bugatsinho — 2.7
- Repository only — repository.butter — 2.2.0
- Repository only — repository.chainsrepo — 0.0.15
- Repository only — repository.cMaNWizard — 3.2
- Repository only — repository.cywteow — 1.1.1
- Repository only — repository.diggz — 28
- Repository only — repository.doomzday — 1.1.0
- Repository only — repository.enigmawiz — 2.1.6
- Repository only — repository.fenskeleton — 1.0.2
- Repository only — repository.forge — 0.1.0
- Repository only — repository.funstersplace — 0.3
- Repository only — repository.gaia.full — 8.0.0
- Repository only — repository.hooty — 1.0
- Repository only — repository.jewrepo — 1.6.0
- Repository only — repository.jmooremcc — 1.1.0
- In Build 1.0.18 — repository.kingblap — 1.0.0
- Repository only — repository.kodifitzwell — 0.0.1
- Repository only — repository.loop — 3.0.4
- Repository only — repository.madforit — 1.6
- Repository only — repository.Magnetic — 1.1.0b
- Repository only — repository.mtr81 — 1.0
- Repository only — repository.nixgates — 2.2.0
- Repository only — repository.octopus — 0.7.0
- Repository only — repository.peno64 — 1.5
- Repository only — repository.prism — 1.0
- Repository only — repository.redwizard — 1.2.2
- Repository only — repository.swagotaku — 0.0.2
- Repository only — repository.the666mafia — 1.0
- Repository only — repository.thecrew — 0.3.8
- Repository only — repository.thelab — 25.3.27
- Repository only — repository.vanilla21 — 1.0.0
- Repository only — repository.zachmorris — 1.0.4
- In Build 1.0.18 — resource.uisounds.appletv — 0.0.2
- In Build 1.0.18 — script.absolution.artwork — 4.1.7
- In Build 1.0.18 — script.ezmaintenanceplus — 2026.04.05.0
- In Build 1.0.18 — script.favourites — 8.1.2
- In Build 1.0.18 — script.homelander.artwork — 1.0.4
- In Build 1.0.18 — script.image.resource.select — 3.0.2
- In Build 1.0.18 — script.module.absolutionscrapers — 4.0.5
- In Build 1.0.18 — script.module.acctmgr — 1.1.6
- In Build 1.0.18 — script.module.acctvwr — 1.1.4
- In Build 1.0.18 — script.module.backports.zoneinfo — 0.2.1
- In Build 1.0.18 — script.module.beautifulsoup4 — 4.12.2
- In Build 1.0.18 — script.module.certifi — 2023.5.7
- In Build 1.0.18 — script.module.chainscrapers — 1.0.8
- In Build 1.0.18 — script.module.chardet — 5.1.0
- In Build 1.0.18 — script.module.cocoscrapers — 1.0.39
- In Build 1.0.18 — script.module.dateutil — 2.8.2
- In Build 1.0.18 — script.module.defusedxml — 0.6.0+matrix.1
- In Build 1.0.18 — script.module.dropbox — 10.3.1+matrix.1
- In Build 1.0.18 — script.module.fenomscrapers — 1.5.4
- In Build 1.0.18 — script.module.future — 1.0.0+matrix.1
- In Build 1.0.18 — script.module.gearsscrapers — 1.6.2
- In Build 1.0.18 — script.module.homelanderscrapers — 2.0.4
- In Build 1.0.18 — script.module.idna — 3.10.0
- In Build 1.0.18 — script.module.inputstreamhelper — 0.8.6
- In Build 1.0.18 — script.module.jetextractors — 3.3.26
- In Build 1.0.18 — script.module.kodi-six — 0.1.3.1
- In Build 1.0.18 — script.module.microjenscrapers — 1.4
- In Build 1.0.18 — script.module.myaccounts — 1.1.3
- In Build 1.0.18 — script.module.myconnpy — 8.0.33
- Repository only — script.module.pvr.artwork — 2.2.10
- In Build 1.0.18 — script.module.pyamf — 0.8.10+matrix.4
- In Build 1.0.18 — script.module.pyjsparser — 3.0.0
- In Build 1.0.18 — script.module.pyqrcode — 1.2.1+matrix.4
- In Build 1.0.18 — script.module.pytz — 2023.3.0+matrix.1
- In Build 1.0.18 — script.module.requests — 2.31.0
- In Build 1.0.18 — script.module.resolveurl — 5.1.210
- In Build 1.0.18 — script.module.routing — 0.2.3+matrix.1
- Repository only — script.module.simplecache — 2.0.2
- In Build 1.0.18 — script.module.simplejson — 3.19.1+matrix.1
- In Build 1.0.18 — script.module.simpleplugin3 — 3.0.6+matrix.1
- In Build 1.0.18 — script.module.six — 1.16.0+matrix.1
- In Build 1.0.18 — script.module.soupsieve — 2.4.1
- In Build 1.0.18 — script.module.tabulate — 0.9.1.2
- In Build 1.0.18 — script.module.tzdata — 2023.3.0+matrix.1
- In Build 1.0.18 — script.module.tzlocal — 5.0.1
- In Build 1.0.18 — script.module.unidecode — 1.3.6
- In Build 1.0.18 — script.module.urllib3 — 2.2.3
- In Build 1.0.18 — script.skinshortcuts — 3.0.4
- In Build 1.0.18 — script.xbmcbackup — 1.7.3
- In Build 1.0.18 — service.upnext — 1.1.9+matrix.1
- In Build 1.0.18 — service.xbmc.versioncheck — 0.5.30+matrix.1
- Repository only — skin.estuary.modv2 — 22.0+piers
- In Build 1.0.18 — skin.xonfluence — 6.0.7
- In Build 1.0.18 — weather.gismeteo — 0.6.4+matrix.1


## Updating the catalog

Add or replace an add-on ZIP under repo/zips/<addon-id>/<addon-id>-<version>.zip, then run the following in the repository root:

    python build_repository.py

Commit the updated ZIP, repo/zips/addons.xml, and repo/zips/addons.xml.md5 together.

After editing this README, regenerate the GitHub Pages landing page with `python tools/render_readme_site.py`.
