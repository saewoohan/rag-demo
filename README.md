# RAG (Retrieval-Augmented Generation) 시스템 구현 데모

이 프로젝트는 RAG(Retrieval-Augmented Generation) 시스템의 구성을 살펴보기 위한 간단한 데모입니다. 동일한 기능에 대해 컴포넌트들을 직접 구현한 방식과 LangChain을 활용한 방식으로 각각 개발하여 두 접근 방식을 살펴볼 수 있습니다.

## RAG란?

RAG는 대규모 언어 모델(LLM)의 응답 생성 능력과 외부 지식을 결합하는 방식입니다. 기존 LLM의 한계점들을 보완하여 다음과 같은 이점을 제공합니다.

1. **최신 정보 반영**: 학습 데이터에 포함되지 않은 최신 정보를 참조할 수 있습니다.
2. **사실 기반 응답**: 특정 문서나 데이터를 기반으로 응답하여 환각(Hallucination) 현상을 줄입니다.
3. **맥락 이해**: 주어진 문맥에 맞는 더 정확하고 관련성 높은 응답을 생성합니다.

### 동작 방식

RAG는 크게 두 단계로 동작합니다.

1. **검색 (Retrieval)**
   - 사용자 질문을 벡터로 변환
   - 벡터 데이터베이스에서 관련 문서 검색
   - 유사도 기반으로 가장 관련성 높은 문서 선택

2. **생성 (Generation)**
   - 검색된 문서들을 프롬프트에 포함
   - LLM이 문서 내용을 참조하여 응답 생성
   - 근거 기반의 정확한 답변 제공

테스트 데이터로는 2025년 초에 등장한 이탈리안 밈 'Italian Brainrot'의 캐릭터 정보를 사용합니다. 이 데이터셋은 각 캐릭터의 특성, 관계, 스토리 등 다양한 맥락 정보를 포함하고 있어 RAG 시스템의 성능을 테스트하기에 적합합니다.

## 구현 방식

1. Raw RAG Implementation (`/raw-rag`)
   - NestJS 기반의 직접 구현 방식
   - 각 컴포넌트(임베딩, 벡터 저장소, LLM)를 개별적으로 통합
   - 상세한 커스터마이징과 제어가 가능한 구조
   - 시스템의 각 부분을 직접 이해하고 구현하는 것이 목적

2. LangChain RAG Implementation (`/langchain-rag`)
   - Python FastAPI와 LangChain 프레임워크 활용
   - LangChain의 추상화된 컴포넌트들을 활용한 빠른 구현

## 시스템 아키텍처

### 핵심 컴포넌트
- **Vector DB**: ChromaDB (포트 8000)
  - 문서의 벡터 임베딩을 저장하고 유사도 검색 제공
  - 효율적인 벡터 검색을 위한 인덱싱 지원
- **임베딩 서버**: Sentence Transformers (포트 8080)
  - all-MiniLM-L6-v2 모델 사용
  - 텍스트를 고차원 벡터로 변환
- **LLM**: Ollama/Mistral (포트 11434)
  - 검색된 문맥을 바탕으로 응답 생성
  - 로컬에서 실행되는 오픈소스 LLM 활용
- **API 서버**:
  - Raw RAG: NestJS (포트 3000)
  - LangChain RAG: FastAPI (포트 3001)

### 데이터 흐름
1. 문서 처리 단계
   - 문서 텍스트 → 임베딩 변환
   - 벡터 데이터베이스 저장 및 인덱싱

2. 질의 처리 단계
   - 사용자 질문 → 임베딩 변환
   - 유사도 기반 관련 문서 검색
   - 검색 결과와 질문으로 프롬프트 생성
   - LLM을 통한 최종 답변 생성

## 프로젝트 구조

```
.
├── docker-compose.yml    # 전체 서비스 구성
├── raw-rag/             # 직접 구현한 RAG
│   ├── src/             # NestJS 서버
│   └── embedding_server/ # 임베딩 서버
└── langchain-rag/       # LangChain 기반 구현
    ├── main.py          # FastAPI 서버
    └── ingest.py        # 데이터 적재 스크립트
```

## 설치 및 실행

### Docker Compose로 전체 실행 (권장)

```bash
# 모든 서비스 실행
docker compose up -d

# Mistral 모델 설치 
curl -X POST http://localhost:11434/api/pull -d '{"name": "mistral"}'

# 서비스 상태 확인
docker compose ps

# 로그 확인
docker compose logs -f
```

### 수동 실행

#### Raw RAG 실행

```bash
cd raw-rag
yarn install
yarn cli:dev load:data # 데이터 적재
yarn start:dev  # API 서버 실행
```

#### LangChain RAG 실행

```bash
cd langchain-rag
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python ingest.py  # 데이터 적재
python main.py    # 서버 실행
```

## API 엔드포인트

### Raw RAG (포트 3000)

```bash
# 질문하기
curl -X POST http://localhost:3000/rag/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "트랄라레오 트랄랄라가 누군지 설명해줘"}'
```

### LangChain RAG (포트 3001)

```bash
# 질문하기
curl -X POST http://localhost:3001/rag/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "트랄라레오 트랄랄라가 누군지 설명해줘"}'
```

## 시스템 요구사항

1. 하드웨어
   - 최소 8GB RAM (Ollama LLM 실행용)
   - 충분한 디스크 공간 (모델 및 벡터 DB 저장용)

2. 소프트웨어
   - Docker 및 Docker Compose
   - Node.js 18+ (수동 실행 시)
   - Python 3.9+ (수동 실행 시)

## 문제 해결

1. LLM 서버 (Ollama) 관련:
   - 메모리 부족 시 Docker 리소스 제한 확인
   - 모델 다운로드 상태 확인
   - API 연결 상태 확인

2. 임베딩 서버 관련:
   - 모델 로드 상태 확인
   - 메모리 사용량 모니터링
   - API 응답 시간 체크

3. 벡터 DB (ChromaDB) 관련:
   - 데이터 적재 상태 확인
   - 인덱스 상태 점검
   - 저장소 권한 설정 확인
