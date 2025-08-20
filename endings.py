# endings.py
# Cinematic endings and evaluation logic (dominance, balance, secret path).

ENDINGS = {
    "CORRUPTION": {
        "title": "Corruption",
        "summary": "You seize control. The machine seizes you.",
        "epilogue": (
            "You strap Theo in before he can wake. The Cerebridge purrs, then roars.\n"
            "His memories open like wounds; you dig your hands into them. Power tastes like truth—\n"
            "hot, metallic, endless. The shop rematerializes around you: sawdust, scroll, black gems.\n"
            "You laugh, and the laugh echoes wrong. The sign above the door reads 'Memories'.\n"
            "You polish the counter. You wait for the next poor soul to wake.\n"
            "Congratulations, Merchant."
        )
    },
    "SACRIFICE": {
        "title": "Sacrifice",
        "summary": "You save Theo by choosing to stay behind.",
        "epilogue": (
            "You slide the Cerebridge onto yourself instead and yank the failsafe loose.\n"
            "'Live,' you whisper, and the machine takes you at your word.\n"
            "Theo jolts awake on the lab floor, coughing. 'Alaric?' Only silence answers.\n"
            "In the shop-that-is-your-mind, the lights dim to a warm dusk. There is no counter now,\n"
            "no merchant—just a chair by the door and a memory that doesn’t hurt as much as it used to.\n"
            "Outside, real rain begins. Theo stands, alive. You are the cost."
        )
    },
    "OBLIVION": {
        "title": "Oblivion",
        "summary": "Curiosity untethered becomes an abyss.",
        "epilogue": (
            "You don’t strap anyone in. You open everything.\n"
            "Logs, traces, dreams, half-born thoughts—your own, Theo’s, the machine’s.\n"
            "Patterns bloom faster than breath. Your name fractures into equations.\n"
            "When Theo wakes, he finds only clean hardware and a note:\n"
            "'There is a door in the mind. I kept walking.'\n"
            "The shop remains, but without walls. The scroll shows constellations no one can name."
        )
    },
    "HOLLOW": {
        "title": "Hollow",
        "summary": "You escape intact, but leave yourself behind.",
        "epilogue": (
            "You power everything down. No straps. No speeches. No goodbyes.\n"
            "You and Theo walk out under the humming lab lights, promising audits and protocols.\n"
            "Weeks later, a stranger stares back from mirrors. Laughter sounds overdubbed.\n"
            "Your inbox says 'Alaric'; your chest says nothing at all.\n"
            "Sometimes, passing a dusty pawnshop, you swear a jagged sign used to say 'Memories'."
        )
    },
    "TRUE": {
        "title": "True Redemption",
        "summary": "Balanced emotion; you choose presence over power.",
        "epilogue": (
            "You kneel beside Theo and let the Cerebridge keep humming without you.\n"
            "'I almost did it again,' you admit. 'I almost turned you into proof.'\n"
            "He opens one eye. 'You didn’t.'\n"
            "You both sit there, listening to the machine breathe like a distant sea.\n"
            "In the shop, the scroll is finally blank—and peaceful. The gems are gone. So is the merchant.\n"
            "When you wake, it is morning. Outside, the world is ordinary. It’s perfect."
        )
    },
    "REUNION_SECRET": {
        "title": "Secret Reunion",
        "summary": "You and Theo co-author the mind—no captor, no captive.",
        "epilogue": (
            "You roll your chair to his and place the electrodes on the desk between you.\n"
            "'Together or never,' you say. Theo smiles, tired and luminous. 'Together.'\n"
            "You don’t enter each other—you design the boundary. You build the rules you wish you’d had.\n"
            "In the shop, the door opens to daylight for the first time. A bell rings. No one is trapped.\n"
            "Later, the paper titles your paper: 'Cerebridge: A Consent-First Architecture.'\n"
            "For once, the headline got it right."
        )
    }
}

def is_balanced(emotions, spread_max=1, min_each=2):
    """Tight balance: every emotion >= min_each and (max-min) <= spread_max."""
    vals = list(emotions.values())
    return min(vals) >= min_each and (max(vals) - min(vals)) <= spread_max

def secret_reunion_unlocked(emotions):
    """
    Secret ending: tight balance PLUS a humane tilt.
    Conditions:
      - curiosity >= 3 and empathy >= 3
      - anger in [1..3], neutral in [1..3]  (not zero, not dominant)
    """
    return (
        emotions.get("curiosity", 0) >= 3 and
        emotions.get("empathy", 0) >= 3 and
        1 <= emotions.get("anger", 0) <= 3 and
        1 <= emotions.get("neutral", 0) <= 3
    )

def get_ending(emotions):
    """
    Order of evaluation:
      1) Dominance (>= 60% of total or hard cap >= 6) → extreme endings
      2) Secret Reunion → tight balance + humane tilt
      3) True Ending → tight balance
      4) Otherwise → lean to nearest extreme by dominance
    """
    total = sum(emotions.values())
    if total == 0:
        return ENDINGS["HOLLOW"]  # empty run → empty self

    dominant = max(emotions, key=emotions.get)
    max_val = emotions[dominant]
    hard_cap = 6
    dominance = (max_val / total >= 0.60) or (max_val >= hard_cap)

    if dominance:
        if dominant == "anger":
            return ENDINGS["CORRUPTION"]
        if dominant == "empathy":
            return ENDINGS["SACRIFICE"]
        if dominant == "curiosity":
            return ENDINGS["OBLIVION"]
        if dominant == "neutral":
            return ENDINGS["HOLLOW"]

    if is_balanced(emotions, spread_max=1, min_each=2) and secret_reunion_unlocked(emotions):
        return ENDINGS["REUNION_SECRET"]

    if is_balanced(emotions, spread_max=1, min_each=2):
        return ENDINGS["TRUE"]

    if dominant == "anger":
        return ENDINGS["CORRUPTION"]
    if dominant == "empathy":
        return ENDINGS["SACRIFICE"]
    if dominant == "curiosity":
        return ENDINGS["OBLIVION"]
    return ENDINGS["HOLLOW"]
