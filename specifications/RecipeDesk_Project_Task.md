# RecipeDesk Project — Ticket List 
---

## 1. Specification Phase（仕様書作成）

### **T1_01_Screen_Specification_Creation**
- 画面仕様書（簡易）の作成を行う。  
  一覧・詳細・登録画面のレイアウト、ヘッダー仕様、遷移仕様をまとめる。

### **T1_02_Function_Specification_Creation**
- 機能仕様書（簡易）の作成を行う。  
  CSV構造、CRUD処理、画像処理、画面遷移ロジックなどを明文化する。

---

## 2. Development Phase（開発）

### **T2_01_CSV_Model_Implementation**
- CSV をデータベースとして扱うモデル層を実装する。  
  レコード読み込み、ID検索、登録処理、材料・ステップ不足分の空欄補完などを含む。

### **T2_02_Image_Management_Module_Implementation**
- 画像管理モジュールを実装する。  
  画像コピー（/images配下）、リサイズ処理、プレビュー用画像生成、パス正規化などを含む。

---

### **T2_10_Common_Header_Implementation**
- 共通ヘッダー（RecipeDeskタイトル左、一覧/登録ボタン右）を実装する。  
  全画面で共通して表示されるナビゲーションバーを構築する。

### **T2_11_List_View_Implementation**
- 一覧画面（ListView）を実装する。  
  2列×N行のカード形式グリッドでサムネイル画像とタイトルを表示し、クリックで詳細画面へ遷移できるようにする。

### **T2_12_Detail_View_Implementation**
- 詳細画面（ReadView）を実装する。  
  画像（左）、材料（右）、ステップ（下段）の構成で表示し、戻る/次へボタンでループ式にレシピを切り替えられるようにする。

### **T2_13_Create_View_Implementation**
- 登録画面（CreateView）を実装する。  
  タイトル、材料（9枠）、ステップ（6枠）、画像アップロード（Explorer + ドラッグ＆ドロップ）を縦並びで配置し、SubmitでCSVへ保存する。

---

### **T2_20_View_Switching_Controller_Implementation**
- 画面切替を管理するコントローラーを実装する。  
  一覧・詳細・登録画面を同一ウィンドウ内で切り替えられるようにする。

---

## 3. Test Phase（テスト）

### **T3_00_Test_Specification_Creation**
- テスト仕様書（Test Specification）の作成を行う。  
  テスト観点、テストケース一覧、入力と期待値の整理などを文書化する。

---

### **T3_01_CSV_Model_Test**
- CSVモデルのテストを行う。  
  読み込み、書き込み、ID管理、空欄補完などの挙動を確認する。

### **T3_02_Image_Management_Test**
- 画像管理モジュールの動作テストを行う。  
  コピー、リサイズ、異常ファイル対応、パス管理の確認。

### **T3_10_List_View_Test**
- 一覧画面の表示テストを行う。  
  サムネイル表示、レイアウト崩れ、クリック遷移などを確認する。

### **T3_11_Detail_View_Test**
- 詳細画面のテストを行う。  
  表示内容、画像・材料・ステップの整合性、戻る/次へのループ動作を検証。

### **T3_12_Create_View_Test**
- 登録画面のテストを行う。  
  入力内容の保存、画像アップロード・D&D動作、CSV保存処理を確認する。

---

