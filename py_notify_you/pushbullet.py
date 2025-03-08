import mimetypes
from dataclasses import dataclass, field
import httpx
import pathlib

@dataclass
class PushBulletProfile:
    """
    Represents a Pushbullet user profile.

    Attributes:
        active (bool): Whether the profile is active.
        iden (str): Unique identifier for the profile.
        created (float): Timestamp when the profile was created.
        modified (float): Timestamp when the profile was last modified.
        email (str): User's email address.
        email_normalized (str): Normalized email address.
        name (str): User's name.
        image_url (str): URL for the profile image.
        max_upload_size (int): Maximum file upload size in bytes.
    """
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
    """
    Represents a Pushbullet device that can receive notifications and files.

    Attributes:
        active (bool): Whether the device is active.
        iden (str): Unique identifier for the device.
        created (float): Timestamp when the device was created.
        modified (float): Timestamp when the device was last modified.
        type (str): Device type.
        kind (str): Device category.
        nickname (str): Device name.
        manufacturer (str): Device manufacturer.
        model (str): Device model.
        app_version (int): Version of the Pushbullet app on the device.
        pushable (bool): Whether notifications can be sent to the device.
        icon (str): Device icon.
        __token (str): Private access token for the Pushbullet API.
    """
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
        """
        Creates a device instance from a dictionary of data.

        Args:
            data (dict): Dictionary containing device data.
            token (str): Access token for the Pushbullet API.

        Returns:
            PushBulletDevice: A new device instance.
        """
        device = cls(**data)
        object.__setattr__(device, "_PushBulletDevice__token", token)
        return device

    def send(self, title: str, body: str, link: str = None):
        """
        Sends a text notification to the device.

        Args:
            title (str): Notification title.
            body (str): Notification text.
            link (str, optional): URL link to add to the notification.

        Raises:
            Exception: If there's an error sending the notification.
        """
        try:
            payload = {
                "type": "note",
                "device_iden": self.iden,
                "title": title,
                "body": body,
            }

            if link:
                payload["url"] = link

            response = httpx.post(
                url="https://api.pushbullet.com/v2/pushes",
                headers={"Access-Token": self.__token},
                data=payload
            )
            if response.status_code != 200:
                print(f"Error! Code: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Exception occurred: {str(e)}")

    def send_file(self, title: str, body: str, file_path: str, link: str = None):
        """
        Sends a file to the device.

        Args:
            title (str): Notification title.
            body (str): Notification text.
            file_path (str): Path to the file being sent.
            link (str, optional): URL link to add to the notification.

        Raises:
            Exception: If there's an error at any stage of sending the file.
        """
        path = pathlib.Path(file_path)
        file_name = path.name
        mime_type = mimetypes.guess_type(file_name)[0] or 'application/octet-stream'

        try:
            upload_request = httpx.post(
                url="https://api.pushbullet.com/v2/upload-request",
                headers={"Access-Token": self.__token, "Content-Type": "application/json"},
                json={
                    "file_name": file_name,
                    "file_type": mime_type
                }
            ).json()

            if "error" in upload_request:
                raise Exception(f"Looping request error: {upload_request ['error']}")

            # Step 2: Upload the file using the provided link
            with open(file_path, "rb") as file:
                upload_response = httpx.post(
                    url=upload_request["upload_url"],
                    data=upload_request["data"],
                    files={"file": file}
                )

            if upload_response.status_code != 204:  # Successful upload returns 204 No Content
                raise Exception(f"File upload error: {upload_response.status_code} - {upload_response.text}")

            # Step 3: Create a push with the file
            payload = {
                "type": "file",
                "device_iden": self.iden,
                "title": title,
                "body": body,
                "file_name": file_name,
                "file_type": mime_type,
                "file_url": upload_request["file_url"]
            }

            if link:
                payload["url"] = link

            push_response = httpx.post(
                url="https://api.pushbullet.com/v2/pushes",
                headers={"Access-Token": self.__token, "Content-Type": "application/json"},
                json=payload
            )

            if push_response.status_code != 200:
                raise Exception(f"Push sending error: {push_response.status_code} - {push_response.text}")

        except Exception as e:
            raise e


class PushBullet:
    """
    Main class for working with the Pushbullet API.

    Attributes:
        __token (str): Private access token for the Pushbullet API.
    """
    def __init__(self, token: str):
        """
        Initializes a Pushbullet client instance.

        Args:
            token (str): Access token for the Pushbullet API.
        """
        self.__token = token

    def get_profile(self):
        """
        Gets information about the user profile.

        Returns:
            PushBulletProfile: Current user's profile.

        Raises:
            Exception: If there's an error in the API request.
        """
        req = httpx.get(
            url="https://api.pushbullet.com/v2/users/me",
            headers={"Access-Token": self.__token}
        )
        return PushBulletProfile(**req.json())

    def get_device(self, name: str = None, iden: str = None, index: int = None):
        """
        Gets a device by name, identifier, or index.

        Args:
            name (str, optional): Device name (nickname).
            iden (str, optional): Unique device identifier.
            index (int, optional): Device index in the list of all devices.

        Returns:
            PushBulletDevice: Device matching the search criteria.

        Raises:
            ValueError: If more than one parameter is provided or the device is not found.
            Exception: If there's an error in the API request.
        """
        criteria = [param is not None for param in (name, iden, index)]
        if sum(criteria) != 1:
            raise ValueError("Provide exactly one parameter: name, iden, or index")

        response = httpx.get(
            url="https://api.pushbullet.com/v2/devices",
            headers={"Access-Token": self.__token}
        ).json()
        devices = response.get("devices", [])

        if index is not None:
            try:
                device_data = devices[index]
            except IndexError:
                raise ValueError("Device with the specified index not found")
            return PushBulletDevice.from_data(device_data, self.__token)

        if name is not None:
            for device in devices:
                if device.get("nickname") == name:
                    return PushBulletDevice.from_data(device, self.__token)
            raise ValueError("Device with the specified name not found")

        if iden is not None:
            for device in devices:
                if device.get("iden") == iden:
                    return PushBulletDevice.from_data(device, self.__token)
            raise ValueError("Device with the specified iden not found")

