"""
Servicio de Telegram para notificaciones automáticas
"""
import requests
import logging
import base64
import io
from typing import Optional

logger = logging.getLogger(__name__)

# Configuración del Bot de Telegram
TELEGRAM_BOT_TOKEN = "8677854391:AAHDh2FrviLoma6eOyeMuEH7qKmKJNy6CEE"
TELEGRAM_CHAT_ID = -5280226198  # Chat ID del grupo TortillApuestas

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def get_chat_id():
    """
    Obtener el chat_id del grupo.
    Llama a esta función después de que el bot sea añadido al grupo.
    """
    try:
        # Primero intentar con offset para obtener los updates más recientes
        response = requests.get(f"{TELEGRAM_API_URL}/getUpdates?offset=-1")
        if response.status_code == 200:
            data = response.json()
            logger.info(f"📥 Updates recibidos: {len(data.get('result', []))} mensajes")
            
            if data.get("result"):
                # Buscar el último mensaje en un grupo
                for update in reversed(data["result"]):
                    logger.info(f"🔍 Analizando update: {update.get('update_id')}")
                    
                    # Verificar diferentes tipos de updates
                    chat = None
                    if "message" in update and "chat" in update["message"]:
                        chat = update["message"]["chat"]
                    elif "my_chat_member" in update and "chat" in update["my_chat_member"]:
                        chat = update["my_chat_member"]["chat"]
                    elif "channel_post" in update and "chat" in update["channel_post"]:
                        chat = update["channel_post"]["chat"]
                    
                    if chat and chat["type"] in ["group", "supergroup"]:
                        logger.info(f"✅ Chat ID encontrado: {chat['id']}")
                        logger.info(f"   Nombre del grupo: {chat.get('title', 'N/A')}")
                        logger.info(f"   Tipo: {chat['type']}")
                        return chat["id"]
                
                logger.warning("⚠️ No se encontraron grupos en los updates recientes")
                logger.info("💡 Intenta enviar un mensaje en el grupo y vuelve a intentarlo")
            else:
                logger.warning("⚠️ No hay updates disponibles")
                logger.info("💡 Asegúrate de que:")
                logger.info("   1. El bot está añadido al grupo")
                logger.info("   2. Has enviado al menos 1 mensaje en el grupo")
        else:
            logger.error(f"❌ Error al obtener updates: {response.status_code}")
            logger.error(f"   Respuesta: {response.text}")
    except Exception as e:
        logger.error(f"❌ Error obteniendo chat_id: {e}")
    return None


def set_chat_id(chat_id: int):
    """Configurar el chat_id del grupo"""
    global TELEGRAM_CHAT_ID
    TELEGRAM_CHAT_ID = chat_id
    logger.info(f"✅ Chat ID configurado: {chat_id}")


def send_message(text: str, parse_mode: str = "Markdown") -> bool:
    """
    Enviar un mensaje de texto al grupo de Telegram
    """
    if not TELEGRAM_CHAT_ID:
        logger.error("❌ Chat ID no configurado")
        return False
    
    try:
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": parse_mode
        }
        
        response = requests.post(f"{TELEGRAM_API_URL}/sendMessage", json=payload)
        
        if response.status_code == 200:
            logger.info("✅ Mensaje enviado correctamente a Telegram")
            return True
        else:
            logger.error(f"❌ Error enviando mensaje: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error enviando mensaje a Telegram: {e}")
        return False


def send_photo(photo_base64: str, caption: str = "", parse_mode: str = "Markdown") -> bool:
    """
    Enviar una foto al grupo de Telegram
    
    Args:
        photo_base64: Imagen en formato base64 (debe incluir el prefijo data:image/...)
        caption: Texto que acompaña la foto
        parse_mode: Formato del texto (Markdown o HTML)
    """
    if not TELEGRAM_CHAT_ID:
        logger.error("❌ Chat ID no configurado")
        return False
    
    try:
        # Extraer el contenido base64 (sin el prefijo data:image/...)
        if "base64," in photo_base64:
            photo_data = photo_base64.split("base64,")[1]
        else:
            photo_data = photo_base64
        
        # Decodificar base64 a bytes
        photo_bytes = base64.b64decode(photo_data)
        
        # Preparar el archivo
        files = {
            "photo": ("photo.jpg", io.BytesIO(photo_bytes), "image/jpeg")
        }
        
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "caption": caption,
            "parse_mode": parse_mode
        }
        
        response = requests.post(
            f"{TELEGRAM_API_URL}/sendPhoto",
            data=data,
            files=files
        )
        
        if response.status_code == 200:
            logger.info("✅ Foto enviada correctamente a Telegram")
            return True
        else:
            logger.error(f"❌ Error enviando foto: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error enviando foto a Telegram: {e}")
        return False


def send_message_with_photo(text: str, photo_base64: Optional[str] = None) -> bool:
    """
    Enviar un mensaje con foto opcional
    
    Args:
        text: Mensaje de texto
        photo_base64: Foto en base64 (opcional)
    """
    if photo_base64:
        # Si hay foto, enviarla con el texto como caption
        return send_photo(photo_base64, caption=text)
    else:
        # Si no hay foto, solo enviar el texto
        return send_message(text)


# Funciones de notificación específicas

def notify_new_bet(bet_data: dict) -> bool:
    """Notificar cuando se crea una nueva apuesta"""
    participants = ", ".join([p.get("name", "Usuario") for p in bet_data.get("participants", [])])
    
    message = f"""🎲 *NUEVA APUESTA EN TORTILLAPUESTAS*

*Título:* {bet_data.get("title", "Sin título")}
*Descripción:* {bet_data.get("description", "Sin descripción")}
*Participantes:* {participants or "Sin participantes"}
*Fecha:* {bet_data.get("date", "Hoy")}

¡Entra en la app para ver los detalles!
🔗 https://tortilla.rubiocloud.duckdns.org
"""
    
    return send_message(message)


def notify_bet_finalized(bet_data: dict) -> bool:
    """Notificar cuando se finaliza una apuesta"""
    winners = bet_data.get("winners", "Nadie")
    losers = bet_data.get("losers", "Nadie")
    
    message = f"""✅ *APUESTA FINALIZADA*

*Apuesta:* {bet_data.get("title", "Sin título")}
*Opción ganadora:* {bet_data.get("winner", "No definido")}
*Tortillas a pagar:* {bet_data.get("tortillas", 1)}

🏆 *Ganadores:* {winners}
😢 *Perdedores (deben tortillas):* {losers}

*Resultado:* {bet_data.get("notes", "Sin notas")}

🥞 ¡Los perdedores deben pagar las tortillas!
🔗 https://tortilla.rubiocloud.duckdns.org
"""
    
    return send_message(message)


def notify_bet_paid(bet_data: dict, photo_base64: Optional[str] = None) -> bool:
    """Notificar cuando se paga una apuesta (con foto opcional)"""
    message = f"""🎉 *APUESTA PAGADA - TORTILLAPUESTAS*

*Apuesta:* {bet_data.get("title", "Sin título")}
*Descripción:* {bet_data.get("description", "Sin descripción")}
*Ganador:* {bet_data.get("winner", "No definido")}
*Tortillas pagadas:* {bet_data.get("tortillas", 1)}
*Resultado:* {bet_data.get("notes", "Sin notas")}

✅ Las tortillas han sido pagadas. ¡Apuesta cerrada!
🔗 https://tortilla.rubiocloud.duckdns.org
"""
    
    return send_message_with_photo(message, photo_base64)


def send_hall_of_fame(hall_data: dict) -> bool:
    """🏆 Enviar Hall of Fame/Shame al grupo"""
    
    message = """🏆 *HALL OF FAME / SHAME* 🏆

𝗘𝘀𝘁𝗮𝗱í𝘀𝘁𝗶𝗰𝗮𝘀 𝗱𝗲 𝗧𝗼𝗿𝘁𝗶𝗹𝗹𝗔𝗽𝘂𝗲𝘀𝘁𝗮𝘀

"""
    
    # 👑 Rey de las Tortillas
    if hall_data.get("king_of_tortillas"):
        king = hall_data["king_of_tortillas"]
        message += f"""👑 *REY DE LAS TORTILLAS*
{king['display_name']} - {king['wins']} victorias

"""
    
    # 🔥 Racha Ganadora
    if hall_data.get("winning_streak"):
        streak = hall_data["winning_streak"]
        message += f"""🔥 *RACHA GANADORA*
{streak['display_name']} - {streak['streak']} victorias consecutivas

"""
    
    # 🎰 Apostador Compulsivo
    if hall_data.get("compulsive_better"):
        comp = hall_data["compulsive_better"]
        message += f"""🎰 *APOSTADOR COMPULSIVO*
{comp['display_name']} - {comp['participations_count']} participaciones

"""
    
    # ⚡ El Generoso
    if hall_data.get("generous_one"):
        gen = hall_data["generous_one"]
        message += f"""⚡ *EL GENEROSO*
{gen['display_name']} - {gen['tortillas_paid']} tortillas pagadas

"""
    
    # 💸 Peor Pagador
    if hall_data.get("worst_payer"):
        worst = hall_data["worst_payer"]
        message += f"""💸 *PEOR PAGADOR*
{worst['display_name']} - {worst['pending_tortillas']} tortillas pendientes

"""
    
    # 💀 Racha Perdedora
    if hall_data.get("losing_streak"):
        losing = hall_data["losing_streak"]
        message += f"""💀 *RACHA PERDEDORA*
{losing['display_name']} - {losing['streak']} derrotas consecutivas

"""
    
    message += """━━━━━━━━━━━━━━━━
🥞 ¡Que fluyan las tortillas!
🔗 https://tortilla.rubiocloud.duckdns.org"""
    
    return send_message(message)
