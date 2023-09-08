import pygame  # pygame 라이브러리를 가져옵니다.
import random  # 랜덤 라이브러리를 가져옵니다.
import sys

pygame.init()  # pygame을 초기화합니다.
pygame.mixer.init()
frame_index = 0
clock = pygame.time.Clock()
animation_delay = 100

# 화면 설정
screen_width = 1400  # 화면 너비 설정
screen_height = 800  # 화면 높이 설정
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("test")

# 화면 배경 이미지 로드
background = pygame.image.load(
    "assets/images/background/background_city1.png"
)  # 배경 이미지 파일을 로드합니다.

# 캐릭터 및 퀘스트 아이템 색상 설정
char_color = (0, 128, 0)  # 캐릭터의 색상을 RGB로 설정
item_colors = [(255, 0, 0), (0, 0, 255), (255, 128, 0)]  # 퀘스트 아이템의 색상을 RGB로 섲어
font = pygame.font.Font("assets/fonts/neodgm.ttf", 30)


# 캐릭터 속성 설정

char_width = 90  # 캐릭터 너비 설정
char_height = 110  # 캐릭터 높이 설정
char_x = 50  # 캐릭터 x 위치 설정
char_y = screen_height / 2 - char_height / 2  # 캐릭터 y 위치 설정 (화면 중앙)
char_speed = 7  # 캐릭터 이동 속도 설정

# 캐릭터의 체력 설정 및 시간에 따른 체력 감소 변수 추가
char_health = 20
max_health = 20
health_decrease_interval = 1000  # 체력이 감소할 시간 간격 (ms 단위, 여기서는 1초)
last_health_decrease_time = pygame.time.get_ticks()  # 마지막으로 체력이 감소한 시간

number_of_frames = 7

# 캐릭터 이미지 불러오기
character_frames = [
    pygame.image.load(f"assets/images/character/1_frame_{i}.png")
    for i in range(number_of_frames)
]
character_frames = [
    pygame.transform.scale(frame, (char_width, char_height))
    for frame in character_frames
]

frame_index = 0  # 현재 프레임의 인덱스
animation_frame_count = 6  # 총 프레임 수
animation_counter = 0  # 애니메이션 업데이트 카운터
animation_delay = 6  # 애니메이션 업데이트 속도 (낮을수록 느림)


# 퀘스트 아이템 속성 설정
item_width = 50  # 퀘스트 아이템  너비 설정
item_height = 70  # 퀘스트 아이템 높이 설정
item_speed = 8  # 퀘스트 아이템 이동 속도 설정

# 점수 초기화
score = 0  # 전체 점수 초기화
programming_score = 0  # 프로그래밍 점수 초기화
math_score = 0  # 수학 점수 초기화
science_score = 0  # 미니게임 점수 초기화
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

        if quest_type == "programming":
            self.image = pygame.image.load("assets/images/items/computer.png")
        elif quest_type == "math":
            self.image = pygame.image.load("assets/images/items/math.jpeg")
        elif quest_type == "science":
            self.image = pygame.image.load("assets/images/items/science.png")

    def move(self):
        # 퀘스트 아이템 이동 메서드
        if self.active:
            self.x -= self.speed  # 왼쪽으로 이동
            if self.x < -item_width:
                self.active = False  # 화면 왼쪽 밖으로 나가면 비활성화

    def draw(self, screen):
        # 퀘스트 아이템을 화면에 그리는 메서드
        if self.active:
            screen.blit(self.image, (self.x, self.y))


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
    global programming_score, math_score, science_score
    messages = {
        "programming": "프로그래밍 퀘스트",
        "math": "수학 퀘스트",
        "science": "과학 상식 퀘스트",
        "coin": "코인 획득",
    }
    print(messages.get(quest_type, "알 수 없는 퀘스트"))  # 퀘스트 유형에 따른 메시지 출력

    choices = ["a", "b", "c", "d", "e"]

    if quest_type == "math":
        questions = [
            (
                "1부터 100까지의 정수 중 7의 배수의 합은?",
                ["735", "504", "874", "946", "271"],
            ),
            (
                "2x + 3y = 27,. 7x - 4y = 22 일 때, x,y의 값은?",
                [
                    "x = 6, y = 5",
                    "x = 4, y = 3",
                    "x = 5, y = 2",
                    "x = 3, y = 6",
                    "x = 5, y = 6",
                ],
            ),
            (
                "576과 168의 최대공약수는?",
                ["24", "28", "36", "46", "52"],
            ),
            (
                "3개의 동전을 던질 때 모두 앞면이 나올 확률은?",
                ["1/8", "1/64", "1/6", "1/18", "8/1"],
            ),
        ]
        question, options = random.choice(questions)
        correct_answer = options[0]
        random.shuffle(options)

    elif quest_type == "programming":
        questions = [
            (
                "Python에서 문자열의 길이를 얻으기 위해 사용하는 함수는?",
                ["len", "size", "length", "count", "measure"],
            ),
            (
                "Python에서 리스트의 마지막 요소를 얻기 위해 사용하는 함수는?",
                ["pop", "push", "remove", "delete", "end"],
            ),
            (
                "Python에서 for 반복문과 함께 사용되는 함수는?",
                ["range", "loop", "repeat", "for", "times"],
            ),
            (
                "Python의 머신러닝 라이브러리를 고르시오",
                ["skiet_learn", "pygame", "random", "jango", "flask"],
            ),
        ]
        question, options = random.choice(questions)
        correct_answer = options[0]
        random.shuffle(options)

    elif quest_type == "science":
        questions = [
            (
                "절대온도 0K에 근접할 때 시스템의 무질서 또는 엔트로피가 최소화된다는 법칙은?",
                ["열역학 제 3법칙", "관성의 법칙", "특수 상대성이론", "가속도의 법칙", "열역학 제 2법칙"],
            ),
            (
                "뉴턴 운동 법칙의 식은?",
                ["F = ma", "E = mc^2", "a^2 + b^2 = c^2", "1/2 * m * h ", "I = BS"],
            ),
            ("태양계에서 가장 큰 행성은?", ["목성", "금성", "지구", "화성", "토성"]),
        ]
        question, options = random.choice(questions)
        correct_answer = options[0]
        random.shuffle(options)

    else:
        return

    # Display the question and choices on the pygame screen
    question_text = font.render(question, True, (0, 0, 0))
    screen.blit(question_text, (screen_width // 4, screen_height // 4))
    for i, option in enumerate(options):
        choice_text = font.render(f"{choices[i]}. {option}", True, (0, 0, 0))
        screen.blit(choice_text, (screen_width // 4, screen_height // 4 + (i + 1) * 40))
    pygame.display.update()

    # Wait for the user to press one of the choice keys
    selected_answer = None
    while selected_answer not in choices:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in [
                    pygame.K_a,
                    pygame.K_b,
                    pygame.K_c,
                    pygame.K_d,
                    pygame.K_e,
                ]:
                    selected_answer = choices[event.key - pygame.K_a]

    if options[choices.index(selected_answer)] == correct_answer:
        print("정답입니다!")
        if quest_type == "math":
            math_score += 10
        elif quest_type == "programming":
            programming_score += 10
        elif quest_type == "science":
            science_score += 10
    else:
        print("틀렸습니다.")


def check_collision(char_x, char_y, item):
    global score, programming_score, math_score, science_score, coins_score
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
        elif item.type == "science":
            science_score += item.points
        elif item.type == "coin":  # 코인 유형 처리
            coins_score += item.points
            item.active = False  # 코인을 먹었으므로 비활성화


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
        "science",
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
        self.image = pygame.image.load("assets/images/items/obs.png")

    def move(self):
        if self.active:
            self.x -= self.speed
            if self.x < -item_width:
                self.active = False

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, (self.x, self.y))


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
            coin.draw(screen)
            check_collision(char_x, char_y, coin)
        else:
            coins.remove(coin)  # 비활성화된 코인은 리스트에서 제거


def settings_screen():
    print("설정 진입")
    pass


def shop_screen():
    print("상점 진입")
    pass


def start_screen():
    pygame.mixer.music.load(
        "assets/sounds/background/lobby_music.mp3"
    )  # 배경 음악 파일을 로드합니다.
    pygame.mixer.music.play(-1)  # 무한 반복으로 음악을 재생합니다.

    while True:
        screen.blit(background, (0, 0))  # 배경 그리기
        screen.blit(character_frames[frame_index], (char_x, char_y))  # 현재 프레임 그리기

        start_text = font.render("Press SPACE to Start", True, (0, 0, 0))
        settings_text = font.render("Press S for Settings", True, (0, 0, 0))
        shop_text = font.render("상점으로 이동하기", True, (0, 0, 0))

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


def game_over_screen():
    pygame.mixer.music.load(
        "assets/sounds/GameOver/Game_over_music.mp3"
    )  # 게임 오버 음악 파일을 로드합니다.
    pygame.mixer.music.play(-1)  # 무한 반복으로 음악을 재생합니다.

    game_over_text = font.render("Game Over", True, (255, 0, 0))
    retry_text = font.render("Press SPACE to Retry", True, (255, 255, 255))

    while True:
        screen.blit(background, (0, 0))  # 배경 그리기
        screen.blit(
            game_over_text,
            (
                screen_width // 2 - game_over_text.get_width() // 2,
                screen_height // 2 - 40,
            ),
        )
        screen.blit(
            retry_text,
            (screen_width // 2 - retry_text.get_width() // 2, screen_height // 2),
        )
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # 게임 다시 시작


def reset_game_variables():
    global char_y, score, last_health_decrease_time, char_health, coins, coins_score, frame_index, animation_counter, programming_score, math_score, science_score
    char_y = screen_height / 2 - char_height / 2
    score = 0
    last_health_decrease_time = pygame.time.get_ticks()
    char_health = max_health
    coins = [
        Coin(
            screen_width + random.randint(50, 300),
            random.randint(0, screen_height - item_height),
            item_speed,
        )
    ]
    coins_score = 0
    frame_index = 0
    animation_counter = 0
    programming_score = 0  # 프로그래밍 점수 초기화
    math_score = 0  # 수학 점수 초기화
    science_score = 0  # 미니게임 점수 초기화


def restart_game():
    reset_game_variables()
    start_screen()


def game_over_screen():
    pygame.mixer.music.load("assets/sounds/GameOver/Game_over_music.mp3")
    pygame.mixer.music.play(-1)
    screen.fill((0, 0, 0))

    game_over_text = font.render("Game Over", True, (255, 0, 0))
    retry_text = font.render("Press SPACE to Retry", True, (255, 255, 255))

    game_over_text = font.render("Game Over", True, (255, 0, 0))
    retry_text = font.render("Press SPACE to Retry", True, (255, 255, 255))

    while True:
        screen.blit(background, (0, 0))
        screen.blit(
            game_over_text,
            (
                screen_width // 2 - game_over_text.get_width() // 2,
                screen_height // 2 - 40,
            ),
        )
        screen.blit(
            retry_text,
            (screen_width // 2 - retry_text.get_width() // 2, screen_height // 2),
        )
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # 게임 다시 시작


def show_ending_image():
    global programming_score, math_score, science_score, coins_score
    ending_image = None

    print("Programming Score:", programming_score)
    print("Math Score:", math_score)
    print("science Score:", science_score)

    if programming_score > math_score and programming_score > science_score:
        ending_image_path = "assets/images/endings/programer.png"
        print("programer")
    elif math_score > programming_score and math_score > science_score:
        ending_image_path = "assets/images/endings/math.png"
        print("math")
    elif science_score > programming_score and science_score > math_score:
        ending_image_path = "assets/images/endings/science.pngg"
        print("science")
    elif science_score == 0 and programming_score == 0 and math_score == 0:
        list_lotto = [1, 1, 1, 1, 1, 1, 1, 0]
        choicelist = random.choice(list_lotto)
        if choicelist == 0:
            ending_image_path = "assets/images/endings/lotto.png"
        else:
            ending_image_path = "assets/images/endings/die.png"
    else:
        list_rand_ending = [0, 1]
        choice_ending_list = random.choice(list_rand_ending)
        if choice_ending_list == 1:
            ending_image_path = "assets/images/endings/rand1.png"
        elif choice_ending_list == 0:
            ending_image_path = "assets/images/endings/rand2.png"

        print("defualt")

    ending_image = pygame.image.load(ending_image_path)
    screen.blit(ending_image, (0, 0))
    pygame.display.update()
    pygame.time.wait(3000)


# 게임 실행 함수
def main():
    global char_y, score, last_health_decrease_time, char_health, coins, coins_score, frame_index, animation_counter
    running = True  # 게임 실행 상태
    while running:
        if char_health <= 0:
            print("Game Over!")
            game_over_screen()
            show_ending_image()
            reset_game_variables()

            start_screen()

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

        screen.blit(background, (0, 0))  # 배경 그리기
        screen.blit(character_frames[frame_index], (char_x, char_y))  # 현재 프레임 그리기

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

        update_quests(quests, coins)

        # 점수 화면에 표시
        programming_text = font.render(
            f"Programming Score: {programming_score}", True, (0, 0, 0)
        )
        screen.blit(programming_text, (10, 50))

        math_text = font.render(f"Math Score: {math_score}", True, (0, 0, 0))
        screen.blit(math_text, (10, 90))

        science_text = font.render(f"science Score: {science_score}", True, (0, 0, 0))
        screen.blit(science_text, (10, 130))

        health_text = font.render(f"Health: {'0' * char_health}", True, (0, 0, 0))
        screen.blit(health_text, (10, 10))

        coins_text = font.render(f"Coins Score: {coins_score}", True, (0, 0, 0))
        screen.blit(coins_text, (10, 170))

        animation_counter += 1
        if animation_counter >= animation_delay:
            frame_index = (frame_index + 1) % animation_frame_count
            animation_counter = 0

        pygame.display.update()

        clock.tick(60)
    pygame.quit()  # 게임 종료


if __name__ == "__main__":
    start_screen()
    main()  # 메인 함수 실행
