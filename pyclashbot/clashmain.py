import time

import numpy
import pyautogui

from client import click, screenshot, scroll_down
from image_rec import (check_for_location, find_references, get_first_location,
                       pixel_is_equal)


#Method for waiting for the clash main menu to appear after loading
def wait_for_clash_main_menu(logger):
    waiting=True
    n=0
    loops=0
    while waiting:
        loops+=1
        if loops>100:
            logger.log("Waited too long for clash main menu to appear")
            return "restart"
        handle_puzzleroyale_popup(logger)
        n=n+1
        logger.log(str("Waiting for clash main menu to appear: " + str(n)))
        time.sleep(1)
        waiting=not(check_if_on_clash_main_menu())
    time.sleep(3)
    logger.log("Done waiting for clash main menu to appear.")
        
#Method to handle puzzleroyale popup
def handle_puzzleroyale_popup(logger):
    if look_for_puzzleroyale_popup():
        logger.log("Handling puzzle royale popup")
        click(366,121)
        time.sleep(3)

#Method to check for puzzleroyale popup
def look_for_puzzleroyale_popup():
    iar=numpy.asarray(screenshot())
    
    pix_list=[
        iar[173][102],
        iar[290][96],
        iar[154][312],
    ]
    
    color = [244,183,118]
    
    #print(pix_list)
    

    for pix in pix_list:
        if not(pixel_is_equal(pix,color,tol=45)):
            return False
    return True

#Method to check if the clash main menu is on screen
def check_if_on_clash_main_menu():
    iar = numpy.asarray(screenshot())

    blue_pix_list = [iar[447][390], iar[391][37]]
    yellow_pix_list = [iar[427][98], iar[468][97], iar[472][192]]
    blue_sentinel=[ 22,70,159]
    yellow_sentinel=[255,187,0]

    for pix in blue_pix_list:
        if not(pixel_is_equal(pix,blue_sentinel,tol=50)):
            return False


    for pix in yellow_pix_list:
        return bool((pixel_is_equal(pix,yellow_sentinel,tol=50)))
    
#Method to change account to the given account number using the supercell ID login screen in the options menu in the clash main menu
def get_to_account(logger,account_number):
    handle_gold_rush_event(logger)
    time.sleep(2)

    logger.log("Opening settings")
    click(x=364, y=99)
    time.sleep(3)

    logger.log("Clicking switch button")
    click(x=198, y=401)
    time.sleep(3)

    if account_number == 0:
        logger.log("Clicking account 1")
        click(x=211, y=388)
    if account_number == 1:
        logger.log("Clicking account 2")
        click(x=193, y=471)
    if account_number == 2:
        logger.log("Clicking account 3")
        click(x=200, y=560)

    time.sleep(3)

    if wait_for_clash_main_menu(logger) == "restart":
        return "restart"


    # handling the various things notifications and such that need to be
    # cleared before bot can get going
    time.sleep(0.5)
    handle_gold_rush_event(logger)
    time.sleep(0.5)
    handle_new_challenge(logger)
    time.sleep(0.5)
    handle_special_offer(logger)
    time.sleep(0.5)
    handle_card_mastery_notification()
    time.sleep(0.5)
     
#Method to see if a gold rush event is happening on the clash main menu
def check_for_gold_rush_event():
    references = [
        "1.png",
        "2.png",
        "3.png",
        "4.png",
    ]
    locations = find_references(
        screenshot=screenshot(),
        folder="gold_rush_event",
        names=references,
        tolerance=0.97
    )
    loc = get_first_location(locations)
    return loc is not None

#Method to handle a gold rush event notification obstructing the bot
def handle_gold_rush_event(logger):
    logger.log(
        "Handling the possibility of a gold rush event notification obstructing the bot.")
    time.sleep(0.5)
    pyautogui.click(193, 465)
    time.sleep(0.5)
    pyautogui.click(193, 465)
    time.sleep(0.5)

#Method to handle a new challenge notification obstructing the bot
def handle_new_challenge(logger):
    logger.log(
        "Handling the possibility of a new challenge notification obstructing the bot.")
    time.sleep(0.5)
    click(376, 639)
    time.sleep(0.5)
    click(196, 633)
    time.sleep(0.5)
    if check_if_on_trophy_progession_rewards_page():
        click(212, 633)
        time.sleep(0.5)

#Method to handle a special offer notification obstructing the bot
def handle_special_offer(logger):
    logger.log(
        "Handling the possibility of special offer notification obstructing the bot.")
    time.sleep(0.5)
    click(35, 633)
    time.sleep(0.5)
    click(242, 633)
    time.sleep(0.5)
    if check_if_on_trophy_progession_rewards_page():
        click(212, 633)
        time.sleep(0.5)

#Method to check if the bot is on the trophy progression rewards page in the given moment
def check_if_on_trophy_progession_rewards_page():
    iar=numpy.asarray(screenshot())
    pix_list=[
        iar[629][240],
        iar[631][185],
        iar[621][232],
    ]
    color=[78,175,255]
    
    #print(pix_list)
    
    for pix in pix_list:
        if not(pixel_is_equal(pix,color,tol=35)):
            return False
    return True

#Method to handle the chest unlocking on the clash main menu
def open_chests(logger):
    #unlock coord (210, 455)
    #chest 1 coord (78, 554)
    #chest 2 coord (162,549)
    #chest 3 coord (263,541)
    #chest 4 coord (349 551)
    #dead space coord (20, 556)
    #check_if_unlock_chest_button_exists()
    logger.log("Opening chests")

    chest_coord_list=[[78, 554],[162,549],[263,541],[349,551]]

    chest_index=0
    for chest_coord in chest_coord_list:
        chest_index=chest_index+1
        logger.log(str("Checking chest slot "+str(chest_index)))
        #click chest
        click(chest_coord[0],chest_coord[1])
        time.sleep(1)

        if check_if_unlock_chest_button_exists():
            print("Found unlock in chest", chest_index)
            time.sleep(0.5)

            logger.log(str(f"Unlocking chest {str(chest_index)}"))
            time.sleep(0.5)
            click(210, 465)

        else:
            logger.log("Handling possibility of rewards screen")
            for _ in range(10):
                click(20,556)
            time.sleep(3)
            

        #close chest menu
        click(20,556)
        time.sleep(0.33)

#Method for checking if the unlock chest button exists in the menu that appears when clicking a chest
def check_if_unlock_chest_button_exists():
    current_image = screenshot()
    reference_folder = "unlock_chest_button"
    references = [
        "1.png",
        "2.png",
        "3.png",
        "4.png",
        "5.png",
        "6.png",
        "7.png",
        "8.png",
        "9.png",
        "10.png",
        "11.png",

    ]

    locations = find_references(
        screenshot=current_image,
        folder=reference_folder,
        names=references,
        tolerance=0.90
    )

    return any(location is not None for location in locations)

#Method to start a 2v2 quickmatch through the party mode through the clash main menu
def start_2v2(logger):
    logger.log("Initiating 2v2 match from main menu")
    
    logger.log("Clicking party mode")
    time.sleep(1)
    click(284,449)
    time.sleep(1)
    
    if find_and_click_2v2_quickmatch_button(logger)=="restart": return "restart"
    
    check_for_reward_limit()
    
#method to find and click the 2v2 quickmatch button in the party mode menu
def find_and_click_2v2_quickmatch_button(logger):
    #starts in the party mode
    #ends when loading a match
    logger.log("Finding and clicking 2v2 quickmatch button")
    #repeatedly scroll down until we find coords for the 2v2 quickmatch button
    coords = None
    loops=0
    while coords is None:
        loops+=1
        if loops>20:
            logger.log("Could not find 2v2 quickmatch button, restarting")
            return "restart"
        scroll_down()
        time.sleep(1)
        coords=find_2v2_quick_match_button()
    time.sleep(2)
    #once we find the coords, click them
    click(coords[0],coords[1])
    logger.log("Done queueing a 2v2 quickmatch")

#Method to check for the reward limit popup notification and close it
def check_for_reward_limit():
    references = [
        "1.png",
        "2.png",
        "3.png",
        "4.png",
        "5.png"
    ]

    locations = find_references(
        screenshot=screenshot(),
        folder="reward_limit",
        names=references,
        tolerance=0.97
    )

    for location in locations:
        if location is not None:
            click(211, 432)

            return True
    return False

#method to find the 2v2 quickmatch button in the party mode menu
def find_2v2_quick_match_button():
    current_image = screenshot()
    reference_folder = "2v2_quick_match"
    references = [
        "1.png",
        "2.png",
        "3.png",
        "4.png",
        "5.png",
        "6.png",
        "7.png",
        "8.png",
        "9.png",
        "10.png",
        "11.png",
        "12.png",
    ]

    locations = find_references(
        screenshot=current_image,
        folder=reference_folder,
        names=references,
        tolerance=0.97
    )
    
    coord= get_first_location(locations)
    if coord is None: return None
    return [coord[1]+200,coord[0]+50]

#Method to wait for a the loading sequence of a battle to finish
def wait_for_battle_start(logger):
    logger.log("Waiting for battle start. . .")
    in_battle = False
    loops = 0

    while in_battle == False:
        if check_if_in_battle(): in_battle = True
        click(100, 100)
        time.sleep(0.25)
        loops += 1
        if loops > 120:
            logger.log("Waited longer than 30 sec for a fight")
            return "restart"

#Method to check if the bot is in a battle in the given moment
def check_if_in_battle():
    for _ in range(10):
        references = [
            "1.png",
            "2.png",
            "3.png",
            "4.png",
            "5.png"
        ]

        locations = find_references(
            screenshot=screenshot(),
            folder="check_if_in_battle",
            names=references,
            tolerance=0.97
        )

        if check_for_location(locations): return True
        time.sleep(1)
    return False

#Method to handle the possibility of a card mastery notification obstructing the bot
def handle_card_mastery_notification():
    click(107,623)
    time.sleep(1)
    
    click(240,630)
    time.sleep(1)
    
    