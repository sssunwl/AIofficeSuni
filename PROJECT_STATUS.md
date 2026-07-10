# Suniverse Virtual Office — 專案狀態

**最後更新**：2026-06-11（v12）
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
  - 走廊：x:8-11，y:12-27（共 16 tiles 高）
  - 左側 5 間：Café / Kitchen / Social / Game Room / Theater（y:16-30）
  - 右側 5 間：Souling / Consulting / Aroma Lab / Zen Room / Meditation（y:16-30）
- [x] Zone-based 隨機移動（rndInZone 自適應 padding）
- [x] Y-sorting 深度渲染（靠南的 agent 顯示在前）

### 角色系統
- [x] 13 位 Agent Limezu sprite（Aseprite Lua 腳本生成，Body+Outfit+Hair+Eyes 合成）
- [x] `FH=64` 修正（原 32，只渲染頭頂 32px；修正後完整顯示全身）
- [x] 角色動畫：walk-south 2 幀循環（frameIdx * FW）
- [x] 角色下方橢圓陰影
- [x] 點擊 agent → 側欄顯示對話記錄
- [x] Agent 名稱標籤顯示
- [x] SCALE 變數統一 click/hover 座標縮放計算

### 辦公室行為
- [x] 12 位 Agent 固定桌位（環形 12 張桌）
- [x] 85% 機率回自己桌子，15% 去 prefer 或 wander zone
- [x] 分散 idle time（staggered）
- [x] **Waypoint 路徑規劃系統**（SECT 分區 + getWaypoints 重寫）：14+ 種跨區路線，不穿牆
  - T↔O：經頂房中央門洞
  - O↔R：開放式，無障礙
  - L↔L / G↔G：繞走廊（無房間互通門）
  - T↔T：經辦公區中線

### 環境／地圖
- [x] Limezu Room_Builder_Floors_32x32 地板 tile 紋理
- [x] Limezu Room_Builder_Walls_32x32 牆壁 tile
- [x] 門洞系統（doorH / doorV）：
  - 頂房 → 辦公區：各房間正中下一個門洞
  - 辦公區 ↔ CEO/SS/走廊：**無牆無門（全開放）**
  - CEO/SS ↔ 側房：側門 + 底門
  - 走廊 ↔ 左/右各 5 間：走廊側門（無房間互通門）
  - 底排：4 個門洞
- [x] 12 張桌子環形佈局：
  - 北排 5（Sterling/Steve/Stephanie/Scott/Sunny，ty=7，背對頂房）
  - **南排 5（Sona/Sosol/Sean/Saki/Scarlett，ty=9，面對頂房，桌子 Y-flip）**
  - 左端 Souling（tx=3, ty=8）/ 右端 Summer（tx=15, ty=8）
- [x] **2.5D 視覺升級**：
  - 橫向牆壁南側梯度陰影（7px 漸層，模擬牆厚感，跳過門洞位置）
  - 桌子南側梯度陰影（8px 漸層，所有 12 張桌）
- [x] 各房間 fillRect 傢具（全部 17 間）
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

**Latest commit**：`d8981d8` — fix: south row desk Y-flip, agent positions, 2.5D wall/desk shadows
**部署狀態**：已推送，GitHub Pages 約 1 分鐘內生效

| 模塊 | 狀態 |
|------|------|
| 地板/牆壁 | ✅ Limezu Room_Builder tile |
| 門洞系統 | ✅ 頂房中央門 + 走廊側門 + CEO/SS 開放式 |
| Open Office 桌子 | ✅ 12 張環形，南排 Y-flip，2.5D 陰影 |
| 其他房間傢具 | ⚠️ fillRect（自製像素，非 Limezu sprite） |
| 2.5D 牆壁深度 | ✅ 橫向牆南側梯度陰影 |
| 2.5D 桌子陰影 | ✅ 桌子南側梯度陰影 |
| 角色顯示 | ✅ FH=64，全身可見 |
| 路徑規劃 | ✅ getWaypoints 14+ 種路線，不穿牆 |
| 對話系統 | ✅ 自動生成，每 5 分鐘 |
| 截圖視覺確認 | ⏳ 待 SS 確認 v12 效果 |

---

## 下一步

| 優先 | 項目 | 說明 |
|------|------|------|
| 🔴 | 截圖確認 v12 | 確認南排桌子方向、2.5D 陰影效果是否正確 |
| 🟡 | Lounge 沙發 sprite | 改用 `2_LivingRoom_32x32` 的沙發 Limezu sprite |
| 🟡 | Gym 器材 sprite | 改用 `8_Gym_32x32` sprite 替換 fillRect |
| 🟡 | Conference 桌 sprite | 確認 `13_Conference_Hall_32x32` tile 座標 |
| 🟢 | 端桌旋轉（Souling/Summer） | 考慮 90° 旋轉讓端桌方向面向中心 |
| 🟢 | 「坐下」感 | Agent 到桌後調整 y-position，頭頂露出桌面 |
| 🟢 | Oracle Cloud 遷移 | `office_tick.py` 移至 cloud 自動執行 |

---

## 問題/風險

| 問題 | 嚴重度 | 狀態 |
|------|--------|------|
| v12 視覺未截圖確認（Y-flip + 2.5D 是否如預期） | 中 | ⏳ 待 SS 確認 |
| Classroom desk source (320,0,64,64) 實際渲染效果待確認 | 中 | ⏳ 待截圖 |
| 大部分房間傢具仍是 fillRect，整體細緻度不及 Limezu 原版 | 中 | 逐步替換中 |
| 端桌（Souling tx=3 / Summer tx=15）方向尚未旋轉面向中心 | 低 | 待決定是否調整 |
| office_tick.py cron 每次 push 後本機需先 git pull --rebase | 低 | 已知，每次 push 前手動處理 |

---

## Tile Sheets 清單

| 檔案 | 用途 | 狀態 |
|------|------|------|
| `Room_Builder_Floors_32x32.png` | 地板紋理 | ✅ 使用中 |
| `Room_Builder_Walls_32x32.png` | 牆壁 tile | ✅ 使用中 |
| `Room_Builder_3d_walls_32x32.png` | 3D 前景牆（未來）| ⏳ 可用，待整合 |
| `5_Classroom_32x32.png` | Open Office 桌（source 320,0,64,64）| ✅ 使用中，方向已修正 |
| `13_Conference_Hall_32x32.png` | Conference 桌 | ⏳ 座標待確認 |
| `2_LivingRoom_32x32.png` | Lounge 沙發 | ⏳ 待替換 |
| `8_Gym_32x32.png` | Gym 器材 | ⏳ 待替換 |
| `1_Generic_32x32.png` | 通用傢具 | ⏳ 待整合 |

---

## 關鍵檔案

| 檔案 | 說明 |
|------|------|
| `index.html` | 主遊戲，所有邏輯在此 |
| `assets/characters/agents/*.png` | 13 個 Agent sprite |
| `assets/tiles/*.png` | 8 個 Limezu tile sheets |
| `scripts/office_tick.py` | 對話自動生成腳本 |
| `scripts/agents.json` | 13 位 agent 角色定義 |
| `office_log.json` | 對話 log（最多 200 筆）|
