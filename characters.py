import pygame
from random import randint
from math import sqrt


class PlayStatistic:
    '''
    Объект который хранит в себе игровую статистику

    Args:
        width (int): ширина екрана, используется для отрисовки текста

    Attributes:
        score (int): текущее количество очков
        money (int): доступное количество денег игрока
        level (int): текущий уровень игры
        font (pygame.font): шрифт для отображения текста
        w1 (int) : координата x для текста очков
        w2 (int) : координата x для текста денег
        w3 (int) :координата x для текста уровня игры
        next_level_points (int) : количество очков которе нужно набрать для перехода
        на следующий уровень
    '''

    def __init__(self, width: int) -> None:
        '''
        '''
        self.score = 0
        self.money = 100
        self.level = 1
        self.font = pygame.font.SysFont("arialalack", 50)
        self.color = (255,255,255)
        self.w1 = width/15
        self.w2 = width/2.5
        self.w3 = 3*width/4
        self.next_level_points = 3000
    

    def get_money(self) -> int:
        '''
        Returns:
            money: текущее количество доступных денег
        '''

        return self.money
    

    def update_money(self, money: int) -> None:
        '''
        Устанавливает новое количество денег
        Args:
            money (int): количество денег которое нужно установить
        '''
        self.money = money
    

    def add_money(self, money: int) -> None:
        '''увеличивает количество денег на указаную величину

        Args:
            money (int): велечина изменения
        '''
        self.money += money


    def add_score(self, score: int) -> None:
        '''Увеличивает текущее значение очков игры

        Args:
            score (int): количество очков которое добавляется
        '''
        self.score += score
        if self.next_level_points < self.score:
            self.next_level()
            self.next_level_points = self.next_level_points*2
            return True
        return False


    def next_level(self) -> None:
        '''
        Метод перехода на следующий уровеень игры
        '''
        self.level += 1

    
    def drow(self, screen: pygame.Surface) -> None:
        '''
        Метот отрисовки всех данных статистики на екране

        Args:
            screen (pygame.Surface): The amount of distance traveled
        '''
        score = self.font.render(f"Score: {self.score} pts", True, self.color)
        money = self.font.render(f"Money: {self.money} $", True, self.color)
        level = self.font.render(f"LVL - {self.level}", True, self.color)
        score_rect = score.get_rect()
        money_rect = money.get_rect()
        level_rect = level.get_rect()
        score_rect.topleft = (self.w1, 0)
        money_rect.topleft = (self.w2, 0)
        level_rect.topleft = (self.w3, 0)
        screen.blit(score, score_rect)
        screen.blit(money, money_rect)
        screen.blit(level, level_rect)



class StaticObject:
    '''
    Базовый класс для всех объектов 

    Args:
        x (int): координаты центра объекта по горизонтали
        y (int): координаты центра объекта по вертикали
        sprite (pygame.Surface): спрайт для объекта

    Attributes:
        sprite (pygame.Surface): спрайт объекта
        sprite_rect (pygame.Rect): прямоугольная область спрайта
        
    '''
    def __init__(self, x: int, y: int, sprite: pygame.Surface) -> None:

        self.sprite = sprite
        self.sprite_rect = self.sprite.get_rect()
        self.sprite_rect.center = (x, y)
    

    def get_coordinates(self) -> tuple:
        '''
        Метод возвращает координаты центра объекта
        Returns:
            tuple: кортеж координатов (х,у)
        '''
        return (self.sprite_rect.center)


    def drow(self, screen: pygame.Surface) -> None:
        '''
        Метод отрисовки объекта на екране 
        Args:
            screen (pygame.Surface): екран на котором будет произведено рисование
        '''
        screen.blit(self.sprite, self.sprite_rect)
    

    def check_collision(self, other_rect: pygame.Rect) -> bool:
        '''
        Метод проверяет коллизию между текущим объектом и 
        промоугольной областью переданой в качестве параметра
        Args:
            other_rect (pygame.Rect): прямоугольная область

        Returns:
            bool: истина если колизия происходит, иначе ложь
        '''
        return self.sprite_rect.colliderect(other_rect)



class StaticHP(StaticObject):
    '''
    Базовый класс для всех объектов которые имеют здоровье
    наследуется от класса StaticObject

    Args:
        x (int): координаты центра объекта по горизонтали
        y (int): координаты центра объекта по вертикали
        sprite (pygame.Surface): спрайт для объекта
        health (int): здоровье для данного объекта

    Attributes:
        sprite (pygame.Surface): спрайт объекта
        sprite_rect (pygame.Rect): прямоугольная область спрайта
        total_health (int): максимальный уровень здоровья
        health (int): текущий уровень здоровья
        
    '''
    def __init__(self, x: int, y: int, sprite: pygame.Surface, health: int) -> None:
        '''
        '''
        StaticObject.__init__(self, x, y, sprite)
        self.total_health = health
        self.health = health


    def drow_HP(self, screen: pygame.Surface) -> None:
        '''
        Метод отрисовки уровня здоровья для текущего объекта на екране 
        Args:
            screen (pygame.Surface): екран на котором будет произведено рисование
        '''
        color_bg = (255,0,0)
        color = (0,255,0)
        height = 10
        start_pos = self.sprite_rect.topleft
        end_pos = self.sprite_rect.topright
        pygame.draw.line(screen, color, start_pos, end_pos, height)
        width = int(self.sprite_rect.width*self.health/self.total_health)
        end_pos = end_pos[0]-width, end_pos[1]
        pygame.draw.line(screen, color_bg, start_pos, end_pos, height)


    def drow(self, screen: pygame.Surface) -> None:
        '''
        Метод отрисовки объекта на екране
        вызывает родительский метод отрисовки объекта + 
        метод отрисовки здоровья
        Args:
            screen (pygame.Surface): екран на котором будет произведено рисование
        '''
        StaticObject.drow(self, screen)
        self.drow_HP(screen)



class Tower(StaticHP):
    '''
    Класс для объекта главного здания
    наследуется от StaticHP

    Args:
        path_to_png (str): путь до изображения спрайта

    Attributes:
        sprite (pygame.Surface): спрайт объекта
        sprite_rect (pygame.Rect): прямоугольная область спрайта
        total_health (int): максимальный уровень здоровья
        health (int): текущий уровень здоровья
    '''

    def __init__(self, path_to_png: str) -> None:

        x = 100
        y = 250
        health = 1000
        sprite = pygame.image.load(path_to_png)
        StaticHP.__init__(self, x, y, sprite, health)
    

    def destroyed(self) -> bool:
        '''
        Метод проверяет разрушено главное здание или нет
        Returns:
            bool: истина если здоровье больше нуля, иначе ложь
        '''
        return self.health <= 0


    def destenation(self) -> tuple:
        '''
        Метод возвращает координаты (низ, центр) крепости
        Returns:
            tuple: координаты (х,у)
        '''
        return self.sprite_rect.midbottom
    

    def hit(self, damage: int) -> None:
        '''
        Метод уменьшения здоровья крепости на указаное количество урона
        Args:
            damage (int): величина урона
        '''
        self.health -= damage
        


class Road(StaticObject):
    '''
    Класс дороги

    Args:
        tower (Tower): обьект крепости
        width (int): ширина дороги

    Attributes:
        destenation (tuple): координаты крепости
        color (tuple): цвет отрисовки дороги
        width (int): ширина дороги
        sprite_rect (pygame.Rect): прямоугольная область спрайта   
    '''
    def __init__(self, tower: Tower, width: int) -> None:

        destenation = tower.destenation()
        self.y = destenation[1]
        self.x1 = width
        self.x2 = 0
        self.color = (80,80,80)
        self.width = 150
        self.sprite_rect = pygame.Rect(0, 0, self.x1, self.width)
        self.sprite_rect.centery = self.y


    @property
    def get_y_range(self) -> tuple:
        '''
        '''
        return (self.sprite_rect.top, self.sprite_rect.bottom)


    @property
    def start_pos(self) -> tuple:
        '''
        '''
        return (self.x1, self.y)
    

    @property
    def end_pos(self) -> tuple:
        '''
        '''
        return (self.x2, self.y)


    def drow(self, screen: pygame.Surface) -> None:
        '''
        '''
        pygame.draw.rect(screen, self.color, self.sprite_rect)



class Enemy(StaticHP):
    '''
    Класс вражеского объекта
    Наследуется от StaticHP
    Args:
        sprite (pygame.image): спрайт объекта
        road (Road): объект дороги
        unit_level (int): уровень врага
        speed (float): скорость передвижения врага
    Attributes:
        sprite (pygame.Surface): спрайт объекта
        sprite_rect (pygame.Rect): прямоугольная область спрайта
        total_health (int): максимальный уровень здоровья
        health (int): текущий уровень здоровья
        speed (float): скорость передвижения врага
        damage (int): урон
        money (int): деньги за уничтожение
    
    '''
    def __init__(self, sprite: pygame.image, road: Road, unit_level: int, speed: float) -> None:
        
        x = randint(road.x1+10, road.x1+50)
        y = randint(*road.get_y_range)
        health = 150 + 10*(unit_level+10)
        sprite = pygame.transform.rotate(sprite, 90)
        StaticHP.__init__(self, x, y, sprite, health)
        self.speed = speed
        self.x = x
        self.damage = 10 * unit_level
        self.money = unit_level * 2


    def move(self):
        
        self.x -= self.speed
        self.sprite_rect.x = self.x
    

    def get_distance(self, rect: pygame.Rect) -> float:
        
        distance = sqrt(
            (self.sprite_rect.centerx - rect.centerx) ** 2 +
            (self.sprite_rect.centery - rect.centery) ** 2)
        
        return distance
    

    def not_alive(self) -> bool:
        
        return self.health <= 0



class Enemies:
    '''
    Класс который хранит в себе все вражеские объекты
    Args:
        img_path (str): путь к директории со спрайтами
        target (Tower): объект крепости
        road (Road): объект дороги
        screen (pygame.Surface): екран
        statistic (PlayStatistic): статистика игры
    Attributes:
        enemies (list): список врагов
        sprites (list): список спрайтов для врагов
        road (Road): объект дороги
        target (Tower): объект крепости
        screen (pygame.Surface): екран
        statistic (PlayStatistic): объект статистики
        speed (float): текущая скорость для всех врагов
    
    '''
    def __init__(self, img_path: str, target: Tower, road: Road, screen: pygame.Surface, statistic: PlayStatistic) -> None:

        self.enemies:list[Enemy] = []
        self.sprites = [pygame.image.load(f"{img_path}{i}.png") for i in range(1,20)]
        self.road = road
        self.target = target
        self.screen = screen
        self.statistic = statistic
        self.speed = 1.0


    def next_score(self):
        
        self.speed += 0.5
        for unit in self.enemies:
            
            unit.speed += 0.5

    def spawn(self) -> None:

        max_lvl = min(len(self.sprites)-1, self.statistic.level*2)
        unit_level = randint(0, max_lvl)
        unit = Enemy(self.sprites[unit_level], self.road, unit_level+1, self.speed)
        for enemy in self.enemies:
            if enemy.check_collision(unit.sprite_rect):
                return
        
        self.enemies.append(unit)


    def move(self) -> None:
        
        i = 0
        while i < len(self.enemies):
            unit = self.enemies[i]
            unit.move()
            if unit.sprite_rect.centerx <= self.target.sprite_rect.centerx:
                self.target.hit(unit.damage)
                self.enemies.pop(i)
                continue
            i += 1
            
    
    def drow(self) -> None:
        
        lvl = self.statistic.level
        rnd = randint(0, 100)
        if rnd < lvl:
            self.spawn()
        for unit in self.enemies:
            unit.drow(self.screen)
    

    def hit(self, index: int, demage: int) -> None:
        
        self.enemies[index].health -= demage
        if self.statistic.add_score(demage):
            self.next_score()
        if self.enemies[index].not_alive():
            money = self.enemies[index].money
            self.statistic.add_money(money)
            self.enemies.pop(index)




class Bulet:
    '''
    Класс пули
    Args:
        start_pos (tuple): координаты начала полета пули
        end_pos (tuple): координаты цели
        width (int): ширина пули
    Attributes:
        start_pos (tuple): координаты начала полета пули
        end_pos (tuple): координаты цели
        color (tuple): цвет выстрела
        width (int): ширина пули
        timer (int): время полета пули

    '''
    def __init__(self, start_pos: tuple, end_pos: tuple, width: int) -> None:
        
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = (255,0,0)
        self.width = width+2
        self.timer = 3
    

    def tick(self) -> None:
        
        self.timer -= 1
        

    def drow(self, screen: pygame.Surface) -> None:
        
        pygame.draw.line(
                    screen,
                    self.color,
                    self.start_pos,
                    self.end_pos,
                    self.width)
        self.tick()


    def is_alive(self) -> bool:
        
        return self.timer > 0



class Defense(StaticObject):
    '''
    Класс объекта защитного сооружения
    Наследуется от StaticObject
    Args:
        x (int): координаты по горизонтали
        y (int): координаты по вертикали
        sprites (list): список спрайтов
        y_road (int): координата центра дороги по вертикали

    Attributes:
        direction (int): положение относсительно дороги
        sprites (list): список спрайтов
        level (int): уровень сооружения
        max_level (int): максимальный возможный уровень
        wait (int): время между выстрелами
        alpha_color (tuple): цвет границы поражения
        font (pygame.font): шрифт надписи для стоимости
        distance (int): дальность поражения
        demage (int): наносимый урон
        upgrade_coast (int): стоимость улучшения
        caption (str): подпись
        caption_rect (pygame.Rect): область подписи
    
    '''
    def __init__(self, x: int, y: int, sprites: list, y_road: int) -> None:
        
        self.direction = -1
        self.sprites = sprites
        sprite = self.sprites[0]
        if y < y_road:
            sprite = pygame.transform.rotate(sprite, 180)
            self.direction = 1
        StaticObject.__init__(self, x, y, sprite)
        self.level = 1
        self.max_level = len(self.sprites)
        self.wait = 0
        self.alpha_color = pygame.Color(50,50,205)
        self.font = pygame.font.SysFont("arialalack", 30)
        self.update_level()
        


    def update_level(self) -> None:
                
        self.level += 1
        self.distance = 120 + self.level * 10
        self.demage = 50 + self.level * 3
        self.upgrade_coast = self.level * 15
        if self.level >= self.max_level:
            self.caption = self.font.render(f"MAX", True, self.alpha_color)
        else:
            self.caption = self.font.render(f"{self.upgrade_coast}$", True, self.alpha_color)
        self.caption_rect = self.caption.get_rect()
        if self.direction == 1:
            self.caption_rect.midbottom = self.sprite_rect.midtop
        else:
            self.caption_rect.midtop = self.sprite_rect.midbottom
        



    def upgrade(self, statistic: PlayStatistic) -> None:
        
        money = statistic.get_money()
        if money < self.upgrade_coast or self.level >= self.max_level:
            return
        sprite = self.sprites[self.level]
        if self.direction == 1:
            sprite = pygame.transform.rotate(sprite, 180)
        statistic.update_money(money - self.upgrade_coast)
        self.sprite = sprite
        self.update_level()



    def show_radius(self, screen: pygame.Surface) -> None:
        
        center = self.sprite_rect.center
        radius = self.distance - 25
        pygame.draw.circle(screen, self.alpha_color, center, radius, width=1)


    def drow(self, screen: pygame.Surface) -> None:
        
        StaticObject.drow(self, screen)
        self.show_radius(screen)
        screen.blit(self.caption, self.caption_rect)




    def get_x_y_for_bulet(self) -> tuple:
        
        if self.direction == 1:
            return self.sprite_rect.midbottom
        else:
            return self.sprite_rect.midtop


    def reload(self) -> None:
        
        self.wait = 25 - self.level


    def is_ready(self) -> bool:
        
        if self.wait <= 0:
            return True
        self.wait -= 1
        return False



    def hit(self, enemies: Enemies, bulets: list[Bulet]) -> None:
        
        if self.is_ready():
            nearest = None
            min_distance = None
            for i in range(len(enemies.enemies)):
                unit = enemies.enemies[i]
                distance = unit.get_distance(self.sprite_rect)
                if distance <= self.distance:
                    if nearest is None:
                        nearest = i
                        min_distance = distance
                    else:
                        if min_distance > distance:
                            nearest = i
                            min_distance = distance
            if nearest is not None:
                bulets.append(Bulet(
                    self.get_x_y_for_bulet(),
                    enemies.enemies[nearest].sprite_rect.center,
                    self.level))
                enemies.hit(nearest, self.demage)
                self.reload()



class Defenses:
    '''
    Класс который хранит в себе все защитные сооружения
    Args:
        img_path (str): путь к директории со спрайтами
        tower (Tower): объект крепости
        road (Road): объект дороги
        screen (pygame.Surface): екран
        enemies (Enemies): вражеские обьекты
    Attributes:
        defenses (list): список защитных сооружений
        sprites (list): список спрайтов для врагов
        road (Road): объект дороги
        tower (Tower): объект крепости
        screen (pygame.Surface): екран
        enemies (Enemies): вражеские обьекты
        bulets (list[Bulet]): список выстрелов
    
    '''
    def __init__(
                self,
                img_path: str,
                tower: Tower,
                road: Road,
                screen: pygame.Surface,
                enemies: Enemies
                ) -> None:
        
        self.defenses:list[Defense] = []
        self.sprites = [pygame.image.load(f"{img_path}{i}.png") for i in range(1, 16)]
        self.road = road
        self.tower = tower
        self.screen = screen
        self.enemies = enemies
        self.bulets:list[Bulet] = []
    

    def left_click(self, position: tuple, statistic: PlayStatistic) -> None:
        
        click_rect = pygame.Rect(*position,1,1)
        for unit in self.defenses:
            if unit.check_collision(click_rect):
                unit.upgrade(statistic)
                return
            
        self.spawn(*position, statistic)


    def right_click(self, position: tuple, statistic: PlayStatistic) -> None:
        
        click_rect = pygame.Rect(*position,1,1)
        for i in range(len(self.defenses)):
            unit = self.defenses[i]
            if unit.check_collision(click_rect):
                coast = unit.upgrade_coast // 2
                statistic.add_money(coast)
                self.defenses.pop(i)
                return




    def spawn(self, x: int, y: int, statistic: PlayStatistic) -> None:
        
        money = statistic.get_money()
        unit = Defense(x, y, self.sprites, self.road.y)
        coast = unit.upgrade_coast
        if coast > money:
            return
        if unit.check_collision(self.road.sprite_rect):
            return
        self.defenses.append(unit)
        statistic.update_money(money - coast)


    def drow(self):
        
        for unit in self.defenses:
            unit.hit(self.enemies, self.bulets)
            unit.drow(self.screen)
        i = 0
        while i < len(self.bulets):
            self.bulets[i].drow(self.screen)
            if not self.bulets[i].is_alive():
                self.bulets.pop(i)
                continue
            i += 1
  