import httpx
import base64


class NtfyExceptions:
    class MailException(Exception):
        def __init__(self, text: str = None):
            self.text = text
            super().__init__(text)

    class AuthorizationException(Exception):
        def __init__(self, text: str = None):
            self.text = text
            super().__init__(text)


class Ntfy:
    """
    Ntfy push notificator class, more information and example can be found on the project's GitHub
    :param link: The link to send the notification...
    """
    link: str

    __headers: dict = {}

    def __init__(self, link: str = None, username: str = None, password: str = None, token: str = None):
        self.link = link
        if not (username and password):
            if token:
                try:
                    req = httpx.get(self.link, headers={"Authorization": f"Bearer {token}"})
                    if req.status_code == 401:
                        raise NtfyExceptions.AuthorizationException("Token is invalid")
                except Exception as e:
                    print(f"Exception!{e.__str__()}")

                self.__headers.update({"Authorization": f"Bearer {token}"})
        else:
            token = base64.b64encode(bytes(f"{username}:{password}", "utf-8"))

            try:
                req = httpx.get(self.link, headers={"Authorization": f"Basic {token}"})
                if req.status_code == 401:
                    raise NtfyExceptions.AuthorizationException("Invalid credentials")
            except Exception as e:
                print(f"Exception!{e.__str__()}")

            self.__headers.update({"Authorization": f"Basic {token}"})

    def send_template(self, text: str = "Some message...") -> None:
        """
        Send notification

        :param text: The main body of the message has markdown support
        """

        payload = message.encode('utf-8')  # encode required to support languages other than English

        try:
            # noinspection PyTypeChecker
            req = httpx.post(self.link, data=payload, headers=self.__headers)
            if req.status_code != 200:
                print(f"Error! Code: {req.status_code}")
        except Exception as e:
            print(f"Exception!{e.__str__()}")

    def send(self, text: str = "Some text...", title: str = None,
             priority: int = None, tags: list[str] = None,
             click_action: str = None, icon: str = None,
             attachment_from_link: str = None, headers: dict = None,
             markdown: bool = None, email: str = None):
        """
        Send unique notifications with their own unique headers

            You can read how to use headers in a project wiki.:



        :param text: (compulsory)
        :param title: (optional)
        :param priority: (optional)
        :param tags: (optional)
        :param click_action: (optional)
        :param icon: (optional)
        :param attachment_from_link: (optional)
        :param headers: (optional)
        :param markdown: (optional)
        :param email: (optional)
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

        if email is not None:
            if "@" in email:
                headers.update({'Email': email})
            else:
                raise NtfyExceptions.MailException("Email address is not valid!")

        payload = text.encode('utf-8')  # encode required to support languages other than English

        try:
            # noinspection PyTypeChecker
            req = httpx.post(self.link, data=payload, headers=headers)
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

    def set_email(self, email: str) -> None:
        """
        Set mail to which notifications will be duplicated

        :param email: target email
        """
        if email is not None:
            if "@" in email:
                self.__headers.update({'Email': email})
            else:
                raise NtfyExceptions.MailException("Email address is not valid!")

    def add_attachment_from_link(self, attachment: str) -> None:
        """
        Add attachment from link

        :param attachment: Link to the file to be sent as an attachment
        """

        self.__headers.update({'Attach': attachment})

    def set_headers(self, headers: dict) -> None:
        """
        Replaces already installed headers that have not been transmitted

        :param headers:
        """
        self.__headers.clear()
        self.__headers = headers

    def clear(self) -> None:
        """
        Clear all headers
        """
        if self.__headers["Authorization"]:
            auth = {"Authorization": self.__headers["Authorization"]}
            self.__headers.clear()
            self.__headers.update({"Markdown": "yes"})
            self.__headers.update(auth)
        else:
            self.__headers.clear()
            self.__headers.update({"Markdown": "yes"})
