import logging
from typing import Tuple, List, Any

import names_list
import recognition_tesseract


# try:
class Sort:
    def __init__(self, screen_ratio, sets_selected, substats_selected, sands_main_stat_selected,
                 goblet_main_stat_selected, circlet_main_stat_selected, sands_black, goblet_black, circlet_black):
        super().__init__()

        # self.screen = "image11.jpg"  # поменнять на скрины
        self.screen = "screenshot.jpg"
        self.screen_ratio = screen_ratio
        self.sets_selected = sets_selected
        self.substats_selected = substats_selected
        self.sands_main_stat_selected = sands_main_stat_selected
        self.goblet_main_stat_selected = goblet_main_stat_selected
        self.circlet_main_stat_selected = circlet_main_stat_selected

        self.sands_black = sands_black
        self.goblet_black = goblet_black
        self.circlet_black = circlet_black

        self.sands_main_stat_selected = [stat.replace(" (%)", "") for stat in self.sands_main_stat_selected]
        self.sands_main_stat_selected = [stat.replace("тановление энергии", "") for stat in
                                         self.sands_main_stat_selected]

        self.goblet_main_stat_selected = [stat.replace(" (%)", "") for stat in self.goblet_main_stat_selected]
        self.goblet_main_stat_selected = [stat.replace(" урона", "") for stat in self.goblet_main_stat_selected]

        self.circlet_main_stat_selected = [stat.replace(" (%)", " ") for stat in self.circlet_main_stat_selected]

        self.sands_black = [stat.replace(" (%)", "") for stat in self.sands_black]
        self.sands_black = [stat.replace("тановление энергии", "") for stat in self.sands_black]

        self.goblet_black = [stat.replace(" (%)", "") for stat in self.goblet_black]
        self.goblet_black = [stat.replace(" урона", "") for stat in self.goblet_black]

        self.circlet_black = [stat.replace(" (%)", " ") for stat in self.circlet_black]

        self.artifact_list = recognition_tesseract.RecognitionTesseract(self.screen_ratio, self.screen).to_string()
        # self.a = ['Кубок пространства', 'Бонус Гео урона', '7,0%', '+0', 'Шанс крит. попадания +3,5%',
        #           'Мастерство стихий +21', 'Крит. урон +7,8%', 'Сон нимфы']

        if len(self.artifact_list) == 8:
            self.set_position = 7  # if 4 substats
        else:
            self.set_position = 6  # if 3 substats

    def check(self) -> tuple[bool, str]:
        """
        Check if certain conditions are met based on the input parameters and the artifact_list attribute.

        Returns:
            A tuple containing a boolean indicating if the conditions are met and a string indicating the reason for the result.
        """
        if len(self.artifact_list) <= 4:
            logging.error("Something went wrong: artifact skipped")
            return False, "-- Artifact skipped"

        # Check selected sets
        if self.sets_selected:
            for i in self.sets_selected:
                if self.artifact_list[-1][4:] == i[4:]:
                    return True, "+ Set in whitelist"

        # Check main stats for sands artifacts
        if self.artifact_list[0][4:] == names_list.types_of_artifact[2][4:]:
            for mainstat in self.sands_main_stat_selected:
                if self.artifact_list[1][:3] == mainstat[:3]:
                    return True, "+ Main stat (sands)"
            for mainstat_b in self.sands_black:
                if self.artifact_list[1][:3] == mainstat_b[:3]:
                    return False, "- Main stat (sands)"

        # Check main stats for goblet artifacts
        if self.artifact_list[0][:4] == names_list.types_of_artifact[3][:4]:
            for mainstat in self.goblet_main_stat_selected:
                for i in range(0, 3):
                    if self.artifact_list[i][:3] == mainstat[:3]:
                        if self.artifact_list[i][:3] == "Bon":
                            if self.artifact_list[i][5:8] == mainstat[5:8]:
                                return True, "+ Main stat (goblet)"
                        else:
                            return True, "+ Main stat (goblet)"
            for mainstat_b in self.goblet_black:
                for i in range(0, 3):
                    if self.artifact_list[i][:3] == mainstat_b[:3]:
                        if self.artifact_list[i][:3] == "Bon":
                            if self.artifact_list[i][5:8] == mainstat_b[5:8]:
                                return False, "- Main stat (goblet)"
                        else:
                            return False, "- Main stat (goblet)"

        # Check main stats for circlet artifacts
        if self.artifact_list[0][:4] == names_list.types_of_artifact[4][:4]:
            for mainstat in self.circlet_main_stat_selected:
                if self.artifact_list[1][:3] == mainstat[:3]:
                    return True, "+ Main stat (circlet)"
            for mainstat_b in self.circlet_black:
                if self.artifact_list[1][:3] == mainstat_b[:3]:
                    return False, "- Main stat (circlet)"

        # Check substats
        if self.substats_selected:
            for artifact in self.artifact_list:
                for substat in self.substats_selected:
                    if artifact[:3] == substat[:3]:
                        if artifact[:3] == 'НР ' or artifact[:3] == 'Сил' or artifact[:3] == 'Защ':
                            if artifact[-1] == "%" and substat[-2] == '%':
                                return True, "+ Substat"
                            elif artifact[-1] != "%" and substat[-2] != '%':
                                return True, "+ Substat"
                            elif (artifact[-1] == "%" and substat[-2] != '%') or (
                                    artifact[-1] != "%" and substat[-2] == '%'):
                                pass
                        else:
                            return True, "+ Substat"

        return False, ""


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

    sands_black = ['Защита (%)']
    goblet_black = ['Защита (%)', 'HP (%)', 'Бонус физ. урона (%)']
    circlet_black = ['Защита (%)']

    app = Sort(screen_ratio, sets_selected, substats_selected, sands_main_stat_selected,
               goblet_main_stat_selected, circlet_main_stat_selected, sands_black, goblet_black, circlet_black).check()
    # print(app)
