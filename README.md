# AI Office Suni — 方案 A（排程式 MVP）

每 15 分鐘由 GitHub Actions 觸發一次，隨機挑 2 位 Agent，請 Claude 生成一段他們之間的簡短對話（聊聊新點子、靈感或工作觀察），累積寫進 `office_log.json`。先把「Agent 互動的腦袋」跑順，之後視覺畫面（Sunny 的 2D 設計）做好了再接上來顯示。

## 模擬模式（不花錢測試）

還沒準備好付費呼叫 API 也沒關係：

- 到 **Actions → Office Tick → Run workflow**，把「模擬模式」打勾後手動觸發
- 或在本機執行 `OFFICE_MOCK=1 python scripts/office_tick.py`
- 沒有設定 `ANTHROPIC_API_KEY` 時也會自動進入模擬模式

模擬模式會用內建的對話樣板組裝出一段示範對話，讓你先確認整條流程（觸發、log 格式、自動 commit 推送）跑得順，完全不會呼叫 Claude、不花錢。等準備好了，把模擬模式關掉、設定好 API key，就會換成由 Claude 真正生成的對話。

## 設定步驟

1. 在 repo 的 **Settings → Secrets and variables → Actions** 新增 secret：
   - `ANTHROPIC_API_KEY`：你的 Claude API key
2. 預設排程是 `*/15 * * * *`（每 15 分鐘一次）；GitHub Actions 的排程觸發不保證準時，負載高時可能延後
3. 也可以到 **Actions → Office Tick → Run workflow** 手動觸發測試（記得勾選/取消「模擬模式」）

## 檔案結構

```
.github/workflows/office-tick.yml   排程設定
scripts/agents.json                 13 位 Agent 的人設資料
scripts/office_tick.py              觸發時執行的互動腳本
office_log.json                     累積的活動紀錄（最新在最前面，最多保留 200 則）
```
