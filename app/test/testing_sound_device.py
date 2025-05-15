import sounddevice as sd


# device = sd.query_devices()
# print(f"Microphone device detecded: {device}")


# devices = sd.query_devices(kind='input')
# for device in devices:
#     print(f"Microphone device detecded: {device}")


# print(sd.query_devices())  # Lihat daftar perangkat
# sd.default.device = (2, None)  # Ganti 2 dengan indeks perangkat input Anda



print(sd.query_devices())  # Lihat daftar perangkat
sd.default.device = (2, None)  # Ganti 2 dengan indeks perangkat input Anda



# device_info = sd.query_devices(kind='input')  # pilih default input device
# sd.default.device = device_info['name']       # set secara eksplisit

# print(f"Microphone device detecded: {sd.default.device}")