#!/bin/bash

echo "=== Shizuku Setup ===="

if ! command -v rish &> /dev/null; then
    echo "[*] rish is missing. Installing via merbah3266/rish_installer..."
    bash <(curl -fsSL tinyurl.com/rish3266)
else
    echo "[+] rish is already installed and available globally."
fi

echo "[+] Rish installer complete"
