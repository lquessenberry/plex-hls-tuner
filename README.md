# plex-hls-tuner

**Live TV Tuner Spoofer for Plex**

Turn any HLS stream into a real Plex Live TV / DVR channel with one click.

This project combines a Chrome extension with an enhanced HDHomeRun emulator so Plex thinks you have a physical tuner. Watch live streams and record them with Plex DVR just like over-the-air TV.

Built on top of the excellent [plex-dvr-hls](https://github.com/duncanleo/plex-dvr-hls) project.

---

## Features (Planned / In Progress)

- **Chrome Extension** – Detects HLS streams on any webpage and lets you add them as Live TV channels instantly
- **HDHomeRun Spoofer** – Companion server that pretends to be a SiliconDust HDHomeRun tuner
- **Plex Live TV + DVR** – Full recording support
- **Cookie / Header support** – Works with authenticated streams
- **Quality picker** – Choose the best available variant
- **Download to disk** – Video DownloadHelper-style remux to clean MP4/MKV (secondary feature)
- **Dynamic channels** – Add/remove channels without restarting the server
- **Docker-first** – Easy deployment

---

## Project Status

**Phase**: Planning complete → Starting foundation  
See [PLAN.md](PLAN.md) for the full roadmap.

---

## Quick Start (Coming Soon)

```bash
# Will be something like:
git clone https://github.com/lquessenberry/plex-hls-tuner.git
cd plex-hls-tuner
docker compose up -d
# Load the Chrome extension
# Point Plex Live TV & DVR at http://localhost:5004
```

---

## How It Works

1. You visit a page with an HLS stream.
2. The Chrome extension detects the `.m3u8` playlist(s).
3. You click **"Add as Live TV Channel"**.
4. The companion server (HDHomeRun emulator) immediately exposes that stream as a channel.
5. Plex discovers the virtual tuner and the new channel appears under Live TV.
6. You can watch it live or set recordings with Plex DVR.

---

## Repository Structure

```
├── companion/          # Enhanced plex-dvr-hls (Go)
├── extension/          # Chrome Manifest V3 extension
├── docs/               # Documentation
├── PLAN.md             # Detailed project plan & roadmap
└── docker-compose.yml
```

---

## Credits

- Base HDHomeRun emulator: [duncanleo/plex-dvr-hls](https://github.com/duncanleo/plex-dvr-hls)
- Inspiration: Video DownloadHelper, Stream Detector, Threadfin/xTeVe

---

## License

MIT (same as upstream plex-dvr-hls)

---

**Created by [lquessenberry](https://github.com/lquessenberry)** – July 2026
