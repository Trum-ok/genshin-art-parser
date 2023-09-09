import os
import sys
import json
import tkinter
import logging
import customtkinter
import tkinter.messagebox
from datetime import datetime

from PIL import Image

import names_list
import mouse_move
import utils
from utils import resource_path
from opens import activate_window

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

log_dir = 'logs'
if not os.path.exists(f"{log_dir}/"):
    # logging.warning(f"'{self.log_dir}' directory is missing")
    os.makedirs(log_dir)
    # logging.info(f"dir created: '{self.log_dir}'")

logging.basicConfig(level=logging.INFO,
                    filename="logs\\art_parser.log",
                    filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

logging.info("Starting...")
logging.info(f"Current OS: {sys.platform}.")

try:
    if sys.platform != "win32":
        logging.error("OSIsNotSupportedError")


        class App(customtkinter.CTk):
            def __init__(self):
                super(App, self).__init__()

                self.title("Error")
                self.geometry(f"{200}x{50}")
                self.label = customtkinter.CTkLabel(self, text="Your OS isn`t supported")
                self.label.grid(row=0, column=0, padx=20, pady=10)
    else:

        class App(customtkinter.CTk):
            def __init__(self):
                super().__init__()

                self.pr_dir = 'presets'
                self.exe_dir = os.path.dirname(sys.executable)
                # self.exe_dir = 'C:\\Users\\TrumW\\PycharmProjects\\art-parser'
                config_path = resource_path(f'{self.exe_dir}\\{self.pr_dir}\\config.json')
                default_path = resource_path(f'{self.exe_dir}\\{self.pr_dir}\\default.json')
                nothing_path = resource_path(f'{self.exe_dir}\\{self.pr_dir}\\nothing.json')

                if not os.path.exists(f"{self.pr_dir}/"):
                    logging.warning(f"'{self.pr_dir}' directory is missing")
                    os.makedirs(self.pr_dir)
                    logging.info(f"dir created: '{self.pr_dir}'")
                    with open(resource_path(config_path), 'w') as json_file:
                        json.dump(["nothing", "default"], json_file, ensure_ascii=False)
                    with open(resource_path(default_path), 'w') as json_file:
                        json.dump(
                            {"sets": [], "sands": [], "goblet": [], "circlet": ["Шанс крит. попадания", "Крит. урон"],
                             "sands_d": [], "goblet_d": [], "circlet_d": [],
                             "substats": ["Шанс крит. попадания", "Крит. урон"]}, json_file, ensure_ascii=False)
                    with open(resource_path(nothing_path), 'w') as json_file:
                        json.dump({"sets": [], "sands": [], "goblet": [], "circlet": [], "sands_d": [], "goblet_d": [],
                                   "circlet_d": [], "substats": []}, json_file, ensure_ascii=False)
                    logging.info("Files 'config.json', 'default.json', 'nothing.json' created")

                with open(config_path, 'r') as json_file:
                    self.presets = json.load(json_file)
                logging.info(f"Presets list: {self.presets}")

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
                if int(self.tab_1_checkbox_values[index].get()) == 99:
                    self.tab_1_selected.remove(names_list.sands_main_stat[index])
                else:
                    self.tab_1_selected.append(names_list.sands_main_stat[index])

            def tab_2_checkbox_changed(self, index):
                if int(self.tab_2_checkbox_values[index].get()) == 99:
                    self.tab_2_selected.remove(names_list.goblet_main_stat[index])
                else:
                    self.tab_2_selected.append(names_list.goblet_main_stat[index])

            def tab_3_checkbox_changed(self, index):
                if int(self.tab_3_checkbox_values[index].get()) == 99:
                    self.tab_3_selected.remove(names_list.circlet_main_stat[index])
                else:
                    self.tab_3_selected.append(names_list.circlet_main_stat[index])

            def tab_1_checkbox_changed2(self, index):
                if int(self.tab_1_checkbox_values2[index].get()) == 99:
                    self.tab_1_selected2.remove(names_list.sands_main_stat[index])
                else:
                    self.tab_1_selected2.append(names_list.sands_main_stat[index])

            def tab_2_checkbox_changed2(self, index):
                if int(self.tab_2_checkbox_values2[index].get()) == 99:
                    self.tab_2_selected2.remove(names_list.goblet_main_stat[index])
                else:
                    self.tab_2_selected2.append(names_list.goblet_main_stat[index])

            def tab_3_checkbox_changed2(self, index):
                if int(self.tab_3_checkbox_values2[index].get()) == 99:
                    self.tab_3_selected2.remove(names_list.circlet_main_stat[index])
                else:
                    self.tab_3_selected2.append(names_list.circlet_main_stat[index])

            def sets_checkbox_changed(self, index):
                if int(self.sets_scrollable_frame_checkbox_values[index].get()) == 99:
                    self.sets_selected.remove(names_list.sets[index])
                else:
                    self.sets_selected.append(names_list.sets[index])

            def substat_checkbox_changed(self, index):
                if int(self.substat_checkbox_values[index].get()) == 99:
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
                        with open(resource_path(f'{self.exe_dir}/{self.pr_dir}/{s}.json'), 'r') as json_file:
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
                if s == "nothing":
                    pass
                else:
                    if s in self.presets:
                        for i in self.presets:
                            if i == s:
                                self.presets.remove(i)
                                # self.presets.append(s)
                                #
                                # with open(resource_path(f'{self.exe_dir}/{self.pr_dir}/{s}.json'), 'w') as json_file:
                                #     json.dump(data, json_file, ensure_ascii=False)
                                # with open(resource_path(f'{self.exe_dir}/{self.pr_dir}/config.json'), 'w') as json_file:
                                #     json.dump(self.presets, json_file, ensure_ascii=False)

                    self.presets.append(s)

                    with open(resource_path(f'{self.exe_dir}/{self.pr_dir}/{s}.json'), 'w') as json_file:
                        json.dump(data, json_file, ensure_ascii=False)

                    with open(resource_path(f'{self.exe_dir}/{self.pr_dir}/config.json'), 'w') as json_file:
                        json.dump(self.presets, json_file, ensure_ascii=False)

                    logging.info(f"Saved preset: {s}.")
                    self.preset_select.configure(values=self.presets)


            def delete_preset_event(self):
                d = self.preset_select.get()
                if d == "nothing" or d == "default":
                    pass
                elif d in self.presets:
                    self.presets.remove(d)

                    with open(resource_path(f'{self.exe_dir}/{self.pr_dir}/config.json'), 'w') as json_file:
                        json.dump(self.presets, json_file, ensure_ascii=False)

                    try:
                        os.remove(resource_path(f'{self.exe_dir}/{self.pr_dir}/{d}.json'))
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
                matching_sets = {}
                for item in data["sets"]:
                    for key, value in names_list.sets_dict.items():
                        if value == item:
                            matching_sets[value] = key
                for i in matching_sets.values():
                    self.sets_scrollable_frame_checkboxes[i - 1].select()
                for j in data["sets"]:
                    self.sets_selected.append(j)

                matching_sands = {}
                for item in data["sands"]:
                    for key, value in names_list.sands_main_stat_dict.items():
                        if value == item:
                            matching_sands[value] = key
                for i in matching_sands.values():
                    self.tab_1_checkboxes[i - 1].select()
                for j in data["sands"]:
                    self.tab_1_selected.append(j)

                matching_goblets = {}
                for item in data["goblet"]:
                    for key, value in names_list.goblet_main_stat_dict.items():
                        if value == item:
                            matching_goblets[value] = key
                for i in matching_goblets.values():
                    self.tab_2_checkboxes[i - 1].select()
                for j in data["goblet"]:
                    self.tab_2_selected.append(j)

                matching_circlets = {}
                for item in data["circlet"]:
                    for key, value in names_list.circlet_main_stat_dict.items():
                        if value == item:
                            matching_circlets[value] = key
                for i in matching_circlets.values():
                    self.tab_3_checkboxes[i - 1].select()
                for j in data["circlet"]:
                    self.tab_3_selected.append(j)

                matching_sands_d = {}
                for item in data["sands_d"]:
                    for key, value in names_list.sands_main_stat_dict.items():
                        if value == item:
                            matching_sands_d[value] = key
                for i in matching_sands_d.values():
                    self.tab_1_checkboxes2[i - 1].select()
                for j in data["sands_d"]:
                    self.tab_1_selected2.append(j)

                matching_goblets_d = {}
                for item in data["goblet_d"]:
                    for key, value in names_list.goblet_main_stat_dict.items():
                        if value == item:
                            matching_goblets_d[value] = key
                for i in matching_goblets_d.values():
                    self.tab_2_checkboxes2[i - 1].select()
                for j in data["goblet_d"]:
                    self.tab_2_selected2.append(j)

                matching_circlets_d = {}
                for item in data["circlet_d"]:
                    for key, value in names_list.circlet_main_stat_dict.items():
                        if value == item:
                            matching_circlets_d[value] = key
                for i in matching_circlets_d.values():
                    self.tab_3_checkboxes2[i - 1].select()
                for j in data["circlet_d"]:
                    self.tab_3_selected2.append(j)

                matching_substats = {}
                for item in data["substats"]:
                    for key, value in names_list.sub_stats_dict.items():
                        if value == item:
                            matching_substats[value] = key
                for i in matching_substats.values():
                    self.substats_scrollable_frame_checkboxes[i - 1].select()
                for j in data["substats"]:
                    self.substats_selected.append(j)

            def start_button_event(self):
                screen_ratio = "16:9"

                try:
                    activate_window()
                except Exception as e:
                    logging.error(e, exc_info=True)

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
                    logging.info(f"Starting sort... Params: {data}")
                    with open("logs\\summary.txt", 'a') as txt_file:
                        txt_file.write("=" * 30)
                        txt_file.write("\n")

                    mouse_move.MoveClickCheck(screen_ratio, self.sets_selected, self.substats_selected,
                                              self.tab_1_selected, self.tab_2_selected, self.tab_3_selected,
                                              self.tab_1_selected2,
                                              self.tab_2_selected2, self.tab_3_selected2).start()
                    logging.info(f"Время выполнения: {datetime.now() - start_time}")
                    logging.info("Finish sort.")
                except utils.FailSafeException:
                    logging.warning("Stopping... (FailSafe triggered from mouse moving to a corner of the screen.)")
                except Exception as e:
                    logging.error(e, exc_info=True)

            def on_app_start(self):
                file_to_open = "default"
                data = None

                try:
                    with open(resource_path(f'{self.exe_dir}/{self.pr_dir}/{file_to_open}.json'), 'r') as json_file:
                        data = json.load(json_file)
                    logging.info(f"Preset '{file_to_open}' loaded.")
                except FileNotFoundError:
                    logging.error(f"FileNotFoundError ({file_to_open})", exc_info=True)
                except Exception as e:
                    logging.error(e, exc_info=True)

                if data:
                    self.select_the_right_ones(data)

except Exception as e:
    logging.error(e, exc_info=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()
