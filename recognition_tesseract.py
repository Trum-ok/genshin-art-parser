import cv2
import json
import pytesseract
from datetime import datetime

import names_list
from utils import resource_path

startTime = datetime.now()


class RecognitionTesseract:
    def __init__(self, screen_ratio, screen):
        super().__init__()
        self.screen_ratio = screen_ratio
        self.screen = screen

        if self.screen_ratio == "16:10":
            self.x1_percent, self.y1_percent = 52, 21
            self.x2_percent, self.y2_percent = self.x1_percent + 24, self.y1_percent + 40
        elif self.screen_ratio == "16:9":
            self.x1_percent, self.y1_percent = 52, 21
            self.x2_percent, self.y2_percent = self.x1_percent + 24, self.y1_percent + 47
            # self.x1_percent, self.y1_percent = 52, 23
            # self.x2_percent, self.y2_percent = self.x1_percent + 24, self.y1_percent + 46

        self.img = cv2.imread(self.screen)

        self.height, self.width, _ = self.img.shape

        self.x1, self.y1 = int(self.width * self.x1_percent / 100), int(self.height * self.y1_percent / 100)
        self.x2, self.y2 = int(self.width * self.x2_percent / 100), int(self.height * self.y2_percent / 100)

        self.cropped_img = self.img[self.y1:self.y2, self.x1:self.x2]

        # self.gray = cv2.cvtColor(self.cropped_img, cv2.COLOR_BGR2GRAY)
        # self.text = pytesseract.image_to_string(self.gray, lang='rus')

        self.alpha = 1.6  # Contrast control
        self.beta = -127  # Brightness control
        self.adjusted = cv2.convertScaleAbs(self.cropped_img, alpha=self.alpha, beta=self.beta)

        self.gray = cv2.cvtColor(self.adjusted, cv2.COLOR_BGR2GRAY)

    def to_string(self):
        # self.text = pytesseract.image_to_string(self.cropped_img, lang='rus', config='--oem 3')
        text = pytesseract.image_to_string(self.gray, lang='rus',
                                           config=f'--oem 3 -c preserve_interword_spaces=1 -c tessedit_char_whitelist="{names_list.char_list}" ')
        text_lines = text.split('\n')

        while "" in text_lines:
            text_lines.remove("")

        # if len(text_lines) > 4:
        #     with open("logs\\summary.txt", 'a') as txt_file:
        #         json.dump(text_lines, txt_file, ensure_ascii=False)
        #         txt_file.write("\n")

        text_lines_mod = [item.replace(":", "") for item in text_lines]
        text_lines_mod = [item.replace("* ", "") for item in text_lines_mod]
        text_lines_mod = [item.replace("т,", "т.") for item in text_lines_mod]
        text_lines_mod = [item.replace("аа", "а а") for item in text_lines_mod]
        text_lines_mod = [item.replace("HP", "НР ") for item in text_lines_mod]  # from En-en to Ru-ru
        text_lines_mod = [item.replace("НР", "НР ") for item in text_lines_mod]
        text_lines_mod = [item.replace(', ', "") for item in text_lines_mod]
        # text_lines_mod = [item.replace(',', "") for item in text_lines_mod]
        text_lines_mod = [item.replace('           А', "") for item in text_lines_mod]
        text_lines_mod = [item.replace('            ц,', "") for item in text_lines_mod]
        text_lines_mod = [item.replace('ох', "") if len(item) == 2 else item for item in text_lines_mod]
        text_lines_mod = [item.replace("п", "") if len(item) == 1 else item for item in text_lines_mod]
        text_lines_mod = [item.replace("П", "") if len(item) == 1 else item for item in text_lines_mod]
        text_lines_mod = [item.replace("ч", "") if len(item) == 1 else item for item in text_lines_mod]
        text_lines_mod = [item.replace("Г", "") if len(item) == 1 else item for item in text_lines_mod]
        text_lines_mod = [item.replace("У", "") if len(item) == 1 else item for item in text_lines_mod]
        text_lines_mod = [item.replace("Х", "") if len(item) == 1 else item for item in text_lines_mod]

        # Удаляем некоторые элементы
        to_remove = ['      ', 'Ж', 'ж', '+', 'ч', '2', '@', 'н', ', ', ',', 'я', 'хи ']
        text_lines_mod = [line for line in text_lines_mod if
                          not any(line.startswith(prefix) for prefix in to_remove)]

        while "" in text_lines_mod:
            text_lines_mod.remove("")

        text_lines_mod = [item.strip() if item.startswith(' ') else item for item in text_lines_mod]

        if text_lines_mod[-1].startswith('2 предмета') or text_lines_mod[-1].startswith('2'):
            text_lines_mod.pop()

        for i in text_lines_mod:
            if i in ["о", "ох", "У", "ох"]:
                text_lines_mod.remove(i)

        if len(text_lines_mod) > 4:
            with open("logs\\summary.txt", 'a') as txt_file:
                json.dump(text_lines_mod, txt_file, ensure_ascii=False)
                txt_file.write("\n")
        return text_lines_mod


second = datetime.now() - startTime

if __name__ == "__main__":  # для тестовых запусков
    screen_ratio = "16:9"
    screen = "img/imaagetest.png"
    # screen = "screenshot.jpg"
    app = RecognitionTesseract(screen_ratio, screen).to_string()
    print(datetime.now() - startTime + second)
