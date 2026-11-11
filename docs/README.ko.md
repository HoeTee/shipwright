<div align="center">

[English](../README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · **한국어**

# Shipwright

Codex, Claude Code, OpenCode를 위한 코딩 전 과정 스킬 묶음입니다.

[HoeTee/shipwright](https://github.com/HoeTee/shipwright)

</div>

## 원칙

Shipwright는 코딩의 전 과정을 하나의 플러그인으로 묶습니다. 모든 작업은 하나의 단계에 놓이고, 하나 이상의 영역 태그를 가집니다.

단계 스킬은 절차만 담습니다. 언제 시작하고, 무엇을 넘기고, 어디서 멈추는지입니다. 영역 스킬은 지식만 담습니다. 그 단계에서 무엇을 확인하는가입니다. 단계 스킬은 영역 스킬 안의 같은 단계 절을 읽습니다. 같은 규칙은 한곳에만 씁니다.

다섯 가지 규칙이 이 과정을 하나로 묶습니다.

**가장 작은 완전한 변경.** 요청된 일을 끝까지 합니다. 그 변경이 닿는 호출부와 확인도 포함합니다. 요청되지 않은 것은 넣지 않습니다. 출처는 [Ponytail](https://github.com/DietrichGebert/ponytail)입니다.

**계획은 그 자체로 실행할 수 있는 기록입니다.** 계획은 그 대화를 보지 못한 실행자를 위해 씁니다. 실제 코드 발췌, 명령, 실행 기록, 증거 부록을 담습니다. 끝난 계획은 `plans/`에 남깁니다. 출처는 [improve](https://github.com/shadcn/improve)입니다.

**실제 결과물로 증명합니다.** 보고서는 HTML 페이지입니다. 제품의 동작은 검사한 버전에서 얻은 증거로 보여 줍니다. 캐시된 스크린샷은 증거가 아닙니다. 출처는 [pstack](https://github.com/cursor/plugins/tree/main/pstack)입니다.

**AI 검토에는 상한이 있고, 마지막 판단은 사람이 합니다.** 풀 리퀘스트를 연 뒤의 AI 검토는 매번 셉니다. 기본 상한은 3이고, 정의는 `shipwright-fix`에만 있습니다. 그 커밋에 대한 최종 판단은 사람이 합니다. 침묵은 승인이 아니며, 에이전트가 스스로 병합하지도 않습니다. 출처는 [code-review-lifecycle](https://github.com/HoeTee/code-review-lifecycle-skill)입니다.

**무거운 오케스트레이션은 요청받을 때만 켭니다.** swarm, arena, autopilot, 여러 PR 계획은 누군가 명시적으로 요청하기 전까지 쓰지 않습니다. 보통은 한 단계씩 진행합니다.

## 핵심 흐름

## 왜 초점 있는 스킬 플러그인인가

## 비교

## 설치

## 빠른 시작

## 자주 묻는 질문

## 저장소 안내

## 라이선스
