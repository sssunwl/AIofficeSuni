# Suniverse 辦公室快照頁

**線上網址**：https://sssunwl.github.io/AIofficeSuni/

這頁是 Suniverse AI 辦公室（Claw Empire，跑在 `AIoffice/claw-empire`）的**靜態快照**——顯示最後一次更新時的部門狀態、員工狀態、最新動態。目的是讓電腦沒開機時，手機也能看到辦公室最後的樣子。

## 這不是即時畫面

- 想操作、看即時動態 → 開電腦，用 Tailscale 連 `http://<Mac 的 Tailscale IP>:8800`
- 這頁只在每次執行 `AIoffice/scripts/publish_snapshot.py` 時更新一次

## 怎麼更新快照

```bash
python3 /Users/sws/Downloads/claude/AIoffice/scripts/publish_snapshot.py
cd /Users/sws/Downloads/claude/AIoffice/AIofficeSuni-check
git add index.html && git commit -m "update snapshot" && git push
```

之後可以设一個 launchd 排程自動跑（例如每小時一次）。

---

*（本頁在 2026-07-10 起改版：舊版讀 `office_log.json` 的模擬對話系統已停用，改為直接讀 Claw Empire 的 `claw-empire.sqlite` 真實資料。）*
