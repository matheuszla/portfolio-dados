import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ========== CONFIGURAÇÕES DO USUÁRIO ==========
# Obtenha suas credenciais em: https://developer.spotify.com/dashboard/
CLIENT_ID = "SEU_CLIENT_ID"
CLIENT_SECRET = "SEU_CLIENT_SECRET"
REDIRECT_URI = "URL_APP"  

# Lista de artistas desejados. Substitua pelos de sua preferência
ARTISTAS = [
    "Artista1", "Artista2", "Artista3"
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
        resultado_busca = sp.search(q=artista, type="artist", limit=1)
        artistas_items = resultado_busca["artists"]["items"]

        if not artistas_items:
            print(f"❌ Artista não encontrado: {artista}")
            continue

        artista_id = artistas_items[0]["id"]

        # Pega as top 10 faixas
        top_tracks = sp.artist_top_tracks(artista_id, country='BR')["tracks"]
        track_ids = [track["id"] for track in top_tracks if track["id"] not in musicas_adicionadas]

        # Busca faixas de álbuns adicionais para chegar a 15 faixas por artista
        albums = sp.artist_albums(artista_id, album_type='album', limit=5)['items']
        for album in albums:
            faixas_album = sp.album_tracks(album['id'])['items']
            for faixa in faixas_album:
                if faixa['id'] not in musicas_adicionadas and len(track_ids) < 15:
                    track_ids.append(faixa['id'])

        if not track_ids:
            print(f"⚠️ Nenhuma faixa encontrada para: {artista}")
            continue

        # Adiciona as músicas na playlist
        sp.playlist_add_items(playlist_id, track_ids)
        musicas_adicionadas.update(track_ids)

        print(f"🎵 {len(track_ids)} músicas adicionadas de {artista}")

    except Exception as e:
        print(f"❌ Erro com {artista}: {e}")

print("\n🚀 Playlist finalizada com sucesso!")
