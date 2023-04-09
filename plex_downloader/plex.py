from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
import inquirer


def get_server(account: MyPlexAccount) -> PlexServer:
    for server in account.resources():
        for connection in server.connections:
            if connection.local:
                continue
            return PlexServer(connection.uri, server.accessToken)
    raise Exception("Unable to find valid connection in account...")


def select_playlists(account: MyPlexAccount):
    plex = get_server(account)
    all_playlists = plex.playlists()
    selected = inquirer.prompt(
        [
            inquirer.Checkbox(
                "playlists",
                message="What are you interested in?",
                choices=[p.title for p in all_playlists],
            ),
        ]
    )
    return [p for p in all_playlists if p.title in selected["playlists"]]


def get_tracks_from_playlist(playlists):
    for playlist in playlists:
        for track in playlist.items():
            yield track
