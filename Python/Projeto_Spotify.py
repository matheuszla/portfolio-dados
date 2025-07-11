import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ========== CONFIGURAÇÕES DO USUÁRIO ==========
# Obtenha suas credenciais em: https://developer.spotify.com/dashboard/
CLIENT_ID = "SEU_CLIENT_ID"
CLIENT_SECRET = "SEU_CLIENT_SECRET"
REDIRECT_URI = "URL_APP"  # Ex: http://127.0.0.1:8888/callback

# Lista de artistas desejados. Substitua pelos de sua preferência
ARTISTAS = [
    "Artista1", "Artista2", "Artista3", "Benito di Paula",
    "Altemar Dutra", "Manolo Otero", "Wando", "José Augusto",
    "Ângela Maria", "Agnaldo Rayol", "Luis Miguel"
]

NOME_DA_PLAYLIST = "Sua Playlist Personalizada"
# ==============================================

# Remove cache antigo para forçar nova autorização
if os.path.exists(".cache"):
    os.remove(".cache")

# Autenticação via OAuth com permissões para modificar playlists públicas
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="playlist-modify-public"
))

# Recupera o ID do usuário autenticado
user_id = sp.current_user()["id"]

# Cria a nova playlist
nova_playlist = sp.user_playlist_create(user=user_id, name=NOME_DA_PLAYLIST, public=True)
playlist_id = nova_playlist["id"]
print(f"✅ Playlist criada: {NOME_DA_PLAYLIST}")

musicas_adicionadas = set()

# Para cada artista, adiciona até 15 faixas populares
for artista in ARTISTAS:
    try:
        resultado_busca = sp.search(q=artista,_
