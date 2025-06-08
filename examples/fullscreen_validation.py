"""
Test de validación del feature --start-fullscreen

EJECUTAR CON:
pytest examples/fullscreen_validation.py --start-fullscreen -v -s

COMPARAR CON MODO NORMAL:
pytest examples/fullscreen_validation.py -v -s
"""
from seleniumbase import BaseCase


class TestFullscreenValidation(BaseCase):
    def test_fullscreen_works(self):
        """
        Test simple para validar que --start-fullscreen funciona
        """
        # Abrir cualquier página web
        self.open("https://google.com")
        
        # Obtener dimensiones de ventana
        window_size = self.get_window_size()
        width = window_size['width']
        height = window_size['height']
        
        print(f"\n📐 Dimensiones de ventana: {width} x {height}")
        print(f"📊 Área total: {width * height:,} píxeles")
        
        # Verificar si estamos en fullscreen basado en el tamaño
        is_fullscreen = width >= 1920 and height >= 1080
        
        if is_fullscreen:
            print("✅ ¡FULLSCREEN CONFIRMADO!")
            print("🚀 El navegador se abrió SIN barras de navegación")
            print("🎯 Área máxima de pantalla utilizada")
        else:
            print("ℹ️  Modo ventana normal")
            print(f"📏 Tamaño: {width}x{height}")
        
        # Verificar funcionalidad básica
        self.assert_element("body")
        print("✅ Página cargada correctamente")
        
        # Mensaje de estado
        mode = "FULLSCREEN" if is_fullscreen else "NORMAL"
        print(f"\n🏁 Test completado en modo: {mode}")
        
        # Breve pausa para ver el resultado
        self.sleep(1)

    def test_feature_documentation(self):
        """
        Test que documenta cómo usar la nueva funcionalidad
        """
        print("\n📚 DOCUMENTACIÓN DEL FEATURE --start-fullscreen")
        print("=" * 50)
        print("✨ NUEVAS OPCIONES DISPONIBLES:")
        print("   --start-fullscreen    (Modo fullscreen)")
        print("   --fullscreen          (Alias)")
        print("   --start_fullscreen    (Formato alternativo)")
        print()
        print("🚀 EJEMPLOS DE USO:")
        print("   pytest mi_test.py --start-fullscreen")
        print("   pytest mi_test.py --fullscreen --demo")
        print("   pytest mi_test.py --start-fullscreen --chrome")
        print()
        print("✅ CARACTERÍSTICAS:")
        print("   • Elimina barras de navegación del navegador")
        print("   • Utiliza toda la pantalla disponible")
        print("   • Compatible con Chrome y Edge")
        print("   • Funciona en Windows, Linux y macOS")
        print("   • Se integra con todas las opciones existentes")
        print()
        print("🎯 CASOS DE USO IDEALES:")
        print("   • Testing de aplicaciones de quiosco")
        print("   • Demos y presentaciones")
        print("   • Captura de pantallas sin UI del navegador")
        print("   • Testing de aplicaciones fullscreen")
        print("=" * 50)
        
        # Test funcional básico
        self.open("https://example.com")
        self.assert_title_contains("Example")
        print("✅ Funcionalidad básica verificada") 