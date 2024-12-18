#!/bin/bash

# Start Ollama server in the background
/bin/ollama serve &
pid=$!

# Wait for Ollama to initialize
echo "⏳ Waiting for Ollama to initialize..."
sleep 5

# Pull the 'llama2' model
echo "🔴 Pulling 'llama2' model..."
ollama pull llama2

# Verify the model is loaded
echo "🔍 Verifying available models..."
ollama list

# Confirm model loading by running a quick command
echo "⚙️ Testing model load..."
ollama run llama2 <<< "Test prompt"

# Keep Ollama server running
wait $pid
