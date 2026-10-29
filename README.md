# KingBlap Kodi Repository

Install individual add-ons from the KingBlap Kodi Repository, or install a complete public or private build with **KingBlap Wizard 1.0.79**. Builds are available for **Kodi 21.3** and **Kodi 22**.

Updated October 29, 2026.

**Kodi File Manager source:** https://kingblap.github.io/

[Install the repository](#install-the-repository) · [Public builds](#install-a-public-build) · [Private builds](#install-a-private-build) · [Contents](#what-is-included) · [Recent updates](#recent-updates) · [Downloads](#downloads)

## Current builds

| Kodi version on your device | Build | Build version | Bundled add-ons | Access |
| --- | --- | --- | --- | --- |
| Kodi 21.3 | Public | 1.0.36 | 64 | No private code required |
| Kodi 22 | Public | 1.0.36 | 64 | No private code required |
| Kodi 21.3 | Private | 1.0.55 | 81 | 16-digit private access code |
| Kodi 22 | Private | 1.0.68 | 78 | 16-digit private access code |

Choose the build for the **Kodi version installed on your device**, whether Kodi runs on Windows, Android/Fire TV, Linux, or macOS. The archives contain portable add-on files and settings; Kodi obtains device-specific native components, including IPTV Simple and InputStream components, from a compatible repository when available. Keep Kodi's official add-on repository enabled and allow Kodi to install dependencies. A package check cannot guarantee that every third-party service works on every device.

Public and private releases are separate. Public builds include the PC Kodi IPTV Simple playlist and guide profile plus bundled add-on API defaults from the October 24 backup. **Those URLs contain credentials, and the URLs and API defaults can be read by anyone who downloads a public ZIP.** Saved personal add-on profiles are omitted. Private builds include GIPTV and selected saved add-on settings and are distributed through the protected build service. Back up an existing Kodi setup before installing either type of build.

## Install the repository

### Add the source in Kodi File Manager

1. In Kodi, open **Settings → System → Add-ons** and enable **Unknown sources**. Accept Kodi's confirmation.
2. Return to **Settings → File Manager → Add source**.
3. Select **<None>**, enter https://kingblap.github.io/, and select **OK**.
4. Name the source **KingBlap Repo** and select **OK**.

Menu positions can vary by skin. Kodi documents its [File Manager](https://kodi.wiki/view/File_manager) and [Add-on manager](https://kodi.wiki/view/Add-on_manager).

### Install the repository and Wizard from Add-ons

1. Open **Add-ons → open box/package icon → Install from zip file → KingBlap Repo**.
2. Select **repository.kingblap-1.0.0.zip** and wait for the repository installed notification.
3. Open **Install from repository → KingBlap Kodi Repository → Program add-ons → KingBlap Wizard**.
4. Select **Install**, accept dependency prompts, and wait for the Wizard installed notification.
5. Open **Add-ons → Program add-ons → KingBlap Wizard**. The current Wizard version is **1.0.79**.

If you downloaded the repository ZIP to a computer, USB drive, or your device's Downloads folder, browse to that file from **Install from zip file** instead of using the File Manager source. The [Wizard 1.0.79 ZIP](https://kingblap.github.io/repo/zips/plugin.program.kingblapwizard/plugin.program.kingblapwizard-1.0.79.zip) can also be installed directly from the same Add-ons menu.

### Install individual add-ons

Open **Add-ons → open box/package icon → Install from repository → KingBlap Kodi Repository**. Select a category and add-on, then choose **Install**. Kodi will request dependencies needed on that device.

## Install a public build

1. Install or update **KingBlap Wizard 1.0.79** using the instructions above.
2. Open **Add-ons → Program add-ons → KingBlap Wizard → Public Builds**.
3. Select **Public KingBlap Build for Kodi 21.3 1.0.36 (download)** on Kodi 21.3, or **Public KingBlap Build for Kodi 22 1.0.36 (download)** on Kodi 22.
4. Review the installation notice and choose **Install build**.
5. Leave Kodi open while the Wizard downloads, checks, and installs the archive. The Wizard verifies the saved IPTV Simple playlist and guide sources, then asks Kodi to reload them. On Android/Fire TV, Kodi may close; reopen it after it exits.

The Wizard downloads the public build and verifies its SHA-256 checksum. Use **Install from zip file** for the repository or Wizard ZIP; install the full build from the Wizard's **Public Builds** menu.

The public build brings 64 portable add-on packages, Fire colors, the Massive font, and Xonfluence and weather settings. It also loads the PC Kodi IPTV Simple profile and its remote playlist and EPG URLs. Those URLs contain credentials and are publicly accessible to anyone who downloads the ZIP. Kodi installs the device-compatible PVR IPTV Simple client through its add-on repository; the public archive does not bundle native platform binaries. Each archive is for its matching Kodi major version: Kodi 21.3 or Kodi 22.

The October 24 public package includes Aliunde K19, Gratis Red, Scrubs V2, and their artwork support. The Wizard removes older add-ons omitted from that package, together with their matching saved settings. These include Absolution, C.O.S.M.O.S, Forge, The Gears, Genocide, Homelander, Loop TV/Guide, The Chains, Zoro, Xstream Pro, and OptiKlean. Back up any settings you want to keep before installing. The inventory below is the definitive list of bundled packages.

## Install a private build

The private build access code is separate from any IPTV username or password. Keep the code and private archives with their intended recipients.

1. Install or update **KingBlap Wizard 1.0.79** using the repository instructions above.
2. Open the Wizard's information page from **Add-ons → open box/package icon → My add-ons → Program add-ons → KingBlap Wizard**, then choose **Configure**.
3. Under **Private build access**, enter the **16-digit private build access code**. Leave **Build service URL** at its default unless you received a replacement address.
4. Open **Add-ons → Program add-ons → KingBlap Wizard → Private Builds**.
5. Select **Private KingBlap Build for Kodi 21.3 (1.0.55)** on Kodi 21.3, or **Private KingBlap Build for Kodi 22 (1.0.68)** on Kodi 22.
6. Review the notice about restoring saved add-on settings, choose **Install build**, and leave Kodi open until installation finishes. If the Wizard asks to reload IPTV Simple, accept the prompt. On Android/Fire TV, Kodi may close; reopen it after it exits.

The private releases are served through the protected Cloudflare build service. They contain selected saved profiles and may contain account settings and credentials. A private build can replace matching saved profiles on the device. Do not share the access code or private ZIPs.

The Cloudflare build listing points to private versions **1.0.55** and **1.0.68**, but an existing Kodi installation stays on its installed build until you select and install the matching version in the Wizard. Install after stopping playback, then reopen Kodi to let IPTV Simple load the playlist and guide.

Wizard 1.0.79 restores Xonfluence menu shortcuts with Kodi's skin-specific commands and verifies they were saved after restart. It restores and verifies the IPTV Simple profile for a private archive that includes one, enables the PVR client, and keeps a valid packaged GIPTV sync checkpoint. On Android/Fire TV, reopen Kodi after the Wizard closes it.

## What is included

| Feature | Public Kodi 21.3 | Public Kodi 22 | Private Kodi 21.3 | Private Kodi 22 |
| --- | --- | --- | --- | --- |
| Packaged add-ons | 64 | 64 | 81 | 78 |
| Skin | Xonfluence 5.1.1 | Xonfluence 6.0.7 | Xonfluence SKINBASE 5.1 | Xonfluence 6.0.8 |
| Appearance and weather | Fire colors, Massive font, Gismeteo | Fire colors, Massive font, Gismeteo | Fire colors, Massive font, Gismeteo | Fire colors, Massive font, Gismeteo |
| IPTV playlist and guide | PC Kodi IPTV Simple profile; credentialed URLs are public | PC Kodi IPTV Simple profile; credentialed URLs are public | GIPTV 3.1.3 and IPTV Simple; USA/24/7 groups with a filtered 24-hour guide | GIPTV 3.1.3 and IPTV Simple; USA/24/7 groups with a filtered 24-hour guide |
| Menus and views | PC Movies & Shows, Anime, TV, and Sports shortcuts with bundled icons | PC Movies & Shows, Anime, TV, and Sports shortcuts with bundled icons | Xonfluence video views plus Preview List for TV channels | Xonfluence video views plus Preview List for TV channels |
| Saved add-on profiles | Otaku reset for first-run setup; other personal profiles omitted | Otaku reset for first-run setup; other personal profiles omitted | Selected profiles restored; Otaku reset for first-run setup | Selected profiles restored; Otaku reset for first-run setup |
| Screensaver | Not configured by this build | Not configured by this build | Kodi's built-in Dim | Kodi's built-in Dim |
| Automatic add-on updates | Enabled | Enabled | Enabled | Enabled |
| Device-specific native add-ons | Installed by Kodi | Installed by Kodi | Installed by Kodi | Installed by Kodi |

The public releases are built from the October 24 snapshot without machine-specific paths, caches, or Windows-native binaries. They include the PC Kodi IPTV Simple instance settings, sanitized skin and weather preferences, and Otaku's context database; the playlist and EPG URLs contain credentials and are publicly accessible. Bundled add-on API defaults are also readable in the ZIP. Kodi obtains the compatible PVR IPTV Simple add-on and other native components for each operating system. Individual third-party add-ons may still depend on services or components unavailable on a particular device.

The public video add-ons are Aliunde K19, Gratis Red, Jet Guide, Mad Titan Sports, Maneflix, Otaku, Scrubs V2, SportHD, TATV2, and WatchNixtoons2. The archives also include the Xonfluence skin, Gismeteo weather, artwork, repositories, and supporting libraries. The October 24 context.otaku database is included for Otaku 5.3.4; the Wizard clears Otaku's existing saved profile so its first-run prompts appear after installation. Kodi may later update Otaku from an enabled repository because automatic add-on updates remain enabled. The exact package list for each Kodi version is in [Build package inventory](#build-package-inventory) below.

The private video add-ons are Absolution, C.O.S.M.O.S, Dailymotion, Forge, The Gears, Genocide, GIPTV, Homelander, Jet Guide, Loop Guide, Loop TV, Mad Titan Sports, Otaku, TATV2, The Chains, WatchNixtoons2, and Zoro. Kodi 21.3 also includes Prism. The archives include Xonfluence, Gismeteo, artwork, Otaku's repository, and supporting libraries. Their saved GIPTV and IPTV Simple setup limits channels and guide data to USA/24/7 groups, and the TV channel view is Preview List. They include selected saved add-on profiles, so installing a private build can replace existing settings. The full private package list is below.

## Recent updates

| Release | Change |
| --- | --- |
| **Private Builds 1.0.55 and 1.0.68** | Updated Jet Guide, Mad Titan Sports, WatchNixtoons2, JetExtractors, ResolveURL, CocoScrapers, GearsScrapers, and Up Next from compatible repository packages. Kodi 22 also updates Skin Shortcuts. Otaku stays at 5.3.4 because that is the current version in its configured repository. Saved profiles, the GIPTV reset fix, and the platform-specific IPTV Simple install flow are unchanged. Both archives passed ZIP, dependency, and Wizard 1.0.79 checks; playback and long-running TV stability have not yet been tested with these releases. |
| **Wizard 1.0.79 / Private Builds 1.0.54 and 1.0.67** | GIPTV keeps its last working playlist and guide when a refresh fails, and a guide-only update no longer disables and restarts IPTV Simple. Portable PVR paths avoid an unnecessary settings rewrite on first startup. The Wizard validates and preserves a complete packaged guide checkpoint; an empty guide still fetches its first listings after startup. Both archives passed ZIP and GIPTV refresh regression checks. The Kodi 22 TV was inspected before release; the new builds have not yet been installed on the TV. |
| **Wizard 1.0.78 / Public Builds 1.0.36** | Rebuilt both public archives from the October 24 PC backup. Restored Otaku 5.3.4 and its required context database, reset Otaku's saved profile for first-run setup, restored Scrubs V2 artwork, and corrected Maneflix and EZ Maintenance+ fanart paths. The Wizard verifies IPTV Simple after installation and shows a clear message if enabling it fails. BlueStacks Kodi 22 installed the build with all 64 packaged add-ons and IPTV Simple enabled; playback and Kodi 21.3 were not runtime-tested. |
| **Private Builds 1.0.53 and 1.0.66** | Replaced Aerial with Kodi's built-in Dim screensaver to address black screens after waking. Kept the filtered USA/24/7 GIPTV playlist and guide, Preview List TV view, and low-memory playback and guide settings. Otaku 5.3.4 was reinstalled from Otaku's repository with saved Otaku settings reset; Hooty's repository, Xstream Pro, and OptiKlean were removed. |
| **Public Builds 1.0.34–1.0.35** | Restored the configured Xonfluence video add-on icons, improved the platform-compatible IPTV Simple install flow, and let Otaku start when optional Simkl metadata was missing. Build 1.0.36 supplies Otaku's required database. |

Updating the Wizard alone does not apply a newer full build. Reopen **Public Builds** or **Private Builds** and install the build matching your Kodi version.

Older public download parts remain available for existing Wizard installs. Update the Wizard to 1.0.79 and choose public build 1.0.36 to use the current archives.

## Help with installation

- **A new build does not appear:** update KingBlap Wizard to 1.0.79, reopen the build list, and check Kodi's version under **Settings → System information**.
- **Kodi version mismatch:** use the Kodi 21.3 build on Kodi 21.3 or the Kodi 22 build on Kodi 22.
- **A dependency cannot install:** enable Kodi's official add-on repository, check the device's connection and free storage, and retry the compatible dependency.
- **Installation stops or Kodi closes:** update to Wizard 1.0.79, reopen Kodi and the Wizard. If the install did not finish, retry after checking free space; the Wizard needs room for the download, staged add-ons, and recovery data.
- **IPTV Simple is disabled or the guide is empty after a build apply:** update to Wizard 1.0.79, reapply the matching build, and accept the IPTV reload prompt. On Android/Fire TV, reopen Kodi after it closes. The private build's first guide fetch starts after Kodi settles; a failed fetch keeps the last working exports and retries later.
- **GIPTV still resets or Kodi exits after installing a private build:** check that the installed build is 1.0.55 for Kodi 21.3 or 1.0.68 for Kodi 22. If the problem continues on that version, collect a fresh Kodi log and Android exit reason. The new archives passed package and Wizard checks, but have not yet completed a long-running TV test.
- **The public IPTV guide or playlist is unavailable:** the public build uses the PC Kodi PVR URLs. They contain credentials and are shared with every ZIP download; contact the owner if they need to be changed.
- **Otaku changes version after installation:** the public ZIP installs Otaku 5.3.4, but Kodi can update it later. To keep 5.3.4, open **Add-ons → My add-ons → Video add-ons → Otaku → Information** and turn off **Auto-update** for Otaku.

## Downloads

- [Repository installer 1.0.0](https://kingblap.github.io/repository.kingblap-1.0.0.zip)
- [KingBlap Wizard 1.0.79](https://kingblap.github.io/repo/zips/plugin.program.kingblapwizard/plugin.program.kingblapwizard-1.0.79.zip)
- [Current public and private build list](https://kingblap.github.io/builds.txt)
- [Repository add-on catalog](https://kingblap.github.io/repo/zips/addons.xml)
- [Repository website and installation guide](https://kingblap.github.io/)

Public builds download through **Wizard → Public Builds**. Private builds download through **Wizard → Private Builds** after entering the private access code.

## Build package inventory

The tables list the add-on packages actually bundled in the current public and private archives. The Kodi-compatible PVR IPTV Simple client is installed by the Wizard through the device's enabled Kodi add-on repository; it is not bundled because its native component is platform-specific. Public archives include the PC playlist and guide profile, whose URLs contain credentials and are visible to anyone who downloads a public ZIP. Private archives include the separate GIPTV and IPTV Simple setup.

### Public packages

| Add-on ID | Kodi 21.3 | Kodi 22 |
| --- | ---: | ---: |
| `context.otaku` | 1.0.35 | 1.0.35 |
| `metadata.generic.albums` | 1.0.20 | 1.0.20 |
| `metadata.generic.artists` | 1.0.20 | 1.0.20 |
| `metadata.tvshows.themoviedb.org.python` | 2.0.9 | 2.0.9 |
| `plugin.program.pvr.setup` | 1.4.1 | 1.4.1 |
| `plugin.video.aliundek19` | 0.3.9 | 0.3.9 |
| `plugin.video.gratisred` | 2.0.8 | 2.0.8 |
| `plugin.video.jet_guide` | 0.0.22 | 0.0.22 |
| `plugin.video.madtitansports` | 2.0.46.1 | 2.0.46.1 |
| `plugin.video.maneflix` | 1.0.6.1 | 1.0.6.1 |
| `plugin.video.otaku` | 5.3.4 | 5.3.4 |
| `plugin.video.scrubsv2` | 5.1.42 | 5.1.42 |
| `plugin.video.sporthdme` | 0.1.91 | 0.1.91 |
| `plugin.video.tatv2` | 1.0.3 | 1.0.3 |
| `plugin.video.watchnixtoons2` | 0.14.24 | 0.14.24 |
| `repository.aliunde` | 1.9.5 | 1.9.5 |
| `repository.bugatsinho` | 2.8 | 2.8 |
| `repository.diggz` | 28 | 28 |
| `repository.jewrepo` | 1.6.0 | 1.6.0 |
| `repository.Magnetic` | 1.1.0b | 1.1.0b |
| `repository.otaku` | 1.0 | 1.0 |
| `repository.peno64` | 1.5 | 1.5 |
| `repository.redwizard` | 1.2.2 | 1.2.2 |
| `repository.thecrew` | 0.3.8 | 0.3.8 |
| `resource.images.kingblapbackgrounds` | 1.0.0 | 1.0.0 |
| `resource.images.skinbackgrounds.xonfluence` | 0.0.1 | 0.0.1 |
| `script.ezmaintenanceplus` | 2026.04.05.0 | 2026.04.05.0 |
| `script.favourites` | 8.1.2 | 8.1.2 |
| `script.gratisred.artwork` | 1.0.6 | 1.0.6 |
| `script.image.resource.select` | 3.0.2 | 3.0.2 |
| `script.module.backports.zoneinfo` | 0.2.1 | 0.2.1 |
| `script.module.beautifulsoup4` | 4.12.2 | 4.12.2 |
| `script.module.certifi` | 2023.5.7 | 2023.5.7 |
| `script.module.chardet` | 5.1.0 | 5.1.0 |
| `script.module.dateutil` | 2.8.2 | 2.8.2 |
| `script.module.defusedxml` | 0.6.0+matrix.1 | 0.6.0+matrix.1 |
| `script.module.dropbox` | 10.3.1+matrix.1 | 10.3.1+matrix.1 |
| `script.module.future` | 1.0.0+matrix.1 | 1.0.0+matrix.1 |
| `script.module.idna` | 3.10.0 | 3.10.0 |
| `script.module.inputstreamhelper` | 0.8.6 | 0.8.6 |
| `script.module.jetextractors` | 3.3.29 | 3.3.29 |
| `script.module.kodi-six` | 0.1.3.1 | 0.1.3.1 |
| `script.module.microjenscrapers` | 1.4 | 1.4 |
| `script.module.pyamf` | 0.8.10+matrix.4 | 0.8.10+matrix.4 |
| `script.module.pyjsparser` | 3.0.0 | 3.0.0 |
| `script.module.pyqrcode` | 1.2.1+matrix.4 | 1.2.1+matrix.4 |
| `script.module.pytz` | 2023.3.0+matrix.1 | 2023.3.0+matrix.1 |
| `script.module.requests` | 2.31.0 | 2.31.0 |
| `script.module.resolveurl` | 5.1.212 | 5.1.212 |
| `script.module.routing` | 0.2.3+matrix.1 | 0.2.3+matrix.1 |
| `script.module.simplejson` | 3.19.1+matrix.1 | 3.19.1+matrix.1 |
| `script.module.simpleplugin3` | 3.0.6+matrix.1 | 3.0.6+matrix.1 |
| `script.module.six` | 1.16.0+matrix.1 | 1.16.0+matrix.1 |
| `script.module.soupsieve` | 2.4.1 | 2.4.1 |
| `script.module.tabulate` | 0.9.1.2 | 0.9.1.2 |
| `script.module.tzdata` | 2023.3.0+matrix.1 | 2023.3.0+matrix.1 |
| `script.module.tzlocal` | 5.0.1 | 5.0.1 |
| `script.module.unidecode` | 1.3.6 | 1.3.6 |
| `script.module.urllib3` | 2.2.3 | 2.2.3 |
| `script.scrubsv2.artwork` | 1.6 | 1.6 |
| `script.xbmcbackup` | 1.7.3 | 1.7.3 |
| `service.xbmc.versioncheck` | 0.5.30+matrix.1 | 0.5.30+matrix.1 |
| `skin.xonfluence` | 5.1.1 | 6.0.7 |
| `weather.gismeteo` | 0.6.4+matrix.1 | 0.6.4+matrix.1 |

### Private packages

Kodi 21.3 has 81 bundled packages; Kodi 22 has 78. A dash means that package is not in that build. Packages can update later from enabled repositories.

| Add-on ID | Kodi 21.3 private | Kodi 22 private |
| --- | ---: | ---: |
| `context.otaku` | 1.0.35 | 1.0.35 |
| `context.prism` | 4.0.2 | — |
| `context.seren` | 3.0.2 | 3.0.2 |
| `metadata.generic.albums` | 1.0.20 | 1.0.20 |
| `metadata.generic.artists` | 1.0.20 | 1.0.20 |
| `metadata.tvshows.themoviedb.org.python` | 2.0.9 | 2.0.9 |
| `plugin.video.absolution` | 4.4.1 | 4.4.1 |
| `plugin.video.cosmos` | 4.3.54 | 4.3.54 |
| `plugin.video.dailymotion_com` | 2.4.5 | 2.4.5 |
| `plugin.video.forge` | 0.2.13 | 0.2.13 |
| `plugin.video.gears` | 2.4.3 | 2.4.3 |
| `plugin.video.genocide` | 6.9.9 | 6.9.9 |
| `plugin.video.giptv` | 3.1.3 | 3.1.3 |
| `plugin.video.homelander` | 1.3.1 | 1.3.1 |
| `plugin.video.jet_guide` | 0.0.22 | 0.0.22 |
| `plugin.video.loopguide` | 3.8.2 | 3.8.2 |
| `plugin.video.looptv` | 26+matrix.2 | 26+matrix.2 |
| `plugin.video.madtitansports` | 2.0.47 | 2.0.47 |
| `plugin.video.otaku` | 5.3.4 | 5.3.4 |
| `plugin.video.prism` | 5.0.56 | — |
| `plugin.video.tatv2` | 1.0.3 | 1.0.3 |
| `plugin.video.thechains` | 6.0.1 | 6.0.1 |
| `plugin.video.watchnixtoons2` | 0.14.24 | 0.14.24 |
| `plugin.video.zoro` | 1.1.9 | 1.1.9 |
| `program.easyplayerswitch` | 1.1.0 | 1.1.0 |
| `repository.otaku` | 1.0 | 1.0 |
| `resource.images.recordlabels.white` | 0.0.7 | 0.0.7 |
| `resource.images.studios.white` | 0.0.34 | 0.0.34 |
| `resource.uisounds.appletv` | 0.0.2 | 0.0.2 |
| `script.absolution.artwork` | 4.1.7 | 4.1.7 |
| `script.ezmaintenanceplus` | 2026.04.05.0 | 2026.04.05.0 |
| `script.favourites` | 8.1.2 | 8.1.2 |
| `script.homelander.artwork` | 1.0.4 | 1.0.4 |
| `script.image.resource.select` | 3.0.2 | 3.0.2 |
| `script.module.absolutionscrapers` | 4.0.5 | 4.0.5 |
| `script.module.acctmgr` | 1.2.0a | 1.2.0a |
| `script.module.acctvwr` | 1.1.5 | 1.1.5 |
| `script.module.backports.zoneinfo` | 0.2.1 | 0.2.1 |
| `script.module.beautifulsoup4` | 4.12.2 | 4.12.2 |
| `script.module.certifi` | 2023.5.7 | 2023.5.7 |
| `script.module.chainscrapers` | 1.0.8 | 1.0.8 |
| `script.module.chardet` | 5.1.0 | 5.1.0 |
| `script.module.cocoscrapers` | 1.0.45 | 1.0.45 |
| `script.module.dateutil` | 2.8.2 | 2.8.2 |
| `script.module.defusedxml` | 0.6.0+matrix.1 | 0.6.0+matrix.1 |
| `script.module.dropbox` | 10.3.1+matrix.1 | 10.3.1+matrix.1 |
| `script.module.fenomscrapers` | 1.5.4 | 1.5.4 |
| `script.module.future` | 1.0.0+matrix.1 | 1.0.0+matrix.1 |
| `script.module.gearsscrapers` | 1.6.3 | 1.6.3 |
| `script.module.homelanderscrapers` | 2.0.4 | 2.0.4 |
| `script.module.idna` | 3.10.0 | 3.10.0 |
| `script.module.inputstreamhelper` | 0.8.6 | 0.8.6 |
| `script.module.jetextractors` | 3.3.30 | 3.3.30 |
| `script.module.kodi-six` | 0.1.3.1 | 0.1.3.1 |
| `script.module.microjenscrapers` | 1.4 | 1.4 |
| `script.module.myaccounts` | 1.1.3 | 1.1.3 |
| `script.module.myconnpy` | 8.0.33 | 8.0.33 |
| `script.module.pyamf` | 0.8.10+matrix.4 | 0.8.10+matrix.4 |
| `script.module.pyjsparser` | 3.0.0 | 3.0.0 |
| `script.module.pyqrcode` | 1.2.1+matrix.4 | 1.2.1+matrix.4 |
| `script.module.pytz` | 2023.3.0+matrix.1 | 2023.3.0+matrix.1 |
| `script.module.qrcode` | 6.1.0+matrix.3 | 6.1.0+matrix.3 |
| `script.module.requests` | 2.31.0 | 2.31.0 |
| `script.module.resolveurl` | 5.1.212 | 5.1.212 |
| `script.module.routing` | 0.2.3+matrix.1 | 0.2.3+matrix.1 |
| `script.module.simpleeval` | 0.9.13 | — |
| `script.module.simplejson` | 3.19.1+matrix.1 | 3.19.1+matrix.1 |
| `script.module.simpleplugin3` | 3.0.6+matrix.1 | 3.0.6+matrix.1 |
| `script.module.six` | 1.16.0+matrix.1 | 1.16.0+matrix.1 |
| `script.module.soupsieve` | 2.4.1 | 2.4.1 |
| `script.module.tabulate` | 0.9.1.2 | 0.9.1.2 |
| `script.module.tzdata` | 2023.3.0+matrix.1 | 2023.3.0+matrix.1 |
| `script.module.tzlocal` | 5.0.1 | 5.0.1 |
| `script.module.unidecode` | 1.3.6 | 1.3.6 |
| `script.module.urllib3` | 2.2.3 | 2.2.3 |
| `script.skinshortcuts` | 2.0.3 | 3.0.5 |
| `script.xbmcbackup` | 1.7.3 | 1.7.3 |
| `service.upnext` | 1.3.0 | 1.3.0 |
| `service.xbmc.versioncheck` | 0.5.30+matrix.1 | 0.5.30+matrix.1 |
| `skin.xonfluence` | — | 6.0.8 |
| `skin.xonfluence.skinbase` | 5.1 | — |
| `weather.gismeteo` | 0.6.4+matrix.1 | 0.6.4+matrix.1 |

## Maintaining this repository

Add or replace an add-on ZIP under repo/zips/<addon-id>/<addon-id>-<version>.zip, then run python build_repository.py from the repository root. Commit the package, repo/zips/addons.xml, and repo/zips/addons.xml.md5 together.

After changing this README, run python tools/render_readme_site.py to update the website. Keep the build list and package inventory aligned with the released archives.

Individual add-ons retain their upstream metadata and licenses. The [repository catalog](https://kingblap.github.io/repo/zips/addons.xml) also contains packages that can be installed separately from the builds.
