import os
import tkinter
import tkinter.messagebox
import customtkinter
from datetime import datetime
from PIL import Image, ImageTk

import names_list
import mouse_move

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Artifacts Parser")
        self.geometry(f"{1100}x{580}")
        customtkinter.set_widget_scaling(1)

        self.iconphoto(False, tkinter.PhotoImage(file=resource_path("Art_img.png")))

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_image = customtkinter.CTkImage(light_image=Image.open(resource_path("Art_img.png")), size=(70, 70))
        self.logo_image_label = customtkinter.CTkLabel(self.sidebar_frame, image=self.logo_image, text="")
        self.logo_image_label.grid(row=0, column=0, padx=20, pady=(50, 0))
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Artifacts Parser",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=1, column=0, padx=20, pady=(0, 10))
        # self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        # self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)

        self.screen_ratio_label = customtkinter.CTkLabel(self.sidebar_frame, text="Соотношение сторон экрана:",
                                                         anchor="w")
        self.screen_ratio_label.grid(row=5, column=0, padx=20, pady=(10, 0))

        self.screen_ratio_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                    values=["16:9", "16:10"],
                                                                    command=self.change_screen_ratio_event,
                                                                    fg_color="gray",
                                                                    button_color="#4a4949",
                                                                    button_hover_color="#3b3a3a")
        self.screen_ratio_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Выбор темы:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event,
                                                                       fg_color="gray",
                                                                       button_color="#4a4949",
                                                                       button_hover_color="#3b3a3a")
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        self.main_button_1 = customtkinter.CTkButton(master=self,
                                                     fg_color="transparent",
                                                     border_width=2,
                                                     text_color=("gray10", "#DCE4EE"),
                                                     text="Старт",
                                                     command=self.start_button_event)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(0, 20), pady=0, sticky="nsew")
        self.tabview.add("Пески")
        self.tabview.add("Кубки")
        self.tabview.add("Короны")
        self.tabview.tab("Пески").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Кубки").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Короны").grid_columnconfigure(0, weight=1)

        self.tab_1_text = customtkinter.CTkTextbox(self.tabview.tab("Пески"), height=20, activate_scrollbars=False)
        self.tab_1_text.insert("0.0", "Выберите нужные мейнстаты")
        self.tab_1_text.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.tab_1_scrollable_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("Пески"))
        self.tab_1_scrollable_frame.grid(row=1, column=0, padx=0, pady=(0, 50), sticky="nsew")

        self.tab_1_checkboxes = []
        self.tab_1_checkbox_values = []  # Список для хранения значений чекбоксов
        self.tab_1_selected = []

        for i in range(len(names_list.sands_main_stat)):
            var = customtkinter.StringVar(value="99")  # Создаем переменную для хранения значения чекбокса
            self.tab_1_checkbox_values.append(var)
            check = customtkinter.CTkCheckBox(self.tab_1_scrollable_frame,
                                              text=f"{names_list.sands_main_stat[i]}",
                                              variable=var,
                                              onvalue=i,
                                              offvalue="99",
                                              command=lambda i=i: self.tab_1_checkbox_changed(i))
            check.grid(row=i, column=0, padx=4, pady=(0, 15), sticky="nsew")
            self.tab_1_checkboxes.append(check)

        self.tab_2_text = customtkinter.CTkTextbox(self.tabview.tab("Кубки"), height=20, activate_scrollbars=False)
        self.tab_2_text.insert("0.0", "Выберите нужные мейнстаты")
        self.tab_2_text.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.tab_2_scrollable_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("Кубки"), height=100)
        self.tab_2_scrollable_frame.grid(row=1, column=0, padx=0, pady=(0, 50), sticky="nsew")

        self.tab_2_checkboxes = []
        self.tab_2_checkbox_values = []  # Список для хранения значений чекбоксов
        self.tab_2_selected = []

        for i in range(len(names_list.goblet_main_stat)):
            var = customtkinter.StringVar(value="99")  # Создаем переменную для хранения значения чекбокса
            self.tab_2_checkbox_values.append(var)
            check = customtkinter.CTkCheckBox(master=self.tab_2_scrollable_frame,
                                              text=f"{names_list.goblet_main_stat[i]}",
                                              variable=var,
                                              onvalue=i,
                                              offvalue="99",
                                              command=lambda i=i: self.tab_2_checkbox_changed(i))
            check.grid(row=i, column=0, padx=4, pady=(0, 15), sticky="nsew")
            self.tab_2_checkboxes.append(check)

        self.tab_3_text = customtkinter.CTkTextbox(self.tabview.tab("Короны"), height=20, activate_scrollbars=False)
        self.tab_3_text.insert("0.0", "Выберите нужные мейнстаты")
        self.tab_3_text.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.tab_3_scrollable_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("Короны"), height=100)
        self.tab_3_scrollable_frame.grid(row=1, column=0, padx=0, pady=(0, 50), sticky="nsew")

        self.tab_3_checkboxes = []
        self.tab_3_checkbox_values = []  # Список для хранения значений чекбоксов
        self.tab_3_selected = []

        for i in range(len(names_list.circlet_main_stat)):
            var = customtkinter.StringVar(value="99")  # Создаем переменную для хранения значения чекбокса
            self.tab_3_checkbox_values.append(var)
            check = customtkinter.CTkCheckBox(self.tab_3_scrollable_frame,
                                              text=f"{names_list.circlet_main_stat[i]}",
                                              variable=var,
                                              onvalue=i,
                                              offvalue="99",
                                              command=lambda i=i: self.tab_3_checkbox_changed(i))
            check.grid(row=i, column=0, padx=4, pady=(0, 15), sticky="nsew")
            self.tab_3_checkboxes.append(check)

        self.sets_scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Сеты")
        self.sets_scrollable_frame.grid(row=0, column=1, rowspan=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.sets_scrollable_frame.grid_columnconfigure(2, weight=1)

        self.sets_text = customtkinter.CTkTextbox(self.sets_scrollable_frame, height=50, activate_scrollbars=False)
        self.sets_text.insert("0.0", "Выберите нужные сеты, которые останутся в инвентаре")
        self.sets_text.grid(row=0, column=0, padx=10, pady=(0, 15), sticky="nsew")

        self.sets_scrollable_frame_checkboxes = []
        self.sets_scrollable_frame_checkbox_values = []  # Список для хранения значений чекбоксов
        self.sets_selected = []

        for i in range(len(names_list.sets)):
            var = customtkinter.StringVar(value="99")  # Создаем переменную для хранения значения чекбокса
            self.sets_scrollable_frame_checkbox_values.append(var)
            check = customtkinter.CTkCheckBox(master=self.sets_scrollable_frame,
                                              text=f"{names_list.sets[i]}",
                                              variable=var,
                                              onvalue=i,
                                              offvalue="99",
                                              command=lambda i=i: self.sets_checkbox_changed(i))
            check.grid(row=i + 1, column=0, padx=10, pady=(0, 15), sticky="nsew")
            self.sets_scrollable_frame_checkboxes.append(check)

        self.substats_scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Сабстаты")
        self.substats_scrollable_frame.grid(row=1, column=2, padx=(0, 20), pady=(20, 0), sticky="nsew")

        self.substats_text = customtkinter.CTkTextbox(self.substats_scrollable_frame, height=20,
                                                      activate_scrollbars=False)
        self.substats_text.insert("0.0", "Выберите нужные сабстаты")
        self.substats_text.grid(row=0, column=0, padx=(10, 0), pady=(0, 15), sticky="nsew")

        self.substats_scrollable_frame_checkboxes = []
        self.substat_checkbox_values = []  # Список для хранения значений чекбоксов
        self.substats_selected = []

        for i in range(len(names_list.sub_stats)):
            var = customtkinter.StringVar(value="99")  # Создаем переменную для хранения значения чекбокса
            self.substat_checkbox_values.append(var)  # Добавляем переменную в список
            check = customtkinter.CTkCheckBox(master=self.substats_scrollable_frame,
                                              text=f"{names_list.sub_stats[i]}",
                                              variable=var,
                                              onvalue=i,
                                              offvalue="99",
                                              command=lambda i=i: self.substat_checkbox_changed(i))
            check.grid(row=i + 1, column=0, padx=10, pady=(0, 15), sticky="nsew")
            self.substats_scrollable_frame_checkboxes.append(check)

        self.tabview2 = customtkinter.CTkTabview(self, width=250)
        self.tabview2.grid(row=0, column=3, padx=(0, 20), pady=(0, 0), sticky="nsew")
        self.tabview2.add("Пески")
        self.tabview2.add("Кубки")
        self.tabview2.add("Короны")
        self.tabview2.tab("Пески").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview2.tab("Кубки").grid_columnconfigure(0, weight=1)
        self.tabview2.tab("Короны").grid_columnconfigure(0, weight=1)

        self.tab_1_text2 = customtkinter.CTkTextbox(self.tabview2.tab("Пески"), height=20, activate_scrollbars=False)
        self.tab_1_text2.insert("0.0", "Выберите ненужные мейнстаты")
        self.tab_1_text2.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.tab_1_scrollable_frame2 = customtkinter.CTkScrollableFrame(self.tabview2.tab("Пески"))
        self.tab_1_scrollable_frame2.grid(row=1, column=0, padx=0, pady=(0, 50), sticky="nsew")

        self.tab_1_checkboxes2 = []
        self.tab_1_checkbox_values2 = []  # Список для хранения значений чекбоксов
        self.tab_1_selected2 = []

        for i in range(len(names_list.sands_main_stat)):
            var = customtkinter.StringVar(value="99")  # Создаем переменную для хранения значения чекбокса
            self.tab_1_checkbox_values2.append(var)
            check = customtkinter.CTkCheckBox(self.tab_1_scrollable_frame2,
                                              text=f"{names_list.sands_main_stat[i]}",
                                              variable=var,
                                              onvalue=i,
                                              offvalue="99",
                                              command=lambda i=i: self.tab_1_checkbox_changed2(i))
            check.grid(row=i, column=0, padx=4, pady=(0, 15), sticky="nsew")
            self.tab_1_checkboxes2.append(check)

        self.tab_2_text2 = customtkinter.CTkTextbox(self.tabview2.tab("Кубки"), height=20, activate_scrollbars=False)
        self.tab_2_text2.insert("0.0", "Выберите ненужные мейнстаты")
        self.tab_2_text2.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.tab_2_scrollable_frame2 = customtkinter.CTkScrollableFrame(self.tabview2.tab("Кубки"), height=100)
        self.tab_2_scrollable_frame2.grid(row=1, column=0, padx=0, pady=(0, 50), sticky="nsew")

        self.tab_2_checkboxes2 = []
        self.tab_2_checkbox_values2 = []  # Список для хранения значений чекбоксов
        self.tab_2_selected2 = []

        for i in range(len(names_list.goblet_main_stat)):
            var = customtkinter.StringVar(value="99")  # Создаем переменную для хранения значения чекбокса
            self.tab_2_checkbox_values2.append(var)
            check = customtkinter.CTkCheckBox(master=self.tab_2_scrollable_frame2,
                                              text=f"{names_list.goblet_main_stat[i]}",
                                              variable=var,
                                              onvalue=i,
                                              offvalue="99",
                                              command=lambda i=i: self.tab_2_checkbox_changed2(i))
            check.grid(row=i, column=0, padx=4, pady=(0, 15), sticky="nsew")
            self.tab_2_checkboxes2.append(check)

        self.tab_3_text2 = customtkinter.CTkTextbox(self.tabview2.tab("Короны"), height=20, activate_scrollbars=False)
        self.tab_3_text2.insert("0.0", "Выберите ненужные мейнстаты")
        self.tab_3_text2.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.tab_3_scrollable_frame2 = customtkinter.CTkScrollableFrame(self.tabview2.tab("Короны"), height=100)
        self.tab_3_scrollable_frame2.grid(row=1, column=0, padx=0, pady=(0, 50), sticky="nsew")

        self.tab_3_checkboxes2 = []
        self.tab_3_checkbox_values2 = []  # Список для хранения значений чекбоксов
        self.tab_3_selected2 = []

        for i in range(len(names_list.circlet_main_stat)):
            var = customtkinter.StringVar(value="99")  # Создаем переменную для хранения значения чекбокса
            self.tab_3_checkbox_values2.append(var)
            check = customtkinter.CTkCheckBox(self.tab_3_scrollable_frame2,
                                              text=f"{names_list.circlet_main_stat[i]}",
                                              variable=var,
                                              onvalue=i,
                                              offvalue="99",
                                              command=lambda i=i: self.tab_3_checkbox_changed2(i))
            check.grid(row=i, column=0, padx=4, pady=(0, 15), sticky="nsew")
            self.tab_3_checkboxes2.append(check)

        self.text_box = customtkinter.CTkTextbox(master=self, activate_scrollbars=False)
        self.text_box.grid(row=1, column=3, padx=(0, 20), pady=(20, 0), sticky="nsew")
        self.text_box.insert("0.0", "Если что-то пошло не так: "
                                    "\n1. Отведите курсор в левый "
                                    "\n    верхний угол "
                                    "\n2. Если первое не помогло, "
                                    "\n    то закройте программу любым "
                                    "\n    знакомым Вам методом")

        self.sets_text.configure(state="disabled")
        self.tab_1_text.configure(state="disabled")
        self.tab_2_text.configure(state="disabled")
        self.tab_3_text.configure(state="disabled")
        self.substats_text.configure(state="disabled")
        self.tab_1_text2.configure(state="disabled", font=("font1", 12))
        self.tab_2_text2.configure(state="disabled", font=("font1", 12))
        self.tab_3_text2.configure(state="disabled", font=("font1", 12))
        self.text_box.configure(state="disabled", autoseparators=True)
        self.screen_ratio_optionemenu.set("16:9")
        self.appearance_mode_optionemenu.set("Dark")

    def tab_1_checkbox_changed(self, index):
        if int(self.tab_1_checkbox_values[index].get()) == 99:
            self.tab_1_selected.remove(names_list.sands_main_stat[index])
        else:
            self.tab_1_selected.append(names_list.sands_main_stat[index])
        # print(self.tab_1_selected)

    def tab_2_checkbox_changed(self, index):
        if int(self.tab_2_checkbox_values[index].get()) == 99:
            self.tab_2_selected.remove(names_list.goblet_main_stat[index])
        else:
            self.tab_2_selected.append(names_list.goblet_main_stat[index])
        # print(self.tab_2_selected)

    def tab_3_checkbox_changed(self, index):
        if int(self.tab_3_checkbox_values[index].get()) == 99:
            self.tab_3_selected.remove(names_list.circlet_main_stat[index])
        else:
            self.tab_3_selected.append(names_list.circlet_main_stat[index])
        # print(self.tab_3_selected)

    def tab_1_checkbox_changed2(self, index):
        if int(self.tab_1_checkbox_values2[index].get()) == 99:
            self.tab_1_selected2.remove(names_list.sands_main_stat[index])
        else:
            self.tab_1_selected2.append(names_list.sands_main_stat[index])
        # print(self.tab_1_selected)

    def tab_2_checkbox_changed2(self, index):
        if int(self.tab_2_checkbox_values2[index].get()) == 99:
            self.tab_2_selected2.remove(names_list.goblet_main_stat[index])
        else:
            self.tab_2_selected2.append(names_list.goblet_main_stat[index])
        # print(self.tab_2_selected)

    def tab_3_checkbox_changed2(self, index):
        if int(self.tab_3_checkbox_values2[index].get()) == 99:
            self.tab_3_selected2.remove(names_list.circlet_main_stat[index])
        else:
            self.tab_3_selected2.append(names_list.circlet_main_stat[index])
        # print(self.tab_3_selected)

    def sets_checkbox_changed(self, index):
        if int(self.sets_scrollable_frame_checkbox_values[index].get()) == 99:
            self.sets_selected.remove(names_list.sets[index])
        else:
            self.sets_selected.append(names_list.sets[index])
        # print(self.sets_selected)

    def substat_checkbox_changed(self, index):
        # Функция будет вызываться при изменении состояния чекбокса
        if int(self.substat_checkbox_values[index].get()) == 99:
            # print(f"Чекбокс {index} изменился.")
            # print(f"- {self.checkbox_values[index].get()} | {names_list.sub_stats[index]}")
            self.substats_selected.remove(names_list.sub_stats[index])
        else:
            # print(f"Чекбокс {index} изменился.")
            # print(f"+ {self.checkbox_values[index].get()} | {names_list.sub_stats[index]}")
            self.substats_selected.append(names_list.sub_stats[index])
        # print(self.substats_selected)

    def change_screen_ratio_event(self, new_screen_ratio: str):
        print(new_screen_ratio)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def start_button_event(self):
        print("> start")
        print(" -" * 15)
        print(f"| + Сеты: {self.sets_selected}")
        print(f"| + Сабстаты: {self.substats_selected}")
        print(f"| + Пески: {self.tab_1_selected}")
        print(f"| + Кубки: {self.tab_2_selected}")
        print(f"| + Короны: {self.tab_3_selected}")
        print(" -" * 15)
        print(f"| - Пески: {self.tab_1_selected2}")
        print(f"| - Кубки: {self.tab_2_selected2}")
        print(f"| - Короны: {self.tab_3_selected2}")
        print(" -" * 15)
        print(f"| Соотношение сторон экрана: {self.screen_ratio_optionemenu.get()}")
        startTime = datetime.now()
        mouse_move.MoveClickCheck(self.screen_ratio_optionemenu.get(), self.sets_selected, self.substats_selected,
                                  self.tab_1_selected, self.tab_2_selected, self.tab_3_selected, self.tab_1_selected2,
                                  self.tab_2_selected2, self.tab_3_selected2).start()
        print(f"Время выполнения: {datetime.now() - startTime}")
        print("> finish")


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    app = App()
    app.mainloop()
