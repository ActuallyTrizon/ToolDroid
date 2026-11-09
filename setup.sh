#!/usr/bin/env bash

echo "=== ToolDroid Setup ==="

CURRENT_SHELL=$(basename "$SHELL")
echo "[*] Detected active shell: $CURRENT_SHELL"

if [ "$CURRENT_SHELL" = "zsh" ]; then
    echo "[*] Running Zsh-specific installers..."
    zsh ./installers/zsh/installer.sh
    zsh ./installers/zsh/shizuku.sh
else
    echo "[*] Running Bash-specific installers..."
    bash ./installers/bash/installer.sh
    bash ./installers/bash/shizuku.sh
fi

REPO_DIR="$(pwd)"

echo "[*] Registering 'tooldroid' global command..."
cat << EOF > "$PREFIX/bin/tooldroid"
#!/data/data/com.termux/files/usr/bin/bash
python3 "$REPO_DIR/main.py" "\$@"
EOF

chmod +x "$PREFIX/bin/tooldroid"

echo ""
echo "=========================================="
echo "✨ Installation complete! Type 'tooldroid' to run."
echo "=========================================="
