import json, requests, re

API_KEY = "sk-uejmkcsbiwamfjcykymcjwlobubbxyvpvwzwbvlndcpfmtph"

def test_short():
    prompt = """Translate this Chinese title to English (12 words max): 
Title: 专访联影智能联席CEO沈定刚：探索脑影像 AI 的无限可能

Output ONLY the English title, nothing else."""

    payload = {
        "model": "deepseek-ai/DeepSeek-R1-0528-Qwen3-8B",
        "messages": [
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 100,
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(
            "https://api.siliconflow.cn/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=60,
        )
        print(f"Status: {resp.status_code}")
        data = resp.json()
        content = data["choices"][0]["message"]["content"].strip()
        print(f"Result: {content}")
    except Exception as e:
        print(f"Error: {e}")

test_short()
