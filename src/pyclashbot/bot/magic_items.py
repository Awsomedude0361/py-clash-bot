"""module for spending the magic items currencies that the bot tends to max out on"""

import time


from pyclashbot.bot.nav import (
    check_if_on_clash_main_menu,
    get_to_collections_page,wait_for_clash_main_menu,
    check_if_on_collection_page,
)
from pyclashbot.utils.logger import Logger
from pyclashbot.memu.client import click, screenshot
from pyclashbot.detection.image_rec import pixels_match_colors


def spend_magic_items_state(vm_index: int, logger: Logger) -> bool:
    logger.change_status("Spending magic item currencies!")

    # if not on clash main, return False
    if not check_if_on_clash_main_menu(vm_index):
        return False

    # get to magic items page
    logger.change_status("Getting to magic items page...")
    if get_to_collections_page(vm_index) is False:
        logger.change_status("Failed to get to magic items page")

    # select magic items tab
    magic_items_tab_coords = (180, 110)
    logger.log("Clicking magic items tab")
    click(vm_index, *magic_items_tab_coords)
    time.sleep(1)

    #spend currency until it doesnt work anymore
    for reward_index in [0,1,2]:
        logger.change_status(f'Spending magic item type: {reward_index}...')
        while spend_rewards(vm_index, logger,reward_index) is True:
            logger.change_status('Successfully spent magic items. Trying again...')
        logger.change_status(f'No more magic item type: {reward_index} to spend')
    logger.change_status('Done spending magic item currencies')

    # return to clash main
    print("Returning to clash main after spending magic items")
    click(vm_index, 243, 600)
    time.sleep(3)

    # wait for main
    if wait_for_clash_main_menu(vm_index, logger, deadspace_click=False) is False:
        logger.change_status("Failed to wait for clash main after upgrading cards")
        return False

    return True


def exit_spend_reward_popup(vm_index) -> bool:
    deadspace = (395, 350)
    start_time = time.time()
    timeout = 30  # s
    while not check_if_on_collection_page(vm_index):
        if time.time() - start_time > timeout:

            return False

        click(vm_index, *deadspace)
        time.sleep(1)

    return True

def spend_rewards(vm_index, logger,reward_index) -> bool:
    logger.change_status("Trying to spend the first reward...")

    #click the reward
    print("Clicking use currency button")
    if reward_index not in [0,1,2]:
        print('Invalid reward index. Must be 0, 1, or 2')
        return False

    reward_index2coord = {0:(100,300),1:(200,300),2:(300,300),}
    click(vm_index, *reward_index2coord[reward_index])
    time.sleep(1)

    # if the use button doesn't pop up, that mean's we're out of rewards to spend
    if not check_for_use_button(vm_index):
        logger.change_status("No more rewards to spend")
        exit_spend_reward_popup(vm_index)
        return False

    # click the use button
    print("Clicking use currency button")
    use_button_coord = (206, 438)
    click(vm_index, *use_button_coord)
    time.sleep(1)

    # click the first card to use it on
    print("Using it on the first card")
    first_card_coord = (80, 200)
    click(vm_index, *first_card_coord)
    time.sleep(1)

    # spend the currency
    print("Clicking confirm spend {amount} currency")
    spend_currency_coord = (200, 430)
    click(vm_index, *spend_currency_coord)

    # click deadspace
    print("Clicking deadspace until we get back to the collection page")
    exit_spend_reward_popup(vm_index)

    return True


def check_for_use_button(vm_index) -> bool:
    iar = screenshot(vm_index)
    pixels = [
        iar[428][188],
        iar[447][198],
        iar[443][208],
        iar[445][218],
        iar[438][220],
        iar[437][222],
        iar[436][224],
        iar[434][226],
        iar[432][227],
        iar[430][225],
        iar[440][223],
        iar[438][189],
        iar[448][227],
    ]
    colors = [
        [255, 131, 156],
        [204, 86, 118],
        [236, 207, 215],
        [75, 55, 61],
        [208, 173, 182],
        [255, 255, 255],
        [101, 52, 62],
        [255, 131, 156],
        [255, 131, 156],
        [255, 131, 156],
        [255, 254, 255],
        [255, 114, 149],
        [255, 108, 147],
    ]

    return pixels_match_colors(pixels, colors, tol=10)


if __name__ == "__main__":
    spend_magic_items_state(1,Logger())
