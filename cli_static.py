#!/usr/bin/env python3
# memory_merchant_static.py
# Static CLI version of the Memory Merchant scene (no backend calls, no AI replies).
# Behavior:
# - Press Enter to advance to the next dialogue line.
# - When a line contains multiple numbered choices (e.g. "1. ... 2. ..."), that whole line
#   is shown at once and the script asks you to type the number of your choice.
# - The dialogue text is included exactly as provided by the user and is not altered,
#   except blank lines are skipped so you don't have to press Enter twice.
# - After you choose, the chosen option is displayed and the script advances immediately
#   (the numeric choice acts as the Enter) — only for choice lines.

import sys
import re

SCRIPT = """
M: Finally awake, huh?
P: 1. Say nothing 2. Who are you? 3. What happened? 4. Where am I?

M: Well, not the time for chitchat. meet me at the shop. *leaves the room*

P: (inner dialogue) What is this place ? Who was that guy ?
P: Wait... Who even am I ??
P: I should probably follow my only current lead.

Narration: It's raining outside, tight alleyways dimly lit by the moon, nobody to be found.
Narration: You see a light not so far away. You decide to head for it
Narration: Under the light hangs a sign. Jagged, chipped, worn down, barely reads "Memories"

Narration: You feel uneasy, but decide to go in anyways. You will do anything to remember.. Remember it all..
Narration: The shop reeks of sawdust, Tiny place with a counter and many gemstones.
Narration: The merchant appears before you seemingly out of nowhere, Eyes staring into yours. You decide to break the tension

P: I came here as you requested. Now answer my questions.
M: Hasty are we ? (chuckles) I needn't answer you myself.. Take a look at this:

Narration: The merchant shows you a scroll with many black dim gemstones scattered inside it. Random at first, but taking a shape the more you stare into it.

M: (whispers) Don't lose yourself now.

Narration: you snap back and look at the merchant.

P: What was that ?
M: Full of questions you are. Here, you will like this.

Narration: The merchant takes out one of the gems on the scroll and hands it to you.

M: Hold onto it tight and close your eyes..

Narration: The merchant closes your grip onto the gemstone while closing your eye lids with his other hand
Narration: You don't feel the urge to resist. It is pleasant.

Narration: You are suddenly teleported into this alternate reality. 
Narration: You are in a warm house, sunlight spilled through the kitchen's window as Soft beams filtered through the glass, casting a gentle glow.
Narration:  you see a woman cooking. She kneels down, food's almost done.
Narration: with a lovely smile she says "hey, dear Alaric" while patting your head.
Narration: You snap back to the rotten shop. The old merchant in front of you, staring you in the eyes.
Narration: You get creeped out and take a strong step back.
Narration: the black gemstone in your hand is now glowing with a pink color.
M: Oh and that's how you react.. (pitiful laughter making fun of you)
M: (whispers) Do you want more ?
P: Why would I want more ?! I don't even know that woman and I'm not that short!
M: You just *have* to question *everything*, haven't you?
M: That's you, and that's your mother. and that pink gemstone is love, your pure mother's love.
M: First one's on the house.
P: (to himself) Considering that this swine is to be trusted, I at least know now my name.
P: I need to know more. I have to make him show me all my memories
M: Spaced out ? Guess that was too much (laugh)

Narration: You feel aggravated, challenged

P: Not at all, show me more of your tricks.
M: Oh but nothing is free in this world dear.
M: For each memory you wish to see, you must sacrifice a part of your body.

P: Whatever do you mean by that ?
M: It's simple. Once you go in and come back out, you'll be missing a finger or two (chuckles) until you lose all of yourself.
P: (to himself) but there must be an exploit to that offer. I can't afford to lose my limbs.
P: Fine, I will play your little game, show me another one of those so-called memories.
M: As you wish.

Narration: The merchant pulls out another black gemstone from the scroll. Putting it in your hands.
Narration: you wonder which emotion you will experience now.
Narration: Before the merchant closes your grip or eyes, you do it yourself. You know the game now.

M: (voice fading away).. This one... goes deeper.
Narration: You get teleported to another place. Same House as the first memory. But it feels different.
Narration: you are sitting on the floor of the living room next to a red headed boy who looks like he is the same age as you. you are surrounded by scattered toy pieces and half-built inventions—batteries, plastic gears, you are holding a screwdriver slightly big for your hands, and you both are laughing softly.

Narration: Then, it started.
Narration; Muffled at first—a sharp voice breaking the quiet, then another voice rising to meet it.
Narration: You hear your mother and a man argue. The words blurred into something jagged and fast. 
Narration: your friend froze, mid-motion, He glanced at you, instinctively, with concerned looks not knowing what to do, but you were quiet as a dear, you didn’t flinch. Didn’t speak, like it was no surprise, you are used to it, your eyes fix at your hand as you twist the screwdriver too tightly.

Narration: your friend was about to say something, asking if you were okay but he's interrupted by a striking sound, a slap followed by screams from your mother.
Narration: you get up instantly, anger building up inside you, You don't have control over your body, like you're watching a movie.
Narration: you run upstairs only to find the man approaching your mother again while she screams, and without thinking, you lunge at the man and stab him with the screwdriver you realize you were still holding. your mother screams and so do you.  
Narration: Looking at your mother to apologize, you see your friend standing at the door, he has seen it all. 
Narration: You feel uneasy, panicking, you drop the screwdriver on the floor, somehow you are relieved to have saved your mother, she does not react, and your friend is staring at the man.
Narration: The cops instantly come in, abnormally too quick of a response time. You were about to speak until your friend instantly takes the blame for you, holding the screwdriver, he is Claiming that he did it.
Narration: your eyes met his and he smiles, reassuringly whispering "it's okay"
Narration: You snap back to the shop, The smell doesn't bother you anymore, you're used to it. the gemstone glows with a blue light in your hand. 

P: What did you just show me ? who is this boy, and I would never hurt someone.
M: this was your childhood best friend, you have caused him a great harm.
p: but why? why did i do this? and why did he have to make such a sacrifice for me?
M: those questions are not important now, the past is already long gone. the important question is what are you going to do about it now?
p: is there really anything i can do about it? i don't even know where am i.
M: don't be so impulsive, choose your gems carefully and you might know your answers soon enough.
p (to himself): apparently i choose the gemstones based on emotions, the first one was love, this one must be sadness, maybe if i concentrate more, i might be able to know the emotion before the memory ends, and i might know how to influence it.
P:  okay, give me the next memory.  
M: Shall we proceed ?
P: We shall...

Narration: The air grows thicker. The candlelight in the shop flickers violently, though there's no wind. The gemstones on the scroll seem to shimmer with anticipation—as if alive.

M: Brave. Or foolish. Hard to tell with your kind.

Narration: The merchant extends a hand, slower this time. As if testing the boundaries of your strange new agreement. You reach out, and he places a third gem into your palm.
Narration: you notice you are missing finger, but you are not surprised, you agreed on this game's rules. 
Narration: Without a word, you close your hand and shut your eyes. and The world turns inside out.

Narration: it is hot, you're sweating, standing before a board hanging on a wall in a school hall, papers pinned to that board in that familiar, slightly crumpled grid. 
Narration: you are surrounded by some high school kids—seemingly your classmates, around the wall, pointing, groaning, cheering. 
Narration: you notice an orbit of students clustered around someone. Laughing, talking, voices overlapping as if everyone was trying to be heard just a little more clearly by the one in the center. that boy was the only who didn't rush to see the list, like he had expected it already, that his name would be on the top.
Narration: He walked up calmly, hands in his sweaters' pockets, scanned the list with a faint smirk that said of course, and nodded once, more to himself than anyone else. People clapped him on the back. And the circle of admiration closed around him once again.

Narration: Your hands are damp, as you move your index finger on the paper. You read the same sentence on the headline again "the test results", Your heartbeat was loud—too loud—like it might give you away.
Narration: you are searching for your name.
Narration: you take a deep breath, lifting your eyes up again to see that dark haired boy smiling like it didn’t even matter. And maybe it didn’t—to him. But you feel anxious like it meant a great deal to you.
Narration: you slide your eyes back to the paper, they immediately behold  the name next to the second place "Theo shaw" your stomach gave that quiet, familiar drop—not quite disappointment, not quite surprise. Just the same dull ache of being almost, again.
Narration: The paper shifts in your hands... no—melts. The ink begins to run.
Narration: The hallway flickers. That boy’s face—smile still frozen—begins to blur, smudged like a watercolor in the rain. and suddenly you are back into the shop.
Narration: you look at the merchant, and for the first time you take in his red hair that is now glitching, his expressions are unreadable. and the gemstone in your hand now has a yellow glow to it, you wonder which emotion have you witnessed.

P: (to himself) This doesn't feel right. it doesn't look real. That merchant scammed me.
p: This isn't my memory.. my name is not Theo, it is Alaric.. you are tricking me.
Narration: The merchant gets visibly frustrated but tries to act cool.
M: a mistake on my part (wicked laugh) here, let me compensate you.

Narration: The merchant goes to pick out another gemstone only to find his index finger missing.
Narration: The merchant gets surprised and scared.

M: What did you do ?! Where's my finger ?!
P: Looks like your offer turned on you for selling a false product.
P: Now, give me another one.

Narration: The merchant mumbling to himself, gets out the forth gemstone and hands it to you.
Narration: You grip it and close your eyes.
Narration: The city lights glow. you are sitting with someone side by side, robes half-off, diplomas at your side. A quiet university rooftop at dusk. The graduation ceremony has just ended. you feel heavy, you have no idea what you're going to do now with your life.

Narration: the person sitting next to you is staring at the skyline and trying to start a conversation: "Hard to believe, huh? That it’s over."
Narration: you are half-smiling and you say casually: "You mean this part. Knowing you, it’s never really over. Just a new beginning."
Narration: he smiles back, move his hand through the waves of his dark hair: "Damn right. And this beginning… it’s big." then he pauses, glances sideways at you with a flash of determination in his eyes: "A Neuro Lab reached out. Full access to their neural interface research. Cutting-edge hardware. Autonomy. They want me to lead a new sub-division."

Narration: you feel quietly surprised: "Of course they do. You were always first in line."
Narration: he ignores the tone replying: "I told them I won’t take it unless you come with me. As my partner."
Narration: you turn to him, stunned: "What?" and he answers: "Lab partner. Co-lead. We build it together—whatever “it” becomes. You and me. Like it’s always been."

Narration: a weird feeling slips into your heart, you say softly: "Alaric, you don’t need me for that. You never did."
Narration: Alaric is suddenly serious: "That’s where you’re wrong. I’ve got the vision, sure. But you see the things I miss. The patterns, the ethical pitfalls, the consequences. I push forward. You anchor me. We’re not balanced without each other."

Narration: "you look away, your tone is quiet, low: "You were always the one people remembered. The name on the poster. The genius.".. you pause as if you are not sure if you would take credits for that: "I was just the one double-checking your equations at 2 AM."

Narration: Alaric leans forward: "Exactly." .."You see things, Theo. That matters more than headlines."

Narration: you're hesitant, you give him that look, studying him and you say: "Is this... gratitude talking? Or guilt?"
Narration: he says softly: "It’s truth. And maybe a little fear. I can’t do what I need to do alone.".. smiles faintly as he continues: "Come with me. Let’s build something no one else even dares to imagine."

Narration: a moment of silence passes by, finally you agree: "Alright. I’m in."
Narration: Alaric smiles, relaxed for the first time all night: "Good. Because I have ideas, Theo. Wild ones. Dangerous ones. But if you’re with me—" he leans back, looking at the stars again "—we’ll change everything."
Narration: The stars shimmer. Then—tremble. a strong light blinding your eyes.. and you are transported back to the old shop, you are frustrated now. and the gemstone glows in a sharp green color.
p: this can not be right, how am i witnessing a memory that i'm also talking to me in it? this can't be me memory either. and i still can't decode the emotions or the ideas behind them

Narration: the merchant's face flickers, glitching again but this time it is stronger, it takes him some time to get back to his stable shape, his face somehow now looks familiar.

M: i don't know what's wrong, you are right, this is not your memory, this is Theo's memory.
P: who is Theo? 
M: Memories are the architects of our identity. you know Theo just like you know yourself. he is a part of you.
P: what about the gem colors, why do they keep changing?
M: Emotions are the colors of the soul, and you have lost your soul, Alaric.
M: you should try to get it back, Hold onto your memories and your emotions. the stronger emotions are the ones that affect you the most and you can affect them as well. 
M: this memory held the joy, the excitement of accepting a friend's offer. it may not be your memory, but it certainly gave you something to learn.
P: i can't tolerate anymore false memories, give me a right one, a true memory of my own.
M: here, take this.

Narration: he takes out the fifth gemstone and place it in your hand, you notice his hand missing another finger, but he doesn't seem to care. the gemstone now feels warm against your palm.
Narration: The shop starts to shift—walls stretch, the counter melts into the floor, and the merchant’s form flickers, and you find yourself in a different place.

Narration: you find yourself in a lab, silent as you hear your footsteps, you are restless, walking back and forth. it is late night, Rain tapping against the high lab windows. The lab was a mess of wires, electrodes, and futuristic gadgets. monitors flicker with neural readouts. you've worked tirelessly, fueled by your determination. you feel your eyes grow heavy.

Narration: In the center: The device, Glowing. finally ready, finally alive.
Narration: you stare at it and whisper: "The Cerebridge."

Narration: After years of theory, failed prototypes, sleepless nights, dead rats, corrupted brain scans, blood on cables and guilt in silence—it’s here. No fanfare. No applause. Just the soft, steady pulse of the interface as it powers on. The light it casts isn’t warm or cold—it’s pure.

Narration: a man standing in the corner asked: "are you sure this is safe?" he is concerned, eyeing the complex setup.
Narration: you take a glance on him he has the merchant's face.
Narration: "Of course it is," you reply, your eyes gleaming with excitement as you continue: "I've run countless simulations. It's foolproof." 
your smile grows wider, you are losing your mind as you stare blankly at his eyes: "And It is the time for the first human test, I must find my subject"

Narration: he moves toward you, cautious, voice low. “Alaric… slow down. Let—just document this. Run a closed-loop trial. We don't even know if the emotional filters are stable—”
Narration: you turn to him, and for the first time in weeks, you are calm: “You still think this is about emotion. About dreams and delusions, Theo. It’s not. It’s about structure. Pattern. Consciousness as architecture. And I’ve built the doorway, and we will dive into it”

Narration: you open your eyes and suddenly you are in the shop again, the gemstone glows with a purple color, you look at the merchant again and now you know, the merchant is Theo. 
P: it's you! you are him! you are a part of my past! i saw you!
M: (smiles calmly) easy, young man. you are on the verge of unmasking your deepest secret.
P: how is this possible? how did i access your memories as well as mine?
M: you know the answer to that, you invented it yourself.
P: (to himself) the cerebridge device..
P: i am in your head!
M: you're close enough. you were in my head, but now i am in yours.
P: I don't believe you. I can't believe you.
M: Then go. Find one more. Let the truth carve what’s left of you.

Narration: You stare down at your hands. They tremble. One more gem sits before you, unclaimed. Unlike the others, it glows before you touch it. the merchant's fingers came back as he handles you the last gemstone.

P (to himself) One more... and I either find who I am—or lose it all.

Narration: You pick it up. And for the first time—you don’t close your eyes.
Narration You don’t teleport. The shop melts around you into a familiar place, it is The same lab, midnight. Theo is asleep in a chair, worn out after another long, heated argument over Cerebridge safety protocols. The machine hums quietly, almost expectantly.*

Narration: you stare at him for a while. His breathing is slow, steady. There’s something unbearably *human* about it. Something fragile. you wonder what his mind sounds like.
He fell asleep arguing with you again,
He doesn’t understand. He *refuses* to.

Narration: you still need a human subject because the final truth of consciousness is not information—it’s experience. And experience cannot be simulated. It must be lived.
Narration: This isn’t about curiosity anymore. It’s necessity. and you just can't see why is Theo so concerned about it. 
He would never volunteer.
He doesn’t trust the machine.
He doesn’t really trust *you*
Narration: But that’s why it has to be him. Not a stranger. Not a test subject. 
Because you know him. you know his patterns, your fears, his rhythms. If you can navigate his mind, if you can see the scaffolding that holds Theo Shaw together… you may understand what the “self” really is.

Narration: His chair creaks as you take closer steps towards him. He stirs, mumbles something, half-asleep: “Alaric… what are you doing…”
Narration: your voice is calm, gentle as you whisper “I am Just making sure everything’s working. Go back to sleep.”

Narration: you lift the Cerebridge electrodes, gently attaching them to his head, and initiate the sequence.
the screen reads: **Connection established. Subject: THEO SHAW**
**Depth Index: 0.03... Syncing...**
you inhale sharply as his thoughts bleed in.

Narration: At first, everything seemed fine. The machine hummed, and Theo's eyes glazed over. But suddenly, his body convulsed, and he screamed in agony.

Narration: "Alaric, what are you doing. stop it! It's hurting!" he begged.

Narration: you were too enthralled by the data streaming on her screens. you didn't notice the warning signs until it was too late.
Narration: Theo's body began to shake violently, his eyes rolling back in his head. you frantically try to shut down the device, but it malfunctioned. The machine shuts down, leaving Theo unconscious on the floor.
 
Narration: you rush to his side, horrified, tears streaming down your face as the realization hit you suddenly.
Narration: "Theo, oh God, I'm so sorry," you whisper, cradling his head.

p: (to himself) no.. this can not be it, it can not be the end..

Narration: a strong feeling of guilt washes over you, you slide the Cerebridge over your head. and try to reconnect it, you must understand!
Narration: The world tilts—not physically, but perceptually. Like closing one eye and seeing a hidden image appear. Connection: Neural sync established. the screen reads: ** Subject: ALARIC VANE**
Depth index: 0.2... 0.4... stabilizing.
Narration: And then—you fall into a hole of deep black.

P: (to himself) This can't be right... this must be some illusion, a test...

Narration: You jolt back into the shop, gasping. But something is wrong. The shop is different—brighter. No sawdust. The gemstones are gone. Only the scroll remains, and it’s... blank.

M: (calmly) You reached the boundary.
P: What boundary
M: Between remembering... and becoming.
P: Becoming what
M: A fragment. A story. A soul trapped in recollection.
P: This isn't memory... it's madness.
M: Memory is madness, if seen too clearly. That's why we forget.
P: I won't accept this memory, i have to go back.

Narration: you press the same gemstone in your hand strongly, it is glowing bright red, you figure out that this is your core memory, your most strong emotion.. regret.
Narration: you know what to do now.

Narration: It is The same lab. Midnight. The machine still hums softly, the screens dim and patient. Nothing has changed, and yet... everything feels different.
Narration: Theo is asleep in the chair again, head slumped, arms crossed tightly across his chest like he’s trying to hold himself together.
He fell asleep arguing with you. Again.
But this time, you don't reach for the Cerebridge.
You just stand there.
And watch him.
Narration: You see him more clearly now—not as a pattern of neural rhythms or a testable subject.
 But as Theo.
 Your friend.
 The boy who sat beside you in lectures. The man who followed you into impossible ideas. The one person who stayed.
He was never just second place. He was the reason you didn’t collapse.

Narration: You take a breath. A long one.
 The Cerebridge waits. It pulses softly. It knows your name.
But you don’t move.
Instead, you kneel beside Theo. Quietly. Like you're afraid the guilt might wake him before your apology does.
Narration: You whisper—not to the machine, but to him.
“I almost did it again.”
“I was ready to take something from you… because I was afraid I couldn’t reach it on my own.”
“But this—what we’re building—it means nothing if it costs you.”

Narration: He stirs, gently this time. One eye opens, heavy-lidded: “Alaric... what’re you doing…?”
You smile. And this time, it’s real.
“Letting you sleep. For once.”

Narration: You sit on the floor beside him, and for the first time in weeks, you don’t touch the machine.
You just listen.
To the quiet hum of the lab.
 To Theo’s steady breath.
 To the space between knowing and loving—and why you ever thought they had to be the same.
Because you finally understand: To know someone’s mind… you have to be invited.

Narration: Then everything shatters. Glass, machines, wires. You scream. A voice yells to go, your voice.
Narration You’re back in the shop, collapsed on your knees.

P: (weakly) I did it, I changed the past..

M: So... who are you now.
P: I was your friend. and I was the reason you lost everything.
M: Truth. A heavier weight than any missing limb.

Narration: The merchant steps back. He seems smaller now. Human, almost.
M: You have what you came for. you can Leave now. you freed yourself from the guilt that trapped you in your head.
P: How? You said that nothing is free.
M: It isn’t.

Narration: the merchant's body starts to fade away.

M: (whispers) you freed me too..

Narration: You look down. Your hands—both whole. But your reflection in the gem's surface is... not. Hollow eyes. Mouth sewn shut. but you feel relieved.
Narration: you hear a distant voice, low, but sharp.
"Wake up, Alaric! You have to wake up! now!"

Narration: you open your eyes slowly, you are in the lab, sleeping on the chair, theo is next to you, glancing at you, with real concern in his eyes, he says: "oh, thank god, you are okay!"
Narration: you ask quickly: "what happened?"
Narration: Theo takes a deep breath then replies: " you tried using the cerebridge on yourself, but it wasn't ready.. you are lucky it shut itself down before anything happens"

Narration: at that moment you realized, it did really happen, you were trapped in your own head. And you've beaten the machine at its own game, the mind game."

GAME OVER.
""".splitlines()

# Determine which lines are "choice blocks". Rule: if a single line contains at least two numbered options like "1." and "2.", treat it as a choice block.
def is_choice_block(line):
    # True if the line has both "1." and "2." or generally multiple numbered options on same line
    return bool(re.search(r"\b1\.", line)) and bool(re.search(r"\b2\.", line))

def parse_choices(line):
    """
    Extract numbered choices from a single line.
    Returns list of tuples (num_str, text).
    Example: "P: 1. Say nothing 2. Who are you?" -> [("1","Say nothing"),("2","Who are you?")]
    """
    pattern = re.compile(r'(\d+)\.\s*(.*?)(?=(?:\s+\d+\.|$))')
    return pattern.findall(line)

def prompt_enter():
    try:
        input("(press Enter to continue) ")
    except (EOFError, KeyboardInterrupt):
        print("\nExiting.")
        sys.exit(0)

def run():
    print("=== MEMORY MERCHANT — STATIC CLI ===")
    print("(Press Enter to advance. Numbered choice lines will ask for a numeric selection.)\n")

    i = 0
    while i < len(SCRIPT):
        line = SCRIPT[i]

        # Skip blank lines entirely so user doesn't have to press Enter for them.
        if line.strip() == "":
            i += 1
            continue

        # Print the line exactly as-is
        print(line)

        # If this line is a choice block (contains multiple numbered options), parse and ask for a choice.
        if is_choice_block(line):
            choices = parse_choices(line)
            if not choices:
                # fallback: just wait once if parsing failed
                prompt_enter()
                i += 1
                continue

            # Build a set of valid numbers (as strings)
            valid_nums = {num for num, _ in choices}

            # Prompt until we get a valid selection
            while True:
                try:
                    sel = input(f"Choose an option {sorted(valid_nums)} (type the number): ").strip()
                except (EOFError, KeyboardInterrupt):
                    print("\nExiting.")
                    sys.exit(0)

                if sel in valid_nums:
                    # find the chosen text
                    chosen_text = next((text.strip() for num, text in choices if num == sel), None)
                    # Display the chosen option (preserve the exact option text from the script fragment)
                    print(f"You chose: {sel}. {chosen_text}")
                    # IMPORTANT: for choice lines, the numeric input immediately counts as the Enter — advance now.
                    break
                else:
                    print("Invalid choice. Please type one of the option numbers shown (e.g. 1, 2...).")

            # Advance without an extra Enter (choice input already advanced).
            i += 1
            continue

        # Otherwise wait for Enter before showing next line
        prompt_enter()
        i += 1

    print("\n=== THE END ===")

if __name__ == '__main__':
    run()
