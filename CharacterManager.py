#import yaml
from os.path import sep, isfile, isdir
from os import listdir, mkdir
import sys
import json
from shutil import copyfile
from ruamel.yaml import YAML
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox, BOTH
from tkinter.ttk import Frame, Button
import traceback

global yaml
yaml = YAML()
yaml.indent(mapping=4, sequence=4, offset=4)
yaml.allow_duplicate_keys = True
def yaml_load(filename):
    f = open(filename)
    data = yaml.load(f)
    f.close()
    return data

def yaml_dump(filename, data):
    f = open(filename, 'w')
    data = yaml.dump(data, f)
    f.close()

def isactive(ability):
    if ability["Level"] == "X":
        return True
    if ability["Level"] <= 10:
        return True
    return False

def translate(mod_info, translation, base_info):
    new_data = {}
    new_data["health_tables"] = base_info["health_tables"]
    for character in mod_info.keys():
        new_data["health_tables"][translation[character]] = mod_info[character]["health_tables"]
    new_data["default_cards"] = base_info["default_cards"]
    for character in mod_info.keys():
        new_data["default_cards"][translation[character]] = mod_info[character]["default_cards"]
    new_data["base_character_information"] = {}
    for character in mod_info.keys():
        new_data["base_character_information"][translation[character]] = mod_info[character]["base_character_information"]
        new_data["base_character_information"][translation[character]]["Name"] = translation[character]
    new_data["character_cards"] = {}
    for character in mod_info.keys():
        new_data["character_cards"][translation[character]] = {}
        for ability_name in mod_info[character]["character_cards"].keys():
            new_data["character_cards"][translation[character]][ability_name] = mod_info[character]["character_cards"][ability_name]
            new_data["character_cards"][translation[character]][ability_name]["Character"] = translation[character]
    new_data["character_perks"] = {}
    for character in mod_info.keys():
        new_data["character_perks"][translation[character]] = {}
        for perk in mod_info[character]["character_perks"].keys():
            new_data["character_perks"][translation[character]][perk] = mod_info[character]["character_perks"][perk]
            new_data["character_perks"][translation[character]][perk]["Character"] = translation[character]
    new_data["default_party"] = base_info["default_party"]
    for character in mod_info.keys():
        new_data["default_party"]["Characters"][translation[character]]["Cards"] = mod_info[character]["default_party"]
    return new_data
        
        
def build_translation(base_ruleset, changed_data):
    characters_to_overwrite = list(base_ruleset["character_cards"].keys())
    translation = {}
    
    
"""
def build_translation(base_ruleset, changed_data):
    characters_to_overwrite = list(base_ruleset["character_cards"].keys())
    translation = {}
    for character in changed_data.keys():
        print("What character would you like to overwrite with the " + character + " data?")
        print("Remaining options are: " + ', '.join(characters_to_overwrite))
        req = input("-->")
        while req not in characters_to_overwrite:
            print("Invalid input, please try again")
            req = input("-->")
        translation[character] = req
        characters_to_overwrite.remove(req)
    print(translation)
    return translation
"""
def load_default_information(base_ruleset):
    health_tables = yaml_load(base_ruleset + sep + "CharacterHealthTables.yml")
    default_cards = yaml_load(base_ruleset + sep + "InitialCards.yml")
    base_character_information = {}
    for character in listdir(base_ruleset + sep + "Characters"):
        temp_information = yaml_load(base_ruleset + sep + "Characters" + sep + character)
        base_character_information[temp_information["Name"]] = temp_information
    character_cards = {}
    for character in listdir(base_ruleset + sep + "AbilityCardDefinitions"):
        if isfile(base_ruleset + sep + "AbilityCardDefinitions" + sep + character):
            continue
        character_cards[character] = {}
        for card in listdir(base_ruleset + sep + "AbilityCardDefinitions" + sep + character):
            character_cards[character][card] = yaml_load(base_ruleset + sep + "AbilityCardDefinitions" + sep + character + sep + card)
    character_perks = {}
    for character in listdir(base_ruleset + sep + "Perks"):
        character_perks[character] = {}
        for perk in listdir(base_ruleset + sep + "Perks" + sep + character):
            temp_information = yaml_load(base_ruleset + sep + "Perks" + sep + character + sep + perk)
            character_perks[character][temp_information["Name"]] = temp_information
    default_party = yaml_load(base_ruleset + sep + "RoguelikeMode" + sep + "Parties" + sep + "Party_Default.yml")
    d = {}
    d["health_tables"] = health_tables
    d["default_cards"] = default_cards
    d["base_character_information"] = base_character_information
    d["character_cards"] = character_cards
    d["character_perks"] = character_perks
    d["default_party"] = default_party
    return d

def load_mod_information(mod_dir, base_info):
    health_tables = None
    default_cards = None
    default_party = None
    if isfile(mod_dir + sep + "CharacterHealthTables.yml"):
        health_tables = yaml_load(mod_dir + sep + "CharacterHealthTables.yml")
    if isfile(mod_dir + sep + "InitialCards.yml"):
        default_cards = yaml_load(mod_dir + sep + "InitialCards.yml")
    base_character_information = {}
    if isdir(mod_dir + sep + "Characters"):
        for character in listdir(mod_dir + sep + "Characters"):
            temp_information = yaml_load(mod_dir + sep + "Characters" + sep + character)
            base_character_information[temp_information["Name"]] = temp_information
    character_cards = {}
    if isdir(mod_dir + sep + "AbilityCardDefinitions"):
        for character in listdir(mod_dir + sep + "AbilityCardDefinitions"):
            character_cards[character] = {}
            if isdir(mod_dir + sep + "AbilityCardDefinitions" + sep + character):
                for card in listdir(mod_dir + sep + "AbilityCardDefinitions" + sep + character):
                    character_cards[character][card] = yaml_load(mod_dir + sep + "AbilityCardDefinitions" + sep + character + sep + card)
    character_perks = {}
    if isdir(mod_dir + sep + "Perks"):
        for character in listdir(mod_dir + sep + "Perks"):
            character_perks[character] = {}
            if isdir(mod_dir + sep + "Perks" + sep + character):
                for perk in listdir(mod_dir + sep + "Perks" + sep + character):
                    temp_information = yaml_load(mod_dir + sep + "Perks" + sep + character + sep + perk)
                    character_perks[character][temp_information["Name"]] = temp_information
    if isfile(mod_dir + sep + "RoguelikeMode" + sep + "Parties" + sep + "Party_Default.yml"):
        default_party = yaml_load(mod_dir + sep + "RoguelikeMode" + sep + "Parties" + sep + "Party_Default.yml")

    changed_characters = character_perks.keys()

    changed_data = {}
    for character in changed_characters:
        changed_data[character] = {}
        if health_tables is None:
            changed_data[character]["health_tables"] = base_info["health_tables"][character]
        else:
            changed_data[character]["health_tables"] = health_tables[character]
        if default_cards is None:
            changed_data[character]["default_cards"] = base_info["default_cards"][character]
        else:
            changed_data[character]["default_cards"] = default_cards[character]
        if default_party is None:
            changed_data[character]["default_party"] = base_info["default_party"]["Characters"][character]["Cards"]
        else:
            changed_data[character]["default_party"] = default_party["Characters"][character]["Cards"]
        if character in base_character_information.keys():
            changed_data[character]["base_character_information"] = base_character_information[character]
        else:
            changed_data[character]["base_character_information"] = base_info["base_character_information"][character]
        changed_data[character]["character_cards"] = {}
        for ability in character_cards[character].keys():
            if isactive(character_cards[character][ability]):
                changed_data[character]["character_cards"][ability] = character_cards[character][ability]
        if character in character_perks.keys():
            changed_data[character]["character_perks"] = {}
            for perk in character_perks[character].keys():
                changed_data[character]["character_perks"][perk] = character_perks[character][perk]
        else:
            for perk in base_info["character_perks"][character]:
                changed_data[character]["character_perks"][perk] = base_info["character_perks"][character]
    return changed_data

def create_new_mod(changed_data, dirname, mod_name, translation, source):
    new_mod_name = mod_name
    for character in translation.keys():
        new_mod_name = new_mod_name + "(" + character + "-" + translation[character] + ")"
    dest = dirname + sep + new_mod_name
    mkdir(dest)
    copyfile(source + sep + "meta.dat", dest + sep + "meta.dat")
    copyfile(source + sep + "preview.png", dest + sep + "preview.png")
    yaml_dump(dest + sep + "CharacterHealthTables.yml", changed_data["health_tables"])
    mkdir(dest + sep + "RoguelikeMode")
    mkdir(dest + sep + "RoguelikeMode" + sep + "Parties")
    yaml_dump(dest + sep + "RoguelikeMode" + sep + "Parties" + sep + "Party_Default.yml", changed_data["default_party"])
    mkdir(dest + sep + "Perks")
    for character in changed_data["character_perks"].keys():
        mkdir(dest + sep + "Perks" + sep + character)
        for perk in changed_data["character_perks"][character].keys():
            yaml_dump(dest + sep + "Perks" + sep + character + sep + perk, changed_data["character_perks"][character][perk])
    mkdir(dest + sep + "Characters")
    for character in translation.keys():
        yaml_dump(dest + sep + "Characters" + sep + translation[character] + ".yml", changed_data["base_character_information"][translation[character]])
    mkdir(dest + sep + "AbilityCardDefinitions")
    for character in changed_data["character_cards"].keys():
        mkdir(dest + sep + "AbilityCardDefinitions" + sep + character)
        for card in changed_data["character_cards"][character].keys():
            yaml_dump(dest + sep + "AbilityCardDefinitions" + sep + character + sep + card, changed_data["character_cards"][character][card])
    return       
        
    
    
class Main(Frame):
    def __init__(self):
        super().__init__(width=350, height=400)
        self.mod_dir = ""
        self.ruleset_dir = ""
        self.initUI()
    def initUI(self):
        self.master.title("Character Manager")
        self.mod_button = Button(self, text="Select Mod", command=self.set_mod_dir)
        self.mod_button.place(x=200, y = 300)
        self.ruleset_button = Button(self, text="Select Ruleset", command=self.set_ruleset)
        self.ruleset_button.place(x=50, y=300)
        self.pack(fill=BOTH, expand=1)
    def set_mod_dir(self):
        self.mod_dir = filedialog.askdirectory(initialdir="E:\\SteamLibrary\\steamapps\\workshop\\content\\780290\\1974517056")
        if self.ruleset_dir != "":
            self.set_selection_options()
    def set_ruleset(self):
        self.ruleset_dir = filedialog.askdirectory(initialdir="C:\\Users\\kylefriedline\\AppData\\LocalLow\\FlamingFowlStudios\\Gloomhaven\\GloomModConfigs\\Second")
        if self.mod_dir != "":
            self.set_selection_options()
    def set_selection_options(self):
        try:
            self.default_data = load_default_information(self.ruleset_dir)
        except:
            messagebox.showerror(message="Ruleset directory ran into error:" + traceback.format_exc())
        try:
            self.changed_data = load_mod_information(self.mod_dir, self.default_data)
        except:
            messagebox.showerror(message="Parsing mod directory ran into error:" + traceback.format_exc())
        self.translation = {}
        self.characters_to_overwrite = list(self.default_data["character_cards"].keys())
        self.translation_characters = list(self.changed_data.keys())
        self.current_index = 0
        self.override_buttons = []
        current_index = 0
        for char in self.characters_to_overwrite:
            self.override_buttons.append(Button(self, text=char, command=lambda c=char: self.add_to_overwrite(c)))
            self.override_buttons[-1].place(x=50 + (current_index%2)*150, y = 50 * (int(current_index/2)+1))
            current_index += 1
    def add_to_overwrite(self, char):
        self.translation[self.translation_characters[self.current_index]] = char
        self.current_index += 1
        if self.current_index == len(self.changed_data.keys()):
            try:
                finalized_data = translate(self.changed_data, self.translation, self.default_data)
                create_new_mod(finalized_data, sep.join(self.ruleset_dir.split("/")[:-2]) + sep + "GloomMods", self.mod_dir.split("/")[-1], self.translation, self.mod_dir)
            except:
                messagebox.showerror(message="Issue creating new mod.  Check to make sure there isn't a previous conversion of the same mod")
            Frame.quit(self)

if __name__ == "__main__":
    app = Main()
    app.mainloop()
    """
    messagebox.showinfo("Test", "Please select your mod folder")
    mod_folder = filedialog.askdirectory()
    messagebox.showinfo("Test", "Please select your ruleset folder")
    ruleset_folder = filedialog.askdirectory()
    print(mod_folder)
    #canvas1.create_window(150, 150, window=
    default_data = load_default_information(ruleset_folder)
    changed_data = load_mod_information(mod_folder, default_data)
    translation = build_translation(default_data, changed_data)
    changed_data = translate(changed_data, translation, default_data)
    create_new_mod(changed_data, sep.join(ruleset_folder.split(sep)[:-3]) + sep + "GloomMods", mod_folder.split(sep)[-1], translation, mod_folder)
    #print(json.dumps(changed_data, indent=4))"""
