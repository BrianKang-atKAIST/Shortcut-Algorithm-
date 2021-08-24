import pygame
import time

# 클래스 정의
class ValuesareListdict(dict):
  def add(self, coord, value):
    try:
      self[coord].append(value)
    except KeyError:
      self[coord] = []
      self[coord].append(value)
    except AttributeError:
      self[coord] = []
      self[coord].append(value)
      
class Block:
  def __init__(self, coord, type=int, distance=0, trip_list=[]):
    self.coord = self.x, self.y = coord
    self.distance = distance
    # 0: 빈칸 1: 벽 2: 도착지 3: predicated 4: to_predicate 5: trip_list of shortcut
    self.type = type
    self.trip_list = trip_list

class ShortcutFinder:
  def __init__(self, map, origin, blockpixel):
    self.row = len(map)
    self.col = len(map[0])
    self.blockpixel = blockpixel
    self.origin = origin
    self.map = {(x, y): Block((x, y), map[y][x]) for y in range(self.row) for x in range(self.col)}
    self.map[origin].trip_list.append(origin)
    self.predicated = dict()
    self.to_predicate = {self.origin: self.map[self.origin]}
    self.screen_width = self.blockpixel * self.col
    self.screen_height = self.blockpixel * self.row
    self.found = False

  def draw_background(self):
    pygame.draw.rect(screen, color_dict['BLACK'], [0, 0, self.screen_width, self.screen_height])

  def draw_grid(self):
    for i in range(1, self.row):
      pygame.draw.line(screen, color_dict['WHITE'], (0, i*self.blockpixel), (self.screen_width, i*self.blockpixel))
    for i in range(1, self.col):
      pygame.draw.line(screen, color_dict['WHITE'], (i*self.blockpixel, 0), (i*self.blockpixel, self.screen_height))

  def draw_map(self):
    for blockcoord, block in self.map.items():
      if block.type == 0:
        continue
      color = color_dict[num_vs_color[block.type]]
      pygame.draw.rect(screen, color, [blockcoord[0]*self.blockpixel, blockcoord[1]*self.blockpixel, self.blockpixel, self.blockpixel])

  def draw_tile(self):
    for _, block in self.predicated.items():
      x = block.x*self.blockpixel
      y = block.y*self.blockpixel
      pygame.draw.rect(screen, color_dict['RED'], [x, y, self.blockpixel, self.blockpixel])
      # 글씨
    for _, block in self.to_predicate.items():
      x = block.x*self.blockpixel
      y = block.y*self.blockpixel
      pygame.draw.rect(screen, color_dict['GREEN'], [x, y, self.blockpixel, self.blockpixel])
      # 글씨
    try:
      for coord in self.shortcutlist:
        block = self.map[coord]
        x = block.x*self.blockpixel
        y = block.y*self.blockpixel
        pygame.draw.rect(screen, color_dict['BLUE'], [x, y, self.blockpixel, self.blockpixel])
    except AttributeError:
      pass



  def make_new_predication(self):
    self.predicated.update(self.to_predicate)
    new_predication_VaLdict = ValuesareListdict()
    for coord, block in self.to_predicate.items():
      x, y = coord
      distance = block.distance
      trip_list = block.trip_list
      for new_coord in [(x, y+1), (x, y-1), (x+1, y), (x-1, y)]:
        if new_coord[0]<0 or new_coord[1]<0 or new_coord[0]>=self.col or new_coord[1]>=self.row:
          continue
        new_predication_VaLdict.add(new_coord, Block(new_coord, 4, distance+10, trip_list+[new_coord,]))
      for new_coord in [(x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1)]:
        if new_coord[0]<0 or new_coord[1]<0 or new_coord[0]>=self.col or new_coord[1]>=self.row:
          continue
        new_predication_VaLdict.add(new_coord, Block(new_coord, 4, distance+14, trip_list+[new_coord,]))
    temp_dict = dict(new_predication_VaLdict)
    for coord in temp_dict:
      if coord in self.predicated.keys():
        new_predication_VaLdict.pop(coord)
        continue
      if self.map[coord].type == 1:
        new_predication_VaLdict.pop(coord)
        continue
      new_predication_VaLdict[coord]=sorted(new_predication_VaLdict[coord], key=get_distance)
    self.to_predicate = {coord: blocklist[0] for coord, blocklist in new_predication_VaLdict.items()}
  
  def check_found(self):
    for coord in self.to_predicate:
      if self.map[coord].type == 2:
        self.shortcutlist = self.to_predicate[coord].trip_list
        self.found = True
        break

# 함수 정의
def get_distance(block):
  return block.distance

# 상수 정의
color_dict = {
  'BLACK': (0, 0, 0),
  'WHITE': (255, 255, 255),
  'RED': (255, 0, 0),
  'GREEN': (0, 255, 0),
  'BLUE': (0, 0, 255),
  'YELLOW': (255, 255, 0),
  'SKYBLUE': (0, 0, 255),
  'BROWN': (153, 102, 000),
  'LT_BROWN': (204, 153, 102),
  'CREAMY_PURPLE': (204, 153, 255),
  'PALE_YELLOW': (255, 204, 102),
  'DIM_BLACK': (51, 51, 51),
  'DIM_WHITE': (204, 204, 204)
}
map = [
  [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
  [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
  [0, 0, 1, 0, 0, 0, 0, 1, 1, 1],
  [0, 1, 1, 1, 0, 1, 0, 1, 0, 0],
  [0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
  [0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
  [0, 0, 1, 1, 1, 1, 0, 1, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
  [0, 0, 0, 0, 0, 1, 0, 1, 1, 1],
  [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
]
origin = (3, 9)
blockpixel = 40
font_vs_blockpixel = {40: 30}
num_vs_color = {1: 'BROWN', 2: 'YELLOW', 3: 'RED', 4: 'GREEN', 5: 'BLUE'}

# 객체 생성
sfa = ShortcutFinder(map, origin, blockpixel)

pygame.init() # 초기화 (반드시 필요)

# 화면 크기 설정
screen = pygame.display.set_mode((sfa.screen_width, sfa.screen_height))

# 화면 타이틀 설정
pygame.display.set_caption('Shortcut Algorithm')

def main():
  # 이벤트 루프
  running = True # 게임이 진행중인가?
  while running:
    for event in pygame.event.get(): # 어떤 이벤트가 발생하였는가? 를 체크
      if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는가?
        running = False # 게임이 진행중이 아님
  
    sfa.draw_background()
    sfa.draw_grid()
    sfa.draw_map()
    sfa.draw_tile()
    time.sleep(1)
    if not sfa.found:
      sfa.make_new_predication()
    sfa.check_found()

    pygame.display.update()

  # pygame 종료
  pygame.quit()

if __name__=='__main__':
  main()