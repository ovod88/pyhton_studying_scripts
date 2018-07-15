import time
from datetime import datetime as dt

hosts_temp=r"C:\Windows\System32\drivers\etc\hosts"
hosts_path="hosts"
redirect_to="127.0.0.1"
website_list=["www.facebook.com","facebook.com","vk.com", "youtube.com", "www.youtube.com"]


while True:
    start_time = dt(dt.now().year,dt.now().month,dt.now().day,8)
    end_time = dt(dt.now().year,dt.now().month,dt.now().day,18)
    now = dt.now()

    if start_time < now < end_time:
        print('Working hours')

        with open(hosts_temp, 'r+') as file:
            content = file.read()
            for website in website_list:
                if website not in content:
                    file.write(redirect_to + " " + website +"\n")
    else:
        print('Out of working hours')
        with open(hosts_temp, 'r+') as file:
            content=file.readlines()
            file.seek(0)

            for line in content:
                if not any(website in line for website in website_list):
                    file.write(line)
            file.truncate()

    time.sleep(30)
