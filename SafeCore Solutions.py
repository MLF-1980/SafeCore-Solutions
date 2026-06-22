import sys

class SafeCoreApp:
    def __init__(self):
        self.empresa_actual = None
        self.rubro_actual = None
        self.personal = []

    def mostrar_menu(self):
        while True:
            print("\n" + "="*40)
            print("       🛡️ SYSTEM SAFE-CORE v1.0 🛡️")
            print("="*40)
            if self.empresa_actual:
                print(f"🏢 Empresa activa: {self.empresa_actual} ({self.rubro_actual})")
            else:
                print("⚠️ Ninguna empresa configurada todavía.")
            print("-" * 40)
            print("1. Configurar Nueva Empresa / Cliente")
            print("2. Registrar Trabajador y Puesto")
            print("3. Correr Auditoría HSE de Control")
            print("4. Salir del Sistema")
            print("="*40)
            
            opcion = input("Seleccione una opción (1-4): ")
            
            if opcion == "1":
                self.configurar_empresa()
            elif opcion == "2":
                self.registrar_operario()
            elif opcion == "3":
                self.ejecutar_control()
            elif opcion == "4":
                print("\nCerrando SafeCore. ¡Gestión segura garantizada!")
                sys.exit()
            else:
                print("❌ Opción inválida. Intente de nuevo.")

    def configurar_empresa(self):
        print("\n--- CONFIGURACIÓN DE CLIENTE ---")
        self.empresa_actual = input("Nombre de la empresa: ")
        print("Seleccione el Rubro:")
        print("A - Construcción / Obra")
        print("B - Laboratorio / Planta Química")
        print("C - Logística / Industria General")
        letra = input("Opción (A/B/C): ").upper()
        
        if letra == "A": self.rubro_actual = "Construcción"
        elif letra == "B": self.rubro_actual = "Laboratorio"
        else: self.rubro_actual = "Logística"
        
        print(f"✅ Empresa {self.empresa_actual} guardada como rubro {self.rubro_actual}.")

    def registrar_operario(self):
        if not self.empresa_actual:
            print("❌ Primero debe configurar una empresa en la Opción 1.")
            return
        print("\n--- REGISTRO DE PERSONAL ---")
        nombre = input("Nombre del trabajador: ")
        puesto = input("Puesto de trabajo: ")
        meses_epp = int(input("Meses de uso del EPP actual: "))
        
        empleado = {"nombre": nombre, "puesto": puesto, "meses_epp": meses_epp}
        self.personal.append(empleado)
        print(f"✅ {nombre} registrado correctamente.")

    def ejecutar_control(self):
        if not self.empresa_actual or not self.personal:
            print("❌ Falta configurar la empresa o registrar personal para auditar.")
            return
        
        print(f"\n=== REPORTE DE AUDITORÍA AUTOMÁTICO: {self.empresa_actual} ===")
        # Definimos el límite según el rubro dinámicamente
        limite = 3 if self.rubro_actual == "Construcción" else 6
        
        for p in self.personal:
            print(f"👤 {p['nombre']} | Puesto: {p['puesto']}")
            if p['meses_epp'] > limite:
                print(f"   ⚠️ ALERTA: EPP excedido ({p['meses_epp']} meses). Solicitar recambio para {self.rubro_actual}.")
            else:
                print(f"   ✅ EPP en regla ({p['meses_epp']} meses de uso).")
        print("==================================================")

# Ejecución del programa
if __name__ == "__main__":
    sistema = SafeCoreApp()
    sistema.mostrar_menu()