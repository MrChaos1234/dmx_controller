import json
import os


class FixtureManager:
    def __init__(self):
        pass

    def add_fixture(self, str_fixture_library_id: int, str_mode_id: int, str_fixture_id: int, fixture_display_name: str, dmx_address: str) -> str:
        print("add fixture started")
        fixture_library_id: int = int(str_fixture_library_id)
        mode_id: int = int(str_mode_id)
        fixture_id: int = int(str_fixture_id)

        all_available_fixtures = self.list_available_fixtures()
        name: str = str(all_available_fixtures[fixture_library_id][0])
        channels: list = all_available_fixtures[fixture_library_id][1][mode_id][1]

        with open("data/fixture_patch.json") as f:
            data = json.load(f)

        # check if fixture id is empty
        for i in range(len(data)):
            if data[i]["id"] == fixture_id:
                print("fixture manager.add_fixture: error: fixture id is already taken")
                return "error: fixture id is already taken"

        new_fixture: dict = {"id": int(fixture_id), "fixture_name": name, "fixture_library_id": fixture_library_id,
                             "display_name": fixture_display_name, "channel_mode": mode_id, "dmx_start_address": str(dmx_address)}

        data.append(new_fixture)
        with open("data/fixture_patch.json", 'w') as f:
            json.dump(data, f, indent=4, separators=(',', ': '))

        return "Done"

    def add_multiple_fixtures(self, fixture_library_id, mode_id, fixture_id, fixture_display_name, dmx_address, quantity, spacing):
        channel_length = len(self.list_available_fixtures()[
                             fixture_library_id][1][mode_id][1])

        for i in range(quantity):
            spacing_temp = spacing + 1
            if i == 0:
                spacing_temp = 0
            ret = self.add_fixture(fixture_library_id, int(mode_id), int(fixture_id + i), str(fixture_display_name + " " + str(i)), str(
                dmx_address.split(".")[0] + "." + str(int(int(dmx_address.split(".")[1]) + i * channel_length) + i * spacing_temp)))
            if ret == "error: fixture id is already taken":
                return "Fixture ID Complications"

        return "Done"

    def remove_fixture(self, fixture_id):
        with open("data/fixture_patch.json") as f:
            data = json.load(f)
        for i in range(len(data)):
            if data[i]["id"] == fixture_id:
                del data[i]
                break
        with open("data/fixture_patch.json", 'w') as f:
            json.dump(data, f, indent=4, separators=(',', ': '))

    def list_available_fixtures(self) -> dict:
        available_fixtures: dict = {}
        for file in os.listdir("data/fixture_library"):
            mode: dict = {}
            if file.endswith(".json"):
                filepath = os.path.join("data/fixture_library", file)
                with open(filepath) as f:
                    data = json.load(f)
                for i in range(len(data["modes"])):
                    mode[i] = [data["modes"][i]["name"],
                               data["modes"][i]["channels"]]
                available_fixtures[int(str(file).split("__")[0])] = (
                    [data["name"], mode])

        return available_fixtures

    def get_fixture_library_id(self, fixture_id):
        with open("data/fixture_patch.json") as f:
            data = json.load(f)
        for i in range(len(data)):
            if data[i]["id"] == fixture_id:
                return data[i]["fixture_library_id"]

    def get_fixute_mode_id(self, fixture_id):
        with open("data/fixture_patch.json") as f:
            data = json.load(f)
        for i in range(len(data)):
            if data[i]["id"] == fixture_id:
                return data[i]["channel_mode"]

    def calculate_dmx_patch(self) -> dict:
        with open("data/fixture_patch.json") as f:
            data = json.load(f)

        # create empty dmx patch
        dmx_patch = {}
        # add another loop here to create multiple universes
        for i in range(1, 513, 1):
            # dmx_patch[str(0) + "." + str(i)] = ["empty", "empty", "empty"]
            dmx_patch[str(i)] = ["empty", "empty", "empty"]

        # fill dmx patch
        for i in range(len(data)):
            dmx_patch[str(str(data[i]["dmx_start_address"]).split(".")[1])] = [data[i]["id"], data[i]["display_name"]]
            channels: list = self.list_available_fixtures()[data[i]["fixture_library_id"]][1][data[i]["channel_mode"]][1]
            for i_channel in range(len(channels)):
                # [fixture_id, fixture_display_name, channel_name]
                build_list = [data[i]["id"], data[i]
                              ["display_name"], channels[i_channel]]
                dmx_patch[str(int(str(data[i]["dmx_start_address"]).split(".")[1]) + i_channel)] = build_list
        # dmx_patch = {"1": [id, display_name, channel_name], "2": {..}}
        return dmx_patch

    def calculate_fixture_patch(self) -> dict:
        with open("data/fixture_patch.json") as f:
            data = json.load(f)

        fixture_patch = []
        for i in range(len(data)):
            fixture_patch.append(data[i])

        return fixture_patch


class Fixture(object):
    id: int
    fixture_name: str
    fixture_library_id: int
    display_name: str
    channel_mode: 0
    dmx_start_address: str
    selected: bool

    def __init__(self, data: dict, selected: bool = False):
        self.id = str(data["id"])
        self.fixture_name = str(data["fixture_name"])
        self.fixture_library_id = str(data["fixture_library_id"])
        self.display_name = str(data["display_name"])
        self.channel_mode = str(data["channel_mode"])
        self.dmx_start_address = str(data["dmx_start_address"])
        self.selected = selected

        if selected:
            self.selected = True
        else:
            self.selected = False


class LibraryFixture(object):
    id: str
    name: str

    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name


class Channel(object):
    id: str
    fixture_id: str
    fixture_display_name: str
    fixture_channel_name: str
    
    def __init__(self, id: str, fixture_id: str, fixture_display_name: str, fixture_channel_name: str):
        self.id = id
        self.fixture_id = fixture_id
        self.fixture_display_name = fixture_display_name
        self.fixture_channel_name = fixture_channel_name

# F = FixtureManager()
# print(F.list_available_fixtures())
# print(F.add_fixture(0, 0, 2, "LED PAR 64 1", "0.1"))
# F.remove_fixture(1004)
# print(F.add_multiple_fixtures(2, 0, 2, "LED PAR", "0.10", 3, 5))
# print(F.calculate_dmx_patch())
# print(F.calculate_fixture_patch())
# for el in F.calculate_fixture_patch():
    # print(F.calculate_fixture_patch()[el])
