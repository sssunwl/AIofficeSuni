# Suniverse Virtual Office — 專案狀態

**最後更新**：2026-06-10
**網址**：https://sssunwl.github.io/AIofficeSuni
**Repo**：github.com/sssunwl/AIofficeSuni（main branch）
**本機路徑**：`/tmp/AIofficeSuni/`

---

## 專案

Gather Town 風格 pixel art 虛擬辦公室。13 位 AI Agent 在辦公室裡走動、對話。
HTML5 Canvas 960×576px（30×18 tiles @ 32px），Limezu Modern Interiors 素材。

---

## 完成

### 基礎架構
- [x] HTML5 Canvas 遊戲主框架（960×576px，30×18 tiles）
- [x] 15 個房間 ZONES 定義（正確 layout）
  - 左側 5 間：Café / Kitchen / Social / Game Room / Theater
  - 中上 3 間：Gym / Conference / Lounge
  - 中間：Open Office（20×9 tiles）
  - 中下 2 間：CEO Suite / SS Studio
  - 右側 5 間：Souling / Consulting / Aroma Lab / Zen Room / Meditation
- [x] Zone-based 隨機移動（rndInZone 自適應 padding）
- [x] Y-sorting 深度渲染（靠南的 agent 顯示在前）

### 角色系統
- [x] 13 位 Agent Limezu sprite（Aseprite Lua 腳本生成，Body+Outfit+Hair+Eyes 合成）
- [x] 角色動畫：sy=0 walk-south（面向觀看者），FW=32，DW/DH=64，2 幀循環
- [x] FW=32 修正（之前 FW=48 導致取到灰色背面 row → gray blob bug 修復）
- [x] 角色下方橢圓陰影
- [x] 點擊 agent → 側欄顯示對話記錄
- [x] Agent 名稱標籤顯示

### 辦公室行為
- [x] Home desk 分配（Sterling/Steve/Stephanie/Scott/Sunny/Sona/Sosol/Sean 有固定座位）
- [x] 85% 機率回自己桌子，15% 去 prefer 或 wander zone
- [x] 分散 idle time（staggered，避免全員同時移動）
- [x] 走路後 idle 500-1200 ms

### 環境／地圖
- [x] Limezu Room_Builder_Floors_32x32 地板 tile 紋理
- [x] Limezu Room_Builder_Walls_32x32 牆壁 tile（2 row wall strip + 深度陰影線）
- [x] Open Office 8 張桌子改用 Limezu Classroom sprite（真實像素桌，64×64px）
- [x] 各房間 fillRect 傢具（Café 吧台/桌椅、Kitchen 爐灶/冰箱、Theater 大銀幕座位、Gym 器材、Conference 桌椅、Lounge 沙發書架、CEO/Studio 豪華辦公桌、右側各房間特色傢具）
- [x] Zone labels（房間名稱）
- [x] 3D 太陽 favicon（SVG radial gradient）

### 自動化
- [x] `scripts/office_tick.py`：每 5 分鐘隨機挑 2 位 agent，呼叫 Claude API 生成對話
- [x] 模擬模式（OFFICE_MOCK=1，無需 API key 可測試）
- [x] 對話結果寫入 `office_log.json`（最多 200 筆）
- [x] 前端每 5 分鐘 fetch 最新 log

---

## 目前狀態

**Latest commit**：`7db6e1c` — feat: 用 Limezu Classroom sprite 取代 fillRect 桌子
**部署狀態**：已推送，GitHub Pages 約 1 分鐘內生效

### 架構現況

| 模塊 | 狀態 |
|------|------|
| 地板/牆壁 | ✅ Limezu Room_Builder tile |
| Open Office 桌子 | ✅ Limezu Classroom sprite (8 張，2 列) |
| 其他房間傢具 | ⚠️ fillRect（自製像素，非 Limezu sprite） |
| Conference 桌 | ⚠️ Conference_Hall sheet 已載入但 tile 座標待驗證 |
| 角色 sprite | ✅ Limezu 13 位 |
| 角色動畫 | ✅ walk-south 2 幀 |
| 對話系統 | ✅ 自動生成，每 5 分鐘 |

---

## 下一步

### 視覺優先（最大改善效果）
1. **截圖驗證** Classroom desk sprite（`source: 320, 0, 64, 64`）是否顯示正確桌子
2. **Conference room**：確認 CT13 tile 座標，讓會議桌用真實 sprite
3. **Lounge 沙發**：改用 2_LivingRoom_32x32 的灰色沙發 sprite（Conference_Hall 金色沙發 source ~0,0,128,96 也可用）
4. **Gym 器材**：改用 8_Gym_32x32 sprite
5. 全房間逐步替換 fillRect → Limezu sprite（1_Generic 有很多通用傢具）

### 功能優化
6. Agent 到桌子時真正「坐下」感（調整 agent y-position 讓頭頂剛好露出桌面上方）
7. Hover tooltip（滑過 agent 顯示名字/角色，不用點擊）
8. 加入 Sona 的 office_tick cron 設定（目前只在本機跑）

### 長期
9. 虛擬辦公室 Phase II（移至 cloud 自動執行 office_tick）
10. 角色互動動畫（兩人靠近時播放特定動作）

---

## 問題/風險

| 問題 | 嚴重度 | 狀態 |
|------|--------|------|
| Classroom desk sprite 座標未視覺驗證（source 320,0,64,64 可能不是正確桌子） | 中 | 待截圖確認 |
| Room_Builder Floors/Walls tile 座標為估算值，部分房間可能顯示錯誤 tile | 中 | 待截圖確認 |
| office_tick.py cron 每次 push 會導致本機 push 被 rejected（需先 rebase） | 低 | 已知，每次 push 前 git pull --rebase |
| 大部分房間傢具仍是 fillRect，整體細緻度仍不及 Limezu 原版 Modern Office | 中 | 逐步替換中 |
| Conference room CT13 tile 渲染可能不正確（直接用 5×3 tile 從 (0,0) 開始可能不是桌子） | 中 | 待確認 |
| 角色 chibi 風格 + 暗色系 → 在某些房間背景下仍顯得小 | 低 | 可接受，Limezu 本身風格 |

---

## Tile Sheets 清單

| 檔案 | 用途 | 座標備註 |
|------|------|---------|
| `Room_Builder_Floors_32x32.png` | 地板紋理 | ft=[x,y] in ZD table |
| `Room_Builder_Walls_32x32.png` | 牆壁 tile | wt=[x,y] in ZD table |
| `5_Classroom_32x32.png` | Open Office 桌子 | source (320,0,64,64) = teacher desk |
| `13_Conference_Hall_32x32.png` | Conference 桌（待驗證） | 直接用 (0,0) 5×3 tiles |
| `2_LivingRoom_32x32.png` | Lounge 沙發（待實作） | 灰色沙發位置待找 |
| `8_Gym_32x32.png` | Gym 器材（待實作） | 座標待定 |
| `1_Generic_32x32.png` | 通用傢具（待實作） | 座標待定 |

---

## 關鍵檔案

| 檔案 | 說明 |
|------|------|
| `index.html` | 主遊戲，所有邏輯在此 |
| `assets/characters/agents/*.png` | 13 個 Agent sprite |
| `assets/tiles/*.png` | 7 個 Limezu tile sheets |
| `scripts/office_tick.py` | 對話自動生成腳本 |
| `scripts/agents.json` | 13 位 agent 角色定義 |
| `office_log.json` | 對話 log（最多 200 筆） |
| `/Users/sws/Downloads/claude/AIoffice/generate_agents.lua` | Aseprite 角色生成腳本 |
| `/Users/sws/Downloads/claude/AIoffice/limezu.itch.io/moderninteriors-win/` | Limezu 素材原始位置 |
