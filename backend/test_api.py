import requests

url = "https://api.siliconflow.cn/v1/chat/completions"
headers = {
    "Authorization": "Bearer sk-uejmkcsbiwamfjcykymcjwlobubbxyvpvwzwbvlndcpfmtph",
    "Content-Type": "application/json",
}
payload = {
    "model": "deepseek-ai/DeepSeek-R1-0528-Qwen3-8B",
    "messages": [{"role": "user", "content": "Say hi"}],
    "max_tokens": 10,
}

try:
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text[:300]}")
except Exception as e:
    print(f"Error: {e}")
