# game.py
# CLI runner with adaptive Merchant reactions and dynamic memory progression.

from scenario import scenes, emotions_init, select_scene_variation, scene_variations
from endings import get_ending
import sys
import random

# ---------- UI helpers ----------
def print_rule():
    print("\nEmotion Balance Rule:")
    print("- Your responses add to Anger, Empathy, Curiosity, or Neutrality.")
    print("- Extremes lock an 'extreme' ending.")
    print("- Keep a balanced spread to unlock the True or Secret Reunion ending.")
    print("- The Merchant will react to your emotional state and choices.")
    print("- Your choices will change the memories you experience.\n")

def safe_input(prompt="> "):
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\nExiting...")
        sys.exit(0)

# ---------- Enhanced Adaptive Merchant ----------
def get_merchant_personality(emotions):
    """Determine merchant's current personality based on player's emotional state"""
    a, e, c, n = emotions["anger"], emotions["empathy"], emotions["curiosity"], emotions["neutral"]
    
    if a >= 3 and a > e + c:
        return "aggressive"
    elif e >= 3 and e > a:
        return "sympathetic"
    elif c >= 3 and c > a:
        return "intrigued"
    elif n >= 3:
        return "dismissive"
    else:
        return "neutral"

def merchant_conversation(emotions, scene_key, last_choice=None):
    """Generate dynamic merchant conversation based on context"""
    personality = get_merchant_personality(emotions)
    a, e, c, n = emotions["anger"], emotions["empathy"], emotions["curiosity"], emotions["neutral"]
    
    conversations = {
        "aggressive": {
            "scene1": [
                "Merchant's eyes narrow: 'Ah, the fighter. Your anger burns bright—but fire consumes everything.'",
                "Merchant smirks: 'Defiance. I've seen it before. It never ends well.'",
                "Merchant's voice hardens: 'You think you can intimidate me? This is my domain.'"
            ],
            "scene2": [
                "Merchant's grin turns predatory: 'Still fighting? The memories will break you harder.'",
                "Merchant leans forward: 'Your rage makes you predictable. Easy prey.'"
            ],
            "general": [
                "Merchant's face darkens: 'Your anger is a weapon—but it's pointed at yourself.'",
                "Merchant chuckles darkly: 'The more you fight, the deeper you sink.'"
            ]
        },
        "sympathetic": {
            "scene1": [
                "Merchant's expression softens: 'You carry such pain. Let me help you understand.'",
                "Merchant nods gently: 'Your heart is heavy. The memories will lighten the load.'"
            ],
            "scene2": [
                "Merchant's voice becomes warmer: 'You feel deeply. That's rare in this place.'",
                "Merchant smiles sadly: 'Your empathy is a gift, even here.'"
            ],
            "general": [
                "Merchant looks concerned: 'You care too much. That will hurt you.'",
                "Merchant's eyes show understanding: 'Your compassion is beautiful, but dangerous.'"
            ]
        },
        "intrigued": {
            "scene1": [
                "Merchant's eyes sparkle: 'A curious mind! You'll find the answers you seek.'",
                "Merchant grins: 'Questions, questions. I love a thinker.'"
            ],
            "scene2": [
                "Merchant taps the scroll excitedly: 'Your mind is sharp. The patterns will reveal themselves.'",
                "Merchant leans in: 'You see the connections, don't you? Keep looking.'"
            ],
            "general": [
                "Merchant's voice is animated: 'Your curiosity is insatiable. Perfect.'",
                "Merchant nods approvingly: 'You're asking the right questions.'"
            ]
        },
        "dismissive": {
            "scene1": [
                "Merchant shrugs: 'Indifference. How... boring.'",
                "Merchant's voice is flat: 'You don't care. That makes this easier.'"
            ],
            "scene2": [
                "Merchant yawns: 'Your apathy is almost impressive.'",
                "Merchant's expression is blank: 'Nothing moves you. How sad.'"
            ],
            "general": [
                "Merchant's voice is monotone: 'You're empty inside. Perfect for my purposes.'",
                "Merchant looks away: 'Your indifference is a shield. But shields can break.'"
            ]
        },
        "neutral": {
            "scene1": [
                "Merchant observes you carefully: 'Interesting. You're... balanced.'",
                "Merchant nods: 'You approach this with caution. Wise.'"
            ],
            "scene2": [
                "Merchant tilts his head: 'You're neither hot nor cold. Intriguing.'",
                "Merchant studies you: 'Your equilibrium is... unusual.'"
            ],
            "general": [
                "Merchant's expression is unreadable: 'You maintain your center. How... disciplined.'",
                "Merchant's voice is measured: 'Your balance is your strength. And your weakness.'"
            ]
        }
    }
    
    # Get appropriate conversation pool
    if scene_key in conversations[personality]:
        pool = conversations[personality][scene_key]
    else:
        pool = conversations[personality]["general"]
    
    return random.choice(pool)

def merchant_reaction_to_choice(emotions, choice_text, emotion_type):
    """Merchant reacts specifically to the player's choice"""
    a, e, c, n = emotions["anger"], emotions["empathy"], emotions["curiosity"], emotions["neutral"]
    
    reactions = {
        "anger": [
            "Merchant's smile sharpens: 'Anger burns bright, but it blinds you to the truth.'",
            "Merchant chuckles: 'Your rage is a beacon. It calls to the darkness.'",
            "Merchant's eyes gleam: 'Fire and fury. You're predictable in your passion.'"
        ],
        "empathy": [
            "Merchant's expression softens: 'Your heart still beats with compassion. How... human.'",
            "Merchant nods gently: 'You feel for others. That makes you vulnerable.'",
            "Merchant's voice becomes warmer: 'Your empathy is a light in this darkness.'"
        ],
        "curiosity": [
            "Merchant's eyes sparkle: 'Questions lead to answers, but answers lead to more questions.'",
            "Merchant grins: 'Your mind seeks patterns. The truth is a pattern too.'",
            "Merchant leans forward: 'Curiosity killed the cat, but satisfaction brought it back.'"
        ],
        "neutral": [
            "Merchant's expression is unreadable: 'Indifference is a choice. Every choice has consequences.'",
            "Merchant shrugs: 'You choose to feel nothing. That's a feeling too.'",
            "Merchant's voice is flat: 'Your neutrality is a mask. Masks can slip.'"
        ]
    }
    
    return random.choice(reactions[emotion_type])

def merchant_reaction(emotions, scene_key):
    a, e, c, n = emotions["anger"], emotions["empathy"], emotions["curiosity"], emotions["neutral"]
    
    # Scene-specific reactions
    if scene_key == "scene2":  # first shop talk reaction
        if a >= 2 and a >= e and a >= c and a >= n:
            return "Merchant's smile thins: 'Always barking. Careful—rage has a price.'"
        if e >= 2 and e >= a and e >= c and e >= n:
            return "Merchant softens: 'Strange. Even here, your heart still listens.'"
        if c >= 2 and c > a:
            return "Merchant taps the scroll: 'Still the scientist, hm? Poke carefully.'"
        if n >= 2:
            return "Merchant's voice flattens: 'Indifference is a chain too.'"
    
    # General reactive lines
    if a >= 3 and a > e + c:
        return "Merchant snarls: 'Your anger clouds you. One more outburst and the gems might bite back.'"
    if e >= 3 and e > a:
        return "Merchant tilts his head: 'After all this, your heart still bleeds for others.'"
    if c >= 3 and c > a:
        return "Merchant grins: 'You can't resist, can you? Always dissecting, always analyzing.'"
    if n >= 3:
        return "Merchant glitches, voice flat: 'Nothing moves you. Maybe you're already hollow.'"
    return None

def reactive_overlay(emotions):
    a, e, c, n = emotions["anger"], emotions["empathy"], emotions["curiosity"], emotions["neutral"]
    overlays = []
    if a >= 3 and a > e + c:
        overlays.append("A gemstone hairline-cracks in your palm.")
    if e >= 3 and e >= c and a == 0:
        overlays.append("For a heartbeat, the sawdust smell fades. Theo's eyes almost look human again.")
    if c >= 3 and c > a:
        overlays.append("Numbers ripple along the scroll margins—diagrams only you can see.")
    if n >= 3:
        overlays.append("Your voice sounds distant, as if dubbed a second too late.")
    return "\n".join(overlays)

# ---------- Dynamic progression ----------
def resolve_dynamic_next(emotions):
    """
    Choose which memory comes after the shop (scene2), based on emotion tilt.
    - Anger → Violence memory first (scene4)
    - Empathy → Mother first (scene3)
    - Curiosity → Insert glitch scene
    - Neutral → Stall with riddles
    - Default → Mother (scene3)
    """
    a, e, c, n = emotions["anger"], emotions["empathy"], emotions["curiosity"], emotions["neutral"]
    if a >= 2 and a >= e and a >= c and a >= n:
        return "scene4"
    if e >= 2 and e >= a and e >= c and e >= n:
        return "scene3"
    if c >= 2 and c > a:
        return "glitch"
    if n >= 2:
        return "stall"
    return "scene3"

# ---------- Natural Merchant Interactions ----------
def get_merchant_dialogue(emotions, scene_key, choice_made=None):
    """Generate natural merchant dialogue that flows with the story"""
    personality = get_merchant_personality(emotions)
    a, e, c, n = emotions["anger"], emotions["empathy"], emotions["curiosity"], emotions["neutral"]
    
    # Scene-specific merchant dialogue
    scene_dialogues = {
        "scene1": {
            "aggressive": [
                "Merchant's eyes narrow as you speak. 'Ah, the fighter awakens. Your anger burns bright—but fire consumes everything.'",
                "Merchant smirks at your defiance. 'I've seen your type before. It never ends well.'",
                "Merchant's voice hardens. 'You think you can intimidate me? This is my domain.'"
            ],
            "sympathetic": [
                "Merchant's expression softens. 'You carry such pain. Let me help you understand.'",
                "Merchant nods gently. 'Your heart is heavy. The memories will lighten the load.'",
                "Merchant's voice becomes warm. 'You feel deeply. That's rare in this place.'"
            ],
            "intrigued": [
                "Merchant's eyes sparkle. 'A curious mind! You'll find the answers you seek.'",
                "Merchant grins. 'Questions, questions. I love a thinker.'",
                "Merchant leans forward. 'Your mind never stops, does it?'"
            ],
            "dismissive": [
                "Merchant shrugs. 'Indifference. How... boring.'",
                "Merchant's voice is flat. 'You don't care. That makes this easier.'",
                "Merchant yawns. 'Your apathy is almost impressive.'"
            ],
            "neutral": [
                "Merchant observes you carefully. 'Interesting. You're... balanced.'",
                "Merchant nods. 'You approach this with caution. Wise.'",
                "Merchant tilts his head. 'You're neither hot nor cold. Intriguing.'"
            ]
        },
        "scene2": {
            "aggressive": [
                "Merchant's grin turns predatory. 'Still fighting? The memories will break you harder.'",
                "Merchant leans forward. 'Your rage makes you predictable. Easy prey.'",
                "Merchant's face darkens. 'Your anger is a weapon—but it's pointed at yourself.'"
            ],
            "sympathetic": [
                "Merchant's voice becomes warmer. 'You feel deeply. That's rare in this place.'",
                "Merchant smiles sadly. 'Your empathy is a gift, even here.'",
                "Merchant looks concerned. 'You care too much. That will hurt you.'"
            ],
            "intrigued": [
                "Merchant taps the scroll excitedly. 'Your mind is sharp. The patterns will reveal themselves.'",
                "Merchant leans in. 'You see the connections, don't you? Keep looking.'",
                "Merchant's voice is animated. 'Your curiosity is insatiable. Perfect.'"
            ],
            "dismissive": [
                "Merchant's expression is blank. 'Nothing moves you. How sad.'",
                "Merchant's voice is monotone. 'You're empty inside. Perfect for my purposes.'",
                "Merchant looks away. 'Your indifference is a shield. But shields can break.'"
            ],
            "neutral": [
                "Merchant studies you. 'Your equilibrium is... unusual.'",
                "Merchant's expression is unreadable. 'You maintain your center. How... disciplined.'",
                "Merchant's voice is measured. 'Your balance is your strength. And your weakness.'"
            ]
        }
    }
    
    # Get appropriate dialogue pool
    if scene_key in scene_dialogues and personality in scene_dialogues[scene_key]:
        pool = scene_dialogues[scene_key][personality]
    else:
        # General personality-based dialogue
        general_dialogues = {
            "aggressive": [
                "Merchant chuckles darkly. 'The more you fight, the deeper you sink.'",
                "Merchant's eyes gleam. 'Fire and fury. You're predictable in your passion.'"
            ],
            "sympathetic": [
                "Merchant's eyes show understanding. 'Your compassion is beautiful, but dangerous.'",
                "Merchant nods approvingly. 'You're asking the right questions.'"
            ],
            "intrigued": [
                "Merchant nods approvingly. 'You're asking the right questions.'",
                "Merchant's eyes sparkle. 'Questions lead to answers, but answers lead to more questions.'"
            ],
            "dismissive": [
                "Merchant's voice is flat. 'Your neutrality is a mask. Masks can slip.'",
                "Merchant shrugs. 'You choose to feel nothing. That's a feeling too.'"
            ],
            "neutral": [
                "Merchant's voice is measured. 'Your balance is your strength. And your weakness.'",
                "Merchant's expression is unreadable. 'You maintain your center. How... disciplined.'"
            ]
        }
        pool = general_dialogues.get(personality, ["Merchant watches silently."])
    
    return random.choice(pool)

def get_choice_reaction(emotions, choice_text, emotion_type):
    """Generate merchant reaction to specific choices"""
    a, e, c, n = emotions["anger"], emotions["empathy"], emotions["curiosity"], emotions["neutral"]
    
    reactions = {
        "anger": [
            "Merchant's smile sharpens. 'Anger burns bright, but it blinds you to the truth.'",
            "Merchant chuckles. 'Your rage is a beacon. It calls to the darkness.'",
            "Merchant's eyes gleam. 'Fire and fury. You're predictable in your passion.'"
        ],
        "empathy": [
            "Merchant's expression softens. 'Your heart still beats with compassion. How... human.'",
            "Merchant nods gently. 'You feel for others. That makes you vulnerable.'",
            "Merchant's voice becomes warmer. 'Your empathy is a light in this darkness.'"
        ],
        "curiosity": [
            "Merchant's eyes sparkle. 'Questions lead to answers, but answers lead to more questions.'",
            "Merchant grins. 'Your mind seeks patterns. The truth is a pattern too.'",
            "Merchant leans forward. 'Curiosity killed the cat, but satisfaction brought it back.'"
        ],
        "neutral": [
            "Merchant's expression is unreadable. 'Indifference is a choice. Every choice has consequences.'",
            "Merchant shrugs. 'You choose to feel nothing. That's a feeling too.'",
            "Merchant's voice is flat. 'Your neutrality is a mask. Masks can slip.'"
        ]
    }
    
    return random.choice(reactions[emotion_type])

# ---------- Interactive Merchant Options ----------
# def offer_merchant_interaction(emotions, scene_key):
#     """Offer player the chance to interact with the merchant"""
#     personality = get_merchant_personality(emotions)
#     
#     if personality == "aggressive":
#         print("\nMerchant glares at you. You can:")
#         print("1. Challenge him directly")
#         print("2. Ask about the memories")
#         print("3. Demand answers")
#         print("4. Continue with the story")
#     elif personality == "sympathetic":
#         print("\nMerchant looks at you with concern. You can:")
#         print("1. Ask for his help")
#         print("2. Share your confusion")
#         print("3. Ask about Theo")
#         print("4. Continue with the story")
#     elif personality == "intrigued":
#         print("\nMerchant's eyes sparkle with interest. You can:")
#         print("1. Ask about the machine")
#         print("2. Discuss the patterns")
#         print("3. Ask about the scroll")
#         print("4. Continue with the story")
#     elif personality == "dismissive":
#         print("\nMerchant barely acknowledges you. You can:")
#         print("1. Try to engage him")
#         print("2. Ask why he's here")
#         print("3. Demand his attention")
#         print("4. Continue with the story")
#     else:  # neutral
#         print("\nMerchant observes you calmly. You can:")
#         print("1. Ask about your emotions")
#         print("2. Discuss the process")
#         print("3. Ask about the ending")
#         print("4. Continue with the story")
#     
#     choice = safe_input("> ")
#     if choice == "4":
#         return None
#     
#     # Handle merchant interaction based on personality
#     responses = {
#         "aggressive": {
#             "1": "Merchant's face darkens: 'You want to fight? Fine. But remember—I control what you see.'",
#             "2": "Merchant snarls: 'The memories are real enough. Your denial won't change that.'",
#             "3": "Merchant's voice is dangerous: 'Answers have a price. Are you willing to pay?'"
#         },
#         "sympathetic": {
#             "1": "Merchant nods gently: 'I want to help you understand. The truth will set you free.'",
#             "2": "Merchant's voice is warm: 'Confusion is natural. The memories will bring clarity.'",
#             "3": "Merchant smiles sadly: 'Theo is... complicated. You'll understand soon.'"
#         },
#         "intrigued": {
#             "1": "Merchant's eyes light up: 'The Cerebridge! A marvel of neural engineering. Your creation.'",
#             "2": "Merchant gestures excitedly: 'Patterns everywhere! Your mind seeks order in chaos.'",
#             "3": "Merchant taps the scroll: 'The scroll contains all possibilities. Your choices write the story.'"
#         },
#         "dismissive": {
#             "1": "Merchant barely looks up: 'Engage? Why bother? You're just another customer.'",
#             "2": "Merchant shrugs: 'I'm here because you're here. Simple as that.'",
#             "3": "Merchant's voice is flat: 'My attention? You haven't earned it.'"
#         },
#         "neutral": {
#             "1": "Merchant tilts his head: 'Your emotions are data points. They tell a story.'",
#             "2": "Merchant nods: 'The process is simple: choose, feel, remember, repeat.'",
#             "3": "Merchant's expression is thoughtful: 'The ending depends on your emotional balance.'"
#         }
#     }
#     
#     if choice in responses[personality]:
#         print(f"\n{responses[personality][choice]}")
#         return responses[personality][choice]
#     
#     return None

# ---------- Game loop ----------
def run(input_fn=safe_input, output_fn=print):
    emotions = {k: v for k, v in emotions_init.items()}
    current = "scene1"
    last_choice = None
    choice_history = {}  # Track choices for dynamic scene selection

    print_rule()

    while True:
        # Get the appropriate scene variation based on emotional state and history
        scene_variation = select_scene_variation(current, emotions, choice_history)
        
        if scene_variation:
            node = scene_variation
        else:
            # Fallback to legacy scenes
            node = scenes.get(current, {"text": "Scene not found.", "choices": {}})
        
        output_fn("\n" + node["text"] + "\n")
        
        # Natural merchant dialogue that flows with the scene
        if current != "final" and random.random() < 0.4:  # 40% chance of merchant speaking
            merchant_dialogue = get_merchant_dialogue(emotions, current)
            if merchant_dialogue:
                output_fn(merchant_dialogue + "\n")
        
        # Merchant reacts to the *state at entry* of a scene
        reaction = merchant_reaction(emotions, current)
        if reaction:
            output_fn(reaction + "\n")
        
        # Offer merchant interaction (except in final scene)
        # if current != "final" and random.random() < 0.3:  # 30% chance
        #     merchant_response = offer_merchant_interaction(emotions, current)
        #     if merchant_response:
        #         # Small emotion adjustment based on interaction
        #         personality = get_merchant_personality(emotions)
        #         if personality == "sympathetic":
        #             emotions["empathy"] += 1
        #         elif personality == "aggressive":
        #             emotions["anger"] += 1
        #         elif personality == "intrigued":
        #             emotions["curiosity"] += 1
        #         elif personality == "dismissive":
        #             emotions["neutral"] += 1
        
        choices = node.get("choices", {})
        if not choices:
            break  # final scene reached → score-based ending

        # Show options
        for key, opt in choices.items():
            output_fn(f"{key}. {opt['text']}")
        
        choice = None
        while choice not in choices:
            choice = input_fn("> ").strip()
            if choice.lower() in ("q", "quit", "exit"):
                output_fn("Exiting...")
                sys.exit(0)
            if choice not in choices:
                output_fn("Please enter a valid option number.")

        picked = choices[choice]
        emo = picked["emotion"]
        emotions[emo] += 1
        last_choice = picked["text"]
        
        # Store choice in history for dynamic scene selection
        choice_history[current] = picked["text"]

        # Natural merchant reaction to the specific choice
        choice_reaction = get_choice_reaction(emotions, picked["text"], emo)
        if choice_reaction:
            output_fn("\n" + choice_reaction + "\n")

        # Flavor overlay after choice updates the mood
        overlay = reactive_overlay(emotions)
        if overlay:
            output_fn("\n" + overlay + "\n")

        # Progression
        nxt = picked["next"]
        if nxt == "dynamic":
            current = resolve_dynamic_next(emotions)
        else:
            current = nxt

    # Resolve ending
    ending = get_ending(emotions)
    output_fn("\n=== {} Ending ===".format(ending["title"]))
    output_fn(ending["summary"] + "\n")
    output_fn(ending["epilogue"] + "\n")

if __name__ == "__main__":
    run()
