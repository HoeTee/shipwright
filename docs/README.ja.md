<h1 align="center">Shipwright</h1>

<p align="center">
  <em>Shipwright は、1 つのコーディング作業を最初の確認から人のマージ判断まで進める。</em>
</p>

<p align="center">
  <a href="https://github.com/HoeTee/shipwright/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/HoeTee/shipwright/ci.yml?style=flat-square&label=CI" alt="CI"></a>
  <a href="https://github.com/HoeTee/shipwright/releases/tag/v1.0.0"><img src="https://img.shields.io/badge/release-v1.0.0-111111?style=flat-square" alt="リリース v1.0.0"></a>
  <a href="../references/platforms.md"><img src="https://img.shields.io/badge/works%20with-Codex%20%C2%B7%20Claude%20Code%20%C2%B7%20OpenCode-111111?style=flat-square" alt="Codex、Claude Code、OpenCode で動く"></a>
  <a href="../LICENSE"><img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="MIT ライセンス"></a>
</p>

<p align="center">
  <sub><a href="../README.md">English</a> &middot; <a href="README.zh-CN.md">中文</a> &middot; <a href="README.ko.md">한국어</a></sub>
</p>

<p align="center">
  <img src="media/shipwright-hero.png" width="880" alt="Python の行は 43% 少ない。隠しテストは skill ありで 30/32、skill なしでも 30/32。">
</p>

<p align="center">
  <strong>Python の行は 43% 少ない。隠しテストは skill あり 30/32、skill なし 30/32。</strong><br>
  <sub>実在する Click のバグ修正 16 件。同じエージェントが skill ありと skill なしで動く。各腕 2 回。<a href="#数値">数値</a>。</sub>
</p>

<p align="center">
  <img src="media/shipwright-workflow.png" alt="作業、計画、構築、レビューと修正、出荷、その後に人のマージ。">
</p>

| していること | Skill | 原則 |
| --- | --- | --- |
| 作業を始める | [shipwright-flow](../skills/shipwright-flow/SKILL.md) | 段階と許可した操作を記録する。 |
| 計画を書く | [shipwright-plan](../skills/shipwright-plan/SKILL.md) | 新しいエージェントが実行できる計画を書く。 |
| 変更する | [shipwright-build](../skills/shipwright-build/SKILL.md) | 実製品から証拠を持ち帰る。 |
| 変更を確認する | [shipwright-review](../skills/shipwright-review/SKILL.md) | 指摘を報告する。編集しない。 |
| 阻止項目を直す | [shipwright-fix](../skills/shipwright-fix/SKILL.md) | AI レビューの上限を持つ。 |
| pull request を開く | [shipwright-ship](../skills/shipwright-ship/SKILL.md) | CI を追う。マージしない。 |
| 資料を用意する | [shipwright-signoff](../skills/shipwright-signoff/SKILL.md) | 人がこの資料を読む。 |
| マージする | [shipwright-land](../skills/shipwright-land/SKILL.md) | 作者以外が確認し、許可の後にマージする。 |

[skill の全一覧](skills.ja.md) に 48 個すべてを書く。

## クイックスタート

最も速い導入は 1 つのコマンドである。
Claude Code 2.1.292 以降が必要である。

```bash
claude plugin install shipwright --marketplace HoeTee/shipwright
```

HTML レポートには Node.js 20 以降が必要である。
評価スクリプトには Python 3 が必要である。

<details>
<summary>Claude Code</summary>

導入の後、新しいセッションを開く。
その後 `/shipwright:shipwright-flow` を実行する。

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add HoeTee/shipwright
codex plugin add shipwright@shipwright
```

新しいスレッドを開く。
その後 `$shipwright:shipwright-flow` を呼ぶ。

</details>

<details>
<summary>OpenCode</summary>

次の項目を `opencode.json` に書く。
末尾のスラッシュを残す。

```json
{
  "skills": ["https://raw.githubusercontent.com/HoeTee/shipwright/main/skills/"]
}
```

その後 `@shipwright-flow` を頼む。

</details>

このプロンプトを送る。

```text
Use shipwright-flow.
The order list groups dates by UTC. Use the store time zone.
You may edit local files and run tests.
Do not push. Do not open a pull request. Do not merge.
```

## 数値

<p align="center">
  <img src="../eval/results/2026-11-round2/chart.png" width="880" alt="Click 第 2 回。skill なしは 100。skill ありは 56.6。隠しテストは両腕とも 30/32。">
</p>

skill ありは、同じエージェントの skill なしより Python の行が 43% 少ない。
隠しテストは両腕とも 32 回中 30 回通った。通過率は同じである。
95% 区間は 27% から 57% 少ない。[報告](../eval/results/2026-11-round2/report.md) に方法と限界を書く。

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
