init python:
    import random
##############################################################################
#This function is optional. Only include it if you want automatic pauses between punctuation
    def typography(what):
        replacements = [
                ('. ','. {w=.25}'), # Moderate pause after periods
                ('? ','? {w=.25}'), # Long pause after question marks
                ('! ','! {w=.25}'), # Long pause after exclamation marks
                (', ',', {w=.25}'), # Short pause after commas
        ]
        for item in replacements:
            what = what.replace(item[0],item[1])
        return what
    config.say_menu_text_filter = typography # This ensures the text block has the same ID value, even after all the replacements are made
##############################################################################

##############################################################################

##############################################################################
# This function is an alternative to the above "text_sounds" function. This one plays text sounds at a rate that is based on the current CPS. 
# A slower CPS means that the sounds play at a slower rate. A faster CPS means the sounds play at a faster rate.
# The current limitation with this function, is that it can only handle one text speed per dialog block. It cannot switch between speeds within the same dialog block.
# You need to begin a dialog block with a {cps=} tag in order for this function to use that speed.
# Example:
#    ce "{cps=90}The text sounds will play one after another with almost no pauses in between."
#    ce "{cps=5}The text sounds will have a noticeable pause between each char"
#    ce "{cps=5}Despite the increase in character speed midway through this dialog block, {cps=190} the text sounds will remain at the lower speed. The function will only use the first instance of the CPS tag in a dialog block, and ignore the others"

init python:
    import random, re

    renpy.music.register_channel("textsound", "voice", False) # Add a new sound channel for the text sounds so that they don't overlap with anything else

    _TAG = re.compile(r'{cps=(\d+)}') # Use regex to find and store the first instance of the {cps=} tag in a character dialog block

    def adaptive_text_sounds(event, interact=True, **kw):
        if event == "show":
            renpy.sound.stop(channel="textsound")
            raw  = renpy.store._last_say_what or ""
            text = renpy.substitute(raw)
            cps  = (kw.get("slow_cps") or kw.get("cps") or renpy.store.preferences.text_cps)

            for chunk in _TAG.split(text):
                if chunk.isdigit():
                    cps = int(chunk)
                    continue
                pause = 0 if cps <= 0 else 1.0 / cps

                for char in chunk:
                    if not char.isspace():
                        renpy.sound.queue(f"audio/voice{random.randint(1,7)}.ogg",channel="textsound") # Replace "audio/popcat{random.randint(1,11)}.wav" with sound files of your choice
                    if pause:
                        renpy.sound.queue(f"<silence {pause}>", channel="textsound")

        elif event in ("slow_done", "end"):
            renpy.sound.stop(channel="textsound")

##############################################################################

# Make sure the "callback" function is the same name as our text sounds function
define n = Character(callback=adaptive_text_sounds)

##########################################
# █ █ ▄▀▄ █▀█ ▀█▀ ▄▀▄ █▄▄ █   █▀▀ █▀▀ 
# ▀▄▀ █▀█ █▀▄ ▄█▄ █▀█ █▄█ █▄▄ ██▄ ▄██ 
##########################################
default persistent.seen_warning = False

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

    add "blackBG"
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
# ▀█▀ █▄ ▄█ ▄▀▄ █▀▀ █▀▀ █▀▀ 
# ▄█▄ █ ▀ █ █▀█ █▄█ ██▄ ▄██ 
##########################################
#images
image blackBG = "images/bg/black.png"
image whiteBG = "images/bg/white.png"
image warningsign = "images/warningsign.png"
image guy neutral = "images/guy_neutral.png"
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

#transforms
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

#lightning light
transform lightning_lighting:
    matrixcolor TintMatrix("#ffffff") * BrightnessMatrix(0.0)
    0.05
    linear 0.05 matrixcolor TintMatrix("#cccff7") * BrightnessMatrix(0.3) * ContrastMatrix(1.5)
    pause 0.5
    linear 0.25 matrixcolor TintMatrix("#ffffff")  * BrightnessMatrix(0.0) * ContrastMatrix(1.0)

transform lightning_lighting_soft:
    matrixcolor TintMatrix("#ffffff") * BrightnessMatrix(0.0)
    0.05
    linear 0.05 matrixcolor TintMatrix("#cccff7") * BrightnessMatrix(0.1) * ContrastMatrix(1.2)
    pause 0.5
    linear 0.25 matrixcolor TintMatrix("#ffffff")  * BrightnessMatrix(0.0) * ContrastMatrix(1.0)


#styles
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
    
    n "The heavens weep over the remains of the battleground."

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
    n "My brethren and foes surround me{cps=5}, {/cps}united in death."    
    n "Their bloodied weapons cleaned by the rain{cps=5}, {/cps}left to rust."
    n "Tents stood abandoned with tattered sleeping mats."
    n "Few still hold onto life yet lack the strength to move."
    n "They wait for rescue{cps=5}, {/cps}but the victors have already moved on."

    camera at lightning_lighting
    play sound thunder
    $ renpy.with_statement(vpunch)
    pause(1.5)
    #safety force reset
    camera:
        matrixcolor IdentityMatrix() 
    n "Nobody is coming back for us."

    window hide
    pause(1.5)
    n ".{cps=3}..{/cps}God{cps=5}, {/cps}can you hear me?"

    n "I know I've never kept up with prayer before."
    n ".{cps=3}..{/cps}I never thought I'd need it."
    n "But you're my last hope now."
    window hide
    camera:
        subpixel True 
        pos (-1719, 1818) 
        linear 3.00 pos (-657, 360) 
    with Pause(3.10)
    camera:
        pos (-657, 360) 
    #TODO: something where he dosent even know if he still has his arm here

    n "I figure it won't be long 'till I drop now{cps=5},{/cps} everything's already spinning{cps=3}...{/cps}"

    "He exhales shakily."

    n "{cps=8}What am I doing{cps=3}...?{/cps}"

    window hide
    camera:
        subpixel True 
        pos (-657, 360) zoom 1.96 
        linear 4.00 pos (0, 1080) zoom 1.0 
    with Pause(4.10)
    camera:
        pos (0, 1080) zoom 1.0 
    window show

    n "My family's been in the countryside for as long as time can tell."
    n "I swear{cps=5}, {/cps}I was helping with harvest before I could even stand{cps=3}...{/cps}"
    n "My momma always snuck me extra food{cps=5}, {/cps}hoping I'd grow bigger than my pops."

    show guy smile with Dissolve(0.5)
    n "And I guess she got her wish."

    window hide
    pause (1.5)
    show guy neutral with Dissolve(0.5)
    n "When the invasion started{cps=5}, {/cps}I didn't care about it."

    n "I was in my own world{cps=5}, {/cps}and everything else didn't matter."
    n "But then it came to take me with it{cps=5}, {/cps}'forced me to go{cps=3}...{/cps}"
    n "If my momma ever taught me anything{cps=5}, {/cps}it's that things worth doing are worth doing well."

    window hide
    pause (1.5)
    show guy smile with Dissolve(0.5)
    n "I've always been a stickler for the rules."
    n "Listening gets you far in the ranks."
    camera at lightning_lighting_soft
    play sound thunder volume(0.5)
    $ renpy.with_statement(vpunch)
    pause(1.5)
    #safety force reset
    camera:
        matrixcolor IdentityMatrix() 
    n "I was put in charge of a squadron."
    n "And I led them all around doing whatever task I had."

    show guy neutral with Dissolve(1.5)
    n "I was just parroting commands{cps=5}, {/cps}and we all were executing someone else's grand scheme."

    n "I never thought too far into it{cps=5}; {/cps} it was almost like a game. "
    n "Each success I had was just{cps=3}...{/cps} me earning points."
    n "It didn't matter what I destroyed or who I killed because it was just events in my story."
    n "Just like the grand knight tales I was raised on."

    show guy angry with Dissolve(0.5)
    n "People who opposed me deserved what happened to them{cps=3}...{/cps}"

    n "The second they chose the wrong side{cps=5}, {/cps}they were fated to die."
    n "Without them{cps=3}...{/cps} I'd still be with my family{cps=5}, {/cps}working the summers away and lazing through the winters."

    show guy neutral with Dissolve(0.5)
    n "But about a week ago{cps=5}, {/cps}something changed in my mind."

    n "You see{cps=5}, {/cps}there is a small village near the border{cps=3}...{/cps}"
    n "Well{cps=5}, {/cps}small as in there weren't many people{cps=3}...{/cps}"
    n "But their fields were grand."
    n "Each field could fit at least ten of my fields at home{cps=3}...{/cps}"
    n "However{cps=5}, {/cps}they were ill-fated to feed those bastardly invaders. "
    n "And so{cps=5}, {/cps}with my luck{cps=5}, {/cps}my next task was to destroy them."
    window hide
    show guy angry with Dissolve(1.5)
    pause(1.0)
    n "And{cps=3}...{/cps} I did."
    
    n "I've seen my fair share of the war's horrors."
    camera at lightning_lighting
    play sound thunder
    $ renpy.with_statement(vpunch)
    pause(1.5)
    #safety force reset
    camera:
        matrixcolor IdentityMatrix() 
    n "I've killed people with my own hands{cps=5}, {/cps}and I've seen people lose everything."
    n "I've seen injuries and ailments not even fiction would have the soul to tell."
    n "But none of it felt real until then."

    window hide
    pause (1.5)
    n "The fields were burned to the ground{cps=5}, {/cps}and the sky was painted black with their cinders."

    show guy neutral with Dissolve(0.5)
    n ".{cps=3}..{/cps}The smell reminded me of my father's cooking."

    window hide
    pause (1.5)
    n "The fire spread from the fields to the houses{cps=5}, {/cps}and it didn't take long for the whole village to be engulfed."

    n "Right before I left{cps=5}, {/cps}I watched a cottage collapse."
    n "The wooden beams turned to ash{cps=5}, {/cps}and the rest of the building crumpled after."

    show guy angry with Dissolve(0.5)
    n "There was a man still in there."

    n "But then{cps=5}, {/cps}all I could see was his head and arm."
    n "He must have been gone for a while; his face was already pale."
    n "But he looked like an ordinary man."
    n "I'd seen someone like him thousands of times before."
    n "It felt like his blank and lifeless eyes bore into mine."
    n "I couldn't meet his gaze anymore."
    n "His arm stood out of the rubble{cps=5}, {/cps}bent the wrong way{cps=3}...{/cps}"
    n "His flesh blackened and flaked away."
    n "Like the burnt firewood I'd cleaned from the stoves after cold winter nights."
    n "Crackling and{cps=3}...{/cps}"
    n "And{cps=3}...{/cps}"
    n "When all of my memories go{cps=5}, {/cps}his face will be the last one I see."

    window hide
    show guy neutral with Dissolve(1.5)
    pause (1.5)
    n "I can't help but wonder if in another life that was me."

    n "If I stayed in the peace of my home{cps=5}, {/cps}would a war find me{cps=3}...{/cps}"
    n "Would I be burned beneath my house?"
    n "I can't shake the cruelty of it."
    n "I have no way of knowing if that person was even aligned with the invaders."
    n "Would it matter if he were?"
    n "I just know I fated him to a cruel death."
    n "And many{cps=5}, {/cps}many{cps=5}, {/cps}many{cps=5}, {/cps}more."
    n "If not for this wound{cps=5}, {/cps}I'd be preparing for another attack right now."
    n "Another bread basket to burn{cps=3}...{/cps}"

    show guy angry with Dissolve(0.5)
    n "But I can't{cps=3}...{/cps}"
    window hide
    pause(1.0)
    n "I look at my enemies now and see myself."
    n "Many have already died because of my willful ignorance."
    
    window hide
    show guy neutral with Dissolve(0.5)
    pause(1.5)
    n "I'm sorry I failed to see that until now."
    window hide
    pause(2.5)

    n "{cps=20}I know what I've done.{/cps}"
    n "{cps=17}I know what I deserve.{/cps}"
    n "{cps=15}But if I die here{cps=5}, {/cps}it will never end.{/cps}"
    n "{cps=8}So please{cps=3}...{/cps}{/cps}"
    n "{cps=3}{shader=jitter}Give me strength.{/shader}{/cps}"
    
    menu: 
        "You've earned your rest now.":
            show guy smile with Dissolve(0.5)
            "His head perks up one more time{cps=5}, {/cps}and he stares into the sky."

            "The rain pounds against his face."
            "Each drop rolls down to the gaping wound in his arm."
            "His blood slowly pools around him."
            "A daze steals his consciousness away{cps=3}...{/cps}"
            camera 
            stop music
            scene blackBG 
            with Dissolve(3.5)
            
            "His posture loosens at first{cps=5}, {/cps}then he crumples forward into the mud."

            "His last thoughts were prayers: Let his next life be peaceful{cps=5}, {/cps}and let his family be safe."
            "Justice had finally caught him."
            pause(1.5)
        "Wreak your redemption on the world.":
            "His body explodes with vitality."
            "His arm{cps=5}, {/cps}once spewing blood{cps=5}, {/cps}had mended."

            show guy smile with Dissolve(0.5)
            "He inspects his arm{cps=5}, {/cps}then looks towards the heavens with a wry smile." 
            "Using his sword{cps=5}, {/cps}he stumbles back onto his feet."
            
            camera 
            stop music
            scene whiteBG 
            with Dissolve(3.5)
            "Forward on he marches."
            "Along his path{cps=5}, {/cps}he finds a wounded invader clinging to life like he was moments ago."
            "After a moment of hesitation{cps=5}, {/cps}he picked the soldier up and kept moving forward. "
            "This mercy won't go to waste."
            pause(1.5)
    
#end game   
return
