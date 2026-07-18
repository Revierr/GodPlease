##########################################
# █ █ ▄▀▄ █▀█ ▀█▀ ▄▀▄ █▄▄ █   █▀▀ █▀▀ 
# ▀▄▀ █▀█ █▀▄ ▄█▄ █▀█ █▄█ █▄▄ ██▄ ▄██ 
##########################################
default persistent.ending1_achieved = False
default persistent.ending2_achieved = False
default persistent.seen_warning = False

##########################################
# █▀▀ █▀▀ █▀▀ █▄ █ █▀▀ █▀▀ 
# ▄██ █▄▄ ██▄ █ ▀█ ██▄ ▄██ 
##########################################

##########################################
#content warning
default show_element = False

screen content_warning():
    modal True 
    style_prefix "confirm"

    # 2. Timer that waits 1.5 seconds, then changes the variable
    timer 1.5 action SetScreenVariable("show_element", True)

    add "blackBG"# Solid black background
    if show_element == True:
        button:# An invisible button covering the entire standard game window
            xsize 1920
            ysize 1080
            action [Return(), With(Dissolve(1.5))] # Returns from the called screen and continues the script
    frame:
        background None            # Makes the container invisible
        padding (300, 10, 300, 10)   # (Left, Top, Right, Bottom) margins/padding
        
        add "warningsign":
            at fade_in_out_loop
            xalign 0.5
            yalign 0.1
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 100

            text _("This game was made for the O2A2 VN Jam 2026, a micro Visual Novel jam with strict asset limitations and a 1000 word limit.\n"):
                xalign 0.5
                text_align 0.5
                #text_size 24

            text _("This game features mild blood and cartoon gore.\n"):
                xalign 0.5
                text_align 0.5
                #text_size 24
        if show_element == True:
            hbox:
                at fade_in
                xalign 0.5
                yalign 0.8
                spacing 100
                text _("Click anywhere to continue")
##########################################

##########################################
# █▀▀ █▀█ █▄ █ █▀▀ ▀█▀ █▀▀ 
# █▄▄ █▄█ █ ▀█ █▀  ▄█▄ █▄█ 
##########################################
init python:
    config.has_autosave = False
    config.has_quicksave = False
    config.autosave_on_quit = False
    config.autosave_on_choice = False
    config.default_textshader = 'typewriter'
    config.menu_include_disabled = True

##########################################
# ▀█▀ █▄ ▄█ ▄▀▄ █▀▀ █▀▀ █▀▀ 
# ▄█▄ █ ▀ █ █▀█ █▄█ ██▄ ▄██ 
##########################################
#images
image blackBG ="images/blackBG.png"
image warningsign = "images/warningsign.png"
image guy neutral ="images/guy_neutral.png"
image guy angry = "images/guy_angry.png"
image guy smile = "images/guy_smile.png"
image rain = "images/rain.png"
image dust = "images/fartcloud.png"

#sounds
define amb_rain = "audio/amb_rain.ogg"
define thunder = "audio/thunderstrike.ogg"

#particle effects
image dusty = SnowBlossom(At("dust", varying_size), count=12, border=50, xspeed=(3, -3), yspeed=(-20, -30), start=0.5, fast=True)
image rainy = SnowBlossom(At("rain", varying_size), count=75, border=1095, xspeed=(3, -3), yspeed=(1740, 1990), start=0.5, fast=True) #front layer
image rainy2 = SnowBlossom(At("rain", varying_size_small), count=45, border=1095, xspeed=(3, -3), yspeed=(2740, 2090), start=0.5, fast=True) #back layer

#lightning light
transform lightning_lighting:
    matrixcolor TintMatrix("#fff") #no tint
    block:
        linear 0.25 matrixcolor TintMatrix("#f7e57f")
        linear 0.25 matrixcolor TintMatrix("#ecde8b")
        linear 0.25 matrixcolor TintMatrix("#fffadc")
        linear 0.5 matrixcolor TintMatrix("#fff")

transform varying_size:
    zoom renpy.random.uniform(0.5, 1.5)
transform varying_size_small:
    zoom renpy.random.uniform(0.5, 0.75)

transform fade_in_out_loop:
    alpha 0.5
    linear 1.0 alpha 1.0
    linear 1.0 alpha 0.5
    repeat

transform fade_in:
    alpha 0.0
    linear 0.5 alpha 1.0  

style navigation_button_text is gui_text:
    properties gui.button_text_properties("navigation_button")
    
    # Keeps text from jittering by giving idle state invisible padding
    idle_outlines [ (3, "#00000000", 0, 0) ]
    
    # The glowing effect (Stacked outlines from sharpest to softest)
    hover_outlines [ (2, "#e7fcfc40", 0, 0), (3, "#99999940", 0, 0) ]

##########################################
# █████ █████  ███  ████  █████ 
# █       █   █   █ █   █   █   
# █████   █   █████ ████    █   
#     █   █   █   █ █   █   █   
# █████   █   █   █ █   █   █ 
# The game starts here.
##########################################

#Trigger the warning when the game boots up
label splashscreen:
    if persistent.seen_warning == False:
        scene black
        call screen content_warning 
        $ persistent.seen_warning = True
    return

label start:
    
    "The heavens weep over the remains of the battleground."

    window hide
    scene field 
    show rainy2
    show guy neutral 
    show rainy
    camera:
        subpixel True pos (-1719, 1818) zoom 1.96 
    
    with Dissolve (3.0)

    play music amb_rain fadein 3.0 fadeout 3.0
    pause 3.0
    "My brethren and foes surround me, united in death."    
    "Their bloodied weapons cleaned by the rain, left to rust."
    "Tents stood abandoned with tattered sleeping mats."
    "Few still hold onto life yet lack the strength to move."
    "They wait for rescue, but the victors have already moved on."

    camera at lightning_lighting
    $ renpy.with_statement(vpunch)
    pause(1.5)
    "Nobody is coming back for us."

    window hide
    pause(1.5)
    "...God, can you hear me?"

    "I know I've never kept up with prayer before."
    "...I never thought I'd need it."
    "But you're my last hope now."
    window hide
    camera:
        subpixel True 
        pos (-1719, 1818) 
        linear 3.00 pos (-657, 360) 
    with Pause(3.10)
    camera:
        pos (-657, 360) 
    #TODO: something where he dosent even know if he still has his arm here

    "He exhales shakily."

    window hide
    camera:
        subpixel True 
        pos (-657, 360) zoom 1.96 
        linear 4.00 pos (0, 1080) zoom 1.0 
    with Pause(4.10)
    camera:
        pos (0, 1080) zoom 1.0 
    window show

    "My family's been in the countryside for as long as time can tell."
    "I swear, I was helping with harvest before I could even stand..."
    "My momma always snuck me extra food, hoping I'd grow bigger than my pops."

    show guy smile with Dissolve(0.5)
    "And I guess she got her wish."

    pause (1.5)
    show guy neutral with Dissolve(0.5)
    "When the invasion started, I didn't care about it."

    "I was in my own world, and everything else didn't matter."
    "But then it came to take me with it, forced me to go..."
    "If my momma ever taught me anything, it's that things worth doing are worth doing well."

    pause (1.5)
    show guy smile with Dissolve(0.5)
    "I've always been a stickler for the rules."

    "Listening gets you far in the ranks."
    "I was put in charge of a squadron."
    "And I led them all around doing whatever task I had."

    show guy neutral with Dissolve(1.5)
    "I was just parroting commands, and we all were executing someone else's grand scheme."

    "I never thought too far into it; it was almost like a game. "
    "Each success I had was just... me earning points."
    "It didn't matter what I destroyed or who I killed because it was just events in my story."
    "Just like the grand knight tales I was raised on."

    show guy angry with Dissolve(0.5)
    "People who opposed me deserved what happened to them..."

    "The second they chose the wrong side, they were fated to die."
    "Without them... I'd still be with my family, working the summers away and lazing through the winters."

    show guy neutral with Dissolve(0.5)
    "But about a week ago, something changed in my mind."

    "You see, there is a small village near the border..."
    "Well, small as in there weren't many people..."
    "But their fields were grand."
    "Each field could fit at least ten of my fields at home..."
    "However, they were ill-fated to feed those bastardly invaders. "
    "And so, with my luck, my next task was to destroy them."

    show guy angry with Dissolve(1.5)
    pause(1.0)
    "And... I did."
    
    "I've seen my fair share of the war's horrors."
    "I've killed people with my own hands, and I've seen people lose everything."
    "I've seen injuries and ailments not even fiction would have the soul to tell."
    "But none of it felt real until then."

    pause (1.5)
    "The fields were burned to the ground, and the sky was painted black with their cinders."

    show guy neutral with Dissolve(0.5)
    "...The smell reminded me of my father's cooking."

    pause (1.5)
    "The fire spread from the fields to the houses, and it didn't take long for the whole village to be engulfed."

    "Right before I left, I watched a cottage collapse."
    "The wooden beams turned to ash, and the rest of the building crumpled after."

    show guy angry with Dissolve(0.5)
    "There was a man still in there."

    "But then, all I could see was his head and arm."
    "He must have been gone for a while; his face was already pale."
    "But he looked like an ordinary man."
    "I'd seen someone like him thousands of times before."
    "It felt like his blank and lifeless eyes bore into mine."
    "I couldn't meet his gaze anymore."
    "His arm stood out of the rubble, bent the wrong way..."
    "His flesh blackened and flaked away."
    "Like the burnt firewood I'd cleaned from the stoves after cold winter nights."
    "Crackling and..."
    "And..."
    "When all of my memories go, his face will be the last one I see."

    show guy neutral with Dissolve(1.5)
    pause (1.5)
    "I can't help but wonder if in another life that was me."

    "If I stayed in the peace of my home, would a war find me..."
    "Would I be burned beneath my house?"
    "I can't shake the cruelty of it."
    "I have no way of knowing if that person was even aligned with the invaders."
    "Would it matter if he were?"
    "I just know I fated him to a cruel death."
    "And many, many, many, more."
    "If not for this wound, I'd be preparing for another attack right now."
    "Another bread basket to burn..."

    show guy angry with Dissolve(0.5)
    "But I can't..."

    "I look at my enemies now and see myself."
    "Many have already died because of my willful ignorance."

    show guy neutral with Dissolve(0.5)
    "I'm sorry I failed to see that until now."

    "{cps=20}I know what I've done.{/cps}"
    "{cps=17}I know what I deserve.{/cps}"
    "{cps=15}But if I die here, it will never end.{/cps}"
    "{cps=8}So please...{/cps}"
    "{cps=4}{shader=jitter}Give me the strength.{/shader}{/cps}"
menu: 
    "You've earned your rest now.":
        show guy smile with Dissolve(0.5)
        "His head perks up one more time, and he stares into the sky."

        "The rain pounds against his face."
        "Each drop rolls down to the gaping wound in his arm."
        "His blood slowly pools around him."
        "A daze steals his consciousness away..."

        stop music
        scene blackBG with Dissolve(3.5)
        "His posture loosens at first, then he crumples forward into the mud."

        "His last thoughts were prayers: Let his next life be peaceful, and let his family be safe."
        "Justice had finally caught him."
        pause(1.5)
    "Wreak your redemption on the world.":
        "His body explodes with vitality."
        "His arm, once spewing blood, had mended."

        show guy smile with Dissolve(0.5)
        "He inspects his arm, then looks towards the heavens with a wry smile." 
        "Using his sword, he stumbles back onto his feet."
        
        stop music
        scene blackBG with Dissolve(3.5)
        "Forward on he marches."
        "Along his path, he finds a wounded invader clinging to life like he was moments ago."
        "After a moment of hesitation, he picked the soldier up and kept moving forward. "
        "This mercy won't go to waste."
        pause(1.5)
    
#end game   
return
