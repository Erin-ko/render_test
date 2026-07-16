# FastAPI Hello API for Render

這是一個準備好部署到 Render 的簡單 FastAPI API。它包含一個回傳 `"Hello"` 的根路由以及一個用於健康檢查的 `/health` 路由。

## 專案結構
- [main.py](file:///c:/Users/Erin/Desktop/render_test/main.py): FastAPI 應用程式主程式。
- [requirements.txt](file:///c:/Users/Erin/Desktop/render_test/requirements.txt): 專案相依套件。
- [render.yaml](file:///c:/Users/Erin/Desktop/render_test/render.yaml): Render Blueprint 部署設定檔。

## 本地開發與測試

1. **建立虛擬環境並安裝套件**：
   ```bash
   python -m venv venv
   # Windows
   ./venv/Scripts/activate
   # macOS/Linux
   source venv/bin/activate

   pip install -r requirements.txt
   ```

2. **啟動開發伺服器**：
   ```bash
   uvicorn main:app --reload
   ```

3. **測試 API**：
   - 瀏覽器開啟 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)，應該會看到：`{"message": "Hello"}`。
   - 瀏覽器開啟 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 查看自動生成的 Swagger API 文件。

---

## 部署到 Render

你可以透過以下兩種方式之一來部署此專案到 Render：

### 方法一：使用 Blueprint 部署（最推薦，一鍵設定）
1. 將此專案推送到你的 GitHub 或 GitLab 儲存庫。
2. 登入 [Render 控制台](https://dashboard.render.com/)。
3. 點擊 **Blueprints** -> **New Blueprint Instance**。
4. 選擇你的儲存庫。
5. Render 會自動讀取 `render.yaml`，你只需要確認並點擊 **Apply** 即可完成部署！

### 方法二：手動建立 Web Service
1. 將此專案推送到你的 GitHub 或 GitLab 儲存庫。
2. 登入 [Render 控制台](https://dashboard.render.com/)。
3. 點擊 **New +** -> **Web Service**。
4. 連結你的 GitHub 帳號並選擇此專案的儲存庫。
5. 設定以下欄位：
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. 點擊 **Create Web Service** 即可開始部署。
