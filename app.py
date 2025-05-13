from flask import Flask, render_template, request, redirect
import random

app = Flask(__name__)

# Game State
player = {"hp": 100, "mana": 100}
enemy = {"hp": 100}
inventory = {
    'healing_potion': 1,
    'mana_potion': 1
}
message = ""

@app.route('/')
def index():
    return render_template("index.html", player=player, enemy=enemy, inventory=inventory, message=message)

@app.route('/action', methods=['POST'])
def action():
    global player, enemy, inventory, message
    move = request.form.get('move')
    message = ""

    if move == 'attack':
        damage = random.randint(0, 10)
        enemy['hp'] = max(enemy['hp'] - damage, 0)
        message = f"You attacked the enemy for {damage} damage!"
    
    elif move == 'heal':
        if player['mana'] >= 20 and player['hp'] < 100:
            player['mana'] -= 20
            player['hp'] = min(player['hp'] + 30, 100)
            message = "You healed 30 HP!"
        else:
            message = "Not enough mana or HP full."

    elif move == 'use_healing_potion':
        if inventory['healing_potion'] > 0:
            player['hp'] = min(player['hp'] + 50, 100)
            inventory['healing_potion'] -= 1
            message = "Used healing potion!"
        else:
            message = "No healing potions left!"

    elif move == 'use_mana_potion':
        if inventory['mana_potion'] > 0:
            player['mana'] = min(player['mana'] + 50, 100)
            inventory['mana_potion'] -= 1
            message = "Used mana potion!"
        else:
            message = "No mana potions left!"

    # Enemy turn
    if enemy['hp'] > 0:
        enemy_damage = random.randint(0, 15)
        player['hp'] = max(player['hp'] - enemy_damage, 0)
        message += f" Enemy hits you for {enemy_damage}!"

    return redirect('/')
    
if __name__ == "__main__":
    app.run(debug=True)