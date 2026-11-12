<h1 align="center"><img src="media/shipwright-logo.png" width="64" height="64" alt="Shipwright" valign="middle"> Shipwright</h1>

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
  <img src="media/shipwright-hero.png" width="880" alt="shipwright。最初の確認から人のマージまで。Python の行は 43% 少ない。">
</p>

<p align="center">
  <sub>実在する Click のバグ修正 16 件。同じエージェントが skill ありと skill なしで動く。各腕 2 回。<a href="#実測">実測</a>。</sub>
</p>

<p align="center">
  <img src="media/shipwright-workflow.gif" alt="作業、計画、構築、その後レビューと修正をクリアまで繰り返し、出荷して人がマージする。">
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

導入の後、新しいセッションを開く。
その後 `/shipwright:shipwright-flow` を実行する。

HTML レポートには Node.js 20 以降が必要である。
評価スクリプトには Python 3 が必要である。

#### Codex

```bash
codex plugin marketplace add HoeTee/shipwright
codex plugin add shipwright@shipwright
```

新しいスレッドを開く。
その後 `$shipwright:shipwright-flow` を呼ぶ。

#### OpenCode

次の項目を `opencode.json` に書く。
末尾のスラッシュを残す。

```json
{
  "skills": ["https://raw.githubusercontent.com/HoeTee/shipwright/main/skills/"]
}
```

その後 `@shipwright-flow` を頼む。

このプロンプトを送る。

```text
Use shipwright-flow.
The order list groups dates by UTC. Use the store time zone.
You may edit local files and run tests.
Do not push. Do not open a pull request. Do not merge.
```

## 実測

<p align="center">
  <img src="media/shipwright-evidence.png" width="880" alt="Python の行。skill なしは 100。skill ありは 56.6。通過率は同じ。">
</p>

skill ありは、同じエージェントの skill なしより Python の行が 43% 少ない。
通過率は同じである。
95% 区間は 27% から 57% 少ない。[報告](../eval/results/2026-11-round2/report.md) に方法と限界を書く。

## よくある質問

<details>
<summary><h3>どのエージェントで動くか。</h3></summary>

Shipwright は Claude Code、Codex、OpenCode で動く。
同じ skill が各ホストに読み込まれる。
変わるのは、導入コマンドと呼び出し方だけである。

</details>

<details>
<summary><h3>どう導入するか。</h3></summary>

上のクイックスタートを使う。
Claude Code はコマンド 1 つで足りる。
Codex と OpenCode は、それぞれの見出しの手順を使う。
導入の後、新しいセッションを開く。

</details>

<details>
<summary><h3>48 個の skill がすべて必要か。</h3></summary>

必要ではない。
[shipwright-flow](../skills/shipwright-flow/SKILL.md) を呼び、段階を選ばせる。
上の表の 8 個が、計画からマージまでの道を覆う。
他の skill は、その段階が必要とするまで静かである。

</details>

<details>
<summary><h3>レビューの繰り返しはいつ止まるか。</h3></summary>

[shipwright-review](../skills/shipwright-review/SKILL.md) は指摘を報告し、コードを編集しない。
[shipwright-fix](../skills/shipwright-fix/SKILL.md) が修正し、AI レビューの上限は 3 である。
回数は pull request を開いたときに始まる。
沈黙は承認ではなく、マージは人が決める。

</details>

<details>
<summary><h3>エージェントは自分でマージするか。</h3></summary>

しない。
[shipwright-ship](../skills/shipwright-ship/SKILL.md) は pull request を開いて止まる。
[shipwright-land](../skills/shipwright-land/SKILL.md) は、作者以外が確認し、許可のあとだけマージする。

</details>

<details>
<summary><h3>評価は何を測ったか。</h3></summary>

同じエージェントが、skill ありと skill なしで、実在する Click のバグ修正 16 件を扱った。
各腕は 2 回動いた。
skill ありは Python の行が 43% 少なく、通過率は同じである。
3 回目、より難しい題、盲検の判定は走っていない。

</details>

<details>
<summary><h3>どう更新するか。</h3></summary>

同じ導入コマンドをもう一度実行する。
その後、新しいセッションを開き、ホストに新しいファイルを読ませる。
古いセッションは、開始時のファイルのままである。

</details>

<details>
<summary><h3>トークンを余分に使うか。</h3></summary>

Shipwright はトークンの価格を定めない。
この評価は金額もトークンの請求も測っていない。
より小さい差分はトークンを減らせるかもしれないが、約束ではない。
支払うのは、ホストの通常のモデル費用である。

</details>

## 考え方

**コードの前に計画を書く**

製品を変える前に、計画を書く。
後のエージェントは、この会話なしでその計画を実行できなければならない。
計画は、メモ、コマンド、実行、証拠を記録する。
[shipwright-flow](../skills/shipwright-flow/SKILL.md) が段階を記録し、[shipwright-plan](../skills/shipwright-plan/SKILL.md) が計画を `plans/` に書く。

**最小で完全な変更**

仕事を完全に終える最小の変更だけをする。
頼まれていない仕事は足さない。
より小さい差分は、レビューしやすく、戻しやすい。
コードを書く間、[shipwright-lean](../skills/shipwright-lean/SKILL.md) は止めるまでオンである。

**完了の前に証拠を出す**

実製品で証明するまで、変更は完了ではない。
保存済みのスクリーンショットは証拠ではない。
証拠は、この変更で実行したコマンドから来なければならない。
[shipwright-build](../skills/shipwright-build/SKILL.md) は証拠を `/tmp/shipwright-<plan-id>/<short-sha>/` に置く。

**レビューしてから直す**

[shipwright-review](../skills/shipwright-review/SKILL.md) は指摘を報告し、コードを編集しない。
各指摘は、実際の害に基づいて P0、P1、P2 のいずれかである。P0 と P1 は既定で止める。
実害のないメモは P2 ではない。
[shipwright-fix](../skills/shipwright-fix/SKILL.md) が修正を行い、AI レビューの上限は 3 である。

**人がマージする**

マージは人が決める。
エージェントは pull request を開いてよいが、単独ではマージしない。
[shipwright-ship](../skills/shipwright-ship/SKILL.md) はマージの前に止まり、[shipwright-signoff](../skills/shipwright-signoff/SKILL.md) は人が読む資料を書く。
[shipwright-land](../skills/shipwright-land/SKILL.md) は、作者以外が確認し、許可のあとだけマージする。

**実測する**

実際の比較で測った改善だけを書いてよい。
[shipwright-eval](../skills/shipwright-eval/SKILL.md) は、同じエージェントを skill ありと skill なしで動かす。
日常の小さな変更では、この比較を走らせない。
他のプロジェクトの数字は Shipwright の結果ではない。

**追加モードはオフ**

swarm、arena、autopilot、複数 PR の計画は、頼むまでオフである。
それらは、頼んでいない並列作業か長い実行を足す。
その作業を名指しするまで、[shipwright-flow](../skills/shipwright-flow/SKILL.md) はそれらを始めない。
通常の作業は、1 つの変更と 1 つの pull request にとどまる。

## 出典と比較

Shipwright はこれらの考えを残す。

| 出典 | Shipwright が残すもの |
| --- | --- |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | [shipwright-lean](../skills/shipwright-lean/SKILL.md) は最小で完全な変更を残し、[shipwright-debt](../skills/shipwright-debt/SKILL.md) は shortcut 台帳を残す |
| [pstack](https://github.com/cursor/plugins/tree/main/pstack)（poteto） | 共通の verify の組と prove の組 |
| [improve](https://github.com/shadcn/improve) | [shipwright-audit](../skills/shipwright-audit/SKILL.md) と計画テンプレート |
| [code-review-lifecycle](https://github.com/HoeTee/code-review-lifecycle-skill) | [shipwright-fix](../skills/shipwright-fix/SKILL.md) のレビュー上限と、[shipwright-signoff](../skills/shipwright-signoff/SKILL.md) の人向けの資料 |
| [agent-skills](https://github.com/addyosmani/agent-skills) | この README の形。コマンド表を含む |
| [garden-skills](https://github.com/ConardLi/garden-skills) | ヒーロー、流れ、実測図のデザイン方法 |
| [Click](https://github.com/pallets/click) | 評価の問題に使った、実在するバグ修正 16 件 |

Ponytail が公開するのは、Ponytail 自身の測定である。
その数字は Shipwright の結果ではない。

## フィードバックと貢献

問題は [Issues](https://github.com/HoeTee/shipwright/issues) に報告する。
変更は [pull requests](https://github.com/HoeTee/shipwright/pulls) に送る。
Skill を編集する前に [CONTRIBUTING-skills.md](../CONTRIBUTING-skills.md) を読む。

## ライセンス

MIT © HoeTee/shipwright
