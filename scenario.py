# scenario.py
# Dynamic scenes with multiple variations based on player choices and emotional state.

emotions_init = {
    "anger": 0,
    "empathy": 0,
    "curiosity": 0,
    "neutral": 0
}

# Scene variations based on emotional state and previous choices
scene_variations = {
    "scene1": {
        "default": {
            "text": (
                "You wake up in a dimly lit room.\n"
                "Merchant: 'Finally awake, huh?'"
            ),
            "choices": {
                "1": {"text": "Remain silent.", "emotion": "neutral", "next": "scene2"},
                "2": {"text": "Who are you?", "emotion": "anger", "next": "scene2"},
                "3": {"text": "What happened?", "emotion": "empathy", "next": "scene2"},
                "4": {"text": "Is this… a dream?", "emotion": "curiosity", "next": "scene2"}
            }
        },
        "aggressive": {
            "text": (
                "You wake up in a dimly lit room, head pounding with rage.\n"
                "Merchant: 'Ah, the fighter awakens. Your anger precedes you.'"
            ),
            "choices": {
                "1": {"text": "Where am I, you bastard?", "emotion": "anger", "next": "scene2"},
                "2": {"text": "What did you do to me?", "emotion": "anger", "next": "scene2"},
                "3": {"text": "I'll find a way out of here.", "emotion": "anger", "next": "scene2"},
                "4": {"text": "You're going to regret this.", "emotion": "anger", "next": "scene2"}
            }
        },
        "sympathetic": {
            "text": (
                "You wake up in a dimly lit room, feeling strangely calm.\n"
                "Merchant: 'Welcome back. Your heart is still intact, I see.'"
            ),
            "choices": {
                "1": {"text": "Where am I?", "emotion": "empathy", "next": "scene2"},
                "2": {"text": "Are you here to help me?", "emotion": "empathy", "next": "scene2"},
                "3": {"text": "I feel... lost.", "emotion": "empathy", "next": "scene2"},
                "4": {"text": "Can you tell me what's happening?", "emotion": "empathy", "next": "scene2"}
            }
        },
        "curious": {
            "text": (
                "You wake up in a dimly lit room, mind racing with questions.\n"
                "Merchant: 'The curious one awakens. Your mind never stops, does it?'"
            ),
            "choices": {
                "1": {"text": "What is this place?", "emotion": "curiosity", "next": "scene2"},
                "2": {"text": "How did I get here?", "emotion": "curiosity", "next": "scene2"},
                "3": {"text": "What are you?", "emotion": "curiosity", "next": "scene2"},
                "4": {"text": "Is this some kind of experiment?", "emotion": "curiosity", "next": "scene2"}
            }
        }
    },

    "scene2": {
        "default": {
            "text": (
                "The Merchant smirks and leaves. You stumble outside. It's raining; alleys are empty.\n"
                "A faint light glows ahead — a jagged sign barely reads: 'Memories.'\n"
                "Inside, the shop smells of sawdust. Jewels glitter faintly.\n"
                "Merchant: 'Take a look at this scroll. Black gemstones. Hold one. Don't lose yourself.'"
            ),
            "choices": {
                "1": {"text": "Yes, I need to remember—whatever it costs.", "emotion": "curiosity", "next": "dynamic"},
                "2": {"text": "You think I'm scared? Bring it on.", "emotion": "anger", "next": "dynamic"},
                "3": {"text": "How do I know any of this is real?", "emotion": "neutral", "next": "dynamic"},
                "4": {"text": "What if these aren't even my memories?", "emotion": "empathy", "next": "dynamic"}
            }
        },
        "after_aggressive": {
            "text": (
                "The Merchant's smirk falters as you storm out. The rain feels like needles on your skin.\n"
                "A jagged sign glows ahead: 'Memories.' The shop reeks of something metallic.\n"
                "Merchant: 'Your anger makes you predictable. The gems will show you what you're missing.'"
            ),
            "choices": {
                "1": {"text": "I don't need your tricks!", "emotion": "anger", "next": "dynamic"},
                "2": {"text": "Show me what you've got.", "emotion": "anger", "next": "dynamic"},
                "3": {"text": "This is all a lie.", "emotion": "neutral", "next": "dynamic"},
                "4": {"text": "Fine. Let's get this over with.", "emotion": "neutral", "next": "dynamic"}
            }
        },
        "after_sympathetic": {
            "text": (
                "The Merchant's expression softens as you follow. The rain feels gentle, almost cleansing.\n"
                "A warm light glows ahead — the sign reads 'Memories' in elegant script.\n"
                "Inside, the shop smells like old books and comfort. Jewels pulse softly.\n"
                "Merchant: 'The gems hold truth. Your heart will guide you to what matters.'"
            ),
            "choices": {
                "1": {"text": "I want to understand.", "emotion": "empathy", "next": "dynamic"},
                "2": {"text": "Can you help me remember?", "emotion": "empathy", "next": "dynamic"},
                "3": {"text": "What am I supposed to see?", "emotion": "curiosity", "next": "dynamic"},
                "4": {"text": "I trust you to show me.", "emotion": "empathy", "next": "dynamic"}
            }
        }
    },

    "scene3": {
        "default": {
            "text": (
                "First Memory: A warm kitchen. Sunlight spills through the window.\n"
                "A woman hums while cooking. She kneels, smiling: 'Hey, dear Alaric,' and pats your head.\n"
                "You snap back — the gemstone glows pink.\n"
                "Merchant: 'That was your mother's love. First one's free.'"
            ),
            "choices": {
                "1": {"text": "I need more.", "emotion": "curiosity", "next": "scene4"},
                "2": {"text": "Show me more of your tricks.", "emotion": "anger", "next": "scene4"},
                "3": {"text": "There's a workaround, isn't there?", "emotion": "neutral", "next": "scene4"},
                "4": {"text": "I don't like this… but I need answers.", "emotion": "empathy", "next": "scene4"}
            }
        },
        "mother_loving": {
            "text": (
                "Memory: A sunlit kitchen filled with warmth and laughter.\n"
                "Your mother hums while cooking, her smile lighting up the room.\n"
                "She kneels beside you: 'Hey, dear Alaric, ready for your big day?'\n"
                "The gemstone glows with a soft pink light.\n"
                "Merchant: 'That was unconditional love. Pure and true.'"
            ),
            "choices": {
                "1": {"text": "I miss her so much.", "emotion": "empathy", "next": "scene4"},
                "2": {"text": "Why can't I remember more?", "emotion": "curiosity", "next": "scene4"},
                "3": {"text": "This feels too perfect.", "emotion": "neutral", "next": "scene4"},
                "4": {"text": "Show me what happened to her.", "emotion": "empathy", "next": "scene4"}
            }
        },
        "mother_conflicted": {
            "text": (
                "Memory: A tense kitchen, shadows playing on the walls.\n"
                "Your mother's hands shake as she cooks, her smile forced.\n"
                "She pats your head: 'Hey, dear Alaric,' but her eyes are distant.\n"
                "The gemstone flickers with uncertain light.\n"
                "Merchant: 'Love can be complicated. Even the purest hearts have shadows.'"
            ),
            "choices": {
                "1": {"text": "She was hurting too.", "emotion": "empathy", "next": "scene4"},
                "2": {"text": "What was she hiding?", "emotion": "curiosity", "next": "scene4"},
                "3": {"text": "This memory is flawed.", "emotion": "neutral", "next": "scene4"},
                "4": {"text": "I need to know the truth.", "emotion": "anger", "next": "scene4"}
            }
        },
        "mother_absent": {
            "text": (
                "Memory: An empty kitchen, cold and silent.\n"
                "No humming, no warmth, just the echo of what should have been.\n"
                "A note on the table: 'Sorry, Alaric. I had to go.'\n"
                "The gemstone glows with a cold blue light.\n"
                "Merchant: 'Sometimes the most painful memories are the ones that never happened.'"
            ),
            "choices": {
                "1": {"text": "She abandoned me.", "emotion": "anger", "next": "scene4"},
                "2": {"text": "Why did she leave?", "emotion": "curiosity", "next": "scene4"},
                "3": {"text": "It doesn't matter anymore.", "emotion": "neutral", "next": "scene4"},
                "4": {"text": "She must have had her reasons.", "emotion": "empathy", "next": "scene4"}
            }
        }
    },

    "scene4": {
        "default": {
            "text": (
                "Second Memory: You sit on the floor beside a red-haired boy, laughing with toy inventions.\n"
                "Suddenly, your parents' voices rise into an argument. A slap. Screams.\n"
                "You rush upstairs, screwdriver still in hand. In blind fury, you stab the man threatening your mother.\n"
                "Your friend sees everything. When police burst in, he takes the blame, holding the weapon.\n"
                "The gemstone glows blue."
            ),
            "choices": {
                "1": {"text": "He saved me… That means something.", "emotion": "empathy", "next": "scene5"},
                "2": {"text": "That was on me.", "emotion": "anger", "next": "scene5"},
                "3": {"text": "Irrelevant. What does this prove?", "emotion": "neutral", "next": "scene5"},
                "4": {"text": "Why does he seem so familiar?", "emotion": "curiosity", "next": "scene5"}
            }
        },
        "violence_heroic": {
            "text": (
                "Memory: You and Theo inventing together, laughter filling the room.\n"
                "Suddenly, screams echo from upstairs. Your mother's voice, desperate.\n"
                "You rush up, heart pounding. A man towers over her, hand raised.\n"
                "In a blur of motion, you protect her. Theo takes the blame to save you.\n"
                "The gemstone glows with protective blue light.\n"
                "Merchant: 'Sometimes violence is the only answer. Sometimes it's love.'"
            ),
            "choices": {
                "1": {"text": "I had no choice.", "emotion": "anger", "next": "scene5"},
                "2": {"text": "Theo saved me.", "emotion": "empathy", "next": "scene5"},
                "3": {"text": "What happened to the man?", "emotion": "curiosity", "next": "scene5"},
                "4": {"text": "I would do it again.", "emotion": "anger", "next": "scene5"}
            }
        },
        "violence_regret": {
            "text": (
                "Memory: You and Theo playing, but tension fills the air.\n"
                "Your father's voice booms from upstairs, followed by your mother's cries.\n"
                "You rush up, rage blinding you. The screwdriver in your hand feels heavy.\n"
                "Theo follows, tries to stop you, but it's too late. He takes the blame.\n"
                "The gemstone pulses with guilt-ridden light.\n"
                "Merchant: 'Violence has consequences. Even when it feels justified.'"
            ),
            "choices": {
                "1": {"text": "I should have controlled myself.", "emotion": "empathy", "next": "scene5"},
                "2": {"text": "Theo didn't deserve that.", "emotion": "empathy", "next": "scene5"},
                "3": {"text": "What was I thinking?", "emotion": "curiosity", "next": "scene5"},
                "4": {"text": "I can't change the past.", "emotion": "neutral", "next": "scene5"}
            }
        },
        "violence_manipulated": {
            "text": (
                "Memory: You and Theo in the basement, but something feels wrong.\n"
                "Voices echo from above, but they sound... rehearsed.\n"
                "You rush upstairs, but the scene feels staged. The man looks familiar.\n"
                "Theo's expression is knowing. This was planned.\n"
                "The gemstone flickers with uncertain light.\n"
                "Merchant: 'Not all memories are what they seem. Some are... constructed.'"
            ),
            "choices": {
                "1": {"text": "This was a setup.", "emotion": "anger", "next": "scene5"},
                "2": {"text": "Why would Theo do this?", "emotion": "curiosity", "next": "scene5"},
                "3": {"text": "None of this is real.", "emotion": "neutral", "next": "scene5"},
                "4": {"text": "There must be a reason.", "emotion": "empathy", "next": "scene5"}
            }
        }
    },

    "scene5": {
        "default": {
            "text": (
                "Third Memory: A school hallway. Students crowd a notice board labeled 'Test Results.'\n"
                "You scan anxiously. Theo Shaw: 1st place. You: 2nd.\n"
                "The paper melts, faces blur. You jolt back — gemstone glows yellow.\n"
                "The Merchant glitches slightly."
            ),
            "choices": {
                "1": {"text": "You tricked me! These aren't mine!", "emotion": "anger", "next": "scene6"},
                "2": {"text": "That name… Theo… why does it sound familiar?", "emotion": "curiosity", "next": "scene6"},
                "3": {"text": "Am I even Alaric?", "emotion": "neutral", "next": "scene6"},
                "4": {"text": "Not my memory. Stop lying.", "emotion": "neutral", "next": "scene6"}
            }
        },
        "competition_friendly": {
            "text": (
                "Memory: A school hallway buzzing with excitement.\n"
                "You and Theo stand before the results board, both nervous.\n"
                "Theo Shaw: 1st place. You: 2nd place.\n"
                "Theo turns to you, beaming: 'We did it together, partner!'\n"
                "The gemstone glows with warm yellow light.\n"
                "Merchant: 'Competition can bring people together, not just drive them apart.'"
            ),
            "choices": {
                "1": {"text": "We were a great team.", "emotion": "empathy", "next": "scene6"},
                "2": {"text": "I'm happy for him.", "emotion": "empathy", "next": "scene6"},
                "3": {"text": "What happened to our friendship?", "emotion": "curiosity", "next": "scene6"},
                "4": {"text": "We should celebrate together.", "emotion": "empathy", "next": "scene6"}
            }
        },
        "competition_bitter": {
            "text": (
                "Memory: A tense school hallway, students whispering.\n"
                "You scan the results board, heart sinking.\n"
                "Theo Shaw: 1st place. You: 2nd place.\n"
                "Theo's smile looks smug. Your fists clench.\n"
                "The gemstone glows with jealous green light.\n"
                "Merchant: 'Envy can poison even the strongest bonds.'"
            ),
            "choices": {
                "1": {"text": "He always gets everything.", "emotion": "anger", "next": "scene6"},
                "2": {"text": "I deserved first place.", "emotion": "anger", "next": "scene6"},
                "3": {"text": "Why does he always win?", "emotion": "curiosity", "next": "scene6"},
                "4": {"text": "This isn't fair.", "emotion": "anger", "next": "scene6"}
            }
        },
        "competition_manipulated": {
            "text": (
                "Memory: A school hallway that feels... wrong.\n"
                "The results board shows impossible scores.\n"
                "Theo Shaw: 1st place. You: 2nd place.\n"
                "But you remember getting first. The numbers keep changing.\n"
                "The gemstone flickers erratically.\n"
                "Merchant: 'Memory is unreliable. Especially when someone else is writing it.'"
            ),
            "choices": {
                "1": {"text": "This isn't what happened.", "emotion": "anger", "next": "scene6"},
                "2": {"text": "Someone changed the results.", "emotion": "curiosity", "next": "scene6"},
                "3": {"text": "I don't trust any of this.", "emotion": "neutral", "next": "scene6"},
                "4": {"text": "Why would someone do this?", "emotion": "empathy", "next": "scene6"}
            }
        }
    },

    "scene6": {
        "default": {
            "text": (
                "Fourth Memory: A rooftop at dusk. Graduation day. Diplomas beside you.\n"
                "Theo leans back, smiling: 'I got an offer — a Neuro Lab. Cutting-edge. But I won't take it without you, my partner.'\n"
                "You hesitate. He insists: 'You anchor me. Without you, I collapse.'\n"
                "The gemstone glows green."
            ),
            "choices": {
                "1": {"text": "Am I watching myself, or you?", "emotion": "neutral", "next": "scene7"},
                "2": {"text": "I want real memories, not tricks!", "emotion": "anger", "next": "scene7"},
                "3": {"text": "Even if it's not mine… maybe it still matters.", "emotion": "curiosity", "next": "scene7"},
                "4": {"text": "Then who am I if none of this is mine?", "emotion": "empathy", "next": "scene7"}
            }
        },
        "partnership_true": {
            "text": (
                "Memory: A rooftop at sunset, diplomas in hand.\n"
                "Theo leans back, genuine joy in his eyes.\n"
                "'I got an offer from the Neuro Lab. Cutting-edge research. But I won't go without you.'\n"
                "'You're my partner, Alaric. We do this together or not at all.'\n"
                "The gemstone glows with pure green light.\n"
                "Merchant: 'True partnership is rare. Cherish it.'"
            ),
            "choices": {
                "1": {"text": "We'll do amazing things together.", "emotion": "empathy", "next": "scene7"},
                "2": {"text": "I'm honored you chose me.", "emotion": "empathy", "next": "scene7"},
                "3": {"text": "What will we discover?", "emotion": "curiosity", "next": "scene7"},
                "4": {"text": "I won't let you down.", "emotion": "empathy", "next": "scene7"}
            }
        },
        "partnership_manipulative": {
            "text": (
                "Memory: A rooftop at sunset, but Theo's smile doesn't reach his eyes.\n"
                "'I got an offer from the Neuro Lab. They want me, but they'll take you too.'\n"
                "'You're useful, Alaric. Your mind complements mine perfectly.'\n"
                "The gemstone glows with cold green light.\n"
                "Merchant: 'Partnership can be a cage, disguised as opportunity.'"
            ),
            "choices": {
                "1": {"text": "You're using me.", "emotion": "anger", "next": "scene7"},
                "2": {"text": "I'm not your tool.", "emotion": "anger", "next": "scene7"},
                "3": {"text": "What's your real agenda?", "emotion": "curiosity", "next": "scene7"},
                "4": {"text": "Maybe I can change his mind.", "emotion": "empathy", "next": "scene7"}
            }
        },
        "partnership_imagined": {
            "text": (
                "Memory: A rooftop at sunset, but the scene feels... hollow.\n"
                "Theo's words echo strangely, like a recording.\n"
                "'I got an offer... Neuro Lab... won't go without you...'\n"
                "But you can't remember his face clearly.\n"
                "The gemstone flickers weakly.\n"
                "Merchant: 'Some memories are wishes, dressed up as truth.'"
            ),
            "choices": {
                "1": {"text": "This never happened.", "emotion": "neutral", "next": "scene7"},
                "2": {"text": "I wanted this to be real.", "emotion": "empathy", "next": "scene7"},
                "3": {"text": "Why would I imagine this?", "emotion": "curiosity", "next": "scene7"},
                "4": {"text": "It feels so real though.", "emotion": "empathy", "next": "scene7"}
            }
        }
    },

    "scene7": {
        "default": {
            "text": (
                "Fifth Memory: A lab at night. Wires, screens, electrodes. The Cerebridge hums.\n"
                "The Merchant's face flickers — it is Theo.\n"
                "Theo: 'You built this. And you trapped us here.'\n"
                "The gemstone glows purple."
            ),
            "choices": {
                "1": {"text": "This is manipulation!", "emotion": "anger", "next": "final"},
                "2": {"text": "Why would I see your life as mine?", "emotion": "neutral", "next": "final"},
                "3": {"text": "The Cerebridge created resonance.", "emotion": "curiosity", "next": "final"},
                "4": {"text": "Theo… it was ours.", "emotion": "empathy", "next": "final"}
            }
        },
        "lab_revelation_true": {
            "text": (
                "Memory: A high-tech lab, the Cerebridge humming softly.\n"
                "Theo lies unconscious, connected to the machine.\n"
                "Your hands shake as you realize what you've done.\n"
                "The Merchant's face flickers — it is Theo, trapped in his own mind.\n"
                "The gemstone glows with painful purple light.\n"
                "Merchant: 'You built this prison. Now you must choose: free him or join him.'"
            ),
            "choices": {
                "1": {"text": "I have to save him.", "emotion": "empathy", "next": "final"},
                "2": {"text": "This was a mistake.", "emotion": "empathy", "next": "final"},
                "3": {"text": "How do I fix this?", "emotion": "curiosity", "next": "final"},
                "4": {"text": "I'll take his place.", "emotion": "empathy", "next": "final"}
            }
        },
        "lab_revelation_false": {
            "text": (
                "Memory: A lab that feels wrong, like a stage set.\n"
                "Theo's unconscious form looks artificial.\n"
                "The Merchant's face glitches — it's not Theo at all.\n"
                "This is all a simulation, a test.\n"
                "The gemstone glows with angry red light.\n"
                "Merchant: 'You're smarter than I thought. But the choice remains the same.'"
            ),
            "choices": {
                "1": {"text": "This is all fake.", "emotion": "anger", "next": "final"},
                "2": {"text": "What are you really testing?", "emotion": "curiosity", "next": "final"},
                "3": {"text": "I won't play your game.", "emotion": "neutral", "next": "final"},
                "4": {"text": "Show me the real Theo.", "emotion": "empathy", "next": "final"}
            }
        },
        "lab_revelation_shared": {
            "text": (
                "Memory: A lab where you and Theo work side by side.\n"
                "The Cerebridge hums with shared consciousness.\n"
                "You both chose this, to explore the depths of the mind together.\n"
                "The Merchant's face is both of you, merged.\n"
                "The gemstone glows with harmonious purple light.\n"
                "Merchant: 'You chose to share this journey. Now you must face its consequences.'"
            ),
            "choices": {
                "1": {"text": "We chose this together.", "emotion": "empathy", "next": "final"},
                "2": {"text": "We can find a way out.", "emotion": "curiosity", "next": "final"},
                "3": {"text": "This is what we wanted.", "emotion": "empathy", "next": "final"},
                "4": {"text": "We'll face this together.", "emotion": "empathy", "next": "final"}
            }
        }
    },

    "final": {
        "default": {
            "text": (
                "Final Choice: Theo lies before you, vulnerable and trusting.\n"
                "The Cerebridge pulses, waiting for your decision.\n"
                "Electrodes gleam in the dim light.\n"
                "You stand at the crossroads of your destiny.\n"
                "What will you choose?"
            ),
            "choices": {}
        }
    }
}

# Dynamic scene selection based on emotional state and previous choices
def select_scene_variation(scene_key, emotions, choice_history):
    """Select the appropriate scene variation based on emotional state and history"""
    variations = scene_variations.get(scene_key, {})
    
    if not variations:
        return None
    
    # Get dominant emotion
    a, e, c, n = emotions["anger"], emotions["empathy"], emotions["curiosity"], emotions["neutral"]
    dominant_emotion = max([("anger", a), ("empathy", e), ("curiosity", c), ("neutral", n)], key=lambda x: x[1])
    
    # Scene-specific selection logic
    if scene_key == "scene1":
        if a >= 2:
            return variations.get("aggressive", variations.get("default", list(variations.values())[0]))
        elif e >= 2:
            return variations.get("sympathetic", variations.get("default", list(variations.values())[0]))
        elif c >= 2:
            return variations.get("curious", variations.get("default", list(variations.values())[0]))
        else:
            return variations.get("default", list(variations.values())[0])
    
    elif scene_key == "scene2":
        # Check previous choice from scene1
        if choice_history and "scene1" in choice_history:
            last_choice = choice_history["scene1"]
            if "anger" in last_choice.lower() or emotions["anger"] >= 2:
                return variations.get("after_aggressive", variations.get("default", list(variations.values())[0]))
            elif "empathy" in last_choice.lower() or emotions["empathy"] >= 2:
                return variations.get("after_sympathetic", variations.get("default", list(variations.values())[0]))
        return variations.get("default", list(variations.values())[0])
    
    elif scene_key == "scene3":
        if e >= 3:
            return variations.get("mother_loving", variations.get("default", list(variations.values())[0]))
        elif a >= 2:
            return variations.get("mother_absent", variations.get("default", list(variations.values())[0]))
        else:
            return variations.get("mother_conflicted", variations.get("default", list(variations.values())[0]))
    
    elif scene_key == "scene4":
        if a >= 3:
            return variations.get("violence_regret", variations.get("default", list(variations.values())[0]))
        elif e >= 3:
            return variations.get("violence_heroic", variations.get("default", list(variations.values())[0]))
        else:
            return variations.get("violence_manipulated", variations.get("default", list(variations.values())[0]))
    
    elif scene_key == "scene5":
        if e >= 3:
            return variations.get("competition_friendly", variations.get("default", list(variations.values())[0]))
        elif a >= 3:
            return variations.get("competition_bitter", variations.get("default", list(variations.values())[0]))
        else:
            return variations.get("competition_manipulated", variations.get("default", list(variations.values())[0]))
    
    elif scene_key == "scene6":
        if e >= 3:
            return variations.get("partnership_true", variations.get("default", list(variations.values())[0]))
        elif a >= 3:
            return variations.get("partnership_manipulative", variations.get("default", list(variations.values())[0]))
        else:
            return variations.get("partnership_imagined", variations.get("default", list(variations.values())[0]))
    
    elif scene_key == "scene7":
        if e >= 3:
            return variations.get("lab_revelation_shared", variations.get("default", list(variations.values())[0]))
        elif a >= 3:
            return variations.get("lab_revelation_false", variations.get("default", list(variations.values())[0]))
        else:
            return variations.get("lab_revelation_true", variations.get("default", list(variations.values())[0]))
    
    # Fallback to first available variation
    return variations.get("default", list(variations.values())[0] if variations else None)

# Legacy scenes dict for backward compatibility
scenes = {
    "scene1": scene_variations["scene1"]["default"],
    "scene2": scene_variations["scene2"]["default"],
    "scene3": scene_variations["scene3"]["mother_loving"],
    "scene4": scene_variations["scene4"]["violence_heroic"],
    "scene5": scene_variations["scene5"]["competition_friendly"],
    "scene6": scene_variations["scene6"]["partnership_true"],
    "scene7": scene_variations["scene7"]["lab_revelation_true"],
    "final": scene_variations["final"]["default"]
}
