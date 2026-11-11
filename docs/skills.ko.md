# Skill 목록

[English](skills.md) · [中文](skills.zh-CN.md) · [日本語](skills.ja.md)

[README](README.ko.md)는 주요 경로의 여덟 skill을 보여 준다.
이 페이지는 48개를 모두 적는다.
각 줄은 일 하나이다.

shipwright-autopilot, shipwright-swarm, shipwright-arena, shipwright-eval은 요청할 때까지 꺼 둔다.

## 시작

| Skill | 하는 일 |
| --- | --- |
| [shipwright-flow](../skills/shipwright-flow/SKILL.md) | 단계, 범위, 허용한 작업을 고른다. |
| [shipwright-help](../skills/shipwright-help/SKILL.md) | 카드와 프롬프트를 보여 준다. 작업을 시작하지 않는다. |
| [shipwright-setup](../skills/shipwright-setup/SKILL.md) | 역할별 모델과 Git 호스트를 설정한다. |
| [shipwright-rules](../skills/shipwright-rules/SKILL.md) | 프로젝트 규칙 파일을 초안한다. 동의한 뒤에 기록한다. |

## 이해

| Skill | 하는 일 |
| --- | --- |
| [shipwright-how](../skills/shipwright-how/SKILL.md) | 코드 한 부분이 어떻게 동작하는지 설명한다. |
| [shipwright-why](../skills/shipwright-why/SKILL.md) | 코드가 이런 형태인 이유를 설명한다. |
| [shipwright-teach](../skills/shipwright-teach/SKILL.md) | how와 why를 쉬운 설명 하나로 합친다. |
| [shipwright-recall](../skills/shipwright-recall/SKILL.md) | 이전 진행과 결정을 찾는다. |

## 발견

| Skill | 하는 일 |
| --- | --- |
| [shipwright-audit](../skills/shipwright-audit/SKILL.md) | 저장소나 범위를 감사하고 작업을 순위로 매긴다. |
| [shipwright-roadmap](../skills/shipwright-roadmap/SKILL.md) | 저장소 증거로 다음 기능을 제안한다. |
| [shipwright-diagnose](../skills/shipwright-diagnose/SKILL.md) | 버그를 재현하고 원인을 찾는다. 고치지 않는다. |
| [shipwright-impact](../skills/shipwright-impact/SKILL.md) | 변경이 다른 곳에서 깨뜨릴 수 있는 것을 확인한다. |

## 계획

| Skill | 하는 일 |
| --- | --- |
| [shipwright-plan](../skills/shipwright-plan/SKILL.md) | 새 에이전트가 실행할 계획을 plans/에 쓴다. |
| [shipwright-architect](../skills/shipwright-architect/SKILL.md) | 함수 경계를 넘어 설계한다. 호출자부터 시작한다. |
| [shipwright-prototype](../skills/shipwright-prototype/SKILL.md) | 한 번 쓰는 시제품으로 방법을 비교한다. |

## 빌드

| Skill | 하는 일 |
| --- | --- |
| [shipwright-build](../skills/shipwright-build/SKILL.md) | 변경을 하고 증거를 가져온다. |
| [shipwright-autopilot](../skills/shipwright-autopilot/SKILL.md) | 긴 무인 루프를 진행한다. 병합하지 않는다. |

## 검토

| Skill | 하는 일 |
| --- | --- |
| [shipwright-review](../skills/shipwright-review/SKILL.md) | 한 버전에 대해 확인한 발견을 보고한다. 고치지 않는다. |
| [shipwright-fix](../skills/shipwright-fix/SKILL.md) | 막는 발견을 고친다. AI 검토 한도를 가진다. |
| [shipwright-interrogate](../skills/shipwright-interrogate/SKILL.md) | 맞서는 확인을 쓴다. 각 확인은 실행으로 증명한다. |
| [shipwright-comments](../skills/shipwright-comments/SKILL.md) | 검토 전에 나쁜 주석을 지운다. |

## 출고

| Skill | 하는 일 |
| --- | --- |
| [shipwright-ship](../skills/shipwright-ship/SKILL.md) | pull request를 열고 CI를 따라간다. 병합하지 않는다. |
| [shipwright-signoff](../skills/shipwright-signoff/SKILL.md) | 사람용 꾸러미를 준비한다. |
| [shipwright-land](../skills/shipwright-land/SKILL.md) | 작성자가 아닌 사람이 검증하고 당신이 허용한 뒤에 그 버전을 병합한다. |

## 병합 이후

| Skill | 하는 일 |
| --- | --- |
| [shipwright-deploy](../skills/shipwright-deploy/SKILL.md) | 변경을 배포하고 대상 환경을 확인한다. |
| [shipwright-recover](../skills/shipwright-recover/SKILL.md) | 장애 로그를 읽고 새 수정 pull request를 연다. |
| [shipwright-reconcile](../skills/shipwright-reconcile/SKILL.md) | plans/에서 완료, 막힘, 오래된 계획을 확인한다. |
| [shipwright-debt](../skills/shipwright-debt/SKILL.md) | shortcut 주석을 장부로 모은다. |
| [shipwright-prevent](../skills/shipwright-prevent/SKILL.md) | 반복된 실수가 돌아오지 않도록 구조를 바꾼다. |
| [shipwright-reflect](../skills/shipwright-reflect/SKILL.md) | skill 변경을 제안한다. 동의한 뒤에만 고친다. |
| [shipwright-cleanup](../skills/shipwright-cleanup/SKILL.md) | 확인 뒤에 병합된 worktree와 브랜치를 지운다. |

## 검증

| Skill | 하는 일 |
| --- | --- |
| [shipwright-verify-create](../skills/shipwright-verify-create/SKILL.md) | 실제 제품을 조작하는 프로젝트 skill을 만든다. |
| [shipwright-verify-maintain](../skills/shipwright-verify-maintain/SKILL.md) | 제품이 바뀐 뒤에 그 skill을 갱신한다. |
| [shipwright-prove-create](../skills/shipwright-prove-create/SKILL.md) | 비용이 가장 큰 속성에 형식 증명을 더한다. |
| [shipwright-prove-maintain](../skills/shipwright-prove-maintain/SKILL.md) | 증명한 코드가 바뀐 뒤에 증명을 갱신한다. |

## 분야 지식

| Skill | 하는 일 |
| --- | --- |
| [shipwright-bugs](../skills/shipwright-bugs/SKILL.md) | 작업의 정확성 확인을 적는다. |
| [shipwright-security](../skills/shipwright-security/SKILL.md) | 입력, 권한, 비밀의 확인을 적는다. |
| [shipwright-test](../skills/shipwright-test/SKILL.md) | 동작 테스트 방법과 증거 보관 방법을 적는다. |
| [shipwright-structure](../skills/shipwright-structure/SKILL.md) | 모듈, 계층, 삭제의 확인을 적는다. |
| [shipwright-perf](../skills/shipwright-perf/SKILL.md) | 속도를 바꾸기 전에 측정하는 방법을 적는다. |
| [shipwright-lean](../skills/shipwright-lean/SKILL.md) | 각 변경을 작고 완전하게 유지한다. |

## 추가 도구

| Skill | 하는 일 |
| --- | --- |
| [shipwright-swarm](../skills/shipwright-swarm/SKILL.md) | 병렬 작업자를 실행하고 보고서 하나를 돌려준다. |
| [shipwright-arena](../skills/shipwright-arena/SKILL.md) | 같은 일의 후보를 비교하고 강한 부분을 남긴다. |
| [shipwright-trail](../skills/shipwright-trail/SKILL.md) | 결정 기록을 남기고 다른 모델에 재확인을 맡긴다. |
| [shipwright-recap](../skills/shipwright-recap/SKILL.md) | 각 결과에 대해 HTML 페이지를 그린다. |
| [shipwright-write](../skills/shipwright-write/SKILL.md) | 문서, pull request 글, commit 메시지를 쓴다. |
| [shipwright-skillsmith](../skills/shipwright-skillsmith/SKILL.md) | skill을 쓰거나 고친다. |
| [shipwright-eval](../skills/shipwright-eval/SKILL.md) | 요청할 때만 skill을 측정한다. |
