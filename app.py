import json
import logging
import os
import sys
from datetime import datetime

import customtkinter
from PIL import Image

import mouse_move
import names_list
import utils
from utils import check_dir_exists, config_info, path_and_dir, resource_path

# from opens import activate_window

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

logs_dir = 'logs'
if not os.path.exists(f"{logs_dir}/"):
    os.makedirs(logs_dir)

logging.basicConfig(level=logging.INFO,
                    filename="logs\\art_parser.log",
                    filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

logging.info("Starting...")
logging.info(f"Current OS: {sys.platform}.")

try:
    class App(customtkinter.CTk):
        def __init__(self):
            super().__init__()

            '''paths required for the application to work'''
            self.paths = path_and_dir()
            self.presets_dir = 'presets'
            self.exe_dir = self.paths[0]
            self.config_path = self.paths[1]
            self.default_path = self.paths[2]
            self.nothing_path = self.paths[3]

            '''creates a directory and the necessary files if they don`t exist'''
            check_dir_exists(self.exe_dir, self.config_path, self.default_path, self.nothing_path)

            self.config = config_info(self.config_path)
            self.presets = self.config['presets']
            # self.auto_open = self.config["auto_open_genshin"]
            # self.languge = self.config['language']
            self.theme = self.config['app_theme']
            logging.info(f"Presets list: {self.presets}")

            if self.theme in ['dark', 'light', 'system']:
                customtkinter.set_appearance_mode(self.theme)

            # configure window
            self.title("Artifacts Parser")
            self.geometry(f"{1100}x{580}")
            customtkinter.set_widget_scaling(1)
            self.maxsize(1100, 580)
            self.minsize(1030, 450)
            self.iconbitmap(resource_path("parser.ico"))

            # configure grid layout (4x4)
            self.grid_columnconfigure(1, weight=1)
            self.grid_columnconfigure((2, 3), weight=0)
            self.grid_rowconfigure((0, 1, 2), weight=1)

            # create sidebar frame with widgets
            self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
            self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
            self.sidebar_frame.grid_rowconfigure(4, weight=1)
            # self.sidebar_frame.grid_columnconfigure(2, weight=1)
            self.logo_image = customtkinter.CTkImage(light_image=Image.open(resource_path("Art_img.png")),
                                                     size=(70, 70))
            self.logo_image_label = customtkinter.CTkLabel(self.sidebar_frame, image=self.logo_image, text="")
            self.logo_image_label.grid(row=0, column=0, padx=20, pady=(50, 0))
            self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Artifacts Parser",
                                                     font=customtkinter.CTkFont(size=20, weight="bold"))
            self.logo_label.grid(row=1, column=0, padx=20, pady=(0, 10))
            # self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
            # self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)

            self.preset_select_label = customtkinter.CTkLabel(self.sidebar_frame, text="Выбор пресета:", anchor="w")
            self.preset_select_label.grid(row=6, column=0, padx=0, pady=(10, 0))
            self.preset_select_var = customtkinter.StringVar(value="default")
            self.preset_select = customtkinter.CTkComboBox(self.sidebar_frame,
                                                           values=self.presets,
                                                           variable=self.preset_select_var,
                                                           command=self.change_preset_event)
            self.preset_select.grid(row=7, column=0, padx=0, pady=(10, 10))

            self.save_button = customtkinter.CTkButton(self.sidebar_frame,
                                                       width=5,
                                                       text="Сохранить",
                                                       font=("font1", 12),
                                                       command=lambda: self.save_preset_event())
            self.save_button.grid(row=8, column=0, padx=(25, 5), pady=(10, 20), sticky="w")

            self.delete_icon_image = customtkinter.CTkImage(Image.open(resource_path('bin.png')),
                                                            size=(20, 20))
            self.delete_button = customtkinter.CTkButton(self.sidebar_frame,
                                                         width=5,
                                                         text="",
                                                         border_width=2,
                                                         image=self.delete_icon_image,
                                                         font=("font1", 12),
                                                         fg_color="transparent",
                                                         command=lambda: self.delete_preset_event())
            self.delete_button.grid(row=8, column=0, padx=(5, 25), pady=(10, 20), sticky="e")

            # self.screen_ratio_label = customtkinter.CTkLabel(self.sidebar_frame, text="Соотношение сторон экрана:",
            #                                                  anchor="w")
            # self.screen_ratio_label.grid(row=5, column=0, padx=20, pady=(10, 0))
            #
            # self.screen_ratio_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
            #                                                             values=["16:9", "16:10"],
            #                                                             command=self.change_screen_ratio_event,
            #                                                             fg_color="gray",
            #                                                             button_color="#4a4949",
            #                                                             button_hover_color="#3b3a3a")
            # self.screen_ratio_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

            # self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Выбор темы:", anchor="w")
            # self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
            # self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
            #                                                                values=["Light", "Dark", "System"],
            #                                                                command=self.change_appearance_mode_event,
            #                                                                fg_color="gray",
            #                                                                button_color="#4a4949",
            #                                                                button_hover_color="#3b3a3a")
            # self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

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
            self.tabview.tab("Пески").grid_columnconfigure(0, weight=1)
            self.tabview.tab("Кубки").grid_columnconfigure(0, weight=1)
            self.tabview.tab("Короны").grid_columnconfigure(0, weight=1)

            self.tab_1_text = customtkinter.CTkTextbox(self.tabview.tab("Пески"), height=20,
                                                       activate_scrollbars=False)
            self.tab_1_text.insert("0.0", "Выберите нужные мейнстаты")
            self.tab_1_text.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="nsew")

            self.tab_1_scrollable_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("Пески"))
            self.tab_1_scrollable_frame.grid(row=1, column=0, padx=0, pady=(0, 50), sticky="nsew")

            self.tab_1_checkboxes = []
            self.tab_1_checkbox_values = []
            self.tab_1_selected = []

            for i in range(len(names_list.sands_main_stat)):
                var = customtkinter.StringVar(value="99")
                self.tab_1_checkbox_values.append(var)
                check = customtkinter.CTkCheckBox(self.tab_1_scrollable_frame,
                                                  text=f"{names_list.sands_main_stat[i]}",
                                                  variable=var,
                                                  onvalue=i,
                                                  offvalue="99",
                                                  command=lambda i=i: self.tab_1_checkbox_changed(i))
                check.grid(row=i, column=0, padx=4, pady=(0, 15), sticky="nsew")
                self.tab_1_checkboxes.append(check)

            self.tab_2_text = customtkinter.CTkTextbox(self.tabview.tab("Кубки"), height=20,
                                                       activate_scrollbars=False)
            self.tab_2_text.insert("0.0", "Выберите нужные мейнстаты")
            self.tab_2_text.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="nsew")

            self.tab_2_scrollable_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("Кубки"), height=100)
            self.tab_2_scrollable_frame.grid(row=1, column=0, padx=0, pady=(0, 50), sticky="nsew")

            self.tab_2_checkboxes = []
            self.tab_2_checkbox_values = []
            self.tab_2_selected = []

            for i in range(len(names_list.goblet_main_stat)):
                var = customtkinter.StringVar(value="99")
                self.tab_2_checkbox_values.append(var)
                check = customtkinter.CTkCheckBox(master=self.tab_2_scrollable_frame,
                                                  text=f"{names_list.goblet_main_stat[i]}",
                                                  variable=var,
                                                  onvalue=i,
                                                  offvalue="99",
                                                  command=lambda i=i: self.tab_2_checkbox_changed(i))
                check.grid(row=i, column=0, padx=4, pady=(0, 15), sticky="nsew")
                self.tab_2_checkboxes.append(check)

            self.tab_3_text = customtkinter.CTkTextbox(self.tabview.tab("Короны"), height=20,
                                                       activate_scrollbars=False)
            self.tab_3_text.insert("0.0", "Выберите нужные мейнстаты")
            self.tab_3_text.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="nsew")

            self.tab_3_scrollable_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("Короны"), height=100)
            self.tab_3_scrollable_frame.grid(row=1, column=0, padx=0, pady=(0, 50), sticky="nsew")

            self.tab_3_checkboxes = []
            self.tab_3_checkbox_values = []
            self.tab_3_selected = []

            for i in range(len(names_list.circlet_main_stat)):
                var = customtkinter.StringVar(value="99")
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

            self.sets_text = customtkinter.CTkTextbox(self.sets_scrollable_frame, height=50,
                                                      activate_scrollbars=False)
            self.sets_text.insert("0.0", "Выберите нужные сеты, которые останутся в инвентаре")
            self.sets_text.grid(row=0, column=0, padx=10, pady=(0, 15), sticky="nsew")

            self.sets_scrollable_frame_checkboxes = []
            self.sets_scrollable_frame_checkbox_values = []
            self.sets_selected = []

            for i in range(len(names_list.sets)):
                var = customtkinter.StringVar(value="99")
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
            self.substat_checkbox_values = []
            self.substats_selected = []

            for i in range(len(names_list.sub_stats)):
                var = customtkinter.StringVar(value="99")
                self.substat_checkbox_values.append(var)
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
            self.tabview2.tab("Пески").grid_columnconfigure(0, weight=1)
            self.tabview2.tab("Кубки").grid_columnconfigure(0, weight=1)
            self.tabview2.tab("Короны").grid_columnconfigure(0, weight=1)

            self.tab_1_text2 = customtkinter.CTkTextbox(self.tabview2.tab("Пески"), height=20,
                                                        activate_scrollbars=False)
            self.tab_1_text2.insert("0.0", "Выберите ненужные мейнстаты")
            self.tab_1_text2.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="nsew")

            self.tab_1_scrollable_frame2 = customtkinter.CTkScrollableFrame(self.tabview2.tab("Пески"))
            self.tab_1_scrollable_frame2.grid(row=1, column=0, padx=0, pady=(0, 50), sticky="nsew")

            self.tab_1_checkboxes2 = []
            self.tab_1_checkbox_values2 = []
            self.tab_1_selected2 = []

            for i in range(len(names_list.sands_main_stat)):
                var = customtkinter.StringVar(value="99")
                self.tab_1_checkbox_values2.append(var)
                check = customtkinter.CTkCheckBox(self.tab_1_scrollable_frame2,
                                                  text=f"{names_list.sands_main_stat[i]}",
                                                  variable=var,
                                                  onvalue=i,
                                                  offvalue="99",
                                                  command=lambda i=i: self.tab_1_checkbox_changed2(i))
                check.grid(row=i, column=0, padx=4, pady=(0, 15), sticky="nsew")
                self.tab_1_checkboxes2.append(check)

            self.tab_2_text2 = customtkinter.CTkTextbox(self.tabview2.tab("Кубки"), height=20,
                                                        activate_scrollbars=False)
            self.tab_2_text2.insert("0.0", "Выберите ненужные мейнстаты")
            self.tab_2_text2.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="nsew")

            self.tab_2_scrollable_frame2 = customtkinter.CTkScrollableFrame(self.tabview2.tab("Кубки"), height=100)
            self.tab_2_scrollable_frame2.grid(row=1, column=0, padx=0, pady=(0, 50), sticky="nsew")

            self.tab_2_checkboxes2 = []
            self.tab_2_checkbox_values2 = []
            self.tab_2_selected2 = []

            for i in range(len(names_list.goblet_main_stat)):
                var = customtkinter.StringVar(value="99")
                self.tab_2_checkbox_values2.append(var)
                check = customtkinter.CTkCheckBox(master=self.tab_2_scrollable_frame2,
                                                  text=f"{names_list.goblet_main_stat[i]}",
                                                  variable=var,
                                                  onvalue=i,
                                                  offvalue="99",
                                                  command=lambda i=i: self.tab_2_checkbox_changed2(i))
                check.grid(row=i, column=0, padx=4, pady=(0, 15), sticky="nsew")
                self.tab_2_checkboxes2.append(check)

            self.tab_3_text2 = customtkinter.CTkTextbox(self.tabview2.tab("Короны"), height=20,
                                                        activate_scrollbars=False)
            self.tab_3_text2.insert("0.0", "Выберите ненужные мейнстаты")
            self.tab_3_text2.grid(row=0, column=0, padx=10, pady=(0, 10), sticky="nsew")

            self.tab_3_scrollable_frame2 = customtkinter.CTkScrollableFrame(self.tabview2.tab("Короны"), height=100)
            self.tab_3_scrollable_frame2.grid(row=1, column=0, padx=0, pady=(0, 50), sticky="nsew")

            self.tab_3_checkboxes2 = []
            self.tab_3_checkbox_values2 = []
            self.tab_3_selected2 = []

            for i in range(len(names_list.circlet_main_stat)):
                var = customtkinter.StringVar(value="99")
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
            # self.screen_ratio_optionemenu.set("16:9")
            # self.appearance_mode_optionemenu.set("Dark")

            self.on_app_start()

        def tab_1_checkbox_changed(self, index):
            value = int(self.tab_1_checkbox_values[index].get())
            if value == 99:
                self.tab_1_selected.remove(names_list.sands_main_stat[index])
            else:
                self.tab_1_selected.append(names_list.sands_main_stat[index])

        def tab_2_checkbox_changed(self, index):
            value = int(self.tab_2_checkbox_values[index].get())
            if value == 99:
                self.tab_2_selected.remove(names_list.goblet_main_stat[index])
            else:
                self.tab_2_selected.append(names_list.goblet_main_stat[index])

        def tab_3_checkbox_changed(self, index):
            value = int(self.tab_3_checkbox_values[index].get())
            if value == 99:
                self.tab_3_selected.remove(names_list.circlet_main_stat[index])
            else:
                self.tab_3_selected.append(names_list.circlet_main_stat[index])

        def tab_1_checkbox_changed2(self, index):
            value = int(self.tab_1_checkbox_values2[index].get())
            if value == 99:
                self.tab_1_selected2.remove(names_list.sands_main_stat[index])
            else:
                self.tab_1_selected2.append(names_list.sands_main_stat[index])

        def tab_2_checkbox_changed2(self, index):
            value = int(self.tab_2_checkbox_values2[index].get())
            if value == 99:
                self.tab_2_selected2.remove(names_list.goblet_main_stat[index])
            else:
                self.tab_2_selected2.append(names_list.goblet_main_stat[index])

        def tab_3_checkbox_changed2(self, index):
            value = int(self.tab_3_checkbox_values2[index].get())
            if value == 99:
                self.tab_3_selected2.remove(names_list.circlet_main_stat[index])
            else:
                self.tab_3_selected2.append(names_list.circlet_main_stat[index])

        def sets_checkbox_changed(self, index):
            value = int(self.sets_scrollable_frame_checkbox_values[index].get())
            if value == 99:
                self.sets_selected.remove(names_list.sets[index])
            else:
                self.sets_selected.append(names_list.sets[index])

        def substat_checkbox_changed(self, index):
            value = int(self.substat_checkbox_values[index].get())
            if value == 99:
                self.substats_selected.remove(names_list.sub_stats[index])
            else:
                self.substats_selected.append(names_list.sub_stats[index])

        # def change_screen_ratio_event(self, new_screen_ratio: str):
        #     print(new_screen_ratio)
        #
        # def change_appearance_mode_event(self, new_appearance_mode: str):
        #     customtkinter.set_appearance_mode(new_appearance_mode)

        def change_preset_event(self, preset: str):
            s = self.preset_select.get()
            logging.info(f"Preset '{s}' selected.")

            file_to_open = s
            data = None

            if s != "nothing":
                try:
                    with open(resource_path(f'{self.exe_dir}/{self.presets_dir}/{s}.json'), 'r') as json_file:
                        data = json.load(json_file)
                    logging.info(f"Preset '{file_to_open}' loaded.")
                except FileNotFoundError:
                    logging.error(f"FileNotFoundError ({file_to_open})", exc_info=True)
                except Exception as e:
                    logging.error(e, exc_info=True)

            if s == "nothing":
                self.deselect_all()
            else:
                if data:
                    self.deselect_all()
                    self.select_the_right_ones(data)

        def save_preset_event(self):

            data = {
                "sets": self.sets_selected,
                "sands": self.tab_1_selected,
                "goblet": self.tab_2_selected,
                "circlet": self.tab_3_selected,
                "sands_d": self.tab_1_selected2,
                "goblet_d": self.tab_2_selected2,
                "circlet_d": self.tab_3_selected2,
                "substats": self.substats_selected
            }

            s = self.preset_select.get()
            banned_symbols = ['/', ':', '*', '?', '"', '<', '>', '|', '+', " ", '\\']
            for char in s:
                if char in banned_symbols:
                    logging.error(f"Invalid character in the preset name: '{char}'")
                    break
            else:
                if s == "nothing":
                    pass
                else:
                    if s in self.presets:
                        for i in self.presets:
                            if i == s:
                                self.presets.remove(i)
                    self.presets.append(s)

                    with open(resource_path(f'{self.exe_dir}/{self.presets_dir}/{s}.json'), 'w') as json_file:
                        json.dump(data, json_file, ensure_ascii=False)

                    self.config['presets'] = self.presets
                    with open(resource_path(self.config_path), 'w') as json_file:
                        json.dump(self.config, json_file, ensure_ascii=False)

                    logging.info(f"Saved preset: {s}.")
                    self.preset_select.configure(values=self.presets)

        def delete_preset_event(self):
            d = self.preset_select.get()
            if d == "nothing" or d == "default":
                pass
            elif d in self.presets:
                self.presets.remove(d)

                self.config['presets'] = self.presets
                with open(self.config_path, 'w') as json_file:
                    json.dump(self.config, json_file, ensure_ascii=False)

                try:
                    os.remove(resource_path(f'{self.exe_dir}/{self.presets_dir}/{d}.json'))
                    logging.info(f"Preset '{d}' deleted.")
                except FileNotFoundError:
                    logging.error(f"FileNotFoundError ({d})", exc_info=True)
                except Exception as e:
                    logging.error(e, exc_info=True)

                logging.info(f"Preset {d} deleted.")
                self.preset_select.configure(values=self.presets)

        def deselect_all(self):
            for i in [self.sets_scrollable_frame_checkboxes,
                      self.tab_1_checkboxes, self.tab_2_checkboxes, self.tab_3_checkboxes,
                      self.tab_1_checkboxes2, self.tab_2_checkboxes2, self.tab_3_checkboxes2,
                      self.substats_scrollable_frame_checkboxes]:
                for j in i:
                    j.deselect()

            self.sets_selected = []
            self.substats_selected = []
            self.tab_1_selected = []
            self.tab_2_selected = []
            self.tab_3_selected = []
            self.tab_1_selected2 = []
            self.tab_2_selected2 = []
            self.tab_3_selected2 = []
            
        def select_the_right_ones(self, data):
            """
            Selects the appropriate checkboxes in the GUI based on the data provided.

            Args:
                data (dict): A dictionary containing the data to match and select checkboxes in the GUI.
            """
            def match_and_select_items(data, names_dict, checkboxes_list, selected_list):
                matching_items = {}
                for item in data:
                    for key, value in names_dict.items():
                        if value == item:
                            matching_items[value] = key
                for i in matching_items.values():
                    checkboxes_list[i - 1].select()
                for j in data:
                    selected_list.append(j)

            match_and_select_items(data["sets"], names_list.sets_dict, self.sets_scrollable_frame_checkboxes, self.sets_selected)
            match_and_select_items(data["sands"], names_list.sands_main_stat_dict, self.tab_1_checkboxes, self.tab_1_selected)
            match_and_select_items(data["goblet"], names_list.goblet_main_stat_dict, self.tab_2_checkboxes, self.tab_2_selected)
            match_and_select_items(data["circlet"], names_list.circlet_main_stat_dict, self.tab_3_checkboxes, self.tab_3_selected)
            match_and_select_items(data["sands_d"], names_list.sands_main_stat_dict, self.tab_1_checkboxes2, self.tab_1_selected2)
            match_and_select_items(data["goblet_d"], names_list.goblet_main_stat_dict, self.tab_2_checkboxes2, self.tab_2_selected2)
            match_and_select_items(data["circlet_d"], names_list.circlet_main_stat_dict, self.tab_3_checkboxes2, self.tab_3_selected2)
            match_and_select_items(data["substats"], names_list.sub_stats_dict, self.substats_scrollable_frame_checkboxes, self.substats_selected)

        def start_button_event(self):
            screen_ratio = "16:9"

            data = {
                "sets": self.sets_selected,
                "sands": self.tab_1_selected,
                "goblet": self.tab_2_selected,
                "circlet": self.tab_3_selected,
                "sands_d": self.tab_1_selected2,
                "goblet_d": self.tab_2_selected2,
                "circlet_d": self.tab_3_selected2,
                "substats": self.substats_selected
            }

            start_time = datetime.now()
            try:
                # if self.auto_open == 'True':
                #     activate_window()

                logging.info(f"Starting sort... Params: {data}")
                with open("logs\\summary.txt", 'a') as txt_file:
                    txt_file.write("=" * 30)
                    txt_file.write("\n")

                mouse_move.MoveClickCheck(screen_ratio,
                                          self.sets_selected, self.substats_selected,
                                          self.tab_1_selected, self.tab_2_selected, self.tab_3_selected,
                                          self.tab_1_selected2, self.tab_2_selected2, self.tab_3_selected2).start()
                logging.info(f"Время выполнения: {datetime.now() - start_time}")
                logging.info("Finish sort.")
            except utils.FailSafeException:
                logging.warning("Stopping... (FailSafe triggered from mouse moving to a corner of the screen.)")
            except Exception as e:
                logging.error(e, exc_info=True)

        def on_app_start(self):
            data = None

            try:
                with open(self.default_path, 'r') as json_file:
                    data = json.load(json_file)
                logging.info("Preset 'default' loaded.")
            except FileNotFoundError:
                logging.error("FileNotFoundError (default.json)", exc_info=True)
            except Exception as e:
                logging.error(e, exc_info=True)

            if data:
                self.select_the_right_ones(data)

except Exception as e:
    logging.error(e, exc_info=True)

if __name__ == "__main__":
    if sys.platform == "win32":
        app = App()
        app.mainloop()
    else:
        logging.error("OSIsNotSupportedError")
