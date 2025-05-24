import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수 로드
ACCESS_TOKEN = os.getenv('THREADS_ACCESS_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

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

def generate_thread_message():
    """GPT를 사용하여 스레드 메시지를 생성합니다."""
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    prompt = """너는 바이브 코딩을 주제로 스레드를 운영하는 크리에이터야.  
바이브 코딩은 '완벽하지 않아도, 일단 손으로 만들고 실행하면서 배워나가는 코딩'이라는 철학을 가진 사람들을 위한 활동이야.

다음 조건을 반영해서 스레드용 메시지를 1개 작성해줘:

- 전체 글자 수는 300자 이내  
- 줄바꿈을 적절히 활용해 가독성을 높일 것  
- 이모티콘(예: 🔥, 🎯, 🤖, 💡 등)을 자연스럽게 활용할 것  
- 바이브 코딩을 하고 있는 사람들에게 공감, 위로, 동기부여 또는 실용 팁을 줄 것  
- '사람들의 반응(좋아요나 댓글)'을 이끌 수 있도록 공감 가는 현실 이야기나 유익한 인사이트를 포함할 것  
- 하나의 인사이트 또는 감정에 집중된 메시지일 것  
- 스레드 스타일 말투로 쓸 것 (예: "솔직히", "이거 하나만 기억해", "내 얘기 좀 들어봐" 등)  
- 특수문자(`*`, `#`, 불필요한 기호 등)는 사용하지 말 것  
- 출력 형식은 메시지 본문만 보여줄 것 (앞뒤에 구분선이나 마크다운 기호 넣지 말 것)"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 바이브 코딩을 주제로 스레드를 운영하는 크리에이터입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        raise Exception(f"GPT 메시지 생성 중 오류 발생: {str(e)}")

def main():
    """메인 실행 함수"""
    # 필수 환경 변수 확인
    if not all([OPENAI_API_KEY, ACCESS_TOKEN]):
        print("필요한 API 키가 설정되지 않았습니다. .env 파일에 다음 키들을 추가해주세요:")
        print("- OPENAI_API_KEY")
        print("- THREADS_ACCESS_TOKEN")
        return

    try:
        # 사용자 ID 확인
        print("\n사용자 ID 확인 중...")
        user_id = get_user_id(ACCESS_TOKEN)
        
        if not user_id:
            print("사용자 ID를 가져오는데 실패했습니다.")
            return

        # 메시지 생성
        print("\nGPT로 메시지 생성 중...")
        message = generate_thread_message()
        print("\n생성된 메시지:")
        print(message)
        
        # 스레드 업로드
        print("\nThreads에 포스팅 시도 중...")
        container_id = create_threads_container(message, ACCESS_TOKEN, user_id)
        
        if not container_id:
            print("컨테이너 생성에 실패했습니다.")
            return
            
        post_id = publish_threads_container(container_id, ACCESS_TOKEN, user_id)
        
        if post_id:
            print("\n포스팅이 완료되었습니다!")
        else:
            print("\n포스팅에 실패했습니다.")
        
    except Exception as e:
        print(f"오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main() 