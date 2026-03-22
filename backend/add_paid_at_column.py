#!/usr/bin/env python3
"""
Script de migración: Agregar columna paid_at a la tabla bets
"""
import sqlite3
from datetime import datetime

DB_PATH = "/app/data/tortilla_apuestas_dev.db"

def migrate():
    """Agregar columna paid_at a la tabla bets"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Verificar si la columna ya existe
        cursor.execute("PRAGMA table_info(bets)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'paid_at' in columns:
            print("✅ La columna 'paid_at' ya existe en la tabla 'bets'")
            return
        
        # Agregar la columna paid_at
        cursor.execute("""
            ALTER TABLE bets 
            ADD COLUMN paid_at TIMESTAMP
        """)
        
        conn.commit()
        print("✅ Columna 'paid_at' agregada exitosamente a la tabla 'bets'")
        
        # Opcional: Actualizar apuestas ya pagadas con la fecha de completed_at
        cursor.execute("""
            UPDATE bets 
            SET paid_at = completed_at 
            WHERE status = 'paid' AND paid_at IS NULL AND completed_at IS NOT NULL
        """)
        
        affected_rows = cursor.rowcount
        conn.commit()
        
        if affected_rows > 0:
            print(f"✅ {affected_rows} apuesta(s) pagadas actualizadas con paid_at")
        
    except sqlite3.Error as e:
        print(f"❌ Error en la migración: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔄 Iniciando migración: Agregar columna paid_at")
    migrate()
    print("✅ Migración completada")
