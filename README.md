# KingBlap Kodi Repository

A Kodi add-on repository and portable build installer assembled from the supplied Kodi 22 backup snapshot dated October 4, 2026, with GIPTV 3.1.0 included in place of XStream Player.

## Install in Kodi

1. In Kodi, open **Settings → System → Add-ons** and enable **Unknown sources** if needed.
2. In Kodi, open **File Manager → Add Source**, enter https://kingblap.github.io/, and name the source **KingBlap Kodi Repository**.
3. Choose **Add-ons → Install from zip file → KingBlap Kodi Repository** and select repository.kingblap-1.0.0.zip.
4. Choose **Install from repository → KingBlap Kodi Repository** to browse the add-ons.

## Android phones, Android TV, and Fire TV Stick

The repository installer and HTTPS catalog work in Kodi on Android, including phones, Android TV devices, and Fire TV Stick devices that can run Kodi. Use the same installation steps above; a touch screen or TV remote can navigate Kodi's menus. No Android APK or local file download is needed for the repository add-on.

## Install the KingBlap Wizard build

1. Install or update **KingBlap Wizard 1.0.5** from **Install from repository → KingBlap Kodi Repository → Program add-ons**.
2. If an older Wizard is already installed and no update appears, choose **Add-ons → Check for updates**. You can also install the [Wizard 1.0.5 ZIP](https://kingblap.github.io/repo/zips/plugin.program.kingblapwizard/plugin.program.kingblapwizard-1.0.5.zip).
3. Open **KingBlap Wizard**, choose **KingBlap Kodi Build 1.0.7**, and confirm the install.
4. Restart Kodi after the wizard reports completion. Open GIPTV and enter your own provider details.

Build 1.0.7 replaces Xonfluence with Estuary MOD V2 (version 22.0+piers), a Kodi 22 skin marked for all platforms. The skin includes 16:9, 18:9, and 19.5:9 screen layouts. Its Skin Shortcuts, Image Resource Select, PVR Artwork, Simple Cache, and Requests modules are included. Wizard 1.0.5 validates these packages, switches to Kodi's default Estuary while replacing the skin files, removes the installed Xonfluence add-on, and activates the new skin. It does not carry Xonfluence settings into the new skin. The build also replaces XStream Player and its saved settings when you confirm. The public build excludes account credentials, add-on profile data, Kodi databases, personal libraries, media source paths, and the profile thumbnail cache. Show and channel artwork is supplied by each add-on after you configure it. Keep Kodi's official repository enabled for Android-specific native binary dependencies; device and add-on compatibility can vary.

Build list: https://kingblap.github.io/builds.txt

Build archive: https://github.com/KingBlap/KingBlap.github.io/releases/download/kingblap-build-v1.0.7/KingBlapKodiBuild-1.0.7.zip

This repository was assembled from a Windows Kodi 22 snapshot. Its four native binary add-ons (`inputstream.adaptive`, `inputstream.ffmpegdirect`, `inputstream.rtmp`, and `pvr.iptvsimple`) are tagged `windows-x86_64`, so Kodi filters those Windows packages out on Android. Leave Kodi's official add-on repository enabled: it provides Android ARM builds of those binary dependencies where available. The other add-ons retain their original Kodi compatibility metadata, so individual add-on availability and service behavior can still vary by device and Kodi version.

Repository URL: https://kingblap.github.io/  
Installer: https://kingblap.github.io/repository.kingblap-1.0.0.zip  
Kodi catalog: https://kingblap.github.io/repo/zips/addons.xml

## Contents

This repository contains 120 add-on packages, including GIPTV 3.1.0 from the [GIPTV developer's Kodi repository](https://github.com/G00380316/GIPTV/tree/main/repo/zips/plugin.video.giptv), Kodi's Up Next dependency, Skin Shortcuts 3.0.4 from its [upstream Kodi add-on](https://github.com/MikeSiLVO/script.skinshortcuts), Estuary MOD V2 for Kodi 22 from its [Piers branch](https://github.com/b-jesch/skin.estuary.modv2/tree/Piers), its PVR Artwork module and Simple Cache dependency, KingBlap Wizard 1.0.5, and this repository add-on. GIPTV is marked for all platforms and requires `script.module.requests` and `service.upnext`. The Up Next package is from [Kodi's official Omega add-on repository](https://kodi.tv/addons/omega/service.upnext/); Simple Cache 2.0.2 is from [Kodi's Omega add-on repository](https://kodi.tv/addons/omega/script.module.simplecache/). Keep Kodi's official add-on repository enabled so Kodi can resolve other platform-specific dependencies. Xonfluence and XStream Player were removed. The repository packages do not include Kodi profile databases, personal account data, settings, or the profile thumbnail cache. Individual packages retain their metadata and licensing information.

- context.otaku — 1.0.35
- context.prism — 4.0.2
- context.seren — 3.0.2
- inputstream.adaptive — 22.3.22
- inputstream.ffmpegdirect — 22.2.7
- inputstream.rtmp — 22.1.3
- metadata.generic.albums — 1.0.20
- metadata.generic.artists — 1.0.20
- metadata.tvshows.themoviedb.org.python — 2.0.9
- One.repo — 1.16
- plugin.program.kingblapwizard — 1.0.5
- plugin.video.absolution — 4.4.1
- plugin.video.cosmos — 4.3.26
- plugin.video.dailymotion_com — 2.4.5
- plugin.video.forge — 0.2.13
- plugin.video.gears — 2.4.3
- plugin.video.genocide — 6.9.9
- plugin.video.giptv — 3.1.0
- plugin.video.homelander — 1.3.1
- plugin.video.jet_guide — 0.0.21
- plugin.video.loopguide — 3.8.2
- plugin.video.looptv — 26+matrix.2
- plugin.video.madtitansports — 2.0.44
- plugin.video.otaku — 5.3.3
- plugin.video.prism — 5.0.56
- plugin.video.tatv2 — 1.0.3
- plugin.video.thechains — 6.0.1
- plugin.video.watchnixtoons2 — 0.14.23
- plugin.video.zoro — 1.1.9
- program.easyplayerswitch — 1.1.0
- program.optiklean — 2.0.7
- pvr.iptvsimple — 22.6.4
- repository.709 — 1.0.2
- repository.aliunde — 1.9.5
- repository.autowidget — 1.1
- repository.bugatsinho — 2.7
- repository.butter — 2.2.0
- repository.chainsrepo — 0.0.15
- repository.cMaNWizard — 3.2
- repository.cywteow — 1.1.1
- repository.diggz — 28
- repository.doomzday — 1.1.0
- repository.enigmawiz — 2.1.6
- repository.fenskeleton — 1.0.2
- repository.forge — 0.1.0
- repository.funstersplace — 0.3
- repository.gaia.full — 8.0.0
- repository.hooty — 1.0
- repository.jewrepo — 1.6.0
- repository.jmooremcc — 1.1.0
- repository.kingblap — 1.0.0
- repository.kodifitzwell — 0.0.1
- repository.loop — 3.0.4
- repository.madforit — 1.6
- repository.Magnetic — 1.1.0b
- repository.mtr81 — 1.0
- repository.nixgates — 2.2.0
- repository.octopus — 0.7.0
- repository.peno64 — 1.5
- repository.prism — 1.0
- repository.redwizard — 1.2.2
- repository.swagotaku — 0.0.2
- repository.the666mafia — 1.0
- repository.thecrew — 0.3.8
- repository.thelab — 25.3.27
- repository.vanilla21 — 1.0.0
- repository.zachmorris — 1.0.4
- resource.uisounds.appletv — 0.0.2
- script.absolution.artwork — 4.1.7
- script.ezmaintenanceplus — 2026.04.05.0
- script.favourites — 8.1.2
- script.homelander.artwork — 1.0.4
- script.image.resource.select — 3.0.2
- script.module.absolutionscrapers — 4.0.5
- script.module.acctmgr — 1.1.6
- script.module.acctvwr — 1.1.4
- script.module.backports.zoneinfo — 0.2.1
- script.module.beautifulsoup4 — 4.12.2
- script.module.certifi — 2023.5.7
- script.module.chainscrapers — 1.0.8
- script.module.chardet — 5.1.0
- script.module.cocoscrapers — 1.0.39
- script.module.dateutil — 2.8.2
- script.module.defusedxml — 0.6.0+matrix.1
- script.module.dropbox — 10.3.1+matrix.1
- script.module.fenomscrapers — 1.5.4
- script.module.future — 1.0.0+matrix.1
- script.module.gearsscrapers — 1.6.2
- script.module.homelanderscrapers — 2.0.4
- script.module.idna — 3.10.0
- script.module.inputstreamhelper — 0.8.6
- script.module.jetextractors — 3.3.26
- script.module.kodi-six — 0.1.3.1
- script.module.microjenscrapers — 1.4
- script.module.myaccounts — 1.1.3
- script.module.myconnpy — 8.0.33
- script.module.pvr.artwork — 2.2.10
- script.module.pyamf — 0.8.10+matrix.4
- script.module.pyjsparser — 3.0.0
- script.module.pyqrcode — 1.2.1+matrix.4
- script.module.pytz — 2023.3.0+matrix.1
- script.module.requests — 2.31.0
- script.module.resolveurl — 5.1.210
- script.module.routing — 0.2.3+matrix.1
- script.module.simplecache — 2.0.2
- script.module.simplejson — 3.19.1+matrix.1
- script.module.simpleplugin3 — 3.0.6+matrix.1
- script.module.six — 1.16.0+matrix.1
- script.module.soupsieve — 2.4.1
- script.module.tabulate — 0.9.1.2
- script.module.tzdata — 2023.3.0+matrix.1
- script.module.tzlocal — 5.0.1
- script.module.unidecode — 1.3.6
- script.module.urllib3 — 2.2.3
- script.skinshortcuts — 3.0.4
- script.xbmcbackup — 1.7.3
- service.upnext — 1.1.9+matrix.1
- service.xbmc.versioncheck — 0.5.30+matrix.1
- skin.estuary.modv2 — 22.0+piers
- weather.gismeteo — 0.6.4+matrix.1

## Updating the catalog

Add or replace an add-on ZIP under repo/zips/<addon-id>/<addon-id>-<version>.zip, then run the following in the repository root:

    python build_repository.py

Commit the updated ZIP, repo/zips/addons.xml, and repo/zips/addons.xml.md5 together.
