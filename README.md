# Home Assistant 資源總站（教學 · 銷售 · 提示詞 · Skill）

Home Assistant 的四本手冊集中地，繁體中文靜態網站：

| 分類 | 頁面 | 給誰 | 下載 |
|---|---|---|---|
| **入住教學** | [`tutorial.html`](https://woowtech.github.io/Woow_ha_tutorial_site/tutorial.html) ＋ 22 章＋3 附錄 | 用戶 | 整站 zip（GitHub archive） |
| **銷售手冊** | [`sales.html`](https://woowtech.github.io/Woow_ha_tutorial_site/sales.html) | 客戶與經銷商 | 自包含單檔 HTML |
| **AI 提示詞庫** | [`prompts.html`](https://woowtech.github.io/Woow_ha_tutorial_site/prompts.html) | 進階用戶（43+ 條可複製） | 自包含單檔 HTML |
| **Skill 手冊** | [`skills.html`](https://woowtech.github.io/Woow_ha_tutorial_site/skills.html) | 進階用戶（型錄＋速查） | 自包含單檔 HTML |

四類共用一個對外入口 [`index.html`（資源總覽）](https://woowtech.github.io/Woow_ha_tutorial_site/)，hub 上提供各分冊的線上閱讀與下載載點。

- 純靜態站，沒有框架、沒有打包工具，push 到 `main` 由 GitHub Pages 直接提供
- 所有截圖都是 Playwright 從真實 HA 介面自動抓取並疊上紅框／箭頭／編號
- 內容以 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh-hant) 授權釋出

## 入住教學 — 22 章 + 3 附錄

### 基礎：從零到能用

| # | 檔案 | 主題 |
|---|---|---|
| 1 | `ch1_login.html` | 登入 HA、記住我、網頁 vs. Companion App |
| 2 | `ch2_system_settings.html` | 時區、語言、單位、地理位置 |
| 3 | `ch3_floors_areas.html` | 樓層、區域、把設備放進區域 |
| 4 | `ch4_naming_labels.html` | 命名 entity、實體 ID、標籤與分類 |
| 5 | `ch5_users.html` | Users vs. Persons、權限、MFA、位置追蹤 |
| 6 | `ch6_dashboard.html` | 儀表板編輯、多分頁、四種檢視類型 |
| 7 | `ch7_notifications.html` | Companion App、手機通知、動作按鈕 |
| 8 | `ch8_first_automation.html` | 觸發／條件／動作、device_id 陷阱、Blueprint |
| 9 | `ch9_backups.html` | 手動與自動備份、還原、備份存放位置 |
| 10 | `ch10_scripts.html` | 腳本、Fields 參數、執行模式、四種呼叫入口 |
| 11 | `ch11_devices.html` | 裝置頁、韌體更新、停用/隱藏/刪除、Repairs |
| 12 | `ch12_domains.html` | 各 Domain 的常用動作、UI 卡片與常見坑 |

### 擴充：接上更多裝置

| # | 檔案 | 主題 |
|---|---|---|
| 13 | `ch13_themes.html` | 深色模式、社群主題、主題變數、品牌客製 |
| 14 | `ch14_integrations.html` | 整合的新增與診斷、雲端 vs 本地、HACS 自訂整合 |
| 15 | `ch15_protocols.html` | Wi-Fi/Zigbee/Z-Wave/Matter/Thread/BLE/KNX/Modbus/MQTT |
| 16 | `ch16_todo_calendar.html` | 待辦清單、本地與 Google 行事曆、行事曆觸發自動化 |

### 數據、能源與 AI

| # | 檔案 | 主題 |
|---|---|---|
| 17 | `ch17_energy.html` | 能源儀表板、Riemann sum 與 Utility Meter、電價成本 |
| 18 | `ch18_history_data.html` | History/Logbook、Recorder、長期統計、CSV 匯出、InfluxDB |
| 19 | `ch19_voice_ai.html` | Assist pipeline、本地與雲端語音、接 LLM 當對話代理 |

### 進階架構與應用

| # | 檔案 | 主題 |
|---|---|---|
| 20 | `ch20_addons_docker.html` | 四種安裝方式、Supervisor、容器觀念、雲端備份 |
| 21 | `ch21_network_remote.html` | 固定 IP、Cloudflare Tunnel、VPN、反向代理、資安硬規則 |
| 22 | `ch22_life_logs.html` | Helper 做生活紀錄、統計圖表、客製儀表板版面 |

### 附錄

| # | 檔案 | 主題 |
|---|---|---|
| A | `appendix_hacs_addons.html` | 應用程式商店、HACS、遠端連線概觀 |
| B | `appendix_scenes_helpers_groups.html` | 場景、10 種 Helper、群組 |
| C | `appendix_hardware_install.html` | 裝機前傳：安裝方式比較、硬體選擇、HAOS 燒錄與首次開機 |

## 站內結構（hub 模式）

```
index.html               資源總覽 hub       ← 人手維護，build_nav 不碰
tutorial.html            教學目錄            ← build_nav 產生（chapters.json 的 hub.catalog）
ch*.html / appendix_*    教學內容頁         ← head/側欄/pager/footer 由 build_nav 產生
sales.html               銷售手冊            ← 自包含單檔（自帶樣式與圖示，可直接下載）
prompts.html             AI 提示詞庫         ← 自包含單檔，同上
skills.html              Skill 手冊          ← 自包含單檔，同上
404.html                 找不到頁面
chapters.json            單一來源            ← 章節順序/文案/SEO + hub 設定（catalog、pages）
sitemap.xml              產生物，勿手改
robots.txt
assets/css/style.css     全站樣式
assets/js/toc.js         章內錨點 scroll-spy＋手機版側欄收合
assets/screenshots/      標注過的教學截圖
scripts/build_nav.js     導覽產生器（hub 模式）
scripts/check_links.js   站內連結／錨點健檢
scripts/capture.js       截圖產生器
scripts/annotations.json 截圖與標注定義
```

規則：

- 教學章節照舊由 `chapters.json` ＋ `<section data-nav>` 驅動，改完跑 `node scripts/build_nav.js`；目錄卡片輸出到 `tutorial.html`，側欄自帶「◂ 資源總覽」回 hub。
- `sales.html` / `prompts.html` / `skills.html` 是**自包含單檔**（樣式、圖示全部內嵌，離線可開），列在 `chapters.json` 的 `hub.pages`，會納入 sitemap 與 `check_links` 白名單，但不吃內容頁房規（kicker/FAQ/data-icon 對 style.css 的檢查）。
- 新增第五本手冊：寫好自包含 HTML → `hub.pages` 加一筆 → `index.html` 加卡片 → 重跑 build_nav。

## 本地檢視

```bash
git clone https://github.com/WOOWTECH/Woow_ha_tutorial_site.git
cd Woow_ha_tutorial_site
python3 -m http.server 8080     # 或 npx http-server -p 8080
# 瀏覽器打開 http://localhost:8080
```

## 改內容的規則（重要）

導覽結構是**產生**出來的，不要手改。

### 側欄、上下章、目錄卡片、SEO meta

全部來自 `chapters.json` + 每個 `<section>` 上的 `data-nav`。改完跑：

```bash
node scripts/build_nav.js
```

它會覆寫每一頁的 `<head>`、`<aside class="sidebar">`、`chapter-header` 裡的「第 N 章／附錄 X」標記、`<div class="pager">`、`<footer class="site-footer">`，重建 `index.html` 的卡片，並重新產生 `sitemap.xml`。

`chapters.json` 每一章的 `part` 欄位決定它在目錄頁與側欄裡歸在哪一篇；同一個 `part` 字串的章節會被歸成一組。

- **改章節標題／順序／目錄文案** → 改 `chapters.json`，重跑
- **改章內錨點文字** → 改該 `<section>` 的 `data-nav` 屬性，重跑
- **新增一章** → `chapters.json` 加一筆 + 寫好該 HTML 的 `<main>` 內容，重跑。其他 26 個檔案的側欄會自動跟上
- **章節編號不用手寫** → `chapter-header` 的 kicker 由 `num` 產生，所以檔名裡的數字只是穩定網址用的 slug

每個 `<section>` 都必須有 `id` 與 `data-nav`：

```html
<section id="steps" data-nav="動手做：日落開燈">
  <h2 data-icon="steps">動手做：當日落時打開客廳燈</h2>
```

`data-nav` 是側欄用的短標題，`<h2>` 是內文用的完整標題，兩者可以不同。

### 檢查

```bash
node scripts/build_nav.js --check   # 導覽是否與 chapters.json 同步（CI 會擋）
node scripts/check_links.js         # 站內連結、圖片、錨點、重複 id、sitemap 涵蓋率
                                    # 另外會擋：data-icon 沒有對應字符、表格用 inline style、
                                    #           FAQ 不足、缺 chapter-header kicker
```

`.github/workflows/checks.yml` 會：

- **push 到 `main`**：跑一次 `build_nav.js`，有變動就由 `github-actions[bot]` 自動 commit 回來。所以就算忘了在本機跑產生器，線上站也不會跟 `chapters.json` 脫節
- **PR**：只跑 `--check` 與連結檢查，不改檔，把「忘了跑產生器」擋在合併前
- 另外有一個不擋合併的外部連結檢查（lychee）

`build_nav.js` 仍保留 `sectionLabels` 的相容邏輯：HTML 裡的 `<section>` 若沒有 `data-nav`，會去 `chapters.json` 的 `sectionLabels` 找；找不到就從 `<h2>` 推一個短標題並寫回檔案。目前所有章節都已經有 `data-nav`，所以 `chapters.json` 裡不再需要這張表。

新章節的寫作規格在 [`STYLE.md`](STYLE.md)：語氣、可用元件、`data-icon` 清單、章節結構模板與事實查證要求都在那裡。

## 截圖產生器（capture.js）

章節內的截圖都是 Playwright 從一台真實 HA 抓下來，並在 DOM 上疊紅色框／箭頭／編號氣泡後才存檔的。

### 需求

- Node.js ≥ 18
- Playwright（`npm i playwright` + `npx playwright install chromium`）
- 專案根目錄放一個 `.env`（不入版控）：

  ```
  HA_URL=https://your-ha.example.com
  HA_USER=你的帳號
  HA_PASS=你的密碼
  ```

  請用**你自己的 HA**。建議另開一個只做示範用的管理員帳號，不要用擁有者帳號。

### 執行

```bash
node scripts/capture.js                            # 全部章節
node scripts/capture.js --chapter=ch3              # 只跑一章（可逗號多章）
node scripts/capture.js --shot=01_login_page.png   # 只跑一張
```

第一次跑會做 UI 登入並把 session 存到 `storage_state.json`，之後直接復用。要重新登入把該檔刪掉即可。

`scripts/probe_login.js` 是輔助工具，把 HA 登入頁（含 shadow DOM）裡的表單元素印出來，方便對選擇器：

```bash
HA_URL=https://your-ha.example.com node scripts/probe_login.js
```

### 新增／修改截圖

編輯 [`scripts/annotations.json`](scripts/annotations.json)。單一 shot 的欄位：

| 欄位 | 說明 |
|---|---|
| `chapter` | 子目錄名（例 `ch3`），截圖會落到 `assets/screenshots/ch3/` |
| `filename` | 檔名，須是 `.png` |
| `url` | HA 相對路徑，例如 `/config/areas/dashboard` |
| `waitFor` | CSS 選擇器，等它出現才截圖 |
| `waitMs` | 等待毫秒（HA 有很多 shadow DOM 需要 hydrate） |
| `viewport` | `{ width, height }` |
| `fresh` | `true` = 用未登入的新 context（如登入頁截圖） |
| `actions[]` | 截圖前的互動 |
| `annotations[]` | 要疊在圖上的紅色標注 |

`actions[]` 支援：

```json
{ "click": "text=Create floor" }
{ "hover": "some-selector" }
{ "press": "Escape" }
{ "type": { "selector": "input[name=x]", "text": "foo" } }
{ "wait": 2000 }
{ "waitFor": "some-selector" }
{ "url": "/config/other-page" }
```

`annotations[]` 支援三型：

```json
{ "type": "callout", "at": {"x":720,"y":40}, "number": 1, "text": "說明文字" }
{ "type": "box", "selector": "some-element" }
{ "type": "box", "at": {"x":100,"y":200}, "w": 300, "h": 60 }
{ "type": "arrow", "from": {"x":100,"y":100}, "to": {"x":300,"y":200} }
{ "type": "arrow", "from": {"x":100,"y":100}, "selector": "target-element" }
```

### 安全

> **這是活的 HA。** capture.js 只做「開啟頁面 / 開啟對話框 / 截圖 / 關閉頁面」，關頁面 = 未儲存的 draft 丟掉，不會弄壞設定。**請絕對不要在 `actions[]` 裡加 `text=Save` / `text=Delete` / `text=Remove` 之類的 click。**
>
> 這是公開站台 — 提交截圖前請確認畫面上沒有不想公開的資訊（真實姓名、住址、對外網址、Wi-Fi SSID、Token）。

`.gitignore` 已排除 `.env`、`storage_state.json`、`node_modules/`。

## 部署

純靜態站，丟到任何靜態託管都能跑。

- **GitHub Pages（現行）**：push 到 `main` 即生效，來源是 branch `main` / root
- **Docker**：`docker build -t ha-tutorial . && docker run -p 8080:80 ha-tutorial`
  image 只會包含實際對外的檔案 —— `scripts/`、`chapters.json`、`README.md` 都被 `.dockerignore` 擋掉
- **Zeabur / Cloudflare Pages / Netlify**：直接指向這個資料夾
- **內網 nginx**：`root <本目錄>;` + `error_page 404 /404.html;`

站台網址寫在 `chapters.json` 的 `site.baseUrl`（canonical、Open Graph、sitemap 都吃這個值）。換網域時改它再重跑 `build_nav.js`，並同步更新 `robots.txt` 裡的 Sitemap 行。

## 授權

內容（文字與截圖）以 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh-hant) 授權：可自由分享、改作、商業使用，**請保留出處並註明 WoowTech**。完整條款見 [`LICENSE`](LICENSE)。

`scripts/` 內的工具程式同樣以 CC BY 4.0 提供，如需其他授權請開 issue 詢問。

Home Assistant 為 Open Home Foundation 的商標，本專案與其無隸屬關係。
