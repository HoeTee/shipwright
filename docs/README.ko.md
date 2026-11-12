<h1 align="center"><img src="media/shipwright-logo.png" width="64" height="64" alt="Shipwright" valign="middle"> Shipwright</h1>

<p align="center">
  <em>Shipwright는 코딩 작업 하나를 첫 확인에서 사람의 병합 결정까지 진행한다.</em>
</p>

<p align="center">
  <a href="https://github.com/HoeTee/shipwright/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/HoeTee/shipwright/ci.yml?style=flat-square&label=CI" alt="CI"></a>
  <a href="https://github.com/HoeTee/shipwright/releases/tag/v1.0.0"><img src="https://img.shields.io/badge/release-v1.0.0-111111?style=flat-square" alt="릴리스 v1.0.0"></a>
  <a href="../references/platforms.md"><img src="https://img.shields.io/badge/works%20with-Codex%20%C2%B7%20Claude%20Code%20%C2%B7%20OpenCode-111111?style=flat-square" alt="Codex, Claude Code, OpenCode에서 동작"></a>
  <a href="../LICENSE"><img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="MIT 라이선스"></a>
</p>

<p align="center">
  <sub><a href="../README.md">English</a> &middot; <a href="README.zh-CN.md">中文</a> &middot; <a href="README.ja.md">日本語</a></sub>
</p>

<p align="center">
  <img src="media/shipwright-hero.png" width="880" alt="shipwright. 첫 확인에서 사람의 병합까지. Python 줄이 43% 적다.">
</p>

<p align="center">
  <sub>실제 Click 버그 수정 16건. 같은 에이전트가 skill이 있을 때와 없을 때 실행한다. 각 팔 2회. <a href="#실측">실측</a>.</sub>
</p>

<p align="center">
  <img src="media/shipwright-workflow.gif" alt="작업, 계획, 빌드, 그다음 검토와 수정을 통과할 때까지 반복하고, 출고한 뒤 사람이 병합한다.">
</p>

| 하는 일 | Skill | 원칙 |
| --- | --- | --- |
| 작업을 시작한다 | [shipwright-flow](../skills/shipwright-flow/SKILL.md) | 단계와 허용한 작업을 기록한다. |
| 계획을 쓴다 | [shipwright-plan](../skills/shipwright-plan/SKILL.md) | 새 에이전트가 실행할 계획을 쓴다. |
| 변경한다 | [shipwright-build](../skills/shipwright-build/SKILL.md) | 실제 제품에서 증거를 가져온다. |
| 변경을 확인한다 | [shipwright-review](../skills/shipwright-review/SKILL.md) | 발견을 보고한다. 고치지 않는다. |
| 막는 항목을 고친다 | [shipwright-fix](../skills/shipwright-fix/SKILL.md) | AI 검토 한도를 가진다. |
| pull request를 연다 | [shipwright-ship](../skills/shipwright-ship/SKILL.md) | CI를 따라간다. 병합하지 않는다. |
| 꾸러미를 준비한다 | [shipwright-signoff](../skills/shipwright-signoff/SKILL.md) | 사람이 이 꾸러미를 읽는다. |
| 병합한다 | [shipwright-land](../skills/shipwright-land/SKILL.md) | 작성자가 아닌 사람이 확인하고 허용한 뒤에 병합한다. |

[전체 skill 목록](skills.ko.md)에 48개를 모두 적는다.

## 구조

모든 skill 파일의 앞머리는 이 두 칸이다.
아래는 자주 나오는 제목이다.
skill은 필요한 제목만 남긴다.

```
┌────────────────────────────────────────────────────────────────────┐
│ skills/shipwright-*/SKILL.md                                       │
│                                                                    │
│ ┌─ 앞머리 ───────────────────────────────────────────────────────┐ │
│ │ name: shipwright-<skill>                                       │ │
│ │ description: 언제 쓰고, 언제 쓰지 않는가                       │ │
│ └────────────────────────────────────────────────────────────────┘ │
│ # 제목                                                             │
│ When to use       -> 앞의 몇 줄. 제목인 skill도 있다.              │
│ Steps / Procedure -> 이 skill이 하는 일                            │
│ Handoff           -> 다음 단계를 누구에게 넘기는가                 │
│ Stop              -> 이 skill이 하지 않는 일                       │
│                                                                    │
│ references/*.md   -> 대부분 있다. 단계가 이름을 부를 때 읽는다.    │
│ scripts/          -> 일부만 있다. 검사와 도우미.                   │
└────────────────────────────────────────────────────────────────────┘
```

이 저장소의 플러그인 파일:

```
shipwright/
  skills/                         skill 48개. 각각 SKILL.md.
    shipwright-*/references/      보충. 37개 skill에 있다.
    shipwright-*/scripts/         도우미. 18개 skill에 있다.
    plugin.json                   이 폴더를 가리킨다
    index.json                    OpenCode HTTP 카탈로그
  .claude-plugin/plugin.json      Claude Code 플러그인
  .claude-plugin/marketplace.json 마켓 이름
  .codex-plugin/plugin.json       Codex. skills: ./skills/
  docs/                           README와 skill 목록
  eval/results/                   Click 라운드 보고서
  references/                     skill이 공유하는 규칙
```

OpenCode 플러그인 목록 파일은 이 저장소에 없다.
`skills/index.json`이 HTTP 카탈로그다.
`opencode.jsonc`에는 폴더나 그 카탈로그 주소를 적는다.

## 빠른 시작

가장 빠른 설치는 명령 하나이다.
Claude Code 2.1.292 이상이 필요하다.

```bash
claude plugin install shipwright --marketplace HoeTee/shipwright
```

설치 뒤에 새 세션을 연다.
그다음 `/shipwright:shipwright-flow`를 실행한다.

HTML 보고서에는 Node.js 20 이상이 필요하다.
평가 스크립트에는 Python 3이 필요하다.

#### Codex

```bash
codex plugin marketplace add HoeTee/shipwright
codex plugin add shipwright@shipwright
```

새 스레드를 연다.
그다음 `$shipwright:shipwright-flow`를 호출한다.

#### OpenCode

OpenCode는 skill 폴더를 읽는다.
플러그인 목록 파일은 쓰지 않는다.

저장소를 먼저 복제한다.
그다음 폴더를 `~/.config/opencode/opencode.jsonc`에 넣는다.

```bash
git clone https://github.com/HoeTee/shipwright ~/shipwright
```

```jsonc
{
  "skills": ["~/shipwright/skills"]
}
```

또는 `skills/`를 `~/.config/opencode/skills`에 복사하거나 심볼릭 링크로 둔다.
프로젝트에서는 `.opencode/skills`를 같은 방식으로 쓴다.

복제하지 않는 방법도 있다.
HTTP 카탈로그를 가리킨다.
끝의 슬래시를 유지한다.

```jsonc
{
  "skills": ["https://raw.githubusercontent.com/HoeTee/shipwright/main/skills/"]
}
```

카탈로그 파일은 `skills/index.json`이다.
그다음 `@shipwright-flow`를 요청한다.

이 프롬프트를 보낸다.

```text
Use shipwright-flow.
The order list groups dates by UTC. Use the store time zone.
You may edit local files and run tests.
Do not push. Do not open a pull request. Do not merge.
```

## 실측

<p align="center">
  <img src="media/shipwright-evidence.png" width="880" alt="skill 없음을 100%로 둔 비율. Python 줄은 skill 없음 100%, skill 있음 56.6%로 43.4% 적다. 95% 구간은 27.0%에서 57.4% 더 적다.">
</p>

skill이 있으면 Python 줄이 43.4% 적다. 95% 구간은 27.0%에서 57.4% 더 적다.

<p align="center">
  <img src="media/shipwright-evidence-count.png" width="880" alt="16문제 중 14문제에서 Python 줄이 더 적다. 통과율은 같다.">
</p>

16문제 중 14문제에서 줄이 더 적다. 통과율은 같다.

<p align="center">
  <img src="media/shipwright-evidence-tests.png" width="880" alt="diff가 테스트 줄을 바꾼 실행. skill 없음은 32번 중 27번으로 84%. skill 있음은 32번 중 32번으로 100%.">
</p>

diff가 테스트 줄을 바꾼 실행은 skill이 있으면 32번 중 32번, 없으면 32번 중 27번이다.

<p align="center">
  <img src="media/shipwright-evidence-q03.png" width="880" alt="sentinel 한 번. 테스트를 뺀 Python 줄은 skill 없음 17, Shipwright 4. 둘 다 src/click/_utils.py와 sentinel 테스트를 고쳤다. 둘 다 통과. 기록에 diff는 없다.">
</p>

sentinel 한 번: skill이 있으면 Python 4줄, 없으면 17줄. 둘 다 통과했다. 이것은 한 예이다.

방법과 한계는 [보고서](../eval/results/2026-11-round2/report.md)에 있다.

## 자주 묻는 질문

**어떤 에이전트에서 도는가?**
Claude Code, Codex, OpenCode는 같은 skill을 쓴다. 바뀌는 것은 설치 명령과 호출 방식뿐이다.

**어떻게 설치하는가?**
위의 빠른 시작을 쓰고, 그다음 새 세션을 연다. 옛 세션은 시작할 때의 파일을 유지한다.

**skill 48개가 모두 필요한가?**
아니다. shipwright-flow를 호출한다. 표의 여덟 skill이 길을 덮고, 나머지는 필요할 때까지 조용하다.

**검토 반복은 언제 멈추는가?**
검토는 발견을 보고하고 코드를 고치지 않는다. 수정은 Fix가 하고, 한도는 3이며, 횟수는 pull request를 열 때 시작하고, 침묵은 승인이 아니다.

**에이전트가 스스로 병합하는가?**
아니다. Ship는 pull request를 열고 멈춘다. Land는 작성자가 아닌 사람이 확인하고 허용한 뒤에만 병합한다.

**평가는 무엇을 재었는가?**
같은 에이전트가 skill이 있을 때와 없을 때 실제 Click 버그 수정 16건을 다뤘고, 각 팔은 2회 실행했다. skill이 있으면 Python 줄이 43.4% 적고, 통과율은 같으며, 세 번째 반복은 실행하지 않았다.

**어떻게 갱신하는가?**
같은 설치 명령을 다시 실행하고, 새 세션을 연다.

**토큰을 더 쓰는가?**
Shipwright는 토큰 가격을 정하지 않고, 이 평가도 토큰 청구를 재지 않았다. 내는 비용은 호스트의 보통 모델 비용이다.

## 원칙

**계획 먼저. 그다음 잘라.**

코드 건드리기 전에 계획을 써라.
다음 사람은 이 채팅 없이도 그걸 실행할 수 있어야 한다.
그다음, 일을 끝내는 가장 작은 변경만 넣어라.
diff가 작을수록 버그가 적다. 그게 전부다.

**증명해**

돈다고 증명 못 하는 코드는 쓰지 마라.
이 변경에서 명령을 돌리고, 저장한 화면은 증거로 치지 마라.
검토는 구멍만 찾고 코드는 안 고친다.
고치는 건 Fix이고, AI 검토는 3에서 멈춘다.

**병합은 네가 해**

에이전트는 pull request를 열 수 있다.
자기가 병합할 자격은 없다.
코드를 안 쓴 사람이 봐야 한다.
그다음 네가 승낙한다.

**안 잰 수는 꺼내지 마**

재지 않은 걸 우리 성적이라고 하지 마라.
여기 있는 수는 이 프로젝트의 실측이다.
남의 수는 우리 결과가 아니다.
추가 모드는 네가 시키기 전에 켜지 마라.

## 비교

각 행은 그 저장소가 하는 일과, Shipwright가 남기거나 더하는 일을 적는다.

| | 그것이 하는 일 | Shipwright가 남기거나 더하는 것 |
| --- | --- | --- |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | 항상 켜진 프롬프트이다. 작업에 필요한 코드만 쓰고, shortcut 장부를 남긴다. | 가장 작은 완전한 변경과 장부를 남긴다. 계획에서 사람의 병합까지의 길을 더한다. |
| [pstack](https://github.com/cursor/plugins/tree/main/pstack) (poteto) | 매일의 엔지니어링 모드와 playbook이다. 동작을 검증하고, 어려운 성질을 증명할 수 있다. | verify 쌍과 prove 쌍을 남긴다. 병렬과 밤새 모드는 요청할 때까지 꺼 둔다. |
| [improve](https://github.com/shadcn/improve) | 저장소를 감사하고, 다른 에이전트가 실행할 계획을 쓴다. 스스로 구현하지는 않는다. | 감사와 계획 템플릿을 남긴다. 같은 에이전트가 빌드하고, 검토하고, pull request를 열 수도 있다. |
| [code-review-lifecycle](https://github.com/HoeTee/code-review-lifecycle-skill) | 변경을 검토하고, 확인된 결함을 고친 뒤, 사람 앞에서 멈춘다. AI 검토 한도는 3이다. | 그 한도와 사람이 읽는 꾸러미를 남긴다. 검토 전에 계획과 빌드를 더한다. |
| [agent-skills](https://github.com/addyosmani/agent-skills) | 명세에서 출고까지의 수명 주기 명령을 명령 표로 보여 준다. | 이 README는 그 표의 형태를 남긴다. skill과 규칙은 Shipwright 자신의 것이다. |
| Shipwright | 코딩 작업 하나에 길이 하나 있다. | 계획, 빌드, 검토, 수정, 출고, 그다음 사람이 병합한다. 에이전트는 혼자 병합하지 않는다. |

Ponytail이 공개하는 수는 Ponytail 자신의 측정이다. 그 수는 Shipwright의 결과가 아니다.
평가 문제는 [Click](https://github.com/pallets/click)의 실제 버그 수정 16건이다. 그림은 [garden-skills](https://github.com/ConardLi/garden-skills)의 디자인 방법을 쓴다.

## 피드백과 기여

문제는 [Issues](https://github.com/HoeTee/shipwright/issues)에 보고한다.
변경은 [pull requests](https://github.com/HoeTee/shipwright/pulls)로 보낸다.
Skill을 고치기 전에 [CONTRIBUTING-skills.md](../CONTRIBUTING-skills.md)를 읽는다.

## 라이선스

MIT © HoeTee/shipwright
