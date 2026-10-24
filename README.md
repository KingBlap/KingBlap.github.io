# KingBlap Kodi Repository

Install individual add-ons from the KingBlap Kodi Repository, or install a complete public or private build with **KingBlap Wizard 1.0.69**. Builds are available for **Kodi 21.3** and **Kodi 22**.

Updated October 24, 2026.

**Kodi File Manager source:** https://kingblap.github.io/

[Install the repository](#install-the-repository) · [Public builds](#install-a-public-build) · [Private builds](#install-a-private-build) · [Contents](#what-is-included) · [Recent updates](#recent-updates) · [Downloads](#downloads)

## Current builds

| Kodi version on your device | Build | Build version | Bundled add-ons | Access |
| --- | --- | --- | --- | --- |
| Kodi 21.3 | Public | 1.0.29 | 59 | No private code required |
| Kodi 22 | Public | 1.0.29 | 59 | No private code required |
| Kodi 21.3 | Private | 1.0.53 | Separate private set | 16-digit private access code |
| Kodi 22 | Private | 1.0.66 | Separate private set | 16-digit private access code |

Choose the build for the **Kodi version installed on your device**, whether Kodi runs on Windows, Android/Fire TV, Linux, or macOS. The public packages contain portable add-on files and settings. Kodi obtains device-specific native components, including IPTV Simple and InputStream components, from a compatible repository when available. Keep Kodi's official add-on repository enabled and allow Kodi to install dependencies. Individual add-ons may still depend on services or components unavailable on a particular device.

Public and private releases are separate. Both public builds include the PC Kodi IPTV Simple playlist and guide profile. Its URLs contain credentials, and anyone who downloads the public ZIP can inspect or use them. Other saved personal profiles and API keys are omitted. Private builds restore selected saved add-on settings and are distributed through the protected build service. Back up an existing Kodi setup before installing either type of build.

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
5. Open **Add-ons → Program add-ons → KingBlap Wizard**. The current Wizard version is **1.0.69**.

If you downloaded the repository ZIP to a computer, USB drive, or your device's Downloads folder, browse to that file from **Install from zip file** instead of using the File Manager source. The [Wizard 1.0.69 ZIP](https://kingblap.github.io/repo/zips/plugin.program.kingblapwizard/plugin.program.kingblapwizard-1.0.69.zip) can also be installed directly from the same Add-ons menu.

### Install individual add-ons

Open **Add-ons → open box/package icon → Install from repository → KingBlap Kodi Repository**. Select a category and add-on, then choose **Install**. Kodi will request dependencies needed on that device.

## Install a public build

1. Install or update **KingBlap Wizard 1.0.69** using the instructions above.
2. Open **Add-ons → Program add-ons → KingBlap Wizard → Public Builds**.
3. Select **Public KingBlap Build for Kodi 21.3 1.0.29 (download)** on Kodi 21.3, or **Public KingBlap Build for Kodi 22 1.0.29 (download)** on Kodi 22.
4. Review the installation notice and choose **Install build**.
5. Leave Kodi open while the Wizard downloads, checks, and installs the archive. Restart Kodi once installation finishes.

The Wizard downloads the public build and verifies its SHA-256 checksum. Use **Install from zip file** for the repository or Wizard ZIP; install the full build from the Wizard's **Public Builds** menu.

The public build brings 59 portable add-on packages, Fire colors, the Massive font, and Xonfluence and weather settings. It also loads the PC Kodi IPTV Simple profile and its remote playlist and EPG URLs. Those URLs contain credentials and are publicly accessible to anyone who downloads the ZIP. Kodi installs the device-compatible PVR IPTV Simple client through its add-on repository; the public archive does not bundle native platform binaries. Each archive is for its matching Kodi major version: Kodi 21.3 or Kodi 22.

**This release changes the add-on set.** The Wizard removes older add-ons omitted from the October 24 public package, together with their matching saved settings. These include Absolution, C.O.S.M.O.S, Forge, The Gears, Genocide, Homelander, Loop TV/Guide, The Chains, Zoro, Xstream Pro, OptiKlean, and Jet Guide. Back up any settings you want to keep before installing. The inventory below is the definitive list of bundled packages.

## Install a private build

The private build access code is separate from any IPTV username or password. Keep the code and private archives with their intended recipients.

1. Install or update **KingBlap Wizard 1.0.69** using the repository instructions above.
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
| Saved personal accounts and API keys from backup | Excluded except PVR URLs | Excluded except PVR URLs | Selected saved profiles included |
| IPTV playlist and guide | PC Kodi PVR URLs (public credentials) | PC Kodi PVR URLs (public credentials) | Separate private GIPTV configuration |
| Device-specific native add-ons | Installed by Kodi | Installed by Kodi | Installed by Kodi |
| Screensaver | Not configured by this build | Not configured by this build | Kodi's built-in Dim screensaver |

The public releases are built from the October 24 snapshot with portable add-on resources and no machine-specific paths, caches, databases, or Windows-native binaries. They include only the PC Kodi IPTV Simple instance settings in addition to the sanitized skin and weather preferences; the playlist and EPG URLs contain credentials and are publicly accessible. Kodi obtains the compatible PVR IPTV Simple add-on and other native components for each operating system. Individual third-party add-ons may still depend on services or components unavailable on a particular device.

The public archive includes a selected set of video, guide, weather, skin, and supporting add-ons. The exact package list for each Kodi version is in [Build package inventory](#build-package-inventory) below. Kodi 21.3 and Kodi 22 use different Xonfluence packages so that each build can load its matching skin.

## Recent updates

| Release | Change |
| --- | --- |
| **Wizard 1.0.66 / Public Builds 1.0.23** | Previous release with shorter persistent install staging paths on Android and recovery for older transactions. |
| **Wizard 1.0.69 / Public Builds 1.0.29** | Validates and applies the skin package matched to each Kodi major version, repairs malformed XML in the staged Mad Titan, Otaku, and Kodi 21 skin files, checks the authorized IPTV Simple profile, and verifies each archive checksum. Kodi obtains the compatible PVR client through its own repository. The public PVR URLs contain credentials and are accessible to anyone who downloads the ZIP. |
| **Public Builds 1.0.23** | Previous portable add-on set for both Kodi versions. |
| **Private Builds 1.0.53 and 1.0.66** | Current separate private releases use Kodi's built-in Dim screensaver. Private build archives and access remain separate from the public packages. |

Updating the Wizard alone does not apply a newer full build. Reopen **Public Builds** or **Private Builds** and install the build matching your Kodi version.

Older public download parts remain available for existing Wizard installs. Update the Wizard to 1.0.69 and choose public build 1.0.29 to use the current archives.

## Help with installation

- **A new build does not appear:** update KingBlap Wizard to 1.0.69, reopen the build list, and check Kodi's version under **Settings → System information**.
- **Kodi version mismatch:** use the Kodi 21.3 build on Kodi 21.3 or the Kodi 22 build on Kodi 22.
- **A dependency cannot install:** enable Kodi's official add-on repository, check the device's connection and free storage, and retry the compatible dependency.
- **Installation stops or Kodi closes:** update to Wizard 1.0.69, reopen Kodi and the Wizard. If the install did not finish, retry after checking free space; the Wizard needs room for the download, staged add-ons, and recovery data.
- **The public IPTV guide or playlist is unavailable:** the public build uses the PC Kodi PVR URLs. They contain credentials and are shared with every ZIP download; contact the owner if they need to be changed.

## Downloads

- [Repository installer 1.0.0](https://kingblap.github.io/repository.kingblap-1.0.0.zip)
- [KingBlap Wizard 1.0.69](https://kingblap.github.io/repo/zips/plugin.program.kingblapwizard/plugin.program.kingblapwizard-1.0.69.zip)
- [Current public and private build list](https://kingblap.github.io/builds.txt)
- [Repository add-on catalog](https://kingblap.github.io/repo/zips/addons.xml)
- [Repository website and installation guide](https://kingblap.github.io/)

Public builds download through **Wizard → Public Builds**. Private builds download through **Wizard → Private Builds** after entering the private access code.

## Build package inventory

The table lists the packages actually bundled in each archive. The Kodi-compatible PVR IPTV Simple client is installed by the Wizard through the device's enabled Kodi add-on repository; it is not bundled because its native component is platform-specific. The archives include the authorized PC playlist and guide profile, whose URLs contain credentials and are visible to anyone who downloads the public ZIP.

| Add-on ID | Kodi 21.3 | Kodi 22 |
| --- | ---: | ---: |
| `context.otaku` | 1.0.35 | 1.0.35 |
| `metadata.generic.albums` | 1.0.20 | 1.0.20 |
| `metadata.generic.artists` | 1.0.20 | 1.0.20 |
| `metadata.tvshows.themoviedb.org.python` | 2.0.9 | 2.0.9 |
| `plugin.program.pvr.setup` | 1.4.1 | 1.4.1 |
| `plugin.video.jet_guide` | 0.0.22 | 0.0.22 |
| `plugin.video.madtitansports` | 2.0.46.1 | 2.0.46.1 |
| `plugin.video.maneflix` | 1.0.6.1 | 1.0.6.1 |
| `plugin.video.otaku` | 5.3.4.1 | 5.3.4.1 |
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
| `script.xbmcbackup` | 1.7.3 | 1.7.3 |
| `service.xbmc.versioncheck` | 0.5.30+matrix.1 | 0.5.30+matrix.1 |
| `skin.xonfluence` | 5.1.1 | 6.0.7 |
| `weather.gismeteo` | 0.6.4+matrix.1 | 0.6.4+matrix.1 |

## Maintaining this repository

Add or replace an add-on ZIP under repo/zips/<addon-id>/<addon-id>-<version>.zip, then run python build_repository.py from the repository root. Commit the package, repo/zips/addons.xml, and repo/zips/addons.xml.md5 together.

After changing this README, run python tools/render_readme_site.py to update the website. Keep the build list and package inventory aligned with the released archives.

Individual add-ons retain their upstream metadata and licenses. The [repository catalog](https://kingblap.github.io/repo/zips/addons.xml) also contains packages that can be installed separately from the builds.
