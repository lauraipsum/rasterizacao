import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QFileDialog, QWidget
from PyQt5.QtGui import QPixmap, QImage
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

def ler_arquivo_ppm(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()

        # verifica se é P2
        if linhas[0].strip() != 'P2':
            print("Formato de arquivo inválido. Deve ser do tipo P2.")
            return None

        # Obtém largura, altura e valor máximo do pixel
        largura, altura = map(int, linhas[1].split())
        valor_maximo = int(linhas[2])

        # le o valor de cada pixel da img
        matriz = []
        for linha in linhas[3:]:
            valores = linha.split()
            matriz.append([int(valor) for valor in valores])
            
        #print(matriz)
        return largura, altura, valor_maximo, matriz

def salvar_arquivo_ppm(nome_arquivo, largura, altura, valor_maximo, matriz):
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write("P2\n")
        arquivo.write(f"{largura} {altura}\n")
        arquivo.write(f"{valor_maximo}\n")

        for linha in matriz:
            linha_str = ' '.join(str(valor) for valor in linha)
            arquivo.write(f"{linha_str}\n")

def negativo(nome_arquivo):
    largura, altura, valor_maximo, matriz = ler_arquivo_ppm('exemplo.ppm') 
    matriz_negativo = [ 
                       [valor_maximo - pixel # s = (L-1) - r , transformacao negativa
                        for pixel in linha] 
                       for linha in matriz  
                       ]       
    
    novo_nome_arquivo = nome_arquivo.replace('.ppm', '_negativo.ppm')
    salvar_arquivo_ppm(novo_nome_arquivo, largura, altura, valor_maximo, matriz_negativo)
    
def threshold(nome_arquivo, limite):
    largura, altura, valor_maximo, matriz = ler_arquivo_ppm('exemplo.ppm') 
    
    matriz_threshold = [
                        [0 if pixel <= limite else valor_maximo 
                         for pixel in linha] 
                        for linha in matriz
                        ]

    novo_nome_arquivo = nome_arquivo.replace('.ppm', f'_threshold_{limite}.ppm')
    salvar_arquivo_ppm(novo_nome_arquivo, largura, altura, valor_maximo, matriz_threshold)

def imprimir_histograma(matriz):
    # Flatten da matriz para uma lista de pixels
    pixels = [pixel for linha in matriz for pixel in linha]

    # Criar histograma
    histograma, bins = np.histogram(pixels, bins=range(257))

    # Plotar histograma
    plt.bar(range(256), histograma, width=1, align='edge')
    plt.title('Histograma da Imagem')
    plt.xlabel('Valor do Pixel')
    plt.ylabel('Frequência')
    plt.show()
    
def equalizar_histograma(nome_arquivo):
    largura, altura, valor_maximo, matriz = ler_arquivo_ppm(nome_arquivo)

    # Flatten da matriz para uma lista de pixels
    pixels = [pixel for linha in matriz for pixel in linha]

    # Calcular a função de distribuição acumulativa (CDF)
    cdf = np.cumsum(np.histogram(pixels, bins=range(257))[0])

    # Normalizar a CDF para o intervalo [0, valor_maximo]
    cdf_normalized = (cdf - min(cdf)) * (valor_maximo - 1) / (max(cdf) - min(cdf))

    # Aplicar equalização do histograma à matriz
    matriz_equalizada = [
        [int(cdf_normalized[pixel]) for pixel in linha]
        for linha in matriz
    ]

    # Imprimir o histograma equalizado
    imprimir_histograma(matriz_equalizada)

    # Salvar a imagem equalizada
    novo_nome_arquivo = nome_arquivo.replace('.ppm', '_equalizado.ppm')
    salvar_arquivo_ppm(novo_nome_arquivo, largura, altura, valor_maximo, matriz_equalizada)

class ImageProcessorGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Widgets
        self.image_label = QLabel(self)
        self.histogram_canvas = FigureCanvas(Figure())
        self.histogram_axes = self.histogram_canvas.figure.add_subplot(111)

        # Buttons
        self.load_button = QPushButton('Load Image', self)
        self.load_button.clicked.connect(self.load_image)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.load_button)
        layout.addWidget(self.image_label)
        layout.addWidget(self.histogram_canvas)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Initialize variables
        self.image_path = None

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Image Processor GUI')
        self.show()

    def load_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "PPM Files (*.ppm);;All Files (*)", options=options)

        if file_name:
            self.image_path = file_name
            self.show_image()

    def show_image(self):
        # Original Image
        self.show_ppm_image('Original Image', self.image_path, subplot_index=121)

        # Negative Image
        neg_path = self.process_image('negativo')
        self.show_ppm_image('Negative Image', neg_path, subplot_index=122)

        # Histograms
        self.show_histogram(self.image_path, 'Original Image Histogram', subplot_index=121)
        self.show_histogram(neg_path, 'Negative Image Histogram', subplot_index=122)

    def process_image(self, transformation):
        if not self.image_path:
            return

        if transformation == 'negativo':
            neg_path = self.image_path.replace('.ppm', '_negativo.ppm')
            negativo(self.image_path)
            return neg_path

    def show_ppm_image(self, title, path, subplot_index):
        if not path:
            return

        largura, altura, valor_maximo, matriz = ler_arquivo_ppm(path)
        image_array = np.array(matriz)

        pixmap = self.array_to_pixmap(image_array)
        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setScaledContents(True)

        layout = self.centralWidget().layout()
        layout.addWidget(label)

    def array_to_pixmap(self, array):
        height, width = array.shape
        q_img = QPixmap.fromImage(QImage(array.flatten(), width, height, QImage.Format_Indexed8))
        return q_img

    def show_histogram(self, path, title, subplot_index):
        if not path:
            return

        largura, altura, valor_maximo, matriz = ler_arquivo_ppm(path)
        pixels = [pixel for linha in matriz for pixel in linha]

        histogram, bins = np.histogram(pixels, bins=range(257))

        self.histogram_axes.clear()
        self.histogram_axes.bar(range(256), histogram, width=1, align='edge')
        self.histogram_axes.set_title(title)
        self.histogram_axes.set_xlabel('Pixel Value')
        self.histogram_axes.set_ylabel('Frequency')
        self.histogram_canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageProcessorGUI()
    sys.exit(app.exec_())
negativo('exemplo.ppm')
threshold('exemplo.ppm', limite=125)

largura, altura, valor_maximo, matriz = ler_arquivo_ppm('exemplo_threshold_125.ppm')
imprimir_histograma(matriz)

equalizar_histograma('exemplo_threshold_125.ppm')