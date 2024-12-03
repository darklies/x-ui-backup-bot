#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print colored message
print_message() {
    echo -e "${2}${1}${NC}"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    print_message "Please run as root (use sudo)" "$RED"
    exit 1
fi

# Function to check command status
check_status() {
    if [ $? -eq 0 ]; then
        print_message "✓ $1 successful" "$GREEN"
    else
        print_message "✗ $1 failed" "$RED"
        exit 1
    fi
}

# Update system
print_message "Updating system packages..." "$YELLOW"
apt-get update
check_status "System update"

# Install required packages
print_message "Installing required packages..." "$YELLOW"
apt-get install -y python3 python3-pip git
check_status "Package installation"

# Create installation directory
INSTALL_DIR="/opt/telegram-xui-bot"
print_message "Creating installation directory..." "$YELLOW"
mkdir -p $INSTALL_DIR
check_status "Directory creation"

# Clone repository
print_message "Cloning repository..." "$YELLOW"
git clone https://github.com/yourusername/telegram-xui-bot.git $INSTALL_DIR
check_status "Repository cloning"

# Install Python requirements
print_message "Installing Python dependencies..." "$YELLOW"
cd $INSTALL_DIR
python3 -m pip install -r requirements.txt
check_status "Python dependencies installation"

# Create systemd service
print_message "Creating systemd service..." "$YELLOW"
cat > /etc/systemd/system/telegram-xui-bot.service << EOL
[Unit]
Description=Telegram X-UI Monitor Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$INSTALL_DIR
ExecStart=/usr/bin/python3 $INSTALL_DIR/src/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOL
check_status "Service creation"

# Configure bot token
print_message "Please enter your Telegram Bot Token:" "$YELLOW"
read -r token
sed -i "s/YOUR_BOT_TOKEN/'$token'/" $INSTALL_DIR/src/config.py
check_status "Bot token configuration"

# Set permissions
print_message "Setting permissions..." "$YELLOW"
chmod -R 755 $INSTALL_DIR
check_status "Permissions setup"

# Start and enable service
print_message "Starting bot service..." "$YELLOW"
systemctl daemon-reload
systemctl enable telegram-xui-bot
systemctl start telegram-xui-bot
check_status "Service startup"

# Final status check
if systemctl is-active --quiet telegram-xui-bot; then
    print_message "✅ Telegram X-UI Monitor Bot has been successfully installed and started!" "$GREEN"
    print_message "You can check the bot status with: systemctl status telegram-xui-bot" "$YELLOW"
    print_message "View logs with: journalctl -u telegram-xui-bot -f" "$YELLOW"
else
    print_message "⚠️ Bot service is not running. Please check the logs for errors." "$RED"
    exit 1
fi