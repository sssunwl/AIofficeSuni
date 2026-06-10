# Suniverse Virtual Office — 專案狀態

**最後更新**：2026-06-10
**網址**：https://sssunwl.github.io/AIofficeSuni
**Repo**：github.com/sssunwl/AIofficeSuni（main branch）
**本機路徑**：`/tmp/AIofficeSuni/`

---

## 專案

Gather Town 風格 pixel art 虛擬辦公室。13 位 AI Agent 在辦公室裡走動、對話。
HTML5 Canvas 640×992px（20×31 tiles @ 32px），直式佈局，Limezu Modern Interiors 素材。

---

## 完成

### 基礎架構
- [x] HTML5 Canvas 遊戲主框架（640×992px，20×31 tiles，直式）
- [x] 17 個 ZONES 定義（含 corridor）
  - 頂排 3 間：Gym / Conference / Lounge
  - 中間：Open Office（20×8 tiles）
  - 辦公室正下方：CEO Suite (x:0-7) + Corridor (x:8-11) + SS Studio (x:12-19)（y:12-15）
  - 走廊：x:8-11，y:12-27（CEO/SS 行直通至側面房間，共 16 tiles 高）
  - 左側 5 間：Café / Kitchen / Social / Game Room / Theater（y:16-30）
  - 右側 5 間：Souling / Consulting / Aroma Lab / Zen Room / Meditation（y:16-30）
- [x] Zone-based 隨機移動（rndInZone 自適應 padding）
- [x] Y-sorting 深度渲染（靠南的 agent 顯示在前）

### 角色系統
- [x] 13 位 Agent Limezu sprite（Aseprite Lua 腳本生成，Body+Outfit+Hair+Eyes 合成）
- [x] 角色動畫：sy=0 walk-south，FW=32，DW/DH=32（1:1），2 幀循環
- [x] 角色下方橢圓陰影
- [x] 點擊 agent → 側欄顯示對話記錄
- [x] Agent 名稱標籤顯示
- [x] SCALE 變數統一 click/hover 座標縮放計算

### 辦公室行為
- [x] 12 位 Agent 固定桌位（4 cols × 3 rows，ty=7/9/11）
- [x] 85% 機率回自己桌子，15% 去 prefer 或 wander zone
- [x] 分散 idle time（staggered）
- [x] **Waypoint 路徑規劃系統**（SECT 分區 + getWaypoints 重寫）：14 種跨區路線，不穿牆

### 環境／地圖
- [x] Limezu Room_Builder_Floors_32x32 地板 tile 紋理
- [x] Limezu Room_Builder_Walls_32x32 牆壁 tile
- [x] Open Office 12 張桌子用 Limezu Classroom sprite（64×64px）
- [x] 各房間 fillRect 傢具（全部 17 間）
- [x] **門洞視覺**（doorH / doorV 函數）：辦公室→CEO/SS、CEO/SS→各區、走廊兩側每間房均有門
- [x] 走廊環境光條紋 + 走廊標籤
- [x] Zone labels
- [x] 3D 太陽 favicon

### 自動化
- [x] `scripts/office_tick.py`：每 5 分鐘呼叫 Claude API 生成對話
- [x] 模擬模式（OFFICE_MOCK=1）
- [x] 對話寫入 `office_log.json`（最多 200 筆）
- [x] 前端每 5 分鐘 fetch 最新 log

---

## 目前狀態

**Latest commit**：`082e577` — fix: DH=32、CEO/SS with corridor、路徑規劃重寫、theater/meditation 佈局修正
**部署狀態**：已推送，GitHub Pages 約 1 分鐘內生效

### 架構現況

| 模塊 | 狀態 |
|------|------|
| 地板/牆壁 | ✅ Limezu Room_Builder tile |
| Open Office 桌子 | ✅ Limezu Classroom sprite（12 張，3 列） |
| 其他房間傢具 | ⚠️ fillRect（自製像素，非 Limezu sprite） |
| CEO Suite (x:0-7) / SS Studio (x:12-19) | ✅ 辦公室正下方，走廊 (x:8-11) 居中 |
| Theater (x:0-9) / Meditation (x:10-19) | ✅ 最底並排無走廊，各佔 10 tiles |
| 走廊 zone | ✅ x:8-11，y:12-27（共 16 tiles 高）有環境光、格線 |
| 門洞 | ✅ 辦公室入口 3 個 + 走廊側門 8 個 + 底排 4 個 |
| 路徑規劃 | ✅ getWaypoints 重寫，14 種跨區路線，不穿牆 |
| 角色尺寸 | ✅ DW/DH=32，1:1 原始比例 |
| 對話系統 | ✅ 自動生成，每 5 分鐘 |

---

## 下一步

### 視覺優先（最大改善效果）
1. 實際截圖驗證目前版面 — 確認門洞、CEO/SS 位置、走廊渲染正確
2. **Conference room**：確認 CT13 tile 座標，讓會議桌用真實 sprite
3. **Lounge 沙發**：改用 2_LivingRoom_32x32 的沙發 sprite
4. **Gym 器材**：改用 8_Gym_32x32 sprite
5. 逐步替換各房間 fillRect → Limezu sprite（1_Generic 通用傢具優先）

### 功能優化
6. Agent 到桌子時調整 y-position，讓頭頂剛好露出桌面（「坐下」感）
7. Hover tooltip（滑過 agent 顯示名字/角色）
8. office_tick.py 移至 cloud 自動執行（Oracle Cloud Always Free VM）

### 長期
9. 角色互動動畫（兩人靠近時播放特定動作）
10. 3D 感加強（Room_Builder_3d_walls_32x32 實作前景牆面）

---

## 問題/風險

| 問題 | 嚴重度 | 狀態 |
|------|--------|------|
| 門洞位置已重算，需截圖確認視覺效果 | 低 | 待截圖確認 |
| Classroom desk sprite 座標（source 320,0,64,64）未視覺驗證 | 中 | 待截圖確認 |
| Room_Builder Floors/Walls tile 座標為估算值 | 中 | 待截圖確認 |
| 大部分房間傢具仍是 fillRect，整體細緻度不及 Limezu 原版 | 中 | 逐步替換中 |
| office_tick.py cron 每次 push 後本機需先 git pull --rebase | 低 | 已知，每次 push 前手動處理 |
| Conference room CT13 tile 渲染可能不正確 | 中 | 待確認 |
| 路徑規劃 getWaypoints 已全面重寫；若仍發現穿牆需回報具體路線 | 低 | 待觀察 |

---

## Tile Sheets 清單

| 檔案 | 用途 | 座標備註 |
|------|------|---------|
| `Room_Builder_Floors_32x32.png` | 地板紋理 | ft=[x,y] in ZD table |
| `Room_Builder_Walls_32x32.png` | 牆壁 tile | wt=[x,y] in ZD table |
| `5_Classroom_32x32.png` | Open Office 桌子 | source (320,0,64,64) = teacher desk |
| `13_Conference_Hall_32x32.png` | Conference 桌（待驗證） | (0,0) 5×3 tiles |
| `2_LivingRoom_32x32.png` | Lounge 沙發（待實作） | 灰色沙發位置待找 |
| `8_Gym_32x32.png` | Gym 器材（待實作） | 座標待定 |
| `1_Generic_32x32.png` | 通用傢具（待實作） | 座標待定 |
| `Room_Builder_3d_walls_32x32.png` | 3D 前景牆（長期） | 座標待定 |

---

## 關鍵檔案

| 檔案 | 說明 |
|------|------|
| `index.html` | 主遊戲，所有邏輯在此 |
| `assets/characters/agents/*.png` | 13 個 Agent sprite |
| `assets/tiles/*.png` | 8 個 Limezu tile sheets |
| `scripts/office_tick.py` | 對話自動生成腳本 |
| `scripts/agents.json` | 13 位 agent 角色定義 |
| `office_log.json` | 對話 log（最多 200 筆） |
| `/Users/sws/Downloads/claude/AIoffice/generate_agents.lua` | Aseprite 角色生成腳本 |
| `/Users/sws/Downloads/claude/AIoffice/limezu.itch.io/moderninteriors-win/` | Limezu 素材原始位置 |
