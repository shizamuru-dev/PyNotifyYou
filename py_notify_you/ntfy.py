import requests


class Ntfy:
    """
    Ntfy push notificator class, more information and exampe can be found on the project's GitHub
    :param link: The link to send the notification...
    """
    message: str
    link: str

    __headers: dict = {}

    def __init__(self, link: str = None):
        self.link = link

    def send(self, message: str = "Some message...") -> None:
        """
        Send notification

        :param message: The main body of the message has markdown support
        """

        payload = message.encode("utf-8")  # encode required to support languages other than English

        try:
            req = requests.post(self.link, data=payload, headers=self.__headers)
            if req.status_code != 200:
                print(f"Error! Code: {req.status_code}")
        except Exception as e:
            print(f"Exception!{e.__str__()}")

    def set_title(self, title: str) -> None:
        """
        Set notification title

        :param title: The headline of the message. Located above the main text and always in bold
        """

        self.__headers.update({'Title': title})
