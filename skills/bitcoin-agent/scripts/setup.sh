#!/usr/bin/env bash
# Bitcoin AI Agent — Setup Script
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Bitcoin AI Agent Setup ==="
echo

# 1. Install Python dependencies
echo "[1/3] Installing Python dependencies..."
pip3 install --quiet fastapi uvicorn httpx pymacaroons pyyaml python-dotenv
echo "    ✓ Dependencies installed"

# 2. Create config.yaml from template if missing
if [ ! -f config.yaml ]; then
    echo "[2/3] Creating config.yaml from template..."
    cp config.yaml.template config.yaml
    echo "    ✓ config.yaml created — edit it with your API keys"
else
    echo "[2/3] config.yaml already exists, skipping"
fi

# 3. Create .env template if missing
if [ ! -f .env ]; then
    echo "[3/3] Creating .env template..."
    cat > .env << 'EOF'
# Bitcoin AI Agent Environment Variables
# These override values in config.yaml

# LNBITS_URL=http://localhost:5000
# LNBITS_API_KEY=your-invoice-read-key
# L402_SECRET_KEY=random-secret-string
# LLM_API_KEY=your-openai-or-anthropic-key
# LLM_PROVIDER=openai
# LLM_MODEL=gpt-4o-mini
# SERVER_HOST=0.0.0.0
# SERVER_PORT=8402
EOF
    echo "    ✓ .env template created"
else
    echo "[3/3] .env already exists, skipping"
fi

echo
echo "=== Setup Complete ==="
echo
echo "Next steps:"
echo "  1. Install Phoenixd:  https://phoenix.acinq.co/server"
echo "  2. Run LNbits:        docker run -d -p 5000:5000 lnbits/lnbits"
echo "  3. Edit config.yaml   with your LNbits API key and LLM API key"
echo "  4. Start the agent:   python server.py"
echo "  5. Test it:           python test_client.py"
echo
