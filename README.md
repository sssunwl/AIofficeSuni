# AI Office Suni — 方案 A（排程式 MVP）

每 15 分鐘由 GitHub Actions 觸發一次，隨機挑 1-2 位 Agent，請 Claude 生成一句他們此刻在辦公室裡的狀態/想法，累積寫進 `office_log.json`。先把「Agent 互動的腦袋」跑順，之後視覺畫面（Sunny 的 2D 設計）做好了再接上來顯示。

## 設定步驟

1. 在 repo 的 **Settings → Secrets and variables → Actions** 新增 secret：
   - `ANTHROPIC_API_KEY`：你的 Claude API key
2. 預設排程是 `*/15 * * * *`（每 15 分鐘一次）；GitHub Actions 的排程觸發不保證準時，負載高時可能延後
3. 也可以到 **Actions → Office Tick → Run workflow** 手動觸發測試

## 檔案結構

```
.github/workflows/office-tick.yml   排程設定
scripts/agents.json                 13 位 Agent 的人設資料
scripts/office_tick.py              觸發時執行的互動腳本
office_log.json                     累積的活動紀錄（最新在最前面，最多保留 200 則）
```
