from booking.booking import Booking
from selenium import webdriver

# TODO: add logging, and better way to deal with popup

place = input("Input location where you want to go: ")
check_in_date = input("Check in date (yyyy-mm-dd): ")
check_out_date = input("Check out date (yyyy-mm-dd): ")
adults_num = int(input("Number of adults (integer): "))

try:
    bot = Booking(detach=True, disable_logging=True)
    bot.land_first_page()
    # remove sign in popup
    bot.close_popup()
    bot.change_currency(currency="EUR")
    bot.select_place_to_go(place=place)
    bot.select_dates(check_in_date=check_in_date,
                    check_out_date=check_out_date)
    bot.select_adults(adults_num)
    bot.do_search()
    bot.apply_filters()
    bot.refresh() # to make sure we scrape needed data
    bot.report_results()
    
except Exception as e:
    if 'in PATH' in str(e):
        print(
            'You are trying to run the bot from command line \n'
            'Please add to PATH your Selenium Drivers \n'
            'Windows: \n'
            '    set PATH=%PATH%;C:path-to-your-folder \n \n'
            'Linux: \n'
            '    PATH=$PATH:/path/toyour/folder/ \n'
        )
    else:
        raise e