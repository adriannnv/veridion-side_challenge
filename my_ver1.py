import random
    from nltk.corpus import wordnet
    from time import sleep
    import requests

    host = "http://172.18.4.158:8000"
    post_url = f"{host}/submit-word"
    get_url = f"{host}/get-word"
    status_url = f"{host}/status"


    NUM_ROUNDS = 5
    WORDS = {
        1: {"text": "Feather", "cost": 1},
        2: {"text": "Coal", "cost": 1},
        3: {"text": "Pebble", "cost": 1},
        4: {"text": "Leaf", "cost": 2},
        5: {"text": "Paper", "cost": 2},
        6: {"text": "Rock", "cost": 2},
        7: {"text": "Water", "cost": 3},
        8: {"text": "Twig", "cost": 3},
        9: {"text": "Sword", "cost": 4},
        10: {"text": "Shield", "cost": 4},
        11: {"text": "Gun", "cost": 5},
        12: {"text": "Flame", "cost": 5},
        13: {"text": "Rope", "cost": 5},
        14: {"text": "Disease", "cost": 6},
        15: {"text": "Cure", "cost": 6},
        16: {"text": "Bacteria", "cost": 6},
        17: {"text": "Shadow", "cost": 7},
        18: {"text": "Light", "cost": 7},
        19: {"text": "Virus", "cost": 7},
        20: {"text": "Sound", "cost": 8},
        21: {"text": "Time", "cost": 8},
        22: {"text": "Fate", "cost": 8},
        23: {"text": "Earthquake", "cost": 9},
        24: {"text": "Storm", "cost": 9},
        25: {"text": "Vaccine", "cost": 9},
        26: {"text": "Logic", "cost": 10},
        27: {"text": "Gravity", "cost": 10},
        28: {"text": "Robots", "cost": 10},
        29: {"text": "Stone", "cost": 11},
        30: {"text": "Echo", "cost": 11},
        31: {"text": "Thunder", "cost": 12},
        32: {"text": "Karma", "cost": 12},
        33: {"text": "Wind", "cost": 13},
        34: {"text": "Ice", "cost": 13},
        35: {"text": "Sandstorm", "cost": 13},
        36: {"text": "Laser", "cost": 14},
        37: {"text": "Magma", "cost": 14},
        38: {"text": "Peace", "cost": 14},
        39: {"text": "Explosion", "cost": 15},
        40: {"text": "War", "cost": 15},
        41: {"text": "Enlightenment", "cost": 15},
        42: {"text": "Nuclear Bomb", "cost": 16},
        43: {"text": "Volcano", "cost": 16},
        44: {"text": "Whale", "cost": 17},
        45: {"text": "Earth", "cost": 17},
        46: {"text": "Moon", "cost": 17},
        47: {"text": "Star", "cost": 18},
        48: {"text": "Tsunami", "cost": 18},
        49: {"text": "Supernova", "cost": 19},
        50: {"text": "Antimatter", "cost": 19},
        51: {"text": "Plague", "cost": 20},
        52: {"text": "Rebirth", "cost": 20},
        53: {"text": "Tectonic Shift", "cost": 21},
        54: {"text": "Gamma-Ray Burst", "cost": 22},
        55: {"text": "Human Spirit", "cost": 23},
        56: {"text": "Apocalyptic Meteor", "cost": 24},
        57: {"text": "Earth's Core", "cost": 25},
        58: {"text": "Neutron Star", "cost": 26},
        59: {"text": "Supermassive Black Hole", "cost": 35},
        60: {"text": "Entropy", "cost": 45},
    }

    # Define themes and their counter-themes (e.g., "fire" is countered by "water")
    THEMES = {
        "fire": "water",    # Fire is countered by Water
        "water": "earth",   # Water is countered by Earth
        "earth": "wind",    # Earth is countered by Wind
        "wind": "fire",     # Wind is countered by Fire
        "light": "dark",    # Light vs Dark
        "dark": "light",
        "life": "death",
        "death": "life",
        "energy": "matter",
        "matter": "energy",
        "order": "chaos",
        "chaos": "order"
    }

    def is_related_word(word, theme):
        """Check if word is related to theme through hypernym/hyponym relationships"""
        word_synsets = wordnet.synsets(word.lower())
        theme_synsets = wordnet.synsets(theme)
        
        for word_syn in word_synsets:
            for theme_syn in theme_synsets:
                # Check if they're the same synset
                if word_syn == theme_syn:
                    return True
                # Check if theme is a hypernym of word (more general)
                if theme_syn in word_syn.hypernyms():
                    return True
                # Check if word is a hypernym of theme (more specific)
                if word_syn in theme_syn.hypernyms():
                    return True
        return False

    def get_counter_words(theme):
        """Dynamically fetch counter-words from WORDS for the given theme."""
        theme_counters = {
            "earth": ["Stone", "Earth"],
            "fire": ["Flame"],
            "water": ["Water"],
            "wind": ["Storm", "Wind"],
            "light": ["Light", "star"],
            "dark": ["Shadow"],
            "life": ["Rebirth", "Cure"],
            "death": ["Death", "Gun", "Rope"],
        }
        possible_words = [
            info["text"] for info in WORDS.values()
            if any(keyword.lower() in info["text"].lower() 
                for keyword in theme_counters.get(theme, []))
        ]
        return possible_words

    def weighted_choice(words):
        weights = [WORDS[id]["cost"] for id in words]
        return random.choices(words, weights=weights, k=1)[0]

    def what_beats(word):
        word_lower = word.lower()
        responses = []
        # 1. Check for powerful keywords
        powerful_keywords = [
            "massive", "super", "black hole", "apocalypse", "nuclear", "gamma", "supernova", "entropy",
            "unstoppable", "infinite", "galactic", "eternal", "devastating", "cataclysmic", "titanic", "colossal",
            "legendary", "ultimate", "immense", "inexorable", "immortal", "raging", "invincible", "universal",
            "monstrous", "boundless", "mighty", "overwhelming", "world-shaking", "crushing", "tremendous", 
            "god", "limitless", "cosmic", "formidable", "indestructible", "unbeatable", "infallible", 
            "terrifying", "infernal", "fiery", "relentless", "unyielding", "giant", "huge", "strong", "powerful",
            "huge", "mass", "giant", "immense", "vast", "great", "epic", "fierce", "unstoppable", "colossus"
        ]
        if any(keyword in word_lower for keyword in powerful_keywords):
            print("Powerful keyword detected - automatic Neutron Star")
            return "Neutron Star"

        # 2. Check for thematic synonyms and counter with WORDS
        for theme in THEMES:
            if is_related_word(word, theme):
                # print(f"'{word}' relates to '{theme}' through hypernym/hyponym relationship")
                counter_theme = THEMES[theme]
                counter_words = get_counter_words(counter_theme)
                # print(f"Possible counters: {counter_words}")
                responses.extend(counter_words)

        # 3. Check for special characters (y, space, apostrophe, hyphen)
        if any(char in word_lower for char in [' ', "'", '-']):
            # print("Special character detected - selecting word with cost between 25 and 35")
            responses.extend([
                info["text"] for info in WORDS.values()
                if 24 <= info["cost"] <= 26
            ])

        # 4. Fallback to word length → cost range
        word_length = len(word)
        if word_length <= 6:
            cost_range = (4, 8)
            # print(f"Short word ({word_length} chars) - using cost range {cost_range}")
        elif 7 <= word_length <= 12:
            cost_range = (14, 19)
            # print(f"Medium word ({word_length} chars) - using cost range {cost_range}")
        else:
            # print(f"Long word ({word_length} chars) - using cost range between 25 and 35")
            responses.append("Neutron Star")

        if not responses:
            possible_words = [
                info["text"] for info in WORDS.values()
                if cost_range[0] <= info["cost"] <= cost_range[1]
            ]
            responses.extend(possible_words if possible_words else ["Neutron Star"])

        if responses:
            response_weights = [
                WORDS[next(k for k, info in WORDS.items() if info["text"] == word)]["cost"]
                for word in responses
            ]
            
            chosen_word = random.choices(responses, weights=response_weights, k=1)[0]
            return chosen_word

        return "Neutron Star"

    def play_game():
        for round_id in range(1, NUM_ROUNDS+1):
            round_num = -1
            while round_num != round_id:
                response = requests.get(get_url)
                print(response.json())
                sys_word = response.json()['word']
                round_num = response.json()['round']

                sleep(0.2)

            if round_id > 1:
                status = requests.get(status_url)
                # print(status_url)
                print(status.json())

            chosen_word = what_beats(sys_word)
            print(sys_word)
            chosen_word_id = next((k for k, v in WORDS.items() if v["text"] == chosen_word), None)
            print(chosen_word_id)

            if chosen_word_id is None:
                print(f"Error: Could not find ID for word '{chosen_word}'")
                continue

            data = {"player_id":"1" , "word_id": chosen_word_id, "round_id": round_id}
            response = requests.post(post_url, json=data)
            print(response.json())

    if __name__ == "__main__":
        play_game()