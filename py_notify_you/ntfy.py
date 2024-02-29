import requests


class Ntfy:
    """
    Ntfy push notificator class, more information and example can be found on the project's GitHub
    :param link: The link to send the notification...
    """
    link: str

    __headers: dict = {}

    def __init__(self, link: str = None):
        self.link = link

    def send(self, message: str = "Some message...") -> None:
        """
        Send notification

        :param message: The main body of the message has markdown support
        """

        payload = message.encode('utf-8')  # encode required to support languages other than English

        try:
            req = requests.post(self.link, data=payload, headers=self.__headers)
            if req.status_code != 200:
                print(f"Error! Code: {req.status_code}")
        except Exception as e:
            print(f"Exception!{e.__str__()}")

    def send_unique(self, message: str = "Some text...", title: str = None,
                    priority: int = None, tags: list[str] = None,
                    click_action: str = None, icon: str = None,
                    attachment_from_link: str = None, headers: dict = None, markdown: bool = None):
        """
        Send unique notifications with their own unique headers

            You can read how to use headers in a project wiki.:



        :param message: (compulsory)
        :param title: (optional)
        :param priority: (optional)
        :param tags: (optional)
        :param click_action: (optional)
        :param icon: (optional)
        :param attachment_from_link: (optional)
        :param headers: (optional)
        :param markdown: (optional)
        """

        if headers is None:
            headers = {"Markdown": "yes"}

        if title is not None:
            headers.update({'Title': title.encode('utf-8')})

        if priority is not None:
            if priority < 1 or priority > 5:
                self.__headers.update({'Priority': priority})
            else:
                self.__headers.update({'Priority': 3})

        if tags is not None:
            headers.update({'Tags': ', '.join(map(str, tags))})

        if click_action is not None:
            headers.update({'Click': click_action})

        if icon is not None:
            headers.update({'Icon': icon})

        if attachment_from_link is not None:
            headers.update({'Attach': attachment_from_link})

        if markdown is not None:
            headers.update({'Markdown': str(markdown)})

        payload = message.encode('utf-8')  # encode required to support languages other than English

        try:
            req = requests.post(self.link, data=payload, headers=headers)
            if req.status_code != 200:
                print(f"Error! Code: {req.status_code}")
        except Exception as e:
            print(f"Exception!{e.__str__()}")

    def set_title(self, title: str) -> None:
        """
        Set notification title

        :param title: The headline of the message. Located above the main text and always in bold
        """

        self.__headers.update(
            {'Title': title.encode('utf-8')})  # encode required to support languages other than English

    def set_priority(self, priority: int) -> None:
        """
        Set notification priority

        :param priority: The priority of the notification, 1-5 (one is minimum priority)
        """

        if priority < 1 or priority > 5:
            self.__headers.update({'Priority': priority})
        else:
            self.__headers.update({'Priority': 3})

    def set_tags(self, tags: list[str]) -> None:
        """
        Set notification tags

            See https://docs.ntfy.sh/emojis/ from get tags
        :param tags: List of tags to be added to the notification
        """
        self.__headers.update({'Tags': ', '.join(map(str, tags))})

    def set_click_action(self, action: str) -> None:
        """
        Set notification click action

            See https://docs.ntfy.sh/publish/#click-action from get more information
        :param action: The link to be taken when the notification is clicked ( working with apps )
        """

        self.__headers.update({'Click': action})

    def set_icon(self, icon: str) -> None:
        """
        Set notification icon

        :param icon: Link to the image that will be used as the icon
        """

        self.__headers.update({'Icon': icon})

    def add_attachment_from_link(self, attachment: str) -> None:
        """
        Add attachment from link

        :param attachment: Link to the file to be sent as an attachment
        """

        self.__headers.update({'Attach': attachment})

    def set_headers(self, headers: dict) -> None:
        """

        :param headers:
        :return:
        """
        self.__headers.clear()
        self.__headers = headers

    def clear(self) -> None:
        """
        Clear all headers
        """

        self.__headers.clear()
        self.__headers.update({"Markdown": "yes"})
