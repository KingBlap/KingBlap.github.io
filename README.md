# KingBlap Kodi Repository

Install individual add-ons from the KingBlap Kodi Repository, or install a complete public or private build with **KingBlap Wizard 1.0.52**. Builds are available for **Kodi 21.3** and **Kodi 22**.

Updated October 14, 2026.

**Kodi File Manager source:** `https://kingblap.github.io/`

[Install the repository](#install-the-repository) · [Public builds](#install-a-public-build) · [Private builds](#install-a-private-build) · [Contents](#what-is-included) · [Recent updates](#recent-updates) · [Downloads](#downloads)

## Current builds

| Kodi version on your device | Build | Build version | Bundled add-ons | Private access code |
| --- | --- | --- | --- | --- |
| Kodi 21.3 | Public | 1.0.22 | 81 | Not required |
| Kodi 22 | Public | 1.0.22 | 79 | Not required |
| Kodi 21.3 | Private | 1.0.22 | 81 | Required: 16 digits |
| Kodi 22 | Private | 1.0.35 | 79 | Required: 16 digits |

Public and private builds for the same Kodi version contain the same add-on packages. Public builds include sanitized skin and weather preferences. Private builds also restore selected saved add-on profiles and configure GIPTV for IPTV Simple.

Check your Kodi version in **Settings → System information** before selecting a build. Back up an existing setup before installing: the Wizard replaces packaged add-on files and skin preferences, and private builds can replace saved settings and login data for included add-ons. Keep **Kodi Add-on repository** enabled so Kodi can obtain dependencies for your device.

## Install the repository

### Add the source in Kodi File Manager

1. Open Kodi and select **Settings** (the gear icon).
2. Open **System → Add-ons → Unknown sources** and enable it. Accept Kodi's confirmation if you want to proceed.
3. Return to **Settings → File Manager → Add source**.
4. Select **<None>** and enter `https://kingblap.github.io/`, including the final slash. Select **OK**.
5. Enter **KingBlap Repo** as the source name and select **OK** again.

File Manager saves the source. Continue in Kodi's Add-ons area to install the repository. Menu positions can vary by skin; Kodi documents its [File Manager](https://kodi.wiki/view/File_manager) and [Add-on manager](https://kodi.wiki/view/Add-on_manager).

### Install the repository and Wizard from Add-ons

1. Return to Kodi's home screen and open **Add-ons**.
2. Select the **open box/package icon** to enter the Add-on browser.
3. Select **Install from zip file → KingBlap Repo**.
4. Select **repository.kingblap-1.0.0.zip**. Accept any dependency prompt and wait for the **KingBlap Kodi Repository installed** notification.
5. Select **Install from repository → KingBlap Kodi Repository → Program add-ons → KingBlap Wizard**.
6. Select **Install**, accept any dependency prompt, and wait for the Wizard installed notification. The current Wizard version is **1.0.52**.
7. Open the Wizard from **Add-ons → Program add-ons → KingBlap Wizard**.

### Install from a downloaded ZIP or USB drive

If you already have the ZIP on your device, download [repository.kingblap-1.0.0.zip](https://kingblap.github.io/repository.kingblap-1.0.0.zip) to a location Kodi can access, such as Downloads or a USB drive. Enable Unknown sources, then open **Add-ons → open box icon → Install from zip file**, browse to that ZIP, and select it. Continue with the **Install from repository** steps above.

The [Wizard 1.0.52 ZIP](https://kingblap.github.io/repo/zips/plugin.program.kingblapwizard/plugin.program.kingblapwizard-1.0.52.zip) can also be installed through **Install from zip file** if you need to update the Wizard directly.

### Install individual add-ons

Open **Add-ons → open box icon → Install from repository → KingBlap Kodi Repository**. Choose a category such as **Video add-ons** or **Program add-ons**, select an add-on, and choose **Install**. The repository catalog contains **121 packages**; the complete builds bundle the smaller sets shown above.

## Install a public build

Follow these steps on either Kodi 21.3 or Kodi 22. A public build does not require the private access code.

1. Install or update **KingBlap Wizard 1.0.52** using the repository instructions above.
2. Open **Add-ons → Program add-ons → KingBlap Wizard**.
3. Choose **Public Builds**. The Wizard shows the public build that matches the Kodi version running on this device.
4. Select the matching entry below.
5. Review the installation notice and choose **Install build**.
6. Leave Kodi open while the Wizard downloads, verifies, and installs the build. Close the completion notice, let the skin finish applying, and restart Kodi once.

| Device | Entry in Public Builds |
| --- | --- |
| Kodi 21.3 | **Public KingBlap Build for Kodi 21.3 1.0.22 (download)** |
| Kodi 22 | **Public KingBlap Build for Kodi 22 1.0.22 (download)** |

Both public builds download directly in the Wizard and verify the archive's SHA-256 checksum. The Wizard combines the download parts automatically.

Public builds import only sanitized Xonfluence and Gismeteo settings. They omit saved account profiles, API keys, credentials, IPTV playlists, and guides from the backup. Enter your own account information in any add-ons you use. For GIPTV/live TV, configure your own GIPTV account and its IPTV Simple integration; public builds do not preload an account playlist or IPTV Simple instance settings.

## Install a private build

Private builds require the **16-digit private build access code** supplied privately. This is the Wizard access code, separate from any IPTV username or password.

1. Install or update **KingBlap Wizard 1.0.52** using the repository instructions above.
2. Open the Wizard's add-on information page from **Add-ons → open box icon → My add-ons → Program add-ons → KingBlap Wizard** and choose **Configure**.
3. Under **Private build access**, enter the code in **Private build access code**, then select **OK**. Keep **Build service URL** at its default unless you have been given a replacement address.
4. Open **Add-ons → Program add-ons → KingBlap Wizard → Private Builds**.
5. Both Kodi versions are listed. Select the entry that matches the Kodi version on this device, using the table below. The Wizard blocks a private build intended for a different Kodi major version.
6. Review the notice about restoring saved add-on settings and login data, then choose **Install build**.
7. Leave Kodi open until installation finishes. Close the completion notice, let the skin finish applying, and restart Kodi once.

| Device | Entry in Private Builds |
| --- | --- |
| Kodi 21.3 | **Private KingBlap Build for Kodi 21.3 (1.0.22)** |
| Kodi 22 | **Private KingBlap Build for Kodi 22 1.0.35** |

Private builds list and download through the protected Cloudflare build service. Selected saved add-on profiles, including saved service credentials, are restored. Keep private archives and the access code with their intended recipients. The access code is not published in this README, and the Wizard preserves its own service URL and access-code settings.

## What is included

### Appearance and shared features

| Feature | Kodi 21.3 builds | Kodi 22 builds |
| --- | --- | --- |
| Skin | Xonfluence (SKINBASE) 5 | Xonfluence 6.0.7 |
| Interface colors | Fire | Fire |
| Font | Massive | Massive |
| Backgrounds | Eight supplied Demon Women images in a randomized, crossfading slideshow | Same eight-image slideshow |
| Weather | Gismeteo 0.6.4+matrix.1, Thomasville, North Carolina | Same weather add-on and location |
| Up Next | 1.1.9+matrix.1 | 1.1.9+matrix.1 |
| Skin Shortcuts | 2.0.3 | 3.0.4 |
| Build add-on packages | 81, enabled by the Wizard | 79, enabled by the Wizard |

All four builds include these add-ons and their supporting modules:

- **Video:** Absolution, C.O.S.M.O.S, DailyMotion, Forge, The Gears, Genocide, Homelander, The Chains, and Zoro.
- **Live TV, guides, and sports:** GIPTV 3.1.0, TV Guide - Beta, Loop Guide, Loop TV, and Mad Titan Sports.
- **Anime and cartoons:** Otaku, Toonami Aftermath TV, and WatchNixtoons2.
- **Programs and tools:** Backup, Easy Player Switch, OptiKlean, and EZ Maintenance+.
- **Supporting add-ons:** Up Next, artwork helpers, account and resolver modules, metadata scrapers, Apple TV UI Sounds, and the KingBlap repository.

**Kodi 21.3 also includes Prism and its context menu. Kodi 22 also includes Xstream Pro 1.1.4.** Xstream Pro remains available as an add-on in Kodi 22; the private build's IPTV Simple configuration uses GIPTV, and Xstream Pro's automatic PVR sync is disabled.

### Public and private settings

| Included data or behavior | Public builds | Private builds |
| --- | --- | --- |
| Add-on packages for the chosen Kodi version | Included | Same packages |
| Fire colors, Massive font, slideshow, and Thomasville weather | Included | Included |
| Saved account settings, credentials, and API keys from the backup | Excluded | Selected saved add-on profiles are restored |
| Preloaded GIPTV playlist | Excluded; configure your own account | Filtered local USA and 24/7 playlist included |
| IPTV Simple configuration | Configure after entering your own account details | Points to GIPTV's local playlist and lightweight guide file |
| Saved add-on databases and history | Excluded from the archive | Some are included in selected saved profiles |
| Existing account profiles on the device | Other account profiles are left in place | Matching included profiles can be replaced |

GIPTV's packaged IPTV Simple export limits live groups to **USA and 24/7**. The private builds preload that filtered lineup and use an **empty local XMLTV guide** for IPTV Simple to reduce the memory needed on TVs. The provider-wide XMLTV feed is not imported by that integration; guide information inside GIPTV remains separate.

The Wizard requests device-compatible **IPTV Simple** and **InputStream** components through Kodi's add-on manager. Their platform-specific native binaries are not bundled in these archives. Keep Kodi's official repository enabled.

Build installation removes **XStream Player**, **Estuary MOD V2**, **Aeon Nox: SiLVO**, **OnePlay**, and duplicate legacy KingBlap installers, including their matching saved settings. XStream Player and Xstream Pro are separate add-ons. Kodi 21.3 uses its compatible Xonfluence SKINBASE package in place of the Kodi 22 skin package.

Kodi's core media libraries, media databases, and texture thumbnails are excluded from the build archives. Selected private add-on profiles can contain their own databases, caches, bookmarks, and history.

## Recent updates

| Release or change | What was updated |
| --- | --- |
| **Wizard 1.0.52** | Checks installed Xonfluence files before preserving the active skin. If files are incomplete, the build replaces them and confirms the skin loads before committing. |
| **Wizard 1.0.51** | Honors the saved Xonfluence selection after recovery from an interrupted install, then records the request as handled. |
| **Wizard 1.0.50** | Recovers incomplete installs after Kodi restarts, pauses background add-on services during file changes, and starts IPTV Simple/GIPTV after the build commits. |
| **Wizard 1.0.49** | Reports preparation progress more often, checks add-on registration in batches, and starts GIPTV's IPTV Simple channel import after the other build and skin setup is complete. Removes the synchronous artwork-cache sweep from installation. |
| **Wizard 1.0.48 / Private Builds 1.0.22 and 1.0.35** | Replaces stale IPTV Simple instances cleanly, stores a sync state matching the packaged USA/24/7 playlist and empty guide, and avoids rebuilding that lineup as soon as Kodi starts. |
| **Wizard 1.0.47 / Kodi 21.3 Public Build 1.0.22** | Kodi 21.3 public builds now show a named direct download with checksum verification. The public package matches the Kodi 21.3 private package set and includes Fire/Massive with sanitized skin and weather settings. |
| **Wizard 1.0.46 / Kodi 22 Public Build 1.0.22** | The Kodi 22 public package now matches Private Build 1.0.34's 79 add-on packages and Fire/Massive appearance, while omitting saved accounts and IPTV profile data. |
| **Wizard 1.0.45** | Both Kodi 21.3 and Kodi 22 private builds appear together. Installation is blocked when the selected private build targets the wrong Kodi major version. |
| **Wizard 1.0.44** | Kodi 21.3 private builds gained direct listing and downloads through the protected service. |
| **Appearance updates in Wizard 1.0.42–1.0.43** | Aeon Nox: SiLVO was removed from the builds. Fire colors and the Massive font are applied, and an already active, matching Xonfluence version is kept loaded during routine updates. |
| **Current private builds: Kodi 21.3 1.0.22 / Kodi 22 1.0.35** | GIPTV supplies the filtered USA/24/7 playlist for IPTV Simple with a lightweight local guide. The private builds apply Fire and Massive and restore selected saved add-on profiles. |
| **Current bundled add-ons** | The packages include C.O.S.M.O.S 4.3.54, Mad Titan Sports 2.0.45, GIPTV 3.1.0, Up Next 1.1.9+matrix.1, and the Kodi-specific Xonfluence/Skin Shortcuts versions listed above. |

To apply a newer full build, first update the Wizard, then reopen **Public Builds** or **Private Builds** and install the current build for your Kodi version. Updating the Wizard alone does not apply a new full build archive.

## Help with installation

- **Wizard 1.0.52 is missing:** open the Add-on browser's side menu and choose **Check for updates**. Install the available KingBlap Wizard update, or use the linked Wizard ZIP below.
- **Kodi 21.3 public build is missing:** update the Wizard to 1.0.52 and reopen **Public Builds** on Kodi 21.3. That menu shows the public build for the running Kodi version.
- **Private builds will not open:** check that **Private build access code** contains exactly 16 numeric digits, then reopen the Wizard. Use the code you received privately.
- **Kodi was closed during installation:** update the Wizard to 1.0.52 and start Kodi again. It will restore the last safe add-on state from an interrupted install; then reopen the build list and install again if the build did not finish.
- **Kodi version mismatch:** select Kodi 21.3's build on Kodi 21.3 or Kodi 22's build on Kodi 22.
- **Build profile data list error:** update the Wizard and select the current private release shown in the table above. If installation still fails, record the error and check the Kodi log.
- **A dependency cannot install:** enable Kodi's official repository and check the device's internet connection and available storage.
- **You see .part001/.part002/.part003 files:** install the complete build through the Wizard. These are download parts that the Wizard combines; Kodi's **Install from zip file** step is for the repository or Wizard add-on ZIP.

## Downloads

- [Repository installer 1.0.0](https://kingblap.github.io/repository.kingblap-1.0.0.zip)
- [KingBlap Wizard 1.0.52](https://kingblap.github.io/repo/zips/plugin.program.kingblapwizard/plugin.program.kingblapwizard-1.0.52.zip)
- [Current public and private build list](https://kingblap.github.io/builds.txt)
- [Repository add-on catalog](https://kingblap.github.io/repo/zips/addons.xml)
- [Repository package inventory](https://kingblap.github.io/addon_catalog.json)
- [Repository website and installation guide](https://kingblap.github.io/)

Public builds download through **Wizard → Public Builds**. Private builds download through **Wizard → Private Builds** after entering the private access code.

## Build package inventory

These versions are read from the current released public archives. Each Kodi version's private build has the same packaged add-on files as its public build. **Not bundled** means that package is absent from that Kodi version's archive. The counts include supporting modules and the KingBlap repository; the Wizard is installed separately, and Kodi obtains native components for the device.

| Add-on | Package ID | Kodi 21.3 | Kodi 22 |
| --- | --- | --- | --- |
| Otaku - Global Context Menu Items | `context.otaku` | 1.0.35 | 1.0.35 |
| Prism - Global Context Menu Items | `context.prism` | 4.0.2 | Not bundled |
| Seren - Global Context Menu Items | `context.seren` | 3.0.2 | 3.0.2 |
| Generic Album Scraper | `metadata.generic.albums` | 1.0.20 | 1.0.20 |
| Generic Artist Scraper | `metadata.generic.artists` | 1.0.20 | 1.0.20 |
| TMDb TV Shows | `metadata.tvshows.themoviedb.org.python` | 2.0.9 | 2.0.9 |
| Absolution | `plugin.video.absolution` | 4.4.1 | 4.4.1 |
| C.O.S.M.O.S | `plugin.video.cosmos` | 4.3.54 | 4.3.54 |
| DailyMotion.com | `plugin.video.dailymotion_com` | 2.4.5 | 2.4.5 |
| Forge | `plugin.video.forge` | 0.2.13 | 0.2.13 |
| The Gears | `plugin.video.gears` | 2.4.3 | 2.4.3 |
| Genocide | `plugin.video.genocide` | 6.9.9 | 6.9.9 |
| GIPTV | `plugin.video.giptv` | 3.1.0 | 3.1.0 |
| Homelander | `plugin.video.homelander` | 1.3.1 | 1.3.1 |
| TV Guide - Beta | `plugin.video.jet_guide` | 0.0.21 | 0.0.21 |
| Loop Guide | `plugin.video.loopguide` | 3.8.2 | 3.8.2 |
| Loop TV | `plugin.video.looptv` | 26+matrix.2 | 26+matrix.2 |
| Mad Titan Sports V2.0 | `plugin.video.madtitansports` | 2.0.45 | 2.0.45 |
| Otaku | `plugin.video.otaku` | 5.3.3 | 5.3.3 |
| Prism | `plugin.video.prism` | 5.0.56 | Not bundled |
| Toonami Aftermath TV | `plugin.video.tatv2` | 1.0.3 | 1.0.3 |
| The Chains | `plugin.video.thechains` | 6.0.1 | 6.0.1 |
| WatchNixtoons2 | `plugin.video.watchnixtoons2` | 0.14.23 | 0.14.23 |
| Xstream Pro | `plugin.video.xstream-pro` | Not bundled | 1.1.4 |
| Zoro | `plugin.video.zoro` | 1.1.9 | 1.1.9 |
| Easy Player Switch | `program.easyplayerswitch` | 1.1.0 | 1.1.0 |
| OptiKlean | `program.optiklean` | 2.0.7 | 2.0.7 |
| Recordlabel Icons - White | `resource.images.recordlabels.white` | 0.0.7 | 0.0.7 |
| Studio Icons - White | `resource.images.studios.white` | 0.0.34 | 0.0.34 |
| AppleTv UI Sounds | `resource.uisounds.appletv` | 0.0.2 | 0.0.2 |
| Absolution Artwork | `script.absolution.artwork` | 4.1.7 | 4.1.7 |
| EZ Maintenance+ | `script.ezmaintenanceplus` | 2026.04.05.0 | 2026.04.05.0 |
| Favourites script | `script.favourites` | 8.1.2 | 8.1.2 |
| Homelander Artwork | `script.homelander.artwork` | 1.0.4 | 1.0.4 |
| Image Resource Select Addon | `script.image.resource.select` | 3.0.2 | 3.0.2 |
| Absolution Scrapers Module | `script.module.absolutionscrapers` | 4.0.5 | 4.0.5 |
| Account Manager Lite | `script.module.acctmgr` | 1.2.0a | 1.2.0a |
| Account Viewer | `script.module.acctvwr` | 1.1.5 | 1.1.5 |
| zoneinfo | `script.module.backports.zoneinfo` | 0.2.1 | 0.2.1 |
| beautifulsoup4 | `script.module.beautifulsoup4` | 4.12.2 | 4.12.2 |
| certifi | `script.module.certifi` | 2023.5.7 | 2023.5.7 |
| Chains Scrapers | `script.module.chainscrapers` | 1.0.8 | 1.0.8 |
| chardet | `script.module.chardet` | 5.1.0 | 5.1.0 |
| CocoScrapers Module | `script.module.cocoscrapers` | 1.0.39 | 1.0.39 |
| python-dateutil | `script.module.dateutil` | 2.8.2 | 2.8.2 |
| defusedxml | `script.module.defusedxml` | 0.6.0+matrix.1 | 0.6.0+matrix.1 |
| Dropbox API | `script.module.dropbox` | 10.3.1+matrix.1 | 10.3.1+matrix.1 |
| FenomScrapers Module | `script.module.fenomscrapers` | 1.5.4 | 1.5.4 |
| future | `script.module.future` | 1.0.0+matrix.1 | 1.0.0+matrix.1 |
| Gears Scrapers | `script.module.gearsscrapers` | 1.6.2 | 1.6.2 |
| homelanderscrapers Module | `script.module.homelanderscrapers` | 2.0.4 | 2.0.4 |
| idna | `script.module.idna` | 3.10.0 | 3.10.0 |
| InputStream Helper | `script.module.inputstreamhelper` | 0.8.6 | 0.8.6 |
| JetExtractors | `script.module.jetextractors` | 3.3.27 | 3.3.27 |
| Kodi Six | `script.module.kodi-six` | 0.1.3.1 | 0.1.3.1 |
| MicroJen Scraper Module | `script.module.microjenscrapers` | 1.4 | 1.4 |
| My Accounts | `script.module.myaccounts` | 1.1.3 | 1.1.3 |
| mysql-connector-python | `script.module.myconnpy` | 8.0.33 | 8.0.33 |
| PyAMF | `script.module.pyamf` | 0.8.10+matrix.4 | 0.8.10+matrix.4 |
| pyjsparser | `script.module.pyjsparser` | 3.0.0 | 3.0.0 |
| pyQRcode | `script.module.pyqrcode` | 1.2.1+matrix.4 | 1.2.1+matrix.4 |
| pytz | `script.module.pytz` | 2023.3.0+matrix.1 | 2023.3.0+matrix.1 |
| qrcode | `script.module.qrcode` | 6.1.0+matrix.3 | 6.1.0+matrix.3 |
| requests | `script.module.requests` | 2.31.0 | 2.31.0 |
| ResolveURL | `script.module.resolveurl` | 5.1.211 | 5.1.211 |
| Plugin routing | `script.module.routing` | 0.2.3+matrix.1 | 0.2.3+matrix.1 |
| Simple Eval | `script.module.simpleeval` | 0.9.13 | Not bundled |
| simplejson | `script.module.simplejson` | 3.19.1+matrix.1 | 3.19.1+matrix.1 |
| SimplePlugin 3 | `script.module.simpleplugin3` | 3.0.6+matrix.1 | 3.0.6+matrix.1 |
| six | `script.module.six` | 1.16.0+matrix.1 | 1.16.0+matrix.1 |
| soupsieve | `script.module.soupsieve` | 2.4.1 | 2.4.1 |
| Tabulate | `script.module.tabulate` | 0.9.1.2 | 0.9.1.2 |
| tzdata | `script.module.tzdata` | 2023.3.0+matrix.1 | 2023.3.0+matrix.1 |
| tzlocal | `script.module.tzlocal` | 5.0.1 | 5.0.1 |
| Unidecode | `script.module.unidecode` | 1.3.6 | 1.3.6 |
| urllib3 | `script.module.urllib3` | 2.2.3 | 2.2.3 |
| Skin Shortcuts | `script.skinshortcuts` | 2.0.3 | 3.0.4 |
| Backup | `script.xbmcbackup` | 1.7.3 | 1.7.3 |
| Up Next | `service.upnext` | 1.1.9+matrix.1 | 1.1.9+matrix.1 |
| Version Check | `service.xbmc.versioncheck` | 0.5.30+matrix.1 | 0.5.30+matrix.1 |
| Xonfluence | `skin.xonfluence` | Not bundled | 6.0.7 |
| Xonfluence (SKINBASE) | `skin.xonfluence.skinbase` | 5 | Not bundled |
| Gismeteo | `weather.gismeteo` | 0.6.4+matrix.1 | 0.6.4+matrix.1 |

## Maintaining this repository

Add or replace an add-on ZIP under `repo/zips/<addon-id>/<addon-id>-<version>.zip`, then run `python build_repository.py` from the repository root. Commit the package, `repo/zips/addons.xml`, and `repo/zips/addons.xml.md5` together.

After changing this README, run `python tools/render_readme_site.py` to update the website's installation guide. Keep the current build table and package inventory aligned with the released archives.

Individual add-ons retain their upstream metadata and licenses. The [repository catalog](https://kingblap.github.io/repo/zips/addons.xml) also contains packages that can be installed separately from the builds.
