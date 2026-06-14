# ワークスペース設計仕様書 v2

タスク・作業履歴管理のためのディレクトリ構成と作業ルーティン。
3層構造（root_ws → tmp/ 仮WS → 確定WS）で、AI自動振り分けとユーザ確認を分離する。

---

## 1. 全体ディレクトリ構成

```
root_ws/
├── root_ws.instructions.md     ← root WS 専用 Instruction（tmp/・確定WS には適用しない）
├── Inbox/                      ← 生データ 何でも投入（変更・削除禁止）
│   ├── mail/
│   ├── attachments/
│   ├── meeting_transcripts/
│   ├── chat_logs/
│   └── notes/
├── tmp/                        ← AI自動振り分け・仮整理（ユーザ確認前）
│   ├── ws-{slug}-01/
│   │   ├── Inbox/              ← root/Inbox から振り分けてコピー
│   │   └── Summary/
│   │       ├── Report/
│   │       └── meta/
│   └── ws-{slug}-02/ …
├── ws/                         ← 確定ワークスペース群（ユーザ確認・承認後）
│   ├── ws_registry.md          ← 全WS一覧・ステータス管理
│   ├── {slug-A}/
│   │   ├── this_ws.instructions.md
│   │   ├── Inbox/              ← 生データ（不変・read-only）
│   │   ├── Archive/            ← 蒸留済み生データの移動先
│   │   ├── Summary/
│   │   │   ├── Report/
│   │   │   └── meta/           ← sources.md / links.md / status.md
│   │   ├── Output/
│   │   │   ├── drafts/
│   │   │   └── final/
│   │   └── Log/
│   │       ├── sessions/
│   │       ├── decisions/
│   │       └── errors/
│   └── {slug-B}/ …
└── Log/                        ← root WS レベルの AI作業ログ・改善ループ
```

---

## 2. 各層の役割

### Layer 0 — `root_ws/`（常設・受信口）

| ディレクトリ | 役割 |
|---|---|
| `Inbox/` | 全ての生データを無条件で受け入れる。変更・削除禁止。 |
| `tmp/` | AI が自動で仮分類した作業エリア。ユーザ確認前の「草稿」。 |
| `ws/` | ユーザが承認した確定ワークスペース群。 |
| `Log/` | root レベルの AI 作業ログ。全 WS をまたぐ改善ループに使う。 |
| `root_ws.instructions.md` | root WS 専用の Instruction。tmp/ や ws/ には継承しない。 |

### Layer 1 — `tmp/{slug}/`（AI仮整理）

- `Inbox/`・`Summary/`（Report/ + meta/）のみを持つ
- `Output/`・`Log/` は持たない（仮整理段階のため）
- AI がクラスタリングで自動生成。ユーザは Summary を見て判断するだけ

### Layer 2 — `ws/{slug}/`（確定WS）

| ディレクトリ | 役割 |
|---|---|
| `this_ws.instructions.md` | WS init 時生成。このWS内の全操作に適用されるInstruction |
| `Inbox/` | 生データ（不変・read-only） |
| `Archive/` | Inbox から蒸留が完了したファイルの移動先。処理済みの原本置場。 |
| `Summary/` | 蒸留情報・要約・参照リンク |
| `Output/` | 生成成果物（drafts/ / final/） |
| `Log/` | AI作業ログ（sessions/ / decisions/ / errors/） |

---

## 3. Inbox → Archive の移行ルール

確定WS での処理フロー：

```
Inbox/ にファイルが存在する
    ↓
AI が読込・Summary を生成（Inbox は変更しない）
    ↓
Summary/meta/sources.md にソース対応を記録
    ↓
Output/ に成果物を生成
    ↓
（ユーザまたはAIが）蒸留完了と判断
    ↓
Inbox/{file} を Archive/{file} に移動
```

**Archive の意味**：「この生データは Summary/Output に昇華済みであり、Inbox で継続処理の対象ではない」という状態表現。Inbox をクリーンに保ち、まだ処理していないファイルを一目で判断できる。

---

## 4. `root_ws.instructions.md` の設計方針

root WS 専用であり、**tmp/ や ws/ の配下には継承・伝搬しない**。

記述する内容：
- root Inbox の受け入れルール
- tmp/ への自動振り分け基準（AI へのルール）
- ws_registry.md の更新タイミング
- root/Log/ への集約ルール

記述しない内容：
- 個別 WS のタスク詳細（→ this_ws.instructions.md に書く）
- Skill 定義（→ 各 Skill の SKILL.md に書く）

---

## 5. `this_ws.instructions.md`（確定WS用）

WS init 時に生成。このワークスペース内の全 Agent/Skill に適用される。

```markdown
# this_ws.instructions.md

## WS 概要
| 項目 | 値 |
|---|---|
| slug | {YYYY-MM-DD}_{keyword} |
| 案件名 | {案件名} |
| 作成日 | {YYYY-MM-DD} |
| 状態 | active |
| 関連WS | ws/{slug}/ |

## 目的・背景
{この WS で何を達成するか。1〜3 文で記述。}

## 利用可能 Skill
| Skill | SKILL.md | 用途 |
|---|---|---|
| 要約生成 | skills/summarize/SKILL.md | Inbox → Summary/Report/ |
| 成果物作成 | skills/draft-output/SKILL.md | Output/drafts/ 生成 |

## ルール
1. Inbox/ は変更・削除しない（read-only）
2. 蒸留完了したファイルを Archive/ に移動する
3. 成果物はすべて Output/ 以下に保存する
4. セッション終了時に Log/sessions/ にログを記録する
5. ソースと要約の対応は Summary/meta/sources.md に記録する

## 現在の状況
- [ ] {タスク 1}
- [ ] {タスク 2}

---
<!-- state: active | closed -->
<!-- last_updated: {YYYY-MM-DD} -->
```

---

## 6. 作業ルーティン（5フェーズ）

### Phase 1 — 受信（常時）
```
生データ → root_ws/Inbox/ に投入
変更・削除しない。着信順に蓄積するだけ。
```

### Phase 2 — AI仮整理（自動実行）
```
root/Inbox/ を読込
    ↓
件名・差出人・内容でクラスタリング
    ↓
tmp/{slug}/ を生成
    ├── Inbox/ に関連ファイルをコピー
    └── Summary/Report・meta を生成（要約・ソース対応）
    ↓
root/Log/ にセッション記録
    ↓
ユーザへ確認通知
```

### Phase 3 — ユーザ確認・トリアージ
```
tmp/ の Summary を確認
    ↓
判断：
  A. 確定WS に昇格  → ws/{slug}/ を作成、this_ws.instructions.md 生成
  B. 既存WS に統合  → 該当WSのInboxに追加
  C. 破棄           → tmp/{slug}/ を削除
    ↓
ws_registry.md を更新
```

### Phase 4 — 確定WS 処理（AI実行）
```
Inbox/ 読込（不変）
    ↓
Summary/Report・meta 更新
蒸留完了ファイル → Archive/ に移動
    ↓
Output/drafts/ に成果物生成（Skill 呼出）
    ↓
Log/sessions/ にセッション記録
    ↓
ユーザレビュー → Output/final/ に昇格
```

### Phase 5 — クローズ / アーカイブ
```
Log/decisions/ に最終判断を記録
handoff.md を Output/ に生成
    ↓
this_ws.instructions.md の state を closed に更新
ws_registry.md 更新
    ↓
WS をアーカイブ（_archive/ に移動 or zip）
改善点を root/Log/ に集約
```

---

## 7. `ws_registry.md`（全WS一覧）

```markdown
# WS Registry

| slug | 案件名 | 層 | 作成日 | 状態 | 優先度 | 関連WS |
|---|---|---|---|---|---|---|
| 2025-06-14_report-q2 | Q2報告書作成 | ws | 2025-06-14 | active | high | - |
| 2025-06-14_vendor-mail | ベンダー問合せ | tmp | 2025-06-14 | pending | - | - |
| 2025-05-30_vendor-eval | ベンダー評価 | ws | 2025-05-30 | closed | - | - |
```

---

## 8. 設計原則

### tmp/ は「AI の下書き」、ws/ は「ユーザが承認した作業場」
tmp/ はゴミ箱でも最終成果物でもない。AI が人間の確認コストを下げるための「整理済みの提案」。ユーザは Summary を見て3択（昇格・統合・破棄）を選ぶだけ。

### Archive/ は「処理済み」の状態表現
Inbox は「未処理または処理中」の生データ置場。蒸留が完了したファイルを Archive/ に移動することで、Inbox に残るファイルが「まだ処理が必要なもの」だとわかる。Archive の中身は変更しない。

### root_ws.instructions.md は継承しない
root WS のルールが各確定 WS に暗黙的に染み出すと、WS 間の独立性が崩れる。root 専用の Instruction は root スコープにとどめ、確定 WS は this_ws.instructions.md で自己完結させる。

### Log の三分割
`sessions/`（何をしたか）、`decisions/`（なぜそうしたか）、`errors/`（何が失敗したか）を分離。root/Log/ は全 WS をまたぐ横断的な改善に使う。

### Skill との接合点
Agent は「Inbox 読込 → Summary 生成 → Output 生成 → Log 記録」の4ステップだけを担う。ロジックの詳細は Skill 側に持たせる（Skills thick, Agents thin）。
