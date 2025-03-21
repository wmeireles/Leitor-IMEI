import cv2
import openpyxl
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import numpy as np
import pytesseract
import re

# Configuração do Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Lista para armazenar os dados antes de salvar no Excel
dados_lidos = []

def preprocessar_imagem(frame):
    """ Melhora a imagem para leitura de código de barras e texto """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    _, binary = cv2.threshold(blurred, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Melhorando o contraste
    kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
    sharpened = cv2.filter2D(binary, -1, kernel)
    
    return sharpened

def validar_imei(codigo):
    """ Verifica se um código é um IMEI válido (14 a 16 dígitos numéricos) """
    codigo = codigo.lstrip("1")  # Remove qualquer "1" no início do IMEI
    return bool(re.fullmatch(r"\d{14,16}", codigo))

def validar_sn(codigo):
    """ Verifica se um código é um Número de Série válido (alfanumérico com 6 a 20 caracteres) """
    return bool(re.fullmatch(r"[A-Z0-9]{6,20}", codigo, re.IGNORECASE))

def extrair_info_ocr(texto):
    """ Extrai IMEI e SN do texto lido pelo OCR """
    imei, sn = None, None

    # Limpa o texto e mantém apenas letras e números
    texto = re.sub(r"[^a-zA-Z0-9:\n\s]", "", texto).strip()
    linhas = texto.split("\n")

    for linha in linhas:
        if "IMEI" in linha.upper():
            possivel_imei = "".join(filter(str.isdigit, linha))
            if validar_imei(possivel_imei):
                imei = possivel_imei.lstrip("1")  # Remove o "1" extra do começo
        elif "SN:" in linha.upper() or "SERIAL:" in linha.upper():
            match_sn = re.search(r"SN[:\s]*(\S+)|SERIAL[:\s]*(\S+)", linha, re.IGNORECASE)
            if match_sn:
                sn = match_sn.group(1) or match_sn.group(2)

    return imei, sn

def ler_codigo_opencv(frame):
    """ Tenta detectar código de barras com OpenCV BarcodeDetector """
    detector = cv2.barcode_BarcodeDetector()
    decoded_info, _, _ = detector.detectAndDecode(frame)

    if decoded_info and decoded_info[0]:
        codigo = decoded_info[0].strip()
        if validar_imei(codigo) or validar_sn(codigo):  
            return codigo.lstrip("1")  # Remove o "1" extra no início do IMEI
    return None  

def ler_codigo_ocr(frame):
    """ Usa OCR como último recurso para tentar ler números do código de barras """
    texto = pytesseract.image_to_string(frame, config="--psm 6")
    return extrair_info_ocr(texto)

def ler_camera():
    """ Captura a imagem da câmera e processa os códigos """
    cap = cv2.VideoCapture(0)
    sucesso = False

    while not sucesso:
        ret, frame = cap.read()
        if not ret:
            break

        frame_proc = preprocessar_imagem(frame)
        imei = ler_codigo_opencv(frame_proc)

        if not imei:  
            imei, sn = ler_codigo_ocr(frame_proc)
        else:
            sn = "SN não detectado"

        if imei and not verificar_existencia(imei):
            adicionar_dado(imei, sn)
            sucesso = True
            cv2.putText(frame, "Código detectado!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Escaneie o código do tablet", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC para sair
            break
        elif key == 32 and not sucesso:  # Espaço para tentar leitura manual
            imei, sn = ler_codigo_ocr(frame_proc)
            if imei:
                adicionar_dado(imei, sn)
                sucesso = True
                break

    cap.release()
    cv2.destroyAllWindows()

def verificar_existencia(imei):
    """ Verifica se o IMEI já foi registrado na lista """
    return any(dado[1] == imei for dado in dados_lidos)

def adicionar_dado(imei, sn):
    """ Adiciona os dados na tabela da interface """
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sn = sn if sn else "SN não detectado"
    dados_lidos.append([data, imei, sn])
    tree.insert("", "end", values=(data, imei, sn))

def salvar_em_excel():
    """ Salva os dados em um arquivo Excel """
    if not dados_lidos:
        messagebox.showwarning("Aviso", "Nenhum dado para salvar!")
        return

    nome_arquivo = "dados_tablets.xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Tablets"
    ws.append(["Data", "IMEI 1", "Número de Série"])

    for linha in dados_lidos:
        ws.append(linha)

    wb.save(nome_arquivo)
    messagebox.showinfo("Sucesso", f"Arquivo salvo como {nome_arquivo}!")

def iniciar_interface():
    global tree, root
    root = tk.Tk()
    root.title("Leitor de Tablets - IMEI/NS")
    root.geometry("500x400")

    label = tk.Label(root, text="Clique no botão abaixo para iniciar a leitura do código", font=("Arial", 12))
    label.pack(pady=10)

    btn_ler = tk.Button(root, text="📷 Ler com a câmera", font=("Arial", 12), command=ler_camera)
    btn_ler.pack(pady=5)

    # Criando a Tabela (Treeview)
    frame = tk.Frame(root)
    frame.pack(pady=10)

    colunas = ("Data", "IMEI 1", "Número de Série")
    tree = ttk.Treeview(frame, columns=colunas, show="headings")

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    tree.pack()

    # Botão para salvar em Excel
    btn_salvar = tk.Button(root, text="💾 Salvar em Excel", font=("Arial", 12), command=salvar_em_excel)
    btn_salvar.pack(pady=5)

    # Botão para sair
    btn_sair = tk.Button(root, text="Sair", font=("Arial", 10), command=root.destroy)
    btn_sair.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    iniciar_interface()
