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
    return inquirer.prompt(
        [
            inquirer.Checkbox(
                "playlists",
                message="What are you interested in?",
                choices=[(p.title, p) for p in plex.playlists()],
            ),
        ]
    )["playlists"]


def get_tracks_from_playlist(playlists):
    for playlist in playlists:
        for track in playlist.items():
            yield track
