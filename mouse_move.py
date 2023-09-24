import json
import time
import logging
from PIL import Image
from datetime import datetime

import check
import screenshot
from custom_scroll import scroll
# from utils import *
from utils import moveRel, moveTo, click


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

        # if self.screen_ratio == "16:10":
        #     self.x, self.y = 45, 80
        #     self.final_x, self.final_y = 1150, 750
        #     self.right = 95
        #     self.scroll = -89.5
        #     self.y_correction = 85
        #     self.steps = 5
        #     self.y_plus = 4
        # elif self.screen_ratio == "16:9":
        #     # self.x, self.y = 72, 123
        #     # self.final_x, self.final_y = 1750, 1020
        #     # self.right = 142
        #     # self.scroll = -9
        #     # self.y_correction = self.y
        #     # self.steps = 5
        #     self.y_plus = 6
        #     ...
        # else:
        #     self.y_correction = 85

    def get_positions(self):
        screenshot.take_screenshot()
        im = Image.open("screenshot.jpg")
        width, height = im.size

        self.x0 = width * 0.038
        self.y0 = height * 0.1125

        self.y_correction = self.y0

        self.right_shift = width * 0.074
        self.scroll = -9
        self.steps = 5
        self.y_plus = 6

        self.final_x = width * 0.9065
        self.final_y = height * 0.95

    def start(self):
        time.sleep(3)  # time to open Genshin window
        self.get_positions()
        moveTo(self.x0, self.y0)  # start position
        logging.info("Mouse moved to the start position")
        click()
        time.sleep(0.9)
        screenshot.take_screenshot()
        self.sort()
        screenshot.delete_screenshot()

        self.moves()

    def move_down(self):
        moveTo(self.x0, self.y_correction)
        time.sleep(0.07)
        scroll(self.scroll)
        time.sleep(0.1)
        click()
        time.sleep(self.sleep_time)
        screenshot.take_screenshot()
        self.sort()
        screenshot.delete_screenshot()

    def move_right(self):
        for _ in range(self.steps):
            moveRel(self.right_shift, 0)
            time.sleep(self.sleep_time / 2)
            click()
            time.sleep(self.sleep_time)
            screenshot.take_screenshot()
            self.sort()
            screenshot.delete_screenshot()

    def sort(self):
        sort_result = check.Sort(self.screen_ratio, self.sets_selected, self.substats_selected,
                                 self.sands_main_stat_selected,
                                 self.goblet_main_stat_selected, self.circlet_main_stat_selected, self.sands_black,
                                 self.goblet_black, self.circlet_black).check()
        if sort_result[0]:
            click()
            time.sleep(0.07)
            with open("logs\\summary.txt", 'a') as txt_file:
                json.dump(f"Оставить ({sort_result[1]})", txt_file, ensure_ascii=False, indent=2)
                txt_file.write("\n")
        else:
            self.counter += 1
            with open("logs\\summary.txt", 'a') as txt_file:
                if sort_result[1] == "-- Artifact skipped":
                    json.dump(sort_result[1], txt_file, ensure_ascii=False, indent=2)
                else:
                    json.dump(f"Перекрафт ({sort_result[1]})", txt_file, ensure_ascii=False, indent=2)
                txt_file.write("\n")

    def moves(self):
        i = 0
        while self.counter < 39 and i < 15:
            start_time = datetime.now()
            self.move_right()
            self.move_down()
            self.y_correction += self.y_plus

            i += 1
            logging.info(f"Avg. time: {(datetime.now() - start_time) / 6}")
        moveTo(self.final_x, self.final_y)
        click()
        click()


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
