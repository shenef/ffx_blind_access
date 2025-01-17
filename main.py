# Libraries and Core Files
import logging
import sys
import time

# This needs to be before the other imports in case they decide to log things when imported
import log_init
import reset
from area import dream_zan
from avina_event import special, trigger
from avina_event.map_change import map_description
from avina_event.message import handle_message
from avina_speech.tts import speak
from keyboard import battle_controls, controls

# This sets up console and file logging (should only be called once)
log_init.initialize_logging()

logger = logging.getLogger(__name__)

import config
import load_game
import memory.main
import save_sphere
import vars

msg_queue = vars.msg_handle()
import xbox
from gamestate import game

FFXC = xbox.controller_handle()


def configuration_setup():
    game_vars = vars.vars_handle()
    msg_queue = vars.msg_handle()
    # Open the config file and parse game configuration
    # This may overwrite configuration above
    config_data = config.open_config()
    # gamestate
    game.state = config_data.get("gamestate", "none")
    game.step = config_data.get("step_counter", 1)


def memory_setup():
    # Initiate memory reading, after we know the game is open.
    try:
        logger.debug("Connecting")
        memory.main.start()
        logger.debug("Connected to memory")
    except:
        return False
    try:
        # Main
        if memory.main.get_map() not in [23, 348, 349]:
            reset.reset_to_main_menu()

        logger.info("Game start screen")
        return True
    except:
        reset.reset_to_main_menu()
        logger.info("Game start screen")
        return True


def load_game_state():
    # loading from a save file
    load_game.load_into_game(gamestate=game.state, step_counter=game.step)
    game.start_time = logs.time_stamp()


def maybe_create_save(save_num: int):
    game_vars = vars.vars_handle()
    if game_vars.create_saves():
        save_sphere.touch_and_save(
            save_num=save_num, game_state=game.state, step_count=game.step
        )


def launch_game(filename: str = "none"):
    logger.debug("Attempting to launch game")
    import os

    if filename == "none":
        filename = "C:\\'Program Files (x86)'\\Steam\\steamapps\\common\\'FINAL FANTASY FFX&FFX-2 HD Remaster'\\FFX.exe"
    logger.debug(f"File path: {filename} -config filename")
    os.system(filename)


def perform_avina():
    game_vars = vars.vars_handle()
    game.state = "intro"

    # Original seed for when looping

    while game.state != "End":
        try:
            # Start of the game, start of Dream Zanarkand section
            if game.state == "intro":
                # speak("Hello. I am a virtual intelligence named Aveena.")
                # speak("I will be your guide to playing Final Fantasy 10.")
                game.state = "config"

            if game.state == "config":
                # Set up gamestate and rng-related variables
                configuration_setup()
                game.state = "launch"

            if game.state == "launch":

                # Initialize memory access
                while not memory_setup():
                    speak("Something is wrong, the game is not running.")
                    # speak("I'll try to fix this. One moment.")
                    # launch_game()
                    # Launch Game not yet working
                    time.sleep(5)
                speak("I am now connected to the game.")
                game.state = "check_tutorial"

            if game.state == "check_tutorial":
                # speak("Would you like a quick tutorial on how I work?")
                # speak("Press Y for tutorial, or any key to proceed, then press enter.")
                if input("Awaiting decision ").lower() == "y":
                    from avina_speech import guide

                    guide.tutorial()
                game.state = "new_game"

            if game.state == "new_game":
                # speak("Would you like to start a new game?")
                # speak("Press N for new or L for load, then press enter.")
                response = input("Awaiting decision ").lower()
                if response == "n":
                    speak("Starting new game.")
                    dream_zan.new_game(gamestate="none")
                    dream_zan.new_game_2()
                    speak("New game starting now.")
                    game.state = "story"
                elif response == "l":
                    speak("Loading the most recent save.")
                    dream_zan.new_game(gamestate="load")
                    load_game.load_into_game(gamestate="last", step_counter="none")
                    game.state = "overworld"
                controls.start()

            if game.state == "story":
                pass
                # speak("story")

            if game.state == "battle":
                speak("Battle is now active.")
                controls.stop()
                battle_controls.start()
                while not avina_event.battle.battle_complete():
                    pass
                battle_controls.stop()
                controls.start()

            if game.state == "overworld":
                next_event = trigger.new_event()
                while next_event == "overworld":
                    next_event = trigger.new_event()

            if game.state == "map":
                map_description()

            if "special" in game.state:
                if game.state == "special_name_aeon":
                    logger.debug("Naming aeon.")
                    controls.stop()
                    memory.main.wait_frames(15)
                    special.name_aeon()
                    controls.start()
                elif game.state == "special_message":
                    # from avina_event.message
                    handle_message()

            if game.state == "wait":
                pass

            # Determine the next state of the game.
            game.state = trigger.new_event()

            # End of game section
            if game.state == "End":
                speak("Thank you for playing Final Fantasy 10 with me.")
                speak("Good bye.")

        except KeyboardInterrupt as e:
            logger.info("Keyboard Interrupt - Exiting.")
            speak("Keyboard Interrupt - Exiting.")
            logging.exception(e)
            sys.exit(0)


def write_final_logs():
    if memory.main.get_story_progress() > 3210:
        end_time = logs.time_stamp()
        total_time = end_time - game.start_time
        logs.write_stats("Total time:")
        logs.write_stats(str(total_time))
        logger.info(f"The game duration was: {str(total_time)}")
        logger.info("This duration is intended for internal comparisons only.")
        logger.info("It is not comparable to non-TAS runs.")
        memory.main.wait_frames(30)
        logger.info("--------")
        logger.info("In order to conform to the speedrun.com/ffx ruleset,")
        memory.main.wait_frames(60)
        logger.info("we now wait until the end of the credits and open")
        memory.main.wait_frames(60)
        logger.info("the Load Game menu to show the last autosave.")

        while memory.main.get_map() != 23:
            if memory.main.get_map() in [348, 349]:
                xbox.tap_start()
            elif memory.main.cutscene_skip_possible():
                xbox.skip_scene()
        memory.main.wait_frames(180)
        while not memory.main.save_menu_open():
            xbox.tap_b()

    memory.main.end()

    logger.info("Automation complete. Shutting down. Have a great day!")


# Main entry point of TAS
if __name__ == "__main__":
    # Load up vars.py
    vars.init_vars()

    # Next, check if we are loading to a save file
    # if game.state != "none":
    #    load_game_state()

    # Run the TAS itself
    perform_avina()

    # Finalize writing to logs
    write_final_logs()
