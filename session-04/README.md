# 4회차 — AI 기초 이론 (5/16 토, 10:00~13:00)

## 🎯 학습 목표

1. 생성형 AI(LLM)의 작동 원리를 직관적으로 이해한다
2. 프롬프트 엔지니어링, 토큰화, 임베딩, Transformer/GPT 개념을 학습한다
3. 노트북 실습을 통해 ChatGPT/GPT의 기본 원리를 체험한다

## 📊 강의 흐름

| 순서 | 섹션 | 내용 | 시간 |
|------|------|------| ------|
| 1 | AI 개요와 역사 | PPTX로 AI 역사 타임라인, 전통 AI vs 생성형 AI 비교 | 10분
| 2 | 프롬프트 엔지니어링 | `prompt_engineering_guide.ipynb`로 역할, 목표, 맥락, 형식, 제약 실습 | 20분
| 3 | 토크나이저 | `tokenizer_tutorial.ipynb`로 토큰화 방식과 토큰 ID 실습 | 30분
| 4 | 임베딩 | `embedding_guide.ipynb`로 벡터화, 유사도, 미니 검색 엔진 실습 | 30분
| 5 | MicroGPT 미리보기 | `microgpt-preview.ipynb`로 LLM 내부를 들여다보기 전 큰 그림 잡기 | 15분
| 6 | MicroGPT | `microgpt-tutorial.ipynb`로 Transformer/GPT 구조와 학습·추론 실습 | 60분

## 🛠️ 실습 파일

- `prompt_engineering_guide.ipynb` — 프롬프트 엔지니어링 기법 실습
- `tokenizer_tutorial.ipynb` — 토크나이저 개념과 코드 실습
- `embedding_guide.ipynb` — 임베딩, 유사도, 미니 검색 엔진 실습
- `microgpt-preview.ipynb` — MicroGPT 본 실습 전 도입 및 큰 그림 잡기
- `microgpt-tutorial.ipynb` — MicroGPT로 Transformer/GPT 구조 이해

## 🔑 핵심 용어

| 용어 | 설명 |
|------|------|
| LLM | Large Language Model, 대규모 언어 모델 |
| Token | AI가 텍스트를 처리하는 최소 단위 |
| Transformer | 현대 LLM의 핵심 아키텍처 |
| Attention | 문장 내 단어 간 관계를 파악하는 메커니즘 |
| Prompt | AI에게 보내는 입력/지시문 |
| Temperature | 응답의 무작위성 조절 (0=결정적, 1=창의적) |
| Hallucination | AI가 사실이 아닌 내용을 생성하는 현상 |

---

## 📝 숙제: 프롬프트 마스터 챌린지

### 미션

5가지 주제(과학, 수학, 역사, 영어, 일상)에 대해 **"나쁜 프롬프트"** 와 **"좋은 프롬프트"** 를 작성하고, 결과를 비교 분석합니다.

**좋은 프롬프트에 포함할 요소:**
- 역할 부여 (시스템 프롬프트)
- 구체적인 맥락과 제약 조건
- 출력 형식 지정
- 예시(Few-shot) 활용

### 보너스 ⭐

여러 번의 대화를 이어가며 복잡한 문제를 해결하는 **프롬프트 체이닝** 사례 추가

### 제출

- 노션/구글 독스/GitHub에 정리 (스크린샷 포함)
- 다음 수업 전까지 제출 링크 공유
