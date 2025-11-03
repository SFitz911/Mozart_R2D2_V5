#!/bin/bash
# Quick script to get the public URL from logs

echo "🔍 Finding Public URL..."
echo ""

# Try gradio_url.txt first (fastest)
if [ -f "gradio_url.txt" ]; then
    URL=$(cat gradio_url.txt)
    if [ ! -z "$URL" ]; then
        echo "📡 Public URL:"
        echo ""
        echo "    $URL"
        echo ""
        echo "✅ Found in gradio_url.txt"
        exit 0
    fi
fi

# Try server.out.log with markers
if [ -f "server.out.log" ]; then
    URL=$(grep -A 1 "PUBLIC_URL_START" server.out.log | tail -1)
    if [ ! -z "$URL" ]; then
        echo "📡 Public URL:"
        echo ""
        echo "    $URL"
        echo ""
        echo "✅ Found in server.out.log"
        exit 0
    fi
fi

# Try finding in recent logs
if [ -f "server.out.log" ]; then
    URL=$(grep "https://.*\.gradio\.live" server.out.log | tail -1 | awk '{print $NF}')
    if [ ! -z "$URL" ]; then
        echo "📡 Public URL:"
        echo ""
        echo "    $URL"
        echo ""
        echo "✅ Found in server.out.log"
        exit 0
    fi
fi

echo "❌ No URL found. Is the app running?"
echo "💡 Try: ./start.sh"
exit 1

