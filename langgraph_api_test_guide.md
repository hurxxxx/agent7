# LangGraph API 테스트 가이드

이 문서는 LangGraph API를 테스트하는 방법을 설명합니다. LangGraph는 LangChain 생태계의 일부로, 복잡한 AI 워크플로우를 관리하기 위한 라이브러리입니다.

## 목차
1. [환경 설정](#환경-설정)
2. [LangGraph 서버 실행](#langgraph-서버-실행)
3. [API 테스트 방법](#api-테스트-방법)
   - [검색 기능 테스트](#검색-기능-테스트)
   - [농담 생성 기능 테스트](#농담-생성-기능-테스트)
4. [LangGraph Studio UI 사용](#langgraph-studio-ui-사용)
5. [문제 해결](#문제-해결)

## 환경 설정

LangGraph API를 테스트하기 전에 필요한 환경 설정을 완료해야 합니다.

1. 필요한 API 키가 포함된 `.env` 파일이 있는지 확인합니다:
   ```
   TAVILY_API_KEY=your_tavily_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

2. 필요한 패키지가 설치되어 있는지 확인합니다:
   ```bash
   pip install langgraph langchain-openai langchain-anthropic langchain-tavily
   ```

## LangGraph 서버 실행

LangGraph API를 테스트하기 위해 로컬 개발 서버를 실행합니다.

```bash
langgraph dev
```

서버가 성공적으로 시작되면 다음과 같은 출력이 표시됩니다:
```
- 🚀 API: http://127.0.0.1:2024
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- 📚 API Docs: http://127.0.0.1:2024/docs
```

## API 테스트 방법

LangGraph API는 HTTP 요청을 통해 테스트할 수 있습니다. 여기서는 `curl` 명령을 사용한 테스트 방법을 설명합니다.

### 기본 API 호출 형식

```bash
curl -s --request POST \
    --url "http://localhost:2024/runs/stream" \
    --header 'Content-Type: application/json' \
    --data "{
        \"assistant_id\": \"agent\",
        \"input\": {
            \"messages\": [
                {
                    \"role\": \"human\",
                    \"content\": \"YOUR_QUERY_HERE\"
                }
            ]
        },
        \"stream_mode\": \"updates\"
    }"
```

### 검색 기능 테스트

Tavily 검색 도구를 사용하여 웹에서 정보를 검색하는 기능을 테스트합니다.

```bash
curl -s --request POST \
    --url "http://localhost:2024/runs/stream" \
    --header 'Content-Type: application/json' \
    --data "{
        \"assistant_id\": \"agent\",
        \"input\": {
            \"messages\": [
                {
                    \"role\": \"human\",
                    \"content\": \"What is LangGraph?\"
                }
            ]
        },
        \"stream_mode\": \"updates\"
    }"
```

예상 응답:
- 에이전트가 "search" 도구를 호출하여 LangGraph에 대한 정보를 검색합니다.
- 검색 결과를 바탕으로 LangGraph에 대한 요약 정보를 제공합니다.

### 농담 생성 기능 테스트

jokeMaker 도구를 사용하여 농담을 생성하는 기능을 테스트합니다.

```bash
curl -s --request POST \
    --url "http://localhost:2024/runs/stream" \
    --header 'Content-Type: application/json' \
    --data "{
        \"assistant_id\": \"agent\",
        \"input\": {
            \"messages\": [
                {
                    \"role\": \"human\",
                    \"content\": \"Make a joke about Python programming\"
                }
            ]
        },
        \"stream_mode\": \"updates\"
    }"
```

예상 응답:
- 에이전트가 "jokeMaker" 도구를 호출하여 Python 프로그래밍에 관한 농담을 생성합니다.
- 생성된 농담과 함께 설명을 제공합니다.

## LangGraph Studio UI 사용

LangGraph Studio UI를 사용하여 그래픽 인터페이스로 API를 테스트할 수도 있습니다.

1. 웹 브라우저에서 다음 URL을 엽니다:
   ```
   https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
   ```

2. UI에서 "ReAct Agent" 그래프를 클릭합니다.

3. 입력 필드에 쿼리를 입력하고 제출합니다.

4. 그래프 시각화를 통해 에이전트의 작동 과정을 확인할 수 있습니다.

## 문제 해결

### 서버 시작 문제

- **Docker 권한 오류**: Docker 관련 오류가 발생하면 다음 명령을 실행하여 권한을 설정합니다:
  ```bash
  sudo usermod -aG docker $USER && newgrp docker
  ```

- **API 키 오류**: 필요한 API 키가 `.env` 파일에 올바르게 설정되어 있는지 확인합니다.

### API 호출 문제

- **연결 오류**: 서버가 실행 중인지 확인합니다. 다른 터미널에서 `langgraph dev` 명령이 실행 중이어야 합니다.

- **응답 타임아웃**: 검색 쿼리가 복잡한 경우 응답 시간이 길어질 수 있습니다. 충분한 시간을 기다려주세요.

- **도구 호출 오류**: 도구 이름이 올바른지 확인합니다. 현재 사용 가능한 도구는 "search"와 "jokeMaker"입니다.

---

이 문서는 LangGraph API 테스트를 위한 기본 가이드입니다. 더 자세한 정보는 [LangGraph 공식 문서](https://langchain-ai.github.io/langgraph/)를 참조하세요.
