import json
import os


class FixtureManager:
    def __init__(self):
        pass

    def add_fixture(self, fixture_library_id, mode_id, fixture_id, fixture_display_name, dmx_address):
        all_available_fixtures = self.list_available_fixtures()
        name: str = str(all_available_fixtures[fixture_library_id][0])
        channels: list = all_available_fixtures[fixture_library_id][1][mode_id][1]

        with open("internal_files/dmx_patch.json") as f:
            data = json.load(f)

        # check if fixture id is empty
        for i in range(len(data)):
            if data[i]["id"] == fixture_id:
                return "error: fixture id is already taken"

        new_fixture: dict = {"id": int(fixture_id), "fixture_name": name, "display_name": fixture_display_name, "channel_length": len(channels), "dmx_start_address": str(dmx_address)}

        data.append(new_fixture)
        with open("internal_files/dmx_patch.json", 'w') as f:
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
        with open("internal_files/dmx_patch.json") as f:
            data = json.load(f)
        for i in range(len(data)):
            if data[i]["id"] == fixture_id:
                del data[i]
                break
        with open("internal_files/dmx_patch.json", 'w') as f:
            json.dump(data, f, indent=4, separators=(',', ': '))

    def list_available_fixtures(self):
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

    def select_mode(self):
        pass


F = FixtureManager()
# print(F.list_available_fixtures())
# print(F.add_fixture(0, 0, 2, "LED PAR 64 1", "0.1"))
# F.remove_fixture(1004)
print(F.add_multiple_fixtures(1, 1, 2000, "MHX", "0.100", 10, 7))