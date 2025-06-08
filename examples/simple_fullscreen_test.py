"""
Test simple para verificar la funcionalidad de fullscreen
sin depender de BaseCase
"""
import sys
import os

# Añadir el directorio raíz al path para importar seleniumbase
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seleniumbase.core import browser_launcher

def test_fullscreen_basic():
    """Test básico para verificar que --start-fullscreen funciona"""
    print("🚀 Iniciando test de fullscreen...")
    
    # Configurar opciones para fullscreen
    driver = browser_launcher.get_driver(
        browser_name="chrome",
        headless=False,
        start_fullscreen=True,  # Esta es la nueva opción
    )
    
    try:
        # Navegar a una página de prueba
        driver.get("https://seleniumbase.io/demo_page")
        
        # Verificar el tamaño de la ventana
        window_size = driver.get_window_size()
        print(f"📐 Tamaño de ventana: {window_size['width']} x {window_size['height']}")
        
        # Verificar que estamos en fullscreen
        assert window_size['width'] >= 1024, f"Ancho muy pequeño: {window_size['width']}"
        assert window_size['height'] >= 768, f"Alto muy pequeño: {window_size['height']}"
        
        print("✅ Test de fullscreen exitoso!")
        print("🎯 El navegador se abrió correctamente en modo fullscreen")
        
        # Esperar un poco para ver el resultado
        import time
        time.sleep(3)
        
    finally:
        # Cerrar el navegador
        driver.quit()
        print("🔚 Navegador cerrado")

if __name__ == "__main__":
    test_fullscreen_basic() 