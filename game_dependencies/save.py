import json

hr = 0
thr = 0
mny = 2500.0
btcs = 0.00000000
watt = 0
bill = 0
InventoryMiner = []

save_file = {
    "hashrate": hr,
    "totalhashrate": thr,
    "money": mny,
    "btcs": btcs,
    "watt": watt,
    "bill": bill,
    "InventoryMiner": [],
}


def savegame(hr, thr, mny, btcs, watt, bill, InventoryMiner):
    global save_file
    try: 
        save_file = {
            "hashrate": hr,
            "totalhashrate": thr,
            "money": mny,
            "btcs": btcs,
            "watt": watt,
            "bill": bill,
            "InventoryMiner": InventoryMiner,
        }
    except:
        print("Error: Filed to load all stats for saving game.")
    json_save_object = json.dumps(save_file, indent=6)
    with open("save/save.json", "w") as outfile:
        outfile.write(json_save_object)

def loadgame():
    global hr, thr, mny, btcs, watt, bill, InventoryMiner
    try:
        with open('save/save.json', 'r') as openfile:
            json_save_object = json.load(openfile)
        hr = json_save_object["hashrate"]
        thr = json_save_object["totalhashrate"]
        mny = json_save_object["money"]
        btcs = json_save_object["btcs"]
        watt = json_save_object["watt"]
        bill = json_save_object["bill"]
        InventoryMiner = json_save_object["InventoryMiner"]
    except Exception as e:
        print(f'Error: {e}')
    return hr, thr, mny, btcs, watt, bill, InventoryMiner
