import threading
import unittest
from mock import patch
import pygame
from alien_invasion import AlienInvasion
import time


class MyTestCase(unittest.TestCase):
    def test_UP(self):
        # 判断是否按下"上"键
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
        self.mock_obj._check_keydown_events(event)
        self.assertEqual(self.mock_obj.ship.moving_up, True)
        # 休眠2秒
        time.sleep(2)
        # 4秒后判断是否超出范围
        self.assertGreaterEqual(self.mock_obj.ship.rect.top, 0)

        # 判断是否松开"上"键
        event = pygame.event.Event(pygame.KEYUP, key=pygame.K_UP)
        self.mock_obj._check_keyup_events(event)
        self.assertEqual(self.mock_obj.ship.moving_up, False)
        print("上移测试通过")

    def test_DOWN(self):
        # 判断是否按下"下"键
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
        self.mock_obj._check_keydown_events(event)
        self.assertEqual(self.mock_obj.ship.moving_down, True)
        # 休眠2秒
        time.sleep(2)
        # 8秒后判断是否超出范围,界面底部的值要大于飞船底部的值,否则就是超出界面
        self.assertGreaterEqual(self.mock_obj.screen.get_rect().bottom, self.mock_obj.ship.rect.bottom)

        # 判断是否松开"下"键
        event = pygame.event.Event(pygame.KEYUP, key=pygame.K_DOWN)
        self.mock_obj._check_keyup_events(event)
        self.assertEqual(self.mock_obj.ship.moving_down, False)
        print("下移测试通过")

    def test_RIGHT(self):
        # 判断是否按下"右"键
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
        self.mock_obj._check_keydown_events(event)
        self.assertEqual(self.mock_obj.ship.moving_right, True)
        # 休眠1秒
        time.sleep(1)
        # 1秒后判断是否超出范围,飞船右边要小于200像素,否则就是超出界面
        self.assertGreaterEqual(250, self.mock_obj.ship.rect.right)

        # 判断是否松开"右"键
        event = pygame.event.Event(pygame.KEYUP, key=pygame.K_RIGHT)
        self.mock_obj._check_keyup_events(event)
        self.assertEqual(self.mock_obj.ship.moving_right, False)
        print("右移测试通过")

    def test_LEFT(self):
        # 判断是否按下"左"键
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)
        self.mock_obj._check_keydown_events(event)
        self.assertEqual(self.mock_obj.ship.moving_left, True)
        # 休眠2秒
        time.sleep(2)
        # 2秒后判断是否超出范围,飞船左边要大于0像素,否则就是超出界面
        self.assertGreaterEqual(self.mock_obj.ship.rect.left, 0)

        # 判断是否松开"左"键
        event = pygame.event.Event(pygame.KEYUP, key=pygame.K_LEFT)
        self.mock_obj._check_keyup_events(event)
        self.assertEqual(self.mock_obj.ship.moving_left, False)
        print("左移测试通过")

    def test_Space(self):
        # 连续按3次空格
        for bullet_num in range(1, 4):
            event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
            self.mock_obj._check_keydown_events(event)
            event = pygame.event.Event(pygame.KEYUP, key=pygame.K_SPACE)
            self.mock_obj._check_keyup_events(event)
            # 休眠0.2秒,继续
            time.sleep(0.3)
        # 子弹数量是否等于num(当前应该正确的子弹数量)
        self.assertEqual(len(self.mock_obj.bullets), bullet_num)
        print("子弹测试通过")

    def test_ship_hit(self):
        # 模拟飞船被击中
        self.mock_obj._ship_hit()
        # 被击中一次,生命值减1
        self.assertEqual(self.mock_obj.stats.ships_left, 2)
        print("生命值减少测试通过")

    def test_quit(self):
        # 模拟按下"Q"键
        time.sleep(1)
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q)
        self.mock_obj._check_keydown_events(event)
        self.assertEqual(self.mock_obj.end_game, True)
        event = pygame.event.Event(pygame.KEYUP, key=pygame.K_q)
        print("退出游戏测试通过")

    def test_click_play(self):
        # 模拟按下play
        time.sleep(2)
        pygame.mouse.set_pos(773, 455)
        mouse_pos = pygame.mouse.get_pos()
        self.mock_obj._check_play_button(mouse_pos)
        self.assertEqual(self.mock_obj.stats.game_active, True)
        print()
        print("开始游戏测试通过")

    @patch("alien_invasion.AlienInvasion")
    def test(self, mock_game):
        mock_game.return_value = AlienInvasion()
        self.mock_obj = mock_game()

        try:
            t = threading.Thread(target=self.mock_obj.run_game)
            # 开始游戏
            t.start()
            # 鼠标单击测试
            self.test_click_play()
            # 右移测试
            self.test_RIGHT()
            # 左移测试
            self.test_LEFT()
            # 上移测试
            self.test_UP()
            # 下移测试
            self.test_DOWN()
            # 子弹测试
            self.test_Space()
            # 生命值减少测试
            self.test_ship_hit()
            # q键退出测试
            self.test_quit()

        except Exception as e:
            print(e)


if __name__ == '__main__':
    unittest.main()
