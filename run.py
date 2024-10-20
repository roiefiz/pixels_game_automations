from main import *
import httpx


def list_new_accounts_file(file_path="new_accounts.txt"):
    na = []
    with open(file_path, 'r') as na_file:
        all_lines = na_file.readlines()
        for line in all_lines:
            at_symbol = str(line).find('@')
            account_name = line[at_symbol - 8:at_symbol].strip(" ")
            na.append(account_name)
    return na


response = httpx.get(accounts_url)
my_macbook_accounts = response.json()['roi']
print(my_macbook_accounts)
print(len(my_macbook_accounts))
accounts_counter = 0
game = True
while game:
    for account in my_macbook_accounts:
        print(f'account counter on {accounts_counter}')
        account_email = account + '@mail7.io'
        m_driver = webdriver.Chrome()
        running_user = PixelsUser(my_driver=m_driver, operation_system="macOS")
        running_user.username = account
        running_user.email = account_email
        running_user.LOCATIONS = my_own_macbook_locations
        running_user.mail_for_errors.append("roiefiz@icloud.com")
        print(running_user.email)
        try:
            running_user.start_game_with_existing_account()
            while True:
                target_farm = 298
                farming_level = running_user.discover_farming_level()
                current_money = running_user.get_berry_amount()
                starting_energy = running_user.get_energy_amount()
                default_energy = 240
                missions = []
                popberry_level = 1
                butterberry_level = 2
                grainbow_level = 5
                watermint_level = 11
                if farming_level >= watermint_level:
                    if farming_level <= 12:
                        missions = [("Watermint Seeds", 301)]
                    else:
                        missions = [('Watermint Seeds', 600)]
                elif grainbow_level <= farming_level < watermint_level:
                    missions = [("Grainbow Seeds", 361)]
                elif butterberry_level <= farming_level < grainbow_level:
                    missions = [("Butterberry Seeds", 301)]
                else:
                    missions = [("Popberry Seeds", 201)]
                if starting_energy <= default_energy:
                    raise Exception("not enough energy to start with")
                # Buy seeds for the missions if needed
                for pair in missions:
                    print(f"This is missions {missions}")
                    mission_seeds = pair[0]
                    mission_required_quantity = pair[1]
                    requirements_met = False
                    checking_inventory_counter = 0
                    while not requirements_met:
                        items_to_buy = {}
                        running_user.arranged_inventory = running_user.arrange_inventory_details(item_slicer=10)
                        seeds_inventory_details = running_user.query_inventory(query=mission_seeds)
                        if bool(seeds_inventory_details):
                            print("Seeds are in the inventory")
                            current_seeds_quantity = seeds_inventory_details["quantity"]
                            if current_seeds_quantity < 65:
                                print("Need to buy more seeds")
                                amount_to_buy = mission_required_quantity - current_seeds_quantity
                                items_to_buy[mission_seeds] = amount_to_buy
                            else:
                                print("Requirement is met.")
                                requirements_met = True
                        else:
                            print("Item not even in the inventory. Should Buy it.")
                            amount_to_buy = mission_required_quantity
                            items_to_buy[mission_seeds] = amount_to_buy
                        if items_to_buy:
                            # Sell items
                            items_to_sell = {}
                            items_you_can_sell = ["Popberry", "Butterberry", "Grainbow", "Watermint"]
                            for item in items_you_can_sell:
                                if bool(running_user.query_inventory(query=item)):
                                    items_to_sell[item] = "max"
                            sleep(2)
                            running_user.make_sure_game_is_on()
                            print(f'Items to sell: {items_to_sell}')
                            if items_to_sell:
                                running_user.sell_goods(items_to_sell_dict=items_to_sell)
                            running_user.buy_goods(items_to_buy_dict=items_to_buy)
                        checking_inventory_counter += 1
                        if checking_inventory_counter >= 3:
                            statement = "Something is seriously Fucked with the buy items or inventory functions"
                            print(statement)
                            raise Exception(f"{statement}")
                stand_still = False
                # Go to the farm and initialize known adjustments
                if not stand_still:
                    running_user.go_to_farm(farm_number=target_farm)
                    print("Got here successfully!!!1")
                    sleep(5)
                    running_user.make_sure_game_is_on()
                    keyboard_move_figure('up', 3)
                    keyboard_move_figure('left', 1)
                print("Got here successfully!!!2")
                adjust_up = 0.5
                adjust_left = 0.5
                adjust_right = 0.17
                adjust_down = 0.85
                if target_farm == 298:
                    keyboard_move_figure('left', 0.5)
                    keyboard_move_figure('up', 0.5)
                    running_user.quantity_input_highlight_distance = -30
                    running_user.click_fields_offset = 65
                    running_user.clicking_fields_dict = dict(costume=(23, -90), costume1=(100, -90),
                                                             costume2=(23, -25), costume7=(100, -25),
                                                             costume3=(23, 40), costume4=(100, 40),
                                                             costume5=(23, 105), costume6=(100, 105),
                                                             costume8=(23, 170), costume9=(100, 170),
                                                             costume10=(23, 235), costume11=(100, 235))
                    running_user.get_close_to_the_soil = 3
                #  Clean the field if needed
                clear_farming_items = ["shears"]
                cleaning_counter = 1
                field_condition = running_user.discover_needed_operation()
                if field_condition == 'plant':
                    cleaning_counter = False
                elif cleaning_counter >= 2:
                    raise Exception("Cannot clean the field, probably some seeds are still being loaded")
                else:
                    cleaning_counter += 1
                    if field_condition == "empty":
                        soil_color = running_user.COLORS["empty_soil_color"]
                    else:
                        soil_color = running_user.COLORS["worked_on_soil_color"]
                    slicing = 1
                    for operation in clear_farming_items:
                        item_inventory_location = running_user.query_inventory(operation)["inventory_location"]
                        running_user.click_on_all_the_field(distance_field=0.27, soil_color=soil_color,
                                                            item_name=operation,
                                                            inventory_location=item_inventory_location,
                                                            up=adjust_up,
                                                            left=adjust_left, down=adjust_down, right=adjust_right)
                        keyboard_move_figure('left', 1.5)
                # Do the missions
                ending_energy = 240
                for mission_pair in missions:
                    mission_seeds = mission_pair[0]
                    current_seeds_quantity = running_user.query_inventory(query=mission_seeds)["quantity"]
                    if mission_seeds == "Popberry Seeds":
                        slicer = 3
                        if len(missions) == 1:
                            energy_break = 240
                        else:
                            energy_break = 500

                        spins_on_farm = int(current_seeds_quantity // 60)
                    else:
                        ending_energy = 900
                        slicer = 2
                        spins_on_farm = 1
                        energy_break = 240
                    farming_items = [mission_seeds, "water_can", "shears"]
                    for spin in range(spins_on_farm):
                        if running_user.get_energy_amount() >= energy_break:
                            for operation in farming_items[:slicer]:
                                if operation == "shears":
                                    sleep(25)
                                if operation == mission_seeds:
                                    soil_color = running_user.COLORS["empty_soil_color"]
                                else:
                                    soil_color = running_user.COLORS["worked_on_soil_color"]
                                item_inventory_location = running_user.query_inventory(query=operation)[
                                    "inventory_location"]
                                running_user.click_on_all_the_field(distance_field=0.27, soil_color=soil_color,
                                                                    item_name=operation,
                                                                    inventory_location=item_inventory_location,
                                                                    up=adjust_up, left=adjust_left, down=adjust_down,
                                                                    right=adjust_right)
                                keyboard_move_figure('left', 1.5)
                running_user.make_sure_game_is_on()
                username_index = my_macbook_accounts.index(running_user.username)
                if running_user.get_energy_amount() <= ending_energy:
                    end_money = running_user.get_berry_amount()
                    end_level = running_user.discover_farming_level()
                    username_index = my_macbook_accounts.index(running_user.username)
                    with open(file='running_accounts.text', mode='a') as running:
                        running.write(
                            f'username_mail: {running_user.email},'
                            f' berry amount: {end_money},'
                            f' time: {str(datetime.now().today())[:19]},'
                            f' farming level: {end_level}'
                            f' index: {username_index}\n')
                    sleep(2)
                    pyautogui.click(running_user.LOCATIONS["log_out_button_location"])
                    sleep(3)
                    running_user.driver.quit()
                    break
        except Exception as unexpected_error:
            running_user.record_error(
                f'Unexpected_error {unexpected_error} {running_user.username}, notifier {running_user.errors_notifier}')
            running_user.driver.quit()
        else:
            continue
        finally:
            accounts_counter += 1
            continue
