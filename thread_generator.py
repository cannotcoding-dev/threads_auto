import os
import openai
from dotenv import load_dotenv
import requests
from datetime import datetime

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수 로드
ACCESS_TOKEN = os.getenv('THREADS_ACCESS_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# OpenAI API 키 설정
openai.api_key = OPENAI_API_KEY

def get_user_id(access_token):
    """Threads API를 통해 사용자 ID를 가져옵니다."""
    try:
        response = requests.get(
            "https://graph.threads.net/v1.0/me",
            params={'access_token': access_token}
        ).json()
        
        if 'error' in response:
            print(f"사용자 ID 확인 중 오류 발생: {response['error']}")
            return None
            
        user_id = response['id']
        print(f"사용자 ID 확인 성공: {user_id}")
        return user_id
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return None

def create_threads_container(text, access_token, user_id):
    """스레드 컨테이너를 생성합니다."""
    try:
        response = requests.post(
            f"https://graph.threads.net/v1.0/{user_id}/threads",
            params={
                'text': text,
                'media_type': 'TEXT',
                'access_token': access_token
            }
        ).json()
        
        if 'error' in response:
            print(f"컨테이너 생성 중 오류 발생: {response['error']}")
            return None
            
        container_id = response['id']
        print(f"컨테이너 생성 성공! ID: {container_id}")
        return container_id
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return None

def publish_threads_container(container_id, access_token, user_id):
    """생성된 컨테이너를 발행합니다."""
    try:
        response = requests.post(
            f"https://graph.threads.net/v1.0/{user_id}/threads_publish",
            params={
                'creation_id': container_id,
                'access_token': access_token
            }
        ).json()
        
        if 'error' in response:
            print(f"포스팅 중 오류 발생: {response['error']}")
            return None
            
        post_id = response['id']
        print(f"포스팅 성공! Post ID: {post_id}")
        return post_id
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return None

def generate_message():
    try:
        # GPT API 호출
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 바이브 코딩을 주제로 스레드를 운영하는 크리에이터입니다. 바이브 코딩은 '완벽하지 않아도, 일단 손으로 만들고 실행하면서 배워나가는 코딩'이라는 철학을 가진 사람들을 위한 활동입니다."},
                {"role": "user", "content": """다음 조건을 반영해서 스레드용 메시지를 1개 작성해줘:

- 전체 글자 수는 300자 이내  
- 줄바꿈을 적절히 활용해 가독성을 높일 것  
- 이모티콘(예: 🔥, 🎯, 🤖, 💡 등)을 자연스럽게 활용할 것  
- 바이브 코딩을 하고 있는 사람들에게 공감, 위로, 동기부여 또는 실용 팁을 줄 것  
- '사람들의 반응(좋아요나 댓글)'을 이끌 수 있도록 공감 가는 현실 이야기나 유익한 인사이트를 포함할 것  
- 하나의 인사이트 또는 감정에 집중된 메시지일 것  
- 스레드 스타일 말투로 쓸 것 (예: "솔직히", "이거 하나만 기억해", "내 얘기 좀 들어봐" 등)  
- 특수문자(`*`, `#`, 불필요한 기호 등)는 사용하지 말 것  
- 출력 형식은 메시지 본문만 보여줄 것 (앞뒤에 구분선이나 마크다운 기호 넣지 말 것)"""}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        # 생성된 메시지 반환
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"GPT로 메시지 생성 중 오류 발생: {str(e)}")
        return None

def check_permissions():
    try:
        # Facebook Graph API를 통해 권한 확인
        response = requests.get(
            f"https://graph.facebook.com/v18.0/me/permissions",
            params={"access_token": ACCESS_TOKEN}
        )
        print("권한 확인 응답:", response.json())
        return response.status_code == 200
    except Exception as e:
        print(f"권한 확인 중 오류 발생: {str(e)}")
        return False

def post_to_threads(message):
    try:
        # 사용자 ID 확인
        print("사용자 ID 확인 중...")
        user_id = get_user_id(ACCESS_TOKEN)
        
        if not user_id:
            print("사용자 ID를 가져오는데 실패했습니다.")
            return False

        # Threads API를 통해 포스팅
        response = requests.post(
            f"https://graph.threads.net/v1.0/{user_id}/threads",
            params={
                'text': message,
                'media_type': 'TEXT',
                'access_token': ACCESS_TOKEN
            }
        )
        
        print("API 요청 상세 정보:")
        print(f"URL: {response.url}")
        print(f"상태 코드: {response.status_code}")
        print(f"응답 내용: {response.text}")
        
        if response.status_code == 200:
            print("Threads에 성공적으로 포스팅되었습니다!")
            return True
        else:
            print(f"포스팅 실패: {response.text}")
            return False
    except Exception as e:
        print(f"Threads 포스팅 중 오류 발생: {str(e)}")
        return False

def main():
    # 권한 확인
    if not check_permissions():
        print("Threads API 권한이 없습니다. 액세스 토큰을 확인해주세요.")
        return

    # 메시지 생성
    print("GPT로 메시지 생성 중...")
    message = generate_message()
    if not message:
        print("메시지 생성에 실패했습니다.")
        return

    # Threads에 포스팅
    print("생성된 메시지:", message)
    print("Threads에 포스팅 중...")
    if post_to_threads(message):
        print("포스팅이 완료되었습니다!")
    else:
        print("포스팅에 실패했습니다.")

if __name__ == "__main__":
    main() 