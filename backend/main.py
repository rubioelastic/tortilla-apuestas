"""
🚀 API Principal - TortillApuestas Backend
FastAPI server con endpoints CRUD
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from datetime import timedelta, datetime
import logging

# Importar nuestros módulos
from database import init_db, get_db
from models import User, Bet, BetParticipant
from schemas import (
    UserCreate, UserLogin, UserResponse, UserUpdate, PasswordChange,
    BetCreate, BetJoin, BetInvite, BetChooseOption, BetUpdate, BetResponse, BetFinalize, BetMarkPaid,
    Token, RankingItem, StatsResponse, GlobalStatsResponse, HallOfFameResponse
)
from auth import (
    hash_password, verify_password, create_access_token,
    get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
)
import telegram_service

# ═══════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════

app = FastAPI(
    title="TortillApuestas API",
    description="API para gestionar apuestas entre amigos",
    version="1.0.0",
    docs_url="/docs",  # Documentación en /docs
    redoc_url="/redoc"
)

# Configurar CORS (permitir requests desde tu frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8080",
        "https://tortilla.rubiocloud.duckdns.org",
        "http://tortilla.rubiocloud.duckdns.org",
        "https://api.tortilla.rubiocloud.duckdns.org",
        "http://api.tortilla.rubiocloud.duckdns.org",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar BD al startup
@app.on_event("startup")
async def startup():
    init_db()
    logger.info("🚀 API iniciada - TortillApuestas")


# ═══════════════════════════════════════════════════════════════
# HEALTH CHECK
# ═══════════════════════════════════════════════════════════════

@app.get("/health")
async def health_check():
    """Verificar que el servidor está en línea"""
    return {"status": "✅ API en línea"}


# ═══════════════════════════════════════════════════════════════
# TELEGRAM - CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════

@app.get("/api/telegram/get-chat-id")
async def get_telegram_chat_id():
    """
    Obtener el Chat ID del grupo de Telegram
    IMPORTANTE: El bot debe estar en el grupo y debe haberse enviado al menos 1 mensaje
    """
    chat_id = telegram_service.get_chat_id()
    if chat_id:
        # Auto-configurar el chat_id
        telegram_service.set_chat_id(chat_id)
        return {
            "success": True,
            "chat_id": chat_id,
            "message": f"✅ Chat ID obtenido y configurado automáticamente: {chat_id}"
        }
    else:
        return {
            "success": False,
            "message": "No se pudo obtener el Chat ID. Asegúrate de que:\n1. El bot está en el grupo\n2. Se ha enviado al menos 1 mensaje en el grupo\n3. Intenta /api/telegram/debug para ver más detalles"
        }


@app.get("/api/telegram/debug")
async def debug_telegram():
    """Ver todos los updates recibidos por el bot (para debugging)"""
    try:
        import requests
        response = requests.get(f"https://api.telegram.org/bot{telegram_service.TELEGRAM_BOT_TOKEN}/getUpdates")
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "updates_count": len(data.get("result", [])),
                "updates": data.get("result", [])
            }
        else:
            return {
                "success": False,
                "error": f"Error {response.status_code}: {response.text}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@app.post("/api/telegram/set-chat-id")
async def set_telegram_chat_id(chat_id: int):
    """Configurar el Chat ID del grupo"""
    telegram_service.set_chat_id(chat_id)
    return {
        "success": True,
        "message": f"Chat ID configurado: {chat_id}",
        "chat_id": chat_id
    }


@app.post("/api/telegram/test")
async def test_telegram():
    """Enviar un mensaje de prueba al grupo de Telegram"""
    success = telegram_service.send_message("🧪 *Mensaje de prueba*\n\n✅ TortillApuestas está conectado correctamente a Telegram!")
    
    if success:
        return {"success": True, "message": "Mensaje de prueba enviado correctamente"}
    else:
        return {"success": False, "message": "Error al enviar mensaje. Verifica que el Chat ID esté configurado"}


@app.post("/api/telegram/remind-debts")
async def remind_pending_debts(db: Session = Depends(get_db)):
    """
    🔔 Recordatorio semanal de deudas pendientes
    
    Este endpoint envía un recordatorio a Telegram con todas las apuestas 
    finalizadas pero no pagadas (estado 'completed').
    
    Se puede llamar manualmente o programar con un cron job semanal.
    """
    try:
        # Obtener todas las apuestas completadas pero no pagadas
        pending_bets = db.query(Bet).options(
            joinedload(Bet.creator),
            joinedload(Bet.participants).joinedload(BetParticipant.user)
        ).filter(Bet.status == "completed").all()
        
        if not pending_bets:
            return {
                "success": True, 
                "message": "No hay deudas pendientes",
                "pending_count": 0
            }
        
        # Construir mensaje de recordatorio
        message = f"""⏰ *RECORDATORIO SEMANAL - TORTILLAS PENDIENTES*

📊 Hay *{len(pending_bets)} apuesta(s)* sin pagar:

"""
        
        for bet in pending_bets:
            # Identificar perdedores (quienes NO eligieron la opción ganadora)
            losers = []
            for participant in bet.participants:
                if participant.chosen_option != bet.winning_option and participant.chosen_option:
                    losers.append(participant.user.display_name if participant.user else "Anónimo")
            
            losers_text = ", ".join(losers) if losers else "Nadie"
            
            message += f"""━━━━━━━━━━━━━━━━━━━━
🎯 *{bet.title}*
💰 Tortillas: {bet.tortillas_count}
😢 Deben pagar: {losers_text}
📅 Finalizada: {bet.completed_at.strftime('%d/%m/%Y') if bet.completed_at else 'Fecha desconocida'}

"""
        
        message += f"""━━━━━━━━━━━━━━━━━━━━
🥞 ¡A pagar las tortillas, amigos!
🔗 https://tortilla.rubiocloud.duckdns.org
"""
        
        # Enviar mensaje
        success = telegram_service.send_message(message)
        
        if success:
            logger.info(f"📢 Recordatorio de {len(pending_bets)} deudas enviado a Telegram")
            return {
                "success": True,
                "message": f"Recordatorio enviado: {len(pending_bets)} deuda(s) pendiente(s)",
                "pending_count": len(pending_bets)
            }
        else:
            return {
                "success": False,
                "message": "Error al enviar recordatorio a Telegram",
                "pending_count": len(pending_bets)
            }
            
    except Exception as e:
        logger.error(f"❌ Error en recordatorio de deudas: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar recordatorio: {str(e)}"
        )


@app.post("/api/telegram/hall-of-fame")
async def send_hall_of_fame_telegram(
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    🏆 Enviar Hall of Fame/Shame a Telegram
    
    Calcula y envía las estadísticas más divertidas al grupo de Telegram:
    - Rey de las Tortillas (más victorias)
    - Peor Pagador (más deudas pendientes)
    - Apostador Compulsivo (más apuestas creadas)
    - El Generoso (paga más rápido)
    - Rachas actuales (ganadoras y perdedoras)
    """
    try:
        # Obtener estadísticas del Hall of Fame
        users = db.query(User).all()
        
        hall_data = {
            "king_of_tortillas": None,
            "worst_payer": None,
            "compulsive_better": None,
            "generous_one": None,
            "winning_streak": None,
            "losing_streak": None
        }
        
        king_stats = {"user_id": None, "display_name": "Nadie", "wins": 0}
        worst_payer_stats = {"user_id": None, "display_name": "Nadie", "pending_tortillas": 0}
        compulsive_stats = {"user_id": None, "display_name": "Nadie", "participations_count": 0}
        generous_stats = {"user_id": None, "display_name": "Nadie", "tortillas_paid": 0}
        winning_streak_stats = {"user_id": None, "display_name": "Nadie", "streak": 0}
        losing_streak_stats = {"user_id": None, "display_name": "Nadie", "streak": 0}
        
        for user in users:
            # Calcular victorias
            participations = db.query(BetParticipant).filter(
                BetParticipant.user_id == user.id
            ).all()
            
            wins = 0
            for part in participations:
                bet = db.query(Bet).filter(Bet.id == part.bet_id).first()
                if bet and bet.status in ["completed", "paid"] and bet.winning_option:
                    if part.chosen_option == bet.winning_option:
                        wins += 1
            
            if wins > king_stats["wins"]:
                king_stats = {"user_id": user.id, "display_name": user.display_name, "wins": wins}
            
            # Calcular deudas pendientes
            pending = db.query(BetParticipant).join(Bet).filter(
                BetParticipant.user_id == user.id,
                Bet.status == "completed",
                Bet.winning_option.isnot(None),
                BetParticipant.chosen_option != Bet.winning_option,
                BetParticipant.chosen_option.isnot(None)
            ).all()
            
            pending_tortillas = sum([p.bet.tortillas_count for p in pending if p.bet])
            
            if pending_tortillas > worst_payer_stats["pending_tortillas"]:
                worst_payer_stats = {
                    "user_id": user.id,
                    "display_name": user.display_name,
                    "pending_tortillas": pending_tortillas
                }
            
            # Calcular participaciones (apuestas en las que ha participado)
            participations_count = db.query(BetParticipant).filter(BetParticipant.user_id == user.id).count()
            if participations_count > compulsive_stats["participations_count"]:
                compulsive_stats = {
                    "user_id": user.id,
                    "display_name": user.display_name,
                    "participations_count": participations_count
                }
            
            # Calcular tortillas pagadas (El Generoso)
            paid_losses = db.query(BetParticipant).join(Bet).filter(
                BetParticipant.user_id == user.id,
                Bet.status == "paid",
                Bet.winning_option.isnot(None),
                BetParticipant.chosen_option != Bet.winning_option,
                BetParticipant.chosen_option.isnot(None)
            ).all()
            
            if paid_losses:
                total_tortillas_paid = sum(pl.bet.tortillas_count for pl in paid_losses)
                
                if total_tortillas_paid > generous_stats["tortillas_paid"]:
                    generous_stats = {
                        "user_id": user.id,
                        "display_name": user.display_name,
                        "tortillas_paid": total_tortillas_paid
                    }
            
            # Calcular racha actual
            recent_bets = db.query(BetParticipant).join(Bet).filter(
                BetParticipant.user_id == user.id,
                Bet.status.in_(["completed", "paid"]),
                Bet.winning_option.isnot(None),
                BetParticipant.chosen_option.isnot(None)
            ).order_by(desc(Bet.completed_at)).limit(20).all()
            
            if recent_bets:
                current_streak = 0
                streak_type = None
                
                for bet_part in recent_bets:
                    is_win = bet_part.chosen_option == bet_part.bet.winning_option
                    
                    if streak_type is None:
                        streak_type = "win" if is_win else "loss"
                        current_streak = 1
                    elif (streak_type == "win" and is_win) or (streak_type == "loss" and not is_win):
                        current_streak += 1
                    else:
                        break
                
                if streak_type == "win" and current_streak > winning_streak_stats["streak"]:
                    winning_streak_stats = {
                        "user_id": user.id,
                        "display_name": user.display_name,
                        "streak": current_streak
                    }
                elif streak_type == "loss" and current_streak > losing_streak_stats["streak"]:
                    losing_streak_stats = {
                        "user_id": user.id,
                        "display_name": user.display_name,
                        "streak": current_streak
                    }
        
        # Preparar datos para enviar
        if king_stats["wins"] > 0:
            hall_data["king_of_tortillas"] = king_stats
        if worst_payer_stats["pending_tortillas"] > 0:
            hall_data["worst_payer"] = worst_payer_stats
        if compulsive_stats["participations_count"] > 0:
            hall_data["compulsive_better"] = compulsive_stats
        if generous_stats["tortillas_paid"] > 0:
            hall_data["generous_one"] = generous_stats
        if winning_streak_stats["streak"] > 0:
            hall_data["winning_streak"] = winning_streak_stats
        if losing_streak_stats["streak"] > 0:
            hall_data["losing_streak"] = losing_streak_stats
        
        # Enviar mensaje a Telegram
        success = telegram_service.send_hall_of_fame(hall_data)
        
        if success:
            logger.info("🏆 Hall of Fame enviado a Telegram")
            return {
                "success": True,
                "message": "Hall of Fame enviado a Telegram",
                "data": hall_data
            }
        else:
            return {
                "success": False,
                "message": "Error al enviar Hall of Fame a Telegram"
            }
            
    except Exception as e:
        logger.error(f"❌ Error enviando Hall of Fame: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al enviar Hall of Fame: {str(e)}"
        )


# ═══════════════════════════════════════════════════════════════
# AUTENTICACIÓN - USUARIOS
# ═══════════════════════════════════════════════════════════════

@app.post("/api/auth/register", response_model=Token)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Registrar nuevo usuario"""
    
    # Verificar si usuario ya existe
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario o email ya existe"
        )
    
    # Crear nuevo usuario
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        display_name=user_data.display_name,
        phone=user_data.phone
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Crear token
    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    logger.info(f"✅ Usuario registrado: {db_user.username}")
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(db_user)
    }


@app.post("/api/auth/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login de usuario"""
    
    # Buscar usuario
    db_user = db.query(User).filter(User.username == user_data.username).first()
    
    if not db_user or not verify_password(user_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )
    
    if not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    # Crear token
    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    logger.info(f"✅ Login: {db_user.username}")
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(db_user)
    }


@app.get("/api/auth/me", response_model=UserResponse)
async def get_me(
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener datos del usuario actual"""
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UserResponse.from_orm(db_user)


@app.get("/api/users/me", response_model=UserResponse)
async def get_user_me(
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Alias para /api/auth/me - Obtener datos del usuario actual"""
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UserResponse.from_orm(db_user)


@app.put("/api/auth/me", response_model=UserResponse)
async def update_me(
    user_update: UserUpdate,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualizar datos del usuario actual"""
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if user_update.display_name:
        db_user.display_name = user_update.display_name
    if user_update.phone:
        db_user.phone = user_update.phone
    
    db.commit()
    db.refresh(db_user)
    return UserResponse.from_orm(db_user)


@app.post("/api/auth/change-password")
async def change_password(
    password_data: PasswordChange,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cambiar contraseña del usuario actual"""
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Verificar contraseña actual
    if not verify_password(password_data.current_password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")
    
    # Actualizar contraseña
    db_user.hashed_password = hash_password(password_data.new_password)
    db.commit()
    
    return {"message": "Contraseña actualizada exitosamente"}


@app.get("/api/users", response_model=list[UserResponse])
async def list_users(
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Listar todos los usuarios registrados"""
    users = db.query(User).order_by(User.display_name).all()
    return [UserResponse.from_orm(user) for user in users]


# ═══════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════
# APUESTAS - CRUD
# ═══════════════════════════════════════════════════════════════

@app.post("/api/bets", response_model=BetResponse)
async def create_bet(
    bet_data: BetCreate,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crear nueva apuesta"""
    
    # Obtener usuario actual
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Crear apuesta
    db_bet = Bet(
        title=bet_data.title,
        description=bet_data.description,
        options=bet_data.options,
        creator_id=db_user.id,
        status="open"
    )
    
    db.add(db_bet)
    db.commit()
    db.refresh(db_bet)
    
    # Añadir usuarios invitados
    if bet_data.invited_user_ids:
        for user_id in bet_data.invited_user_ids:
            # Verificar que el usuario existe
            invited_user = db.query(User).filter(User.id == user_id).first()
            if invited_user:
                # Verificar si se ha asignado una opción para este usuario
                chosen_option = None
                if bet_data.participant_choices and user_id in bet_data.participant_choices:
                    chosen_option = bet_data.participant_choices[user_id]
                
                # Crear participación con o sin opción elegida
                participant = BetParticipant(
                    bet_id=db_bet.id,
                    user_id=user_id,
                    chosen_option=chosen_option
                )
                db.add(participant)
        db.commit()
    
    # Recargar la apuesta con todas sus relaciones para el response
    db_bet = db.query(Bet).options(
        joinedload(Bet.creator),
        joinedload(Bet.participants).joinedload(BetParticipant.user)
    ).filter(Bet.id == db_bet.id).first()
    
    logger.info(f"✅ Apuesta creada: {db_bet.title} por {username}")
    
    # 🔔 Enviar notificación a Telegram sobre la nueva apuesta
    try:
        participants = []
        for participant in db_bet.participants:
            if participant.user:
                participants.append({
                    "name": participant.user.display_name or participant.user.username,
                    "chosen_option": participant.chosen_option
                })
        
        bet_data = {
            "title": db_bet.title,
            "description": db_bet.description or "Sin descripción",
            "participants": participants,
            "date": db_bet.created_at.strftime("%d/%m/%Y")
        }
        telegram_service.notify_new_bet(bet_data)
        logger.info("📱 Notificación de nueva apuesta enviada a Telegram")
    except Exception as e:
        logger.error(f"⚠️ Error enviando notificación a Telegram: {e}")
        # No fallar el endpoint si falla la notificación
    
    return BetResponse.from_orm(db_bet)


@app.get("/api/bets", response_model=list[BetResponse])
async def list_bets(
    status: str = None,
    skip: int = 0,
    limit: int = 50,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Listar apuestas (todas o por estado)"""
    
    query = db.query(Bet)
    
    if status:
        query = query.filter(Bet.status == status)
    
    bets = query.order_by(desc(Bet.created_at)).offset(skip).limit(limit).all()
    return [BetResponse.from_orm(bet) for bet in bets]


@app.get("/api/bets/{bet_id}", response_model=BetResponse)
async def get_bet(
    bet_id: int,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener detalles de una apuesta"""
    
    db_bet = db.query(Bet).filter(Bet.id == bet_id).first()
    if not db_bet:
        raise HTTPException(status_code=404, detail="Apuesta no encontrada")
    
    return BetResponse.from_orm(db_bet)


@app.put("/api/bets/{bet_id}", response_model=BetResponse)
async def update_bet(
    bet_id: int,
    bet_update: BetUpdate,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualizar apuesta (solo el creador)"""
    
    db_user = db.query(User).filter(User.username == username).first()
    db_bet = db.query(Bet).filter(Bet.id == bet_id).first()
    
    if not db_bet:
        raise HTTPException(status_code=404, detail="Apuesta no encontrada")
    
    if db_bet.creator_id != db_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el creador puede modificar la apuesta"
        )
    
    # Solo permitir editar si la apuesta está en estado "open"
    if db_bet.status != "open" and any([
        bet_update.options,
        bet_update.participant_choices,
        bet_update.remove_participants,
        bet_update.add_participants
    ]):
        raise HTTPException(
            status_code=400,
            detail="Solo se pueden editar participantes y opciones en apuestas abiertas"
        )
    
    # Actualizar campos básicos
    if bet_update.title:
        db_bet.title = bet_update.title
    if bet_update.description is not None:
        db_bet.description = bet_update.description
    if bet_update.notes is not None:
        db_bet.notes = bet_update.notes
    if bet_update.tortillas_count:
        db_bet.tortillas_count = bet_update.tortillas_count
    
    # Actualizar opciones de la apuesta
    if bet_update.options is not None:
        db_bet.options = bet_update.options
    
    # Eliminar participantes
    if bet_update.remove_participants:
        db.query(BetParticipant).filter(
            BetParticipant.bet_id == bet_id,
            BetParticipant.user_id.in_(bet_update.remove_participants)
        ).delete(synchronize_session=False)
    
    # Añadir nuevos participantes
    if bet_update.add_participants:
        for user_id in bet_update.add_participants:
            # Verificar que el usuario existe
            user_exists = db.query(User).filter(User.id == user_id).first()
            if not user_exists:
                continue
            
            # Verificar que no esté ya añadido
            already_participant = db.query(BetParticipant).filter(
                BetParticipant.bet_id == bet_id,
                BetParticipant.user_id == user_id
            ).first()
            
            if not already_participant:
                chosen_option = None
                if bet_update.participant_choices and user_id in bet_update.participant_choices:
                    chosen_option = bet_update.participant_choices[user_id]
                
                new_participant = BetParticipant(
                    bet_id=bet_id,
                    user_id=user_id,
                    chosen_option=chosen_option
                )
                db.add(new_participant)
    
    # Actualizar opciones de participantes existentes
    if bet_update.participant_choices:
        for user_id, chosen_option in bet_update.participant_choices.items():
            participant = db.query(BetParticipant).filter(
                BetParticipant.bet_id == bet_id,
                BetParticipant.user_id == user_id
            ).first()
            
            if participant:
                participant.chosen_option = chosen_option if chosen_option else None
    
    # Actualizar estado
    if bet_update.status:
        # Si se está cerrando la apuesta, verificar que haya al menos 2 participantes con opción elegida
        if bet_update.status == "closed" and db_bet.status == "open":
            participants_with_choice = db.query(BetParticipant).filter(
                BetParticipant.bet_id == bet_id,
                BetParticipant.chosen_option.isnot(None)
            ).count()
            
            if participants_with_choice < 2:
                raise HTTPException(
                    status_code=400,
                    detail=f"No se puede cerrar la apuesta. Se requieren mínimo 2 participantes con opción elegida. Actual: {participants_with_choice}"
                )
        
        db_bet.status = bet_update.status
        if bet_update.status == "closed":
            db_bet.closed_at = datetime.utcnow()
    
    if bet_update.winning_option:
        db_bet.winning_option = bet_update.winning_option
    if bet_update.payment_photo is not None:
        db_bet.payment_photo = bet_update.payment_photo
    
    db.commit()
    
    # Recargar con relaciones
    db_bet = db.query(Bet).options(
        joinedload(Bet.creator),
        joinedload(Bet.participants).joinedload(BetParticipant.user)
    ).filter(Bet.id == bet_id).first()
    
    logger.info(f"✅ Apuesta actualizada: {db_bet.id}")
    return BetResponse.from_orm(db_bet)


@app.delete("/api/bets/{bet_id}")
async def delete_bet(
    bet_id: int,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Eliminar apuesta (solo el creador)"""
    
    db_user = db.query(User).filter(User.username == username).first()
    db_bet = db.query(Bet).filter(Bet.id == bet_id).first()
    
    if not db_bet:
        raise HTTPException(status_code=404, detail="Apuesta no encontrada")
    
    if db_bet.creator_id != db_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el creador puede eliminar la apuesta"
        )
    
    db.delete(db_bet)
    db.commit()
    
    logger.info(f"✅ Apuesta eliminada: {bet_id}")
    return {"detail": "Apuesta eliminada"}


@app.post("/api/bets/{bet_id}/finalize", response_model=BetResponse)
async def finalize_bet(
    bet_id: int,
    finalize_data: BetFinalize,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Finalizar apuesta con un ganador (solo el creador)"""
    
    db_user = db.query(User).filter(User.username == username).first()
    db_bet = db.query(Bet).filter(Bet.id == bet_id).first()
    
    if not db_bet:
        raise HTTPException(status_code=404, detail="Apuesta no encontrada")
    
    # Solo el creador puede finalizar
    if db_bet.creator_id != db_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el creador puede finalizar la apuesta"
        )
    
    # Verificar que esté en estado open o closed
    if db_bet.status not in ["open", "closed"]:
        raise HTTPException(
            status_code=400,
            detail=f"No se puede finalizar una apuesta en estado '{db_bet.status}'"
        )
    
    # Verificar que haya al menos 2 participantes con opción elegida
    participants_with_choice = db.query(BetParticipant).filter(
        BetParticipant.bet_id == bet_id,
        BetParticipant.chosen_option.isnot(None)
    ).count()
    
    if participants_with_choice < 2:
        raise HTTPException(
            status_code=400,
            detail=f"No se puede finalizar la apuesta. Se requieren mínimo 2 participantes con opción elegida. Actual: {participants_with_choice}"
        )
    
    # Verificar que la opción ganadora exista (si hay opciones)
    if db_bet.options and finalize_data.winning_option not in db_bet.options:
        raise HTTPException(
            status_code=400,
            detail="La opción ganadora no es una opción válida de esta apuesta"
        )
    
    # Actualizar apuesta
    db_bet.status = "completed"
    db_bet.winning_option = finalize_data.winning_option
    db_bet.notes = finalize_data.notes
    db_bet.tortillas_count = finalize_data.tortillas_count
    db_bet.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_bet)
    
    logger.info(f"✅ Apuesta {bet_id} finalizada. Opción ganadora: {finalize_data.winning_option}")
    
    # 🔔 Enviar notificación a Telegram sobre quién perdió
    try:
        # Obtener participantes con la apuesta completa
        db_bet_with_participants = db.query(Bet).options(
            joinedload(Bet.participants).joinedload(BetParticipant.user)
        ).filter(Bet.id == bet_id).first()
        
        # Identificar ganadores y perdedores
        winners = []
        losers = []
        
        for participant in db_bet_with_participants.participants:
            if participant.chosen_option == finalize_data.winning_option:
                winners.append(participant.user.display_name if participant.user else "Anónimo")
            elif participant.chosen_option:  # Solo contar si eligió opción
                losers.append(participant.user.display_name if participant.user else "Anónimo")
        
        bet_data = {
            "title": db_bet.title,
            "description": db_bet.description,
            "winner": finalize_data.winning_option,
            "tortillas": finalize_data.tortillas_count,
            "notes": finalize_data.notes,
            "winners": ", ".join(winners) if winners else "Nadie",
            "losers": ", ".join(losers) if losers else "Nadie"
        }
        telegram_service.notify_bet_finalized(bet_data)
        logger.info("📱 Notificación de finalización enviada a Telegram")
    except Exception as e:
        logger.error(f"⚠️ Error enviando notificación a Telegram: {e}")
        # No fallar el endpoint si falla la notificación
    
    return BetResponse.from_orm(db_bet)


@app.post("/api/bets/{bet_id}/mark-paid")
async def mark_bet_as_paid(
    bet_id: int,
    mark_paid_data: BetMarkPaid,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Marcar apuesta como pagada (solo el creador)"""
    
    db_user = db.query(User).filter(User.username == username).first()
    db_bet = db.query(Bet).filter(Bet.id == bet_id).first()
    
    if not db_bet:
        raise HTTPException(status_code=404, detail="Apuesta no encontrada")
    
    # Solo el creador puede marcar como pagada
    if db_bet.creator_id != db_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el creador puede marcar como pagada"
        )
    
    # Debe estar completada para poder marcarla como pagada
    if db_bet.status != "completed":
        raise HTTPException(
            status_code=400,
            detail="La apuesta debe estar completada primero"
        )
    
    # Marcar como pagada y guardar la foto si existe
    db_bet.status = "paid"
    db_bet.paid_at = datetime.utcnow()  # Guardar fecha de pago
    if mark_paid_data.payment_photo:
        db_bet.payment_photo = mark_paid_data.payment_photo
    
    db.commit()
    db.refresh(db_bet)
    
    logger.info(f"✅ Apuesta {bet_id} marcada como pagada")
    
    # 🔔 Enviar notificación a Telegram automáticamente
    try:
        bet_data = {
            "title": db_bet.title,
            "description": db_bet.description,
            "winner": db_bet.winning_option,
            "tortillas": db_bet.tortillas_count,
            "notes": db_bet.notes
        }
        telegram_service.notify_bet_paid(bet_data, mark_paid_data.payment_photo)
        logger.info("📱 Notificación de pago enviada a Telegram")
    except Exception as e:
        logger.error(f"⚠️ Error enviando notificación a Telegram: {e}")
        # No fallar el endpoint si falla la notificación
    
    return {"detail": "Apuesta marcada como pagada", "bet_id": bet_id}


@app.post("/api/bets/{bet_id}/reopen")
async def reopen_bet(
    bet_id: int,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reabrir una apuesta cerrada (solo el creador)"""
    
    db_user = db.query(User).filter(User.username == username).first()
    db_bet = db.query(Bet).filter(Bet.id == bet_id).first()
    
    if not db_bet:
        raise HTTPException(status_code=404, detail="Apuesta no encontrada")
    
    # Solo el creador puede reabrir
    if db_bet.creator_id != db_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el creador puede reabrir la apuesta"
        )
    
    # Resetear estado
    db_bet.status = "open"
    db_bet.winning_option = None
    db_bet.completed_at = None
    db_bet.closed_at = None
    
    db.commit()
    db.refresh(db_bet)
    
    logger.info(f"✅ Apuesta {bet_id} reabierta")
    return {"detail": "Apuesta reabierta", "bet_id": bet_id}


# ═══════════════════════════════════════════════════════════════
# PARTICIPACIÓN EN APUESTAS
# ═══════════════════════════════════════════════════════════════

@app.post("/api/bets/{bet_id}/join")
async def join_bet(
    bet_id: int,
    join_data: BetJoin,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Unirse a una apuesta"""
    
    db_user = db.query(User).filter(User.username == username).first()
    db_bet = db.query(Bet).filter(Bet.id == bet_id).first()
    
    if not db_bet:
        raise HTTPException(status_code=404, detail="Apuesta no encontrada")
    
    if db_bet.status != "open":
        raise HTTPException(status_code=400, detail="Apuesta no está abierta")
    
    # Verificar si ya está en la apuesta
    existing = db.query(BetParticipant).filter(
        (BetParticipant.bet_id == bet_id) & (BetParticipant.user_id == db_user.id)
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Ya estás en esta apuesta")
    
    # Añadir participante
    participant = BetParticipant(
        bet_id=bet_id,
        user_id=db_user.id,
        chosen_option=join_data.chosen_option
    )
    db.add(participant)
    db.commit()
    
    logger.info(f"✅ {username} se unió a apuesta {bet_id}")
    return {"detail": "Unido a la apuesta"}


@app.post("/api/bets/{bet_id}/invite")
async def invite_users_to_bet(
    bet_id: int,
    invite_data: BetInvite,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Invitar usuarios adicionales a una apuesta (solo el creador)"""
    
    db_user = db.query(User).filter(User.username == username).first()
    db_bet = db.query(Bet).filter(Bet.id == bet_id).first()
    
    if not db_bet:
        raise HTTPException(status_code=404, detail="Apuesta no encontrada")
    
    # Solo el creador puede invitar
    if db_bet.creator_id != db_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el creador puede invitar usuarios"
        )
    
    invited_count = 0
    already_in = []
    not_found = []
    
    for user_id in invite_data.user_ids:
        # Verificar que el usuario existe
        invited_user = db.query(User).filter(User.id == user_id).first()
        if not invited_user:
            not_found.append(user_id)
            continue
        
        # Verificar si ya está en la apuesta
        existing = db.query(BetParticipant).filter(
            (BetParticipant.bet_id == bet_id) & (BetParticipant.user_id == user_id)
        ).first()
        
        if existing:
            already_in.append(invited_user.display_name)
            continue
        
        # Añadir participante invitado
        participant = BetParticipant(
            bet_id=bet_id,
            user_id=user_id
        )
        db.add(participant)
        invited_count += 1
    
    db.commit()
    
    logger.info(f"✅ {invited_count} usuarios invitados a apuesta {bet_id}")
    return {
        "detail": f"{invited_count} usuarios invitados",
        "invited": invited_count,
        "already_in": already_in,
        "not_found": not_found
    }


@app.put("/api/bets/{bet_id}/choose-option")
async def choose_option(
    bet_id: int,
    choice_data: BetChooseOption,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Elegir o cambiar la opción apostada (para participantes)"""
    
    db_user = db.query(User).filter(User.username == username).first()
    db_bet = db.query(Bet).filter(Bet.id == bet_id).first()
    
    if not db_bet:
        raise HTTPException(status_code=404, detail="Apuesta no encontrada")
    
    if db_bet.status not in ["open", "closed"]:
        raise HTTPException(status_code=400, detail="No se puede elegir opción en una apuesta completada o pagada")
    
    # Verificar que el usuario es participante
    participant = db.query(BetParticipant).filter(
        (BetParticipant.bet_id == bet_id) & (BetParticipant.user_id == db_user.id)
    ).first()
    
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No eres participante de esta apuesta"
        )
    
    # Validar que la opción existe en las opciones de la apuesta
    if db_bet.options and choice_data.chosen_option not in db_bet.options:
        raise HTTPException(
            status_code=400,
            detail=f"Opción inválida. Opciones disponibles: {', '.join(db_bet.options)}"
        )
    
    # Actualizar la opción elegida
    participant.chosen_option = choice_data.chosen_option
    db.commit()
    
    logger.info(f"✅ {username} eligió '{choice_data.chosen_option}' en apuesta {bet_id}")
    return {
        "detail": "Opción actualizada",
        "chosen_option": choice_data.chosen_option
    }


@app.delete("/api/bets/{bet_id}/leave")
async def leave_bet(
    bet_id: int,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Abandonar una apuesta"""
    
    db_user = db.query(User).filter(User.username == username).first()
    
    participant = db.query(BetParticipant).filter(
        (BetParticipant.bet_id == bet_id) & (BetParticipant.user_id == db_user.id)
    ).first()
    
    if not participant:
        raise HTTPException(status_code=404, detail="No estás en esta apuesta")
    
    db.delete(participant)
    db.commit()
    
    logger.info(f"✅ {username} abandonó apuesta {bet_id}")
    return {"detail": "Abandonaste la apuesta"}


# ═══════════════════════════════════════════════════════════════
# ESTADÍSTICAS Y RANKING
# ═══════════════════════════════════════════════════════════════

@app.get("/api/ranking", response_model=list[RankingItem])
async def get_ranking(
    limit: int = 10,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener ranking de usuarios"""
    
    # Query para obtener estadísticas
    users = db.query(User).all()
    
    ranking = []
    for user in users:
        # Contar victorias: apuestas completadas donde eligió la opción ganadora
        wins = 0
        participations_query = db.query(BetParticipant).filter(
            BetParticipant.user_id == user.id
        ).all()
        
        participations = len(participations_query)
        
        for part in participations_query:
            bet = db.query(Bet).filter(Bet.id == part.bet_id).first()
            if bet and bet.status in ["completed", "paid"] and bet.winning_option:
                if part.chosen_option == bet.winning_option:
                    wins += 1
        
        win_rate = (wins / participations * 100) if participations > 0 else 0
        
        ranking.append(RankingItem(
            user_id=user.id,
            username=user.username,
            display_name=user.display_name,
            wins=wins,
            total_participations=participations,
            win_rate=round(win_rate, 2)
        ))
    
    # Ordenar por wins descendente
    ranking.sort(key=lambda x: x.wins, reverse=True)
    
    return ranking[:limit]


@app.get("/api/users/{user_id}/stats", response_model=StatsResponse)
async def get_user_stats(
    user_id: int,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de un usuario"""
    
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Contar victorias: apuestas completadas donde eligió la opción ganadora
    wins = 0
    participations_query = db.query(BetParticipant).filter(
        BetParticipant.user_id == user_id
    ).all()
    
    for part in participations_query:
        bet = db.query(Bet).filter(Bet.id == part.bet_id).first()
        if bet and bet.status in ["completed", "paid"] and bet.winning_option:
            if part.chosen_option == bet.winning_option:
                wins += 1
    
    bets_created = db.query(Bet).filter(Bet.creator_id == user_id).count()
    participations = len(participations_query)
    
    # Obtener posición en ranking
    ranking = db.query(Bet).filter(Bet.winner_id != None).count()
    
    return StatsResponse(
        user_id=user_id,
        username=db_user.username,
        wins=wins,
        total_bets_created=bets_created,
        total_participations=participations,
        ranking_position=None
    )


@app.get("/api/stats/global", response_model=GlobalStatsResponse)
async def get_global_stats(
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener estadísticas globales de la aplicación"""
    
    # Contar apuestas por estado
    total_bets = db.query(Bet).count()
    active_bets = db.query(Bet).filter(Bet.status.in_(["open", "closed", "completed"])).count()
    completed_bets = db.query(Bet).filter(Bet.status == "completed").count()
    paid_bets = db.query(Bet).filter(Bet.status == "paid").count()
    
    # Calcular tortillas
    total_tortillas_owed = db.query(func.sum(Bet.tortillas_count)).filter(
        Bet.status == "completed"
    ).scalar() or 0
    
    total_tortillas_paid = db.query(func.sum(Bet.tortillas_count)).filter(
        Bet.status == "paid"
    ).scalar() or 0
    
    # Encontrar al "Rey de la Tortilla" (quien más ganó)
    # Necesitamos contar manualmente porque ahora las victorias dependen de chosen_option
    users = db.query(User).all()
    winner_stats = None
    max_wins = 0
    
    for user in users:
        wins = 0
        participations = db.query(BetParticipant).filter(
            BetParticipant.user_id == user.id
        ).all()
        
        for part in participations:
            bet = db.query(Bet).filter(Bet.id == part.bet_id).first()
            if bet and bet.status in ["completed", "paid"] and bet.winning_option:
                if part.chosen_option == bet.winning_option:
                    wins += 1
        
        if wins > max_wins:
            max_wins = wins
            winner_stats = (user.id, user.username, user.display_name, wins)
    
    top_winner = None
    if winner_stats:
        top_winner = {
            "user_id": winner_stats[0],
            "username": winner_stats[1],
            "display_name": winner_stats[2],
            "wins": winner_stats[3]
        }
    
    # Contar usuarios
    total_users = db.query(User).count()
    
    return GlobalStatsResponse(
        total_bets=total_bets,
        active_bets=active_bets,
        completed_bets=completed_bets,
        paid_bets=paid_bets,
        total_tortillas_owed=total_tortillas_owed,
        total_tortillas_paid=total_tortillas_paid,
        top_winner=top_winner,
        total_users=total_users
    )


@app.get("/api/stats/hall-of-fame", response_model=HallOfFameResponse)
async def get_hall_of_fame(
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """🏆 Hall of Fame/Shame - Estadísticas divertidas"""
    
    users = db.query(User).all()
    
    # 👑 Rey de las Tortillas (más victorias)
    king_stats = {"user_id": None, "display_name": "Nadie", "wins": 0}
    
    # 💸 Peor Pagador (más tortillas pendientes)
    worst_payer_stats = {"user_id": None, "display_name": "Nadie", "pending_tortillas": 0}
    
    # 🎰 Apostador Compulsivo (más participaciones en apuestas)
    compulsive_stats = {"user_id": None, "display_name": "Nadie", "participations_count": 0}
    
    # ⚡ El Generoso (más tortillas pagadas)
    generous_stats = {"user_id": None, "display_name": "Nadie", "tortillas_paid": 0}
    
    # 🔥 Rachas actuales
    winning_streak_stats = {"user_id": None, "display_name": "Nadie", "streak": 0}
    losing_streak_stats = {"user_id": None, "display_name": "Nadie", "streak": 0}
    
    for user in users:
        # Calcular victorias
        participations = db.query(BetParticipant).filter(
            BetParticipant.user_id == user.id
        ).all()
        
        wins = 0
        losses = 0
        for part in participations:
            bet = db.query(Bet).filter(Bet.id == part.bet_id).first()
            if bet and bet.status in ["completed", "paid"] and bet.winning_option:
                if part.chosen_option == bet.winning_option:
                    wins += 1
                elif part.chosen_option:
                    losses += 1
        
        if wins > king_stats["wins"]:
            king_stats = {"user_id": user.id, "display_name": user.display_name, "wins": wins}
        
        # Calcular deudas pendientes
        pending = db.query(BetParticipant).join(Bet).filter(
            BetParticipant.user_id == user.id,
            Bet.status == "completed",
            Bet.winning_option.isnot(None),
            BetParticipant.chosen_option != Bet.winning_option
        ).all()
        
        pending_tortillas = sum([p.bet.tortillas_count for p in pending if p.bet])
        
        if pending_tortillas > worst_payer_stats["pending_tortillas"]:
            worst_payer_stats = {
                "user_id": user.id,
                "display_name": user.display_name,
                "pending_tortillas": pending_tortillas
            }
        
        # Calcular participaciones (apuestas en las que ha participado)
        participations_count = db.query(BetParticipant).filter(BetParticipant.user_id == user.id).count()
        if participations_count > compulsive_stats["participations_count"]:
            compulsive_stats = {
                "user_id": user.id,
                "display_name": user.display_name,
                "participations_count": participations_count
            }
        
        # Calcular tortillas pagadas (El Generoso)
        paid_losses = db.query(BetParticipant).join(Bet).filter(
            BetParticipant.user_id == user.id,
            Bet.status == "paid",
            Bet.winning_option.isnot(None),
            BetParticipant.chosen_option != Bet.winning_option,
            BetParticipant.chosen_option.isnot(None)
        ).all()
        
        if paid_losses:
            total_tortillas_paid = sum(pl.bet.tortillas_count for pl in paid_losses)
            
            if total_tortillas_paid > generous_stats["tortillas_paid"]:
                generous_stats = {
                    "user_id": user.id,
                    "display_name": user.display_name,
                    "tortillas_paid": total_tortillas_paid
                }
        
        # Calcular racha actual (últimas apuestas completadas)
        recent_bets = db.query(BetParticipant).join(Bet).filter(
            BetParticipant.user_id == user.id,
            Bet.status.in_(["completed", "paid"]),
            Bet.winning_option.isnot(None),
            BetParticipant.chosen_option.isnot(None)
        ).order_by(desc(Bet.completed_at)).limit(20).all()
        
        if recent_bets:
            current_streak = 0
            streak_type = None
            
            for bet_part in recent_bets:
                is_win = bet_part.chosen_option == bet_part.bet.winning_option
                
                if streak_type is None:
                    streak_type = "win" if is_win else "loss"
                    current_streak = 1
                elif (streak_type == "win" and is_win) or (streak_type == "loss" and not is_win):
                    current_streak += 1
                else:
                    break
            
            if streak_type == "win" and current_streak > winning_streak_stats["streak"]:
                winning_streak_stats = {
                    "user_id": user.id,
                    "display_name": user.display_name,
                    "streak": current_streak
                }
            elif streak_type == "loss" and current_streak > losing_streak_stats["streak"]:
                losing_streak_stats = {
                    "user_id": user.id,
                    "display_name": user.display_name,
                    "streak": current_streak
                }
    
    return HallOfFameResponse(
        king_of_tortillas=king_stats if king_stats["wins"] > 0 else None,
        worst_payer=worst_payer_stats if worst_payer_stats["pending_tortillas"] > 0 else None,
        compulsive_better=compulsive_stats if compulsive_stats["participations_count"] > 0 else None,
        generous_one=generous_stats if generous_stats["tortillas_paid"] > 0 else None,
        winning_streak=winning_streak_stats if winning_streak_stats["streak"] > 0 else None,
        losing_streak=losing_streak_stats if losing_streak_stats["streak"] > 0 else None
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
