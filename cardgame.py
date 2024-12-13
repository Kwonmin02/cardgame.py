import pygame, sys, random, time
import tkinter, tkinter.messagebox

BLACK = (0, 0, 0)
blood_color = (172, 50, 50)
defense_color = (95, 205, 228)
pygame.font.init()
Nfont = pygame.font.Font("NUM_FONT.ttf", 64)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((2240, 1260))
clock = pygame.time.Clock()

card_sounds = ["damage"]
card_sounds = [
    pygame.mixer.Sound("sound_effect/slash.mp3"), #슬래쉬
    pygame.mixer.Sound("sound_effect/hunger_skull.mp3"), #먹보 해골
    pygame.mixer.Sound("sound_effect/fire_hell.mp3"), #불지옥
    pygame.mixer.Sound("sound_effect/dirt.mp3"), #흙뿌리기
    pygame.mixer.Sound("sound_effect/like_stone.mp3"), #금강불괴
    pygame.mixer.Sound("sound_effect/god_weight.mp3"), #신의 무게
    pygame.mixer.Sound("sound_effect/harvest.mp3"), #벼베기
    pygame.mixer.Sound("sound_effect/light.mp3"), #라이트
    pygame.mixer.Sound("sound_effect/dark_clouds.mp3"), #먹구름
    pygame.mixer.Sound("sound_effect/curse.mp3"), #저주
    pygame.mixer.Sound("sound_effect/meteor.mp3"), #메테오   #-------------------------여기까지가 공격카드
    pygame.mixer.Sound("sound_effect/defense.mp3"), #방어카드
    pygame.mixer.Sound("sound_effect/eyewash.mp3"), #눈속임
    pygame.mixer.Sound("sound_effect/trickery.mp3"), #밑장빼기  #----------------------여기까지가 방어카드
    pygame.mixer.Sound("sound_effect/two_hands.mp3"), #양손잡이 
    pygame.mixer.Sound("sound_effect/strengthening_spells.mp3"), #주문 강화
    pygame.mixer.Sound("sound_effect/1+1.mp3"), # 일석이조
]       
    
class button():
    def __init__(self, img, pos):
        self.image = pygame.image.load(img)
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect = self.image.get_rect(topleft = (self.x_pos, self.y_pos))

    def update(self):
        screen.blit(self.image, self.rect)

    def checkmouse(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        else: return False

    def button_change(self, position, img):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.image = pygame.image.load(img)
            self.rect = self.image.get_rect(topleft = (self.x_pos, self.y_pos))
            screen.blit(self.image, self.rect)
            pygame.display.update()

class Card:
    def __init__(self, name, cost, effect_function, image):
        self.name = name
        self.cost = cost
        self.effect_function = effect_function
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

    def apply_effect(self, target):
        if self.effect_function:
            self.effect_function(target)
# 플레이어, 적 클래스
class Entity:
    def __init__(self, name, cost, pos, hp, max_hp, defense, damage, image):
        self.name = name
        self.cost = cost
        self.image = pygame.image.load(image)
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect = self.image.get_rect(topleft = (self.x_pos, self.y_pos))
        self.max_hp = max_hp
        self.hp = hp
        self.defense = defense
        self.damage = damage
        if self.hp > 0:
            self.alive = True
        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    def action(self, target):
        if target.defense > self.damage:
            target.defense = target.defense - self.damage
        elif target.defense < self.damage:
            target.hp = (target.hp + target.defense) - self.damage
            target.defense = 0
# 공격 카드 클래스
class DamageCard(Card):
    def __init__(self, name, cost, damage, defense, selfdam, image):
        super().__init__(name, cost, self.apply_effect, image)
        self.rect = self.image.get_rect()
        self.defense = defense
        self.selfdam = selfdam
        self.damage = damage# 카드가 줄 데미지

    def apply_effect(self, target, target1, target2):
        if target1.alive == False:
            return  # 이미 죽어있으면 효과 없음
        if target2.cost == 0:
            return  #코스트가 0이면 효과 없음
        if target2.cost < self.cost:
            return
        
        if self.name == "slash" :
            card_sounds[0].play()
        elif self.name == "먹보 해골" :
            card_sounds[1].play()
        elif self.name == "주문 강화" :
            card_sounds[15].play()
        elif self.name == "불지옥" :
            card_sounds[2].play()
        elif self.name == "흙뿌리기" :
            card_sounds[3].play()
        elif self.name == "신의 무게" :
            card_sounds[5].play()
        elif self.name == "벼베기" :
            card_sounds[6].play()
        elif self.name == "라이트" :
            card_sounds[7].play()
        elif self.name == "먹구름" :
            card_sounds[8].play()
        elif self.name == "저주" :
            card_sounds[9].play()
        elif self.name == "메테오" :
            card_sounds[10].play()

        if self.name == "벼베기" or self.name == "먹구름":
            target.hp = target.hp - self.damage
        if self.name == "먹보 해골" or self.name == "주문 강화":
            self.damage = self.damage + 5
        target2.hp = target2.hp - self.selfdam
        target2.cost = target2.cost - self.cost
        if target1.defense > self.damage:
            target1.defense = target1.defense - self.damage
        elif target1.defense < self.damage:
            target1.defense = 0
            target1.hp = (target1.hp + target1.defense) - self.damage
        if target.hp <= 0:
            target.hp = 0
            target.alive = False
        if target1.hp <= 0:
            target1.hp = 0
            target1.alive = False

    def update(self, pos):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect = self.image.get_rect(topleft = (self.x_pos, self.y_pos))
        screen.blit(self.image, self.rect)
# 방어 카드 클래스
class DefenseCard(Card):
    def __init__(self, name, cost, damage, defense, image):
        super().__init__(name, cost, self.apply_effect, image)
        self.rect = self.image.get_rect()
        self.damage = damage
        self.defense = defense  # 증가할 방어도

    def apply_effect(self, target, target1, target2):
        if target1.alive == False:
            return  # 죽어있는 타겟엔 방어도 효과 없음
        if target2.cost == 0:
            return  #코스트가 0이면 효과 없음
        if target2.cost < self.cost:
            return
        
        if self.name == "defense" :
            card_sounds[11].play()
        elif self.name == "눈속임" :
            card_sounds[12].play()
        elif self.name == "미러 스킨" or self.name == "금강불괴":
            card_sounds[4].play()
        elif self.name == "밑장빼기" :
            card_sounds[13].play()
        
        target2.cost = target2.cost - self.cost
        target2.defense = target2.defense + self.defense
    
    def update(self, pos):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect = self.image.get_rect(topleft = (self.x_pos, self.y_pos))
        screen.blit(self.image, self.rect)
# 혼합 카드 클래스
class Damdef(Card): 
    def __init__(self, name, cost, damage, defense, image):
        super().__init__(name, cost, self.apply_effect, image)
        self.rect = self.image.get_rect()
        self.damage = damage
        self.defense = defense

    def apply_effect(self, target, target1, target2):
        if target1.alive == False:
            return  # 이미 죽어있으면 효과 없음
        if target2.cost == 0:
            return  #코스트가 0이면 효과 없음
        if target2.cost < self.cost:
            return
        
        if self.name == "양손잡이" :
            card_sounds[14].play()
        elif self.name == "1+1" :
            card_sounds[16].play()
        
        target2.cost = target2.cost - self.cost
        if target1.defense > self.damage:
            target1.defense = target1.defense - self.damage
        elif target1.defense < self.damage:
            target1.defense = 0
            target1.hp = (target1.hp + target1.defense) - self.damage
        if target1.hp <= 0:
            target1.hp = 0
            target1.alive = False
        target2.defense = target2.defense + self.defense

    def update(self, pos):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect = self.image.get_rect(topleft = (self.x_pos, self.y_pos))
        screen.blit(self.image, self.rect)

def play_background_music() :
    pygame.mixer.music.load("sound/background/MP_Rise.mp3")
    pygame.mixer.music.set_volume(5)  
    pygame.mixer.music.play(-1)

def stop_background_music() :
    pygame.mixer.music.stop()

class BloodBar():
    def __init__(self, x, y, hp, max_hp, BC = blood_color):
        self.x = x
        self.y = y # 고정 값 = 735
        self.hp = hp
        self.max_hp = max_hp
        self.BC = BC

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, 728, 200, 35))  # (x, y(위치), 가로, 높이) / 검정 / 세로길게
        pygame.draw.rect(screen, (0, 0, 0), (self.x - 7, 735, 214, 21))  # 검정 / 가로길게
        pygame.draw.rect(screen, self.BC, (self.x, self.y, 200 * (self.hp / self.max_hp), 21))  # 빨강 / (378(x), 735, 350(피통50*7), 21(3*7))
        pygame.draw.rect(screen, (106,106,106), (self.x + 200 * (self.hp / self.max_hp), self.y, 200 - 200 * (self.hp/self.max_hp), 21)) # 줄어든 부분을 이걸로 채울거야

class ShieldBar():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, Entity):
        if Entity.defense > 0:    
            text = Nfont.render(f"{Entity.defense}", True, (255, 255, 255))
            if Entity.defense < 10:
                screen.blit(text, (392, 699))  # 글자 위치
            else:
                screen.blit(text, (378, 699))  # 글자 위치
        else:
            return

class Animation:
    def __init__(self,frames,speed):
        self.frames = frames  
        self.current_frame = 0
        self.speed = speed
        self.animation_timer = 0
        self.is_playing = False

    def play(self,screen,x,y):
        if self.is_playing:
            self.animation_timer += 1
            if self.animation_timer >= self.speed:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.animation_timer = 0
                
            current_image = self.frames[self.current_frame]
            screen.blit(self.frames[self.current_frame], (x, y))
            
            if self.current_frame == len(self.frames) - 1:
                self.is_playing = False
                self.current_frame = 0

    def start(self):
        self.is_playing= True
        self.current_frame =0

map1 = [
    pygame.image.load("image/map/sp1/0.png"),
    pygame.image.load("image/map/sp1/1.png"),
    pygame.image.load("image/map/sp1/2.png"),
    pygame.image.load("image/map/sp1/3.png"),
    pygame.image.load("image/map/sp1/4.png"),
    pygame.image.load("image/map/sp1/5.png"),
    pygame.image.load("image/map/sp1/6.png"),
    pygame.image.load("image/map/sp1/7.png"),
    pygame.image.load("image/map/sp1/8.png"),
    pygame.image.load("image/map/sp1/9.png"),
    pygame.image.load("image/map/sp1/10.png")
    ]
map2 = [
    pygame.image.load("image/map/sp2/0.png"),
    pygame.image.load("image/map/sp2/1.png"),
    pygame.image.load("image/map/sp2/2.png"),
    pygame.image.load("image/map/sp2/3.png"),
    pygame.image.load("image/map/sp2/4.png"),
    pygame.image.load("image/map/sp2/5.png"),
    pygame.image.load("image/map/sp2/6.png"),
    pygame.image.load("image/map/sp2/7.png"),
    pygame.image.load("image/map/sp2/8.png"),
    pygame.image.load("image/map/sp2/9.png"),
    pygame.image.load("image/map/sp2/10.png")
    ]
land = [
        pygame.image.load("image/land/1.png"),
        pygame.image.load("image/land/2.png"),
        pygame.image.load("image/land/3.png"),
        pygame.image.load("image/land/4.png"),
        pygame.image.load("image/land/5.png"),
        pygame.image.load("image/land/6.png"),
        pygame.image.load("image/land/7.png"),
        pygame.image.load("image/land/8.png"),
        pygame.image.load("image/land/9.png")
        ]
P_1 = "image/character/P-ch/1/idle/0.png"
P_2 = "image/character/P-ch/2/idle/0.png"
p1_attack_frames = [
    pygame.image.load("image/character/P-ch/1/attack/0.png"),
    pygame.image.load("image/character/P-ch/1/attack/1.png"),
    pygame.image.load("image/character/P-ch/1/attack/2.png"),
    pygame.image.load("image/character/P-ch/1/attack/3.png"),
    pygame.image.load("image/character/P-ch/1/attack/4.png"),
    pygame.image.load("image/character/P-ch/1/attack/5.png"),
    pygame.image.load("image/character/P-ch/1/attack/6.png"),
    pygame.image.load("image/character/P-ch/1/attack/7.png")
]
p2_attack_frames = [
    pygame.image.load("image/character/P-ch/2/attack/1/0.png"),
    pygame.image.load("image/character/P-ch/2/attack/1/1.png"),
    pygame.image.load("image/character/P-ch/2/attack/1/2.png"),
    pygame.image.load("image/character/P-ch/2/attack/1/3.png"),
    pygame.image.load("image/character/P-ch/2/attack/1/4.png"),
    pygame.image.load("image/character/P-ch/2/attack/1/5.png"),
    pygame.image.load("image/character/P-ch/2/attack/1/6.png"),
    pygame.image.load("image/character/P-ch/2/attack/1/7.png")
]
adven1 = "image/character/E-ch/adventurer/Adven_1/idle/0.png"
adven2 = "image/character/E-ch/adventurer/Adven_2/idle/0.png"
archer1 = "image/character/E-ch/archer/arc_1/idle/0.png"
archer2 = "image/character/E-ch/archer/arc_2/idle/0.png"
witch = "image/character/E-ch/witch/idle/0.png"
chef1 = "image/character/E-ch/chef/chef_1/idle/0.png"
chef2 = "image/character/E-ch/chef/chef_2/idle/0.png"
farm_m = "image/character/E-ch/farmer/man/idle/0.png"
farm_w = "image/character/E-ch/farmer/woman/idle/0.png"
captain = "image/character/E-ch/guard captain/idle/0.png"
patrol = "image/character/E-ch/patrolman/idle/0.png"
brave = "image/character/E-ch/brave/attack/1/0.png"
stage = [
    pygame.image.load("image/main/B1_1.png"),
    pygame.image.load("image/main/B1_2.png"),
    pygame.image.load("image/main/B1_3.png"),
    pygame.image.load("image/main/B2_1.png"),
    pygame.image.load("image/main/B2_2.png"),
    pygame.image.load("image/main/B2_3.png"),
    pygame.image.load("image/main/B3_1.png"),
    pygame.image.load("image/main/B3_2.png"),
    pygame.image.load("image/main/B3_3.png")
         ]
cover = pygame.image.load("image/main/game_cover.png")
P_ch = [
    Entity("P_1", 6, (460, 400), 20, 20, 0, 0, P_1), Entity("P_2", 6, (460, 500), 20, 20, 0, 0, P_2)
    ]
enemy = [
    Entity("adven1", 0, (1300, 500), 10, 10, 0, 3, adven1), Entity("adven2", 0, (1650, 500), 10, 10, 0, 3, adven2),
    Entity("arc1", 0, (1300, 500), 10, 10, 0, 3, archer1), Entity("arc2", 0, (1650, 500), 10, 10, 0, 3, archer2),
    Entity("witch", 0, (1150, 250), 50, 50, 0, 5, witch),
    Entity("chef1", 0, (1300, 500), 10, 10, 0, 3, chef1), Entity("chef2", 0, (1650, 500), 10, 10, 0, 3, chef2),
    Entity("farmer", 0, (1280, 450), 10, 10, 0, 3, farm_m), Entity("farmer", 0, (1530, 450), 10, 10, 0, 3, farm_w),
    Entity("captain", 0, (1270, 480), 50, 50, 0, 5, captain),
    Entity("patrol", 0, (1320, 440), 10, 10, 0, 3, patrol),
    Entity("brave", 0, (-680, 370), 50, 50, 0, 5, brave)
    ]
p1_deck = [
    DamageCard("slash", 2, 5, 0, 0, "image/card/p1/2_slash.png"),
    DamageCard("slash", 2, 5, 0, 0, "image/card/p1/2_slash.png"),
    DamageCard("slash", 2, 5, 0, 0, "image/card/p1/2_slash.png"),
    DefenseCard("defense", 2, 0, 5, "image/card/p1/2_defense.png"),
    DefenseCard("defense", 2, 0, 5, "image/card/p1/2_defense.png"),
    Damdef("1+1", 2, 10, 5, "image/card/p1/2_1+1.png")
    ]
p2_deck = [
    DamageCard("slash", 2, 5, 0, 0, "image/card/p2/2_nox.png"),
    DamageCard("slash", 2, 5, 0, 0, "image/card/p2/2_nox.png"),
    DamageCard("slash", 2, 5, 0, 0, "image/card/p2/2_nox.png"),
    DefenseCard("defense", 2, 0, 5, "image/card/p2/2_defense.png"),
    DefenseCard("defense", 2, 0, 5, "image/card/p2/2_defense.png"),
    Damdef("양손잡이", 2, 10, 5, "image/card/p2/2_two_hands.png")
    ]
en_bar = [
    "image/en_bar/0.png",
    "image/en_bar/1.png",
    "image/en_bar/2.png",
    "image/en_bar/3.png",
    "image/en_bar/4.png",
    "image/en_bar/5.png",
    "image/en_bar/6.png"
]
dirt = DamageCard("흙뿌리기", 2, 7, 0, 0, "image/card/p1/2_dirt.png")
light = DamageCard("라이트", 2, 7, 0, 0, "image/card/p2/2_light.png")
skull = DamageCard("먹보 해골", 2, 2, 0, 0, "image/card/p1/2_hunger_skull.png")
spell = DamageCard("주문 강화", 2, 2, 0, 0, "image/card/p2/2_strengthening_spells.png")
stone = DefenseCard("금강불괴", 3, 0, 25, "image/card/p1/3_like_stone.png")
mirror = DefenseCard("미러 스킨", 3, 0, 25, "image/card/p2/3_mirror_skin.png")
harvest = DamageCard("벼베기", 2, 10, 0, 0, "image/card/p1/2_harvest.png")
dark = DamageCard("먹구름", 2, 10, 0, 0, "image/card/p2/2_dark_clouds.png")
one = Damdef("1+1", 2, 10, 5, "image/card/p1/2_1+1.png")
dual = Damdef("양손잡이", 2, 10, 5, "image/card/p2/2_two_hands.png")
hell = DamageCard("불지옥", 3, 21, 0, 5, "image/card/p1/3_fire_hell.png")
curse = DamageCard("저주", 3, 21, 0, 5, "image/card/p2/3_curse.png")
tric = DefenseCard("밑장빼기", 1, 0, 10, "image/card/p1/1_trickery.png")
eye = DefenseCard("눈속임", 2, 0, 10, "image/card/p2/2_eyewash.png")
weight = DamageCard("신의 무게", 4, 30, 0, 0, "image/card/p1/4_god_weight.png")
meteor = DamageCard("신의 무게", 4, 30, 0, 0, "image/card/p2/4_meteor.png")
x = 0

def warning():
    root = tkinter.Tk()
    root.withdraw()
    tkinter.messagebox.showwarning("경고", "캐릭터를 선택하세요.")

#게임 시작시 나오는 메뉴 화면
def menu():
    play_background_music()
    pygame.display.set_caption("MENU")
    tmr = 0
    global x
    x = 0

    bg_img = [pygame.image.load("image/main/main1.png"), pygame.image.load("image/main/main2.png")]
    p1_default = "image/main/p1_1.png"
    p1_change = "image/main/p1_2.png"
    p2_default = "image/main/p2_1.png"
    p2_change = "image/main/p2_2.png"
    p1_current = p1_default
    p2_current = p2_default

    while True:
        tmr = tmr + 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.blit(bg_img[0], (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_MOUSE_PRESS = pygame.mouse.get_pressed()

        start = button("image/main/start1.png", (266, 938))
        exit = button("image/main/exit1.png", (266, 1071))
        P1 = button(p1_current, (987, 868))
        P2 = button(p2_current, (1589, 868))
        
        start.update()
        exit.update()
        P1.update()
        P2.update()

        #start
        if start.checkmouse(MENU_MOUSE_POS):
            start.button_change(MENU_MOUSE_POS, "image/main/start2.png")
            if MENU_MOUSE_PRESS[0]:
                if x == 0:
                    warning()
                else:
                    main()
        else:
            start.button_change(MENU_MOUSE_POS, "image/main/start1.png")
        
        #exit
        if exit.checkmouse(MENU_MOUSE_POS):
            exit.button_change(MENU_MOUSE_POS, "image/main/exit2.png")
            if MENU_MOUSE_PRESS[0]:
                pygame.quit()
                sys.exit()
        else:
            exit.button_change(MENU_MOUSE_POS, "image/main/exit1.png")
        
        #P1
        if P1.checkmouse(MENU_MOUSE_POS):
            P1.button_change(MENU_MOUSE_POS, "image/main/p1_2.png") 
            if MENU_MOUSE_PRESS[0]:
                p1_current = p1_change
                p2_current = p2_default
                x = 1
        
        #P2
        if P2.checkmouse(MENU_MOUSE_POS):
            P2.button_change(MENU_MOUSE_POS, "image/main/p2_2.png")
            if MENU_MOUSE_PRESS[0]:
                p2_current = p2_change
                p1_current = p1_default
                x = 2

        if MENU_MOUSE_POS[0] in range(0, 2240) and MENU_MOUSE_POS[1] in range(0, 818):
            screen.blit(bg_img[1], (0, 0))
            start.update()
            exit.update()
            P1.update()
            P2.update()

        pygame.display.update()
        clock.tick(100)

#플레이 버튼 눌렀을 때 넘어갈 화면
def main():
    tmr = 0
    screen.fill(BLACK)
    global x
    
    while True:
        tmr = tmr + 1
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_MOUSE_PRESS = pygame.mouse.get_pressed()
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        if x == 1:
            if tmr < 11:
                screen.fill(BLACK)
                screen.blit(map1[tmr % 11], (0,270))
                
        elif x == 2:
            if tmr < 11:
                screen.fill(BLACK)
                screen.blit(map2[tmr % 11], (0,270))

        stand = button("image/map/stand1.png", (189, 655))
        stop = button("image/main/stop1.png", (1940, 100))
        stand.update()
        stop.update()

        #stage_click
        if stand.checkmouse(MENU_MOUSE_POS):
            stand.button_change(MENU_MOUSE_POS, "image/map/stand2.png")
            if MENU_MOUSE_PRESS[0]:
                stop_background_music()
                stage1_1()
        else:
            stand.button_change(MENU_MOUSE_POS, "image/map/stand1.png")

        if stop.checkmouse(MENU_MOUSE_POS):
            pygame.draw.rect(screen, BLACK, stop.rect)
            stop.button_change(MENU_MOUSE_POS, "image/main/stop2.png")
            if MENU_MOUSE_PRESS[0]:
                option()
        else:
            stop.button_change(MENU_MOUSE_POS, "image/main/stop1.png")

        pygame.display.update()
        clock.tick(10)

#스테이지 화면에서 톱니바퀴 누를때
def option():
    tmr = 0
    screen.fill(BLACK)
    global x
    BG = pygame.image.load("image/main/stop_bg.png")

    while True:
        tmr = tmr + 1
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_MOUSE_PRESS = pygame.mouse.get_pressed()
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
        screen.blit(BG, (784, 406))
        title = button("image/main/title1.png", (987, 476))
        exit = button("image/main/exit1.png", (987, 644))
        title.update()
        exit.update()

        if title.checkmouse(MENU_MOUSE_POS):
            title.button_change(MENU_MOUSE_POS, "image/main/title2.png")
            if MENU_MOUSE_PRESS[0]:
                menu()
        else:
            title.button_change(MENU_MOUSE_POS, "image/main/title1.png")

        if exit.checkmouse(MENU_MOUSE_POS):
            exit.button_change(MENU_MOUSE_POS, "image/main/exit2.png")
            if MENU_MOUSE_PRESS[0]:
                pygame.quit()
                sys.exit()
        else:
            exit.button_change(MENU_MOUSE_POS, "image/main/exit1.png")
        
        pygame.display.update()
        clock.tick(100)

def stage1_1():
    tmr = 0
    screen.fill(BLACK)
    global x
    x = x - 1
    if x == 0:
        deck = p1_deck
        attack_animation = Animation(p1_attack_frames, 1)
    elif x == 1:
        deck = p2_deck
        attack_animation = Animation(p2_attack_frames, 1)
    o = []
    P_ch[x].hp = 20
    p_blood = BloodBar(440, 735, P_ch[x].hp, P_ch[x].max_hp)
    defense = ShieldBar(440, 735)
    e1_blood = BloodBar(1280, 735, enemy[0].hp, enemy[0].max_hp)
    e2_blood = BloodBar(1630, 735, enemy[0].hp, enemy[0].max_hp)

    while True:
        tick = 100
        tmr = tmr + 1
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_MOUSE_PRESS = pygame.mouse.get_pressed()
        press = True

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        screen.blit(land[0], (0, 0))
        screen.blit(cover, (0, 0))
        screen.blit(stage[0], (49, 49))

        draw = random.randint(0, len(deck) - 1)
        if tmr < 2:
            for i in range(10):
                draw = random.randint(0, len(deck) - 1)
                if deck[draw] not in o:
                    if len(o) == 0:
                        i = 0
                    elif len(o) == 1:
                        i = 1
                    elif len(o) == 2:
                        i = 2
                    o.append(deck[draw])
                    o[i].update((400 + i * 400, 840))
                if len(o) == 3:
                    break

        if MENU_MOUSE_POS[0] < o[0].rect.left or o[0].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[0].rect.top or o[0].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[0].update((400, 840))
        else:
            if o[0].rect.left <= MENU_MOUSE_POS[0] <= o[0].rect.right and o[0].rect.top <= MENU_MOUSE_POS[1] <= o[0].rect.bottom:
                if MENU_MOUSE_PRESS[0] == press:
                    o[0].rect.x = MENU_MOUSE_POS[0] - o[0].rect.width // 2
                    o[0].rect.y = MENU_MOUSE_POS[1] - o[0].rect.height // 2
                    o[0].update((o[0].rect.x, o[0].rect.y))
                    if MENU_MOUSE_PRESS[2] == True:
                        if enemy[0].rect.colliderect(o[0]):
                            if P_ch[x].cost == 0 or enemy[0].alive == False:
                                o[0].update((400, 840))
                            else:
                                attack_animation.start()
                                o[0].apply_effect(enemy[1], enemy[0], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[0] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
                        elif enemy[1].rect.colliderect(o[0]):
                            if P_ch[x].cost == 0 or enemy[1].alive == False:
                                o[0].update((400, 840))
                            else:
                                attack_animation.start()
                                o[0].apply_effect(enemy[0], enemy[1], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[0] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False

        if MENU_MOUSE_POS[0] < o[1].rect.left or o[1].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[1].rect.top or o[1].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[1].update((800, 840))
        else:
            if o[1].rect.left <= MENU_MOUSE_POS[0] <= o[1].rect.right and o[1].rect.top <= MENU_MOUSE_POS[1] <= o[1].rect.bottom:
                if MENU_MOUSE_PRESS[0] == True:
                    o[1].rect.x = MENU_MOUSE_POS[0] - o[1].rect.width // 2
                    o[1].rect.y = MENU_MOUSE_POS[1] - o[1].rect.height // 2
                    o[1].update((o[1].rect.x, o[1].rect.y))
                    if MENU_MOUSE_PRESS[2] == press:
                        if enemy[0].rect.colliderect(o[1]):
                            if P_ch[x].cost == 0 or enemy[0].alive == False:
                                o[1].update((800, 840))
                            else:
                                attack_animation.start()
                                o[1].apply_effect(enemy[1], enemy[0], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[1] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
                        elif enemy[1].rect.colliderect(o[1]):
                            if P_ch[x].cost == 0 or enemy[1].alive == False:
                                o[1].update((800, 840))
                            else:
                                attack_animation.start()
                                o[1].apply_effect(enemy[0], enemy[1], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[1] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False

        if MENU_MOUSE_POS[0] < o[2].rect.left or o[2].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[2].rect.top or o[2].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[2].update((1200, 840))
        else:
            if o[2].rect.left <= MENU_MOUSE_POS[0] <= o[2].rect.right and o[2].rect.top <= MENU_MOUSE_POS[1] <= o[2].rect.bottom:
                if MENU_MOUSE_PRESS[0] == True:
                    o[2].rect.x = MENU_MOUSE_POS[0] - o[2].rect.width // 2
                    o[2].rect.y = MENU_MOUSE_POS[1] - o[2].rect.height // 2
                    o[2].update((o[2].rect.x, o[2].rect.y))
                    if MENU_MOUSE_PRESS[2] == press:
                        if enemy[0].rect.colliderect(o[2]):
                            if P_ch[x].cost == 0 or enemy[0].alive == False:
                                o[2].update((400, 840))
                            else:
                                attack_animation.start()
                                o[2].apply_effect(enemy[1], enemy[0], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[2] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
                        elif enemy[1].rect.colliderect(o[2]):
                            if P_ch[x].cost == 0 or enemy[1].alive == False:
                                o[2].update((400, 840))
                            else:
                                attack_animation.start()
                                o[2].apply_effect(enemy[0], enemy[1], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[2] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
    
        if attack_animation.is_playing:
            if x == 0:
                attack_animation.play(screen, 256, 231)
            elif x == 1:
                attack_animation.play(screen, 467, 367)
        else:
            if x == 0:
                P_ch[x].image = pygame.image.load(P_1)
            else:
                P_ch[x].image = pygame.image.load(P_2)
            screen.blit(P_ch[x].image, P_ch[x].rect)

        if enemy[0].alive:
     
            enemy[0].image = pygame.image.load(adven1)
            screen.blit(enemy[0].image, enemy[0].rect)
            e1_blood.draw()
            text2 = Nfont.render(f"{enemy[0].hp}", True, (255, 255, 255))
            screen.blit(text2, (1358, 699))
        

        if enemy[1].alive:
            
            enemy[1].image = pygame.image.load(adven2)
            screen.blit(enemy[1].image, enemy[1].rect)
            e2_blood.draw()
            text3 = Nfont.render(f"{enemy[1].hp}", True, (255, 255, 255))
            screen.blit(text3, (1708, 699))



        screen.blit(pygame.image.load(en_bar[P_ch[x].cost]), (56, 280))
        text0 = Nfont.render(f"{P_ch[x].cost}", True, (255, 255, 255))
        screen.blit(text0, (70, 473))

        p_blood.draw()
        text1 = Nfont.render(f"{P_ch[x].hp}", True, (255, 255, 255))
        screen.blit(text1, (518, 699))
        screen.blit(pygame.image.load("image/effect/실드.png"), (363, 714))
        defense.draw(P_ch[x])
        e1_blood.draw()
        text2 = Nfont.render(f"{enemy[0].hp}", True, (255, 255, 255))
        screen.blit(text2, (1358, 699))
        e2_blood.draw()
        text3 = Nfont.render(f"{enemy[1].hp}", True, (255, 255, 255))
        screen.blit(text3, (1708, 699))

        if P_ch[x].hp < 0:
                P_ch[x].hp = 0

        if P_ch[x].hp == 0:
            time.sleep(1)
            sys.exit()

        next_img = "image/button/next_bt/0.png"
        next = button(next_img, (2000, 600))
        if enemy[0].alive == False and enemy[1].alive == False:
            if not next.checkmouse(MENU_MOUSE_POS):
                next.update()
            elif next.checkmouse(MENU_MOUSE_POS):
                next_img = "image/button/next_bt/1.png"
                next = button(next_img, (2000, 600))
                next.update()
                if MENU_MOUSE_PRESS[0] == True:
                    p1_deck.append(dirt)
                    p2_deck.append(light)
                    stage1_2()

        turn = button("image/main/turn_end1.png", (2000, 800))
        turn.update()
        if turn.checkmouse(MENU_MOUSE_POS):
            tick = 10
            turn.button_change(MENU_MOUSE_POS, "image/main/turn_end2.png")
            if MENU_MOUSE_PRESS[0] == True:
                P_ch[x].cost = 6
                if enemy[0].alive == True:
                    enemy[0].action(P_ch[x])
                time.sleep(0.1)
                if enemy[1].alive == True:
                    enemy[1].action(P_ch[x])
                time.sleep(0.1)
                P_ch[x].defense = 0

        pygame.display.update()
        clock.tick(tick)

def stage1_2():
    tmr = 0
    screen.fill(BLACK)
    global x
    if x == 0:
        deck = p1_deck
        attack_animation = Animation(p1_attack_frames, 1)
    elif x == 1:
        deck = p2_deck
        attack_animation = Animation(p2_attack_frames, 1)
    o = []
    P_ch[x].hp = 20
    P_ch[x].cost = 6
    P_ch[x].defense = 0
    p_blood = BloodBar(440, 735, P_ch[x].hp, P_ch[x].max_hp)
    defense = ShieldBar(440, 735)
    e1_blood = BloodBar(1280, 735, enemy[2].hp, enemy[2].max_hp)
    e2_blood = BloodBar(1630, 735, enemy[3].hp, enemy[3].max_hp)

    while True:
        tick = 100
        tmr = tmr + 1
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_MOUSE_PRESS = pygame.mouse.get_pressed()
        press = True

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        screen.blit(land[1], (0, 0))
        screen.blit(cover, (0, 0))
        screen.blit(stage[1], (49, 49))

        draw = random.randint(0, len(deck) - 1)
        if tmr < 2:
            for i in range(10):
                draw = random.randint(0, len(deck) - 1)
                if deck[draw] not in o:
                    if len(o) == 0:
                        i = 0
                    elif len(o) == 1:
                        i = 1
                    elif len(o) == 2:
                        i = 2
                    o.append(deck[draw])
                    o[i].update((400 + i * 400, 840))
                if len(o) == 3:
                    break

        if MENU_MOUSE_POS[0] < o[0].rect.left or o[0].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[0].rect.top or o[0].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[0].update((400, 840))
        else:
            if o[0].rect.left <= MENU_MOUSE_POS[0] <= o[0].rect.right and o[0].rect.top <= MENU_MOUSE_POS[1] <= o[0].rect.bottom:
                if MENU_MOUSE_PRESS[0] == press:
                    o[0].rect.x = MENU_MOUSE_POS[0] - o[0].rect.width // 2
                    o[0].rect.y = MENU_MOUSE_POS[1] - o[0].rect.height // 2
                    o[0].update((o[0].rect.x, o[0].rect.y))
                    if MENU_MOUSE_PRESS[2] == True:
                        if enemy[2].rect.colliderect(o[0]):
                            if P_ch[x].cost == 0 or enemy[2].alive == False:
                                o[0].update((400, 840))
                            else:
                                attack_animation.start()
                                o[0].apply_effect(enemy[3], enemy[2], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[0] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
                        elif enemy[3].rect.colliderect(o[0]):
                            if P_ch[x].cost == 0 or enemy[3].alive == False:
                                o[0].update((400, 840))
                            else:
                                attack_animation.start()
                                o[0].apply_effect(enemy[2], enemy[3], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[0] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False

        if MENU_MOUSE_POS[0] < o[1].rect.left or o[1].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[1].rect.top or o[1].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[1].update((800, 840))
        else:
            if o[1].rect.left <= MENU_MOUSE_POS[0] <= o[1].rect.right and o[1].rect.top <= MENU_MOUSE_POS[1] <= o[1].rect.bottom:
                if MENU_MOUSE_PRESS[0] == True:
                    o[1].rect.x = MENU_MOUSE_POS[0] - o[1].rect.width // 2
                    o[1].rect.y = MENU_MOUSE_POS[1] - o[1].rect.height // 2
                    o[1].update((o[1].rect.x, o[1].rect.y))
                    if MENU_MOUSE_PRESS[2] == press:
                        if enemy[2].rect.colliderect(o[1]):
                            if P_ch[x].cost == 0 or enemy[2].alive == False:
                                o[1].update((800, 840))
                            else:
                                attack_animation.start()
                                o[1].apply_effect(enemy[3], enemy[2], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[1] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
                        elif enemy[3].rect.colliderect(o[1]):
                            if P_ch[x].cost == 0 or enemy[3].alive == False:
                                o[1].update((800, 840))
                            else:
                                attack_animation.start()
                                o[1].apply_effect(enemy[2], enemy[3], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[1] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False

        if MENU_MOUSE_POS[0] < o[2].rect.left or o[2].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[2].rect.top or o[2].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[2].update((1200, 840))
        else:
            if o[2].rect.left <= MENU_MOUSE_POS[0] <= o[2].rect.right and o[2].rect.top <= MENU_MOUSE_POS[1] <= o[2].rect.bottom:
                if MENU_MOUSE_PRESS[0] == True:
                    o[2].rect.x = MENU_MOUSE_POS[0] - o[2].rect.width // 2
                    o[2].rect.y = MENU_MOUSE_POS[1] - o[2].rect.height // 2
                    o[2].update((o[2].rect.x, o[2].rect.y))
                    if MENU_MOUSE_PRESS[2] == press:
                        if enemy[2].rect.colliderect(o[2]):
                            if P_ch[x].cost == 0 or enemy[2].alive == False:
                                o[2].update((400, 840))
                            else:
                                attack_animation.start()
                                o[2].apply_effect(enemy[3], enemy[2], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[2] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
                        elif enemy[3].rect.colliderect(o[2]):
                            if P_ch[x].cost == 0 or enemy[3].alive == False:
                                o[2].update((400, 840))
                            else:
                                attack_animation.start()
                                o[2].apply_effect(enemy[2], enemy[3], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[2] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
    
        if attack_animation.is_playing:
            if x == 0:
                attack_animation.play(screen, 256, 231)
            elif x == 1:
                attack_animation.play(screen, 467, 367)
        else:
            if x == 0:
                P_ch[x].image = pygame.image.load(P_1)
            else:
                P_ch[x].image = pygame.image.load(P_2)
            screen.blit(P_ch[x].image, P_ch[x].rect)

        if enemy[2].alive:
     
            enemy[2].image = pygame.image.load(archer1)
            screen.blit(enemy[2].image, enemy[2].rect)
            e1_blood.draw()
            text2 = Nfont.render(f"{enemy[2].hp}", True, (255, 255, 255))
            screen.blit(text2, (1358, 699))
        

        if enemy[3].alive:
            
            enemy[3].image = pygame.image.load(archer2)
            screen.blit(enemy[3].image, enemy[3].rect)
            e2_blood.draw()
            text3 = Nfont.render(f"{enemy[1].hp}", True, (255, 255, 255))
            screen.blit(text3, (1708, 699))



        screen.blit(pygame.image.load(en_bar[P_ch[x].cost]), (56, 280))
        text0 = Nfont.render(f"{P_ch[x].cost}", True, (255, 255, 255))
        screen.blit(text0, (70, 473))

        p_blood.draw()
        text1 = Nfont.render(f"{P_ch[x].hp}", True, (255, 255, 255))
        screen.blit(text1, (518, 699))
        screen.blit(pygame.image.load("image/effect/실드.png"), (363, 714))
        defense.draw(P_ch[x])
        e1_blood.draw()
        text2 = Nfont.render(f"{enemy[2].hp}", True, (255, 255, 255))
        screen.blit(text2, (1358, 699))
        e2_blood.draw()
        text3 = Nfont.render(f"{enemy[3].hp}", True, (255, 255, 255))
        screen.blit(text3, (1708, 699))

        if P_ch[x].hp < 0:
                P_ch[x].hp = 0

        if P_ch[x].hp == 0:
            time.sleep(1)
            sys.exit()

        next_img = "image/button/next_bt/0.png"
        next = button(next_img, (2000, 600))
        if enemy[2].alive == False and enemy[3].alive == False:
            if not next.checkmouse(MENU_MOUSE_POS):
                next.update()
            elif next.checkmouse(MENU_MOUSE_POS):
                next_img = "image/button/next_bt/1.png"
                next = button(next_img, (2000, 600))
                next.update()
                if MENU_MOUSE_PRESS[0] == True:
                    p1_deck.append(skull)
                    p2_deck.append(spell)
                    stage1_3()

        turn = button("image/main/turn_end1.png", (2000, 800))
        turn.update()
        if turn.checkmouse(MENU_MOUSE_POS):
            tick = 10
            turn.button_change(MENU_MOUSE_POS, "image/main/turn_end2.png")
            if MENU_MOUSE_PRESS[0] == True:
                P_ch[x].cost = 6
                if enemy[2].alive == True:
                    enemy[2].action(P_ch[x])
                time.sleep(0.1)
                if enemy[3].alive == True:
                    enemy[3].action(P_ch[x])
                time.sleep(0.1)
                P_ch[x].defense = 0

        pygame.display.update()
        clock.tick(tick)

def stage1_3():
    tmr = 0
    screen.fill(BLACK)
    global x
    if x == 0:
        deck = p1_deck
        attack_animation = Animation(p1_attack_frames, 1)
    elif x == 1:
        deck = p2_deck
        attack_animation = Animation(p2_attack_frames, 1)
    o = []
    P_ch[x].hp = 20
    P_ch[x].cost = 6
    P_ch[x].defense = 0
    p_blood = BloodBar(440, 735, P_ch[x].hp, P_ch[x].max_hp)
    defense = ShieldBar(440, 735)
    e1_blood = BloodBar(1280, 735, enemy[4].hp, enemy[4].max_hp)

    while True:
        tick = 100
        tmr = tmr + 1
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_MOUSE_PRESS = pygame.mouse.get_pressed()
        press = True

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        screen.blit(land[2], (0, 0))
        screen.blit(cover, (0, 0))
        screen.blit(stage[2], (49, 49))

        draw = random.randint(0, len(deck) - 1)
        if tmr < 2:
            for i in range(10):
                draw = random.randint(0, len(deck) - 1)
                if deck[draw] not in o:
                    if len(o) == 0:
                        i = 0
                    elif len(o) == 1:
                        i = 1
                    elif len(o) == 2:
                        i = 2
                    o.append(deck[draw])
                    o[i].update((400 + i * 400, 840))
                if len(o) == 3:
                    break

        if MENU_MOUSE_POS[0] < o[0].rect.left or o[0].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[0].rect.top or o[0].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[0].update((400, 840))
        else:
            if o[0].rect.left <= MENU_MOUSE_POS[0] <= o[0].rect.right and o[0].rect.top <= MENU_MOUSE_POS[1] <= o[0].rect.bottom:
                if MENU_MOUSE_PRESS[0] == press:
                    o[0].rect.x = MENU_MOUSE_POS[0] - o[0].rect.width // 2
                    o[0].rect.y = MENU_MOUSE_POS[1] - o[0].rect.height // 2
                    o[0].update((o[0].rect.x, o[0].rect.y))
                    if MENU_MOUSE_PRESS[2] == True:
                        if enemy[4].rect.colliderect(o[0]):
                            if P_ch[x].cost == 0 or enemy[4].alive == False:
                                o[0].update((400, 840))
                            else:
                                attack_animation.start()
                                o[0].apply_effect(enemy[4], enemy[4], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[0] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False

        if MENU_MOUSE_POS[0] < o[1].rect.left or o[1].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[1].rect.top or o[1].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[1].update((800, 840))
        else:
            if o[1].rect.left <= MENU_MOUSE_POS[0] <= o[1].rect.right and o[1].rect.top <= MENU_MOUSE_POS[1] <= o[1].rect.bottom:
                if MENU_MOUSE_PRESS[0] == True:
                    o[1].rect.x = MENU_MOUSE_POS[0] - o[1].rect.width // 2
                    o[1].rect.y = MENU_MOUSE_POS[1] - o[1].rect.height // 2
                    o[1].update((o[1].rect.x, o[1].rect.y))
                    if MENU_MOUSE_PRESS[2] == press:
                        if enemy[4].rect.colliderect(o[1]):
                            if P_ch[x].cost == 0 or enemy[4].alive == False:
                                o[1].update((800, 840))
                            else:
                                attack_animation.start()
                                o[1].apply_effect(enemy[4], enemy[4], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[1] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
                        
        if MENU_MOUSE_POS[0] < o[2].rect.left or o[2].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[2].rect.top or o[2].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[2].update((1200, 840))
        else:
            if o[2].rect.left <= MENU_MOUSE_POS[0] <= o[2].rect.right and o[2].rect.top <= MENU_MOUSE_POS[1] <= o[2].rect.bottom:
                if MENU_MOUSE_PRESS[0] == True:
                    o[2].rect.x = MENU_MOUSE_POS[0] - o[2].rect.width // 2
                    o[2].rect.y = MENU_MOUSE_POS[1] - o[2].rect.height // 2
                    o[2].update((o[2].rect.x, o[2].rect.y))
                    if MENU_MOUSE_PRESS[2] == press:
                        if enemy[4].rect.colliderect(o[2]):
                            if P_ch[x].cost == 0 or enemy[4].alive == False:
                                o[2].update((400, 840))
                            else:
                                attack_animation.start()
                                o[2].apply_effect(enemy[4], enemy[4], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[2] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
                        
        if attack_animation.is_playing:
            if x == 0:
                attack_animation.play(screen, 256, 231)
            elif x == 1:
                attack_animation.play(screen, 467, 367)
        else:
            if x == 0:
                P_ch[x].image = pygame.image.load(P_1)
            else:
                P_ch[x].image = pygame.image.load(P_2)
            screen.blit(P_ch[x].image, P_ch[x].rect)

        enemy[4].image = pygame.image.load(witch)
        screen.blit(enemy[4].image, enemy[4].rect)

        screen.blit(pygame.image.load(en_bar[P_ch[x].cost]), (56, 280))
        text0 = Nfont.render(f"{P_ch[x].cost}", True, (255, 255, 255))
        screen.blit(text0, (70, 473))

        p_blood.draw()
        text1 = Nfont.render(f"{P_ch[x].hp}", True, (255, 255, 255))
        screen.blit(text1, (518, 699))
        screen.blit(pygame.image.load("image/effect/실드.png"), (363, 714))
        defense.draw(P_ch[x])
        e1_blood.draw()
        text2 = Nfont.render(f"{enemy[4].hp}", True, (255, 255, 255))
        screen.blit(text2, (1360, 699))

        if P_ch[x].hp < 0:
                P_ch[x].hp = 0

        if P_ch[x].hp == 0:
            time.sleep(1)
            sys.exit()

        next_img = "image/button/next_bt/0.png"
        next = button(next_img, (2000, 600))
        if enemy[4].alive == False:
            if not next.checkmouse(MENU_MOUSE_POS):
                next.update()
            elif next.checkmouse(MENU_MOUSE_POS):
                next_img = "image/button/next_bt/1.png"
                next = button(next_img, (2000, 600))
                next.update()
                if MENU_MOUSE_PRESS[0] == True:
                    skull.damage = 2
                    spell.damage = 2
                    p1_deck.append(stone)
                    p2_deck.append(mirror)
                    stage2_1()

        turn = button("image/main/turn_end1.png", (2000, 800))
        turn.update()
        if turn.checkmouse(MENU_MOUSE_POS):
            tick = 10
            turn.button_change(MENU_MOUSE_POS, "image/main/turn_end2.png")
            if MENU_MOUSE_PRESS[0] == True:
                P_ch[x].cost = 6
                if enemy[4].alive == True:
                    enemy[4].action(P_ch[x])
                time.sleep(0.1)
                P_ch[x].defense = 0

        pygame.display.update()
        clock.tick(tick)

def stage2_1():
    tmr = 0
    screen.fill(BLACK)
    global x
    if x == 0:
        deck = p1_deck
        attack_animation = Animation(p1_attack_frames, 1)
    elif x == 1:
        deck = p2_deck
        attack_animation = Animation(p2_attack_frames, 1)
    o = []
    P_ch[x].hp = 20
    P_ch[x].cost = 6
    P_ch[x].defense = 0
    p_blood = BloodBar(440, 735, P_ch[x].hp, P_ch[x].max_hp)
    defense = ShieldBar(440, 735)
    e1_blood = BloodBar(1280, 735, enemy[5].hp, enemy[5].max_hp)
    e2_blood = BloodBar(1630, 735, enemy[6].hp, enemy[6].max_hp)

    while True:
        tick = 100
        tmr = tmr + 1
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_MOUSE_PRESS = pygame.mouse.get_pressed()
        press = True

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        screen.blit(land[3], (0, 0))
        screen.blit(cover, (0, 0))
        screen.blit(stage[3], (49, 49))

        draw = random.randint(0, len(deck) - 1)
        if tmr < 2:
            for i in range(10):
                draw = random.randint(0, len(deck) - 1)
                if deck[draw] not in o:
                    if len(o) == 0:
                        i = 0
                    elif len(o) == 1:
                        i = 1
                    elif len(o) == 2:
                        i = 2
                    o.append(deck[draw])
                    o[i].update((400 + i * 400, 840))
                if len(o) == 3:
                    break

        if MENU_MOUSE_POS[0] < o[0].rect.left or o[0].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[0].rect.top or o[0].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[0].update((400, 840))
        else:
            if o[0].rect.left <= MENU_MOUSE_POS[0] <= o[0].rect.right and o[0].rect.top <= MENU_MOUSE_POS[1] <= o[0].rect.bottom:
                if MENU_MOUSE_PRESS[0] == press:
                    o[0].rect.x = MENU_MOUSE_POS[0] - o[0].rect.width // 2
                    o[0].rect.y = MENU_MOUSE_POS[1] - o[0].rect.height // 2
                    o[0].update((o[0].rect.x, o[0].rect.y))
                    if MENU_MOUSE_PRESS[2] == True:
                        if enemy[5].rect.colliderect(o[0]):
                            if P_ch[x].cost == 0 or enemy[5].alive == False:
                                o[0].update((400, 840))
                            else:
                                attack_animation.start()
                                o[0].apply_effect(enemy[6], enemy[5], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[0] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
                        elif enemy[6].rect.colliderect(o[0]):
                            if P_ch[x].cost == 0 or enemy[6].alive == False:
                                o[0].update((400, 840))
                            else:
                                attack_animation.start()
                                o[0].apply_effect(enemy[5], enemy[6], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[0] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False

        if MENU_MOUSE_POS[0] < o[1].rect.left or o[1].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[1].rect.top or o[1].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[1].update((800, 840))
        else:
            if o[1].rect.left <= MENU_MOUSE_POS[0] <= o[1].rect.right and o[1].rect.top <= MENU_MOUSE_POS[1] <= o[1].rect.bottom:
                if MENU_MOUSE_PRESS[0] == True:
                    o[1].rect.x = MENU_MOUSE_POS[0] - o[1].rect.width // 2
                    o[1].rect.y = MENU_MOUSE_POS[1] - o[1].rect.height // 2
                    o[1].update((o[1].rect.x, o[1].rect.y))
                    if MENU_MOUSE_PRESS[2] == press:
                        if enemy[5].rect.colliderect(o[1]):
                            if P_ch[x].cost == 0 or enemy[5].alive == False:
                                o[1].update((800, 840))
                            else:
                                attack_animation.start()
                                o[1].apply_effect(enemy[6], enemy[5], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[1] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
                        elif enemy[6].rect.colliderect(o[1]):
                            if P_ch[x].cost == 0 or enemy[6].alive == False:
                                o[1].update((800, 840))
                            else:
                                attack_animation.start()
                                o[1].apply_effect(enemy[5], enemy[6], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[1] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False

        if MENU_MOUSE_POS[0] < o[2].rect.left or o[2].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[2].rect.top or o[2].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[2].update((1200, 840))
        else:
            if o[2].rect.left <= MENU_MOUSE_POS[0] <= o[2].rect.right and o[2].rect.top <= MENU_MOUSE_POS[1] <= o[2].rect.bottom:
                if MENU_MOUSE_PRESS[0] == True:
                    o[2].rect.x = MENU_MOUSE_POS[0] - o[2].rect.width // 2
                    o[2].rect.y = MENU_MOUSE_POS[1] - o[2].rect.height // 2
                    o[2].update((o[2].rect.x, o[2].rect.y))
                    if MENU_MOUSE_PRESS[2] == press:
                        if enemy[5].rect.colliderect(o[2]):
                            if P_ch[x].cost == 0 or enemy[5].alive == False:
                                o[2].update((400, 840))
                            else:
                                attack_animation.start()
                                o[2].apply_effect(enemy[6], enemy[5], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[2] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
                        elif enemy[6].rect.colliderect(o[2]):
                            if P_ch[x].cost == 0 or enemy[6].alive == False:
                                o[2].update((400, 840))
                            else:
                                attack_animation.start()
                                o[2].apply_effect(enemy[5], enemy[6], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[2] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
    
        if attack_animation.is_playing:
            if x == 0:
                attack_animation.play(screen, 256, 231)
            elif x == 1:
                attack_animation.play(screen, 467, 367)
        else:
            if x == 0:
                P_ch[x].image = pygame.image.load(P_1)
            else:
                P_ch[x].image = pygame.image.load(P_2)
            screen.blit(P_ch[x].image, P_ch[x].rect)

        if enemy[5].alive:
     
            enemy[5].image = pygame.image.load(chef1)
            screen.blit(enemy[5].image, enemy[5].rect)
            e1_blood.draw()
            text2 = Nfont.render(f"{enemy[5].hp}", True, (255, 255, 255))
            screen.blit(text2, (1358, 699))
        

        if enemy[6].alive:
            
            enemy[6].image = pygame.image.load(chef2)
            screen.blit(enemy[6].image, enemy[6].rect)
            e2_blood.draw()
            text3 = Nfont.render(f"{enemy[6].hp}", True, (255, 255, 255))
            screen.blit(text3, (1708, 699))


        screen.blit(pygame.image.load(en_bar[P_ch[x].cost]), (56, 280))
        text0 = Nfont.render(f"{P_ch[x].cost}", True, (255, 255, 255))
        screen.blit(text0, (70, 473))

        p_blood.draw()
        text1 = Nfont.render(f"{P_ch[x].hp}", True, (255, 255, 255))
        screen.blit(text1, (518, 699))
        screen.blit(pygame.image.load("image/effect/실드.png"), (363, 714))
        defense.draw(P_ch[x])
        e1_blood.draw()
        text2 = Nfont.render(f"{enemy[5].hp}", True, (255, 255, 255))
        screen.blit(text2, (1358, 699))
        e2_blood.draw()
        text3 = Nfont.render(f"{enemy[6].hp}", True, (255, 255, 255))
        screen.blit(text3, (1708, 699))

        if P_ch[x].hp < 0:
                P_ch[x].hp = 0

        if P_ch[x].hp == 0:
            time.sleep(1)
            sys.exit()

        next_img = "image/button/next_bt/0.png"
        next = button(next_img, (2000, 600))
        if enemy[5].alive == False and enemy[6].alive == False:
            if not next.checkmouse(MENU_MOUSE_POS):
                next.update()
            elif next.checkmouse(MENU_MOUSE_POS):
                next_img = "image/button/next_bt/1.png"
                next = button(next_img, (2000, 600))
                next.update()
                if MENU_MOUSE_PRESS[0] == True:
                    skull.damage = 2
                    spell.damage = 2
                    p1_deck.append(harvest)
                    p2_deck.append(dark)
                    stage2_2()

        turn = button("image/main/turn_end1.png", (2000, 800))
        turn.update()
        if turn.checkmouse(MENU_MOUSE_POS):
            tick = 10
            turn.button_change(MENU_MOUSE_POS, "image/main/turn_end2.png")
            if MENU_MOUSE_PRESS[0] == True:
                P_ch[x].cost = 6
                if enemy[5].alive == True:
                    enemy[5].action(P_ch[x])
                time.sleep(0.1)
                if enemy[6].alive == True:
                    enemy[6].action(P_ch[x])
                time.sleep(0.1)
                P_ch[x].defense = 0

        pygame.display.update()
        clock.tick(tick)

def stage2_2():
    tmr = 0
    screen.fill(BLACK)
    global x
    if x == 0:
        deck = p1_deck
        attack_animation = Animation(p1_attack_frames, 1)
    elif x == 1:
        deck = p2_deck
        attack_animation = Animation(p2_attack_frames, 1)
    o = []
    P_ch[x].hp = 20
    P_ch[x].cost = 6
    P_ch[x].defense = 0
    p_blood = BloodBar(440, 735, P_ch[x].hp, P_ch[x].max_hp)
    defense = ShieldBar(440, 735)
    e1_blood = BloodBar(1280, 735, enemy[7].hp, enemy[7].max_hp)
    e2_blood = BloodBar(1630, 735, enemy[8].hp, enemy[8].max_hp)

    while True:
        tick = 100
        tmr = tmr + 1
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_MOUSE_PRESS = pygame.mouse.get_pressed()
        press = True

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        screen.blit(land[4], (0, 0))
        screen.blit(cover, (0, 0))
        screen.blit(stage[4], (49, 49))

        draw = random.randint(0, len(deck) - 1)
        if tmr < 2:
            for i in range(10):
                draw = random.randint(0, len(deck) - 1)
                if deck[draw] not in o:
                    if len(o) == 0:
                        i = 0
                    elif len(o) == 1:
                        i = 1
                    elif len(o) == 2:
                        i = 2
                    o.append(deck[draw])
                    o[i].update((400 + i * 400, 840))
                if len(o) == 3:
                    break

        if MENU_MOUSE_POS[0] < o[0].rect.left or o[0].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[0].rect.top or o[0].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[0].update((400, 840))
        else:
            if o[0].rect.left <= MENU_MOUSE_POS[0] <= o[0].rect.right and o[0].rect.top <= MENU_MOUSE_POS[1] <= o[0].rect.bottom:
                if MENU_MOUSE_PRESS[0] == press:
                    o[0].rect.x = MENU_MOUSE_POS[0] - o[0].rect.width // 2
                    o[0].rect.y = MENU_MOUSE_POS[1] - o[0].rect.height // 2
                    o[0].update((o[0].rect.x, o[0].rect.y))
                    if MENU_MOUSE_PRESS[2] == True:
                        if enemy[7].rect.colliderect(o[0]):
                            if P_ch[x].cost == 0 or enemy[7].alive == False:
                                o[0].update((400, 840))
                            else:
                                attack_animation.start()
                                o[0].apply_effect(enemy[8], enemy[7], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[0] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
                        elif enemy[8].rect.colliderect(o[0]):
                            if P_ch[x].cost == 0 or enemy[8].alive == False:
                                o[0].update((400, 840))
                            else:
                                attack_animation.start()
                                o[0].apply_effect(enemy[7], enemy[8], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[0] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False

        if MENU_MOUSE_POS[0] < o[1].rect.left or o[1].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[1].rect.top or o[1].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[1].update((800, 840))
        else:
            if o[1].rect.left <= MENU_MOUSE_POS[0] <= o[1].rect.right and o[1].rect.top <= MENU_MOUSE_POS[1] <= o[1].rect.bottom:
                if MENU_MOUSE_PRESS[0] == True:
                    o[1].rect.x = MENU_MOUSE_POS[0] - o[1].rect.width // 2
                    o[1].rect.y = MENU_MOUSE_POS[1] - o[1].rect.height // 2
                    o[1].update((o[1].rect.x, o[1].rect.y))
                    if MENU_MOUSE_PRESS[2] == press:
                        if enemy[7].rect.colliderect(o[1]):
                            if P_ch[x].cost == 0 or enemy[7].alive == False:
                                o[1].update((800, 840))
                            else:
                                attack_animation.start()
                                o[1].apply_effect(enemy[8], enemy[7], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[1] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
                        elif enemy[8].rect.colliderect(o[1]):
                            if P_ch[x].cost == 0 or enemy[8].alive == False:
                                o[1].update((800, 840))
                            else:
                                attack_animation.start()
                                o[1].apply_effect(enemy[7], enemy[8], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[1] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False

        if MENU_MOUSE_POS[0] < o[2].rect.left or o[2].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[2].rect.top or o[2].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[2].update((1200, 840))
        else:
            if o[2].rect.left <= MENU_MOUSE_POS[0] <= o[2].rect.right and o[2].rect.top <= MENU_MOUSE_POS[1] <= o[2].rect.bottom:
                if MENU_MOUSE_PRESS[0] == True:
                    o[2].rect.x = MENU_MOUSE_POS[0] - o[2].rect.width // 2
                    o[2].rect.y = MENU_MOUSE_POS[1] - o[2].rect.height // 2
                    o[2].update((o[2].rect.x, o[2].rect.y))
                    if MENU_MOUSE_PRESS[2] == press:
                        if enemy[7].rect.colliderect(o[2]):
                            if P_ch[x].cost == 0 or enemy[7].alive == False:
                                o[2].update((400, 840))
                            else:
                                attack_animation.start()
                                o[2].apply_effect(enemy[8], enemy[7], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[2] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
                        elif enemy[8].rect.colliderect(o[2]):
                            if P_ch[x].cost == 0 or enemy[8].alive == False:
                                o[2].update((400, 840))
                            else:
                                attack_animation.start()
                                o[2].apply_effect(enemy[7], enemy[8], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[2] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
    
        if attack_animation.is_playing:
            if x == 0:
                attack_animation.play(screen, 256, 231)
            elif x == 1:
                attack_animation.play(screen, 467, 367)
        else:
            if x == 0:
                P_ch[x].image = pygame.image.load(P_1)
            else:
                P_ch[x].image = pygame.image.load(P_2)
            screen.blit(P_ch[x].image, P_ch[x].rect)

        if enemy[7].alive:
     
            enemy[7].image = pygame.image.load(farm_m)
            screen.blit(enemy[7].image, enemy[7].rect)
            e1_blood.draw()
            text2 = Nfont.render(f"{enemy[7].hp}", True, (255, 255, 255))
            screen.blit(text2, (1358, 699))
        

        if enemy[8].alive:
            
            enemy[8].image = pygame.image.load(farm_w)
            screen.blit(enemy[8].image, enemy[8].rect)
            e2_blood.draw()
            text3 = Nfont.render(f"{enemy[8].hp}", True, (255, 255, 255))
            screen.blit(text3, (1708, 699))



        screen.blit(pygame.image.load(en_bar[P_ch[x].cost]), (56, 280))
        text0 = Nfont.render(f"{P_ch[x].cost}", True, (255, 255, 255))
        screen.blit(text0, (70, 473))

        p_blood.draw()
        text1 = Nfont.render(f"{P_ch[x].hp}", True, (255, 255, 255))
        screen.blit(text1, (518, 699))
        screen.blit(pygame.image.load("image/effect/실드.png"), (363, 714))
        defense.draw(P_ch[x])
        e1_blood.draw()
        text2 = Nfont.render(f"{enemy[7].hp}", True, (255, 255, 255))
        screen.blit(text2, (1358, 699))
        e2_blood.draw()
        text3 = Nfont.render(f"{enemy[8].hp}", True, (255, 255, 255))
        screen.blit(text3, (1708, 699))

        if P_ch[x].hp < 0:
                P_ch[x].hp = 0

        if P_ch[x].hp == 0:
            time.sleep(1)
            sys.exit()

        next_img = "image/button/next_bt/0.png"
        next = button(next_img, (2000, 600))
        if enemy[7].alive == False and enemy[8].alive == False:
            if not next.checkmouse(MENU_MOUSE_POS):
                next.update()
            elif next.checkmouse(MENU_MOUSE_POS):
                next_img = "image/button/next_bt/1.png"
                next = button(next_img, (2000, 600))
                next.update()
                if MENU_MOUSE_PRESS[0] == True:
                    skull.damage = 2
                    spell.damage = 2
                    p1_deck.append(one)
                    p2_deck.append(dual)
                    stage2_3()

        turn = button("image/main/turn_end1.png", (2000, 800))
        turn.update()
        if turn.checkmouse(MENU_MOUSE_POS):
            tick = 10
            turn.button_change(MENU_MOUSE_POS, "image/main/turn_end2.png")
            if MENU_MOUSE_PRESS[0] == True:
                P_ch[x].cost = 6
                if enemy[7].alive == True:
                    enemy[7].action(P_ch[x])
                time.sleep(0.1)
                if enemy[8].alive == True:
                    enemy[8].action(P_ch[x])
                time.sleep(0.1)
                P_ch[x].defense = 0

        pygame.display.update()
        clock.tick(tick)

def stage2_3():
    tmr = 0
    screen.fill(BLACK)
    global x
    if x == 0:
        deck = p1_deck
        attack_animation = Animation(p1_attack_frames, 1)
    elif x == 1:
        deck = p2_deck
        attack_animation = Animation(p2_attack_frames, 1)
    o = []
    P_ch[x].hp = 20
    P_ch[x].cost = 6
    P_ch[x].defense = 0
    p_blood = BloodBar(440, 735, P_ch[x].hp, P_ch[x].max_hp)
    defense = ShieldBar(440, 735)
    e1_blood = BloodBar(1280, 735, enemy[9].hp, enemy[9].max_hp)

    while True:
        tick = 100
        tmr = tmr + 1
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_MOUSE_PRESS = pygame.mouse.get_pressed()
        press = True

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        screen.blit(land[5], (0, 0))
        screen.blit(cover, (0, 0))
        screen.blit(stage[5], (49, 49))

        draw = random.randint(0, len(deck) - 1)
        if tmr < 2:
            for i in range(10):
                draw = random.randint(0, len(deck) - 1)
                if deck[draw] not in o:
                    if len(o) == 0:
                        i = 0
                    elif len(o) == 1:
                        i = 1
                    elif len(o) == 2:
                        i = 2
                    o.append(deck[draw])
                    o[i].update((400 + i * 400, 840))
                if len(o) == 3:
                    break

        if MENU_MOUSE_POS[0] < o[0].rect.left or o[0].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[0].rect.top or o[0].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[0].update((400, 840))
        else:
            if o[0].rect.left <= MENU_MOUSE_POS[0] <= o[0].rect.right and o[0].rect.top <= MENU_MOUSE_POS[1] <= o[0].rect.bottom:
                if MENU_MOUSE_PRESS[0] == press:
                    o[0].rect.x = MENU_MOUSE_POS[0] - o[0].rect.width // 2
                    o[0].rect.y = MENU_MOUSE_POS[1] - o[0].rect.height // 2
                    o[0].update((o[0].rect.x, o[0].rect.y))
                    if MENU_MOUSE_PRESS[2] == True:
                        if enemy[9].rect.colliderect(o[0]):
                            if P_ch[x].cost == 0 or enemy[9].alive == False:
                                o[0].update((400, 840))
                            else:
                                attack_animation.start()
                                o[0].apply_effect(enemy[9], enemy[9], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[0] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False

        if MENU_MOUSE_POS[0] < o[1].rect.left or o[1].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[1].rect.top or o[1].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[1].update((800, 840))
        else:
            if o[1].rect.left <= MENU_MOUSE_POS[0] <= o[1].rect.right and o[1].rect.top <= MENU_MOUSE_POS[1] <= o[1].rect.bottom:
                if MENU_MOUSE_PRESS[0] == True:
                    o[1].rect.x = MENU_MOUSE_POS[0] - o[1].rect.width // 2
                    o[1].rect.y = MENU_MOUSE_POS[1] - o[1].rect.height // 2
                    o[1].update((o[1].rect.x, o[1].rect.y))
                    if MENU_MOUSE_PRESS[2] == press:
                        if enemy[9].rect.colliderect(o[1]):
                            if P_ch[x].cost == 0 or enemy[9].alive == False:
                                o[1].update((800, 840))
                            else:
                                attack_animation.start()
                                o[1].apply_effect(enemy[9], enemy[9], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[1] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
                        
        if MENU_MOUSE_POS[0] < o[2].rect.left or o[2].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[2].rect.top or o[2].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[2].update((1200, 840))
        else:
            if o[2].rect.left <= MENU_MOUSE_POS[0] <= o[2].rect.right and o[2].rect.top <= MENU_MOUSE_POS[1] <= o[2].rect.bottom:
                if MENU_MOUSE_PRESS[0] == True:
                    o[2].rect.x = MENU_MOUSE_POS[0] - o[2].rect.width // 2
                    o[2].rect.y = MENU_MOUSE_POS[1] - o[2].rect.height // 2
                    o[2].update((o[2].rect.x, o[2].rect.y))
                    if MENU_MOUSE_PRESS[2] == press:
                        if enemy[9].rect.colliderect(o[2]):
                            if P_ch[x].cost == 0 or enemy[9].alive == False:
                                o[2].update((400, 840))
                            else:
                                attack_animation.start()
                                o[2].apply_effect(enemy[9], enemy[9], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[2] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
                        
        if attack_animation.is_playing:
            if x == 0:
                attack_animation.play(screen, 256, 231)
            elif x == 1:
                attack_animation.play(screen, 467, 367)
        else:
            if x == 0:
                P_ch[x].image = pygame.image.load(P_1)
            else:
                P_ch[x].image = pygame.image.load(P_2)
            screen.blit(P_ch[x].image, P_ch[x].rect)

        enemy[9].image = pygame.image.load(captain)
        screen.blit(enemy[9].image, enemy[9].rect)

        screen.blit(pygame.image.load(en_bar[P_ch[x].cost]), (56, 280))
        text0 = Nfont.render(f"{P_ch[x].cost}", True, (255, 255, 255))
        screen.blit(text0, (70, 473))

        p_blood.draw()
        text1 = Nfont.render(f"{P_ch[x].hp}", True, (255, 255, 255))
        screen.blit(text1, (518, 699))
        screen.blit(pygame.image.load("image/effect/실드.png"), (363, 714))
        defense.draw(P_ch[x])
        e1_blood.draw()
        text2 = Nfont.render(f"{enemy[9].hp}", True, (255, 255, 255))
        screen.blit(text2, (1360, 699))

        if P_ch[x].hp < 0:
                P_ch[x].hp = 0

        if P_ch[x].hp == 0:
            time.sleep(1)
            sys.exit()

        next_img = "image/button/next_bt/0.png"
        next = button(next_img, (2000, 600))
        if enemy[9].alive == False:
            if not next.checkmouse(MENU_MOUSE_POS):
                next.update()
            elif next.checkmouse(MENU_MOUSE_POS):
                next_img = "image/button/next_bt/1.png"
                next = button(next_img, (2000, 600))
                next.update()
                if MENU_MOUSE_PRESS[0] == True:
                    skull.damage = 2
                    spell.damage = 2
                    p1_deck.append(hell)
                    p2_deck.append(curse)
                    stage3_1()

        turn = button("image/main/turn_end1.png", (2000, 800))
        turn.update()
        if turn.checkmouse(MENU_MOUSE_POS):
            tick = 10
            turn.button_change(MENU_MOUSE_POS, "image/main/turn_end2.png")
            if MENU_MOUSE_PRESS[0] == True:
                P_ch[x].cost = 6
                if enemy[9].alive == True:
                    enemy[9].action(P_ch[x])
                time.sleep(0.1)
                P_ch[x].defense = 0

        pygame.display.update()
        clock.tick(tick)

def stage3_1():
    tmr = 0
    screen.fill(BLACK)
    global x
    if x == 0:
        deck = p1_deck
        attack_animation = Animation(p1_attack_frames, 1)
    elif x == 1:
        deck = p2_deck
        attack_animation = Animation(p2_attack_frames, 1)
    o = []
    enemy[6].hp = 10
    enemy[6].alive = True
    P_ch[x].hp = 20
    P_ch[x].cost = 6
    P_ch[x].defense = 0
    p_blood = BloodBar(440, 735, P_ch[x].hp, P_ch[x].max_hp)
    defense = ShieldBar(440, 735)
    e1_blood = BloodBar(1280, 735, enemy[10].hp, enemy[10].max_hp)
    e2_blood = BloodBar(1630, 735, enemy[6].hp, enemy[6].max_hp)

    while True:
        tick = 100
        tmr = tmr + 1
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_MOUSE_PRESS = pygame.mouse.get_pressed()
        press = True

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        screen.blit(land[6], (0, 0))
        screen.blit(cover, (0, 0))
        screen.blit(stage[6], (49, 49))

        draw = random.randint(0, len(deck) - 1)
        if tmr < 2:
            for i in range(10):
                draw = random.randint(0, len(deck) - 1)
                if deck[draw] not in o:
                    if len(o) == 0:
                        i = 0
                    elif len(o) == 1:
                        i = 1
                    elif len(o) == 2:
                        i = 2
                    o.append(deck[draw])
                    o[i].update((400 + i * 400, 840))
                if len(o) == 3:
                    break

        if MENU_MOUSE_POS[0] < o[0].rect.left or o[0].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[0].rect.top or o[0].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[0].update((400, 840))
        else:
            if o[0].rect.left <= MENU_MOUSE_POS[0] <= o[0].rect.right and o[0].rect.top <= MENU_MOUSE_POS[1] <= o[0].rect.bottom:
                if MENU_MOUSE_PRESS[0] == press:
                    o[0].rect.x = MENU_MOUSE_POS[0] - o[0].rect.width // 2
                    o[0].rect.y = MENU_MOUSE_POS[1] - o[0].rect.height // 2
                    o[0].update((o[0].rect.x, o[0].rect.y))
                    if MENU_MOUSE_PRESS[2] == True:
                        if enemy[10].rect.colliderect(o[0]):
                            if P_ch[x].cost == 0 or enemy[10].alive == False:
                                o[0].update((400, 840))
                            else:
                                attack_animation.start()
                                o[0].apply_effect(enemy[6], enemy[10], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[0] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
                        elif enemy[6].rect.colliderect(o[0]):
                            if P_ch[x].cost == 0 or enemy[6].alive == False:
                                o[0].update((400, 840))
                            else:
                                attack_animation.start()
                                o[0].apply_effect(enemy[10], enemy[6], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[0] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False

        if MENU_MOUSE_POS[0] < o[1].rect.left or o[1].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[1].rect.top or o[1].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[1].update((800, 840))
        else:
            if o[1].rect.left <= MENU_MOUSE_POS[0] <= o[1].rect.right and o[1].rect.top <= MENU_MOUSE_POS[1] <= o[1].rect.bottom:
                if MENU_MOUSE_PRESS[0] == True:
                    o[1].rect.x = MENU_MOUSE_POS[0] - o[1].rect.width // 2
                    o[1].rect.y = MENU_MOUSE_POS[1] - o[1].rect.height // 2
                    o[1].update((o[1].rect.x, o[1].rect.y))
                    if MENU_MOUSE_PRESS[2] == press:
                        if enemy[10].rect.colliderect(o[1]):
                            if P_ch[x].cost == 0 or enemy[10].alive == False:
                                o[1].update((800, 840))
                            else:
                                attack_animation.start()
                                o[1].apply_effect(enemy[6], enemy[10], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[1] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
                        elif enemy[6].rect.colliderect(o[1]):
                            if P_ch[x].cost == 0 or enemy[6].alive == False:
                                o[1].update((800, 840))
                            else:
                                attack_animation.start()
                                o[1].apply_effect(enemy[10], enemy[6], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[1] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False

        if MENU_MOUSE_POS[0] < o[2].rect.left or o[2].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[2].rect.top or o[2].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[2].update((1200, 840))
        else:
            if o[2].rect.left <= MENU_MOUSE_POS[0] <= o[2].rect.right and o[2].rect.top <= MENU_MOUSE_POS[1] <= o[2].rect.bottom:
                if MENU_MOUSE_PRESS[0] == True:
                    o[2].rect.x = MENU_MOUSE_POS[0] - o[2].rect.width // 2
                    o[2].rect.y = MENU_MOUSE_POS[1] - o[2].rect.height // 2
                    o[2].update((o[2].rect.x, o[2].rect.y))
                    if MENU_MOUSE_PRESS[2] == press:
                        if enemy[10].rect.colliderect(o[2]):
                            if P_ch[x].cost == 0 or enemy[10].alive == False:
                                o[2].update((400, 840))
                            else:
                                attack_animation.start()
                                o[2].apply_effect(enemy[6], enemy[10], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[2] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
                        elif enemy[6].rect.colliderect(o[2]):
                            if P_ch[x].cost == 0 or enemy[6].alive == False:
                                o[2].update((400, 840))
                            else:
                                attack_animation.start()
                                o[2].apply_effect(enemy[10], enemy[6], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[2] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
    
        if attack_animation.is_playing:
            if x == 0:
                attack_animation.play(screen, 256, 231)
            elif x == 1:
                attack_animation.play(screen, 467, 367)
        else:
            if x == 0:
                P_ch[x].image = pygame.image.load(P_1)
            else:
                P_ch[x].image = pygame.image.load(P_2)
            screen.blit(P_ch[x].image, P_ch[x].rect)

        if enemy[10].alive:
     
            enemy[10].image = pygame.image.load(patrol)
            screen.blit(enemy[10].image, enemy[10].rect)
            e1_blood.draw()
            text2 = Nfont.render(f"{enemy[10].hp}", True, (255, 255, 255))
            screen.blit(text2, (1358, 699))
        

        if enemy[6].alive:
            
            enemy[6].image = pygame.image.load(chef2)
            screen.blit(enemy[6].image, enemy[6].rect)
            e2_blood.draw()
            text3 = Nfont.render(f"{enemy[6].hp}", True, (255, 255, 255))
            screen.blit(text3, (1708, 699))



        screen.blit(pygame.image.load(en_bar[P_ch[x].cost]), (56, 280))
        text0 = Nfont.render(f"{P_ch[x].cost}", True, (255, 255, 255))
        screen.blit(text0, (70, 473))

        p_blood.draw()
        text1 = Nfont.render(f"{P_ch[x].hp}", True, (255, 255, 255))
        screen.blit(text1, (518, 699))
        screen.blit(pygame.image.load("image/effect/실드.png"), (363, 714))
        defense.draw(P_ch[x])
        e1_blood.draw()
        text2 = Nfont.render(f"{enemy[10].hp}", True, (255, 255, 255))
        screen.blit(text2, (1358, 699))
        e2_blood.draw()
        text3 = Nfont.render(f"{enemy[6].hp}", True, (255, 255, 255))
        screen.blit(text3, (1708, 699))

        if P_ch[x].hp < 0:
                P_ch[x].hp = 0

        if P_ch[x].hp == 0:
            time.sleep(1)
            sys.exit()

        next_img = "image/button/next_bt/0.png"
        next = button(next_img, (2000, 600))
        if enemy[10].alive == False and enemy[6].alive == False:
            if not next.checkmouse(MENU_MOUSE_POS):
                next.update()
            elif next.checkmouse(MENU_MOUSE_POS):
                next_img = "image/button/next_bt/1.png"
                next = button(next_img, (2000, 600))
                next.update()
                if MENU_MOUSE_PRESS[0] == True:
                    skull.damage = 2
                    spell.damage = 2
                    p1_deck.append(tric)
                    p2_deck.append(eye)
                    stage3_2()

        turn = button("image/main/turn_end1.png", (2000, 800))
        turn.update()
        if turn.checkmouse(MENU_MOUSE_POS):
            tick = 10
            turn.button_change(MENU_MOUSE_POS, "image/main/turn_end2.png")
            if MENU_MOUSE_PRESS[0] == True:
                P_ch[x].cost = 6
                if enemy[10].alive == True:
                    enemy[10].action(P_ch[x])
                time.sleep(0.1)
                if enemy[6].alive == True:
                    enemy[6].action(P_ch[x])
                time.sleep(0.1)
                P_ch[x].defense = 0

        pygame.display.update()
        clock.tick(tick)

def stage3_2():
    tmr = 0
    screen.fill(BLACK)
    global x
    if x == 0:
        deck = p1_deck
        attack_animation = Animation(p1_attack_frames, 1)
    elif x == 1:
        deck = p2_deck
        attack_animation = Animation(p2_attack_frames, 1)
    o = []
    enemy[10].hp = 10
    enemy[10].alive = True
    enemy[8].hp = 10
    enemy[8].alive = True
    P_ch[x].hp = 20
    P_ch[x].cost = 6
    P_ch[x].defense = 0
    p_blood = BloodBar(440, 735, P_ch[x].hp, P_ch[x].max_hp)
    defense = ShieldBar(440, 735)
    e1_blood = BloodBar(1280, 735, enemy[10].hp, enemy[10].max_hp)
    e2_blood = BloodBar(1630, 735, enemy[8].hp, enemy[8].max_hp)

    while True:
        tick = 100
        tmr = tmr + 1
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_MOUSE_PRESS = pygame.mouse.get_pressed()
        press = True

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        screen.blit(land[7], (0, 0))
        screen.blit(cover, (0, 0))
        screen.blit(stage[7], (49, 49))

        draw = random.randint(0, len(deck) - 1)
        if tmr < 2:
            for i in range(10):
                draw = random.randint(0, len(deck) - 1)
                if deck[draw] not in o:
                    if len(o) == 0:
                        i = 0
                    elif len(o) == 1:
                        i = 1
                    elif len(o) == 2:
                        i = 2
                    o.append(deck[draw])
                    o[i].update((400 + i * 400, 840))
                if len(o) == 3:
                    break

        if MENU_MOUSE_POS[0] < o[0].rect.left or o[0].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[0].rect.top or o[0].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[0].update((400, 840))
        else:
            if o[0].rect.left <= MENU_MOUSE_POS[0] <= o[0].rect.right and o[0].rect.top <= MENU_MOUSE_POS[1] <= o[0].rect.bottom:
                if MENU_MOUSE_PRESS[0] == press:
                    o[0].rect.x = MENU_MOUSE_POS[0] - o[0].rect.width // 2
                    o[0].rect.y = MENU_MOUSE_POS[1] - o[0].rect.height // 2
                    o[0].update((o[0].rect.x, o[0].rect.y))
                    if MENU_MOUSE_PRESS[2] == True:
                        if enemy[10].rect.colliderect(o[0]):
                            if P_ch[x].cost == 0 or enemy[10].alive == False:
                                o[0].update((400, 840))
                            else:
                                attack_animation.start()
                                o[0].apply_effect(enemy[8], enemy[10], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[0] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
                        elif enemy[8].rect.colliderect(o[0]):
                            if P_ch[x].cost == 0 or enemy[8].alive == False:
                                o[0].update((400, 840))
                            else:
                                attack_animation.start()
                                o[0].apply_effect(enemy[10], enemy[8], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[0] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False

        if MENU_MOUSE_POS[0] < o[1].rect.left or o[1].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[1].rect.top or o[1].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[1].update((800, 840))
        else:
            if o[1].rect.left <= MENU_MOUSE_POS[0] <= o[1].rect.right and o[1].rect.top <= MENU_MOUSE_POS[1] <= o[1].rect.bottom:
                if MENU_MOUSE_PRESS[0] == True:
                    o[1].rect.x = MENU_MOUSE_POS[0] - o[1].rect.width // 2
                    o[1].rect.y = MENU_MOUSE_POS[1] - o[1].rect.height // 2
                    o[1].update((o[1].rect.x, o[1].rect.y))
                    if MENU_MOUSE_PRESS[2] == press:
                        if enemy[10].rect.colliderect(o[1]):
                            if P_ch[x].cost == 0 or enemy[10].alive == False:
                                o[1].update((800, 840))
                            else:
                                attack_animation.start()
                                o[1].apply_effect(enemy[8], enemy[10], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[1] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
                        elif enemy[8].rect.colliderect(o[1]):
                            if P_ch[x].cost == 0 or enemy[8].alive == False:
                                o[1].update((800, 840))
                            else:
                                attack_animation.start()
                                o[1].apply_effect(enemy[10], enemy[8], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[1] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False

        if MENU_MOUSE_POS[0] < o[2].rect.left or o[2].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[2].rect.top or o[2].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[2].update((1200, 840))
        else:
            if o[2].rect.left <= MENU_MOUSE_POS[0] <= o[2].rect.right and o[2].rect.top <= MENU_MOUSE_POS[1] <= o[2].rect.bottom:
                if MENU_MOUSE_PRESS[0] == True:
                    o[2].rect.x = MENU_MOUSE_POS[0] - o[2].rect.width // 2
                    o[2].rect.y = MENU_MOUSE_POS[1] - o[2].rect.height // 2
                    o[2].update((o[2].rect.x, o[2].rect.y))
                    if MENU_MOUSE_PRESS[2] == press:
                        if enemy[10].rect.colliderect(o[2]):
                            if P_ch[x].cost == 0 or enemy[10].alive == False:
                                o[2].update((400, 840))
                            else:
                                attack_animation.start()
                                o[2].apply_effect(enemy[8], enemy[10], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[2] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
                        elif enemy[8].rect.colliderect(o[2]):
                            if P_ch[x].cost == 0 or enemy[8].alive == False:
                                o[2].update((400, 840))
                            else:
                                attack_animation.start()
                                o[2].apply_effect(enemy[10], enemy[8], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[2] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
    
        if attack_animation.is_playing:
            if x == 0:
                attack_animation.play(screen, 256, 231)
            elif x == 1:
                attack_animation.play(screen, 467, 367)
        else:
            if x == 0:
                P_ch[x].image = pygame.image.load(P_1)
            else:
                P_ch[x].image = pygame.image.load(P_2)
            screen.blit(P_ch[x].image, P_ch[x].rect)

        enemy[10].image = pygame.image.load(patrol)
        screen.blit(enemy[10].image, enemy[10].rect)
        enemy[8].image = pygame.image.load(farm_w)
        screen.blit(enemy[8].image, enemy[8].rect)

        screen.blit(pygame.image.load(en_bar[P_ch[x].cost]), (56, 280))
        text0 = Nfont.render(f"{P_ch[x].cost}", True, (255, 255, 255))
        screen.blit(text0, (70, 473))

        p_blood.draw()
        text1 = Nfont.render(f"{P_ch[x].hp}", True, (255, 255, 255))
        screen.blit(text1, (518, 699))
        screen.blit(pygame.image.load("image/effect/실드.png"), (363, 714))
        defense.draw(P_ch[x])
        e1_blood.draw()
        text2 = Nfont.render(f"{enemy[10].hp}", True, (255, 255, 255))
        screen.blit(text2, (1358, 699))
        e2_blood.draw()
        text3 = Nfont.render(f"{enemy[8].hp}", True, (255, 255, 255))
        screen.blit(text3, (1708, 699))

        if P_ch[x].hp < 0:
                P_ch[x].hp = 0

        if P_ch[x].hp == 0:
            time.sleep(1)
            sys.exit()

        next_img = "image/button/next_bt/0.png"
        next = button(next_img, (2000, 600))
        if enemy[10].alive == False and enemy[8].alive == False:
            if not next.checkmouse(MENU_MOUSE_POS):
                next.update()
            elif next.checkmouse(MENU_MOUSE_POS):
                next_img = "image/button/next_bt/1.png"
                next = button(next_img, (2000, 600))
                next.update()
                if MENU_MOUSE_PRESS[0] == True:
                    skull.damage = 2
                    spell.damage = 2
                    p1_deck.append(tric)
                    p2_deck.append(eye)
                    stage3_3()

        turn = button("image/main/turn_end1.png", (2000, 800))
        turn.update()
        if turn.checkmouse(MENU_MOUSE_POS):
            tick = 10
            turn.button_change(MENU_MOUSE_POS, "image/main/turn_end2.png")
            if MENU_MOUSE_PRESS[0] == True:
                P_ch[x].cost = 6
                if enemy[10].alive == True:
                    enemy[10].action(P_ch[x])
                time.sleep(0.1)
                if enemy[8].alive == True:
                    enemy[8].action(P_ch[x])
                time.sleep(0.1)
                P_ch[x].defense = 0

        pygame.display.update()
        clock.tick(tick)

def stage3_3():
    tmr = 0
    screen.fill(BLACK)
    global x
    if x == 0:
        deck = p1_deck
        attack_animation = Animation(p1_attack_frames, 1)
    elif x == 1:
        deck = p2_deck
        attack_animation = Animation(p2_attack_frames, 1)
    o = []
    P_ch[x].hp = 20
    P_ch[x].cost = 6
    P_ch[x].defense = 0
    p_blood = BloodBar(440, 735, P_ch[x].hp, P_ch[x].max_hp)
    defense = ShieldBar(440, 735)
    e1_blood = BloodBar(1280, 735, enemy[11].hp, enemy[11].max_hp)

    while True:
        tick = 100
        tmr = tmr + 1
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_MOUSE_PRESS = pygame.mouse.get_pressed()
        press = True

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        screen.blit(land[8], (0, 0))
        screen.blit(cover, (0, 0))
        screen.blit(stage[8], (49, 49))

        draw = random.randint(0, len(deck) - 1)
        if tmr < 2:
            for i in range(10):
                draw = random.randint(0, len(deck) - 1)
                if deck[draw] not in o:
                    if len(o) == 0:
                        i = 0
                    elif len(o) == 1:
                        i = 1
                    elif len(o) == 2:
                        i = 2
                    o.append(deck[draw])
                    o[i].update((400 + i * 400, 840))
                if len(o) == 3:
                    break

        if MENU_MOUSE_POS[0] < o[0].rect.left or o[0].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[0].rect.top or o[0].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[0].update((400, 840))
        else:
            if o[0].rect.left <= MENU_MOUSE_POS[0] <= o[0].rect.right and o[0].rect.top <= MENU_MOUSE_POS[1] <= o[0].rect.bottom:
                if MENU_MOUSE_PRESS[0] == press:
                    o[0].rect.x = MENU_MOUSE_POS[0] - o[0].rect.width // 2
                    o[0].rect.y = MENU_MOUSE_POS[1] - o[0].rect.height // 2
                    o[0].update((o[0].rect.x, o[0].rect.y))
                    if MENU_MOUSE_PRESS[2] == True:
                        if enemy[11].rect.colliderect(o[0]):
                            if P_ch[x].cost == 0 or enemy[11].alive == False:
                                o[0].update((400, 840))
                            else:
                                attack_animation.start()
                                o[0].apply_effect(enemy[11], enemy[11], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[0] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False

        if MENU_MOUSE_POS[0] < o[1].rect.left or o[1].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[1].rect.top or o[1].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[1].update((800, 840))
        else:
            if o[1].rect.left <= MENU_MOUSE_POS[0] <= o[1].rect.right and o[1].rect.top <= MENU_MOUSE_POS[1] <= o[1].rect.bottom:
                if MENU_MOUSE_PRESS[0] == True:
                    o[1].rect.x = MENU_MOUSE_POS[0] - o[1].rect.width // 2
                    o[1].rect.y = MENU_MOUSE_POS[1] - o[1].rect.height // 2
                    o[1].update((o[1].rect.x, o[1].rect.y))
                    if MENU_MOUSE_PRESS[2] == press:
                        if enemy[11].rect.colliderect(o[1]):
                            if P_ch[x].cost == 0 or enemy[11].alive == False:
                                o[1].update((800, 840))
                            else:
                                attack_animation.start()
                                o[1].apply_effect(enemy[11], enemy[11], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[1] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
                        
        if MENU_MOUSE_POS[0] < o[2].rect.left or o[2].rect.right < MENU_MOUSE_POS[0] or MENU_MOUSE_POS[1] < o[2].rect.top or o[2].rect.bottom < MENU_MOUSE_POS[1] or MENU_MOUSE_PRESS[0] == False:
            o[2].update((1200, 840))
        else:
            if o[2].rect.left <= MENU_MOUSE_POS[0] <= o[2].rect.right and o[2].rect.top <= MENU_MOUSE_POS[1] <= o[2].rect.bottom:
                if MENU_MOUSE_PRESS[0] == True:
                    o[2].rect.x = MENU_MOUSE_POS[0] - o[2].rect.width // 2
                    o[2].rect.y = MENU_MOUSE_POS[1] - o[2].rect.height // 2
                    o[2].update((o[2].rect.x, o[2].rect.y))
                    if MENU_MOUSE_PRESS[2] == press:
                        if enemy[11].rect.colliderect(o[2]):
                            if P_ch[x].cost == 0 or enemy[11].alive == False:
                                o[2].update((400, 840))
                            else:
                                attack_animation.start()
                                o[2].apply_effect(enemy[11], enemy[11], P_ch[x])
                                while True:
                                    if deck[draw] not in o:
                                        o[2] = deck[draw]
                                        break
                                    else:
                                        draw = random.randint(0, len(deck) - 1)
                            press = False
                        
        if attack_animation.is_playing:
            if x == 0:
                attack_animation.play(screen, 256, 231)
            elif x == 1:
                attack_animation.play(screen, 467, 367)
        else:
            if x == 0:
                P_ch[x].image = pygame.image.load(P_1)
            else:
                P_ch[x].image = pygame.image.load(P_2)
            screen.blit(P_ch[x].image, P_ch[x].rect)

        enemy[11].image = pygame.image.load(brave)
        screen.blit(enemy[11].image, enemy[11].rect)

        screen.blit(pygame.image.load(en_bar[P_ch[x].cost]), (56, 280))
        text0 = Nfont.render(f"{P_ch[x].cost}", True, (255, 255, 255))
        screen.blit(text0, (70, 473))

        p_blood.draw()
        text1 = Nfont.render(f"{P_ch[x].hp}", True, (255, 255, 255))
        screen.blit(text1, (518, 699))
        screen.blit(pygame.image.load("image/effect/실드.png"), (363, 714))
        defense.draw(P_ch[x])
        e1_blood.draw()
        text2 = Nfont.render(f"{enemy[11].hp}", True, (255, 255, 255))
        screen.blit(text2, (1360, 699))

        if P_ch[x].hp < 0:
                P_ch[x].hp = 0

        if P_ch[x].hp == 0:
            time.sleep(1)
            sys.exit()

        next_img = "image/button/next_bt/0.png"
        next = button(next_img, (2000, 600))
        if enemy[11].alive == False:
            if not next.checkmouse(MENU_MOUSE_POS):
                next.update()
            elif next.checkmouse(MENU_MOUSE_POS):
                next_img = "image/button/next_bt/1.png"
                next = button(next_img, (2000, 600))
                next.update()
                if MENU_MOUSE_PRESS[0] == True:
                    skull.damage = 2
                    spell.damage = 2
                    p1_deck.append(hell)
                    p2_deck.append(curse)
                    pygame.mixer.music.pause()
                    end()

        turn = button("image/main/turn_end1.png", (2000, 800))
        turn.update()
        if turn.checkmouse(MENU_MOUSE_POS):
            tick = 10
            turn.button_change(MENU_MOUSE_POS, "image/main/turn_end2.png")
            if MENU_MOUSE_PRESS[0] == True:
                P_ch[x].cost = 6
                if enemy[11].alive == True:
                    enemy[11].action(P_ch[x])
                time.sleep(0.1)
                P_ch[x].defense = 0

        pygame.display.update()
        clock.tick(tick)

def end():
    font1 = pygame.font.SysFont("malgun", 200)
    font2 = pygame.font.SysFont("Malgun Gothic", 32)
    credits = "GAME CLEAR"
    text = "제작 : 이권민, 이보성, 유찬종, 박현성"
    text_surface1 = font1.render(credits, True, (255, 255, 255))
    text_surface2 = font2.render(text, True, (255, 255, 255))
    scroll_speed = 2

    scroll_y = 1260
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        if scroll_y > 630:
            scroll_y -= scroll_speed

        screen.blit(text_surface1, (2240 // 2 - text_surface1.get_width() // 2, scroll_y))
        screen.blit(text_surface2, (2240 // 2 - text_surface2.get_width() // 2, scroll_y + 150))
        

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

if __name__ == '__main__':
    menu()


#카드에 마우스 대면 카드 확대 : pygame.transform.scale(img, [폭, 넓이]), 도형이 겹치는지 확인 : rect.colliderect()                 