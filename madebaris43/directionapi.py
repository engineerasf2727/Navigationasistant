import requests
import time
import geocoder
import re

API_KEY = "AIzaSyAlSnk1bIOvN29VcH9vuCNaxbk-62BoSsE"
destination = "41.037060,28.988514"  # Taksim örneği
prev_step = None

def get_current_location():
    return "41.035962,28.984896"

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', raw_html)

def label_instruction(instr):
    instr = instr.lower()
    if "turn right" in instr:
        return "turn_right"
    elif "turn left" in instr:
        return "turn_left"
    elif "slight right" in instr:
        return "slight_right"
    elif "slight left" in instr:
        return "slight_left"
    elif "u-turn" in instr:
        return "u_turn"
    elif "head" in instr:
        return "go_straight"
    else:
        return "unknown"

def get_next_step(origin):
    url = (
        f"https://maps.googleapis.com/maps/api/directions/json"
        f"?origin={origin}&destination={destination}&key={API_KEY}"
    )
    try:
        response = requests.get(url)
        data = response.json()
        step = data["routes"][0]["legs"][0]["steps"][0]
        instruction = clean_html(step["html_instructions"])
        distance = step["distance"]["text"]
        label = label_instruction(instruction)
        return instruction, distance, label
    except Exception as e:
        print("Hata:", e)
        return None

while True:
    origin = get_current_location()
    step = get_next_step(origin)

    if step:
        prev_step = step
        label = step[2]
        with open("next_direction.txt", "w") as file:
            file.write(label)
    else:
        print("Yeni adım alınamadı, önceki gösteriliyor.")

    print(f"Yön: {prev_step[0]} | Mesafe: {prev_step[1]} | Etiket: {prev_step[2]}")
    time.sleep(10)
