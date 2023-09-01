import names_list
import recognition_tesseract


class Sort:
    def __init__(self, screen_ratio, sets_selected, substats_selected, sands_main_stat_selected,
                 goblet_main_stat_selected, circlet_main_stat_selected, sands_black, goblet_black, circlet_black):
        super().__init__()


        # self.screen = "image11.jpg"  # поменнять на скрины
        self.screen = "screenshot.jpg"  # поменнять на скрины
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

        self.circlet_main_stat_selected = [stat.replace(" (%)", "") for stat in self.circlet_main_stat_selected]

        self.sands_black = [stat.replace(" (%)", "") for stat in self.sands_black]
        self.sands_black = [stat.replace("тановление энергии", "") for stat in self.sands_black]

        self.goblet_black = [stat.replace(" (%)", "") for stat in self.goblet_black]
        self.goblet_black = [stat.replace(" урона", "") for stat in self.goblet_black]

        self.circlet_black = [stat.replace(" (%)", "") for stat in self.circlet_black]

        self.artifact_list = recognition_tesseract.RecognitionTesseract(self.screen_ratio, self.screen).to_string()
        # self.a = ['Кубок пространства', 'Бонус Гео урона', '7,0%', '+0', 'Шанс крит. попадания +3,5%',
        #           'Мастерство стихий +21', 'Крит. урон +7,8%', 'Сон нимфы']

        self.reason = []

        if len(self.artifact_list) == 8:
            self.set_position = 7
            print("4 сабстата")
        else:
            self.set_position = 6
            print("3 сабстата")

    def check(self):
        if len(self.artifact_list) < 3:
            print(" -" * 15)
            print("Артефакт пропущен...")
            return False
        else:
            # Сет
            for i in self.sets_selected:
                if self.artifact_list[-1] == i:
                    self.reason = "+ Сет в вайтлисте"
                    print(self.reason)
                    return True  # оставить артефакт

            # ОПЦИОНАЛЬНО

            # Пески
            if self.artifact_list[0][4:] == names_list.types_of_artifact[2][4:]:
                if any(self.artifact_list[i].startswith(substring) for substring in self.sands_main_stat_selected for i
                       in
                       range(1, len(self.artifact_list)-3)):
                    self.reason = "+ Мейнстат (пески)"
                    print(self.reason)
                    return True  # оставить артефакт

                # Блэклист пески
                if any(self.artifact_list[i].startswith(substring) for substring in self.sands_black for i in
                       range(1, len(self.artifact_list)-3)):
                    self.reason = "- Мейнстат (пески)"
                    print(self.reason)
                    return False

            # Кубок
            if self.artifact_list[0][4:] == names_list.types_of_artifact[3][4:]:
                if any(self.artifact_list[i].startswith(substring) for substring in self.goblet_main_stat_selected for i
                       in range(1, len(self.artifact_list)-3)):
                    self.reason = "+ Мейнстат (кубок)"
                    print(self.reason)
                    return True  # оставить артефакт

                # Блэклист кубок
                if any(self.artifact_list[i].startswith(substring) for substring in self.goblet_black for i in
                       range(1, len(self.artifact_list)-3)):
                    self.reason = "- Мейнстат (кубок)"
                    print(self.reason)
                    return False

            # Корона
            if self.artifact_list[0][4:] == names_list.types_of_artifact[4][4:]:
                if any(self.artifact_list[i].startswith(substring) for substring in self.circlet_main_stat_selected for
                       i in
                       range(1, len(self.artifact_list)-3)):
                    self.reason = "+ Мейнстат (корона)"
                    print(self.reason)
                    return True  # оставить артефакт

                # Блэклист корона
                if any(self.artifact_list[i].startswith(substring) for substring in self.circlet_black for i in
                       range(1, len(self.artifact_list)-3)):
                    self.reason = "- Мейнстат (корона)"
                    print(self.reason)
                    return False

            # Сабстаты
            if self.substats_selected:
                if any(self.artifact_list[i].startswith(substring) for substring in self.substats_selected for i in
                       range(1, len(self.artifact_list))):
                    self.reason = "+ Сабстат"
                    print(self.reason)
                    return True  # оставить артефакт

            # Криты
            if any(self.artifact_list[i].startswith(substring) for substring in ['Крит', 'Шанс'] for i in
                   range(1, len(self.artifact_list))):
                self.reason = "+ Криты"
                print(self.reason)
                return True  # оставить артефакт

            return False  # иначе не оставлять артефакт


if __name__ == "__main__":  # для тестовых запусков

    screen_ratio = "16:10"
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
