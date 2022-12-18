import pytest
import pygame
from characters import *

'''
Тестируем класс PlayStatistic
включены как положительные, так и отрицательные результаты
'''

def test_Play_Statistic_money():
    pygame.init()
    statistic = PlayStatistic(1000)
    assert statistic.get_money() == 100
    

def test_Play_Statistic_add_money():
    pygame.init()
    statistic = PlayStatistic(1000)
    statistic.add_money(100)
    assert statistic.get_money() == 200


def test_Play_Statistic_add_score():
    pygame.init()
    statistic = PlayStatistic(1000)
    statistic.add_score(10000)
    assert statistic.score == 10000


def test_Play_Statistic_update_money():
    pygame.init()
    statistic = PlayStatistic(1000)
    statistic.update_money(123)
    assert statistic.money == 123


@pytest.mark.parametrize('width', [1000, 2000, 3000, 4000])
def test_Play_Statistic_width(width):

    pygame.init()
    statistic = PlayStatistic(width)
    assert statistic.w1 == width/15



def test_Play_Statistic_Exception():
    pygame.init()
    with pytest.raises(TypeError):
        statistic = PlayStatistic("1000")



# отрицательный тест
@pytest.mark.xfail()
def test_Play_Statistic_drow():
    pygame.init()
    statistic = PlayStatistic(640)
    statistic.drow("Not screen obj")


