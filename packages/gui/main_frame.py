import customtkinter as ctk

from packages.gui.song_frame import SongFrame


class MainFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)

        self.parent = master

        self.configure(width=700, height=600, corner_radius=0, fg_color="transparent")
        self.grid(row=0, column=1, sticky="nsew", pady=(10, 10))

        self.grid_propagate()

        self.create_initial_box()  # creates 5 initial black text boxes

    def create_textbox(self, song) -> None:
        result_font = ctk.CTkFont(family="Verdana", size=20)

        # ---RESULT TEXTBOX---
        result = ctk.CTkTextbox(self, width=650, height=105, font=result_font)
        result.insert("1.0", f"\n{song}")
        result.configure(state=ctk.DISABLED, wrap=ctk.WORD)
        result.pack(padx=(5, 5), pady=5, expand=True, fill="both")

    def create_initial_box(self) -> None:
        for i in range(5):
            initial_result_box = ctk.CTkTextbox(self, width=650, height=105)
            initial_result_box.configure(state=ctk.DISABLED, wrap=ctk.WORD)
            initial_result_box.pack(padx=(5, 5), pady=5, expand=True, fill="both")

    def destroy_text_boxes(self) -> None:
        if self.winfo_children():
            for widget in self.winfo_children():
                widget.destroy()

    def display_result(self, track_data: dict) -> None:
        song_frame = SongFrame(self, track_data)
        song_frame.pack(padx=(5, 5), pady=5)

    def open_player(self, name: str, image_url: str, preview_url: str) -> None:
        self.parent.open_player(name, image_url, preview_url)
