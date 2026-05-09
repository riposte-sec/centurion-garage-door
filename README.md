# Centurion Garage Door — Home Assistant Integration

A Home Assistant custom integration for the **Centurion Garage Door** controller. Control and monitor your garage door, lamp, and vacation mode — and view the live camera feed — directly from Home Assistant.

## Features

| Entity | Type | Description |
|--------|------|-------------|
| Garage Door | Cover (garage) | Open / Stop / Close with state tracking |
| Lamp | Switch | Toggle the garage light on/off |
| Vacation Mode | Switch | Enable/disable vacation mode |
| Camera | Camera | Live MJPEG stream on port 88 |

## Installation via HACS

1. Open HACS in your Home Assistant instance.
2. Go to **Integrations** → click the three-dot menu → **Custom repositories**.
3. Add this repository URL and select category **Integration**.
4. Click **Install** on the *Centurion Garage Door* card.
5. Restart Home Assistant.

## Configuration

After installation and restart:

1. Go to **Settings → Devices & Services → Add Integration**.
2. Search for **Centurion Garage Door**.
3. Enter:
   - **IP Address / Hostname** — the local IP of your controller (e.g. `192.168.1.100`)
   - **API Key** — found in the controller's web interface
4. Click **Submit**.

All entities will appear under a single device named *Centurion Garage Door*.

## Door State

The door state is derived from the `door` field in the status response. Known states include strings such as `"Closed by WiFi"`, `"Open by WiFi"`, `"Opening"`, and `"Closing"`. The raw status string is exposed as an attribute (`door_status`) on the cover entity for diagnostics.

## Camera

The integration connects to `http://<IP>:88/` as an MJPEG stream. If your device uses a different port or stream format, update the URL in `camera.py`.

## Update Interval

Status is polled every **30 seconds**. After any command (open/close/stop/lamp/vacation) the state is refreshed immediately.
