import json
import os


class FixtureManager:
    def __init__(self):
        pass

    def add_fixture(self, fixture_library_id: int, mode_id: int, fixture_id: int, fixture_display_name: str, dmx_address: str) -> str:
        all_available_fixtures = self.list_available_fixtures()
        name: str = str(all_available_fixtures[fixture_library_id][0])
        channels: list = all_available_fixtures[fixture_library_id][1][mode_id][1]

        with open("internal_files/fixture_patch.json") as f:
            data = json.load(f)

        # check if fixture id is empty
        for i in range(len(data)):
            if data[i]["id"] == fixture_id:
                return "error: fixture id is already taken"

        new_fixture: dict = {"id": int(fixture_id), "fixture_name": name, "fixture_library_id": fixture_library_id, "display_name": fixture_display_name, "channel_mode": mode_id, "dmx_start_address": str(dmx_address)}

        data.append(new_fixture)
        with open("internal_files/fixture_patch.json", 'w') as f:
            json.dump(data, f, indent=4, separators=(',', ': '))

        return "Done"

    def add_multiple_fixtures(self, fixture_library_id, mode_id, fixture_id, fixture_display_name, dmx_address, quantity, spacing):
        channel_length = len(self.list_available_fixtures()[fixture_library_id][1][mode_id][1])

        for i in range(quantity):
            spacing_temp = spacing + 1
            if i == 0:
                spacing_temp = 0
            ret = self.add_fixture(fixture_library_id, int(mode_id), int(fixture_id + i), str(fixture_display_name + " " + str(i)), str(dmx_address.split(".")[0] + "." + str(int(int(dmx_address.split(".")[1]) + i * channel_length) + i * spacing_temp)))
            if ret == "error: fixture id is already taken": return "Fixture ID Complications"

        return "Done"

    def remove_fixture(self, fixture_id):
        with open("internal_files/fixture_patch.json") as f:
            data = json.load(f)
        for i in range(len(data)):
            if data[i]["id"] == fixture_id:
                del data[i]
                break
        with open("internal_files/fixture_patch.json", 'w') as f:
            json.dump(data, f, indent=4, separators=(',', ': '))

    def list_available_fixtures(self) -> dict:
        available_fixtures: dict = {}
        for file in os.listdir("fixtures"):
            mode: dict = {}
            if file.endswith(".json"):
                filepath = os.path.join("fixtures", file)
                with open(filepath) as f:
                    data = json.load(f)
                for i in range(len(data["modes"])):
                    mode[i] = [data["modes"][i]["name"], data["modes"][i]["channels"]]
                available_fixtures[int(str(file).split("__")[0])] = ([data["name"], mode])

        return available_fixtures

    def get_fixture_library_id(self, fixture_id):
        with open("internal_files/fixture_patch.json") as f:
            data = json.load(f)
        for i in range(len(data)):
            if data[i]["id"] == fixture_id:
                return data[i]["fixture_library_id"]

    def get_fixute_mode_id(self, fixture_id):
        with open("internal_files/fixture_patch.json") as f:
            data = json.load(f)
        for i in range(len(data)):
            if data[i]["id"] == fixture_id:
                return data[i]["channel_mode"]

    def calculate_dmx_patch(self) -> dict:
        with open("internal_files/fixture_patch.json") as f:
            data = json.load(f)

        # create empty dmx patch
        dmx_patch = {}
        for u in range(3):
            for i in range(1, 513, 1):
                dmx_patch[str(u) + "." + str(i)] = ["empty", "empty", "empty"]

        # fill dmx patch
        for i in range(len(data)):
            dmx_patch[data[i]["dmx_start_address"]] = [data[i]["id"], data[i]["display_name"]]
            channels: list = self.list_available_fixtures()[data[i]["fixture_library_id"]][1][data[i]["channel_mode"]][1]
            for i_channel in range(len(channels)):
                build_list = [data[i]["id"], data[i]["display_name"], channels[i_channel]]  # [fixture_id, fixture_display_name, channel_name]
                dmx_patch[data[i]["dmx_start_address"].split(".")[0] + "." + str(int(data[i]["dmx_start_address"].split(".")[1]) + i_channel)] = build_list

        return dmx_patch

    def calculate_fixture_patch(self) -> dict:
        with open("internal_files/fixture_patch.json") as f:
            data = json.load(f)

        fixture_patch = {}
        for i in range(len(data)):
            fixture_patch[i] = data[i]

        return fixture_patch

F = FixtureManager()
# print(F.list_available_fixtures())
# print(F.add_fixture(0, 0, 2, "LED PAR 64 1", "0.1"))
# F.remove_fixture(1004)
print(F.add_multiple_fixtures(2, 0, 2, "LED PAR", "0.10", 3, 5))
# print(F.calculate_dmx_patch())
#for el in F.calculate_fixture_patch():
    #print(F.calculate_fixture_patch()[el])
