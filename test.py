
from hashlib import sha1
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pythoncom

devices = AudioUtilities.GetAllDevices()
mic = "Microphone (GXT 258 Microphone)"
for device in devices:
    if device.FriendlyName == mic:
        print(device.EndpointVolume.SetMute(False, None))