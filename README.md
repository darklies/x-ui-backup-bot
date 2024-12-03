# Telegram X-UI Monitor Bot

This bot monitors your X-UI panel and sends periodic updates about the database status.

## Installation

### Quick Install (Recommended)

```bash
curl -sSL https://raw.githubusercontent.com/yourusername/telegram-xui-bot/main/install.sh | sudo bash
```

### Manual Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/telegram-xui-bot.git
cd telegram-xui-bot
```

2. Install dependencies:
```bash
python3 -m pip install -r requirements.txt
```

3. Configure the bot:
- Edit `src/config.py` and set your Telegram Bot Token

4. Run the bot:
```bash
python3 src/bot.py
```

## Usage

1. Start a chat with your bot on Telegram
2. Use `/start` to begin setup
3. Follow the prompts to configure your X-UI panel credentials
4. Use `/status` to check the current monitoring status

## Service Management

- Check status: `systemctl status telegram-xui-bot`
- View logs: `journalctl -u telegram-xui-bot -f`
- Restart bot: `systemctl restart telegram-xui-bot`
- Stop bot: `systemctl stop telegram-xui-bot`

## Security Notes

- The bot stores credentials in `/opt/telegram-xui-bot/data/credentials.json`
- Make sure to secure your server and restrict access to the installation directory
- Regularly update your system and the bot for security patches