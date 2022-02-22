import requests


class Request:
    def __init__(self):
        self.url = None
        self.data = None

    def set_data(self, ifns, oktmmf):
        self.data = {
            "c": "next",
            "step": "1",
            "npKind": "fl",
            "objectAddr": "",
            "objectAddr_zip": "",
            "objectAddr_ifns": "",
            "objectAddr_okatom": "",
            "ifns": ifns,
            "oktmmf": oktmmf,
            "PreventChromeAutocomplete": ""
        }

    def set_url(self, url):
        self.url = url

    def send_request(self):
        return requests.post(self.url, data=self.data).json()


class InfoNalog:
    def __init__(self):
        self.oktmmf = None
        self.ifns = None
        self.info = dict()

    def set_oktmmf(self, oktmmf):
        self.oktmmf = str(oktmmf)

    def set_ifns(self, ifns):
        self.ifns = str(ifns)

    def get_pay_element(self, request: Request):
        request.set_data(self.ifns, self.oktmmf)
        self.info = request.send_request()["payeeDetails"]

    def get_info(self):
        return self.info

    def print_info(self):
        print(f"Получатель платежа: {self.info['payeeName']}\n"
              f"ИНН получателя {self.info['payeeInn']}\n"
              f"КПП получателя {self.info['payeeKpp']}\n"
              f"Банк получателя {self.info['bankName']}\n"
              f"БИК {self.info['bankBic']}\n"
              f"Корр. счет № {self.info['correspAcc']}\n"
              f"Счет № {self.info['payeeAcc']}\n")


if __name__ == "__main__":
    nalog = InfoNalog()
    request = Request()
    request.set_url("https://service.nalog.ru/addrno-proc.json")
    nalog.set_ifns(7840)
    nalog.set_oktmmf(40913000)
    nalog.get_pay_element(request)
    data = nalog.get_info()
    nalog.print_info()
