"""
✅ Esquemas de Validación Pydantic
Define qué datos pueden enviar desde el frontend
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
from datetime import datetime


# ═══════════════════════════════════════════════════════════════
# USUARIO
# ═══════════════════════════════════════════════════════════════

class UserCreate(BaseModel):
    """Datos para registrar nuevo usuario"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    display_name: str = Field(..., min_length=2, max_length=100)
    phone: Optional[str] = None


class UserLogin(BaseModel):
    """Datos para login"""
    username: str
    password: str


class UserResponse(BaseModel):
    """Datos de usuario para enviar al frontend"""
    id: int
    username: str
    email: str
    display_name: str
    phone: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Actualizar datos de usuario"""
    display_name: Optional[str] = None
    phone: Optional[str] = None


class PasswordChange(BaseModel):
    """Cambiar contraseña de usuario"""
    current_password: str
    new_password: str = Field(..., min_length=6, max_length=100)


# ═══════════════════════════════════════════════════════════════
# APUESTA
# ═══════════════════════════════════════════════════════════════

class BetCreate(BaseModel):
    """Crear nueva apuesta"""
    title: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = None
    options: Optional[List[str]] = Field(None, description="Lista de opciones (ej: ['Madrid', 'Barcelona', 'Empate'])")
    invited_user_ids: Optional[List[int]] = Field(None, description="IDs de usuarios invitados")
    participant_choices: Optional[Dict[int, str]] = Field(None, description="Diccionario con user_id como clave y opción elegida como valor")


class BetJoin(BaseModel):
    """Unirse a una apuesta con selección opcional"""
    chosen_option: Optional[str] = Field(None, description="Opción elegida (texto)")


class BetInvite(BaseModel):
    """Invitar usuarios adicionales a una apuesta"""
    user_ids: List[int] = Field(..., description="IDs de usuarios a invitar")


class BetChooseOption(BaseModel):
    """Elegir opción para una apuesta (para participantes invitados)"""
    chosen_option: str = Field(..., min_length=1, description="Opción elegida (texto)")


class BetUpdate(BaseModel):
    """Actualizar apuesta"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None  # open, closed, completed, paid
    winning_option: Optional[str] = None
    notes: Optional[str] = None
    tortillas_count: Optional[int] = None
    options: Optional[List[str]] = None  # Actualizar opciones
    participant_choices: Optional[Dict[int, str]] = None  # Actualizar asignaciones de participantes
    remove_participants: Optional[List[int]] = None  # IDs de participantes a eliminar
    add_participants: Optional[List[int]] = None  # IDs de nuevos participantes a añadir
    payment_photo: Optional[str] = None


class BetFinalize(BaseModel):
    """Finalizar una apuesta con ganador"""
    winning_option: str = Field(..., description="Opción ganadora (texto)")
    notes: Optional[str] = Field(None, max_length=500, description="Resultado/notas de la apuesta")
    tortillas_count: int = Field(1, ge=1, le=100, description="Número de tortillas a pagar")


class BetMarkPaid(BaseModel):
    """Marcar apuesta como pagada"""
    paid_notes: Optional[str] = Field(None, max_length=200, description="Notas sobre el pago")
    payment_photo: Optional[str] = Field(None, description="Foto del pago en base64")


class ParticipantResponse(BaseModel):
    """Participante en una apuesta"""
    id: int
    user_id: int
    user: UserResponse
    chosen_option: Optional[str]
    joined_at: datetime
    
    class Config:
        from_attributes = True


class BetResponse(BaseModel):
    """Apuesta para enviar al frontend"""
    id: int
    title: str
    description: Optional[str]
    options: Optional[List[str]]
    creator_id: int
    creator: UserResponse
    status: str
    created_at: datetime
    closed_at: Optional[datetime]
    completed_at: Optional[datetime]
    winning_option: Optional[str]
    notes: Optional[str]
    tortillas_count: int = 1
    payment_photo: Optional[str] = None
    participants: List[ParticipantResponse] = []
    
    class Config:
        from_attributes = True


# ═══════════════════════════════════════════════════════════════
# AUTENTICACIÓN
# ═══════════════════════════════════════════════════════════════

class Token(BaseModel):
    """Token JWT después de login"""
    access_token: str
    token_type: str
    user: UserResponse


class TokenData(BaseModel):
    """Datos decodificados del token"""
    username: Optional[str] = None


# ═══════════════════════════════════════════════════════════════
# ESTADÍSTICAS
# ═══════════════════════════════════════════════════════════════

class RankingItem(BaseModel):
    """Item para ranking"""
    user_id: int
    username: str
    display_name: str
    wins: int
    total_participations: int
    win_rate: float


class StatsResponse(BaseModel):
    """Estadísticas de usuario"""
    user_id: int
    username: str
    wins: int
    total_bets_created: int
    total_participations: int
    ranking_position: Optional[int]

class GlobalStatsResponse(BaseModel):
    """Estadísticas globales de la aplicación"""
    total_bets: int
    active_bets: int
    completed_bets: int
    paid_bets: int
    total_tortillas_owed: int
    total_tortillas_paid: int
    top_winner: Optional[dict]  # {"username": str, "display_name": str, "wins": int}
    total_users: int

class HallOfFameResponse(BaseModel):
    """Hall of Fame/Shame con estadísticas divertidas"""
    king_of_tortillas: Optional[dict]  # Rey: más victorias
    worst_payer: Optional[dict]  # Peor pagador: más deudas pendientes
    compulsive_better: Optional[dict]  # Apostador compulsivo: más apuestas creadas
    generous_one: Optional[dict]  # El generoso: más tortillas pagadas
    winning_streak: Optional[dict]  # Racha ganadora actual
    losing_streak: Optional[dict]  # Racha perdedora actual
