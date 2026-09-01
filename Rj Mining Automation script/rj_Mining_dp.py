#!/usr/bin/env python3
"""
NRM Packet Sender (SINGLE SOCKET MULTIPLEXER)
=========================================
Reads multiple devices from 'devices.txt' and sends all of their 
packets sequentially over a SINGLE TCP connection. Use this if your 
local test server cannot handle multiple concurrent connections.
"""

import socket
import time
import logging
import re
import os
from datetime import datetime, timezone

# ──────────────────────────────────────────────
# Configuration  ← UPDATE THESE
# ──────────────────────────────────────────────
SERVER_HOST = "minesdata.rajasthan.gov.in"   # ← your local test server
SERVER_PORT = 7001          # ← your local test server port

INTERVAL_SECONDS = 10
SOCKET_TIMEOUT   = 15
RECONNECT_DELAY  = 5

# ──────────────────────────────────────────────
# Logging
# ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# CRC16/ARC checksum
# ──────────────────────────────────────────────
def crc16_arc(data: bytes) -> int:
    crc = 0x0000
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc & 0xFFFF

def compute_checksum(body_with_trailing_comma: str) -> str:
    val = crc16_arc(("$" + body_with_trailing_comma).encode("ascii"))
    return f"{val:04X}"


# ──────────────────────────────────────────────
# Packet parser & Builder
# ──────────────────────────────────────────────
def parse_packet(raw: str, imei: str) -> dict:
    raw = raw.strip()
    if raw.startswith("$"):
        raw = raw[1:]
    raw = raw.split("*")[0]

    fields = raw.split(",")
    frame_idx = None
    for i in range(len(fields) - 1, max(len(fields) - 10, 0), -1):
        if re.fullmatch(r"\d{4,6}", fields[i]):
            frame_idx = i
            break

    if frame_idx is None:
        raise ValueError(f"[{imei}] Could not locate frame number field.")

    return {
        "fields":    fields,
        "frame_idx": frame_idx,
        "date_idx":  9,
        "time_idx":  10,
        "imei":      imei
    }

def build_updated_packet(parsed: dict) -> str:
    fields = parsed["fields"][:]

    now = datetime.now(timezone.utc)
    fields[parsed["date_idx"]] = now.strftime("%d%m%Y")
    fields[parsed["time_idx"]] = now.strftime("%H%M%S")

    old_frame     = fields[parsed["frame_idx"]]
    frame_width   = len(old_frame)
    new_frame_int = int(old_frame) + 1
    if new_frame_int > 999999:
        new_frame_int = 100000
    fields[parsed["frame_idx"]] = str(new_frame_int).zfill(frame_width)

    body = ",".join(fields[:-1]) + ","
    checksum = compute_checksum(body)
    fields[-1] = checksum

    return "$" + ",".join(fields) + "*\r\n"


# ──────────────────────────────────────────────
# TCP helpers
# ──────────────────────────────────────────────
def make_socket(host: str, port: int) -> socket.socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(SOCKET_TIMEOUT)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    s.connect((host, port))
    return s

def ensure_connected(sock, host, port):
    if sock is not None:
        try:
            sock.setblocking(False)
            data = sock.recv(1, socket.MSG_PEEK)
            sock.setblocking(True)
            if len(data) == 0:
                raise ConnectionError("Server closed connection.")
        except BlockingIOError:
            sock.setblocking(True)
            return sock
        except Exception:
            pass

    while True:
        try:
            log.info("Connecting to %s:%s …", host, port)
            s = make_socket(host, port)
            log.info("✓ Connected.")
            return s
        except Exception as exc:
            log.error("Connection failed: %s – retrying in %ss", exc, RECONNECT_DELAY)
            time.sleep(RECONNECT_DELAY)


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  NRM Single-Socket Multiplexer")
    print("=" * 60)
    
    filename = input("Enter the path to your TXT file (default: devices.txt) > ").strip()
    if not filename:
        filename = "imeiVehicle.txt"

    devices = []

    # 1. Read and prepare all devices upfront
    try:
        with open(filename, 'r') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                
                parts = line.split(",")
                if len(parts) >= 2:
                    imei = parts[0].strip()
                    vehicle = parts[1].strip()
                    
                    # Generate the base template for this specific device
                    raw = (
                        f"$1,WTEX,WEA1.0,NR,01,L,{imei},{vehicle},"
                        "0,10072026,094925,028.502982,N,073.086888,E,0.0,293.60,0,"
                        "0217.19,0.00,0.00,airtel,1,1,12.800,3.700,0,O,23,404,10,0964,"
                        "0000000,0|0|00,0011,00,001687,0000,*"
                    )
                    
                    try:
                        parsed = parse_packet(raw, imei)
                        devices.append({"imei": imei, "vehicle": vehicle, "parsed": parsed})
                    except Exception as e:
                        print(f"Failed to parse template for {imei}: {e}")
                else:
                    print(f"Warning: Line {line_num} is malformed. Expected 'IMEI,VehicleNumber'. Skipping.")
                    
    except FileNotFoundError:
        print(f"\nError: Could not find '{filename}'. Please create it and try again.")
        exit(1)

    if not devices:
        print("\nNo valid devices to run. Exiting.")
        exit(0)

    print(f"\nLoaded {len(devices)} devices successfully.")
    print("Starting transmission loop over a SINGLE connection... Press Ctrl+C to stop.\n")

    # 2. Main Transmission Loop
    sock = None
    try:
        while True:
            # Connect to server (or ensure we are still connected)
            sock = ensure_connected(sock, SERVER_HOST, SERVER_PORT)
            
            # Send one packet for every device in the list
            for d in devices:
                packet = build_updated_packet(d["parsed"])
                
                # Update frame number state for the next 10-second cycle
                d["parsed"]["fields"][d["parsed"]["frame_idx"]] = \
                    packet[1:].split("*")[0].split(",")[d["parsed"]["frame_idx"]]

                log.info("[%s] Sending → %s", d["imei"], packet.strip())

                # Attempt to send; reconnect instantly if the socket dropped
                try:
                    sock.sendall(packet.encode("ascii"))
                except Exception as exc:
                    log.warning("[%s] Socket dropped during send (%s). Reconnecting...", d["imei"], exc)
                    sock = None
                    sock = ensure_connected(sock, SERVER_HOST, SERVER_PORT)
                    sock.sendall(packet.encode("ascii"))
            
            # Wait 10 seconds before the next batch
            time.sleep(INTERVAL_SECONDS)
            
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")