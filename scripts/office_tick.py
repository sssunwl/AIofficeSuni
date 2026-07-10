"""
每次觸發：隨機挑 2 位 Agent，請 Claude 生成一段他們之間的簡短辦公室對話
（聊聊新點子、靈感或工作上的觀察），附上時間戳記寫進 office_log.json
（最新的排最前面，只保留最近 200 則避免檔案無限長大）。

模擬模式（不呼叫 API、不花錢）：
- 設定環境變數 OFFICE_MOCK=1，或根本沒有 ANTHROPIC_API_KEY 時自動啟用
- 用內建的對話樣板隨機組裝，讓你可以先測試整條流程（觸發、log 格式、自動 commit）
"""
import json
import os
import random
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENTS_FILE = Path(__file__).resolve().parent / "agents.json"
LOG_FILE = ROOT / "office_log.json"
MAX_ENTRIES = 200

PROMPT_TEMPLATE = """以下是 Suniverse 公司兩位同事的完整角色設定：

【{name1} — {role1}】
{system_prompt1}

【{name2} — {role2}】
{system_prompt2}

請根據以上角色設定，寫一段他們在辦公室裡的真實對話（茶水間、走廊、開會空檔皆可）。內容是聊起一個工作上的新點子、靈感、觀察或趣事，3-4 句，自然口語，繁體中文，不加旁白、舞台指示、表情符號或前後綴。

請嚴格用以下格式輸出，每句一行，不要有空行：
{name1}: ...
{name2}: ...
{name1}: ...
"""

MOCK_TOPICS = [
    "在想要不要把下一支影片改成沒有旁白、純氛圍音的版本",
    "發現最近大家對「慢生活」主題的內容互動率特別高",
    "在考慮幫 SolisAroma 出一款限定香氛，呼應這季的旅行企劃",
    "覺得可以把潛水時拍到的畫面剪成一支療癒系短片",
    "在研究最近一番賞新品牌，覺得有幾款設計很值得追",
    "想嘗試把 ASMR 元素放進產品介紹影片裡",
    "覺得下一篇貼文可以從「沖繩的風」這個角度切入",
]


def load_agents():
    return json.loads(AGENTS_FILE.read_text(encoding="utf-8"))


def load_log():
    if LOG_FILE.exists():
        return json.loads(LOG_FILE.read_text(encoding="utf-8"))
    return []


def parse_turns(raw_text, agent_a, agent_b):
    by_name = {agent_a["name"]: agent_a, agent_b["name"]: agent_b}
    turns = []
    for line in raw_text.splitlines():
        line = line.strip()
        if not line or ":" not in line and "：" not in line:
            continue
        sep = ":" if ":" in line else "："
        name, _, text = line.partition(sep)
        name = name.strip()
        text = text.strip()
        agent = by_name.get(name)
        if agent and text:
            turns.append({"agent": agent["name"], "role": agent["role"], "text": text})
    return turns


def generate_conversation(client, agent_a, agent_b):
    prompt = PROMPT_TEMPLATE.format(
        name1=agent_a["name"], role1=agent_a["role"],
        system_prompt1=agent_a.get("system_prompt", agent_a["style"]),
        name2=agent_b["name"], role2=agent_b["role"],
        system_prompt2=agent_b.get("system_prompt", agent_b["style"]),
    )
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    raw_text = message.content[0].text.strip()
    return parse_turns(raw_text, agent_a, agent_b)


def generate_mock_conversation(agent_a, agent_b):
    topic = random.choice(MOCK_TOPICS)
    return [
        {"agent": agent_a["name"], "role": agent_a["role"],
         "text": f"欸，我剛剛{topic}，你覺得呢？"},
        {"agent": agent_b["name"], "role": agent_b["role"],
         "text": "聽起來蠻有意思的，我覺得可以先做個小範圍測試看看反應。"},
        {"agent": agent_a["name"], "role": agent_a["role"],
         "text": "對啊，先抓個方向出來，之後再一起討論細節。"},
    ]


def main():
    agents = load_agents()
    agent_a, agent_b = random.sample(agents, k=2)

    mock_mode = os.environ.get("OFFICE_MOCK") == "1" or not os.environ.get("ANTHROPIC_API_KEY")

    if mock_mode:
        print("[模擬模式] 不呼叫 API，使用內建對話樣板")
        turns = generate_mock_conversation(agent_a, agent_b)
    else:
        import anthropic
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        turns = generate_conversation(client, agent_a, agent_b)

    if not turns:
        print("沒有產生對話內容，跳過這次。")
        return

    log = load_log()
    now = datetime.now(timezone.utc).isoformat()
    log.insert(0, {
        "time": now,
        "type": "conversation",
        "participants": [agent_a["name"], agent_b["name"]],
        "turns": turns,
    })
    log = log[:MAX_ENTRIES]
    LOG_FILE.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")

    for turn in turns:
        print(f"[{turn['agent']}] {turn['text']}")


if __name__ == "__main__":
    main()
