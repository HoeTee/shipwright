<div align="center">

[English](../README.md) · [中文](README.zh-CN.md) · [한국어](README.ko.md)

# Shipwright

**Shipwright は、1 つのコーディング作業を最初の確認から人のマージ判断まで進める。**

Codex、Claude Code、OpenCode 向けのプラグイン

[![CI](https://github.com/HoeTee/shipwright/actions/workflows/ci.yml/badge.svg)](https://github.com/HoeTee/shipwright/actions/workflows/ci.yml)
[![Plugin](https://img.shields.io/badge/plugin-Codex%20%C2%B7%20Claude%20Code%20%C2%B7%20OpenCode-1f6feb)](../references/platforms.md)
[![MIT](https://img.shields.io/badge/license-MIT-lightgrey)](../LICENSE)

[導入](#インストールして試す) · [流れ](#作業の流れ) · [コア skill](#コア-skill) · [例](#例) · [質問](#よくある質問)

</div>

## インストールして試す

プラグインを入れる。その後、新しいセッションを開く。

### Claude Code

次のコマンドは Claude Code 2.1.292 以降で使う。

```bash
claude plugin install shipwright --marketplace HoeTee/shipwright
```

marketplace を先に追加する。その後でプラグインを入れる。

```bash
claude plugin marketplace add HoeTee/shipwright
claude plugin install shipwright@shipwright
```

セッションの中では、次の 2 つを実行する。

```text
/plugin marketplace add HoeTee/shipwright
/plugin install shipwright@shipwright
```

### Codex

```bash
codex plugin marketplace add HoeTee/shipwright
codex plugin add shipwright@shipwright
```

### OpenCode

次の項目を `opencode.json` に書く。

```json
{
  "skills": ["https://raw.githubusercontent.com/HoeTee/shipwright/main/skills/"]
}
```

末尾のスラッシュを残す。

### 必要なもの

Git が必要である。
HTML レポートには Node.js 20 以降が必要である。
評価スクリプトには Python 3 が必要である。
Skill ファイルは Markdown である。

### 作業を頼む

このプロンプトを送る。

```text
Use shipwright-flow.
The order list groups dates by UTC. Use the store time zone.
You may edit local files and run tests.
Do not push. Do not open a pull request. Do not merge.
```

| エージェント | 開始方法 |
| --- | --- |
| Codex | `$shipwright:shipwright-flow` |
| Claude Code | `/shipwright:shipwright-flow` |
| OpenCode | `@shipwright-flow` |

<p align="center">
  <img src="media/shipwright-workflow.png" alt="作業、計画、構築、レビューと修正、出荷、その後に人のマージ。">
</p>

<p align="center"><em>作業、計画、構築、その後にレビューと修正。妨げがなければ出荷と人のマージへ進む。<a href="media/shipwright-workflow.svg">大きい図</a> · <a href="showcase/shipwright-workflow.html">HTML ガイド</a></em></p>

Shipwright は、1 つのコーディング作業のための skill 集である。
各 skill は 1 つの仕事をする。
[shipwright-flow](../skills/shipwright-flow/SKILL.md) は、目標、段階、範囲、許可した操作を記録する。

計画、コードの変更、実製品での証拠が残る。
マージは人が決める。
[shipwright-land](../skills/shipwright-land/SKILL.md) を許可したときだけ、エージェントはマージする。

## 作業の流れ

上の図が主な経路である。
[HTML ガイド](showcase/shipwright-workflow.html) は各段階を示す。

1. **段階を選ぶ。** [shipwright-flow](../skills/shipwright-flow/SKILL.md) を実行する。目標と許可した操作を記録する。
2. **その段階を行う。** コードを読む、問題を探す、計画を書く、または変更する。
3. **pull request を開く。** [shipwright-ship](../skills/shipwright-ship/SKILL.md) は CI を追う。マージはしない。
4. **レビューには上限がある。** pull request を開いた後、[shipwright-fix](../skills/shipwright-fix/SKILL.md) は AI レビューを 1 回数える。既定の上限は 3 である。開く前の作業は数えない。回数はリセットしない。
5. **人に判断を頼む。** [shipwright-signoff](../skills/shipwright-signoff/SKILL.md) が人向けの資料を用意する。[shipwright-land](../skills/shipwright-land/SKILL.md) は、許可の後にだけマージする。

小さく明確な変更は [shipwright-build](../skills/shipwright-build/SKILL.md) から始めてよい。
監査は、計画を頼むまで監査のままである。

## コア skill

これらはコア skill である。

| Skill | 何をする |
| --- | --- |
| [shipwright-flow](../skills/shipwright-flow/SKILL.md) | 段階、範囲、許可した操作を選ぶ。 |
| [shipwright-plan](../skills/shipwright-plan/SKILL.md) | 新しいエージェントが実行できる計画を書く。 |
| [shipwright-build](../skills/shipwright-build/SKILL.md) | 変更を行い、証拠を持ち帰る。 |
| [shipwright-review](../skills/shipwright-review/SKILL.md) | 確認済みの指摘を報告する。コードは編集しない。 |
| [shipwright-fix](../skills/shipwright-fix/SKILL.md) | 阻止する指摘を直し、レビューの上限を持つ。 |
| [shipwright-ship](../skills/shipwright-ship/SKILL.md) | pull request を開き、CI を追う。 |
| [shipwright-signoff](../skills/shipwright-signoff/SKILL.md) | 人向けの資料を用意する。 |
| [shipwright-land](../skills/shipwright-land/SKILL.md) | 作者以外が検証し、許可の後にマージする。 |

[skill の全一覧](skills.ja.md) に 48 個すべてを書く。

## 例

注文一覧は日付を UTC でまとめる。
店舗は自分のタイムゾーンを使う。
ローカルの編集とテストを許可する。
push、pull request、マージは許可しない。

1. [shipwright-flow](../skills/shipwright-flow/SKILL.md) がその範囲を記録する。
2. [shipwright-diagnose](../skills/shipwright-diagnose/SKILL.md) がバグを再現する。編集はしない。
3. [shipwright-build](../skills/shipwright-build/SKILL.md) が失敗するテストを足し、その後にまとめ方を直す。
4. [shipwright-review](../skills/shipwright-review/SKILL.md) がその commit を確認し、指摘を報告する。

阻止する指摘は [shipwright-fix](../skills/shipwright-fix/SKILL.md) に渡す。
[shipwright-diagnose](../skills/shipwright-diagnose/SKILL.md) は[全一覧](skills.ja.md)にある。

## よくある質問

<details>
<summary>インストールで作業は始まるか。</summary>

インストールは skill を加えるだけである。
新しいセッションが作業を始める。

</details>

<details>
<summary>エージェントはマージするか。</summary>

[shipwright-ship](../skills/shipwright-ship/SKILL.md) は、pull request がマージできる状態で止まる。
[shipwright-land](../skills/shipwright-land/SKILL.md) は、許可の後にだけマージする。

</details>

<details>
<summary>レビューの上限はどこにあるか。</summary>

既定の上限は 3 である。
定義するのは [shipwright-fix](../skills/shipwright-fix/SKILL.md) だけである。
回数は pull request を開いたときに始まる。
開く前の作業は数えない。
沈黙は承認ではない。

</details>

<details>
<summary>証拠はどこに置くか。</summary>

証拠は `/tmp/shipwright-<plan-id>/<short-sha>/` に置く。
保存済みのスクリーンショットは証拠ではない。

</details>

<details>
<summary>Skill の言語は何か。</summary>

Skill の手順は中国語である。
パス、ファイル名、テンプレートの見出しは英語である。

</details>

## 考え方

変更は小さく完全にし、頼まれていない仕事は足さない。

`plans/` の計画は、ノート、コマンド、実行記録、証拠を持つ。

変更は実製品で証明し、保存済みのスクリーンショットは証拠ではない。

AI レビューの既定上限は 3 で、マージは人が決める。

swarm、arena、autopilot、複数 PR の計画は、頼むまでオフである。

## 出典と比較

Shipwright は 4 つの考えを残す。

| 出典 | Shipwright が残すもの |
| --- | --- |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | [shipwright-lean](../skills/shipwright-lean/SKILL.md) と、[shipwright-debt](../skills/shipwright-debt/SKILL.md) の shortcut 台帳 |
| [pstack](https://github.com/cursor/plugins/tree/main/pstack) | 共通の verify の組と prove の組 |
| [improve](https://github.com/shadcn/improve) | [shipwright-audit](../skills/shipwright-audit/SKILL.md) と計画テンプレート |
| [code-review-lifecycle](https://github.com/HoeTee/code-review-lifecycle-skill) | [shipwright-fix](../skills/shipwright-fix/SKILL.md) のレビュー上限と、[shipwright-signoff](../skills/shipwright-signoff/SKILL.md) の人向けの資料 |

Ponytail が公開するのは、Ponytail 自身の測定である。
その数字は Shipwright の結果ではない。

## フィードバックと貢献

問題は [Issues](https://github.com/HoeTee/shipwright/issues) に報告する。
変更は [pull requests](https://github.com/HoeTee/shipwright/pulls) に送る。
Skill を編集する前に [CONTRIBUTING-skills.md](../CONTRIBUTING-skills.md) を読む。

## ライセンス

MIT © HoeTee/shipwright
