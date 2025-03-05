from dataclasses import dataclass, field

import httpx

@dataclass
class PushBulletProfile:
    active: bool
    iden: str
    created: float
    modified: float
    email: str
    email_normalized: str
    name: str
    image_url: str
    max_upload_size: int

@dataclass
class PushBulletDevice:
    active: bool
    iden: str
    created: float
    modified: float
    type: str
    kind: str
    nickname: str
    manufacturer: str
    model: str
    app_version: int
    pushable: bool
    icon: str
    __token: str = field(init=False, repr=False)

    @classmethod
    def from_data(cls, data: dict, token: str):
        device = cls(**data)
        object.__setattr__(device, "_PushBulletDevice__token", token)
        return device

    def send(self, title: str, body: str):
        try:
            response = httpx.post(
                url="https://api.pushbullet.com/v2/pushes",
                headers={"Access-Token": self.__token},
                data={
                    "type": "note",
                    "device_iden": self.iden,
                    "title": title,
                    "body": body
                }
            )
            if response.status_code != 200:
                print(f"Error! Code: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Exception occurred: {str(e)}")

    def send_link(self, title: str, body: str, link: str):
        try:
            response = httpx.post(
                url="https://api.pushbullet.com/v2/pushes",
                headers={"Access-Token": self.__token},
                data={
                    "type": "link",
                    "device_iden": self.iden,
                    "title": title,
                    "body": body,
                    "url": link
                }
            )
            if response.status_code != 200:
                print(f"Error! Code: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Exception occurred: {str(e)}")

class PushBullet:
    def __init__(self, token: str):
        self.__token = token

    def get_profile(self):
        req = httpx.get(
            url="https://api.pushbullet.com/v2/users/me",
            headers={"Access-Token": self.__token}
        )
        return PushBulletProfile(**req.json())

    def get_device(self, name: str = None, iden: str = None, index: int = None):
        criteria = [param is not None for param in (name, iden, index)]
        if sum(criteria) != 1:
            raise ValueError("Передайте ровно один параметр: name, iden или index")

        response = httpx.get(
            url="https://api.pushbullet.com/v2/devices",
            headers={"Access-Token": self.__token}
        ).json()
        devices = response.get("devices", [])

        if index is not None:
            try:
                device_data = devices[index]
            except IndexError:
                raise ValueError("Устройство с данным индексом не найдено")
            return PushBulletDevice.from_data(device_data, self.__token)

        if name is not None:
            for device in devices:
                if device.get("nickname") == name:
                    return PushBulletDevice.from_data(device, self.__token)
            raise ValueError("Устройство с данным именем не найдено")

        if iden is not None:
            for device in devices:
                if device.get("iden") == iden:
                    return PushBulletDevice.from_data(device, self.__token)
            raise ValueError("Устройство с данным iden не найдено")
