import pygame  # pygame 라이브러리를 가져옵니다.
import random  # 랜덤 라이브러리를 가져옵니다.
import sys

pygame.init()  # pygame을 초기화합니다.
pygame.mixer.init()

# 화면 설정
screen_width = 1400  # 화면 너비 설정
screen_height = 800  # 화면 높이 설정
screen = pygame.display.set_mode((screen_width, screen_height))  # 지정된 크기로 게임 화면을 생성합니다.
pygame.display.set_caption("test")  # 게임 창의 제목을 'test'로 설정합니다.

# 화면 배경 이미지 로드
background = pygame.image.load(
    "assets/images/background_city1.png"
)  # 배경 이미지 파일을 로드합니다.

# 캐릭터 및 퀘스트 아이템 색상 설정
char_color = (0, 128, 0)  # 캐릭터의 색상을 RGB로 설정합니다.
item_colors = [(255, 0, 0), (0, 0, 255), (255, 128, 0)]  # 퀘스트 아이템의 색상을 RGB로 설정합니다.
# font = pygame.font.Font(None, 36)  # 글자 폰트 및 크기를 설정합니다.
font = pygame.font.Font("assets/fonts/neodgm.ttf", 30)


# 캐릭터 속성 설정
char_width = 50  # 캐릭터 너비 설정
char_height = 70  # 캐릭터 높이 설정
char_x = 50  # 캐릭터 x 위치 설정
char_y = screen_height / 2 - char_height / 2  # 캐릭터 y 위치 설정 (화면 중앙)
char_speed = 0.8  # 캐릭터 이동 속도 설정

# 캐릭터의 체력 설정 및 시간에 따른 체력 감소 변수 추가
char_health = 20
max_health = 20
health_decrease_interval = 3000  # 체력이 감소할 시간 간격 (ms 단위, 여기서는 5초)
last_health_decrease_time = pygame.time.get_ticks()  # 마지막으로 체력이 감소한 시간

# 퀘스트 아이템 속성 설정
item_width = 50  # 퀘스트 아이템  너비 설정
item_height = 70  # 퀘스트 아이템 높이 설정
item_speed = 1  # 퀘스트 아이템 이동 속도 설정

# 점수 초기화s
score = 0  # 전체 점수 초기화
programming_score = 0  # 프로그래밍 점수 초기화
math_score = 0  # 수학 점수 초기화
mini_game_score = 0  # 미니게임 점수 초기화


# 퀘스트 클래스 정의
class Quest:
    def __init__(self, quest_type, color, x, y, speed):
        # 퀘스트 아이템 속성 초기화
        self.type = quest_type  # 퀘스트 유형
        self.color = color  # 색상
        self.x = x  # x 위치
        self.y = y  # y 위치
        self.speed = speed  # 이동 속도
        self.active = True  # 활성/비활성 상태
        self.collided = False  # 충돌 상태
        self.points = 1  # 점수 (기본 1점)

    def move(self):
        # 퀘스트 아이템 이동 메서드
        if self.active:
            self.x -= self.speed  # 왼쪽으로 이동
            if self.x < -item_width:
                self.active = False  # 화면 왼쪽 밖으로 나가면 비활성화

    def draw(self, screen):
        # 퀘스트 아이템을 화면에 그리는 메서드
        pygame.draw.rect(screen, self.color, (self.x, self.y, item_width, item_height))


# 퀘스트 시작 시 출력하는 함수
def start_quest(quest_type):
    messages = {"programming": "프로그래밍 퀘스트", "math": "수학 퀘스트", "mini_game": "미니게임 퀘스트"}
    print(messages.get(quest_type, "알 수 없는 퀘스트"))  # 퀘스트 유형에 따른 메시지 출력


# 캐릭터와 퀘스트 아이템 간의 충돌 확인 함수
def check_collision(char_x, char_y, quest):
    global score, programming_score, math_score, mini_game_score
    # 충돌 조건 확인
    if (
        quest.active
        and (char_x < quest.x + item_width)
        and (char_x + char_width > quest.x)
        and (char_y < quest.y + item_height)
        and (char_y + char_height > quest.y)
    ):
        quest.collided = True  # 충돌 상태로 설정
        start_quest(quest.type)  # 퀘스트 시작
        # 퀘스트 유형에 따른 점수 추가
        if quest.type == "programming":
            programming_score += quest.points
        elif quest.type == "math":
            math_score += quest.points
        else:
            mini_game_score += quest.points

        score += quest.points  # 전체 점수 증가


# 충돌 후 퀘스트 아이템 상태 업데이트 함수
def update_quests(quests):
    for quest in quests:
        if quest.collided or not quest.active:
            quest.x = screen_width + random.randint(50, 300)  # 새 위치 설정
            quest.y = random.randint(0, screen_height - item_height)  # 새 위치 설정
            quest.collided = False  # 충돌 상태 초기화
            quest.active = True  # 활성화 상태로 설정


# 퀘스트 아이템 초기 설정
quests = [
    Quest(
        "programming",
        item_colors[0],
        screen_width,
        random.randint(0, screen_height - item_height),
        item_speed,
    ),
    Quest(
        "math",
        item_colors[1],
        screen_width + random.randint(200, 400),
        random.randint(0, screen_height - item_height),
        item_speed,
    ),
    Quest(
        "mini_game",
        item_colors[2],
        screen_width + random.randint(400, 600),
        random.randint(0, screen_height - item_height),
        item_speed,
    ),
]


# 장애물 클래스 정의
class Obstacle:
    def __init__(self, x, y, speed):
        self.color = (255, 255, 255)  # 장애물 색상
        self.x = x
        self.y = y
        self.speed = speed
        self.active = True

    def move(self):
        if self.active:
            self.x -= self.speed
            if self.x < -item_width:
                self.active = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, item_width, item_height))


def check_obstacle_collision(char_x, char_y, obstacle):
    global char_health
    if (
        obstacle.active
        and (char_x < obstacle.x + item_width)
        and (char_x + char_width > obstacle.x)
        and (char_y < obstacle.y + item_height)
        and (char_y + char_height > obstacle.y)
    ):
        obstacle.active = False  # 장애물 비활성화
        char_health -= 3  # 체력 감소


def update_obstacles(obstacles):
    for obstacle in obstacles:
        if not obstacle.active:
            obstacle.x = screen_width + random.randint(50, 300)
            obstacle.y = random.randint(0, screen_height - item_height)
            obstacle.active = True


# 장애물 초기 설정
obstacles = [
    Obstacle(
        screen_width + random.randint(50, 300),
        random.randint(0, screen_height - item_height),
        item_speed,
    )
]


def settings_screen():
    # 여기에 설정 화면에 대한 코드 추가
    pass


def shop_screen():
    # 여기에 상점 화면에 대한 코드 추가
    pass


def start_screen():
    pygame.mixer.music.load("assets/sounds/lobby_music.mp3")  # 배경 음악 파일을 로드합니다.
    pygame.mixer.music.play(-1)  # 무한 반복으로 음악을 재생합니다.

    while True:
        screen.blit(background, (0, 0))  # 배경 그리기
        pygame.draw.rect(
            screen, char_color, (char_x, char_y, char_width, char_height)
        )  # 캐릭터 그리기

        start_text = font.render("Press SPACE to Start", True, (255, 255, 255))
        settings_text = font.render("Press S for Settings", True, (255, 255, 255))
        shop_text = font.render("한국어 폰트 테스트", True, (255, 255, 255))

        screen.blit(
            start_text,
            (screen_width // 2 - start_text.get_width() // 2, screen_height // 2 - 40),
        )
        screen.blit(
            settings_text,
            (screen_width // 2 - settings_text.get_width() // 2, screen_height // 2),
        )
        screen.blit(
            shop_text,
            (screen_width // 2 - shop_text.get_width() // 2, screen_height // 2 + 40),
        )

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # 게임 시작
                elif event.key == pygame.K_s:
                    settings_screen()  # 설정 화면으로 이동
                elif event.key == pygame.K_p:
                    shop_screen()  # 상점 화면으로 이동


def pause_screen():
    pygame.mixer.music.pause()
    screen.blit(background, (0, 0))  # 배경 그리기
    pygame.draw.rect(
        screen, char_color, (char_x, char_y, char_width, char_height)
    )  # 캐릭터 그리기
    start_text = font.render("Press SPACE to Start", True, (255, 255, 255))
    screen.blit(
        start_text,
        (screen_width // 2 - start_text.get_width() // 2, screen_height // 2),
    )
    pygame.display.update()
    waiting = True  # 일시 중지 상태를 나타내는 변수
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False  # ESC 키를 누르면 일시 중지 종료


# 게임 실행 함수
def main():
    global char_y, score, last_health_decrease_time, char_health

    running = True  # 게임 실행 상태
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 창 닫기 이벤트 발생 시
                running = False  # 게임 종료
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_screen()  # ESC 키를 누르면 일시 중지 화면으로
                    pygame.mixer.music.unpause()  # 일시 중지된 음악을 다시 재생합니다.
                elif event.key == pygame.K_s:
                    settings_screen()  # S 키를 누르면 설정 화면으로 이동
                elif event.key == pygame.K_p:
                    shop_screen()  # P 키를 누르면 상점 화면으로 이동

        # 시간이 경과하면 체력 감소
        current_time = pygame.time.get_ticks()
        if current_time - last_health_decrease_time > health_decrease_interval:
            char_health -= 1
            last_health_decrease_time = current_time

        # 캐릭터 상하 움직임 처리
        keys = pygame.key.get_pressed()  # 눌린 키 확인
        if keys[pygame.K_UP]:
            char_y -= char_speed  # 위로 이동
        if keys[pygame.K_DOWN]:
            char_y += char_speed  # 아래로 이동

        char_y = max(0, min(screen_height - char_height, char_y))  # 화면 경계 처리

        # 배경 및 캐릭터 그리기
        screen.blit(background, (0, 0))  # 배경 그리기
        pygame.draw.rect(
            screen, char_color, (char_x, char_y, char_width, char_height)
        )  # 캐릭터 그리기

        for quest in quests:  # 각 퀘스트 아이템에 대해
            quest.move()  # 이동
            if quest.active:  # 활성 상태일 때만
                check_collision(char_x, char_y, quest)  # 충돌 확인
                quest.draw(screen)  # 화면에 그리기

        update_quests(quests)  # 퀘스트 상태 업데이트

        for obstacle in obstacles:
            obstacle.move()
            if obstacle.active:
                check_obstacle_collision(char_x, char_y, obstacle)
                obstacle.draw(screen)

        update_obstacles(obstacles)

        # 점수 화면에 표시
        programming_text = font.render(
            f"Programming Score: {programming_score}", True, (0, 0, 0)
        )
        math_text = font.render(f"Math Score: {math_score}", True, (0, 0, 0))
        mini_game_text = font.render(
            f"Mini Game Score: {mini_game_score}", True, (0, 0, 0)
        )
        health_text = font.render(f"Health: {'♥' * char_health}", True, (0, 0, 0))
        screen.blit(health_text, (10, 10))

        if char_health <= 0:
            print("Game Over!")
            running = False

        screen.blit(programming_text, (10, 50))
        screen.blit(math_text, (10, 90))
        screen.blit(mini_game_text, (10, 130))

        pygame.display.update()

    pygame.quit()  # 게임 종료


if __name__ == "__main__":
    start_screen()
    main()  # 메인 함수 실행
