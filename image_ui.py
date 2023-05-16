import customtkinter
import os
from PIL import Image
from orient_solver import *
from q_better import question

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.Solver = solver(True)

        f = open("id.txt","r")
        self.id = f.read()
        self.Solver.id = self.id
        f.close()

        f = open("reeks.txt","r")
        self.reeks = f.read()
        self.Solver.reeks = self.reeks
        f.close()

        self.title("Orient solver")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "orient_icon.png")), size=(26, 26))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.settings_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "settings-light.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "settings-light.png")), size=(20, 20))


        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Orient solver", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Solver",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Settings",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.settings_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")


        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure((0), weight=1)
        self.home_frame.grid_rowconfigure((0), weight=1)
        self.home_frame.grid_rowconfigure((1), weight=0)
        self.home_frame.grid_rowconfigure((2), weight=0)
        #first row
        self.main_output = customtkinter.CTkTextbox(self.home_frame)
        self.main_output.grid(row=0, column=0, sticky="nsew")
        self.main_output.tag_add("green",0.0)
        self.main_output.tag_config("green",foreground="green")
        #self.main_output.insert("0.0","respone1")
        #self.main_output.configure(state="disabled")


        self.submit_reeks = customtkinter.CTkButton(master=self.home_frame, command=self.next, text="Next Question",height=32)
        self.submit_reeks.grid(row=2, column=0, sticky="nsew")



        # create settings frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.entry = customtkinter.CTkEntry(self.second_frame, placeholder_text=self.id,width=500)
        self.entry.place(relx=0.5, rely=0.5,anchor=customtkinter.CENTER)
        self.submit_id = customtkinter.CTkButton(master=self.second_frame, command=self.submit_id_setting, text="Submit")
        self.submit_id.place(relx=0.5, rely=0.6,anchor=customtkinter.CENTER)

        self.entry_oefen_reeks = customtkinter.CTkEntry(self.second_frame, placeholder_text="reeks",width=100)
        self.entry_oefen_reeks.place(relx=0.6, rely=0.3,anchor=customtkinter.CENTER)
        self.entry_oefen_number = customtkinter.CTkEntry(self.second_frame, placeholder_text="numer",width=100)
        self.entry_oefen_number.place(relx=0.4, rely=0.3,anchor=customtkinter.CENTER)

        self.submit_reeks = customtkinter.CTkButton(master=self.second_frame, command=self.submit_reeks_setting, text="Submit")
        self.submit_reeks.place(relx=0.5, rely=0.4,anchor=customtkinter.CENTER)


        

        # select default frame
        self.select_frame_by_name("home")

    def next(self):
        import urllib.request
        
        try:
            answers = self.Solver.main_solve()


            self.main_output.delete("0.0","end")
            try:
                self.image.destroy()
            except:
                pass

            for i in self.Solver.questions:

                    if(i == None or answers[i] == None):
                        self.main_output.insert("0.0",i + " = " + "NO ANSWER FOUND" +"\n"+"\n")
                    else:
                        if(".jpg" in answers[i]):
                            urllib.request.urlretrieve('https://orientplus.ucll.be'+answers[i],"image.jpg")
                            self.answer_image = customtkinter.CTkImage(light_image=Image.open("image.jpg"),
                                            dark_image=Image.open("image.jpg"),
                                            size=(100, 100))
                            self.image = customtkinter.CTkLabel(self.home_frame, text="", image=self.answer_image)
                            self.image.grid(row=1, column=0, sticky="nsew")
                            self.main_output.insert("0.0",i +"\n")
                            print("image")

                        elif(".jpg" in i):
                            urllib.request.urlretrieve('https://orientplus.ucll.be'+i,"image.jpg")
                            self.answer_image = customtkinter.CTkImage(light_image=Image.open("image.jpg"),
                                            dark_image=Image.open("image.jpg"),
                                            size=(250, 250))
                            self.image = customtkinter.CTkLabel(self.home_frame, text="", image=self.answer_image)
                            self.image.grid(row=1, column=0, sticky="nsew")
                            self.main_output.insert("0.0",answers[i] +"\n",tags="green")
                            print("image")
                        else:
                            
                            self.main_output.insert("end", i + " = ")
                            self.main_output.insert("end", answers[i] + "\n" + "\n", tags="green")
        except ValueError as e:
            print(repr(e))
            self.main_output.insert("0.0","SORRY FUCK REEKS C" +"\n"+"\n",tags="green")

                
        



    def submit_id_setting(self):
        if(self.entry.get() != ""):
            self.id = self.entry.get()
            self.Solver.id = self.id
        f = open("id.txt","w")
        f.write(self.id)
        f.close()
        print("submit id = " + self.id) 


    def submit_reeks_setting(self):
        if(self.entry_oefen_number.get() != "" and self.entry_oefen_reeks.get() != ""):
            self.reeks = "exercise-"+self.entry_oefen_number.get()+"-"+self.entry_oefen_reeks.get().upper()
            self.Solver.reeks = self.reeks
        
        f = open("reeks.txt","w")
        f.write(self.reeks)
        f.close()
        print("submit reeks = " + self.reeks) 


    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")


        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")



    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()