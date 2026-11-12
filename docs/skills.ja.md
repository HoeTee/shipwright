# Skill 一覧

[English](skills.md) · [中文](skills.zh-CN.md) · [한국어](skills.ko.md)

[README](README.ja.md) は 8 つのコア skill を示す。
このページは 49 個すべてを書く。
各行は 1 つの仕事である。

shipwright-autopilot、shipwright-swarm、shipwright-arena、shipwright-eval は、頼むまでオフである。

## 開始

| Skill | 何をする |
| --- | --- |
| [shipwright-flow](../skills/shipwright-flow/SKILL.md) | 段階、範囲、許可した操作を選ぶ。 |
| [shipwright-help](../skills/shipwright-help/SKILL.md) | 早見カードとプロンプトを示す。作業は始めない。 |
| [shipwright-setup](../skills/shipwright-setup/SKILL.md) | 各役割のモデルと Git の接続先を設定する。 |
| [shipwright-rules](../skills/shipwright-rules/SKILL.md) | プロジェクトの規則ファイルを下書きする。同意の後に書く。 |

## 理解

| Skill | 何をする |
| --- | --- |
| [shipwright-how](../skills/shipwright-how/SKILL.md) | コードの一区域がどう動くかを説明する。 |
| [shipwright-why](../skills/shipwright-why/SKILL.md) | コードがこの形である理由を説明する。 |
| [shipwright-teach](../skills/shipwright-teach/SKILL.md) | how と why を 1 つの平易な説明にする。 |
| [shipwright-recall](../skills/shipwright-recall/SKILL.md) | 以前の進捗と決定を見つける。 |

## 発見

| Skill | 何をする |
| --- | --- |
| [shipwright-audit](../skills/shipwright-audit/SKILL.md) | リポジトリまたは範囲を監査し、作業を順位づける。 |
| [shipwright-roadmap](../skills/shipwright-roadmap/SKILL.md) | リポジトリの証拠から次の機能を提案する。 |
| [shipwright-diagnose](../skills/shipwright-diagnose/SKILL.md) | バグを再現し、原因を見つける。編集はしない。 |
| [shipwright-impact](../skills/shipwright-impact/SKILL.md) | 変更が別の場所で壊し得るものを確認する。 |

## 計画

| Skill | 何をする |
| --- | --- |
| [shipwright-plan](../skills/shipwright-plan/SKILL.md) | 新しいエージェントが実行できる計画を plans/ に書く。 |
| [shipwright-architect](../skills/shipwright-architect/SKILL.md) | 関数の境界を越えて設計する。呼び出し側から始める。 |
| [shipwright-prototype](../skills/shipwright-prototype/SKILL.md) | 使い捨て試作でやり方を比べる。 |

## 構築

| Skill | 何をする |
| --- | --- |
| [shipwright-build](../skills/shipwright-build/SKILL.md) | 変更を行い、証拠を持ち帰る。 |
| [shipwright-autopilot](../skills/shipwright-autopilot/SKILL.md) | 長い無人のループを進める。マージはしない。 |

## レビュー

| Skill | 何をする |
| --- | --- |
| [shipwright-review](../skills/shipwright-review/SKILL.md) | 1 つの版について確認済みの指摘を報告する。編集はしない。 |
| [shipwright-fix](../skills/shipwright-fix/SKILL.md) | 阻止する指摘を直す。AI レビューの上限を持つ。 |
| [shipwright-interrogate](../skills/shipwright-interrogate/SKILL.md) | 対立する確認を使う。各確認は実行で証明する。 |
| [shipwright-comments](../skills/shipwright-comments/SKILL.md) | レビューの前に悪いコメントを除く。 |

## 出荷

| Skill | 何をする |
| --- | --- |
| [shipwright-ship](../skills/shipwright-ship/SKILL.md) | pull request を開き、CI を追う。マージはしない。 |
| [shipwright-signoff](../skills/shipwright-signoff/SKILL.md) | 人向けの資料を用意する。 |
| [shipwright-land](../skills/shipwright-land/SKILL.md) | 作者以外が検証し、あなたが許可した後に、その版をマージする。 |

## マージの後

| Skill | 何をする |
| --- | --- |
| [shipwright-deploy](../skills/shipwright-deploy/SKILL.md) | 変更を公開し、対象の環境を確認する。 |
| [shipwright-recover](../skills/shipwright-recover/SKILL.md) | 障害ログを読み、新しい修正 pull request を開く。 |
| [shipwright-reconcile](../skills/shipwright-reconcile/SKILL.md) | plans/ の完了、停止、古い計画を確認する。 |
| [shipwright-debt](../skills/shipwright-debt/SKILL.md) | shortcut コメントを台帳に集める。 |
| [shipwright-prevent](../skills/shipwright-prevent/SKILL.md) | 繰り返す誤りが戻らないよう、構造を変える。 |
| [shipwright-reflect](../skills/shipwright-reflect/SKILL.md) | skill の変更を提案する。同意の後にだけ編集する。 |
| [shipwright-cleanup](../skills/shipwright-cleanup/SKILL.md) | 確認の後に、マージ済みの worktree とブランチを除く。 |

## 検証

| Skill | 何をする |
| --- | --- |
| [shipwright-verify-create](../skills/shipwright-verify-create/SKILL.md) | 実製品を操作するプロジェクト skill を作る。 |
| [shipwright-verify-maintain](../skills/shipwright-verify-maintain/SKILL.md) | 製品が変わった後、その skill を更新する。 |
| [shipwright-prove-create](../skills/shipwright-prove-create/SKILL.md) | コストが最も高い性質に形式的証明を足す。 |
| [shipwright-prove-maintain](../skills/shipwright-prove-maintain/SKILL.md) | 証明したコードが変わった後、証明を更新する。 |

## 領域の知識

| Skill | 何をする |
| --- | --- |
| [shipwright-bugs](../skills/shipwright-bugs/SKILL.md) | 作業の正しさの確認を述べる。 |
| [shipwright-security](../skills/shipwright-security/SKILL.md) | 入力、権限、秘密情報の確認を述べる。 |
| [shipwright-test](../skills/shipwright-test/SKILL.md) | 振る舞いのテスト方法と証拠の置き場を述べる。 |
| [shipwright-structure](../skills/shipwright-structure/SKILL.md) | モジュール、層、削除の確認を述べる。 |
| [shipwright-perf](../skills/shipwright-perf/SKILL.md) | 速度を変える前の測定方法を述べる。 |
| [shipwright-lean](../skills/shipwright-lean/SKILL.md) | 各変更を小さく、かつ完全に保つ。 |

## 追加の道具

| Skill | 何をする |
| --- | --- |
| [shipwright-swarm](../skills/shipwright-swarm/SKILL.md) | 並列ワーカーを走らせ、報告を 1 つ返す。 |
| [shipwright-arena](../skills/shipwright-arena/SKILL.md) | 同じ仕事の候補を比べ、強い部分を残す。 |
| [shipwright-trail](../skills/shipwright-trail/SKILL.md) | 決定の記録を残し、別のモデルに再確認を頼む。 |
| [shipwright-recap](../skills/shipwright-recap/SKILL.md) | 各結果について HTML ページを描画する。 |
| [shipwright-write](../skills/shipwright-write/SKILL.md) | 文書、pull request の文、commit メッセージを書く。 |
| [shipwright-readme](../skills/shipwright-readme/SKILL.md) | 実在のファイルと測定結果からプロジェクト README を書く。 |
| [shipwright-skillsmith](../skills/shipwright-skillsmith/SKILL.md) | skill を書く、または編集する。 |
| [shipwright-eval](../skills/shipwright-eval/SKILL.md) | 頼まれたときだけ skill を測定する。 |
