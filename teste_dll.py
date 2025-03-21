import ctypes

try:
    dll = ctypes.CDLL(r"C:\Windows\System32\libzbar-64.dll")
    print("✅ DLL carregada com sucesso!")
except OSError as e:
    print(f"❌ Erro ao carregar a DLL: {e}")
