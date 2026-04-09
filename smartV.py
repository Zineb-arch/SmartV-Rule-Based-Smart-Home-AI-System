import copy

# --- 1. KNOWLEDGE BASE DESIGN ---
kb = {
    "time": "evening",
    "rooms": {
        "living_room": {
            "light_level": "low",
            "temperature": 18,
            "air_quality": "good",
            "occupied": False,
            "is_sleeping": False
        },
        "kitchen": {
            "light_level": "high",
            "temperature": 26,
            "air_quality": "poor",
            "occupied": True,
            "is_sleeping": False
        },
        "bedroom": {
            "light_level": "medium",
            "temperature": 22,
            "air_quality": "good",
            "occupied": False,
            "is_sleeping": False
        }
    },
    "devices": {
        "living_room": {"light": "off", "heater": "off", "window": "closed", "fan": "off"},
        "kitchen": {"light": "on", "heater": "off", "window": "closed", "fan": "off"},
        "bedroom": {"light": "off", "heater": "off", "window": "closed", "fan": "off"}
    }
}

# --- 2. RULE SYSTEM ---
# Rules are structured: (Source, Attribute, Operator, Value)
rules = [
    # --- LIGHTING RULES ---
    {
        "name": "Turn light ON (Occupied & Dark)",
        "priority": 8,
        "conditions": [
            ("room", "light_level", "==", "low"),
            ("room", "occupied", "==", True),
            ("device", "light", "==", "off"),
            ("room", "is_sleeping", "==", False)
        ],
        "actions": [("device", "light", "on")]
    },
    {
        "name": "Turn light OFF (Room Empty)",
        "priority": 7,
        "conditions": [
            ("room", "occupied", "==", False),
            ("device", "light", "==", "on"),
            ("room", "is_sleeping", "==", False)
        ],
        "actions": [("device", "light", "off")]
    },
    {
        "name": "Turn light OFF (Bright Room)",
        "priority": 9,
        "conditions": [
            ("device", "light", "==", "on"),
            ("room", "light_level", "==", "high")
        ],
        "actions": [("device", "light", "off")]
    },
    {
        "name": "Turn light OFF (Sleeping)",
        "priority": 12,
        "conditions": [
            ("room", "is_sleeping", "==", True),
            ("device", "light", "==", "on")
        ],
        "actions": [("device", "light", "off")]
    },
    # --- TEMPERATURE RULES ---
    {
        "name": "Turn heater ON (Cold)",
        "priority": 6,
        "conditions": [
            ("room", "temperature", "<", 20),
            ("device", "heater", "==", "off"),
            ("room", "occupied", "==", True),
            ("room", "is_sleeping", "==", False)
        ],
        "actions": [("device", "heater", "on")]
    },
    {
        "name": "Turn heater OFF (Comfortable)",
        "priority": 9,
        "conditions": [
            ("room", "temperature", ">=", 21),
            ("device", "heater", "==", "on")
        ],
        "actions": [("device", "heater", "off")]
    },
    {
        "name": "Turn fan ON (Hot & Occupied)",
        "priority": 10,
        "conditions": [
            ("room", "temperature", ">", 25),
            ("device", "fan", "==", "off"),
            ("room", "occupied", "==", True),
            ("room", "is_sleeping", "==", False)
        ],
        "actions": [("device", "fan", "on")]
    },
    {
        "name": "Turn fan OFF (Cooling down)",
        "priority": 10,
        "conditions": [
            ("room", "temperature", "<=", 25),
            ("device", "fan", "==", "on")
        ],
        "actions": [("device", "fan", "off")]
    },
    # --- VENTILATION RULES ---
    {
        "name": "Open window (Poor Air Quality)",
        "priority": 5,
        "conditions": [
            ("room", "air_quality", "==", "poor"),
            ("device", "window", "==", "closed"),
            ("room", "is_sleeping", "==", False)
        ],
        "actions": [("device", "window", "open")]
    },
    {
        "name": "Close window (Good Air Quality)",
        "priority": 9,
        "conditions": [
            ("room", "air_quality", "==", "good"),
            ("device", "window", "==", "open")
        ],
        "actions": [("device", "window", "closed")]
    },
    {
        "name": "Close window (Freezing Protection)",
        "priority": 8,
        "conditions": [
            ("room", "temperature", "<", 15),
            ("device", "window", "==", "open")
        ],
        "actions": [("device", "window", "closed")]
    },
    # --- ENERGY SAVING ---
    {
        "name": "Energy Saving (Empty Room)",
        "priority": 11,
        "conditions": [
            ("room", "occupied", "==", False),
            ("room", "is_sleeping", "==", False)
        ],
        "actions": [
            ("device", "heater", "off"),
            ("device", "fan", "off")
        ]
    }
]

# --- 3. REASONING ENGINE ---

def get_value(kb, room, source, attribute):
    if source == "room":
        return kb["rooms"][room][attribute]
    elif source == "device":
        return kb["devices"][room][attribute]
    return None

def compare(left, operator, right):
    if operator == "==": return left == right
    if operator == "<": return left < right
    if operator == ">": return left > right
    if operator == "<=": return left <= right
    if operator == ">=": return left >= right
    return False

def evaluate_rule(kb, room, rule):
    # Check if all conditions are satisfied
    for condition in rule["conditions"]:
        source, attribute, operator, value = condition
        current_value = get_value(kb, room, source, attribute)
        if not compare(current_value, operator, value):
            return False
    return True

def apply_actions(kb, room, actions):
    changes = []
    for action in actions:
        target, attribute, value = action
        if target == "device":
            current_value = kb["devices"][room][attribute]
            if current_value != value:
                kb["devices"][room][attribute] = value
                changes.append(f"{attribute}: {current_value} -> {value}")
    return changes

def forward_chain(kb, rules):
    """
    Implements a fixpoint-based forward chaining.
    Conflict resolution: Rules are scanned in descending order of priority.
    """
    print(">>> ENGINE STARTING REASONING CYCLE")
    
    # Sort rules once by priority (highest first)
    sorted_rules = sorted(rules, key=lambda x: x["priority"], reverse=True)
    
    for room_name in kb["rooms"]:
        stable = False
        while not stable:
            rule_fired_in_loop = False
            for rule in sorted_rules:
                if evaluate_rule(kb, room_name, rule):
                    changes = apply_actions(kb, room_name, rule["actions"])
                    if changes:
                        # Log explaining the action and conditions satisfied
                        cond_str = ", ".join([f"{c[1]} {c[2]} {c[3]}" for c in rule["conditions"]])
                        print(f"[ACTION] Room: {room_name} | Rule: '{rule['name']}'")
                        print(f"         Satisfied: {cond_str}")
                        print(f"         Changes: {', '.join(changes)}")
                        rule_fired_in_loop = True
                        break # Restart scanning from highest priority rule
            
            if not rule_fired_in_loop:
                stable = True # No more rules can fire for this room
                
    print(">>> FIXPOINT REACHED (Environment Stable)")

# --- 4. SIMULATION LOOP ---

SIMULATION_STEPS = [
    {
        "time": "evening",
        "rooms": {
            "living_room": {"light_level": "low", "temperature": 18, "air_quality": "poor", "occupied": True, "is_sleeping": False},
            "bedroom": {"light_level": "high", "temperature": 24, "air_quality": "good", "occupied": False, "is_sleeping": False},
            "kitchen": {"light_level": "medium", "temperature": 22, "air_quality": "good", "occupied": False, "is_sleeping": False}
        }
    },
    {
        "time": "night",
        "rooms": {
            "living_room": {"light_level": "low", "temperature": 17, "air_quality": "good", "occupied": False, "is_sleeping": False},
            "bedroom": {"light_level": "low", "temperature": 21, "air_quality": "good", "occupied": True, "is_sleeping": False},
            "kitchen": {"light_level": "low", "temperature": 20, "air_quality": "good", "occupied": False, "is_sleeping": False}
        }
    },
    {
        "time": "late_night",
        "rooms": {
            "bedroom": {"light_level": "low", "temperature": 20, "air_quality": "poor", "occupied": True, "is_sleeping": True},
        }
    },
    {
        "time": "morning",
        "rooms": {
            "living_room": {"light_level": "high", "temperature": 20, "air_quality": "good", "occupied": True, "is_sleeping": False},
            "kitchen": {"light_level": "medium", "temperature": 27, "air_quality": "poor", "occupied": True, "is_sleeping": False}
        }
    },
    {
        "time": "afternoon",
        "rooms": {
            "living_room": {"light_level": "high", "temperature": 28, "air_quality": "good", "occupied": True, "is_sleeping": False},
            "kitchen": {"light_level": "high", "temperature": 29, "air_quality": "poor", "occupied": True, "is_sleeping": False}
        }
    }
]

def update_environment(kb, step):
    kb["time"] = step["time"]
    for room, data in step["rooms"].items():
        for key, value in data.items():
            kb["rooms"][room][key] = value

# Run Simulation
for step in SIMULATION_STEPS:
    print(f"\n" + "="*50)
    print(f"TIME STEP: {step['time'].upper()}")
    print("="*50)
    update_environment(kb, step)
    forward_chain(kb, rules)
    
    print("\nFINAL DEVICE STATES:")
    for room, devices in kb["devices"].items():
        print(f" {room}: {devices}")