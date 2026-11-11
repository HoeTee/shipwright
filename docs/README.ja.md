<div align="center">

[English](../README.md) · [简体中文](README.zh-CN.md) · **日本語** · [한국어](README.ko.md)

# Shipwright

Codex、Claude Code、OpenCode 向けの、コーディング全工程のスキル集。

[HoeTee/shipwright](https://github.com/HoeTee/shipwright)

</div>

## 考え方

Shipwright は、コーディングのライフサイクル全体を一つのプラグインにまとめたものです。作業は一つの段階に置き、一つ以上の領域タグを付けます。

段階の skill が持つのは手順だけです。いつ始め、何を引き渡し、どこで止まるか。領域の skill が持つのは知識だけです。その段階で何を確認するか。段階の skill は、領域の skill にある同じ段階の節を読みます。同じ規則は一箇所に書きます。

五つの規則が、このライフサイクルを一つに結びます。

**最小で完全な変更。** 頼まれた仕事は最後までやる。影響する呼び出し元と確認も含む。頼まれていないものは足さない。出典は [Ponytail](https://github.com/DietrichGebert/ponytail)。

**計画は単体で実行できる記録。** 計画は、その会話を見ていない実行者のために書く。実際のコード抜粋、コマンド、実行記録、証拠の付録を入れる。終わった計画は `plans/` に残す。出典は [improve](https://github.com/shadcn/improve)。

**本物の成果物で証明する。** 報告は HTML ページ。製品の挙動は、検査した版で取った証拠で示す。キャッシュされたスクリーンショットは証拠にしない。出典は [pstack](https://github.com/cursor/plugins/tree/main/pstack)。

**AI のレビューには上限があり、最終判断は人が行う。** プルリクエストを開いた後、AI のレビューは毎回数える。既定の上限は 3 で、定義は `shipwright-fix` だけにある。そのコミットの最終判断は人が行う。沈黙は承認ではなく、エージェントが自分でマージすることもない。出典は [code-review-lifecycle](https://github.com/HoeTee/code-review-lifecycle-skill)。

**重い編成は頼まれたときだけ使う。** swarm、arena、autopilot、複数 PR の計画は、明示的に頼まれるまで使わない。通常は一段階ずつ進む。

## 中心の流れ

## なぜ焦点を絞った skill のプラグインなのか

## 比較

## インストール

## クイックスタート

## よくある質問

## リポジトリガイド

## ライセンス
