#!/usr/local/bin/python3
# coding: utf-8


logo = (r"""
    _              _        ____                      
   / \   _ __   __| |_   _ / ___|___  _ __ ___  _ __  
  / _ \ | '_ \ / _` | | | | |   / _ \| '_ ` _ \| '_ \ 
 / ___ \| | | | (_| | |_| | |__| (_) | | | | | | |_) |
/_/   \_\_| |_|\__,_|\__, |\____\___/|_| |_| |_| .__/ 
                     |___/                     |_|    


* Search in Shodan       Created by Andranik Mastoyan
""")


try:
    import os
    import socket
    import time
    import shodan
    import datetime
except ImportError as error:
    module = str(error).split()[-1].replace('\'', '')
    print(
        '\nModule ' + module + ' is not installed!',
        '\npip3 install -r requirements.txt'
    )
    raise SystemExit

if not os.path.exists('result'):
    os.mkdir('result')


def main():
    print(logo)

    def scanner():
        api_key = input('[?] Enter Your shodan api key  : ')
        api = shodan.Shodan(api_key)
        date = datetime.datetime.today().strftime("%H.%M.%S-%d-%m")
        textdork = input('[?] Enter Your Shodan query  : ')
        pages_start = int(input('[?] Start scanning from page : '))
        pages_stop = int(input('[?] Stop  scanning on   page : '))
        results_file = r'result/ips-' + date + '.txt'
        print('[?] If you press Ctrl + C scanning will be stopped!')
        for page in range(pages_start, pages_stop, 1):
            try:
                print('[' + str(page) + '/' + str(pages_stop) + '] Loading page results... ')
                time.sleep(1)
                results = api.search(textdork, page=page)
            except KeyboardInterrupt:
                print('\n[!] (Ctrl + C) detected.. Stopping...')
                break
            except shodan.exception.APIError as error:
                print('[EXCEPTION] ' + str(error))
                time.sleep(3)
                continue
            else:
                for result in results['matches']:
                    with open(results_file, 'a') as file:
                        file.write(result['ip_str'] + '\n')
        # Display results after loading
        if os.path.exists(results_file):
            print('\n[+] Okay, all results from page ' + str(pages_start) + ' to page ' + str(
                pages_stop) + ', was saved to ' + results_file)
            if input('[?] Show downloaded results? (y/n) : ').lower() in ('y', 'yes', 'true', '1', '+'):
                with open(results_file, 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        print(line.replace('\n', ''))
                print('[+] Saved ' + str(len(lines)) + ' ips')

    scanner()


if __name__ == '__main__':
    main()
    print('[$] Created by Andranik Mastoyan.')
