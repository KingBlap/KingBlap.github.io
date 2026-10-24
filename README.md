# KingBlap Kodi Repository

Install individual add-ons from the KingBlap Kodi Repository, or install a complete public or private build with **KingBlap Wizard 1.0.65**. Builds are available for **Kodi 21.3** and **Kodi 22**.

Updated October 24, 2026.

**Kodi File Manager source:** https://kingblap.github.io/

[Install the repository](#install-the-repository) · [Public builds](#install-a-public-build) · [Private builds](#install-a-private-build) · [Contents](#what-is-included) · [Recent updates](#recent-updates) · [Downloads](#downloads)

## Current builds

| Kodi version on your device | Build | Build version | Bundled add-ons | Access |
| --- | --- | --- | --- | --- |
| Kodi 21.3 | Public | 1.0.23 | 50 | No private code required |
| Kodi 22 | Public | 1.0.23 | 49 | No private code required |
| Kodi 21.3 | Private | 1.0.53 | Separate private set | 16-digit private access code |
| Kodi 22 | Private | 1.0.66 | Separate private set | 16-digit private access code |

Choose the build for the **Kodi version installed on your device**, whether Kodi runs on Windows, Android/Fire TV, Linux, or macOS. The public packages contain portable add-on files and settings. Kodi obtains device-specific native components, including IPTV Simple and InputStream components, from a compatible repository when available. Keep Kodi's official add-on repository enabled and allow Kodi to install dependencies. Individual add-ons may still depend on services or components unavailable on a particular device.

Public and private releases are separate. Public builds do not contain saved personal account profiles, credentials, API keys, playlists, or guide data from the backup. Third-party add-on code may include keys supplied by its developer. Private builds restore selected saved add-on settings and are distributed through the protected build service. Back up an existing Kodi setup before installing either type of build.

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
5. Open **Add-ons → Program add-ons → KingBlap Wizard**. The current Wizard version is **1.0.65**.

If you downloaded the repository ZIP to a computer, USB drive, or your device's Downloads folder, browse to that file from **Install from zip file** instead of using the File Manager source. The [Wizard 1.0.65 ZIP](https://kingblap.github.io/repo/zips/plugin.program.kingblapwizard/plugin.program.kingblapwizard-1.0.65.zip) can also be installed directly from the same Add-ons menu.

### Install individual add-ons

Open **Add-ons → open box/package icon → Install from repository → KingBlap Kodi Repository**. Select a category and add-on, then choose **Install**. Kodi will request dependencies needed on that device.

## Install a public build

1. Install or update **KingBlap Wizard 1.0.65** using the instructions above.
2. Open **Add-ons → Program add-ons → KingBlap Wizard → Public Builds**.
3. Select **Public KingBlap Build for Kodi 21.3 1.0.23 (download)** on Kodi 21.3, or **Public KingBlap Build for Kodi 22 1.0.23 (download)** on Kodi 22.
4. Review the installation notice and choose **Install build**.
5. Leave Kodi open while the Wizard downloads, checks, and installs the archive. Restart Kodi once installation finishes.

The Wizard downloads the public build and verifies its SHA-256 checksum. Use **Install from zip file** for the repository or Wizard ZIP; install the full build from the Wizard's **Public Builds** menu.

The public build brings portable add-on packages, Fire colors, the Massive font, and sanitized Xonfluence and weather settings. It does **not** preload an IPTV account or configure a provider's playlist. Enter your own service details in the relevant add-on after installation. Existing account profiles already on a device are separate from the downloaded public package.

**This release changes the add-on set.** The Wizard removes older add-ons omitted from the October 24 public package, together with their matching saved settings. These include Absolution, C.O.S.M.O.S, Forge, The Gears, Genocide, Homelander, Loop TV/Guide, The Chains, Zoro, Xstream Pro, OptiKlean, and Jet Guide. Back up any settings you want to keep before installing. The inventory below is the definitive list of bundled packages.

## Install a private build

The private build access code is separate from any IPTV username or password. Keep the code and private archives with their intended recipients.

1. Install or update **KingBlap Wizard 1.0.65** using the repository instructions above.
2. Open the Wizard's information page from **Add-ons → open box/package icon → My add-ons → Program add-ons → KingBlap Wizard**, then choose **Configure**.
3. Under **Private build access**, enter the **16-digit private build access code**. Leave **Build service URL** at its default unless you received a replacement address.
4. Open **Add-ons → Program add-ons → KingBlap Wizard → Private Builds**.
5. Select **Private KingBlap Build for Kodi 21.3 (1.0.53)** on Kodi 21.3, or **Private KingBlap Build for Kodi 22 1.0.66** on Kodi 22.
6. Review the notice about restoring saved add-on settings, choose **Install build**, and leave Kodi open until installation finishes. Restart Kodi once.

The private releases are served through the protected Cloudflare build service. They may contain saved account settings and credentials. A private build can replace matching saved profiles on the device.

## What is included

| Feature | Public Kodi 21.3 | Public Kodi 22 | Private builds |
| --- | --- | --- | --- |
| Skin | Xonfluence SKINBASE 5 | Xonfluence 6.0.7 | Version matched to Kodi |
| Appearance | Fire colors and Massive font | Fire colors and Massive font | Fire colors and Massive font |
| Saved personal accounts and API keys from backup | Excluded | Excluded | Selected saved profiles included |
| IPTV playlist and guide | Excluded | Excluded | Separate private GIPTV configuration |
| Device-specific native add-ons | Installed by Kodi | Installed by Kodi | Installed by Kodi |
| Screensaver | Not configured by this build | Not configured by this build | Kodi's built-in Dim screensaver |

The public releases are assembled from the October 24 Kodi backup after removing saved profiles, local paths, caches, databases, private data, and Windows-native binaries. PVR Setup, Aliunde K19, GratisRed, ScrubsV2, ManeFlix, and Jet Guide are omitted because their source packages contain preset URLs, embedded provider keys, malformed metadata, or a Windows-only fallback. Kodi chooses compatible native packages for each operating system. Add-ons that depend on remote services still require a working service and network connection.

The public archive includes a selected set of video, guide, weather, skin, and supporting add-ons. The exact package list for each Kodi version is in [Build package inventory](#build-package-inventory) below. Kodi 21.3 and Kodi 22 use different Xonfluence packages so that each build can load its matching skin.

## Recent updates

| Release | Change |
| --- | --- |
| **Wizard 1.0.65 / Public Builds 1.0.23** | Updates the portable public add-on set for both Kodi versions, including Otaku 5.3.6 and newer Mad Titan, WatchNixtoons2, and ResolveURL packages. Removes add-ons absent from the selected October 24 set and keeps personal backup data and Windows-native binaries out. |
| **Private Builds 1.0.53 and 1.0.66** | Current separate private releases use Kodi's built-in Dim screensaver. Private build archives and access remain separate from the public packages. |

Updating the Wizard alone does not apply a newer full build. Reopen **Public Builds** or **Private Builds** and install the build matching your Kodi version.

Legacy public download parts for version 1.0.19 and Kodi 22 version 1.0.21 have been retired from the site. Kodi 21.3 and Kodi 22 version 1.0.22 parts remain available for existing Wizard installs. If your Wizard requests a retired file, update it to 1.0.65 and choose public build 1.0.23.

## Help with installation

- **A new build does not appear:** update KingBlap Wizard to 1.0.65, reopen the build list, and check Kodi's version under **Settings → System information**.
- **Kodi version mismatch:** use the Kodi 21.3 build on Kodi 21.3 or the Kodi 22 build on Kodi 22.
- **A dependency cannot install:** enable Kodi's official add-on repository, check the device's connection and free storage, and retry the compatible dependency.
- **Installation stops or Kodi closes:** reopen Kodi and the Wizard. If the install did not finish, retry after checking free space; the Wizard needs room for the download, staged add-ons, and recovery data.
- **A public IPTV account is missing:** configure your own provider details in its add-on; the public package has no saved account or playlist.

## Downloads

- [Repository installer 1.0.0](https://kingblap.github.io/repository.kingblap-1.0.0.zip)
- [KingBlap Wizard 1.0.65](https://kingblap.github.io/repo/zips/plugin.program.kingblapwizard/plugin.program.kingblapwizard-1.0.65.zip)
- [Current public and private build list](https://kingblap.github.io/builds.txt)
- [Repository add-on catalog](https://kingblap.github.io/repo/zips/addons.xml)
- [Repository website and installation guide](https://kingblap.github.io/)

Public builds download through **Wizard → Public Builds**. Private builds download through **Wizard → Private Builds** after entering the private access code.

## Build package inventory

The following versions describe the public archives. A blank entry means that package is not bundled for that Kodi version. Private builds are separate and may contain different packages or versions. Kodi obtains native components for the operating system from an enabled compatible repository.

| Add-on | Package ID | Kodi 21.3 | Kodi 22 |
| --- | --- | --- | --- |
| Otaku - Global Context Menu Items | `context.otaku` | 1.0.35 | 1.0.35 |
| Generic Album Scraper | `metadata.generic.albums` | 1.0.20 | 1.0.20 |
| Generic Artist Scraper | `metadata.generic.artists` | 1.0.20 | 1.0.20 |
| TMDb TV Shows | `metadata.tvshows.themoviedb.org.python` | 2.0.9 | 2.0.9 |
| GIPTV | `plugin.video.giptv` | 3.1.0 | 3.1.0 |
| Mad Titan Sports V2.0 | `plugin.video.madtitansports` | 2.0.46 | 2.0.46 |
| Otaku | `plugin.video.otaku` | 5.3.6 | 5.3.6 |
| SportHD | `plugin.video.sporthdme` | 0.1.91 | 0.1.91 |
| Toonami Aftermath TV | `plugin.video.tatv2` | 1.0.3 | 1.0.3 |
| WatchNixtoons2 | `plugin.video.watchnixtoons2` | 0.14.24 | 0.14.24 |
| Otaku's Repository | `repository.otaku` | 1.0 | 1.0 |
| EZ Maintenance+ | `script.ezmaintenanceplus` | 2026.04.05.0 | 2026.04.05.0 |
| Favourites script | `script.favourites` | 8.1.2 | 8.1.2 |
| Image Resource Select Addon | `script.image.resource.select` | 3.0.2 | 3.0.2 |
| zoneinfo | `script.module.backports.zoneinfo` | 0.2.1 | 0.2.1 |
| beautifulsoup4 | `script.module.beautifulsoup4` | 4.12.2 | 4.12.2 |
| certifi | `script.module.certifi` | 2023.5.7 | 2023.5.7 |
| chardet | `script.module.chardet` | 5.1.0 | 5.1.0 |
| python-dateutil | `script.module.dateutil` | 2.8.2 | 2.8.2 |
| defusedxml | `script.module.defusedxml` | 0.6.0+matrix.1 | 0.6.0+matrix.1 |
| Dropbox API | `script.module.dropbox` | 10.3.1+matrix.1 | 10.3.1+matrix.1 |
| future | `script.module.future` | 1.0.0+matrix.1 | 1.0.0+matrix.1 |
| idna | `script.module.idna` | 3.10.0 | 3.10.0 |
| InputStream Helper | `script.module.inputstreamhelper` | 0.8.6 | 0.8.6 |
| JetExtractors | `script.module.jetextractors` | 3.3.29 | 3.3.29 |
| Kodi Six | `script.module.kodi-six` | 0.1.3.1 | 0.1.3.1 |
| MicroJen Scraper Module | `script.module.microjenscrapers` | 1.4 | 1.4 |
| PyAMF | `script.module.pyamf` | 0.8.10+matrix.4 | 0.8.10+matrix.4 |
| pyjsparser | `script.module.pyjsparser` | 3.0.0 | 3.0.0 |
| pyQRcode | `script.module.pyqrcode` | 1.2.1+matrix.4 | 1.2.1+matrix.4 |
| pytz | `script.module.pytz` | 2023.3.0+matrix.1 | 2023.3.0+matrix.1 |
| requests | `script.module.requests` | 2.31.0 | 2.31.0 |
| ResolveURL | `script.module.resolveurl` | 5.1.212 | 5.1.212 |
| Plugin routing | `script.module.routing` | 0.2.3+matrix.1 | 0.2.3+matrix.1 |
| Simple Eval | `script.module.simpleeval` | 0.9.13 | — |
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
| Xonfluence | `skin.xonfluence` | — | 6.0.7 |
| Xonfluence (SKINBASE) | `skin.xonfluence.skinbase` | 5 | — |
| Gismeteo | `weather.gismeteo` | 0.6.4+matrix.1 | 0.6.4+matrix.1 |

## Maintaining this repository

Add or replace an add-on ZIP under repo/zips/<addon-id>/<addon-id>-<version>.zip, then run python build_repository.py from the repository root. Commit the package, repo/zips/addons.xml, and repo/zips/addons.xml.md5 together.

After changing this README, run python tools/render_readme_site.py to update the website. Keep the build list and package inventory aligned with the released archives.

Individual add-ons retain their upstream metadata and licenses. The [repository catalog](https://kingblap.github.io/repo/zips/addons.xml) also contains packages that can be installed separately from the builds.
