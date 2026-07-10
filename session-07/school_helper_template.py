"""
🏫 AI 학교 생활 도우미 — 숙제 템플릿 (7회차)
================================================================
RAG(검색 + 생성)로 '우리 학교 정보'를 기반으로 답변하는 AI 도우미를 만듭니다.

🔗 6회차 연결: 꼬맨틀에서 임베딩으로 '단어 유사도'를 쟀죠?
   이번엔 같은 임베딩으로 '질문 ↔ 문서 유사도'를 재서 문서를 검색합니다. (= RAG)

🤖 GitHub Copilot 사용법:
   - `# TODO` 와 `???` 부분을 Copilot의 제안을 받아 채우세요.
   - 각 단계 주석에 'Copilot에게 이렇게 시켜보세요' 예시가 있습니다.
   - 제안을 그대로 쓰지 말고, 읽고 이해한 뒤 채택하세요!

실행: python school_helper_template.py
필요 패키지: agent-framework-openai, python-dotenv, numpy  (보너스: gradio)
================================================================
"""
import os
import asyncio
import sys
import numpy as np
from dotenv import load_dotenv, find_dotenv

# MAF (6회차에서 쓴 것과 동일) — APIM Foundry Proxy로 연결
from agent_framework import Agent, tool
from agent_framework.openai import OpenAIChatClient, OpenAIEmbeddingClient

load_dotenv(find_dotenv(usecwd=True), override=True)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ── 환경 설정 (APIM Foundry Proxy) ──────────────────────────
# .env 파일에 아래 값을 채우세요.
#   APIM_ENDPOINT=https://apim-foundryproxy-dev.azure-api.net/foundry/gpt-5.4/
#   APIM_KEY=<키>
#   EMBEDDING_MODEL=text-embedding-3-small
#
# APIM_ENDPOINT는 채팅 모델 엔드포인트입니다.
# 임베딩 엔드포인트는 기본적으로 같은 /foundry/ 아래의 EMBEDDING_MODEL로 자동 구성합니다.
def with_trailing_slash(url: str) -> str:
    return url.rstrip("/") + "/"


APIM_CHAT_ENDPOINT = with_trailing_slash(os.environ["APIM_ENDPOINT"])
APIM_KEY = os.environ["APIM_KEY"]
CHAT_MODEL = os.getenv("CHAT_MODEL") or APIM_CHAT_ENDPOINT.rstrip("/").split("/")[-1]
EMBED_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

DEFAULT_EMBED_ENDPOINT = APIM_CHAT_ENDPOINT.rstrip("/").rsplit("/", 1)[0] + f"/{EMBED_MODEL}/"
APIM_EMBEDDING_ENDPOINT = with_trailing_slash(
    os.getenv("APIM_EMBEDDING_ENDPOINT", DEFAULT_EMBED_ENDPOINT)
)

# 대화용 클라이언트 (MAF) — APIM은 api-key 헤더로 인증
chat_client = OpenAIChatClient(
    model=CHAT_MODEL,
    base_url=APIM_CHAT_ENDPOINT,
    api_key="placeholder",
    default_headers={"api-key": APIM_KEY},
)

# 임베딩용 클라이언트 (MAF) — 같은 APIM 프록시의 임베딩 모델 엔드포인트 사용
embed_client = OpenAIEmbeddingClient(
    model=EMBED_MODEL,
    base_url=APIM_EMBEDDING_ENDPOINT,
    api_key="placeholder",
    default_headers={"api-key": APIM_KEY},
)

# ================================================================
# 1️⃣ [필수] 우리 학교 데이터 채우기 — 최소 10개 이상!
# ================================================================
# 💡 Copilot에게 이렇게 시켜보세요:
#    "아래 리스트 형식에 맞춰서 고등학교 동아리/급식/도서관/시험 정보 8개를 더 만들어줘"
SCHOOL_NAME = "OO고등학교"   # TODO: 우리 학교 이름으로 바꾸기
SCHOOL_DATA = [
    {"cat": "급식",   "content": "월요일 점심 급식은 제육볶음, 미역국, 김치, 요구르트입니다."},
    {"cat": "동아리", "content": "코딩 동아리는 매주 수요일 방과 후 4시에 3층 컴퓨터실에서 모입니다."},
    # TODO: 여기에 8개 이상 더 추가! (시간표, 도서관, 규정, 상담, 방과후 등)
]

# ================================================================
# 2️⃣ [필수] 임베딩으로 지식베이스 인덱싱
# ================================================================
async def aembed_text(text: str) -> np.ndarray:
    """텍스트 한 개를 임베딩 벡터(숫자 배열)로 변환한다.
    💡 Copilot: "embed_client.get_embeddings로 임베딩을 만들고 첫 벡터를 np.array로 반환해줘"
    ⚠️ MAF 임베딩은 비동기라서 await 가 필요합니다. (그래서 이 함수도 async)"""
    result = await embed_client.get_embeddings([text])
    return np.array(result[0].vector)

# 학교 데이터를 미리 벡터로 만들어 둘 곳 (main에서 준비)
DOC_VECTORS: np.ndarray | None = None

async def build_index() -> None:
    """모든 학교 데이터를 임베딩해서 DOC_VECTORS에 저장 (검색 속도 ↑)."""
    global DOC_VECTORS
    # 💡 Copilot: "SCHOOL_DATA의 각 content를 aembed_text로 임베딩해서 np.array로 쌓아줘"
    vectors = [await aembed_text(d["content"]) for d in SCHOOL_DATA]
    DOC_VECTORS = np.array(vectors)

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """두 벡터의 코사인 유사도 (6회차 꼬맨틀과 똑같은 공식!)."""
    # 💡 Copilot: "두 numpy 벡터의 코사인 유사도를 구해줘 (내적 / 노름 곱)"
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

# ================================================================
# 3️⃣ [필수] @tool 검색 함수 — 질문과 가장 비슷한 문서 Top-3 찾기
# ================================================================
@tool(approval_mode="never_require")   # 에이전트가 자동으로 호출
async def search_school_info(query: str) -> str:
    """학교의 급식, 시간표, 동아리, 도서관, 규정 등 정보를 검색합니다.

    Args:
        query: 학생이 궁금해하는 내용 (한국어)
    Returns:
        가장 관련 있는 학교 정보 문서들
    """
    if DOC_VECTORS is None:
        raise RuntimeError("검색 인덱스가 아직 준비되지 않았습니다. 먼저 build_index()를 실행하세요.")

    # (1) 질문을 벡터로
    q_vec = await aembed_text(query)
    # (2) 모든 문서와 유사도 계산
    #     💡 Copilot: "q_vec과 DOC_VECTORS의 각 행을 cosine_similarity로 비교해 리스트로 만들어줘"
    sims = [cosine_similarity(q_vec, doc_vec) for doc_vec in DOC_VECTORS]
    # (3) 유사도 높은 순 Top-3
    top_idx = np.argsort(sims)[::-1][:3]
    parts = [
        f"[{SCHOOL_DATA[i]['cat']}] (관련도 {sims[i]:.2f}) {SCHOOL_DATA[i]['content']}"
        for i in top_idx
    ]
    return "\n".join(parts)

# ================================================================
# 4️⃣ [필수] RAG 에이전트 만들기
# ================================================================
helper_agent = Agent(
    client=chat_client,
    name="학교도우미",
    instructions=f"""당신은 {SCHOOL_NAME}의 친절한 AI 생활 도우미입니다.
학생 질문에 답할 때 반드시 search_school_info 도구로 학교 정보를 검색하세요.
검색된 문서에 근거해서만 답하고, 없는 정보는 '학교에 문의해 주세요'라고 안내하세요.""",
    tools=[search_school_info],   # 3번에서 만든 @tool 등록
)

# ================================================================
# 5️⃣ [필수] 테스트 — 질문 3개 이상!
# ================================================================
async def main():
    await build_index()   # 먼저 학교 데이터를 임베딩(인덱싱)
    print(f"🏫 {SCHOOL_NAME} AI 도우미 (문서 {len(SCHOOL_DATA)}개 로드)\n")
    questions = [
        "오늘 급식 뭐야?",
        "코딩 동아리는 언제 모여?",
        # TODO: 질문 1개 이상 더 추가!
    ]
    for q in questions:
        print(f"👤 학생: {q}")
        resp = await helper_agent.run(q)
        print(f"🤖 도우미: {resp.text}\n")

if __name__ == "__main__":
    asyncio.run(main())


# ================================================================
# 🌟 보너스 1: Gradio 웹 UI  (친구들이 브라우저에서 사용!)
# ================================================================
# 아래 주석을 풀고 위 `if __name__` 블록 대신 실행하세요.
# 💡 Copilot: "helper_agent를 gr.ChatInterface로 감싸는 코드를 완성해줘"
#
# import gradio as gr
#
# def answer(message, history):
#     # gradio는 동기 → asyncio.run으로 에이전트 호출
#     resp = asyncio.run(helper_agent.run(message))
#     return resp.text
#
# if __name__ == "__main__":
#     asyncio.run(build_index())   # 먼저 학교 데이터 인덱싱!
#     gr.ChatInterface(
#         answer,
#         title=f"🏫 {SCHOOL_NAME} AI 도우미",
#         examples=["오늘 급식 뭐야?", "동아리 언제 해?", "도서관 몇 시까지 열어?"],
#     ).launch(server_name="0.0.0.0", server_port=7860)


# ================================================================
# 🌟 보너스 2: Session 결합 — 이전 대화 기억하기
# ================================================================
# 💡 Copilot: "helper_agent.create_session()으로 세션을 만들고,
#              여러 질문을 같은 session으로 run 해서 대화를 기억하게 해줘"
#
# async def chat_with_memory():
#     session = helper_agent.create_session()   # await 없음! (동기)
#     for msg in ["나는 2학년 3반 지민이야.", "우리 반 급식 시간 언제야?", "내가 몇 반이라고 했지?"]:
#         r = await helper_agent.run(msg, session=session)
#         print(f"👤 {msg}\n🤖 {r.text}\n")
