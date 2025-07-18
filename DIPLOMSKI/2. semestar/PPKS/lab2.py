import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d, correlate2d
from PIL import Image

# Funkcija za kreiranje Gaussovog kernela
def gaussian_kernel(size, sigma=1):
    x, y = np.meshgrid(np.linspace(-size//2, size//2, size), np.linspace(-size//2, size//2, size))
    d = np.sqrt(x*x + y*y)
    kernel = np.exp(-(d**2 / (2.0 * sigma**2)))
    return kernel / np.sum(kernel)  # Normalizacija

# Funkcija za primjenu Gaussovog zamućenja
def apply_gaussian_blur(image, kernel):
    return convolve2d(image, kernel, mode='same', boundary='fill', fillvalue=0)

# Sobel detekcija rubova
def detect_edges(image):
    sobel_h = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
    sobel_v = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
    edges_h = convolve2d(image, sobel_h, mode='same', boundary='symm')
    edges_v = convolve2d(image, sobel_v, mode='same', boundary='symm')
    return np.hypot(edges_h, edges_v)

# Učitavanje slike
def load_image(image_path):
    image = Image.open(image_path).convert('L')
    return np.array(image)

# Detekcija kvadrata
def detect_square(image, square_size):
    kernel = np.ones((square_size, square_size), dtype=np.uint8) * 255
    return correlate2d(image, kernel, mode='same', boundary='symm')

if __name__ == "__main__":
    image_path = "mickey.jpg"
    image = load_image(image_path)
    
    # Generiranje Gaussovog kernela
    kernel_size = 15
    sigma = 5
    gaussian_kernel_ = gaussian_kernel(kernel_size, sigma)
    blurred_image = apply_gaussian_blur(image, gaussian_kernel_)
    
    # Detekcija rubova
    edges = detect_edges(image)
    
    # Kreiramo uzorak koji trazimo na slici - bijeli kvadrat
    correlation_1 = detect_square(image, 1)
    correlation_2 = detect_square(image, 2)
    
    # Prikaz slika
    fig, axes = plt.subplots(1, 5, figsize=(10, 5))
    
    titles = ["Original", "Gauss Blurred", "Sobel Edge Detection", "Detected Pattern (1)", "Detected Pattern (2)"]
    images = [image, blurred_image, edges, correlation_1, correlation_2]
    
    for ax, img, title in zip(axes, images, titles):
        ax.imshow(img, cmap='gray')
        ax.set_title(title)
        ax.axis('off')
    
    plt.tight_layout()
    plt.show()
