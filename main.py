from module import modul, envfile, envwebchat, action, envreport


def main():
    """ Initialize.... """
    modul.initialize("Initialize ...")

    """ Time Starting.. """
    today, time = modul.todays()
    start = modul.start_time()
    id_test = modul.id_test()

    # report name
    report_filename = "Test Knowledge Base 100"

    # Logging
    modul.setup_logging(report_filename, id_test)

    print("Test ID : ", id_test, "\n")
    print("Day : ", today)
    print("Start Time : ", time, "\n")

    """ URL/s Test Area """
    # url = "https://chat.botika.online/c73kOrB" # BRINS DEV
    url = "https://chat.botika.online/tpUyiey"

    """ Filename Assets """
    csv_file  = "kb_asuransi_100"
    json_file = "kb_asuransi_100"
    

    """ Detail of test """
    tester_name = modul.tester("Ahmad Nur Brasta")
    greeting = "Hai"
    name = "Tester Props"
    email = "tester.props@gmail.com"
    phone = "08999999999"
    
    """" Choose Browser """
    browser = "chrome"
    # browser = "edge"
    
    # browser = "firefox"

    """ Convert CSV to JSON """
    envfile.convert(csv_file, json_file)

    """ Read JSON """
    json_data = envfile.read_json(json_file)

    """ Read Browser """
    driver, title_page, browser_name = modul.read_browser(url, browser)

    """ Check Available Pre-chat Form """
    envwebchat.prechat_form(driver, greeting, name, email, phone)

    """ Action Run """
    action.actions(driver, json_data, report_filename, id_test, time, today, tester_name, url, title_page, browser_name, browser)


    end = modul.end_time(start)
    today, time = modul.todays()
    print("End Time : ", time)
    print("Duration : ", end, "\n")

    # Write End Time And Duration Summary
    envfile.write_end_time_summary(time, end, report_filename, id_test)
    
    """ Generate Report """
    envreport.report(report_filename, id_test)

    modul.test_done("Test  Done!")
    print("Thank you, Have a great day!😎 \n")

if __name__ == "__main__": 
    main()