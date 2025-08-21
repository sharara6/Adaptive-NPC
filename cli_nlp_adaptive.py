#!/usr/bin/env python3
# cli_memory_merchant_modified.py
# Modified per user request:
# - Sentiment analysis results are NOT printed to terminal
# - Emotion tags (square brackets and parenthetical tags) are stripped from displayed choice texts
# - Server sentiment labels expected: "positive", "negative", "neutral"
# - Added simple ending logic: accumulating positive or negative choices will force good/bad endings

import requests, time, sys, re

SENTIMENT_URL = "http://localhost:8000/classify"
AI_URL = "http://localhost:8001/ai_response"
TIMEOUT = 15

state = {
    "mood": 0,
    "true_memories": 0,
    "false_memories": 0,
    "chapter": 1,
    "lost_fingers": 0,
    "history": [],  # stores dicts: {player_text, sentiment, ai_text}
    # new counters for endings
    "neg_count": 0,
    "pos_count": 0,
    "neu_count": 0,
    # dialogue tracking
    "current_scene": None,
    "scene_history": [],  # track which scenes player has been through
}

# thresholds (tweak these to change how many positive/negative responses trigger endings)
NEGATIVE_THRESHOLD = 2  # Lower threshold for faster endings
POSITIVE_THRESHOLD = 2  # Lower threshold for faster endings
NEUTRAL_THRESHOLD = 4  # If player is mostly neutral, different ending


def call_sentiment(text):
    try:
        r = requests.post(SENTIMENT_URL, json={"text": text}, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        # Do not spam terminal with sentiment details per user request
        return None


def call_ai(text, sentiment=None, history=None, scene=None, choice_label=None):
    payload = {"text": text}
    if sentiment is not None:
        payload["sentiment"] = sentiment
    if history is not None:
        payload["history"] = history
    if scene is not None:
        payload["scene"] = scene
    if choice_label is not None:
        payload["player_choice"] = choice_label
    try:
        r = requests.post(AI_URL, json=payload, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[!] AI error: {e}")
        return None


def wait_for_advance():
    """
    Wait for user to press Enter (or type something then Enter).
    """
    try:
        input()
    except EOFError:
        # In some environments EOF may happen; ignore to not crash.
        pass


def slow_print(lines, paging=True, delay=0.25):
    """
    Print lines one-by-one. If paging is True, wait for Enter between lines.
    If paging is False, print with a small delay (legacy behavior).
    Skips blank lines automatically.
    """
    if paging:
        for ln in lines:
            if ln.strip() == "":
                # skip blank lines silently
                continue
            print(ln)
            wait_for_advance()
    else:
        for ln in lines:
            if ln.strip() == "":
                continue
            print(ln)
            time.sleep(delay)


# ---------- Your SCENES dict (unchanged) ----------
SCENES = {
    "start": {
        "narration": [
            "M: Finally awake, huh?",
            "P:",
            "  1. Remain silent",
            "  2. Who are you?",
            "  3. What happened?",
            "  4. Is this… a dream?",
        ],
        "choices": [
            {
                "label": "Remain silent",
                "text": "Remain silent",
                "next": "what_do_you_want",
            },
            {
                "label": "Who are you?",
                "text": "Who are you?",
                "next": "what_do_you_want",
            },
            {
                "label": "What happened?",
                "text": "What happened?",
                "next": "what_do_you_want",
            },
            {
                "label": "Is this… a dream?",
                "text": "Is this a dream?",
                "next": "what_do_you_want",
            },
        ],
    },
    "what_do_you_want": {
        "narration": [
            "P: what do you want from me?",
            "M: Well, not the time for chitchat. meet me at the shop. *Leaves the room*",
            "P: (inner dialogue) What is this place? Who was that guy?",
            "P: Wait... Who even am I?",
            "P: I should probably follow my only current lead.",
            "Narration: It's raining outside, tight alleyways dimly lit by the moon, nobody to be found.",
            "Narration: You see a light not so far away. You decide to head for it",
            'Narration: Under the light hangs a sign. Jagged, chipped, worn down, barely reads "Memories"',
            "Narration: You feel uneasy, but decide to go in anyways. You will do anything to remember... Remember it all.",
            "Narration: The shop reeks of sawdust, tiny place with a counter and many gemstones.",
            "Narration: The merchant appears before you seemingly out of nowhere, Eyes staring into yours. You decide to break the tension",
            "P: I came here as you requested. Now answer my questions.",
        ],
        "choices": [
            {
                "label": "Say that line (continue)",
                "text": "I came here as you requested. Now answer my questions.",
                "next": "merchant_scroll",
            }
        ],
    },
    "merchant_scroll": {
        "narration": [
            "M: Hasty, are we? (chuckles) I needn't answer you myself… Take a look at this:",
            "Narration: The merchant shows you a scroll with many black dim gemstones scattered inside it. Random at first, but taking a shape the more you stare into it.",
            "M: (whispers) Don't lose yourself now.",
            "Narration: you snap back and look at the merchant.",
            "P: What was that?",
        ],
        "choices": [
            {
                "label": "What was that? (continue)",
                "text": "What was that?",
                "next": "first_memory",
            }
        ],
    },
    "first_memory": {
        "narration": [
            "M: Full of questions you are. Here, you will like this.",
            "Narration: The merchant takes out one of the gems on the scroll and hands it to you.",
            "M: Hold onto it tight and close your eyes...",
            "Narration: The merchant closes your grip onto the gemstone while closing your eye lids with his other hand",
            "Narration: You don't feel the urge to resist. It is pleasant.",
            "Narration: You are suddenly teleported into this alternate reality.",
            "Narration: You are in a warm house, sunlight spilled through the kitchen's window as soft beams filtered through the glass, casting a gentle glow.",
            "Narration: you see a woman cooking. She kneels down; food is almost done.",
            'Narration: with a lovely smile she says "hey, dear Alaric" while patting your head.',
            "Narration: You snap back to the rotten shop. The old merchant in front of you, staring you in the eyes.",
            "Narration: You get creeped out and take a strong step back.",
            "Narration: the black gemstone in your hand is now glowing with a pink color.",
            "M: Oh, and that's how you react. (pitiful laughter making fun of you)",
            "M: (whispers) Do you want more?",
            "P:",
        ],
        "choices": [
            {
                "label": "Yes. I need to remember—whatever it costs. (Vulnerable, curious)",
                "text": "Yes. I need to remember—whatever it costs.",
                "next": "after_first_memory",
            },
            {
                "label": "You think I’m scared? Bring it on. (Anger)",
                "text": "You think I’m scared? Bring it on.",
                "next": "after_first_memory",
            },
            {
                "label": "How do I know any of this is real? (Cautious)",
                "text": "How do I know any of this is real?",
                "next": "after_first_memory",
            },
            {
                "label": "And what if these memories aren’t even mine? (Paranoid)",
                "text": "And what if these memories aren't even mine?",
                "next": "after_first_memory",
            },
            {
                "label": "Why would I want more? (Cold, neutral)",
                "text": "Why would I want more?",
                "next": "after_first_memory",
            },
        ],
    },
    "after_first_memory": {
        "narration": [
            "M: That's you, and that's your mother. and that pink gemstone is love, your pure mother's love.",
            "M: First one's on the house.",
            "P: (to himself) Considering that this swine is to be trusted, I at least know now my name.",
            "P: I need to know more. I have to make him show me all my memories",
            "M: Spaced out? Guess that was too much (laugh)",
            "Narration: You feel aggravated, challenged",
            "P: Not at all, show me more of your tricks.",
            "M: Oh, but nothing is free in this world dear.",
            "M: For each memory you wish to see, you must sacrifice a part of your body.",
            "P: Whatever do you mean by that?",
            "M: It's simple. Once you go in and come back out, you'll be missing a finger or two (chuckles) until you lose all of yourself.",
        ],
        "choices": [
            {
                "label": "If that’s the price… then take what you must. (Vulnerable, curious)",
                "text": "If that’s the price… then take what you must.",
                "next": "gem2",
            },
            {
                "label": "Touch me and I break your damn shop. (Anger)",
                "text": "Touch me and I break your damn shop.",
                "next": "gem2",
            },
            {
                "label": "There’s a workaround, isn’t there? I’ll find it. (Cautious)",
                "text": "There’s a workaround, isn’t there? I’ll find it.",
                "next": "gem2",
            },
            {
                "label": "I don’t like this… but I need answers. (Paranoid)",
                "text": "I don’t like this… but I need answers.",
                "next": "gem2",
            },
            {
                "label": "Fine, I will play your little game. (Cold, neutral)",
                "text": "Fine, I will play your little game.",
                "next": "gem2",
            },
        ],
    },
    "gem2": {
        "narration": [
            "Narration: The merchant pulls out another black gemstone from the scroll. Putting it in your hands.",
            "Narration: you wonder which emotion you will experience now.",
            "Narration: Before the merchant closes your grip or eyes, you do it yourself. You know the game now.",
            "M: (voice fading away) ... This one... goes deeper.",
            "Narration: You get teleported to another place. Same House as the first memory. But it feels different.",
            "Narration: you are sitting on the floor of the living room next to a red headed boy who looks like he is the same age as you. you are surrounded by scattered toy pieces and half-built inventions—batteries, plastic gears, you are holding a screwdriver slightly big for your hands, and you both are laughing softly.",
            "Narration: Then, it started.",
            "Narration: Muffled at first—a sharp voice breaking the quiet, then another voice rising to meet it.",
            "Narration: You hear your mother and a man argue. The words blurred into something jagged and fast.",
            "Narration: your friend froze, mid-motion, He glanced at you, instinctively, with concerned looks not knowing what to do, but you were quiet as a dear, you didn’t flinch. Didn’t speak, like it was no surprise, you are used to it, your eyes fix at your hand as you twist the screwdriver too tightly.",
            "Narration: your friend was about to say something, asking if you were okay but he's interrupted by a striking sound, a slap followed by screams from your mother.",
            "Narration: you get up instantly, anger building up inside you, you don't have control over your body, like you're watching a movie.",
            "Narration: you run upstairs only to find the man approaching your mother again while she screams, and without thinking, you lunge at the man and stab him with the screwdriver you realize you were still holding. your mother screams and so do you.",
            "Narration: Looking at your mother to apologize, you see your friend standing at the door, he has seen it all.",
            "Narration: You feel uneasy, panicking, you drop the screwdriver on the floor, somehow you are relieved to have saved your mother, she does not react, and your friend is staring at the man.",
            "Narration: The cops instantly come in, abnormally too quick of a response time. You were about to speak until your friend instantly takes the blame for you, holding the screwdriver, he is Claiming that he did it.",
            'Narration: your eyes met his and he smiles, reassuringly whispering "it\'s okay"',
            "Narration: You snap back to the shop, The smell doesn't bother you anymore, you're used to it. the gemstone glows with a blue light in your hand.",
            "P: What did you just show me? who is this boy, and I would never hurt someone.",
        ],
        "choices": [
            {
                "label": "He saved me… That means something. (compassion)",
                "text": "He saved me… That means something.",
                "next": "after_gem2",
            },
            {
                "label": "He shouldn't have made such a sacrifice. (anger, guilt)",
                "text": "He shouldn't have made such a sacrifice.",
                "next": "after_gem2",
            },
            {
                "label": "It's irrelevant. (neutral)",
                "text": "It's irrelevant.",
                "next": "after_gem2",
            },
        ],
    },
    "after_gem2": {
        "narration": [
            "M: this was your childhood best friend, you have caused him a great harm.",
            "P: but why? why did this happen?",
            "M: those questions are not important now; the past is already long gone. the important question is what are you going to do about it now?",
            "P: is there really anything I can do about it? I don't even know where am I.",
            "M: don't be so impulsive, pay close attention to the details and you might know your answers soon enough.",
            "P: (to himself) apparently, the colors of the gemstones are based on emotions, the first one was love, this one must be sadness, maybe if I had more focus, I might be able to know the emotion before the memory ends, and I might know how to influence it.",
            "P: okay, give me the next memory.",
            "M: Shall we proceed?",
            "P: We shall...",
        ],
        "choices": [{"label": "Proceed (continue)", "text": "Proceed", "next": "gem3"}],
    },
    "gem3": {
        "narration": [
            "Narration: The air grows thicker. The candlelight in the shop flickers violently, though there's no wind. The gemstones on the scroll seem to shimmer with anticipation—as if alive.",
            "M: Brave. Or foolish. Hard to tell with your kind.",
            "Narration: The merchant extends a hand, slower this time. As if testing the boundaries of your strange new agreement. You reach out, and he places a third gem into your palm.",
            "Narration: you notice you are missing finger, but you are not surprised, you agreed on this game's rules.",
            "Narration: Without a word, you close your hand and shut your eyes. and the world turns inside out.",
            "Narration: it is hot, you're sweating, standing before a board hanging on a wall in a school hall, papers pinned to that board in that familiar, slightly crumpled grid.",
            "Narration: you are surrounded by some high school kids—seemingly your classmates, around the wall, pointing, groaning, cheering.",
            "Narration: you notice an orbit of students clustered around someone. Laughing, talking, voices overlapping as if everyone was trying to be heard just a little more clearly by the one in the center. that boy was the only who didn't rush to see the list, like he had expected it already, that his name would be on the top.",
            "Narration: He walked up calmly, hands in his sweaters' pockets, scanned the list with a faint smirk that said of course, and nodded once, more to himself than anyone else. People clapped him on the back. And the circle of admiration closed around him once again.",
            'Narration: Your hands are damp, as you move your index finger on the paper. You read the same sentence on the headline again "the test results", Your heartbeat was loud—too loud—like it might give you away.',
            "Narration: you are searching for your name.",
            "Narration: you take a deep breath, lifting your eyes up again to see that dark haired boy smiling like it didn’t even matter. And maybe it didn’t—to him. But you feel anxious like it meant a great deal to you.",
            'Narration: you slide your eyes back to the paper, they immediately behold the name next to the second place "Theo Shaw" your stomach gave that quiet, familiar drop—not quite disappointment, not quite surprise. Just the same dull ache of being almost, again.',
            "Narration: The paper shifts in your hands... no—melts. The ink begins to run.",
            "Narration: The hallway flickers. That boy’s face—smile still frozen—begins to blur, smudged like a watercolor in the rain. and suddenly you are back into the shop.",
            "Narration: you look at the merchant, and for the first time you take in his red hair that is now glitching, his expressions are unreadable. and the gemstone in your hand now has a yellow glow to it, you wonder which emotion have you witnessed.",
            "P: (to himself) This doesn't feel right. it doesn't look real. That merchant scammed me.",
        ],
        "choices": [
            {
                "label": "You tricked me! This isn’t my memory! (Anger)",
                "text": "You tricked me! This isn’t my memory!",
                "next": "reaction_glitch",
            },
            {
                "label": "That name… Theo… why does it sound familiar? (Curiosity)",
                "text": "That name… Theo… why does it sound familiar?",
                "next": "reaction_glitch",
            },
            {
                "label": "Wait... am I even Alaric? (Doubt)",
                "text": "Wait... am I even Alaric?",
                "next": "reaction_glitch",
            },
            {
                "label": "This isn't my memory. my name is not Theo. (Cold)",
                "text": "This isn't my memory. my name is not Theo.",
                "next": "reaction_glitch",
            },
        ],
    },
    "reaction_glitch": {
        "narration": [
            "Narration: The merchant goes to pick out another gemstone only to find his index finger missing.",
            "Narration: The merchant gets surprised and scared.",
            "Narration: Based on the previous choices ...",
        ],
        "choices": [
            {
                "label": "Now, give me another one.",
                "text": "Now, give me another one.",
                "next": "gem4",
            }
        ],
    },
    "gem4": {
        "narration": [
            "Narration: The merchant mumbling to himself, gets out the fourth gemstone and hands it to you.",
            "Narration: You grip it and close your eyes.",
            "Narration: The city lights glow. you are sitting with someone side by side, robes half-off, diplomas at your side. A quiet university rooftop at dusk. The graduation ceremony has just ended. you feel heavy, you have no idea what you're going to do now with your life.",
            'Narration: the person sitting next to you is staring at the skyline and trying to start a conversation: "Hard to believe, huh? That it’s over."',
            'Narration: you are half-smiling and you say casually: "You mean this part. Knowing you, it’s never really over. Just a new beginning."',
            'Narration: he smiles back, move his hand through the waves of his dark hair: "Damn right. And this beginning… it’s big." then he pauses, glances sideways at you with a flash of determination in his eyes: "A Neuro Lab reached out. Full access to their neural interface research. Cutting-edge hardware. Autonomy. They want me to lead a new sub-division."',
            'Narration: you feel quietly surprised: "Of course they do. You were always first in line."',
            'Narration: he ignores the tone replying: "I told them I won’t take it unless you come with me. As my partner."',
            'Narration: you turn to him, stunned: "What?" and he answers: "Lab partner. Co-lead. We build it together—whatever “it” becomes. You and me. Like it’s always been."',
            'Narration: a weird feeling slips into your heart, you say softly: "Alaric, you don’t need me for that. You never did."',
            'Narration: Alaric is suddenly serious: "That’s where you’re wrong. I’ve got the vision, sure. But you see the things I miss. The patterns, the ethical pitfalls, the consequences. I push forward. You anchor me. We’re not balanced without each other."',
            "Narration: ... (summarized) ... you are transported back to the old shop; you are frustrated now. and the gemstone glows in a sharp green color.",
            "P: this isn’t real, how am I witnessing a memory that I’m also talking to me in? this can't be me memory either. and I still can't decode the emotions or the ideas behind them",
        ],
        "choices": [
            {
                "label": "Am I… watching myself? (Confusion)",
                "text": "Am I watching myself?",
                "next": "lab_memory",
            },
            {
                "label": "None of this adds up! (Anger)",
                "text": "None of this adds up!",
                "next": "lab_memory",
            },
            {
                "label": "Even if it’s not mine… maybe it still matters. (Curiosity)",
                "text": "Even if it’s not mine… maybe it still matters.",
                "next": "lab_memory",
            },
            {
                "label": "Then who am I if none of this is mine? (Doubt)",
                "text": "Then who am I if none of this is mine?",
                "next": "lab_memory",
            },
        ],
    },
    "lab_memory": {
        "narration": [
            "M: I don't know what's wrong, you are right, this is not your memory, this is Theo's memory.",
            "P: who is Theo?",
            "M: Memories are the architects of our identity. you know Theo just like you know yourself. he is a part of you.",
            "(these aren’t choices, these are scene continuation lines)",
            "Based on the previous choices ...",
            "P: what about the gem colors, why do they keep changing?",
            "M: Emotions are the colors of the soul, and you have lost your soul, Alaric.",
            "M: you should try to get it back, Hold onto your memories and your emotions. the stronger emotions are the ones that affect you the most and you can affect them as well.",
            "M: this memory held the joy, the excitement of accepting a friend's offer. it may not be your memory, but it certainly gave you something to learn.",
            "(these aren’t choices, these are scene continuation lines)",
            "Based on the previous choices ...",
        ],
        "choices": [
            {
                "label": "I can't tolerate any more false memories, give me a right one.",
                "text": "I can't tolerate any more false memories, give me a right one.",
                "next": "gem5",
            },
            {
                "label": "Stop speaking in riddles. I want facts.",
                "text": "Stop speaking in riddles. I want facts.",
                "next": "gem5",
            },
            {
                "label": "Then I’ll find every color, and reclaim what I was.",
                "text": "Then I’ll find every color, and reclaim what I was.",
                "next": "gem5",
            },
            {
                "label": "Or maybe you're just assigning color to keep me guessing.",
                "text": "Or maybe you're just assigning color to keep me guessing.",
                "next": "gem5",
            },
        ],
    },
    "gem5": {
        "narration": [
            "M: here, take this.",
            "Narration: he takes out the fifth gemstone and place it in your hand, you notice his hand missing another finger, but he doesn't seem to care. the gemstone now feels warm against your palm.",
            "(these aren’t choices, these are scene continuation lines)",
            "Narration: The shop starts to shift—walls stretch, the counter melts into the floor, and the merchant’s form flickers, and you find yourself in a different place.",
            "Narration: you find yourself in a lab, silent as you hear your footsteps, you are restless, walking back and forth. it is late night, Rain tapping against the high lab windows...",
            "Narration: In the center: The device, Glowing. finally ready, finally alive.",
            'Narration: you stare at it and whisper: "The Cerebridge."',
            "Narration: ... (long lab sequence omitted for brevity in print) ...",
            "Narration: you open your eyes and suddenly you are in the shop again, the gemstone glows with a purple color, you look at the merchant again and now you know, the merchant is Theo.",
            "P: it's you! you are him! you are a part of my past! i saw you!",
        ],
        "choices": [
            {
                "label": "This is manipulation. You’ve been twisting my mind! (Anger)",
                "text": "This is manipulation. You’ve been twisting my mind!",
                "next": "final_branch",
            },
            {
                "label": "How can that be? Why would I see your life like it’s mine? (Confusion)",
                "text": "How can that be? Why would I see your life like it’s mine?",
                "next": "final_branch",
            },
            {
                "label": "So, the Cerebridge created cross-memory resonance... (Cold, neutral)",
                "text": "So, the Cerebridge created cross-memory resonance...",
                "next": "final_branch",
            },
            {
                "label": "Theo... I remember now. It wasn’t just your life. It was ours. (Empathy)",
                "text": "Theo... I remember now. It wasn’t just your life. It was ours.",
                "next": "final_branch",
            },
        ],
    },
    "final_branch": {
        "narration": [
            "P: but how is this possible? how did I have access to your memories as well as mine?",
            "M: you know the answer to that, you invented it yourself.",
            "P: (to himself) the cerebridge device…",
            "P: I am in your head!",
            "M: you're close enough. you were in my head, but now i am in yours.",
            "P: I don't believe you. I can't believe you.",
            "M: Then go. Find one more. Let the truth carve what’s left of you.",
            "Narration: You stare down at your hands. They tremble. One more gem sits before you, unclaimed. Unlike the others, it glows before you touch it. the merchant's fingers came back as he handles you the last gemstone.",
            "P (to himself) One more... and I either find who I am—or lose it all.",
            "Narration: You pick it up. And for the first time—you don’t close your eyes.",
            "Narration: ... (final lab / Cerebridge sequence) ...",
            "Narration: You jolt back into the shop, gasping. But something is wrong. The shop is different—brighter. No sawdust. The gemstones are gone. Only the scroll remains, and it’s... blank.",
            "M: (calmly) You reached the boundary.",
            "P: What boundary",
            "M: Between remembering... and becoming.",
            "P: Becoming what",
            "M: A fragment. A story. A soul trapped in recollection.",
            "P: This isn't memory... it's madness.",
            "M: Memory is madness, if seen too clearly. That's why we forget.",
            "P: I won't accept this memory, i have to go back.",
            "Narration: you press the same gemstone in your hand strongly, it is glowing bright red, you figure out that this is your core memory, your most strong emotion... regret.",
            "Narration: you know what to do now.",
        ],
        "choices": [
            {
                "label": "Vulnerability (proceed)",
                "text": "Because it hurt too much.",
                "next": "end_vulnerable",
            },
            {
                "label": "Anger, guilt (game over)",
                "text": "Because I had to move on.",
                "next": "end_gameover",
            },
            {
                "label": "Cold, neutral (proceed)",
                "text": "I didn’t think it mattered.",
                "next": "end_vulnerable",
            },
            {
                "label": "Empathy (game over)",
                "text": "I didn't want to abandon my invention.",
                "next": "end_gameover",
            },
        ],
    },
    "end_vulnerable": {
        "narration": [
            "Narration: The shop begins to transform around you. The sawdust scent fades, replaced by something warmer—like morning coffee and old books.",
            "M: (voice growing softer) You understand now, don't you? The weight you've been carrying...",
            "P: I... I remember everything. The accident, the guilt, how I blamed myself for what happened to you.",
            "Narration: The merchant's face becomes clearer—younger, kinder. The red hair catches light that shouldn't exist in this dim place.",
            "M: It isn’t.",
            "Narration: The gemstones on the scroll begin to glow with warm, golden light—not the harsh colors of before.",
            "P: Theo... I'm so sorry. I should have been there. I should have saved you.",
            "M: You did save me. Every day you carried my memory, you kept me alive. But now... now you need to let yourself live too.",
            "Narration: The shop's walls grow transparent, showing glimpses of the real lab beyond—warm light, the steady beep of machines, the smell of antiseptic and hope.",
            "M: The Cerebridge... it was always meant to help people. To heal, not to trap. Remember that.",
            "Narration: The merchant extends his hand, no longer missing fingers. His smile is genuine, peaceful.",
            "M: Thank you for letting me go. And more importantly... thank you for letting yourself go too.",
            "Narration: The shop dissolves like morning mist. You feel yourself falling upward, toward consciousness, toward forgiveness.",
            "Narration: You wake in the lab chair, tears on your cheeks. Beside you, monitors show stable readings. On the screen: 'Memory Integration Complete - Subject Responsive.'",
            "Narration: Through the lab window, dawn is breaking. For the first time in years, it doesn't hurt to remember.",
            "Narration: REDEMPTION ENDING - Your compassion and vulnerability allowed you to forgive yourself and honor Theo's memory in a healthy way.",
        ],
        "choices": [],
    },
    "end_gameover": {
        "narration": [
            "Narration: The shop's temperature plummets. Your breath forms ice crystals as the merchant's laughter grows deeper, more primal.",
            "M: (voice twisting with malice) Oh, how delicious! Your anger feeds me so well. Each bitter thought, each hateful word—pure sustenance.",
            "Narration: The gemstones on the scroll begin to crack, leaking dark, viscous fluid that stains everything it touches.",
            "P: What's happening? This isn't what I wanted!",
            "M: Isn't it? You chose rage over understanding, hatred over healing. This is exactly what you wanted—to punish, to blame, to hurt.",
            "Narration: The merchant's form grows larger, more grotesque. His missing fingers regenerate as twisted claws.",
            "M: You see, dear Alaric, every soul that enters my shop with such beautiful anger becomes part of my collection.",
            "Narration: The walls close in. The sawdust beneath your feet turns to ash, then to something that writhes and whispers.",
            "P: No! I want to leave! I want to go back!",
            "M: There is no back. There is only here, and now, and forever. You are the newest merchant in my chain of shops.",
            "Narration: Your hands begin to fade, becoming translucent. You feel your memories being catalogued, filed away like inventory.",
            "M: Welcome to eternity, my angry friend. The next customer will be here soon. You'll know what to do.",
            "Narration: The shop door opens with a rusty chime. Someone stumbles in—confused, lost, desperate for answers.",
            "Narration: You open your mouth to speak, but the words that come out are not your own: 'Finally awake, huh?'",
            "Narration: CORRUPTION ENDING - Your anger and hatred have transformed you into the very evil you sought to escape.",
        ],
        "choices": [],
    },
    "end_neutral": {
        "narration": [
            "Narration: The shop becomes eerily quiet. Even the merchant seems to lose interest, his movements becoming mechanical.",
            "M: (voice flat, dispassionate) How... disappointing. You feel nothing. Learn nothing. Want nothing.",
            "P: I just want answers. Simple answers.",
            "M: Simple? There is nothing simple about the soul, yet you treat it like a mathematical equation.",
            "Narration: The gemstones on the scroll lose their luster, becoming dull gray stones—ordinary, unremarkable.",
            "M: You came seeking memories, but you refuse to truly experience them. You want the story without the emotion.",
            "P: What's wrong with that? Emotions just complicate things.",
            "M: Everything. Everything is wrong with that. Memories without emotion are just data. And data... data is nothing.",
            "Narration: The shop begins to fade, not dramatically, but slowly—like a photograph left in sunlight too long.",
            "M: You will return to your lab. You will remember this as a strange dream. You will continue your research.",
            "Narration: The merchant's form becomes translucent, uninterested in your fate.",
            "M: But you will never truly live. Never truly feel. You've chosen the safety of numbness over the risk of meaning.",
            "Narration: You wake up in the lab, but something is wrong. Colors seem muted. Food tastes bland. Nothing seems to matter much.",
            "Narration: Your research continues, but you can't remember why it once felt important. Colleagues notice your distant stare.",
            "Narration: Years pass. You achieve professional success but personal emptiness. You've forgotten how to feel.",
            "Narration: HOLLOW ENDING - Your emotional detachment has left you technically alive but spiritually vacant.",
        ],
        "choices": [],
    },
    "end_early_negative": {
        "narration": [
            "Narration: The shop suddenly feels alive, pulsing with malevolent energy. The floorboards creak like hungry mouths.",
            "M: (grinning wickedly) Ah, such beautiful hostility! You've given me exactly what I needed, and so quickly too.",
            "P: What are you talking about? I just want my memories back!",
            "M: Your memories? Oh, sweet child, you misunderstand. This was never about giving. This was about taking.",
            "Narration: The gemstones on the scroll begin to glow with an ominous red light, pulsing in rhythm with your heartbeat.",
            "M: Every word of anger, every flash of rage—you've been feeding me your vital essence without even realizing it.",
            "Narration: You try to move but find your feet rooted to the floor. The sawdust has turned into grasping tendrils.",
            "P: This is impossible! Let me go!",
            "M: The beauty of quick anger is its intensity. Like a concentrated dose of the soul's darkest wine.",
            "Narration: The merchant's appearance shifts—his missing fingers multiply into dozens of writhing appendages.",
            "M: Your rage will sustain me for months. And when it's depleted, I'll simply wait for the next angry soul to stumble in.",
            "Narration: The walls pulse with veiny networks of energy, and you realize they're not walls—they're the inside of something vast and hungry.",
            "M: Thank you for the meal, Alaric. Your hatred was delicious.",
            "Narration: Consciousness fades as your essence is drawn into the shop itself. Somewhere, another confused soul awakens.",
            "Narration: DEVOURED ENDING - Your immediate hostility made you easy prey for an ancient predator.",
        ],
        "choices": [],
    },
    "end_early_positive": {
        "narration": [
            "Narration: The shop transforms around you, becoming brighter and cleaner. The oppressive atmosphere lifts like morning fog.",
            "M: (voice trembling with surprise) You... you see through it. So quickly. How?",
            "P: Your pain. I can see it behind the theatrics. You're not a merchant—you're a prisoner too.",
            "Narration: The false gemstones crumble to dust, revealing simple river stones underneath. The scroll shows children's drawings.",
            "M: (breaking down) I've been trapped here so long. Playing this role, feeding on others' pain to sustain myself.",
            "P: What happened to you? What made you become this?",
            "M: The same thing that happened to you. Guilt. Regret. The inability to forgive myself for failing someone I loved.",
            "Narration: The merchant's form wavers, revealing a young man with kind eyes—tired, scared, but fundamentally good.",
            "M: I was the first to use the Cerebridge improperly. I became lost in the guilt loop, and something else took over.",
            "P: But kindness... kindness breaks the cycle, doesn't it?",
            "M: (nodding through tears) Your compassion reminded me who I used to be. Who I still could be.",
            "Narration: The shop dissolves completely, replaced by two simple chairs in an endless, peaceful space.",
            "M: We can leave together. Both of us. The real world is still there, waiting.",
            "Narration: You take his hand and step forward into light—not the harsh light of the lab, but the warm light of dawn.",
            "Narration: You wake in the real lab to find monitors showing 'Connection Terminated - All Subjects Stable.'",
            "Narration: LIBERATION ENDING - Your immediate compassion broke the cycle and freed two souls from their shared prison.",
        ],
        "choices": [],
    },
}
# ---------- Helpers for detecting numbered blocks ----------
_numbered_line_pattern = re.compile(r"^\s*(\d+)\.\s*(.*)$")


def is_single_line_choice(line: str) -> bool:
    """Detect a single line containing at least two numbered options like '1.' and '2.'."""
    return bool(re.search(r"\b1\.", line)) and bool(re.search(r"\b2\.", line))


def collect_numbered_block(narration_lines, start_index):
    """
    Return (block_lines, end_index, options)
    options: list of (num_str, text)
    """
    n = len(narration_lines)
    cur = narration_lines[start_index]
    # Case A: single line containing multiple "1. ... 2. ..." entries
    if is_single_line_choice(cur):
        pattern = re.compile(r"(\d+)\.\s*(.*?)(?=(?:\s+\d+\.|$))")
        found = pattern.findall(cur)
        options = [(num, text.strip()) for num, text in found]
        return [cur], start_index + 1, options

    # Case B: "P:" line followed by numbered option lines
    if "P:" in cur or "p:" in cur:
        j = start_index + 1
        numbered_lines = []
        while j < n and _numbered_line_pattern.match(narration_lines[j]):
            numbered_lines.append(narration_lines[j])
            j += 1
        if numbered_lines:
            opts = []
            for ln in numbered_lines:
                m = _numbered_line_pattern.match(ln)
                if m:
                    opts.append((m.group(1), m.group(2).rstrip()))
            return [cur] + numbered_lines, j, opts

    # Case C: block of numbered lines without preceding P:
    if _numbered_line_pattern.match(cur):
        j = start_index
        numbered_lines = []
        while j < n and _numbered_line_pattern.match(narration_lines[j]):
            numbered_lines.append(narration_lines[j])
            j += 1
        if len(numbered_lines) >= 2:
            opts = []
            for ln in numbered_lines:
                m = _numbered_line_pattern.match(ln)
                if m:
                    opts.append((m.group(1), m.group(2).rstrip()))
            return numbered_lines, j, opts

    return None, start_index, None


def strip_tags(s: str) -> str:
    """Remove bracketed [] tags and parenthetical () tags from choice labels/display.
    This helps hide emotion tags from the player display per request.
    NOTE: This removes ALL parenthetical content—if you need to preserve some, change the regex.
    """
    if s is None:
        return s
    s2 = re.sub(r"\s*\[.*?\]", "", s)
    s2 = re.sub(r"\s*\(.*?\)", "", s2)
    return s2.strip()


def display_line_for_user(ln: str) -> str:
    """Prepare narration line for display: remove square-bracket tags but keep normal parentheses.
    We intentionally remove [] tags because your choice lines used them for emotions.
    """
    if ln is None:
        return ln
    return re.sub(r"\s*\[.*?\]", "", ln)


def prompt_numeric_choice_inline(options):
    """
    Prompt user to pick a numeric option from a block of options.
    Returns the chosen number string.
    """
    valid_nums = {num for num, _ in options}
    opts_sorted = sorted(valid_nums, key=lambda x: int(x))
    while True:
        try:
            sel = input(f"Choose an option {opts_sorted} (type the number): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            sys.exit(0)
        if sel in valid_nums:
            return sel
        print(
            "Invalid choice. Please type one of the option numbers shown (e.g. 1, 2...)."
        )


def present_scene(scene_id):
    scene = SCENES.get(scene_id)
    if not scene:
        print(f"[!] Missing scene: {scene_id}")
        return None
    print("\n" + "=" * 70)

    narration = scene.get("narration", [])
    i = 0
    while i < len(narration):
        ln = narration[i]
        if ln.strip() == "":
            i += 1
            continue

        # Single-line inline block e.g. "P: 1. Say nothing 2. Who are you?"
        if is_single_line_choice(ln):
            print(display_line_for_user(ln))
            block_lines, next_index, options = collect_numbered_block(narration, i)
            sel = prompt_numeric_choice_inline(options)
            chosen_text = next((t for n, t in options if n == sel), "")
            chosen_text = strip_tags(chosen_text)
            print(f"You chose: {sel}. {chosen_text}")

            # Map to the scene-level choices if available (so user doesn't need to pick twice)
            scene_choices = scene.get("choices", [])
            try:
                idx = int(sel) - 1
                if 0 <= idx < len(scene_choices):
                    choice = scene_choices[idx]
                    # Add the total number of choices for AI decision
                    choice["total_choices"] = len(options)
                    return choice
            except Exception:
                pass
            # If no matching scene-level mapping, return an ad-hoc choice dict
            return {
                "label": chosen_text,
                "text": chosen_text,
                "next": None,
                "total_choices": len(options),
            }

        # Multi-line block: P: then numbered lines, or several numbered lines in a row
        block_lines, next_index, options = collect_numbered_block(narration, i)
        if block_lines:
            # Print the whole block as-is but sanitized
            for b in block_lines:
                print(display_line_for_user(b))
            sel = prompt_numeric_choice_inline(options)
            chosen_text = next((t for n, t in options if n == sel), "")
            chosen_text = strip_tags(chosen_text)
            print(f"You chose: {sel}. {chosen_text}")

            # Map to scene-level choices if exists
            scene_choices = scene.get("choices", [])
            try:
                idx = int(sel) - 1
                if 0 <= idx < len(scene_choices):
                    choice = scene_choices[idx]
                    # Add the total number of choices for AI decision
                    choice["total_choices"] = len(options)
                    return choice
            except Exception:
                pass
            return {
                "label": chosen_text,
                "text": chosen_text,
                "next": None,
                "total_choices": len(options),
            }

        # Normal narration line
        print(display_line_for_user(ln))
        wait_for_advance()
        i += 1

    # If no inline numbered block triggered a return, present the scene-level choices (legacy)
    choices = scene.get("choices", [])
    if not choices:
        return None

    # For single choice scenes, auto-proceed without showing numbered menu
    if len(choices) == 1:
        choice = choices[0]
        choice["total_choices"] = 1
        return choice

    # Multiple choices - show the menu
    print("\nChoices:")
    for idx, c in enumerate(choices, start=1):
        print(f"  {idx}. {strip_tags(c['label'])}")
    print("  0. Quit")
    while True:
        ans = input("\nChoose a number: ").strip()
        if ans == "0":
            print("Exiting.")
            sys.exit(0)
        if not ans.isdigit():
            print("Enter a number.")
            continue
        idx = int(ans) - 1
        if 0 <= idx < len(choices):
            choice = choices[idx]
            choice["total_choices"] = len(choices)
            return choice
        print("Invalid choice.")


def _print_ai_immediate(text):
    """
    Print AI reply immediately, skipping blank lines.
    Used so the player doesn't need to press Enter before seeing the AI reply.
    """
    if text is None:
        return
    lines = text.splitlines()
    for ln in lines:
        if ln.strip() == "":
            continue
        print(ln)


def check_endings():
    """Return a forced ending scene id if thresholds are met; otherwise None."""
    # Check for early negative ending (more dramatic)
    if state.get("neg_count", 0) >= NEGATIVE_THRESHOLD:
        return (
            "end_early_negative" if state.get("neg_count", 0) <= 3 else "end_gameover"
        )

    # Check for early positive ending
    if state.get("pos_count", 0) >= POSITIVE_THRESHOLD:
        return (
            "end_early_positive" if state.get("pos_count", 0) <= 3 else "end_vulnerable"
        )

    # Check for neutral ending if player is being very passive
    if (
        state.get("neu_count", 0) >= NEUTRAL_THRESHOLD
        and (state.get("pos_count", 0) + state.get("neg_count", 0)) <= 1
    ):
        return "end_neutral"

    return None


def process_choice(choice, current_scene=None, total_choices_in_scene=1):
    player_text = choice["text"]
    choice_label = choice.get("label", "")
    # sanitize player_text before sending (strip any tags if present)
    player_text = strip_tags(player_text)

    # Only call sentiment analysis and AI if there are multiple meaningful choices
    if total_choices_in_scene > 1:
        # echo player's chosen text to the log/console
        print(f"\n-- You: {player_text}")

        # 1) sentiment (do NOT print it to terminal per request)
        sentiment = call_sentiment(player_text)

        # update internal counters quietly
        if sentiment and isinstance(sentiment, dict):
            label = sentiment.get("label")
            if label == "positive":
                state["pos_count"] = state.get("pos_count", 0) + 1
            elif label == "negative":
                state["neg_count"] = state.get("neg_count", 0) + 1
            else:
                state["neu_count"] = state.get("neu_count", 0) + 1
        else:
            # if sentiment unavailable, treat as neutral for counters
            state["neu_count"] = state.get("neu_count", 0) + 1

        # Track sentiment internally without displaying
        total_tracked_choices = (
            state.get("pos_count", 0)
            + state.get("neg_count", 0)
            + state.get("neu_count", 0)
        )

        # 2) call AI with enhanced context
        ai_json = call_ai(
            player_text,
            sentiment=sentiment,
            history=state["history"],
            scene=current_scene,
            choice_label=choice_label,
        )
        if ai_json:
            ai_text = (
                ai_json.get("ai_response")
                or ai_json.get("response")
                or ai_json.get("text")
                or "<no response>"
            )
            # Print the AI-generated merchant reply immediately (no paging before it)
            print("\n--- Merchant replies: ---")
            _print_ai_immediate(ai_text)
            print("-------------------------")
            # record history with scene context
            state["history"].append(
                {
                    "player": player_text,
                    "sentiment": sentiment,
                    "ai": ai_text,
                    "scene": current_scene,
                }
            )
        else:
            print(
                "\n[Merchant reply unavailable. Proceeding without merchant dynamic reply.]"
            )
            state["history"].append(
                {
                    "player": player_text,
                    "sentiment": sentiment,
                    "ai": None,
                    "scene": current_scene,
                }
            )

        # Check for forced endings driven by sentiment counters
        forced = check_endings()
    else:
        # For single choices, silently proceed without AI interaction
        forced = None

    wait_for_advance()

    return forced


def main():
    print("=== MEMORY MERCHANT ===")
    cur = "start"
    while cur:
        # Track scene transitions
        if cur != state.get("current_scene"):
            state["current_scene"] = cur
            if cur not in state["scene_history"]:
                state["scene_history"].append(cur)

        chosen = present_scene(cur)
        if chosen is None:
            print("\n=== THE END ===")
            break

        # Get the total choices count for AI decision
        total_choices = chosen.get("total_choices", 1)

        # process_choice will call sentiment + AI only if there are multiple choices
        forced_next = process_choice(
            chosen, current_scene=cur, total_choices_in_scene=total_choices
        )
        nxt = forced_next or chosen.get("next")
        if not nxt:
            print("[!] No next scene configured. Ending.")
            break
        cur = nxt


if __name__ == "__main__":
    main()
