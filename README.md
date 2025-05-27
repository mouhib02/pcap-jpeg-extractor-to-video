# 🕵️‍♂️ PCAP JPEG Extractor to Video

This tool extracts JPEG images directly from TCP streams inside a `.pcap` file and converts them into a video (`.mp4`) **without saving the images on disk**.

## 🔍 Use Case

Useful in forensics, CTFs (like TryHackMe or HackTheBox), or traffic analysis when:

- A `.pcap` file contains many JPEG images.
- You want to reconstruct a video-like sequence of events from raw HTTP traffic.
- You want a clean, memory-only solution (no disk I/O for images).

## 🚀 Features

- Parses raw TCP streams from `.pcap`.
- Detects embedded JPEG images via binary headers (`FFD8`...`FFD9`).
- Converts the image stream into a playable `.mp4` video.
- No need to extract or store image files.

## 🧰 Requirements

- Python 3.7+
- OpenCV
- NumPy
- Scapy

Install dependencies with:

```bash
pip install -r requirements.txt
