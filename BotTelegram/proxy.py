import requests
import ast
#функция получения, проверки, сохранения прокси
def get_prox():
    filename = "proxy_list.txt"
    proxyApiAdress="https://api.getproxylist.com/proxy?lastTested=600&country=KZ&notcountry=RU&protocol[]=http&allowsHttps=1&anonymity[]=high%20anonymity"
    request = ast.literal_eval(str(requests.get(proxyApiAdress).json()))
    if 'error' in request:
        #запрос не удался - берем прокси из файла
        with open(filename,"r") as file:
            #перебор строк в файле
            for line in file:
                try:
                    proxy = line.split('\n', 1)[0]
                    http_proxy = 'http://'+proxy
                    https_proxy = 'https://'+proxy
                    print("Проверка "+str(line))
                    proxies = {
                        'http': http_proxy,
                        'https': https_proxy,
                    }
                    req = requests.get("https://api.telegram.org",proxies=proxies)#попытка подключения к серверам Телеграм, для проверки
                    if '<Response [200]>' in str(req):#http 200 - код успешности запроса
                        print(proxy+" работает")
                        return proxy
                    else:
                        print(proxy+" не работает")
                    continue
                except Exception as e:
                    print("exception "+str(e))
                    print(e)
                    continue
            else:
                print("ВСЕ прокси в файле нерабочие, добавьте рабочие прокси в файл")
                return False
    else:
        #получаем адрес из запроса, проверяем, сохраняем
        addr = str(request['ip']) + ":" + str(request['port'])
        print("Хороший прокси - сохраняю его, ip "+addr)
        with open(filename,"a") as file:
            addr = addr.split('\n', 1)[0]
            file.write(addr+"\n")
        file.close()
        return addr
