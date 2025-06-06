import streamlit as st
from sqlalchemy.orm import sessionmaker
from clases import Usuario, Publicacion, Reaccion
from db import get_session 


session = get_session()

st.title("Interfaz de Red Social con SQLAlchemy + Streamlit")

menu = st.sidebar.selectbox("Selecciona una vista", ["Usuarios", "Publicaciones", "Reacciones"])

if menu == "Usuarios":
    st.header("Lista de Usuarios")
    usuarios = session.query(Usuario).all()
    for usuario in usuarios:
        st.write(f"ID: {usuario.id} - {usuario.nombre}")
    
    usuario_id = st.selectbox("Selecciona un Usuario", [u.id for u in usuarios])
    usuario = session.query(Usuario).get(usuario_id)
    st.subheader(f" Publicaciones de {usuario.nombre}")
    
    data = []
    for pub in usuario.publicaciones:
        reaccion = next((r for r in pub.reacciones if r.usuario_id == usuario.id), None)
        emocion = reaccion.emocion if reaccion else "Sin reacción"
        data.append([pub.id, pub.contenido[:30] + "...", emocion])
    
    st.table({"ID Publicación": [d[0] for d in data],
              "Contenido": [d[1] for d in data],
              "Reacción del Usuario": [d[2] for d in data]})



elif menu == "Publicaciones":
    st.header("Lista de Publicaciones")
    publicaciones = session.query(Publicacion).all()
    
    for pub in publicaciones:
        st.write(f"ID: {pub.id} - {pub.contenido[:10]}...")

    pub_id = st.selectbox("Selecciona una Publicación", [p.id for p in publicaciones])
    publicacion = session.query(Publicacion).get(pub_id)
    st.subheader(f"Usuarios que reaccionaron a la publicación #{publicacion.id}")

    data = []
    for reaccion in publicacion.reacciones:
        data.append([reaccion.usuario.id, reaccion.usuario.nombre])

    st.table({"ID Usuario": [d[0] for d in data],
              "Nombre Usuario": [d[1] for d in data]})



elif menu == "Reacciones":
    st.header("Lista de Reacciones")
    reacciones = session.query(Reaccion).all()

    for reaccion in reacciones:
        st.write(f"ID: {reaccion.id} - {reaccion.emocion}")

    reaccion_id = st.selectbox("Selecciona una Reacción", [r.id for r in reacciones])
    reaccion = session.query(Reaccion).get(reaccion_id)
    
    st.subheader(f"Usuarios que han utilizado la reacción '{reaccion.emocion}'")

    # Buscar todas las reacciones con esa emoción
    mismas_reacciones = session.query(Reaccion).filter_by(emocion=reaccion.emocion).all()
    data = []
    for r in mismas_reacciones:
        data.append([r.usuario.nombre, r.publicacion.contenido[:30] + "..."])

    st.table({"Usuario": [d[0] for d in data],
              "Publicación": [d[1] for d in data]})
