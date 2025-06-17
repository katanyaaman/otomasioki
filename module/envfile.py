import csv
import json
from colorama import Fore, Style
from module import modul, envfolder, envllmscoreeeee
from module.modul import log_function_status
from queue import Queue
import threading
import time
import random
import logging


@log_function_status
def convert(csvFile, jsonFile):
    # File path to your file directory
    csvFile = f'assets/csv/{csvFile}.csv'
    # jsonFile = f'assets/json/converted/{jsonFile}.json'
    result_path = envfolder.json_converted(jsonFile)
    
    title = f"Converting csv to json from {result_path}"
    modul.show_loading(title)
    try:
        csv_data = []
        with open(csvFile, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                lowercased_row = {key.lower(): value for key, value in row.items()}
                csv_data.append(lowercased_row)
        with open(result_path, 'w', encoding='utf-8') as file:
            json.dump(csv_data, file, indent=4)
            print("File CSV berhasil diubah menjadi JSON.........\n")
        return csv_data
    except FileNotFoundError as e:
        print(Fore.RED + "File CSV tidak ditemukan:", str(e) + Style.RESET_ALL)
        raise
    except Exception as e:
        print(Fore.RED + "Terjadi kesalahan saat mengonversi file CSV menjadi JSON:", str(e) + Style.RESET_ALL)
        raise

@log_function_status
def read_json(jsonFile):
    # File path to your file directory
    result_path = envfolder.read_json(jsonFile)

    title = f"Reading file json from {result_path}"
    modul.show_loading(title)
    try:
        with open(result_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            print("File JSON berhasil terbaca.........\n")
        return json_data
    except FileNotFoundError as e:
        print(Fore.RED + "File JSON tidak ditemukan:", str(e) + Style.RESET_ALL)
        raise
    except Exception as e:
        print(Fore.RED + "Terjadi kesalahan saat membaca file JSON:", str(e) + Style.RESET_ALL)
        raise


@log_function_status
def write_json_data_bot(data_bot, report_filename, id_test):
    # worker_thread = threading.Thread(target=scoring_worker, args=(report_filename, id_test))
    # worker_thread.start()
    report_filename = f"{report_filename}-{id_test}"
    # result = f'assets/json/result/{report_filename}.json'
    
    result_path = envfolder.write_json_data_bot(report_filename)

    try:
        with open(result_path) as file:
            data_json = json.load(file)
    except FileNotFoundError:
        data_json = {"summary": [], "chart": [], "data": []}

    # Append data_b terus menerus
    data_json["data"].append(data_bot)


    # Menyimpan data ke file JSON
    with open(result_path, 'w') as file:
        json.dump(data_json, file, indent=4)


def write_end_time_summary(time, end, report_filename, id_test):
    report_filename = f"{report_filename}-{id_test}"
    # result = f'assets/json/result/{report_filename}.json'
    
    result_path = envfolder.write_json_data_summary(report_filename)

    try:
        with open(result_path) as file:
            data_json = json.load(file)
    except FileNotFoundError:
        data_json = {"summary": [], "chart": [], "data": []}

    found = False
    if "summary" in data_json:
        for item in data_json["summary"]:
            if item.get("id_test") == id_test:
                item["duration"] = end
                item["end_time_test"] = time
                found = True
                break

    if found:
        with open(result_path, 'w') as file:
            json.dump(data_json, file, indent=4)
    else:
        print(f"id_test {id_test} tidak ditemukan dalam summary.")
    





@log_function_status
def write_json_data_summary(data_summary, report_filename, id_test):
    report_filename = f"{report_filename}-{id_test}"
    # result = f'assets/json/result/{report_filename}.json'
    
    result_path = envfolder.write_json_data_summary(report_filename)


    try:
        with open(result_path) as file:
            data_json = json.load(file)
    except FileNotFoundError:
        data_json = {"summary": [], "chart": [], "data": []}

    # Update summary jika belum ada atau append jika sudah ada (mengambil data terbaru)
    summary = any(obj.get("id_test") == data_summary["id_test"] for obj in data_json["summary"])
    if not summary:
        data_json["summary"].append(data_summary)
    else: 
        for obj in data_json["summary"]:
            if obj.get("id_test") == data_summary["id_test"]:
                obj.update(data_summary)
                break
    
    # Menyimpan data ke file JSON
    with open(result_path, 'w') as file:
        json.dump(data_json, file, indent=4)

@log_function_status  
def write_json_chart(chart, report_filename, id_test):
    report_filename = f"{report_filename}-{id_test}"
    # result = f'assets/json/result/{report_filename}.json'
    
    result_path = envfolder.write_json_data_bot(report_filename)

    try:
        with open(result_path) as file:
            data_json = json.load(file)
    except FileNotFoundError:
        data_json = {"summary": [], "chart": [], "data": []}

    # Append data_b terus menerus
    data_json["chart"].append(chart)

    # Menyimpan data ke file JSON
    with open(result_path, 'w') as file:
        json.dump(data_json, file, indent=4)
    

