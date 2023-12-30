import pygame
import sys
from pygame.locals import *
import random
import math

PINK = (168, 50, 98)
BLACK = (0,0,0)
SILVER = (191, 184, 191)
RED = (209, 69, 59)
PURPLE = (125, 81, 121)
DEEPBLUE = (146, 116, 207)
YELLOW = (235, 214, 59)

# 이미지 로드
img_howto = pygame.image.load("squirrel_image/howto.png") #스토리와 조작법 이미지
img_field = pygame.image.load("squirrel_image/field.png") #배경 이미지
img_character = [
    pygame.image.load("squirrel_image/squrriel.png"), #다람쥐 캐릭터 1
    pygame.image.load("squirrel_image/squrriel_l.png"),
    pygame.image.load("squirrel_image/squrriel_r.png"),
    pygame.image.load("squirrel_image/windnew.png"), #달리는 효과 이미지
    pygame.image.load("squirrel_image/squirrel1.png"), #다람쥐 캐릭터 2
    pygame.image.load("squirrel_image/newsquirrel1_l.png"),
    pygame.image.load("squirrel_image/newsquirrel1_r.png"),
    pygame.image.load("squirrel_image/windnew.png") #달리는 효과 이미지

]
img_branch = pygame.image.load("squirrel_image/branch.png") #공격도구 나뭇가지
img_enemy = [
    pygame.image.load("squirrel_image/enemy0.png"), #적0(족제비가 남긴 폭탄)
    pygame.image.load("squirrel_image/enemy1.png") #적 1(족제비)
]
img_explode = [
    None,
    pygame.image.load("squirrel_image/explosion1.png"), #터지는 효과음 1~5
    pygame.image.load("squirrel_image/explosion2.png"),
    pygame.image.load("squirrel_image/explosion3.png"),
    pygame.image.load("squirrel_image/explosion4.png"),
    pygame.image.load("squirrel_image/explosion5.png")
]

img_life = pygame.image.load("squirrel_image/life.png") #생명 표시 바
img_title = [
    pygame.image.load("squirrel_image/background.png"), #돌아가는 배경
    pygame.image.load("squirrel_image/title.png") #게임 제목
]

character_colors = [SILVER, SILVER] #캐릭터 선택 박스 색깔(박스1, 박스2)
mychar = 0 #캐릭터 선택 변수
gameSpeed = 30 #게임 속도 변수
index = 0 #인덱스 변수
score = 0 #점수 변수
timer = 0 #타이머 변수
bg_y = 0 #배경 스크롤 변수
#플레이어 위치
player_x = 480
player_y = 360 # 화면의 가운데에 위치하도록 함
player_slope = 0 #플레이어 기울기
space_key = 0 #스페이스 키 초기값
player_life = 100 #플레이어 수명 최대치 100으로 설정
player_invulnerable = 0 #플레이어 무적 상태 변수
# shooting 상태 확인
shooting_false = False
shooting_x = 0
shooting_y = 0
#나뭇가지 개수
shooting_max = 100 #공격할 수 있는 최대 나뭇가지 개수
shooting_number = 0 #나뭇가지 공격 리스트 초기 인덱스
shooting_false = [False]*shooting_max #공격중인지 확인하는 플래그, False(->True)로 나열된 리스트
shooting_x = [0]*shooting_max #나뭇가지 x좌표 리스트
shooting_y = [0]*shooting_max #나뭇가지 y좌표 리스트

ENEMY_MAX = 70 #적 최대수
enemy_number = 0 #적 변수 0으로 정의
enemy_false = [False]*ENEMY_MAX #적이 등장했는지 확인하는 플래그, False(->True)로 나열된 리스트
enemy_x = [0]*ENEMY_MAX #적 x좌표 리스트
enemy_y = [0]*ENEMY_MAX #적 y좌표 리스트
enemy_angle = [0]*ENEMY_MAX #적 이동 각도 리스트
enemy_type = [0]*ENEMY_MAX #적 종류 리스트
enemy_speed = [0]*ENEMY_MAX #적 이동 속도 리스트

ENEMY_BRANCH = 0 #나뭇가지 변수 초깃값 0으로 정의
#현재 윈도우 사이즈 폭 960, 높이 720이므로 화면에서 80픽셀이 추가되면 적 사라지도록 설정함
ENEMY_UP = -80 #적 나타나는(사라지는) 위쪽 좌표
ENEMY_DOWN = 800 #적 나타나는(사라지는) 아래쪽 좌표
ENEMY_LEFT = -80 #적 나타나는(사라지는) 왼쪽 좌표
ENEMY_RIGHT = 1040 #적 나타나는(사라지는) 오른쪽 좌표

EFFECT_MAX = 70 #폭발 최대수(족제비 최대 수와 같음)
effect_number = 0 #폭발 표시 변수
effect_numlist = [0]*EFFECT_MAX #폭발 리스트
effect_x = [0]*EFFECT_MAX
effect_y = [0]*EFFECT_MAX

def get_distance(x1, y1, x2, y2): #두 점 사이 거리 계산
    return ( pow((x1 - x2) , 2) + pow((y1 - y2), 2) )
#루트 사용하지 않고 제곱한 값 그대로 사용

def draw_text(scrn, text, x, y, size, color):
    font = pygame.font.Font(None, size) #폰트 생성(기본 폰트, size 크기)
    surface = font.render(text, True, color) 
    #surface 생성, 문자열, 색 설정, 안티앨리어싱 사용
    x -= surface.get_width() / 2 #문자 중심에서의 x 좌표를 나타냄
    y -= surface.get_height() / 2 #문자 중심에서의 y 좌표를 나타냄
    scrn.blit(surface, [x, y])

def move_character(scrn, key): #플레이어 위치 이동 함수
    global player_x, player_y, player_slope, space_key, player_life, player_invulnerable, index, timer #플레이어 위치 전역 변수
    player_slope = 0 # 기울기 변수 초깃값 0
    if key[pygame.K_UP]: #플레이어가 위쪽 키를 눌렀을 경우
        player_y -= 20 #y좌표 20 감소
        if player_y < 80: #y좌표가 80보다 작은 경우 80으로 설정
            player_y = 80 #다람쥐가 화면 밖으로 나가지 않도록 함
    if key[pygame.K_DOWN]: #플레이어가 아래쪽 키를 눌렀을 경우
        player_y += 20 #y좌표 20 증가
        if player_y >640: #y좌표가 640보다 큰 경우 640으로 설정
            player_y = 640 #다람쥐가 화면 밖으로 나가지 않도록 함
    if key[pygame.K_LEFT]: #플레이어가 왼쪽 키를 눌렀을 경우
        player_slope = 1 #플레이어가 왼쪽으로 이동할 때 기울도록 함(기울기 변수 1로 변경)
        player_x -= 20 #x좌표 20 감소
        if player_x < 40: #x좌표가 40보다 작은 경우 40으로 설정
            player_x = 40 #다람쥐가 화면 밖으로 나가지 않도록 함
    if key[pygame.K_RIGHT]: #플레이어가 오른쪽 키를 눌렀을 경우
        player_slope = 2 #플레이어가 오른쪽으로 이동할 때 기울도록 함(기울기 변수 2로 변경)
        player_x += 20 #x좌표 20 증가
        if player_x > 920: #y좌표가 920보다 큰 경우 920으로 설정
            player_x = 920 #다람쥐가 화면 밖으로 나가지 않도록 함

    space_key = (space_key + 1) * key[K_SPACE]
    #space_key 초깃값 0 설정 -> space바를 누르는 동안 sapce_key 변tnt값 증가
    #key[K_SPACE]가 True일 경우 1, False일 경우 0
    if space_key % 6 == 1 : 
    # space_key 값이 6으로 나누었을 때 나머지가 1이면
        set_shooting() #나뭇가지를 발사하는 함수 작동되도록 함
    # 따라서 일정한 간격으로 나뭇가지가 발사됨, 연속적으로 나뭇가지가 발사되지 않도록 함
    if player_invulnerable % 2 == 0 : #무적 상태(수명 깎인 경우)에서 깜빡거리기 위해 if문 추가
        # player_invulnerable이 60인 상태에서 1씩 줄며 화면에 나타났다 사라졌다하면서
        #깜빡이는 효과를 나타낼 수 있음
        scrn.blit(img_character[3], [player_x - 35 , player_y + 30 + (timer%3)*2]) 
        #달리는 효과 나타내기 img_character[3] 달리기 효과 나타냄
        # (timer%3)*2에 의해 0,2,4 중 하나의 값을 가짐, y좌표가 상하로 움직일 수 있도록 함
        scrn.blit(img_character[player_slope+mychar*4], [player_x - 37, player_y - 48]) #다람쥐 나타내기
        # 다람쥐 이미지의 폭이 74픽셀 높이 96픽셀이므로
        # X좌표에서 37을 빼고 Y 좌표에서 48을 빼 다람쥐의 왼쪽 최상단의 점을 나타내어
        # (player_x, player_y)가 다람쥐의 중심 좌표가 되도록 함
        # 이동 방향에 따라 기울기가 달라질 수 있도록 img_character[player_slope+ mychar*4]로 설정
    if player_invulnerable > 0: # 무적 상태라면
        player_invulnerable -= 1 # 무적 상태 변수 감소시키고
        return #함수 벗어남, 충돌감지하지 않음
    elif index == 1: #무적 상태가 아니고 index가 1이라면
        for i in range(ENEMY_MAX):
            if enemy_false[i] == True: #족제비 존재한다면
                w = img_enemy[enemy_type[i]].get_width() #족제비 폭 구함
                h = img_enemy[enemy_type[i]].get_height() #족제비 높이 구함
                r = int((w+h)/4 + (74 + 96) / 4) #충돌 감지 거리 계산
                #족제비 반지름은 족제비 이미지 폭과 높이 합의 1/4
                #다람쥐 반지름은 다람쥐 이미지(폭 74, 높이 96) 합의 1/4
                if get_distance(enemy_x[i], enemy_y[i], player_x, player_y) <r*r:
                    #족제비와 다람쥐 사이의 거리가 r보다 작으면 충돌한 것으로 감지
                    set_explode(player_x, player_y) #폭발 표시
                    player_life -= 10 #다람쥐 수명 10감소
                    if player_life <= 0 : #다람쥐 수명이 0이하이면
                        player_life = 0 #다람쥐 수명 0으로 재설정
                        index = 2 #게임 오버 이동
                        timer = 0 #timer 초기화
                    if player_invulnerable == 0: #충돌했을 때 무적 상태가 아니면
                        player_invulnerable = 60 #60프레임(2초동안) 무적 상태로 설정
                    enemy_false[i] = False # 족제비 False 설정하여 삭제

def set_shooting():
    global shooting_number
    shooting_false[shooting_number] = True #set_shooting()실행 시 플래그 True로 변경
    shooting_x[shooting_number] = player_x
    shooting_y[shooting_number] = player_y - 50
    #나뭇가지의 위치를 다람쥐의 앞쪽에 두도록 하기 위해 -50
    shooting_number = (shooting_number + 1) % shooting_max 
    #다음 shooting_number계산 -> 1씩 계속 증가하나 %로 인해 shooting_max를 넘지 않음

def move_shooting(scrn): #나뭇가지 이동시킴
    for i in range(shooting_max):
        if shooting_false[i] == True: #나뭇가지가 발사된 상태라면
            shooting_y[i] -= 36 #나뭇가지 위치 위로 옮긴 후
            scrn.blit(img_branch, [shooting_x[i] - 10, shooting_y[i] - 32])
            #현재 나뭇가지 좌표가 나뭇가지 이미지의 중심좌표를 나타내는 것이므로 
            #위치를 왼쪽 최상단으로 조정해줌(나뭇가지 이미지 폭 20 높이 64)
            if shooting_y[i] < 0: #나뭇가지가 화면에서 사라지면
                shooting_false[i] = False #False 처리하여 나뭇가지 없애기

def show_enemy(): #적 등장 함수
    if timer % 20 == 0: #타이머의 숫자가 20의 배수일 때
        set_enemy(random.randint(20,940), ENEMY_UP, 90,1,6) 
        #족제비 등장
        #x좌표 랜덤 설정, y좌표 = (ENEMY_UP =-80), 각도 90, 적 종류1(족제비), 족제비 이동 속도 6 

def set_enemy(x,y,angle,type,speed): #적 설정 함수
    global enemy_number #enemy_number 전역 변수 설정
    while True:
        if enemy_false[enemy_number] == False: #함수가 실행됐을 때 리스트 속 플래그가 False이면
            enemy_false[enemy_number] = True #True로 변경
            enemy_x[enemy_number] = x #x좌표 리스트 속 enemy_number번째 x로 변경
            enemy_y[enemy_number] = y #y좌표 리스트 속 enemy_number번째 y로 변경
            enemy_angle[enemy_number] = angle
            #angle 좌표 리스트 속 enemy_number번째 angle로 변경
            enemy_type[enemy_number] = type
            #type 좌표 리스트 속 enemy_number번째 type로 변경
            enemy_speed[enemy_number] = speed
            #speed 좌표 리스트 속 enemy_number번째 speed로 변경
            break
        enemy_number = (enemy_number + 1) % ENEMY_MAX 
        #번호 순서 1증가한 순서로 변경, ENEMY_MAX로 인해 enemy_number은 
        #ENEMY_MAX 넘어가지 않음

def move_enemy(scrn):
    global index, timer, score, player_life, gameSpeed
    for i in range(ENEMY_MAX): #ENEMY_MAX번만큼 반복
        if enemy_false[i] == True: #플래그의 변수가 True이면(적이 존재하면)
            angle = -90 - enemy_angle[i] 
            #이미지를 회전한 각도 대입(스크린 좌표계 고려하여 -90)
            enemy_x[i] += enemy_speed[i]* math.cos(math.radians(enemy_angle[i])) #적 이동 x방향
            enemy_y[i] += enemy_speed[i]* math.sin(math.radians(enemy_angle[i])) #적 이동 y방향
            if enemy_type[i] == 1 and enemy_y[i] > 360: 
                #enemy_type[i] == 1은 족제비, 족제비의 y좌표가 360을 넘을 때
                set_enemy(enemy_x[i],enemy_y[i],90,0,8)
                #적 설정함수 실행, 폭탄이 실행됨
                enemy_angle[i] = -45 #방향(각도) 변경, 45도 방향으로 적 날아감
                enemy_speed[i] = 16 #속도 변경
            if enemy_x[i] < ENEMY_LEFT or ENEMY_RIGHT < enemy_x[i] or enemy_y[i] < ENEMY_UP or ENEMY_DOWN < enemy_y[i]:
            #적이 화면에서 벗어났다면
                enemy_false[i] = False #적 삭제
            img_rotate = pygame.transform.rotozoom(img_enemy[enemy_type[i]], angle, 1.0)
                #적 회전시킨 이미지 생성, 1.0은 scale
            scrn.blit(img_rotate, [enemy_x[i] - img_rotate.get_width()/2, enemy_y[i] - img_rotate.get_height()/2])
            #이미지의 중심에 좌표가 위치하도록 설정

            if enemy_type[i] != ENEMY_BRANCH:
                #ENEMY_BRANCH가 0이므로 적만을 충돌 체크함
                enemy_w = img_enemy[enemy_type[i]].get_width() #적 폭
                enemy_h = img_enemy[enemy_type[i]].get_height() #적 높이
                enemy_d = int((enemy_w + enemy_h)/4) + 12 #적 거리 계산 + 나뭇가지 반지름 12픽셀
                for j in range(shooting_max):
                    if shooting_false[j] == True and get_distance(enemy_x[i], enemy_y[i], shooting_x[j], shooting_y[j]) < enemy_d*enemy_d:
                    #나뭇가지에 맞은 경우    
                        shooting_false[j] = False #나뭇가지 삭제
                        set_explode(enemy_x[i], enemy_y[i])
                        score += 100 #나뭇가지에 맞은 경우 점수 100증가
                        enemy_false[i] = False #적 삭제
                        gameSpeed += 0.5 #적 맞출때마다 속도 0.5씩 증가
                        if player_life < 100: 
                        #적을 맞추었을 때 player 수명이 100보다 작은 경우
                            player_life += 1 #수명 1 증가시킴

def set_explode(x, y) : #폭발 설정
    global effect_number #전역 변수 설정
    effect_numlist[effect_number] = 1 
    #폭발 연출 이미지 번호 대입, 이미지가 None부터 시작하므로
    #effect_numlist[effect_number] = 1인 경우 폭발 그림 load가 시작됨
    effect_x[effect_number] = x 
    effect_y[effect_number] = y
    effect_number = (effect_number + 1) % EFFECT_MAX #다음 번호 1만큼 증가시킴,EFFECT_MAX를 넘을 수 없음

def draw_explode(scrn):
    for i in range(EFFECT_MAX):
        if effect_numlist[i] > 0:  # 폭발 표현 진행중이라면
            scrn.blit(img_explode[effect_numlist[i]], [effect_x[i] - 48, effect_x[i] - 48])
            #폭발 이미지 크기가 폭 96, 높이 96이므로 48씩 빼 effect_x, effect_x의 좌표가
            #이미지 중간에 위치하도록 함
            effect_numlist[i] += 1  # 리스트 속 값 1 증가
            if effect_numlist[i] == 6:
                effect_numlist[i] = 0  # 이펙트 단계가 5단계까지이므로 6이되면 다시 0으로 변경해줌

def main():
    global index, score, player_x, player_y, player_slope, player_life, player_invulnerable, timer, bg_y, mychar, gameSpeed #배경 스크롤, timer 전역변수
    pygame.init() # pygame 초기화
    pygame.display.set_caption("Squirrel's Adventure") #이름 설정
    # 화면 설정
    width = 960
    height = 720
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock() #프레임 속도 조절

    while True:
        timer += 1 #timer의 값 1씩 증가
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN: #버튼을 누를 경우
                if event.key == pygame.K_ESCAPE : #esc 키 누른 경우 게임 종료
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN: #버튼을 누를 경우
                if event.key == pygame.K_F1: #F1 키를 누르면
                    screen = pygame.display.set_mode((width, height), 
                                                     pygame.FULLSCREEN) #게임 전체 화면
                if event.key == pygame.K_F2: #F2 키 누를 경우
                    screen = pygame.display.set_mode((width, height)) #게임 전체화면 나가기
    
        #배경 스크롤
        bg_y = (bg_y + 16) % 720 #16의 크기만큼 스크롤해줌, 화면 높이인 720의 약수인 16 사용
        screen.blit(img_field, [0, bg_y-720]) 
        # 화면 위, bg_y가 720을 초과할경우 screen 좌표계의 아래로 다시 가져옴
        screen.blit(img_field, [0,bg_y]) # 화면 아래, 컴퓨터 화면 상 밑으로 계속 내려감

        #다람쥐 움직이기 입력받기
        key = pygame.key.get_pressed() #동시에 입력한 키 처리 가능
        
        #index에 따른 화면 표시
        if index == 0: #게임 시작 전
            img_rotation = pygame.transform.rotozoom(img_title[0], timer%360, 1.0)
            #회전하는 이미지 생성
            #배경이 오른쪽으로 돌아가게 하기 위해 -timer%360 사용함
            screen.blit(img_rotation, [480 - img_rotation.get_width()/2, 300 - img_rotation.get_height()/2])
            #좌표를 이미지의 중심에 두기 위해 나누기 2 사용
            screen.blit(img_title[1], [70,160]) #로고 표현
            #텍스트 표현
            draw_text(screen, "Press [SPACE] to start!", 480, 600, 50, PURPLE)
            draw_text(screen, "[Q] to see Story & How to play", 480, 400, 45, PINK)
            draw_text(screen, "[S] to select the character", 480,632,30,RED)
            draw_text(screen, "Press [ESC] to exit", 480, 660, 30, DEEPBLUE)
            if key[K_SPACE]: #스페이스 키를 누르면
                index = 1
                timer = 0
                score = 0
                #플레이어 초기 위치
                player_x = 480
                player_y = 600
                player_slope = 0
                player_life = 100
                player_invulnerable = 0
                gameSpeed = 30
                for i in range(ENEMY_MAX):
                    enemy_false[i] = False #적이 등장하지 않는 동안 False 설정
                for i in range(shooting_max):
                    shooting_false = False #나뭇가지 발사하지 않은 상태로 설정
            if key[K_s]: #캐릭터 변경을 위해 s키를 누르면
                index = 4 #index 4로 이동함
            if key[K_q]: #스토리와 사용법을 보기 위해 p키를 누르면
                index = 5 #index 5로 이동함
        
        if index == 1:  #게임 중    
            move_character(screen, key) #다람쥐 움직이기
            move_shooting(screen) #나뭇가지 쏘기
            show_enemy() #적 등장
            move_enemy(screen) #적 움직이기
            if score == 10000: #스코어가 10000이면 게임 클리어 되도록 함
                index = 3 #게임 클리어 화면으로 이동
                timer = 0 #타이머 0으로 초기화
    
        if index == 2: #게임 오버
            move_shooting(screen)
            show_enemy()
            screen.fill(BLACK)  # 검은 화면으로 채우기
            draw_text(screen, "GAME OVER", 480, 300, 80, RED)  # 게임 오버 메시지 표시
            draw_text(screen, "Press 'Z' to start again", 480, 350, 50, SILVER)
            if key[pygame.K_z]:  # Z 키를 누를 경우
                index = 0 #다시 첫 화면(게임 시작 전)으로 돌아감
        
        if index == 3: #게임 클리어
            move_character(screen, key)
            move_shooting(screen)
            screen.fill(BLACK)  # 검은 화면으로 채우기
            draw_text(screen, "GAME CLEAR!!", 480, 300, 80, YELLOW)
            draw_text(screen, "Press 'Z' to start again", 480, 350, 50, SILVER)
            draw_text(screen, "Press [ESC] to exit", 480, 640, 30, DEEPBLUE)
            if key[pygame.K_z]:  # Z 키를 누를 경우
                index = 0 #다시 첫 화면으로 돌아감
                score = 0
        
        if index == 4:
            draw_text(screen, "Select your character", 470, 160, 50, DEEPBLUE)
            for i in range(2):
                #캐릭터 선택 박스 위치 좌표(x,y)
                x = 350 + 240 * i
                y = 300
                color = character_colors[i]  #다람쥐 1, 다람쥐 2의 캐릭터 선택 박스 색깔
                #초깃값은 [SILVER, SILVER]
                pygame.draw.rect(screen,color,[x-100,y-80,200,160])
                #직사각형 그리기, x,y좌표가 직사각형의 중심에 위치한 좌표를 나타냄
                draw_text(screen,"[SQUIRREL "+str(i+1)+"]",x,y-50,30,DEEPBLUE)
                screen.blit(img_character[i*4],[x-40,y-20])
                #i에 따라 각각의 캐릭터 박스에 다람쥐 1, 다람쥐 2가 들어감
                draw_text(screen,"[ENTER] to SELECT!",460,440,40,PURPLE)
                if key[K_1]:
                    mychar = 0  # 캐릭터 1 선택
                    character_colors[0] = RED  # 선택된 캐릭터 색 변경
                    character_colors[1] = SILVER  # 다른 캐릭터 색 원래대로 변경
                elif key[K_2]:
                    mychar = 1  # 캐릭터 2 선택
                    character_colors[0] = SILVER  # 다른 캐릭터 색 원래대로 변경
                    character_colors[1] = RED  # 선택된 캐릭터 색 변경
                if key[K_RETURN]:
                    index = 0 #ENTER 누를 시 시작화면으로 돌아감
        
        if index == 5: #스토리와 사용법 화면 나타내기
            global img_height, img_width #전역 변수 설정
            img_height = img_howto.get_height() #사용법 이미지의 높이 저장
            img_width = img_howto.get_width() #사용법 이미지의 폭 저장
            screen.blit(img_howto, [480 - img_width / 2, 360 - img_height / 2])
            #이미지가 화면의 가운데에 위치하도록 설정함
            draw_text(screen, "To go back press [Z]!", 480, 30, 50, RED)
            if key[K_z]:  # Z 키를 누를 경우
                index = 0  # 다시 첫 화면으로 돌아감


        draw_explode(screen) #폭발 효과 나타내기 함수
        draw_text(screen, "SCORE "+str(score), 120 , 50, 50, PURPLE) #점수 표시

        if index != 0 : #인덱스 값이 0이 아니라면(게임 시작화면이 아니라면) 수명 표시함
            screen.blit(img_life, [40, 680]) # 수명 나타내는 화면 표시
            pygame.draw.rect(screen, (83, 114, 181), [40 + player_life*4, 680, (100 - player_life)*4, 12])
            #깎인 수명만큼을 표현, (83, 114, 181)는 파란색 표현
        pygame.display.update()
        clock.tick(gameSpeed)

if __name__ == "__main__":
    main()