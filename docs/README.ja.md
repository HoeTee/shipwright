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

[skill の全一覧](skills.ja.md) に 49 個すべてを書く。

## 構造

どの skill ファイルも、先頭の欄はこの 2 つだ。
下はよく出る見出しだ。
skill は必要な見出しだけを残す。

```
┌────────────────────────────────────────────────────────────────────┐
│ skills/shipwright-*/SKILL.md                                       │
│                                                                    │
│ ┌─ 先頭の欄 ─────────────────────────────────────────────────────┐ │
│ │ name: shipwright-<skill>                                       │ │
│ │ description: いつ使うか、いつ使わないか                        │ │
│ └────────────────────────────────────────────────────────────────┘ │
│ # タイトル                                                         │
│ When to use       -> 冒頭の数行。見出しの skill もある。           │
│ Steps / Procedure -> この skill がやる仕事                         │
│ Handoff           -> 次の段階を誰に渡すか                          │
│ Stop              -> この skill がやらないこと                     │
│                                                                    │
│ references/*.md   -> 多くの skill にある。手順が名指しする。       │
│ scripts/          -> 一部の skill にある。検査と補助。             │
└────────────────────────────────────────────────────────────────────┘
```

このリポジトリにあるプラグインのファイル：

```
shipwright/
  skills/                         skill 49 個。各 SKILL.md。
    shipwright-*/references/      補足。38 skill にある。
    shipwright-*/scripts/         補助スクリプト。18 skill にある。
    plugin.json                   このフォルダを指す
    index.json                    OpenCode の HTTP カタログ
  .claude-plugin/plugin.json      Claude Code プラグイン
  .claude-plugin/marketplace.json マーケット名
  .codex-plugin/plugin.json       Codex。skills: ./skills/
  docs/                           README と skill 一覧
  eval/results/                   Click のラウンド報告
  references/                     skill が共有する規則
```

OpenCode のプラグインマニフェストは、このリポジトリにはない。
`skills/index.json` が HTTP カタログだ。
`opencode.jsonc` には、フォルダかそのカタログ URL を書く。

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

OpenCode は skill フォルダを読む。
プラグインマニフェストは使わない。

まずリポジトリをクローンする。
その後、フォルダを `~/.config/opencode/opencode.jsonc` に足す。

```bash
git clone https://github.com/HoeTee/shipwright ~/shipwright
```

```jsonc
{
  "skills": ["~/shipwright/skills"]
}
```

または `skills/` を `~/.config/opencode/skills` にコピーかシンボリックリンクする。
プロジェクトでは `.opencode/skills` を同じように使える。

クローンしない方法もある。
HTTP カタログを指す。
末尾のスラッシュを残す。

```jsonc
{
  "skills": ["https://raw.githubusercontent.com/HoeTee/shipwright/main/skills/"]
}
```

カタログファイルは `skills/index.json` だ。
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
  <img src="media/shipwright-evidence.png" width="880" alt="skill なしを 100% とした割合。Python の行は skill なし 100%、skill あり 56.6% で 43.4% 少ない。95% 区間は 27.0% から 57.4% 少ない。">
</p>

skill ありは Python の行が 43.4% 少ない。95% 区間は 27.0% から 57.4% 少ない。

<p align="center">
  <img src="media/shipwright-evidence-count.png" width="880" alt="16 問中 14 問で Python の行が少ない。通過率は同じ。">
</p>

16 問中 14 問で行が少ない。通過率は同じである。

<p align="center">
  <img src="media/shipwright-evidence-tests.png" width="880" alt="diff がテスト行を変えた実行。skill なしは 32 回中 27 回で 84%。skill ありは 32 回中 32 回で 100%。">
</p>

diff がテスト行を変えたのは、skill あり 32 回中 32 回、skill なし 32 回中 27 回である。

<p align="center">
  <img src="media/shipwright-evidence-q03.png" width="880" alt="sentinel の 1 回。テストを除いた Python 行は skill なし 17、Shipwright 4。どちらも src/click/_utils.py と sentinel テストを編集。どちらも通過。記録に diff はない。">
</p>

sentinel の 1 回：skill ありは Python 4 行、skill なしは 17 行。どちらも通過した。これは 1 例である。

方法と限界は[報告](../eval/results/2026-11-round2/report.md)。

## よくある質問

- **どのエージェントで動くか。** Claude Code、Codex、OpenCode は同じ skill を使う。変わるのは導入コマンドと呼び出し方だけである。
- **どう導入するか。** 上のクイックスタートを使い、その後に新しいセッションを開く。古いセッションは開始時のファイルのままである。
- **49 個の skill がすべて必要か。** 必要ではない。shipwright-flow を呼ぶ。表の 8 個が道を覆い、残りは必要になるまで静かである。
- **レビューの繰り返しはいつ止まるか。** レビューは指摘を報告し、コードを編集しない。修正は Fix が行い、上限は 3 で、回数は pull request を開いたときに始まり、沈黙は承認ではない。
- **エージェントは自分でマージするか。** しない。Ship は pull request を開いて止まる。Land は、作者以外が確認し、許可のあとだけマージする。
- **評価は何を測ったか。** 同じエージェントが skill ありと skill なしで、実在する Click のバグ修正 16 件を扱い、各腕は 2 回動いた。skill ありは Python の行が 43.4% 少なく、通過率は同じで、3 回目は走っていない。
- **どう更新するか。** 同じ導入コマンドをもう一度実行し、新しいセッションを開く。
- **トークンを余分に使うか。** Shipwright はトークンの価格を定めず、この評価はトークンの請求も測っていない。支払うのはホストの通常のモデル費用である。

## 考え方

**計画して、余計なものは削れ**

コードに触る前に計画を書け。
次の人は、このチャットなしでそれを実行できなきゃいけない。
そのあと、仕事が終わる最小の変更だけ入れろ。
差分が小さいほどバグは少ない。それだけだ。

**証明しろ**

動くと証明できないコードは書くな。
この変更でコマンドを回し、保存した画面は証拠にするな。
レビューは穴を見つけて、コードは直さない。
直しは Fix の仕事で、AI レビューは 3 で止まる。

**マージは君がやれ**

エージェントは pull request を開いていい。
自分でマージする資格はない。
コードを書いていない人が見る。
そのあと、君がイエスと言う。

**測ってない数字を出すな**

測っていないことは、うちの結果だと言うな。
ここにある数字は、このプロジェクトの実測だ。
よその数字は、うちの結果じゃない。
追加モードは、頼まれるまで切っておけ。

## 比較

各行は、そのリポジトリから得られる結果と、Shipwright から得られる結果を書く。

| | それから得られるもの | Shipwright から得られるもの |
| --- | --- | --- |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | エージェントはタスクに必要なコードだけを書く。後回しにした shortcut は台帳に集まる。 | その最小の変更と台帳が得られる。タスクは計画から、人がマージする pull request まで進む。 |
| [pstack](https://github.com/cursor/plugins/tree/main/pstack)（poteto） | 日常モードが playbook でタスクを進める。製品を検査し、難しい性質を 1 つ証明できる。エージェントを並列に走らせることも、夜間にマージまで進めることもできる。 | 製品の検査と、難しい性質の証明は、ここでもできる。並列と夜間は頼むまでオフである。夜間の実行は自分ではマージしない。 |
| [improve](https://github.com/shadcn/improve) | 監査と計画が得られる。より安いエージェントがその計画を実装できる。この skill は製品コードを編集しない。マージは人が行う。 | 同じタスクはコードの変更、レビュー、開いた pull request まで続く。人がマージする。 |
| [code-review-lifecycle](https://github.com/HoeTee/code-review-lifecycle-skill) | 変更をレビューし、確認された欠陥を直し、人の判断を待って止まる。AI レビューは 3 ラウンドで止まる。 | AI レビューはやはり 3 で止まる。決定はやはり人が行う。レビューの前に、計画と構築もある。 |
| [agent-skills](https://github.com/addyosmani/agent-skills) | コマンドはタスクを仕様から、コード、テスト、レビュー、本番公開前の確認まで進める。計画を一度承認すると、各タスクを構築し、テストし、コミットし、失敗または危険な手順で一時停止する。 | 1 つの道が、そのタスクを計画から変更、レビュー、開いた pull request まで進める。マージを決めるのは人である。 |

Ponytail が公開するのは、Ponytail 自身の測定である。その数字は Shipwright の結果ではない。
評価の問題は [Click](https://github.com/pallets/click) の実在するバグ修正 16 件である。画像は [garden-skills](https://github.com/ConardLi/garden-skills) のデザイン方法を使う。

## フィードバックと貢献

問題は [Issues](https://github.com/HoeTee/shipwright/issues) に報告する。
変更は [pull requests](https://github.com/HoeTee/shipwright/pulls) に送る。
Skill を編集する前に [CONTRIBUTING-skills.md](../CONTRIBUTING-skills.md) を読む。

## ライセンス

MIT © HoeTee/shipwright
