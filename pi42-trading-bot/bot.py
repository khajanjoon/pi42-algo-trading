CONFIG_FILE = Path("config.json")
config = {}

def load_config():

    global config, SYMBOLS, MIN_QTY

    with open(CONFIG_FILE) as f:

        config = json.load(f)

    SYMBOLS.clear()
    MIN_QTY.clear()

    for sym, s in config["symbols"].items():

        if s["enabled"]:

            SYMBOLS.append(sym)
            MIN_QTY[sym] = s["min_qty"]