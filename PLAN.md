# Plex HLS Tuner – Project Plan

**Goal**: Build a complete "Live TV Tuner Spoofer" that tricks Plex into treating arbitrary HLS streams as real HDHomeRun tuner channels, enabling Live TV viewing + full DVR recording.

This project combines:
- A Chrome extension (HLS detection + easy "Add as Channel" workflow)
- An enhanced version of [plex-dvr-hls](https://github.com/duncanleo/plex-dvr-hls) as the companion backend
- Optional download-to-disk functionality (Video DownloadHelper style)

---

## Vision

1. Browse any website with an HLS stream (news, sports, free live TV, authenticated streams, etc.).
2. Click the extension icon → "Add as Live TV Channel".
3. The stream instantly appears as a channel inside Plex Live TV & DVR.
4. Watch live, pause, and record with Plex DVR just like a real tuner.
5. Optionally download the stream to disk as a clean MP4/MKV.

---

## Architecture

```
┌──────────────────────────────┐
│     Chrome Extension         │
│  • Detects m3u8 / HLS        │
│  • Captures cookies/headers  │
│  • Quality picker            │
│  • "Add as Channel" / Download│
└──────────────┬───────────────┘
               │ Native Messaging / localhost API
               ▼
┌──────────────────────────────┐
│  Companion Server            │
│  (Enhanced plex-dvr-hls)     │
│  • HDHomeRun API emulator    │
│  • Dynamic channel management│
│  • ffmpeg remux / encode     │
│  • Cookie/header injection   │
│  • Download queue            │
│  • Optional DLNA server      │
└──────────────┬───────────────┘
               │ Port 5004 (HDHomeRun)
               ▼
┌──────────────────────────────┐
│         Plex Media Server    │
│  Live TV & DVR               │
│  (sees real tuner channels)  │
└──────────────────────────────┘
```

---

## Phases & Milestones

### Phase 0 – Foundation (Current)
- [x] Create repository
- [x] Write this plan
- [ ] Fork / vendor plex-dvr-hls code as base
- [ ] Set up project structure
- [ ] Basic README and license

### Phase 1 – Core Companion (MVP Backend)
**Target: Working HDHomeRun spoofer with dynamic channels**

- [ ] Clean fork of plex-dvr-hls into `/companion`
- [ ] Add REST API for channel management:
  - `POST /api/channels` – add channel (name, url, headers, cookies, number)
  - `GET /api/channels` – list channels
  - `DELETE /api/channels/:id` – remove
  - `PUT /api/channels/:id` – update
- [ ] Support injecting custom headers / cookies into ffmpeg
- [ ] Persist channels to disk (JSON or SQLite)
- [ ] Keep original plex-dvr-hls features (encoder profiles, device_id, XMLTV)
- [ ] Docker + docker-compose ready
- [ ] Health check endpoint

**Success criteria**: Manually add an HLS URL via API → appears in Plex Live TV within seconds.

### Phase 2 – Chrome Extension (MVP Frontend)
**Target: One-click add from any webpage**

- [ ] Manifest V3 extension
- [ ] HLS detector (based on Stream Detector / webRequest + content scripts)
- [ ] Capture full request headers + cookies from the tab
- [ ] Popup UI:
  - List of detected streams with quality variants
  - "Add as Live TV Channel" button
  - Optional channel name override + channel number
  - Download button (Phase 3)
- [ ] Native Messaging host (or simple localhost with token)
- [ ] Settings page (companion URL, default quality, etc.)

**Success criteria**: On any HLS page → click extension → channel appears in Plex.

### Phase 3 – Download to Disk (VDH feature)
- [ ] Queue system in companion
- [ ] Multi-threaded segment download + ffmpeg remux to MP4/MKV
- [ ] Progress reporting to extension
- [ ] Save location chooser + naming templates
- [ ] Optional auto-add to a Plex movie library after download

### Phase 4 – Polish & Advanced Features
- [ ] Better EPG support (optional real XMLTV or simple scraper)
- [ ] Temporary vs permanent channels
- [ ] Channel groups / categories
- [ ] Concurrent stream limit ("tuner count")
- [ ] Hardware encoding auto-detect
- [ ] Web dashboard for companion (optional, beyond the API)
- [ ] Auto-restart / watchdogs
- [ ] Windows tray app / Electron wrapper (nice-to-have)
- [ ] DLNA/UPnP server mode (bonus)

### Phase 5 – Packaging & Distribution
- [ ] GitHub Releases with binaries (Windows, Linux, macOS)
- [ ] Chrome Web Store listing (or sideload instructions)
- [ ] Docker Hub / GHCR image
- [ ] Documentation site or detailed wiki
- [ ] Example configs for common free live streams

---

## Tech Stack

| Component          | Technology                          |
|--------------------|-------------------------------------|
| Companion backend  | Go (fork of plex-dvr-hls) + REST API |
| HLS processing     | ffmpeg (cpu / nvenc / vaapi / etc.) |
| Channel storage    | JSON file or SQLite                 |
| Chrome Extension   | Manifest V3, TypeScript preferred   |
| Communication      | Native Messaging or authenticated localhost |
| Packaging          | Docker + GitHub Actions for multi-arch binaries |

---

## Repository Structure (Proposed)

```
plex-hls-tuner/
├── README.md
├── PLAN.md                 ← this file
├── LICENSE
├── companion/              ← enhanced plex-dvr-hls
│   ├── cmd/
│   ├── internal/
│   ├── api/                ← new REST endpoints
│   ├── config/
│   ├── templates/
│   ├── Dockerfile
│   └── ...
├── extension/              ← Chrome extension
│   ├── manifest.json
│   ├── src/
│   ├── popup/
│   └── ...
├── docs/
│   ├── setup.md
│   ├── api.md
│   └── development.md
├── docker-compose.yml
└── .github/workflows/
```

---

## Immediate Next Steps (right after this plan)

1. Vendor / fork the current plex-dvr-hls code into `/companion`
2. Add a simple REST API layer for dynamic channels
3. Make channels hot-reloadable (no full restart needed)
4. Create the basic Chrome extension skeleton that can talk to the companion
5. Write setup instructions so anyone can get a working demo in < 10 minutes

---

## Success Metrics for v1.0

- [ ] Add any public HLS stream as a Plex Live TV channel in under 30 seconds
- [ ] Support authenticated streams (cookies/headers)
- [ ] Record a show with Plex DVR from a spoofed channel
- [ ] Optional clean download to disk
- [ ] Works on Windows, Linux, and macOS (Docker + native)
- [ ] Clear documentation

---

**Status**: Planning complete. Ready to start Phase 0/1.

Created: 2026-07-11  
Owner: lquessenberry
