"""
🗄️ Modelos de Base de Datos para TortillApuestas
Define la estructura de las tablas en PostgreSQL
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    """Tabla de Usuarios"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    display_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)  # Número de teléfono (opcional)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relaciones
    bets_created = relationship("Bet", back_populates="creator", foreign_keys="Bet.creator_id")
    participants = relationship("BetParticipant", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.username}>"


# Modelo Participant eliminado - las opciones ahora son texto libre en Bet.options


class Bet(Base):
    """Tabla de Apuestas"""
    __tablename__ = "bets"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True)
    options = Column(JSON, nullable=True)  # Lista de opciones: ["Madrid", "Barcelona", "Empate"]
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), default="open")  # open, closed, completed, paid
    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    paid_at = Column(DateTime, nullable=True)  # Fecha en que se pagó la apuesta
    winning_option = Column(String(200), nullable=True)  # Opción ganadora (texto)
    notes = Column(String(500), nullable=True)  # Resultado de la apuesta
    tortillas_count = Column(Integer, default=1)  # Número de tortillas a pagar
    payment_photo = Column(String, nullable=True)  # Foto del pago (base64)
    
    # Relaciones
    creator = relationship("User", back_populates="bets_created", foreign_keys=[creator_id])
    participants = relationship("BetParticipant", back_populates="bet", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Bet {self.title}>"


class BetParticipant(Base):
    """Tabla de Participantes en Apuestas"""
    __tablename__ = "bet_participants"
    
    id = Column(Integer, primary_key=True, index=True)
    bet_id = Column(Integer, ForeignKey("bets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Solo usuarios registrados
    chosen_option = Column(String(200), nullable=True)  # Opción elegida (texto)
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    bet = relationship("Bet", back_populates="participants")
    user = relationship("User", back_populates="participants")
    
    def __repr__(self):
        return f"<BetParticipant bet_id={self.bet_id} user_id={self.user_id} option={self.chosen_option}>"
