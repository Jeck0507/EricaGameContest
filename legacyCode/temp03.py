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
char_speed = 7  # 캐릭터 이동 속도 설정

# 캐릭터의 체력 설정 및 시간에 따른 체력 감소 변수 추가
char_health = 30
max_health = 30
health_decrease_interval = 1000  # 체력이 감소할 시간 간격 (ms 단위, 여기서는 5초)
last_health_decrease_time = pygame.time.get_ticks()  # 마지막으로 체력이 감소한 시간

# 퀘스트 아이템 속성 설정
item_width = 50  # 퀘스트 아이템  너비 설정
item_height = 70  # 퀘스트 아이템 높이 설정
item_speed = 8  # 퀘스트 아이템 이동 속도 설정

# 점수 초기화
score = 0  # 전체 점수 초기화
programming_score = 0  # 프로그래밍 점수 초기화
math_score = 0  # 수학 점수 초기화
mini_game_score = 0  # 미니게임 점수 초기화
coins_score = 0  # 미니게임 점수 초기화


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


class Coin:
    def __init__(self, x, y, speed):
        self.color = (255, 255, 0)  # 코인 색상 (노란색)
        self.x = x
        self.y = y
        self.speed = speed
        self.active = True
        self.type = "coin"  # 코인 유형 추가
        self.points = 5

    def move(self):
        if self.active:
            self.x -= self.speed
            if self.x < -item_width:
                self.active = False

    def draw(self, screen):
        if self.active:  # 코인이 활성 상태일 때만 그림
            pygame.draw.ellipse(
                screen, self.color, (self.x, self.y, item_width, item_height)
            )


coins = [
    Coin(
        screen_width + random.randint(50, 300),
        random.randint(0, screen_height - item_height),
        item_speed,
    )
]


# 퀘스트 시작 시 출력하는 함수
def start_quest(quest_type):
    messages = {"programming": "프로그래밍 퀘스트", "math": "수학 퀘스트", "mini_game": "미니게임 퀘스트"}
    print(messages.get(quest_type, "알 수 없는 퀘스트"))  # 퀘스트 유형에 따른 메시지 출력


# 캐릭터와 퀘스트 아이템 간의 충돌 확인 함수
def check_collision(char_x, char_y, item):
    global score, programming_score, math_score, mini_game_score
    if (
        item.active
        and (char_x < item.x + item_width)
        and (char_x + char_width > item.x)
        and (char_y < item.y + item_height)
        and (char_y + char_height > item.y)
    ):
        item.collided = True
        start_quest(item.type)  # 퀘스트 시작
        if item.type == "programming":
            programming_score += item.points
        elif item.type == "math":
            math_score += item.points
        elif item.type == "mini_game":
            mini_game_score += item.points
        elif item.type == "coin":  # 코인 유형 처리
            score += item.points
            item.active = False  # 코인을 먹었으므로 비활성화


# 충돌 후 퀘스트 아이템 상태 업데이트 함수
# 충돌 후 퀘스트 아이템 상태 업데이트 함수
def update_quests(quests, coins):
    for quest in quests:
        if quest.collided or not quest.active:
            quest.x = screen_width + random.randint(50, 300)
            quest.y = random.randint(0, screen_height - item_height)
            quest.collided = False
            quest.active = True

            # 새로운 코인 생성
            coins.append(
                Coin(
                    screen_width + random.randint(50, 300),
                    random.randint(0, screen_height - item_height),
                    item_speed,
                )
            )


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
        self.color = (0, 0, 0)  # 장애물 색상
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


def update_coins(coins):
    for coin in coins:
        coin.move()
        if coin.active:
            check_collision(char_x, char_y, coin)
            coin.draw(screen)
        else:
            coins.remove(coin)  # 비활성화된 코인은 리스트에서 제거
            coins_score += coin.points  # 코인 점수 업데이트


def settings_screen():
    print("설정 진입")
    pass


def shop_screen():
    print("상점 진입")
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
    global char_y, score, last_health_decrease_time, char_health, coins, coins_score

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

        for obstacle in obstacles:
            obstacle.move()
            if obstacle.active:
                check_obstacle_collision(char_x, char_y, obstacle)
                obstacle.draw(screen)

        update_obstacles(obstacles)

        for coin in coins:
            coin.move()
            if coin.active:
                check_collision(char_x, char_y, coin)
                coin.draw(screen)
            else:
                coins.remove(coin)  # 비활성화된 코인은 리스트에서 제거
                coins_score += coin.points  # 코인 점수 업데이트

        update_quests(quests, coins)

        # 점수 화면에 표시
        programming_text = font.render(
            f"Programming Score: {programming_score}", True, (0, 0, 0)
        )
        screen.blit(programming_text, (10, 50))

        math_text = font.render(f"Math Score: {math_score}", True, (0, 0, 0))
        screen.blit(math_text, (10, 90))

        mini_game_text = font.render(
            f"Mini Game Score: {mini_game_score}", True, (0, 0, 0)
        )
        screen.blit(mini_game_text, (10, 130))

        mini_game_text = font.render(
            f"Mini Game Score: {mini_game_score}", True, (0, 0, 0)
        )
        screen.blit(mini_game_text, (10, 130))

        health_text = font.render(f"Health: {'♥' * char_health}", True, (0, 0, 0))
        screen.blit(health_text, (10, 10))

        coins_text = font.render(f"Coins Score: {coins_score}", True, (0, 0, 0))
        screen.blit(coins_text, (10, 170))  # 화면에 코인 점수 표시
        if char_health <= 0:
            print("Game Over!")
            running = False

        pygame.display.update()

    pygame.quit()  # 게임 종료


if __name__ == "__main__":
    start_screen()
    main()  # 메인 함수 실행
