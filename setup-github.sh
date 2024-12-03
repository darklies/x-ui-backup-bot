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

# Initialize git repository
print_message "Initializing Git repository..." "$YELLOW"
git init

# Add all files
print_message "Adding files to Git..." "$YELLOW"
git add .

# Initial commit
print_message "Creating initial commit..." "$YELLOW"
git commit -m "Initial commit: Telegram X-UI Monitor Bot"

# Get GitHub username
print_message "Enter your GitHub username:" "$YELLOW"
read -r github_username

# Get repository name (default: telegram-xui-bot)
print_message "Enter repository name (press Enter for 'telegram-xui-bot'):" "$YELLOW"
read -r repo_name
repo_name=${repo_name:-telegram-xui-bot}

# Update README and install.sh with correct username
print_message "Updating README and install script with your username..." "$YELLOW"
sed -i "s/yourusername/$github_username/g" README.md
sed -i "s/yourusername/$github_username/g" install.sh

# Commit the changes
git add README.md install.sh
git commit -m "Update repository URLs with correct username"

# Create GitHub repository
print_message "Creating GitHub repository..." "$YELLOW"
print_message "Please enter your GitHub Personal Access Token (with 'repo' scope):" "$YELLOW"
read -r github_token

curl -H "Authorization: token $github_token" \
     -d "{\"name\":\"$repo_name\", \"private\":false}" \
     https://api.github.com/user/repos

# Add remote and push
print_message "Pushing to GitHub..." "$YELLOW"
git remote add origin "https://github.com/$github_username/$repo_name.git"
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    print_message "✅ Successfully uploaded to GitHub!" "$GREEN"
    print_message "Repository URL: https://github.com/$github_username/$repo_name" "$GREEN"
    print_message "\nNext steps:" "$YELLOW"
    print_message "1. Visit https://github.com/$github_username/$repo_name to view your repository" "$NC"
    print_message "2. Update the bot token in src/config.py" "$NC"
    print_message "3. Share the installation command:" "$NC"
    print_message "   curl -sSL https://raw.githubusercontent.com/$github_username/$repo_name/main/install.sh | sudo bash" "$NC"
else
    print_message "❌ Failed to push to GitHub. Please check your token and try again." "$RED"
fi