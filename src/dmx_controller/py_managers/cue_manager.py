import json
import os


class CueManager:
    def __init__(self):
        pass
    
    def get_cues(self):
        with open("data/cue_list.json") as f:
            data = json.load(f)
        
        return data
    
    def add_cue(self, cue_id: str, cue_name: str, cue_group: str, data: dict):
        cue_id = int(cue_id)
        cue_group = int(cue_group)

        # open cue list
        with open("data/cue_list.json") as f:
            cues = json.load(f)

        # check if cue id is empty
        for i in range(len(cues)):
            if cues[i]["id"] == cue_id:
                print("cue_manager.add_cue: error: cue id is already taken")
                return "error: cue id is already taken"

        # create new cue
        new_cue: dict = {"id": cue_id, "cue_name": cue_name, "cue_group": cue_group, "data": data, "selected": False}
                            
        cues.append(new_cue)
        
        with open("data/cue_list.json", 'w') as f:
            json.dump(cues, f, indent=4, separators=(',', ': '))

        return "Done"
     
    def remove_cue(self, index: int):
        # open cue list
        with open("data/cue_list.json") as f:
            data = json.load(f)

        # remove cue
        for i in range(len(data)):
            if data[i]["id"] == index:
                data.pop(i)
                break
            
        # save cue list
        with open("data/cue_list.json", 'w') as f:
            json.dump(data, f, indent=4, separators=(',', ': '))
            
        return "Done"
    
    def update_button_grid_view(self):
        with open("data/button_grid_view.json") as f:
            data = json.load(f)
        return data

    def add_tile_cue_relation(self, tile_index: int, cue_index: int):
        with open("data/button_grid_view.json") as f:
            data = json.load(f)
        
        for i in range(len(data)):
            if data[i]["tile_id"] == tile_index: 
                data[i]["cue_id"] = cue_index
                
        with open("data/button_grid_view.json", 'w') as f:
            json.dump(data, f, indent=4, separators=(',', ': '))
            
        return "Done"
    
    def remove_tile_cue_relation(self, tile_index: int):
        with open("data/button_grid_view.json") as f:
            data = json.load(f)
            
        for i in range(len(data)):
            if data[i]["tile_id"] == tile_index: 
                data[i]["cue_id"] = "None"
                
        with open("data/button_grid_view.json", 'w') as f:
            json.dump(data, f, indent=4, separators=(',', ': '))
            
        return "Done"

    def get_temp_cue_data(self):
        with open("data/temp_cue_data.json") as f:
            data = json.load(f)
            
        return data
    
    def get_fader_cue_relation(self):
        with open("data/fader_cue.json") as f:
            data = json.load(f)
        return data

    def add_fader_cue_relation(self, page_id: int, fader_index: int, cue_index: int):
        with open("data/fader_cue.json") as f:
            data = json.load(f)
            
        for page in data:
            if page["page_id"] == page_id:
                for fader in page["fader_data"]:
                    fader["cue_id"] = cue_index
                
        with open("data/fader_cue.json", 'w') as f:
            json.dump(data, f, indent=4, separators=(',', ': '))
            
        return "Done"
    
    def remove_fader_cue_relation(self, page_id: int, fader_index: int):
        with open("data/fader_cue.json") as f:
            data = json.load(f)
            
        for page in data:
            if page["page_id"] == page_id:
                for fader in page["fader_data"]:
                    fader["cue_id"] = "None"
                
        with open("data/fader_cue.json", 'w') as f:
            json.dump(data, f, indent=4, separators=(',', ': '))
            
        return "Done"
    
    
class Cue(object):
    id: int
    cue_name: str
    cue_group: int
    data: list
    selected: bool
    
    def __init__(self, data: list, selected: bool = False):
        self.id = str(data["id"])
        self.cue_name = str(data["cue_name"])
        self.cue_group = str(data["cue_group"])
        self.data = data["data"]
        self.selected = selected
        
        if selected:
            self.selected = True
        else:
            self.selected = False

# C = CueManager()
