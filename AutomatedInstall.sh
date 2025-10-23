conda create -n apc -y
conda activate apc

curl -fsSL https://ollama.com/install.sh | sh
# ollama serve
ollama pull gpt-oss:20b

pip install ollama openpyxl