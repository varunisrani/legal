#!/bin/bash
# Install Node.js and Claude CLI for Render deployment

echo "Installing Node.js and Claude CLI..."

# Install Node.js (using node version manager if available)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

# Install latest LTS Node.js
nvm install --lts
nvm use --lts

# Install Claude Code CLI globally
npm install -g @anthropic-ai/claude-code

# Verify installation
node --version
npm --version
claude --version

echo "Claude CLI installation completed!"