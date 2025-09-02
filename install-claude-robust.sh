#!/bin/bash
# Robust Claude CLI installation for Render

echo "=== Claude CLI Installation for Render ==="

# Check if Node.js is already available
if command -v node &> /dev/null; then
    echo "✅ Node.js already installed: $(node --version)"
else
    echo "📦 Installing Node.js..."
    
    # Install Node.js using the official method for Render
    curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Check if npm is available
if command -v npm &> /dev/null; then
    echo "✅ npm available: $(npm --version)"
else
    echo "❌ npm not found"
    exit 1
fi

# Install Claude CLI globally
echo "📦 Installing Claude CLI..."
npm install -g @anthropic-ai/claude-code

# Verify Claude CLI installation
if command -v claude &> /dev/null; then
    echo "✅ Claude CLI installed successfully: $(claude --version)"
else
    echo "❌ Claude CLI installation failed"
    
    # Try alternative installation paths
    if [ -f "/usr/local/bin/claude" ]; then
        echo "✅ Claude CLI found at /usr/local/bin/claude"
        ln -sf /usr/local/bin/claude /usr/bin/claude
    elif [ -f "$HOME/.npm-global/bin/claude" ]; then
        echo "✅ Claude CLI found at $HOME/.npm-global/bin/claude"
        export PATH="$HOME/.npm-global/bin:$PATH"
    elif [ -f "$HOME/node_modules/.bin/claude" ]; then
        echo "✅ Claude CLI found at $HOME/node_modules/.bin/claude"
        export PATH="$HOME/node_modules/.bin:$PATH"
    else
        echo "🔍 Searching for Claude CLI..."
        find /usr -name "claude" 2>/dev/null | head -5
        find $HOME -name "claude" 2>/dev/null | head -5
    fi
fi

echo "🔧 Final PATH check..."
echo "PATH: $PATH"
which claude || echo "❌ Claude CLI not in PATH"

echo "=== Installation Complete ==="