import pygame, random
import pygame.freetype

pygame.init()

WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
VERSION = "0.2"

clock = pygame.time.Clock()
font_freetype_6 = pygame.freetype.SysFont('Comic Sans MS', 6)
font_freetype_15 = pygame.freetype.SysFont('Comic Sans MS', 15)
font_main_8 = pygame.font.SysFont('Comic Sans MS', 8)
font_main_17 = pygame.font.SysFont('Comic Sans MS', 17)


# Рубрика "харе все забывать, разраб"
# Типы карт:          | entity, spell, weapon
# Типы существ:
# - Ошибка (error)          : Название говорит само за себя
# - Механизм (mech)         : Имеет малую прочность и высокую атаку
# - Нежить (undead)         : Слабые существа, некоторые могут возрадится с 1 хп
# - Элементаль (elemental)  : Имеют свойства своих элементов
# - Дракон (dragon)         : Имеют хорошое количество здоровья и сложности, многие драконы имеют провокацию до 1 удара
# - Орк (orc)               : Имеют хорошую атаку и сложность, многие орки могут атаковать сразу после выставления
# Типы заклинаний:    | Лед, Огонь, Электричество, Ветер, Кровь, Свет,  Тьма
#                     | ice, fire,  electricity,   wind,  blood, light, darkness
# Спец. способности:  | 
# Типы предметов:     | 

CARDS = {
    0: {
        "id": 0,
        "name": "Ошибка",
        "description": "Как ты это получил????",
        "card_type": "entity", 
        "type": "any",
        "rarity": "none",
        "hp": 1,
        "attack": 0,
        "defence": 99,
        "mana": 10,
        "special": [],
        "special_vals": [],
        "original": True,
        "attacks": 0
    },
    # spell
    1: {
        "id": 1,
        "name": "Волшебная стрела",
        "description": "Наносит 2 урона герою противника",
        "card_type": "spell", 
        "type": "light",
        "rarity": "basic",
        "mana": 2,
        "special": ["damageEnemyPlayer"],
        "special_vals": [2],
        "original": True
    },
    2: {
        "id": 2,
        "name": "Молния",
        "description": "Наносит 3 урона ВСЕМ персонажам",
        "card_type": "spell", 
        "type": "electricity",
        "rarity": "rare",
        "mana": 5,
        "special": ["damageAllEntity", "damagePlayer", "damageEnemyPlayer"],
        "special_vals": [3, 3, 3],
        "original": True
    },
    3: {
        "id": 3,
        "name": "ЭМИ вспышка",
        "description": "Изменяет урон всех механизмов до 1",
        "card_type": "spell", 
        "type": "electricity",
        "rarity": "rare",
        "mana": 7,
        "special": ["setTypeDamage"],
        "special_vals": [[1, "mech"]],
        "original": True
    },
    4: {
        "id": 4,
        "name": "Ярость",
        "description": "Наносит 5 урона герою игрока и противника",
        "card_type": "spell", 
        "type": "blood",
        "rarity": "rare",
        "mana": 5,
        "special": ["damagePlayer", "damageEnemyPlayer"],
        "special_vals": [5, 5],
        "original": True
    },
    5: {
        "id": 5,
        "name": "Солнечное затмение",
        "description": "Выдает вам 3 солнечные вспышки",
        "card_type": "spell", 
        "type": "fire",
        "rarity": "epic",
        "mana": 5,
        "special": ["addCards"],
        "special_vals": [[3, 6]],
        "original": True
    },
    6: {
        "id": 6,
        "name": "Солнечная вспышка",
        "description": "Наносит 1 урона ВСЕМ",
        "card_type": "spell", 
        "type": "error",
        "rarity": "basic",
        "mana": 2,
        "special": ["damageAllEntity", "damagePlayer", "damageEnemyPlayer"],
        "special_vals": [1, 1, 1],
        "original": True
    },
    7: {
        "id": 7,
        "name": "Солнечная буря",
        "description": "Наносит 3 урона всей нежити",
        "card_type": "spell", 
        "type": "fire",
        "rarity": "rare",
        "mana": 7,
        "special": ["damageAllEntityType"],
        "special_vals": [[3, "undead"]],
        "original": True
    },
    # mech
    8: {
        "id": 8,
        "name": "Бип-буп",
        "description": "Обычный боевой робот",
        "card_type": "entity", 
        "type": "mech",
        "rarity": "basic",
        "hp": 1,
        "attack": 2,
        "defence": 1,
        "mana": 1,
        "special": [],
        "special_vals": [],
        "original": True,
        "attacks": 0
    },
}

PLAYER_MAIN_DECK = []
PLAYER_BATTLE_DECK = []
PLAYER_HAND = []
PLAYER_TABLE = []

ENEMY_BATTLE_DECK = []
ENEMY_HAND = []
ENEMY_TABLE = []

tableLimit = 7
inBattle = False

playerAngles = [random.randint(0, 50),random.randint(0, 50),random.randint(0, 50)]
enemyAngles = [random.randint(0, 50),random.randint(0, 50),random.randint(0, 50)]

PLAYER_MONEY = 100

PLAYER_SELLECTED_CARD = -1

PLAYER_HP = 25
ENEMY_HP = 25

PLAYER_SHIELD = 0
ENEMY_SHIELD = 0

PLAYER_ATTACK = 0
ENEMY_ATTACK = 0

PLAYER_MANA = 0
ENEMY_MANA = 0

PLAYER_MANA_MAX = 0
ENEMY_MANA_MAX = 0

PLAYER_FATIUGE_DAMAGE = 1
ENEMY_FATIUGE_DAMAGE = 1

#00ffff МЕХАНИКА -------------------------------------------------------------

def player_fatiuge(count = -1, add = True):
    global PLAYER_HP, PLAYER_FATIUGE_DAMAGE, PLAYER_SHIELD
    if count < 0: count = PLAYER_FATIUGE_DAMAGE
    if PLAYER_SHIELD <= 0: PLAYER_HP -= count
    else:
        PLAYER_SHIELD -= count
        if PLAYER_SHIELD <= 0:
            PLAYER_HP -= abs(PLAYER_SHIELD)
            PLAYER_SHIELD = 0
    if add: PLAYER_FATIUGE_DAMAGE += count

def enemy_fatiuge(count = -1, add = True):
    global ENEMY_HP, ENEMY_FATIUGE_DAMAGE, ENEMY_SHIELD
    if count < 0: count = ENEMY_FATIUGE_DAMAGE
    if PLAYER_SHIELD <= 0: ENEMY_HP -= count
    else:
        ENEMY_SHIELD -= count
        if ENEMY_SHIELD <= 0:
            ENEMY_HP -= abs(ENEMY_SHIELD)
            ENEMY_SHIELD = 0
    if add: ENEMY_FATIUGE_DAMAGE += count

def player_damage(count):
    global PLAYER_HP, PLAYER_SHIELD
    if PLAYER_SHIELD <= 0: PLAYER_HP -= count
    else:
        PLAYER_SHIELD -= count
        if PLAYER_SHIELD <= 0:
            PLAYER_HP -= abs(PLAYER_SHIELD)
            PLAYER_SHIELD = 0

def enemy_damage(count):
    global ENEMY_HP, ENEMY_SHIELD
    if ENEMY_SHIELD <= 0: ENEMY_HP -= count
    else:
        ENEMY_SHIELD -= count
        if ENEMY_SHIELD <= 0:
            ENEMY_HP -= abs(ENEMY_SHIELD)
            ENEMY_SHIELD = 0

def damage_all_entity_type(count, type_ = "any"):
    for eid, e in enumerate(PLAYER_TABLE):
        if type_ == e["type"] or type_ == "any" or e["type"] == "any":
            if e["defence"] > 0:
                e["defence"]-=count
                if e["defence"] < 0:
                    e["hp"] -= abs(e["defence"])
                    e["defence"] = 0
                    if e["hp"] <= 0: PLAYER_TABLE.pop(eid)
            else: 
                e["hp"]-=count
                if e["hp"] <= 0: PLAYER_TABLE.pop(eid)
    for eid, e in enumerate(ENEMY_TABLE):
        if type_ == e["type"] or type_ == "any" or e["type"] == "any":
            if e["defence"] > 0:
                e["defence"]-=count
                if e["defence"] < 0:
                    e["hp"] -= abs(e["defence"])
                    e["defence"] = 0
                    if e["hp"] <= 0: ENEMY_TABLE.pop(eid)
            else: 
                e["hp"]-=count
                if e["hp"] <= 0: ENEMY_TABLE.pop(eid)

def player_draw_a_card(count = 1):
    for i in range(count):
        if len(PLAYER_BATTLE_DECK) > 0:
            card = random.randint(0, len(PLAYER_BATTLE_DECK)-1)
            if len(PLAYER_HAND) < 10: PLAYER_HAND.append(PLAYER_BATTLE_DECK[card])
            PLAYER_BATTLE_DECK.pop(card)
        else: player_fatiuge()

def enemy_draw_a_card(count = 1):
    for i in range(count):
        if len(ENEMY_BATTLE_DECK) > 0:
            card = random.randint(0, len(ENEMY_BATTLE_DECK)-1)
            if len(ENEMY_HAND) < 10: ENEMY_HAND.append(ENEMY_BATTLE_DECK[card])
            ENEMY_BATTLE_DECK.pop(card)
        else: enemy_fatiuge()

def player_add_card_hand(id):
    if len(PLAYER_HAND) < 10:
        card = CARDS[id].copy()
        card["original"] = False
        PLAYER_HAND.append(card.copy())


#00ffff ОТРИСОВКА --------------------------------------------

def render_text_in_rect(rect, font, text, color=(0, 0, 0)):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.get_rect(test_line).width <= rect.width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "

    lines.append(current_line)

    line_spacing = font.get_sized_height()
    y_offset = rect.height / 2 - (len(lines) * line_spacing) / 2

    for line in lines:
        line_surface, _ = font.render(line, color)
        line_rect = line_surface.get_rect(center=(rect.centerx, rect.y + y_offset))
        screen.blit(line_surface, line_rect)
        y_offset += line_spacing

def draw_stat(x, y, size, text, c1, c2, tox = 0, toy = 0):
    pygame.draw.rect(screen, c1, pygame.Rect(x, y, size, size))
    pygame.draw.rect(screen, c2, pygame.Rect(x, y, size, size), 2)
    screen.blit(text, pygame.Rect((x+tox, y+toy, size, size)))

def player_draw_hand(x, y, highlight = -1, sellected = -1):
    for i, j in enumerate(PLAYER_HAND):
        clr = (255,255,255)
        if j["original"]: clr = (255,255,123)
        if i != highlight and i != sellected:
            if i % 2: x2, y2 = 55, ((i//2)*80)-5
            else: x2, y2 = -5, ((i//2)*80)-5
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(x+x2+5, y+y2+5, 50, 70))
            pygame.draw.rect(screen, clr, pygame.Rect(x+x2+5, y+y2+5, 50, 70), 2)
            draw_stat(x+x2, y+y2, 10, font_main_8.render(str(j["mana"]), False, (0,0,255)), (128,255,255), (0,255,255), 1, -1)
            if j["card_type"] == "entity":
                draw_stat(x+x2+50, y+y2+70, 10, font_main_8.render(str(j["hp"]), False, (0,0,0)), (255,0,0), (255,0,0), 1, -1)
                if j["defence"] > 0: draw_stat(x+x2+50, y+y2+55, 10, font_main_8.render(str(j["defence"]), False, (0,0,0)), (255,255,255), (200,200,200), 1, -1)
                if j["attack"] > 0: draw_stat(x+x2, y+y2+70, 10, font_main_8.render(str(j["attack"]), False, (0,0,0)), (255,255,200), (255,255,0), 1, -1)
            col = (10,10,10)
            if j["card_type"] == "entity": col = (0,255,0)
            elif j["card_type"] == "spell": col = (0,120,255)
            pygame.draw.rect(screen, col, pygame.Rect(x+x2+46, y+y2+2, 12, 2))
            pygame.draw.rect(screen, col, pygame.Rect(x+x2+56, y+y2+2, 2, 12))
            render_text_in_rect(pygame.Rect(x+x2+5, y+y2+5, 50, 70), font_freetype_6, j["name"], (255,255,255))

    clr = (255,255,255)
    if sellected >= 0 and sellected <= 10 and sellected < len(PLAYER_HAND):
        mx, my = pygame.mouse.get_pos()
        if PLAYER_HAND[sellected]["original"]: clr = (255,255,123)
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(mx-55, my-65, 110, 130))
        pygame.draw.rect(screen, clr, pygame.Rect(mx-55, my-65, 110, 130), 2)
        draw_stat(mx-60, my-70, 20, font_main_17.render(str(PLAYER_HAND[sellected]["mana"]), False, (0,0,255)), (128,255,255), (0,255,255), 2, -2)
        if PLAYER_HAND[sellected]["card_type"] == "entity":
            draw_stat(mx+40, my+50, 20, font_main_17.render(str(PLAYER_HAND[sellected]["hp"]), False, (0,0,0)), (255,0,0), (255,0,0), 2, -2)
            if PLAYER_HAND[sellected]["defence"] > 0: draw_stat(mx+40, my+20, 20, font_main_17.render(str(PLAYER_HAND[sellected]["defence"]), False, (0,0,0)), (255,255,255), (200,200,200), 2, -2)
            if PLAYER_HAND[sellected]["attack"] > 0: draw_stat(mx-60, my+50, 20, font_main_17.render(str(PLAYER_HAND[sellected]["attack"]), False, (0,0,0)), (255,255,200), (255,255,0), 2, -2)
        col = (10,10,10)
        if PLAYER_HAND[sellected]["card_type"] == "entity": col = (0,255,0)
        elif PLAYER_HAND[sellected]["card_type"] == "spell": col = (0,120,255)
        pygame.draw.rect(screen, col, pygame.Rect(mx+34, my-70, 24, 4))
        pygame.draw.rect(screen, col, pygame.Rect(mx+56, my-70, 4, 24))
        render_text_in_rect(pygame.Rect(mx-55, my-65, 110, 130), font_freetype_15, PLAYER_HAND[sellected]["name"], (255,255,255))


    else:
        if highlight >= 0 and highlight <= 10 and highlight < len(PLAYER_HAND):
            if PLAYER_HAND[highlight]["original"]: clr = (255,255,123)
            if highlight % 2: x2, y2 = 30, ((highlight//2)*80)-30
            else: x2, y2 = -30, ((highlight//2)*80)-30
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(x+x2+5, y+y2+5, 110, 130))
            pygame.draw.rect(screen, clr, pygame.Rect(x+x2+5, y+y2+5, 110, 130), 2)
            draw_stat(x+x2, y+y2, 20, font_main_17.render(str(PLAYER_HAND[highlight]["mana"]), False, (0,0,255)), (128,255,255), (0,255,255), 2, -2)
            if PLAYER_HAND[highlight]["card_type"] == "entity":
                draw_stat(x+x2+100, y+y2+120, 20, font_main_17.render(str(PLAYER_HAND[highlight]["hp"]), False, (0,0,0)), (255,0,0), (255,0,0), 2, -2)
                if PLAYER_HAND[highlight]["defence"] > 0: draw_stat(x+x2+100, y+y2+90, 20, font_main_17.render(str(PLAYER_HAND[highlight]["defence"]), False, (0,0,0)), (255,255,255), (200,200,200), 2, -2)
                if PLAYER_HAND[highlight]["attack"] > 0: draw_stat(x+x2, y+y2+120, 20, font_main_17.render(str(PLAYER_HAND[highlight]["attack"]), False, (0,0,0)), (255,255,200), (255,255,0), 2, -2)
            col = (10,10,10)
            if PLAYER_HAND[highlight]["card_type"] == "entity": col = (0,255,0)
            elif PLAYER_HAND[highlight]["card_type"] == "spell": col = (0,120,255)
            pygame.draw.rect(screen, col, pygame.Rect(x+x2+94, y+y2, 24, 4))
            pygame.draw.rect(screen, col, pygame.Rect(x+x2+116, y+y2, 4, 24))
            render_text_in_rect(pygame.Rect(x+x2+5, y+y2+5, 110, 130), font_freetype_15, PLAYER_HAND[highlight]["name"], (255,255,255))



def enemy_draw_hand(x, y, highlight = -1):
    for i, j in enumerate(ENEMY_HAND):
        clr = (255,255,255)
        if j["original"]: clr = (255,255,123)
        if i != highlight:
            if i % 2: x2, y2 = 55, ((i//2)*80)-5
            else: x2, y2 = -5, ((i//2)*80)-5
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(x+x2+5, y+y2+5, 50, 70))
            pygame.draw.rect(screen, clr, pygame.Rect(x+x2+5, y+y2+5, 50, 70), 2)
            draw_stat(x+x2, y+y2, 10, font_main_8.render(str(j["mana"]), False, (0,0,255)), (128,255,255), (0,255,255), 1, -1)
            if j["card_type"] == "entity":
                draw_stat(x+x2+50, y+y2+70, 10, font_main_8.render(str(j["hp"]), False, (0,0,0)), (255,0,0), (255,0,0), 1, -1)
                if j["defence"] > 0: draw_stat(x+x2+50, y+y2+55, 10, font_main_8.render(str(j["defence"]), False, (0,0,0)), (255,255,255), (200,200,200), 1, -1)
                if j["attack"] > 0: draw_stat(x+x2, y+y2+70, 10, font_main_8.render(str(j["attack"]), False, (0,0,0)), (255,255,200), (255,255,0), 1, -1)
            col = (10,10,10)
            if j["card_type"] == "entity": col = (0,255,0)
            elif j["card_type"] == "spell": col = (0,120,255)
            pygame.draw.rect(screen, col, pygame.Rect(x+x2+46, y+y2+2, 12, 2))
            pygame.draw.rect(screen, col, pygame.Rect(x+x2+56, y+y2+2, 2, 12))
            render_text_in_rect(pygame.Rect(x+x2+5, y+y2+5, 50, 70), font_freetype_6, j["name"], (255,255,255))

    clr = (255,255,255)
    if highlight >= 0 and highlight <= 10 and highlight < len(ENEMY_HAND):
        if ENEMY_HAND[highlight]["original"]: clr = (255,255,123)
        if highlight % 2: x2, y2 = 30, ((highlight//2)*80)-30
        else: x2, y2 = -30, ((highlight//2)*80)-30
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(x+x2+5, y+y2+5, 110, 130))
        pygame.draw.rect(screen, clr, pygame.Rect(x+x2+5, y+y2+5, 110, 130), 2)
        draw_stat(x+x2, y+y2, 20, font_main_17.render(str(ENEMY_HAND[highlight]["mana"]), False, (0,0,255)), (128,255,255), (0,255,255), 2, -2)
        if ENEMY_HAND[highlight]["card_type"] == "entity":
            draw_stat(x+x2+100, y+y2+120, 20, font_main_17.render(str(ENEMY_HAND[highlight]["hp"]), False, (0,0,0)), (255,0,0), (255,0,0), 2, -2)
            if ENEMY_HAND[highlight]["defence"] > 0: draw_stat(x+x2+100, y+y2+90, 20, font_main_17.render(str(ENEMY_HAND[highlight]["defence"]), False, (0,0,0)), (255,255,255), (200,200,200), 2, -2)
            if ENEMY_HAND[highlight]["attack"] > 0: draw_stat(x+x2, y+y2+120, 20, font_main_17.render(str(ENEMY_HAND[highlight]["attack"]), False, (0,0,0)), (255,255,200), (255,255,0), 2, -2)
        col = (10,10,10)
        if ENEMY_HAND[highlight]["card_type"] == "entity": col = (0,255,0)
        elif ENEMY_HAND[highlight]["card_type"] == "spell": col = (0,120,255)
        pygame.draw.rect(screen, col, pygame.Rect(x+x2+94, y+y2, 24, 4))
        pygame.draw.rect(screen, col, pygame.Rect(x+x2+116, y+y2, 4, 24))
        render_text_in_rect(pygame.Rect(x+x2+5, y+y2+5, 110, 130), font_freetype_15, ENEMY_HAND[highlight]["name"], (255,255,255))

def player_draw_table(x, y):
    pos = pygame.mouse.get_pos()
    highlight = -1
    for i, j in enumerate(PLAYER_TABLE):
        x2 = (i*60)-(30*len(PLAYER_TABLE))
        if PLAYER_SELLECTED_CARD == -1:
            if pygame.Rect(x+x2+5, y+5, 50, 70).collidepoint(pos): highlight = i
        if i != highlight:
            clr = (255,255,255)
            if j["original"]: clr = (255,255,123)
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(x+x2+5, y+5, 50, 70))
            pygame.draw.rect(screen, clr, pygame.Rect(x+x2+5, y+5, 50, 70), 2)
            draw_stat(x+x2, y, 10, font_main_8.render(str(j["mana"]), False, (0,0,255)), (128,255,255), (0,255,255), 1, -1)
            if j["card_type"] == "entity":
                draw_stat(x+x2+50, y+70, 10, font_main_8.render(str(j["hp"]), False, (0,0,0)), (255,0,0), (255,0,0), 1, -1)
                if j["defence"] > 0: draw_stat(x+x2+50, y+55, 10, font_main_8.render(str(j["defence"]), False, (0,0,0)), (255,255,255), (200,200,200), 1, -1)
                if j["attack"] > 0: draw_stat(x+x2, y+70, 10, font_main_8.render(str(j["attack"]), False, (0,0,0)), (255,255,200), (255,255,0), 1, -1)
            col = (10,10,10)
            if j["card_type"] == "entity": col = (0,255,0)
            pygame.draw.rect(screen, col, pygame.Rect(x+x2+46, y+2, 12, 2))
            pygame.draw.rect(screen, col, pygame.Rect(x+x2+56, y+2, 2, 12))
            render_text_in_rect(pygame.Rect(x+x2+5, y+5, 50, 70), font_freetype_6, j["name"], (255,255,255))
    if highlight > -1:
        clr = (255,255,255)
        if PLAYER_TABLE[highlight]["original"]: clr = (255,255,123)
        x2 = (highlight*60)-(30*len(PLAYER_TABLE))-30
        y2 = -30
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(x+x2+5, y+y2+5, 110, 130))
        pygame.draw.rect(screen, clr, pygame.Rect(x+x2+5, y+y2+5, 110, 130), 2)
        draw_stat(x+x2, y+y2, 20, font_main_17.render(str(PLAYER_TABLE[highlight]["mana"]), False, (0,0,255)), (128,255,255), (0,255,255), 2, -2)
        if PLAYER_TABLE[highlight]["card_type"] == "entity":
            draw_stat(x+x2+100, y+y2+120, 20, font_main_17.render(str(PLAYER_TABLE[highlight]["hp"]), False, (0,0,0)), (255,0,0), (255,0,0), 2, -2)
            if PLAYER_TABLE[highlight]["defence"] > 0: draw_stat(x+x2+100, y+y2+90, 20, font_main_17.render(str(PLAYER_TABLE[highlight]["defence"]), False, (0,0,0)), (255,255,255), (200,200,200), 2, -2)
            if PLAYER_TABLE[highlight]["attack"] > 0: draw_stat(x+x2, y+y2+120, 20, font_main_17.render(str(PLAYER_TABLE[highlight]["attack"]), False, (0,0,0)), (255,255,200), (255,255,0), 2, -2)
        col = (10,10,10)
        if PLAYER_TABLE[highlight]["card_type"] == "entity": col = (0,255,0)
        elif PLAYER_TABLE[highlight]["card_type"] == "spell": col = (0,120,255)
        pygame.draw.rect(screen, col, pygame.Rect(x+x2+94, y+y2, 24, 4))
        pygame.draw.rect(screen, col, pygame.Rect(x+x2+116, y+y2, 4, 24))
        render_text_in_rect(pygame.Rect(x+x2+5, y+y2+5, 110, 130), font_freetype_15, PLAYER_TABLE[highlight]["name"], (255,255,255))

def enemy_draw_table(x, y):
    pos = pygame.mouse.get_pos()
    highlight = -1
    for i, j in enumerate(ENEMY_TABLE):
        x2 = (i*60)-(30*len(ENEMY_TABLE))
        if PLAYER_SELLECTED_CARD == -1:
            if pygame.Rect(x+x2+5, y+5, 50, 70).collidepoint(pos): highlight = i
        if i != highlight:
            clr = (255,255,255)
            if j["original"]: clr = (255,255,123)
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(x+x2+5, y+5, 50, 70))
            pygame.draw.rect(screen, clr, pygame.Rect(x+x2+5, y+5, 50, 70), 2)
            draw_stat(x+x2, y, 10, font_main_8.render(str(j["mana"]), False, (0,0,255)), (128,255,255), (0,255,255), 1, -1)
            if j["card_type"] == "entity":
                draw_stat(x+x2+50, y+70, 10, font_main_8.render(str(j["hp"]), False, (0,0,0)), (255,0,0), (255,0,0), 1, -1)
                if j["defence"] > 0: draw_stat(x+x2+50, y+55, 10, font_main_8.render(str(j["defence"]), False, (0,0,0)), (255,255,255), (200,200,200), 1, -1)
                if j["attack"] > 0: draw_stat(x+x2, y+70, 10, font_main_8.render(str(j["attack"]), False, (0,0,0)), (255,255,200), (255,255,0), 1, -1)
            col = (10,10,10)
            if j["card_type"] == "entity": col = (0,255,0)
            pygame.draw.rect(screen, col, pygame.Rect(x+x2+46, y+2, 12, 2))
            pygame.draw.rect(screen, col, pygame.Rect(x+x2+56, y+2, 2, 12))
            render_text_in_rect(pygame.Rect(x+x2+5, y+5, 50, 70), font_freetype_6, j["name"], (255,255,255))
    if highlight > -1:
        clr = (255,255,255)
        if ENEMY_TABLE[highlight]["original"]: clr = (255,255,123)
        x2 = (highlight*60)-(30*len(ENEMY_TABLE))-30
        y2 = -30
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(x+x2+5, y+y2+5, 110, 130))
        pygame.draw.rect(screen, clr, pygame.Rect(x+x2+5, y+y2+5, 110, 130), 2)
        draw_stat(x+x2, y+y2, 20, font_main_17.render(str(ENEMY_TABLE[highlight]["mana"]), False, (0,0,255)), (128,255,255), (0,255,255), 2, -2)
        if ENEMY_TABLE[highlight]["card_type"] == "entity":
            draw_stat(x+x2+100, y+y2+120, 20, font_main_17.render(str(ENEMY_TABLE[highlight]["hp"]), False, (0,0,0)), (255,0,0), (255,0,0), 2, -2)
            if ENEMY_TABLE[highlight]["defence"] > 0: draw_stat(x+x2+100, y+y2+90, 20, font_main_17.render(str(ENEMY_TABLE[highlight]["defence"]), False, (0,0,0)), (255,255,255), (200,200,200), 2, -2)
            if ENEMY_TABLE[highlight]["attack"] > 0: draw_stat(x+x2, y+y2+120, 20, font_main_17.render(str(ENEMY_TABLE[highlight]["attack"]), False, (0,0,0)), (255,255,200), (255,255,0), 2, -2)
        col = (10,10,10)
        if ENEMY_TABLE[highlight]["card_type"] == "entity": col = (0,255,0)
        elif ENEMY_TABLE[highlight]["card_type"] == "spell": col = (0,120,255)
        pygame.draw.rect(screen, col, pygame.Rect(x+x2+94, y+y2, 24, 4))
        pygame.draw.rect(screen, col, pygame.Rect(x+x2+116, y+y2, 4, 24))
        render_text_in_rect(pygame.Rect(x+x2+5, y+y2+5, 110, 130), font_freetype_15, ENEMY_TABLE[highlight]["name"], (255,255,255))

def draw_mana():
    for i in range(1, 11):
        col = (50,50,255)
        if i <= PLAYER_MANA: col = (170,170,255)
        if i <= PLAYER_MANA_MAX: pygame.draw.rect(screen, col, pygame.Rect(650+(i*20), 515, 15, 15))
        else: pygame.draw.rect(screen, (30,30,30), pygame.Rect(650+(i*20), 515, 15, 15))
        col = (50,50,255)
        if i <= ENEMY_MANA: col = (170,170,255)
        if i <= ENEMY_MANA_MAX: pygame.draw.rect(screen, col, pygame.Rect(650+(i*20), 75, 15, 15))
        else: pygame.draw.rect(screen, (30,30,30), pygame.Rect(650+(i*20), 75, 15, 15))
    screen.blit(font_main_17.render(f"x{PLAYER_MANA}", False, (50,50,255)), pygame.Rect((870, 510, 50, 20)))
    screen.blit(font_main_17.render(f"x{ENEMY_MANA}", False, (50,50,255)), pygame.Rect((870, 70, 50, 20)))

def draw_rotated_rect(x, y, w, h, color, angle):
    rect_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(rect_surface, color, (0, 0, w, h))
    rotated_surface = pygame.transform.rotate(rect_surface, int(angle))
    screen.blit(rotated_surface, (x - rotated_surface.get_width() // 2, y - rotated_surface.get_height() // 2))

def draw_player(x, y):
    draw_rotated_rect(x, y, 40, 40, (150,150,150), playerAngles[2])
    draw_rotated_rect(x, y, 30, 30, (200,200,200), playerAngles[1])
    draw_rotated_rect(x, y, 20, 20, (255,255,255), playerAngles[0])
    draw_stat(x+40, y+10, 25, font_main_17.render(str(PLAYER_HP), False, (0,0,0)), (255,0,0), (255,50,50), 2, 0)
    if PLAYER_SHIELD > 0: draw_stat(x+40, y-20, 25, font_main_17.render(str(PLAYER_SHIELD), False, (0,0,0)), (255,255,255), (200,200,200), 2, 0)
    if PLAYER_ATTACK > 0: draw_stat(x-65, y-20, 25, font_main_17.render(str(PLAYER_ATTACK), False, (0,0,0)), (255,255,200), (255,255,0), 2, 0)

def draw_enemy(x, y):
    draw_rotated_rect(x, y, 40, 40, (150,0,0), enemyAngles[2])
    draw_rotated_rect(x, y, 30, 30, (200,0,0), enemyAngles[1])
    draw_rotated_rect(x, y, 20, 20, (255,0,0), enemyAngles[0])
    draw_stat(x+40, y-10, 25, font_main_17.render(str(ENEMY_HP), False, (0,0,0)), (255,0,0), (255,50,50), 2, 0)
    if ENEMY_SHIELD > 0: draw_stat(x+40, y+20, 25, font_main_17.render(str(ENEMY_SHIELD), False, (0,0,0)), (255,255,255), (200,200,200), 2, 0)
    if ENEMY_ATTACK > 0: draw_stat(x-65, y+20, 25, font_main_17.render(str(ENEMY_ATTACK), False, (0,0,0)), (255,255,200), (255,255,0), 2, 0)

#00ffff ПРОВЕРКИ --------------------------------------------

def check_highlight(x, y):
    pos = pygame.mouse.get_pos()
    for i in range(10):
        if i % 2: 
            if pygame.Rect(x+60, y+((i//2)*80), 50, 70).collidepoint(pos): return i
        else: 
            if pygame.Rect(x, y+((i//2)*80), 50, 70).collidepoint(pos): return i
    return -1

def sellect_card(x, y):
    global PLAYER_SELLECTED_CARD
    if PLAYER_SELLECTED_CARD < 0: PLAYER_SELLECTED_CARD = check_highlight(x, y)
    else: PLAYER_SELLECTED_CARD = -1



for i in range(30):
    card = CARDS[random.randint(0, len(CARDS)-1)].copy()
    PLAYER_MAIN_DECK.append(card)

for i in range(30):
    card = CARDS[random.randint(0, len(CARDS)-1)].copy()
    if random.randint(0, 1): card["original"] = False
    ENEMY_BATTLE_DECK.append(card)

for i in range(10):
    card = CARDS[random.randint(0, len(CARDS)-1)].copy()
    if random.randint(0, 1): card["original"] = False
    if card["card_type"] == "entity": ENEMY_TABLE.append(card)

PLAYER_BATTLE_DECK = PLAYER_MAIN_DECK



for i in range(7):
    player_draw_a_card()
    enemy_draw_a_card()
    PLAYER_MANA_MAX+=1
    ENEMY_MANA_MAX+=1

PLAYER_MANA = 999

temp = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if pygame.Rect(300, 180, 620, 240).collidepoint(pos):
                if PLAYER_SELLECTED_CARD != -1:
                    if PLAYER_HAND[PLAYER_SELLECTED_CARD]["card_type"] == "entity":
                        if PLAYER_MANA >= PLAYER_HAND[PLAYER_SELLECTED_CARD]["mana"]:
                            if len(PLAYER_TABLE) < 7:
                                PLAYER_MANA-=PLAYER_HAND[PLAYER_SELLECTED_CARD]["mana"]
                                PLAYER_TABLE.append(PLAYER_HAND[PLAYER_SELLECTED_CARD].copy())
                                PLAYER_HAND.pop(PLAYER_SELLECTED_CARD)
                                PLAYER_SELLECTED_CARD = -1
                    elif PLAYER_HAND[PLAYER_SELLECTED_CARD]["card_type"] == "spell":
                        if PLAYER_MANA >= PLAYER_HAND[PLAYER_SELLECTED_CARD]["mana"]:
                            PLAYER_MANA-=PLAYER_HAND[PLAYER_SELLECTED_CARD]["mana"]
                            for i, j in enumerate(PLAYER_HAND[PLAYER_SELLECTED_CARD]["special"]):
                                val = PLAYER_HAND[PLAYER_SELLECTED_CARD]["special_vals"][i]
                                if j == "damageAllEntity": damage_all_entity_type(val)
                                elif j == "damageAllEntityType": damage_all_entity_type(val[0], val[1])
                                elif j == "damagePlayer": player_damage(val)
                                elif j == "damageEnemyPlayer": enemy_damage(val)
                                elif j == "addCards":
                                    for t in range(val[0]): player_add_card_hand(val[1])
                                elif j == "null": pass
                                elif j == "null": pass
                                elif j == "null": pass
                                elif j == "null": pass
                                elif j == "null": pass
                            PLAYER_HAND.pop(PLAYER_SELLECTED_CARD)
                            PLAYER_SELLECTED_CARD = -1

            sellect_card(100, 100)

    for i in range(len(playerAngles)):
        playerAngles[i]+=(i+1)/3
        if playerAngles[i] >= 360: playerAngles[i]-=360
    for i in range(len(enemyAngles)):
        enemyAngles[i]+=(i+1)/3
        if enemyAngles[i] >= 360: enemyAngles[i]-=360


    screen.fill((0,0,0))

    pygame.draw.rect(screen, (50,50,50), pygame.Rect(300, 50, 620, 500))
    pygame.draw.rect(screen, (100,100,100), pygame.Rect(300, 180, 620, 100))
    pygame.draw.rect(screen, (100,100,100), pygame.Rect(300, 320, 620, 100))
    pygame.draw.rect(screen, (50,50,50), pygame.Rect(70, 50, 180, 500))
    pygame.draw.rect(screen, (50,50,50), pygame.Rect(970, 50, 180, 500))

    draw_mana()

    player_draw_table(600, 330)
    enemy_draw_table(600, 190)

    draw_player(600, 470)
    draw_enemy(600, 120)

    player_draw_hand(100, 100, check_highlight(100, 100), PLAYER_SELLECTED_CARD)
    if PLAYER_SELLECTED_CARD < 0: enemy_draw_hand(1000, 100, check_highlight(1000, 100))
    else: enemy_draw_hand(1000, 100, -1)
    pygame.display.flip()

    clock.tick(FPS)
