import mouse
import pyautogui
import time
import check
import screenshot
import mouse as m
from datetime import datetime
from custom_scroll import scroll


class MoveClickCheck:
    def __init__(self, screen_ratio, sets_selected, substats_selected, sands_main_stat_selected,
                 goblet_main_stat_selected, circlet_main_stat_selected, sands_black, goblet_black, circlet_black):
        super().__init__()

        self.screen_ratio = screen_ratio
        self.sets_selected = sets_selected
        self.substats_selected = substats_selected
        self.sands_main_stat_selected = sands_main_stat_selected
        self.goblet_main_stat_selected = goblet_main_stat_selected
        self.circlet_main_stat_selected = circlet_main_stat_selected

        self.sands_black = sands_black
        self.goblet_black = goblet_black
        self.circlet_black = circlet_black

        self.counter = 0
        self.sleep_time = 0.7

        if self.screen_ratio == "16:10":
            self.x, self.y = 45, 80
            self.final_x, self.final_y = 1150, 750
            self.right = 95
            self.scroll = -89.5
            self.y_ = 85
            self.steps = 5
            self.y_plus = 4
        elif self.screen_ratio == "16:9":
            self.x, self.y = 72, 123
            self.final_x, self.final_y = 1750, 1020
            self.right = 142
            self.scroll = -9
            self.y_ = self.y
            self.steps = 5
            self.y_plus = 6
        else:
            self.y_ = 85

    def start(self):
        time.sleep(3)
        # стартовая позиция
        pyautogui.moveTo(self.x, self.y)
        pyautogui.click()
        time.sleep(0.9)
        screenshot.take_screenshot()
        self.sort()
        screenshot.delete_screenshot()

        self.moves()

    def move_down(self):
        pyautogui.moveTo(self.x, self.y_)
        scroll(self.scroll)
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(self.sleep_time)
        screenshot.take_screenshot()
        self.sort()
        screenshot.delete_screenshot()

    def move_right(self):
        for _ in range(self.steps):
            pyautogui.move(self.right, 0)
            pyautogui.click()
            time.sleep(self.sleep_time)
            screenshot.take_screenshot()
            self.sort()
            screenshot.delete_screenshot()

    def sort(self):
        if check.Sort(self.screen_ratio, self.sets_selected, self.substats_selected, self.sands_main_stat_selected,
                      self.goblet_main_stat_selected, self.circlet_main_stat_selected, self.sands_black,
                      self.goblet_black, self.circlet_black).check():
            pyautogui.click()
            time.sleep(0.07)
            print("Оставить")
        else:
            self.counter += 1
            print("Перекрафт")

    def moves(self):
        i = 0
        while self.counter < 39 and i < 15:
            start_time = datetime.now()
            # перемещение, клик, проверка(клик) -> по новой
            self.move_right()
            self.move_down()
            self.y_ = self.y_ + self.y_plus

            i += 1
            print(f"Avg. time: {(datetime.now() - start_time) / 6}")
        pyautogui.moveTo(self.final_x, self.final_y)
        pyautogui.click()
        pyautogui.click()


if __name__ == "__main__":  # для тестовых запусков
    screen_ratio = "16:9"
    sets_selected = ["Странствующий ансамбль",
                     "Церемония древней знати",
                     "Рыцарь крови",
                     "Возлюбленная юная дева",
                     "Изумрудная тень"]
    substats_selected = ['Мастерство стихий']
    sands_main_stat_selected = ['Мастерство стихий']
    goblet_main_stat_selected = ['Мастерство стихий', 'Бонус Анемо урона (%)', 'Бонус Гидро урона (%)',
                                 'Бонус Дендро урона (%)', 'Бонус Пиро урона (%)', 'Бонус Электро урона (%)']
    circlet_main_stat_selected = ['Мастерство стихий']

    sands_black = []
    goblet_black = []
    circlet_black = []

    app = MoveClickCheck(screen_ratio, sets_selected, substats_selected, sands_main_stat_selected,
                         goblet_main_stat_selected, circlet_main_stat_selected, sands_black,
                         goblet_black, circlet_black).start()
