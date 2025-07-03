import pygame
import sys
import logging
import time
from random import randint
from textwrap import wrap
from enum import Enum

class ScreenMode(Enum):
    WINDOWED = 1
    FULLSCREEN = 2
    """ cspell:disable-next-line """    
    BORDERLESS = 3
    WINDOWED_RESIZABLE = 4
    """ cspell:disable-next-line """
    BORDERLESS_TAKINGUP_PERCENTAGE = 5

pygame.init()

mode = ScreenMode.BORDERLESS  # Modes: WINDOWED, FULLSCREEN, BORDERLESS, WINDOWED_RESIZABLE, BORDERLESS_TAKINGUP_PERCENTAGE

aspect_ratio = (16, 9)
scale = 75
taking_up_percentage = 50  # Only used for BORDERLESS_TAKINGUP_PERCENTAGE mode

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',handlers=[logging.StreamHandler(sys.stdout)])

logging.debug("Display mode is set to %s", mode.name)

infoObject = pygame.display.Info() 
if mode == ScreenMode.BORDERLESS:
    screen = pygame.display.set_mode((aspect_ratio[0]*scale, aspect_ratio[1]*scale), pygame.NOFRAME)
elif mode == ScreenMode.FULLSCREEN:
    screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.NOFRAME | pygame.FULLSCREEN)
elif mode == ScreenMode.WINDOWED:
    screen = pygame.display.set_mode((aspect_ratio[0]*scale, aspect_ratio[1]*scale))
elif mode == ScreenMode.WINDOWED_RESIZABLE:
    screen = pygame.display.set_mode((aspect_ratio[0]*scale, aspect_ratio[1]*scale), pygame.RESIZABLE)
elif mode == ScreenMode.BORDERLESS_TAKINGUP_PERCENTAGE:
    screen = pygame.display.set_mode((int(infoObject.current_w * taking_up_percentage / 100), int(infoObject.current_h * taking_up_percentage / 100)), pygame.NOFRAME)
else:
    logging.fatal("Unsupported screen mode: %s", mode.name)
    pygame.quit()
    sys.exit("Unsupported screen mode. Please set mode to an supported value.")

assert screen, "Failed to create display surface. Please check your Pygame installation and display settings."

clock = pygame.time.Clock()

TEST_FONT = pygame.font.SysFont("Consolas", 5)
FONT = pygame.font.SysFont("Consolas", 18)

TEST_CHAR = TEST_FONT.render("X", True, (255, 255, 255))
CHAR = FONT.render("X", True, (255, 255, 255))

TEST_TEXTS = [ 
              """ cspell:disable-line """ "Whereas disregard and contempt for human rights have resulted in barbarous acts which have outraged the conscience of mankind, and the advent of a world in which human beings shall enjoy freedom of speech and belief and freedom from fear and want has been proclaimed as the highest aspiration of the common people",
              """ cspell:disable-line """ "že zneuznání lidských práv a pohrdání jimi vedlo k barbarským činům, urážejícím svědomí lidstva, a že vybudování světa, ve kterém lidé, zbavení strachu a nouze, se budou těšiti svobodě projevu a přesvĕdčení, bylo prohlášeno za nejvyšší cíl lidu",
              """ cspell:disable-line """ "da die Nichtanerkennung und Verachtung der Menschenrechte zu Akten der Barbarei geführt haben, die das Gewissen der Menschheit mit Empörung erfüllen, und da verkündet worden ist, daß einer Welt, in der die Menschen Rede- und Glaubensfreiheit und Freiheit von Furcht und Not genießen, das höchste Streben des Menschen gilt",
              """ cspell:disable-line """ "ولما كان تناسي حقوق الإنسان وازدراؤها قد أفضيا إلى أعمال همجية آذت الضمير الإنساني، وكان غاية ما يرنو إليه عامة البشر انبثاق عالم يتمتع فيه الفرد بحرية القول والعقيدة ويتحرر من الفزع والفاقة."
            ]

test_times = []

assert TEST_TEXTS, "Test texts are not defined. Please check your code."

def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        
def test_start(name="Unnamed Test", delay=5):
    id = len(test_times)
    logging.info(f"Delay before starting test {id} ({name})...")
    pygame.display.set_caption(f"Test {id} ({name}) running...")
    for repeat in range(delay * 30):
        check_events()
        screen.fill((0, 0, 0))
        text = FONT.render(f"Test {id} ({name}) starting soon...", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        pygame.display.flip()
        clock.tick(30)
    screen.fill((0, 0, 0))
    pygame.display.flip()
    test_times.append({"name" : name, "id" : id, "start_time" : time.time(), "end_time" : None, "duration" : None})
    logging.info(f"Starting test {id} ({name})...")
    return id

def test_end(id = ..., delay=5):
    if not test_times:
        logging.warning("No test to end.")
        return
    if not id is ...:
        if id < 0 or id > len(test_times):
            logging.error(f"Invalid test ID: {id}. No test ended.")
            return
        test = test_times[id]
    else:
        test = test_times[-1]
    test["end_time"] = time.time()
    duration = test["end_time"] - test["start_time"]
    test["duration"] = duration
    if not test is test_times[-1]:
        test_times[-1] = test
    logging.info(f"Test {test['id']} ({test['name']}) ended. Duration: {duration} seconds.")
    for repeat in range(delay * 30):
        check_events()
        #screen.fill((0, 0, 0))
        text = FONT.render(f"Test {test["id"]} ({test["name"]}) ended.", True, (255, 255, 255),(0,0,0))
        screen.blit(text, (10, 10))
        pygame.display.flip()
        clock.tick(30)
    screen.fill((0, 0, 0))
    pygame.display.flip()
    return duration

assert test_start, "Test start function is not defined. Please check your code."
assert test_end, "Test end function is not defined. Please check your code."

#Test 0: Filling the screen pixel by pixel

test_id = test_start("Filling screen pixel by pixel")
for y in range(screen.get_height()):
    for x in range(screen.get_width()):
        check_events()
        screen.set_at((x, y), (255, 255, 255))
    pygame.display.flip()
test_end(delay=1)

#Test 1: Filling the screen with a rectangle

test_id = test_start("Filling screen with a rectangle")
rect = pygame.Rect(0, 0, screen.get_width(), screen.get_height())
pygame.draw.rect(screen, (255, 255, 255), rect)
pygame.display.flip()
test_end(delay=1)

#Test 2: Filling the screen with random characters

test_id = test_start("Filling screen with random characters")
for y in range(0, int(screen.get_height()), CHAR.get_height()):
    for x in range(0, int(screen.get_width()), CHAR.get_width()):
        check_events()
        r_char = TEST_FONT.render(f"{chr(randint(21,126))}", True, (255, 255, 255))
        screen.blit(r_char, (x, y))
    pygame.display.flip()
test_end(delay=1)

#Test 3: Filling the screen with meaningful text

test_id = test_start("Filling screen with meaningful text")
wrapped_text = []
for text in TEST_TEXTS:
    wrapped_text += wrap(text, width=int(screen.get_width() / TEST_CHAR.get_width()))

for y, line in zip(range(0, int(screen.get_height()), TEST_CHAR.get_height()), wrapped_text*int(screen.get_height() / TEST_CHAR.get_height()*len(wrapped_text))):
    check_events()
    text = TEST_FONT.render(line, True, (255, 255, 255))
    screen.blit(text, (0, y))
    pygame.display.flip()
test_end(delay=1)

#Test 4: Filling the screen with fill()

test_id = test_start("Filling screen with fill")
screen.fill((255, 255, 255))
pygame.display.flip()
test_end(delay=1)


if len(test_times) <= 0:
    logging.fatal("No tests were run. Exiting.")
    pygame.quit()
    sys.exit(1)

logging.info("Showing test results...")
pygame.display.set_caption("Test results")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    screen.fill((0, 0, 0))
    text = FONT.render("Press ESC to exit", True, (255, 255, 255))
    screen.blit(text, (10, 10))
    for test,no in zip(test_times, range(1,len(test_times)+1)):
        test_text = FONT.render(f"Test {test['id']} ({test['name']}): {test['duration']:.5f} seconds", True, (255, 255, 255))
        screen.blit(test_text, (10, 30 + no * CHAR.get_height()))
    pygame.display.flip()
    clock.tick(30)

logging.info("Program finished.")
pygame.quit()
sys.exit(0)