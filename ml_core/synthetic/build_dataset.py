import json
import os
import random
from datetime import datetime

# --- 1. Gold Standard Handcrafted Incidents ---
# Meticulously written natural language to test nuanced contradictions.

gold_incidents = [
    {
        "incident_id": "inc_gold_001",
        "incident_type": "road_accident",
        "ground_truth": {
            "entities": [
                {"id": "v1", "type": "VEHICLE", "attributes": {"make": "Honda Civic", "color": "dark blue", "plate": "XYZ123"}},
                {"id": "v2", "type": "VEHICLE", "attributes": {"make": "Ford F150", "color": "red"}},
                {"id": "p1", "type": "PERSON", "attributes": {"role": "driver_v1", "gender": "male", "clothing": "grey hoodie"}},
            ],
            "timeline": [
                {"time": "14:05:00", "action": "speeding", "subject": "v1", "location": "Main St"},
                {"time": "14:05:05", "action": "ran_red_light", "subject": "v1"},
                {"time": "14:05:06", "action": "crashed_into", "subject": "v1", "object": "v2"},
                {"time": "14:06:00", "action": "fled_scene", "subject": "p1"}
            ]
        },
        "witnesses": [
            {
                "witness_id": "w1",
                "statement": "I was walking down Main St around 2 PM. I saw this dark blue Honda Civic flying down the road. It completely blew through the red light and smashed right into a red pickup truck. After the crash, the guy driving the Honda jumped out and ran away down the alley. He was wearing a grey hoodie.",
                "perception": {"v1_color": "dark blue", "v1_make": "Honda Civic", "v2_color": "red", "v1_ran_red": True, "p1_fled": True, "p1_gender": "male"}
            },
            {
                "witness_id": "w2",
                "statement": "It happened really fast, maybe a bit after 2. A black sedan was going way too fast. I don't think they ran a red light though, the light was yellow when they entered the intersection. They hit a red Ford truck. The driver of the sedan got out, it looked like a woman, and she just took off running.",
                "perception": {"v1_color": "black", "v1_make": "sedan", "v2_color": "red", "v2_make": "Ford truck", "v1_ran_red": False, "p1_fled": True, "p1_gender": "female"}
            },
            {
                "witness_id": "w3",
                "statement": "I was looking out my window. I heard the crash first. I looked and saw a blue car had hit a red truck. The driver of the blue car was a man in a black jacket, and he stayed by the car calling someone on his phone.",
                "perception": {"v1_color": "blue", "v2_color": "red", "p1_fled": False, "p1_gender": "male", "p1_clothing": "black jacket"}
            }
        ],
        "labels": [
            {"claim_pair": ["w1: v1_color(dark blue)", "w2: v1_color(black)"], "type": "attribute", "verdict": "contradiction"},
            {"claim_pair": ["w1: v1_ran_red(True)", "w2: v1_ran_red(False)"], "type": "existence", "verdict": "contradiction"},
            {"claim_pair": ["w1: p1_gender(male)", "w2: p1_gender(female)"], "type": "attribute", "verdict": "contradiction"},
            {"claim_pair": ["w1: p1_fled(True)", "w3: p1_fled(False)"], "type": "existence", "verdict": "contradiction"},
            {"claim_pair": ["w1: p1_clothing(grey hoodie)", "w3: p1_clothing(black jacket)"], "type": "attribute", "verdict": "contradiction"}
        ]
    },
    {
        "incident_id": "inc_gold_002",
        "incident_type": "robbery_assault",
        "ground_truth": {
            "entities": [
                {"id": "p1", "type": "PERSON", "attributes": {"role": "assailant", "gender": "male", "height": "tall", "weapon": "knife"}},
                {"id": "p2", "type": "PERSON", "attributes": {"role": "victim", "gender": "male"}},
                {"id": "v1", "type": "VEHICLE", "attributes": {"role": "getaway", "color": "silver", "make": "Toyota Camry"}}
            ],
            "timeline": [
                {"time": "21:30:00", "action": "approached", "subject": "p1", "object": "p2", "location": "ATM on 5th Ave"},
                {"time": "21:30:15", "action": "threatened_with", "subject": "p1", "object": "knife"},
                {"time": "21:31:00", "action": "fled_in", "subject": "p1", "object": "v1", "direction": "North"}
            ]
        },
        "witnesses": [
            {
                "witness_id": "w1",
                "statement": "I was waiting for a cab at around 9:30 PM. I saw a tall man approach another guy at the ATM. He pulled out a knife and demanded money. After he got it, he ran and jumped into a silver Toyota that sped off heading North.",
                "perception": {"p1_height": "tall", "p1_weapon": "knife", "v1_color": "silver", "v1_make": "Toyota", "v1_direction": "North"}
            },
            {
                "witness_id": "w2",
                "statement": "I was across the street. The attacker was pretty short, honestly. He definitely had a gun, not a knife. I saw it glint in the street light. He took the money and got into a white sedan, then drove away heading South down 5th Ave.",
                "perception": {"p1_height": "short", "p1_weapon": "gun", "v1_color": "white", "v1_make": "sedan", "v1_direction": "South"}
            },
            {
                "witness_id": "w3",
                "statement": "I heard yelling. When I looked, I saw a tall guy holding a knife to someone's back. He grabbed the cash and ran into an alleyway on foot. There was no car involved.",
                "perception": {"p1_height": "tall", "p1_weapon": "knife", "v1_involved": False}
            }
        ],
        "labels": [
            {"claim_pair": ["w1: p1_height(tall)", "w2: p1_height(short)"], "type": "attribute", "verdict": "contradiction"},
            {"claim_pair": ["w1: p1_weapon(knife)", "w2: p1_weapon(gun)"], "type": "attribute", "verdict": "contradiction"},
            {"claim_pair": ["w1: v1_color(silver)", "w2: v1_color(white)"], "type": "attribute", "verdict": "contradiction"},
            {"claim_pair": ["w1: v1_direction(North)", "w2: v1_direction(South)"], "type": "motion", "verdict": "contradiction"},
            {"claim_pair": ["w1: fled_in(v1)", "w3: v1_involved(False)"], "type": "existence", "verdict": "contradiction"}
        ]
    },
    {
        "incident_id": "inc_gold_003",
        "incident_type": "fire",
        "ground_truth": {
            "entities": [
                {"id": "loc1", "type": "LOCATION", "attributes": {"building_type": "warehouse"}},
                {"id": "p1", "type": "PERSON", "attributes": {"role": "arsonist", "clothing": "dark jacket"}}
            ],
            "timeline": [
                {"time": "02:15:00", "action": "started_fire", "subject": "p1", "location": "loading dock"},
                {"time": "02:20:00", "action": "exploded", "subject": "loc1"}
            ]
        },
        "witnesses": [
            {
                "witness_id": "w1",
                "statement": "I work the night shift nearby. Around 2:15 AM, I saw someone in a dark jacket throw something at the loading dock, and suddenly there was a massive fire. About five minutes later, there was a huge explosion.",
                "perception": {"fire_start_time": "02:15", "p1_clothing": "dark jacket", "explosion_occurred": True}
            },
            {
                "witness_id": "w2",
                "statement": "I noticed the flames around 3:00 AM. It started on the roof, not the loading dock. I didn't see anyone around. The building just burned, there was absolutely no explosion at all.",
                "perception": {"fire_start_time": "03:00", "fire_start_location": "roof", "explosion_occurred": False}
            }
        ],
        "labels": [
            {"claim_pair": ["w1: fire_start_time(02:15)", "w2: fire_start_time(03:00)"], "type": "temporal", "verdict": "contradiction"},
            {"claim_pair": ["w1: fire_start_location(loading dock)", "w2: fire_start_location(roof)"], "type": "spatial", "verdict": "contradiction"},
            {"claim_pair": ["w1: explosion_occurred(True)", "w2: explosion_occurred(False)"], "type": "existence", "verdict": "contradiction"}
        ]
    }
]

# --- 2. Procedural Engine for Massive Scale ---
# Generates thousands of varied incidents using dynamic Mad-Libs templates.

def generate_procedural_incidents(num_incidents=50):
    incidents = []
    
    colors = ["red", "blue", "black", "white", "silver", "green", "grey"]
    makes = ["Toyota", "Honda", "Ford", "Chevrolet", "Nissan", "BMW"]
    directions = ["North", "South", "East", "West"]
    times = ["10:00 AM", "12:30 PM", "3:15 PM", "6:45 PM", "11:00 PM"]
    
    for i in range(num_incidents):
        # Pick ground truth
        true_color_1 = random.choice(colors)
        true_color_2 = random.choice(colors)
        true_make_1 = random.choice(makes)
        true_dir = random.choice(directions)
        true_time = random.choice(times)
        
        # Decide if witnesses will contradict
        w1_color = true_color_1
        w2_color = random.choice([true_color_1, random.choice(colors)]) # Maybe wrong
        w3_color = random.choice([true_color_1, random.choice(colors)]) # Maybe wrong
        
        w1_ran_red = True
        w2_ran_red = random.choice([True, False])
        
        w1_dir = true_dir
        w2_dir = random.choice(directions)
        
        # Build statements
        w1_stmt = f"It was {true_time}. I saw a {w1_color} {true_make_1} speeding {w1_dir}. It ran the red light and hit a {true_color_2} car."
        
        # W2 hedges and introduces contradictions
        hedge = random.choice(["I think", "I'm pretty sure", "From what I saw,"])
        ran_red_str = "ran right through the red light" if w2_ran_red else "definitely had a green light"
        w2_stmt = f"{hedge} it was a {w2_color} car. It was heading {w2_dir}. It {ran_red_str} before the crash."
        
        # W3 focuses on something else
        w3_stmt = f"I only saw the aftermath. The {w3_color} car was completely smashed."
        
        labels = []
        if w1_color != w2_color:
            labels.append({"claim_pair": [f"w1: color({w1_color})", f"w2: color({w2_color})"], "type": "attribute", "verdict": "contradiction"})
        if w1_ran_red != w2_ran_red:
            labels.append({"claim_pair": [f"w1: ran_red({w1_ran_red})", f"w2: ran_red({w2_ran_red})"], "type": "existence", "verdict": "contradiction"})
        if w1_dir != w2_dir:
            labels.append({"claim_pair": [f"w1: direction({w1_dir})", f"w2: direction({w2_dir})"], "type": "motion", "verdict": "contradiction"})
            
        incident = {
            "incident_id": f"inc_proc_{i+1:03d}",
            "incident_type": "road_accident",
            "ground_truth": {
                "entities": [
                    {"id": "v1", "type": "VEHICLE", "attributes": {"color": true_color_1, "make": true_make_1}}
                ]
            },
            "witnesses": [
                {"witness_id": "w1", "statement": w1_stmt, "perception": {"color": w1_color, "ran_red": w1_ran_red, "direction": w1_dir}},
                {"witness_id": "w2", "statement": w2_stmt, "perception": {"color": w2_color, "ran_red": w2_ran_red, "direction": w2_dir}},
                {"witness_id": "w3", "statement": w3_stmt, "perception": {"color": w3_color}}
            ],
            "labels": labels
        }
        
        incidents.append(incident)
        
    return incidents

# --- 3. Save Everything ---
def main():
    out_dir = "ml_core/synthetic/generated"
    os.makedirs(out_dir, exist_ok=True)
    
    all_incidents = gold_incidents + generate_procedural_incidents(100)
    
    print(f"Generated {len(all_incidents)} total synthetic incidents.")
    
    for inc in all_incidents:
        file_path = os.path.join(out_dir, f"{inc['incident_id']}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(inc, f, indent=2)
            
    print(f"Successfully wrote {len(all_incidents)} JSON files to {out_dir}")

if __name__ == "__main__":
    main()
