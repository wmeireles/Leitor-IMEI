import os
import ctypes

def carregar_libzbar():
    dll_custom_path = r"C:\Tempo\Leitor-bot\libzbar-64.dll"  # ou qualquer outro onde você tem certeza que está

    if os.path.exists(dll_custom_path):
        os.environ["PATH"] += os.pathsep + os.path.dirname(dll_custom_path)
        try:
            ctypes.cdll.LoadLibrary(dll_custom_path)
            print("✅ libzbar-64.dll carregada manualmente!")
        except OSError as e:
            print(f"❌ Erro ao carregar libzbar manualmente: {e}")
    else:
        print("❌ DLL não encontrada no caminho especificado.")

carregar_libzbar()
