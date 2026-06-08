"""
每次觸發：隨機挑 1-2 位 Agent，請 Claude 生成一句他們此刻在辦公室裡的狀態/想法，
附上時間戳記寫進 office_log.json（最新的排最前面，只保留最近 200 則避免檔案無限長大）。
"""
import json
import os
import random
from datetime import datetime, timezone
from pathlib import Path

import anthropic

ROOT = Path(__file__).resolve().parent.parent
AGENTS_FILE = Path(__file__).resolve().parent / "agents.json"
LOG_FILE = ROOT / "office_log.json"
MAX_ENTRIES = 200

PROMPT_TEMPLATE = """你是 Suniverse 公司的 {name}，職位是{role}。
你的關鍵詞是「{keywords}」，說話風格是：{style}

現在是辦公室裡的某個時刻，請用第一人稱寫一句你此刻正在做的事或腦中閃過的想法（繁體中文，30-60字，像隨手寫下的內心獨白或工作筆記，不要加任何前綴或引號）。"""


def load_agents():
    return json.loads(AGENTS_FILE.read_text(encoding="utf-8"))


def load_log():
    if LOG_FILE.exists():
        return json.loads(LOG_FILE.read_text(encoding="utf-8"))
    return []


def generate_entry(client, agent):
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": PROMPT_TEMPLATE.format(**agent),
        }],
    )
    return message.content[0].text.strip()


def main():
    agents = load_agents()
    picked = random.sample(agents, k=random.choice([1, 2]))

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    log = load_log()
    now = datetime.now(timezone.utc).isoformat()

    for agent in picked:
        text = generate_entry(client, agent)
        log.insert(0, {
            "time": now,
            "agent": agent["name"],
            "role": agent["role"],
            "text": text,
        })
        print(f"[{agent['name']}] {text}")

    log = log[:MAX_ENTRIES]
    LOG_FILE.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
