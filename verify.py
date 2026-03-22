#!/usr/bin/env python3
"""
✅ Checklist de Verificación - TortillApuestas

Este script verifica que todo esté instalado y configurado correctamente
"""

import subprocess
import os
import sys
from pathlib import Path

def check_command(cmd, name):
    """Verificar si un comando existe"""
    try:
        subprocess.run([cmd, "--version"], capture_output=True, check=True)
        print(f"✅ {name}")
        return True
    except:
        print(f"❌ {name} - No instalado")
        return False

def check_file(path, name):
    """Verificar si un archivo existe"""
    if Path(path).exists():
        print(f"✅ {name}")
        return True
    else:
        print(f"❌ {name} - Archivo no encontrado")
        return False

def main():
    print("🔍 Verificando TortillApuestas...")
    print()
    
    checks = []
    
    # 1. Verificar herramientas instaladas
    print("1️⃣  Herramientas Instaladas:")
    checks.append(check_command("docker", "Docker"))
    checks.append(check_command("docker-compose", "Docker Compose"))
    print()
    
    # 2. Verificar estructura de archivos
    print("2️⃣  Estructura de Archivos:")
    checks.append(check_file("backend/main.py", "Backend API"))
    checks.append(check_file("backend/models.py", "Modelos BD"))
    checks.append(check_file("backend/Dockerfile", "Dockerfile"))
    checks.append(check_file("frontend/index.html", "Frontend"))
    checks.append(check_file("docker-compose.yml", "Docker Compose"))
    checks.append(check_file("nginx.conf", "Nginx Config"))
    print()
    
    # 3. Verificar documentación
    print("3️⃣  Documentación:")
    checks.append(check_file("DEPLOYMENT.md", "Guía Deployment"))
    checks.append(check_file("ARCHITECTURE.md", "Arquitectura"))
    checks.append(check_file("QUICKSTART.md", "Quick Start"))
    print()
    
    # 4. Verificar configuración
    print("4️⃣  Configuración:")
    checks.append(check_file(".env.example", "Template de variables"))
    checks.append(check_file(".env.development", "Config desarrollo"))
    print()
    
    # 5. Verificar scripts
    print("5️⃣  Scripts:")
    checks.append(check_file("init.sh", "Script inicialización"))
    checks.append(check_file("stop.sh", "Script parada"))
    print()
    
    # 6. Services listening (si están corriendo)
    print("6️⃣  Servicios en línea:")
    try:
        result = subprocess.run(["docker-compose", "ps"], capture_output=True, text=True)
        if "tortilla" in result.stdout:
            print("✅ Docker Compose servicios activos")
            checks.append(True)
        else:
            print("⚠️  Docker Compose - Sin servicios activos (es normal si no has ejecutado init.sh)")
            checks.append(True)
    except:
        print("⚠️  Docker Compose no disponible")
        checks.append(False)
    print()
    
    # Resumen final
    total = len(checks)
    passed = sum(checks)
    
    print(f"📊 Resultado: {passed}/{total} verificaciones pasadas")
    print()
    
    if all(checks[:8]):  # Los checks más importantes
        print("✅ ¡TODO ESTÁ BIEN! Puedes ejecutar:")
        print()
        print("   chmod +x init.sh")
        print("   ./init.sh")
        print()
        print("O para instrucciones: lee QUICKSTART.md o DEPLOYMENT.md")
        return 0
    else:
        print("❌ Hay problemas. Instala lo que falta y vuelve a intentar.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
