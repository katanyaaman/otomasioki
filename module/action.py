import time
from module import modul, envwebchat, envstatus, envfile, envreport, envfolder, envllmscore, envllmscoreeeee
from module.modul import log_function_status


@log_function_status
def actions(driver, json_data, report_filename, id_test, time, today, tester_name, url, title_page, browser_name, browser):

    # duration start test
    start = modul.start_time()
    
    
    class_name = "message-content-wrapper"
    content = "content"

    title = "📖 Read Question and send to webchat"
    modul.show_loading(title)
    print("\n")

    # calculate total intent
    count_per_element_title = [sum(1 for key in item.keys() if key.startswith("title")) for item in json_data]
    title_counter = sum(count_per_element_title)

    # calculate total sample_text
    count_per_element_question = [sum(1 for key in item.keys() if key.startswith("pertanyaan")) for item in json_data]
    question_count = sum(count_per_element_question)

    # Initiate Intent Count
    intent_count = 0

    for element in json_data:
        # refresh browser
        modul.refresh(driver)
        modul.wait_time(3)
        
        # calculate duration per intent
        duration_perquestion = modul.start_time()
        total_duration_perintent = []

        # animation change intent
        modul.show_loading(element["title"])
        print("\n")

        # loop sampletext
        count= 0
        for key, value in element.items():
            # read sample text
            if key.startswith("pertanyaan") and value is not None and value != "":
                #increment count for each sample text
                count += 1


                # duration per sample text
                # count = int(key.split("sample_text")[1])

                duration_perquestion = modul.start_time()

                question = value
                envwebchat.send_message(driver, question)
                envwebchat.wait_reply(driver, class_name, content, question)
                
                # Refresh browser setiap kelipatan sample text 3
                if count % 3 == 0:
                    modul.wait_time(2)
                    modul.refresh(driver)

                # take screenshot
                image_capture = envreport.take_screenshot(driver, id_test, key, question)
                image_capture = image_capture.replace('report/', '')
                # print(image_capture)
                
            
                # get reply bot
                respond_bot = envwebchat.get_reply_chat(driver, class_name, content, question, message_content="message-content")
                respond_bot = "\n".join(respond_bot).strip()
                respond_bot = envstatus.respond_bot_correction(respond_bot)

                # animation wait done per sample text
                title = f"{key} : {question}"
                modul.show_loading_sampletext(title)
                

                # get response csv
                respond_csv = str(element["context"]).strip()
                respond_csv = envstatus.respond_csv_correction(respond_csv)
                

                # end_duration_persampletext
                end_duration_persampletext = modul.end_time(duration_perquestion)

                # checking comparation string
                compare_strings = envstatus.compare_strings(respond_bot, respond_csv)
                
                # checking different word
                diff_strings = envstatus.diff_strings(respond_bot, respond_csv)

                # checking score probability
                probability = envstatus.probability(respond_bot, respond_csv)

                # checking status
                # status = envstatus.status(probability)

                # skor, output explanation llm
                skor, output, explanation, AI = envllmscore.llm_score(respond_bot, respond_csv)
                
                status = envstatus.status(skor)


                data_bot = {
                        "no": element["no"],
                        # "id": element["id"],
                        # "parent_id": element["parent_id"],
                        # "intent_name": element["intent_name"],
                        "title": element["title"],
                        "question": question,
                        "response_kb": respond_csv,
                        "response_llm": respond_bot,
                        "status": status,
                        # "probability": probability,
                        # "diff_strings": diff_strings,
                        # "compare_result": compare_strings,
                        "duration": end_duration_persampletext,
                        "image_capture": image_capture,
                        "skor": skor,
                        # "output_llm": output,
                        "explanation": explanation
                    }
                
                # write json file to save data_text

                envfile.write_json_data_bot(data_bot, report_filename, id_test)
           
                
                

                # calculating status pass/failed
                pass_count, failed_count = envstatus.calculate(report_filename, id_test)

                data_summary = {
                    "id_test" : id_test,
                    "tester_name" : tester_name,
                    "ai_evaluation" : AI,
                    "url" : url,
                    "page_name" : title_page,
                    "browser_name" : browser_name,
                    "date_test" : today,
                    "start_time_test" : time,
                    "total_title" : title_counter,
                    "total_question" : question_count,
                    "success" : pass_count,
                    "failed" : failed_count
                }

                # write json file to save data_summary
                envfile.write_json_data_summary(data_summary, report_filename, id_test)
                
                # Generate Report
                envreport.report_action(report_filename, id_test)
                
               
            else:
                continue
            


        # end_duration_perintent 
        end_duration_pertitle = modul.end_time(duration_perquestion)

        chart = {
            element["title"] : end_duration_pertitle
        }

        # write json file to save data_chart
        envfile.write_json_chart(chart, report_filename, id_test)

        print("\n")
        print("⏳ Total duration Topic", element["title"], " : ", end_duration_pertitle, "\n")
        
        intent_count += 1
        browser = False
        if intent_count % 20 == 0 and intent_count != len(json_data):
            greeting = "Hai"
            name = "Tester Props"
            email = "tester.props@gmail.com"
            phone = "08999999999"
            browser = "chrome"
            
            modul.close_browser(driver)
            
            # Buka browser baru
            driver, title_page, browser_name = modul.read_browser(url, browser)
            envwebchat.prechat_form(driver, greeting, name, email, phone)
            browser = True
        elif intent_count == len(json_data):
            if browser == True:
                print("Continous Topic Test")
                modul.close_browser(driver)
                break
            else:
                print("🎯 Last Topic \n")
                modul.close_browser(driver)
                continue
        else:
            continue

    
        # envllmscoreeeee.run_scoring(data_bot, report_filename, id_test)

    duration_test = modul.end_time(start)

    data_summary = {
        "id_test" : id_test,
        "tester_name" : tester_name,
        "ai_evaluation" : AI,
        "url" : url,
        "page_name" : title_page,
        "browser_name" : browser_name,
        "date_test" : today,
        "start_time_test" : time,
        "total_title" : title_counter,
        "total_question" : question_count,
        "success" : pass_count,
        "failed" : failed_count,
        # "duration": duration_test
    }
    
    # write json file to save data_summary
    envfile.write_json_data_summary(data_summary, report_filename, id_test)


    # total_duration_perintent.append(end_duration_perintent)
    # print("Total duration all intent", total_duration_perintent)
