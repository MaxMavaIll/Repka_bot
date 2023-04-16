from ntpath import join
import requests

url = {
    "check_freeTime": "https://script.google.com/macros/s/AKfycbzvaiu7VJJBV2MTXYMPOJHoHeeuny__j11FCRkvQ0U79hHOP9aVp1MhoXFzF3rUlkj59Q/exec",
    "get_w": "https://script.google.com/macros/s/AKfycbxw1BpLEvLIgocQFnK1swhscLqq1pf92eov048gTrMLA2Ps_hN0Rc4bwNr-WcVrlSHjqw/exec",
    "write_group": "https://script.google.com/macros/s/AKfycbyPwn_uuRrbhf-LaVgQvTfawsj-7Jtfr2TMnpOm7UrEr14SPDpovSsCW6h0pcbTEzIR/exec",
    "delete_admin": "https://script.google.com/macros/s/AKfycbxv4UoTcfnsDGpWiMnlpeIMwvDu1Z40PX780V7XXGLrHbTOz3jfix9_PptV1LOxcD8F/exec",
    "delete_group": "https://script.google.com/macros/s/AKfycbyyWGDdKteHNE6Jg8Ka4CUSfc9Fxm8a3ZDjZJXeoHs-r_DKd3r6hf7zsfdv3lef1q4/exec",
}

def send_apps_script(data):
    print("send_apps_script")
    get_data_apps = requests.get(
        url["check_freeTime"], params=data)
    json = get_data_apps.json()
    return json["time"]

def write_apps_script(data):
    requests.get(
        url["get_w"], params=data)
    print("Запис успішний")

def write_group_apps_script(data):
    requests.get(
        url["write_group"], params=data)
    print("Запис успішний")

def delete_apps_script(data):
    requests.get(
        url["delete_admin"], params=data)
    print("Запис успішний")

def delete_group_apps_script(data):
    requests.get(
        url["delete_group"], params=data)
    print("Запис успішний")