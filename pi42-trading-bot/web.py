from flask import Flask, request, jsonify, render_template_string
import json
from pathlib import Path

CONFIG_FILE = Path("config.json")

app = Flask(__name__)

# ========= LOAD CONFIG =========

def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)

# ========= UI =========

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Trading Bot Control</title>

<style>
body {
    font-family: Arial;
    background: #0f172a;
    color: white;
    padding: 10px;
}

.card {
    background: #1e293b;
    padding: 15px;
    margin: 10px 0;
    border-radius: 10px;
}

button {
    padding: 10px;
    margin: 5px;
    border: none;
    border-radius: 6px;
}

.add { background: green; color: white; }
.remove { background: red; color: white; }

input {
    padding: 8px;
    margin: 5px;
}
</style>

</head>
<body>

<h2>Trading Bot Dashboard</h2>

<div id="symbols"></div>

<h3>Add Symbol</h3>

<input id="symbol" placeholder="Symbol">
<input id="capital" placeholder="Capital">
<input id="qty" placeholder="Min Qty">

<button class="add" onclick="add()">Add</button>

<script>

async function load(){

    let res = await fetch("/config")
    let data = await res.json()

    let html = ""

    for(let s in data.symbols){

        let sym = data.symbols[s]

        html += `
        <div class="card">
        <b>${s}</b><br>
        Capital: ${sym.capital}<br>
        Min Qty: ${sym.min_qty}<br>
        Enabled: ${sym.enabled}<br>

        <button class="remove" onclick="remove('${s}')">
        Remove
        </button>

        </div>
        `
    }

    document.getElementById("symbols").innerHTML = html
}

async function add(){

    let symbol = document.getElementById("symbol").value
    let capital = document.getElementById("capital").value
    let qty = document.getElementById("qty").value

    await fetch("/add", {

        method:"POST",
        headers:{"Content-Type":"application/json"},

        body:JSON.stringify({
            symbol:symbol,
            capital:parseFloat(capital),
            qty:parseFloat(qty)
        })
    })

    load()
}

async function remove(symbol){

    await fetch("/remove",{

        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({symbol:symbol})

    })

    load()
}

load()

</script>

</body>
</html>
"""

# ========= ROUTES =========

@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/config")
def config():
    return jsonify(load_config())


@app.route("/add", methods=["POST"])
def add():

    data = request.json
    cfg = load_config()

    cfg["symbols"][data["symbol"]] = {

        "capital": data["capital"],
        "min_qty": data["qty"],
        "enabled": True
    }

    save_config(cfg)

    return "OK"


@app.route("/remove", methods=["POST"])
def remove():

    data = request.json
    cfg = load_config()

    cfg["symbols"].pop(data["symbol"], None)

    save_config(cfg)

    return "OK"


# ========= START =========

app.run(host="0.0.0.0", port=5000)
