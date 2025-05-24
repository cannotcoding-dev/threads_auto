# Threads Auto Poster

Threads에 자동으로 포스팅하는 프로그램입니다. GPT를 사용하여 바이브 코딩 관련 메시지를 생성하고, Threads API를 통해 자동으로 포스팅합니다.

## 기능

- GPT를 사용한 자동 메시지 생성
- Threads API를 통한 자동 포스팅
- GitHub Actions를 통한 매일 자동 실행 (오후 1시)

## 설정 방법

1. 저장소 클론
```bash
git clone [repository-url]
cd [repository-name]
```

2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

3. 환경 변수 설정
`.env` 파일을 생성하고 다음 정보를 입력:
```
OPENAI_API_KEY=your_openai_api_key
THREADS_ACCESS_TOKEN=your_threads_access_token
```

4. GitHub Secrets 설정
GitHub 저장소의 Settings > Secrets and variables > Actions에서 다음 시크릿을 추가:
- `OPENAI_API_KEY`: OpenAI API 키
- `THREADS_ACCESS_TOKEN`: Threads API 액세스 토큰

## GitHub Actions 설정

이 프로젝트는 GitHub Actions를 사용하여 매일 오후 1시에 자동으로 실행됩니다. 워크플로우 파일은 `.github/workflows/daily_threads.yml`에 있습니다.

## 수동 실행

GitHub Actions 워크플로우를 수동으로 실행하려면:
1. GitHub 저장소의 Actions 탭으로 이동
2. "Daily Threads Post" 워크플로우 선택
3. "Run workflow" 버튼 클릭

## 주의사항

- Threads API 액세스 토큰은 정기적으로 갱신이 필요할 수 있습니다.
- API 사용량 제한에 주의하세요.
- GitHub Actions의 무료 사용량 제한을 확인하세요. 