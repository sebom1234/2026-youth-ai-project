# 7회차 — AI 에이전트 개발 2차 (멀티 에이전트 · 메모리 · RAG)

## 🎯 학습 목표

1. 멀티 에이전트 오케스트레이션(Sequential · Concurrent · GroupChat) 이해
2. 대화 메모리(Session)로 이전 대화를 "기억"하게 만들기
3. RAG(검색 + 생성)로 문서 기반 답변하는 에이전트 구현
4. GitHub Copilot을 활용해 스스로 코드를 완성하는 경험

## 📊 강의 흐름

| 섹션 | 내용 | 시간 |
|------|------|------|
| 복습 브릿지 | 6회차(도구 · 워크플로우 · 임베딩) → 오늘로 잇기 | 3분 |
| 멀티 에이전트 3패턴 | Sequential / Concurrent / GroupChat 개념 + 라이브 데모 | 8분 |
| Session 메모리 | "세션 없이 vs 있이" 비교 데모 | 7분 |
| RAG (오늘의 핵심) | 검색 + 생성, 임베딩, `@tool` — 학교 도우미 데모 | 10분 |
| 과제 안내 | AI 학교 도우미 만들기 + Copilot 사용법 | 2분 |
| 숙제 실습 | `school_helper_template.py` 완성 (Copilot 자기주도) | 60분 |

## 🛠️ 실습 파일

- `session7_main.ipynb` — 강의용 노트북 (멀티 에이전트 3패턴 + Session + RAG 데모)
- `school_helper_template.py` — 숙제 템플릿 (임베딩 RAG + `@tool`, 보너스 Gradio)

> 노트북과 숙제 모두 6회차 꼬맨틀에서 쓴 **임베딩 유사도**로 RAG를 구현합니다. *단어* 대신 *문서*를 검색할 뿐, 원리는 똑같아요.

### ⚙️ 환경 준비 (APIM Foundry Proxy)

```bash
pip install agent-framework-orchestrations agent-framework-openai python-dotenv numpy   # 보너스: gradio
```

프로젝트 폴더에 `.env`를 만들고 접속 정보를 채웁니다.

```env
APIM_ENDPOINT=https://apim-foundryproxy-dev.azure-api.net/foundry/gpt-5.4/
APIM_KEY=<발급받은 키>
EMBEDDING_MODEL=text-embedding-3-small
```

> 인증은 APIM의 **api-key 헤더 방식**입니다. `.env`는 GitHub에 올리지 마세요.

## 📚 참고 레포

[microsoft/Agent-Framework-Samples](https://github.com/microsoft/Agent-Framework-Samples) 폴더 05~07 기반

## 🔑 핵심 개념

| 개념 | 설명 |
|------|------|
| Sequential / Concurrent / GroupChat | 에이전트를 순차 · 병렬 · 토론 방식으로 협업시키는 오케스트레이션 |
| Session | 에이전트가 대화 이력을 기억하게 하는 장치 (`create_session()`) |
| RAG | 외부 문서를 검색해서 LLM 답변에 활용 (오픈북 시험!) |
| Embedding | 텍스트를 숫자 벡터로 변환 (6회차 꼬맨틀에서 이미 사용) |
| `@tool` | 에이전트가 자동으로 호출하는 함수 (검색 도구로 활용) |

---

## 📝 숙제: AI 학교 생활 도우미 (RAG)

### 미션

RAG를 활용해 **우리 학교 정보**를 기반으로 답변하는 AI 도우미를 만드세요.
6회차 꼬맨틀처럼 **임베딩 유사도**로, 이번엔 *단어*가 아니라 *문서*를 검색합니다.

### 핵심 기술: 임베딩 유사도

```python
def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# 질문과 가장 비슷한 문서 Top-3를 찾아 에이전트에게 근거로 준다
q = embed_text(question)
sims = [cosine_similarity(q, embed_text(doc)) for doc in DOCS]
```

### 필수 구현 (기본)

1. 학교 데이터 **10개 이상** 채우기 (시간표 · 급식 · 동아리 · 도서관 · 규정 등)
2. 질문 → 관련 문서 검색(`@tool` + 임베딩 유사도) → 답변 생성
3. 진로 / 학교 질문 **3개 이상** 테스트

### 보너스 ⭐

- 🌐 **Gradio 웹 UI**로 감싸기 (친구들이 브라우저에서 사용!)
- 🧠 **Session** 결합 — 이전 질문 기억하기
- 👥 멀티 에이전트 (학습코치 + 일정관리 + 급식안내)

### 🤖 GitHub Copilot 활용법

- 코드 위에 **원하는 걸 한국어 주석으로** 쓰면 Copilot이 코드를 제안해요.
- 막히면 `Copilot Chat`에 **"이 함수가 왜 에러 나?"**, **"한 줄씩 설명해줘"** 라고 물어보세요.
- 정답을 그대로 받기보다 **제안을 읽고 이해한 뒤 채택**하는 습관을 들이세요.

### 제출

완성한 `school_helper_template.py`와 실행 화면(질문 3개 답변) 캡처.
