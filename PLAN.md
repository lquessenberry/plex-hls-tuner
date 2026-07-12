# Plex HLS Tuner – Project Plan

**Goal**: Build a complete "Live TV Tuner Spoofer" that tricks Plex into treating arbitrary HLS streams as real HDHomeRun tuner channels, enabling Live TV viewing + full DVR recording.

This project combines:
- A Chrome extension (HLS detection + easy "Add as Channel" workflow)
- An enhanced version of [plex-dvr-hls](https://github.com/duncanleo/plex-dvr-hls) as the companion backend
- Optional download-to-disk functionality (Video DownloadHelper style)
- **Repurposed Kodi plugins** that already source large libraries of HLS streams (to massively expand available channels)

---

## Vision

1. Browse any website with an HLS stream (news, sports, free live TV, authenticated streams, etc.).
2. Click the extension icon → "Add as Live TV Channel".
3. The stream instantly appears as a channel inside Plex Live TV & DVR.
4. Watch live, pause, and record with Plex DVR just like a real tuner.
5. Optionally download the stream to disk as a clean MP4/MKV.
6. **Import entire channel lineups** from popular Kodi IPTV/HLS plugins (sports, news, free-to-air, regional, adult tubes, free movie sources, etc.) so users get hundreds of channels with almost zero effort.

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
│  • Kodi plugin adapters      │
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
- [x] Basic README and license
- [ ] Add Dockerfile + docker-compose.yml

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
- [ ] Docker + docker-compose ready (with multi-arch support)
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

### Phase 4 – Kodi Plugin Source Libraries (Channel Expansion)
**Target: Massively expand available channels by repurposing existing Kodi HLS/IPTV plugins**

Many popular Kodi addons already do the hard work of discovering, scraping, and maintaining large lists of free/public HLS streams (news, sports, international free-to-air, 24/7 channels, adult tubes, free movie sources, etc.). We will reverse-engineer / adapt their source-fetching logic so our companion can import those channel lists directly.

#### Curated High-Value Kodi Addons (as of July 2026)

**Adult / Tube Streaming Sources (Whitecream-style & successors)**  
These specialize in free adult tube sites, live cams, and large libraries of HLS streams:

| Addon              | Notes                                      | Status / Repo                  |
|--------------------|--------------------------------------------|--------------------------------|
| **Cumination**     | Primary Whitecream clone/successor. Massive multi-site aggregator with excellent filtering | Actively recommended 2026     |
| **AdultHideout**   | Very actively maintained (releases as recent as July 2026). Clean adult video addon | GitHub: Vashiel/repository.adulthideout |
| **Area 69 X**      | Popular, broad content, straightforward    | SouthPaw / community repos    |
| **Ultimate Whitecream** | Classic that still gets mentions           | Team Crew related             |
| **XXX-O-DUS**      | Well organized by genre, VR support        | Community                     |
| **FapZone**        | Frequently listed alongside Cumination     | Community                     |
| **Ali ohh la la**  | Aliunde repository                         | Aliunde                       |

**General Audience – Free Movies, TV, Tube-style & Live Streams**  
These provide free movie/TV scraping + live free-to-air style sources (many use HLS):

| Addon              | Notes                                      | Status / Repo                  |
|--------------------|--------------------------------------------|--------------------------------|
| **The Crew**       | Extremely popular all-in-one. Has movies, TV, live, and adult section | team-crew.github.io           |
| **Scrubs V2**      | Excellent free movie/TV scraper, clean & reliable | jewbmx.github.io              |
| **Elementum**      | Strong free torrent/HLS links              | Community                     |
| **Umbrella**       | High quality (often debrid preferred but free options exist) | Community                     |
| **Free99** (Diggz) | Free movies & TV                           | Diggz repository              |
| **Dream Machine**  | Movies, TV, live streams, free M3U         | Community                     |
| **The Magic Dragon**| Large library, free movies                 | narcacist.com/repo            |
| **Ghost**          | All-in-one from Crew repo                  | Crew                          |
| **Gratis Red**     | Free links focus                           | RED Repository                |
| **POV / Red Light / Fen Light forks** | Advanced free/debrid scrapers         | Community                     |

**Priority for Phase 4 adapters**:  
1. Cumination + AdultHideout (adult tubes)  
2. The Crew + Scrubs V2 + Elementum (general free movies + live)  
3. Free99 / Dream Machine / Magic Dragon as secondary packs

- [ ] Research and catalog high-value Kodi plugins that primarily source HLS streams
- [ ] Create adapter/plugin system inside the companion:
  - Each adapter knows how to fetch + parse the channel list from a given Kodi plugin’s source (API, GitHub raw, M3U, JSON, etc.)
  - Convert their output into our internal channel format (name, m3u8 URL, logo, group, headers if needed)
- [ ] One-click “Import from Kodi Plugin” in the web dashboard / API
- [ ] Support for automatic refresh of those source lists (scheduled or on-demand)
- [ ] Channel grouping & filtering (e.g. “Sports”, “News”, “International”, “Adult”, “Movies 24/7”)
- [ ] Legal / ethical notes: only use publicly available free streams; respect ToS and rate limits; clearly mark adult sources
- [ ] Documentation for adding new Kodi plugin adapters

**Success criteria**: User can import 50–500+ channels from popular Kodi sources with a single command and have them appear instantly in Plex Live TV.

### Phase 5 – Polish & Advanced Features
- [ ] Better EPG support (optional real XMLTV or simple scraper)
- [ ] Temporary vs permanent channels
- [ ] Channel groups / categories
- [ ] Concurrent stream limit ("tuner count")
- [ ] Hardware encoding auto-detect
- [ ] Web dashboard for companion (optional, beyond the API)
- [ ] Auto-restart / watchdogs
- [ ] Windows tray app / Electron wrapper (nice-to-have)
- [ ] DLNA/UPnP server mode (bonus)

### Phase 6 – Packaging & Distribution
- [ ] GitHub Releases with binaries (Windows, Linux, macOS)
- [ ] Chrome Web Store listing (or sideload instructions)
- [ ] Docker Hub / GHCR image
- [ ] Documentation site or detailed wiki
- [ ] Example configs for common free live streams
- [ ] Pre-built channel packs from popular Kodi sources

---

## Tech Stack

| Component          | Technology                          |
|--------------------|-------------------------------------|
| Companion backend  | Go (fork of plex-dvr-hls) + REST API |
| HLS processing     | ffmpeg (cpu / nvenc / vaapi / etc.) |
| Channel storage    | JSON file or SQLite                 |
| Kodi adapters      | Go packages that scrape/parse Kodi plugin sources |
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
│   ├── adapters/           ← Kodi plugin adapters
│   │   ├── adult/          ← Cumination, AdultHideout, etc.
│   │   ├── movies/         ← Scrubs, The Crew, Free99, etc.
│   │   └── live/           ← free-to-air / tube style
│   ├── config/
│   ├── templates/
│   ├── Dockerfile          ← multi-stage Go + ffmpeg
│   └── ...
├── extension/              ← Chrome extension
│   ├── manifest.json
│   ├── src/
│   ├── popup/
│   └── ...
├── docs/
│   ├── setup.md
│   ├── api.md
│   ├── kodi-adapters.md    ← how to add new source plugins
│   └── development.md
├── docker-compose.yml
├── Dockerfile              ← (optional root-level for convenience)
└── .github/workflows/
```

---

## Dockerfile (Planned)

We will provide a production-ready multi-stage Dockerfile for the companion:

```dockerfile
# Stage 1: Build the Go binary
FROM golang:1.23-bookworm AS builder

WORKDIR /app
COPY companion/go.mod companion/go.sum ./
RUN go mod download

COPY companion/ .
RUN CGO_ENABLED=0 GOOS=linux go build -o /plex-hls-tuner ./cmd/main.go

# Stage 2: Runtime with ffmpeg
FROM debian:bookworm-slim

# Install ffmpeg and minimal deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy binary and required templates/config
COPY --from=builder /plex-hls-tuner /app/plex-hls-tuner
COPY companion/templates/ /app/templates/
COPY companion/config.example.json /app/config.json
COPY companion/channels.example.json /app/channels.json

# Expose HDHomeRun port + optional API port
EXPOSE 5004 8080

# Default command
CMD ["/app/plex-hls-tuner"]
```

### docker-compose.yml (example)

```yaml
services:
  plex-hls-tuner:
    build: .
    image: plex-hls-tuner:latest
    container_name: plex-hls-tuner
    ports:
      - "5004:5004"   # HDHomeRun emulator (Plex)
      - "8080:8080"   # REST API (extension + management)
    volumes:
      - ./data/config.json:/app/config.json
      - ./data/channels.json:/app/channels.json
      - ./data:/app/data
    restart: unless-stopped
    # Uncomment for NVIDIA NVENC:
    # runtime: nvidia
    # environment:
    #   - NVIDIA_VISIBLE_DEVICES=all
```

---

## Immediate Next Steps (right after this plan)

1. Vendor / fork the current plex-dvr-hls code into `/companion`
2. Add a simple REST API layer for dynamic channels
3. Make channels hot-reloadable (no full restart needed)
4. Create the basic Chrome extension skeleton that can talk to the companion
5. Write setup instructions so anyone can get a working demo in < 10 minutes
6. Add the multi-stage Dockerfile and docker-compose.yml
7. Begin research on high-value Kodi HLS plugins for Phase 4 adapters (start with Cumination, AdultHideout, The Crew, Scrubs V2)

---

## Success Metrics for v1.0

- [ ] Add any public HLS stream as a Plex Live TV channel in under 30 seconds
- [ ] Support authenticated streams (cookies/headers)
- [ ] Record a show with Plex DVR from a spoofed channel
- [ ] Optional clean download to disk
- [ ] Works on Windows, Linux, and macOS (Docker + native)
- [ ] Clear documentation
- [ ] One-command Docker deploy
- [ ] Import large channel packs from at least 2–3 popular Kodi plugin sources (adult + general)

---

**Status**: Planning complete. Ready to start Phase 0/1.

Created: 2026-07-11  
Updated: 2026-07-11 (added Dockerfile + Kodi plugin source expansion + curated addon list)  
Owner: lquessenberry
