# 📷 Leitor de IMEI e Número de Série

Este projeto é um **Leitor de Códigos de Barras** que utiliza a câmera do PC para capturar **IMEI e Número de Série** de tablets/notebooks e os armazena em um arquivo Excel (`.xlsx`).

## 🚀 Funcionalidades
✔ **Captura IMEI e SN** de etiquetas via câmera
✔ **Evita duplicação** de registros
✔ **Exibe os dados na interface** antes de salvar
✔ **Exportação para Excel** (`dados_tablets.xlsx`)
✔ **Atalhos para facilitar o uso**

## 🎥 Como Funciona?
1️⃣ O usuário **clica no botão** para iniciar a leitura
2️⃣ O sistema usa **OCR e OpenCV** para identificar o código
3️⃣ Os dados são **exibidos na interface** e podem ser removidos antes de salvar
4️⃣ O usuário pode **salvar os dados em Excel** clicando em "💾 Salvar em Excel"

---

## 📦 Instalação
### **1️⃣ Clone o repositório**
```sh
git clone https://github.com/seuusuario/leitor-imei.git
cd leitor-imei
```

### **2️⃣ Instale as dependências**
Antes de rodar, instale os pacotes necessários:
```sh
pip install -r requirements.txt
```
Caso não tenha o **Tesseract OCR**, instale:
- **Baixe** o Tesseract OCR: [Clique aqui](https://github.com/UB-Mannheim/tesseract/wiki)
- **Após instalar, configure no código**:
```python
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
```

---

## ▶️ Como Executar
```sh
python Leitor.py
```

Se quiser criar um **arquivo .exe**, execute:
```sh
pyinstaller --onefile --noconsole --icon=icone.ico Leitor.py
```

O `.exe` será gerado na pasta `dist/Leitor.exe` 🎉

---

## ⌨️ Atalhos do Teclado
| Tecla | Ação |
|--------|--------------------------------|
| `L` | Iniciar leitura da câmera |
| `S` | Salvar em Excel |
| `D` | Remover item selecionado |
| `Q` | Fechar o programa |

---

## 📜 Licença
Este projeto está sob a licença MIT. Sinta-se livre para contribuir!

---

## 💡 Contribuições
Sinta-se à vontade para abrir **issues** e enviar **pull requests**. Qualquer melhoria será bem-vinda! 🚀

