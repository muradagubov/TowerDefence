import pygame
from characters import *



def show_game_over(screen: pygame.Surface, score: int) -> None:
    '''
    функция отображения на екране текста после проиграной игры
    Args:
        screen (pygame.Surface): екран на котором будет произведено отображение
        score (int): количество набраных очков
    '''
    texts = ["GAME OVER", f"YOUR SCORE {score}", "press any key to start new game"]
    screen.fill((0,0,0))
    font = pygame.font.SysFont("arialalack", 60)
    color = (220,220,220)
    scren_rec = screen.get_rect()
    x = scren_rec.centerx
    y = 250
    for row in texts:
        text = font.render(row, False, color)
        text_rect = text.get_rect()
        text_rect.center = (x,y)
        y += text_rect.height + 20
        screen.blit(text, text_rect)
        font = pygame.font.SysFont("arialalack", 35)



def show_menu(screen: pygame.Surface) -> None:
    '''
    функция отображения меню и инструкции на екране
    Args:
        screen (pygame.Surface): екран на котором будет произведено отображение
    '''
    instructions = [
                "Tower Defence",
                "Цель игры защитить крепость от вражеских нападений",
                "Чтобы построить защитное сооружение нажмите ЛКМ в любом свободном месте",
                "Для того, чтобы модернизировать сооружение нажмите на него ЛКМ и ПКМ, чтобы разрушить",
                "Стоимость улучшений отображается под или над сооружением",
                "За разрушенное сооружение Вы получаете обратно половину его стоимости",
                "Нажмите Space/Esc, чтобы поставить игру на паузу/продолжить игру"
                ]
    screen.fill((0,0,0))
    font = pygame.font.SysFont("arialalack", 30)
    color = (220,220,220)
    scren_rec = screen.get_rect()
    x = scren_rec.centerx
    y = 150
    for row in instructions:
        text = font.render(row, False, color)
        text_rect = text.get_rect()
        text_rect.center = (x,y)
        y += text_rect.height + 10
        screen.blit(text, text_rect)


def generate_game_objects(
                            w: int,
                            screen: pygame.Surface,
                            tower_img: str,
                            enemy_src: str,
                            defense_src: str) -> tuple:
    '''
    функция генераци игровых обьектов
    Args:
        w (int): ширина екрана
        screen (pygame.Surface): екран на котором будет произведено отображение
        tower_img (str): путь к изображению крепости
        enemy_src: (str): путь к директории со спрайтами врагов
        defense_src (str): путь к директории со спрайтами защитных
    Returns:
            tower (Tower): объект крепости
            road (Road): объект дороги
            statistic (PlayStatistic): объект статистики игры
            enemies (Enemies): объект списка врагов
            defenses (Defenses): объект списка защитных сооружений
    '''

    tower = Tower(tower_img)
    road = Road(tower, w)
    statistic = PlayStatistic(w)
    enemies = Enemies(enemy_src, tower, road, screen, statistic)
    defenses = Defenses(defense_src, tower, road, screen, enemies)
    
    return (tower, road, statistic, enemies, defenses)



def main():
    '''
    Главная функция в которой происходит инициализация всех объектов и 
    запуск цикла игры
    обработка пользовательского ввода
    '''
    w, h = 1000, 600
    FPS = 25
    # спрайты юнитов взяты с сайта:
    # http://freegameassets.blogspot.com/2015/02/free-tower-defence-sets-this-free-tower.html
    tower_img = "src/tower.png"
    enemy_src = "src/enemies/"
    defense_src = "src/defenses/"
    screen_size = (w, h)
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Tower Defence') 
    bg_color = (50,205,50)
    timer = pygame.time.Clock()
    tower, road, statistic, enemies, defenses = generate_game_objects(
            w,
            screen,
            tower_img,
            enemy_src,
            defense_src
            )
    running = True
    new_game = True
    menu = True
    game_over = False
    while running:
        if menu:
            show_menu(screen)
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        menu = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                            menu = False
        else:
            
            if new_game:
                tower, road, statistic, enemies, defenses = generate_game_objects(
                    w,
                    screen,
                    tower_img,
                    enemy_src,
                    defense_src)
                new_game = False
                game_over = False
            elif game_over:
                score = statistic.score
                show_game_over(screen, score)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                        new_game = True
                        menu = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_presses = pygame.mouse.get_pressed()
                        if mouse_presses[0]:
                            defenses.left_click(event.pos, statistic)
                        if mouse_presses[2]:
                            defenses.right_click(event.pos, statistic)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                            menu = True
                screen.fill(bg_color)
                road.drow(screen)
                defenses.drow()
                tower.drow(screen)
                enemies.drow()
                statistic.drow(screen)
                enemies.move()
                if tower.destroyed():
                    game_over = True
        pygame.display.update()
        timer.tick(FPS)


if __name__ == "__main__":
    main()