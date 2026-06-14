# 自律型エージェント開発の設計フレームワーク

コンテキストエンジニアリングにおける **Skill / Prompt / Agent** の定義を統合した設計思想。

**肝心な原則：** 「知能（Prompt）」「機能（Skill）」「役割（Agent）」を **疎結合** に保ち、それぞれを Markdown（.md）で言語化・管理する。

---

## 1. 階層アーキテクチャ（Layered Architecture）

抽象度の高い順に5層で構成される。各レイヤーは「自分の守備範囲」だけに集中し、上位レイヤーの内部実装を知らなくてよい。

| レイヤー | ファイル形式 | 抽象度 | 責務 |
| :--- | :--- | :---: | :--- |
| **Instruction** | `*copilot-instructions.md` | 憲法 | すべての Agent / Prompt / Skill が動作する際の共通前提条件。「重力」として全レイヤーに作用する |
| **Agent** | `*.agent.md` | 役割 | オーケストレーター。ゴール・ポリシー・使用可能な Skill / Prompt のリストを管理する「構成表」 |
| **Prompt** | `*.prompt.md` | 思考 | 思考アルゴリズム。思考プロセス・出力形式・Few-shot を定義し、AI の「解像度」を決定する |
| **Skill** | `SKILL.md` | 能力 | インターフェース仕様書。特定タスクを完遂するための入出力規約と制約。AI にとっての「関数定義」 |
| **Script** | `*.py` / `*.sh` | 実行 | 物理的な手足。LLM を介さない確定的な処理。100% の再現性を担保する実行コード |

---

## 2. Skill レイヤーの定義：能力の外部化

### Skill の粒度

Skill は、**再利用可能な機能モジュール** 単位で定義する。

- **1 Skill = 1 目的** に分割する
- 「何をするか」＋「いつ使うか」を具体的に記述する

```
ワークスペース例
├── skills/
│   ├── data-fetch/SKILL.md       # データ取得 Skill
│   ├── classify/SKILL.md         # 分類・判定 Skill
│   └── generate-output/SKILL.md  # 出力生成 Skill
├── prompts/
│   └── reviewer.prompt.md        # レビュー用 Prompt
└── agents/
    └── orchestrator.agent.md     # 上記 Skill / Prompt を組み合わせて使う Agent
```

---

## 3. 大量データを扱う「動的スケーリング」設計

Agent の認知負荷を抑制しつつ自律性を高めるための **2フェーズ処理**。

### フェーズ①：低解像度スキャン（Script → Manager Agent）

```
Script
  └─ 大量データを取得 → メタデータのみ抽出 → 「目次」を生成

Manager Agent
  └─ 目次だけを読む → どの Skill（または部下 Agent）を呼ぶか判断
```

- Script が詳細データを渡さないことで、Manager のコンテキストウィンドウを節約する
- Manager は「何を処理するか」の **意思決定に専念** する

### フェーズ②：高解像度処理（Skill → Worker Agent）

```
Skill
  └─ Manager から指示された対象の詳細データのみを取得

Worker Agent（Prompt）
  └─ 専用の思考プロセスに従い、限定されたコンテキスト内で作業
```

- 各 Agent が扱う情報量を最小化することで、**精度と速度を両立** する

---

## 4. 疎結合が生む3つの設計メリット

核心的な転換：**「Agent が Skill を所有する」ではなく「Agent が Skill を選択する」**

### 4-1. 情報のカプセル化

`SKILL.md` に入出力の「契約」を書くことで、Agent は内部の Script 実装を知らなくても能力を呼び出せる。

```
Agent ──呼び出す──▶ SKILL.md（契約） ──実行──▶ script.py（実装）
         知らなくていい ↑                      ↑ 変更しても影響なし
```

### 4-2. 認知負荷の分散

役割（Agent）・思考（Prompt）・道具（Skill）を分離することで、大量コンテキストが流れても各レイヤーが守備範囲だけに集中できる。

| レイヤー | 集中する関心事 | 知らなくていいこと |
| :--- | :--- | :--- |
| Agent | 何をいつ呼ぶか | Skill の内部処理 |
| Prompt | どう考えるか | 誰が呼んでいるか |
| Skill | 何を受け取り何を返すか | 上位の判断ロジック |
| Script | どう実行するか | LLM の存在 |

### 4-3. 拡張性

新しい業務が増えたとき、既存ファイルを書き換えない。

```diff
# 新規追加のみ
+ skills/new-capability/SKILL.md
+ skills/new-capability/run.py

# 既存 Agent への最小変更
  agents/orchestrator.agent.md
+   Available Skills:
+     - new-capability
```

---

## 5. 全体像

```
Instruction（憲法）
  └─ Agent（構成表）
       ├─ 使用 Prompt：reviewer.prompt.md
       └─ 使用 Skill：
            ├─ data-fetch/SKILL.md       ──▶ fetch.py
            ├─ classify/SKILL.md         ──▶ classify.py
            └─ generate-output/SKILL.md  ──▶ generate.py
```

> **Agent**（`.agent.md`）は、**Skill**（`SKILL.md`）という道具箱から適切な道具を選び、**Prompt**（`.prompt.md`）という手順書を読みながら、**Script**（`.py`）を使って現実世界を動かす。

この「規格化された仕様書（SKILL.md）」ベースの設計により、AI をチーム開発における **制御可能な同僚** として機能させることができる。
