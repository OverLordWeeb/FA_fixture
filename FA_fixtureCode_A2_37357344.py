import tkinter as tk # imports
from tkinter import filedialog
import random

class FADrawApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FA Cup Fourth Round Draw")
        self.teams = ["Manchester United", "Southampton", "Tottenham", "Watford", "Manchester City", # list of names teams
                      "Liverpool", "Leeds United", "Chelsea", "Arsenal", "Wolverhampton"]
        self.selected_team = ""
        self.fixtures = []

        #GUI elements
        self.teams_label = tk.Label(self, text="Quarter-Final Teams", font=("Arial", 14))
        self.teams_listbox = tk.Listbox(self, font=("Arial", 12), width=45, height=10)
        self.add_team_button = tk.Button(self, text="Add Team", font=("Arial", 12), command=self.add_team)
        self.select_button = tk.Button(self, text="Select Team", font=("Arial", 12), command=self.select_team)
        self.selected_team_label = tk.Label(self, text="Selected Team: ", font=("Arial", 12))
        self.fixtures_label = tk.Label(self, text="Match Fixtures", font=("Arial", 14))
        self.fixtures_listbox = tk.Listbox(self, font=("Arial", 12), width=45, height=10)
        self.draw_button = tk.Button(self, text="Draw Fixtures", font=("Arial", 12), command=self.draw_fixtures)
        self.load_teams_button = tk.Button(self, text="Load Teams", font=("Arial", 12), command=self.load_teams_from_file)
        self.save_fixtures_button = tk.Button(self, text="Save Fixtures", font=("Arial", 12), command=self.save_fixtures_to_file)

        #packing GUI elements
        self.teams_label.pack()
        self.teams_listbox.pack()
        self.add_team_button.pack()
        self.select_button.pack()
        self.selected_team_label.pack()
        self.fixtures_label.pack()
        self.fixtures_listbox.pack()
        self.draw_button.pack()
        self.load_teams_button.pack()
        self.save_fixtures_button.pack()

        # updates listbox with the initial teams
        self.update_teams_listbox()
#adding team to list
    def add_team(self):
        # asks the user for the name of the team to add
        team_name = tk.simpledialog.askstring("Add Team", "Enter team name:")
        if team_name:
            self.teams.append(team_name)
            self.update_teams_listbox()
#loading teams names from a file
    def load_teams_from_file(self):
        # Opens file explorer to find the file to load
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                self.teams = [team.strip() for team in file.readlines()]
                self.update_teams_listbox()
#updates the team list
    def update_teams_listbox(self):
        self.teams_listbox.delete(0, tk.END)
        for i, team in enumerate(self.teams, start=1):
            self.teams_listbox.insert(tk.END, f"{i}. {team}")
# Randomly select a team from the teams list as the selected team
    def select_team(self):
        if not self.teams:
            tk.messagebox.showinfo("Error", "No teams available.")
            return

        team_index = random.randint(1, len(self.teams))
        self.selected_team = self.teams[team_index - 1]
        self.selected_team_label.config(text=f"Selected Team: {self.selected_team}")

#draws fixtures shuffling the teams and makes them into pairs

    def draw_fixtures(self):
        if len(self.teams) < 2:
            tk.messagebox.showinfo("Error", "Not enough teams to draw fixtures.")
            return

        random.shuffle(self.teams)
        self.fixtures = [self.teams[i:i+2] for i in range(0, len(self.teams), 2)]
        self.update_fixtures_listbox()
#updates fixtures
    def update_fixtures_listbox(self):
        self.fixtures_listbox.delete(0, tk.END)
        for i, fixture in enumerate(self.fixtures, start=1):
            team1 = fixture[0] if fixture[0] else "TBD"
            team2 = fixture[1] if fixture[1] else "TBD"
            if self.selected_team and (self.selected_team in fixture):
                self.fixtures_listbox.insert(tk.END, f"Match {i}: {team1} vs {team2} ***")
            else:
                self.fixtures_listbox.insert(tk.END, f"Match {i}: {team1} vs {team2}")
#saves fixtures to a file that user chooses
    def save_fixtures_to_file(self):
        if not self.fixtures:
            tk.messagebox.showinfo("Error", "No fixtures available.")
            return
#asks for filepath and makes sure that the file thats getting loaded is txt file
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    for fixture in self.fixtures:
                        team1 = fixture[0] if fixture[0] else "TBD"
                        team2 = fixture[1] if fixture[1] else "TBD"
                        file.write(f"Match: {team1} vs {team2}\n")
#error message and success message depending on the outcome
                tk.messagebox.showinfo("Success", f"Fixtures saved to {file_path}.")
            except Exception as e:
                tk.messagebox.showinfo("Error", f"An error occurred while saving the fixtures:\n{str(e)}")

if __name__ == "__main__":
    app = FADrawApp()
    app.mainloop()
#ends the loop and the programs ends
