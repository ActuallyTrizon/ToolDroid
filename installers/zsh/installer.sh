#!/bin/zsh
echo "=== ToolDroid Dependency Installer (Zsh) ==="

echo "[*] Updating package repositories..."
pkg update -y

echo "[*] Installing Python, Termux-API, and Curl..."
pkg install python termux-api curl -y

echo "[+] Core dependencies installed successfully."
