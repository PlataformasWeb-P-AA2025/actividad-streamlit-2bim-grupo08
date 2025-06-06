from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint

from config import cadena_base_datos 


engine = create_engine(cadena_base_datos)

Base = declarative_base()

class Reaccion(Base):
    __tablename__ = 'reaccion'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    publicacion_id = Column(Integer, ForeignKey('publicacion.id'))
    emocion = Column(String(50), nullable=False)

    usuario = relationship("Usuario", back_populates="reacciones")
    publicacion = relationship("Publicacion", back_populates="reacciones")


    __table_args__ = (UniqueConstraint('usuario_id', 'publicacion_id', name='uix_usuario_publicacion'),)

    def __repr__(self):
        return f"Reaccion: usuario_id={self.usuario_id}, publicacion_id={self.publicacion_id}, emocion={self.emocion}"


class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)

    publicaciones = relationship("Publicacion", back_populates="usuario")
    reacciones = relationship("Reaccion", back_populates="usuario")

    def __repr__(self):
        return f"Usuario: nombre={self.nombre}"


class Publicacion(Base):
    __tablename__ = 'publicacion'
    id = Column(Integer, primary_key=True)
    contenido = Column(String(250), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))

    usuario = relationship("Usuario", back_populates="publicaciones")
    reacciones = relationship("Reaccion", back_populates="publicacion")

    def __repr__(self):
        return f"Publicacion: contenido={self.contenido[:30]}..."
        

Base.metadata.create_all(engine)
