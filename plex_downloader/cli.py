from pathlib import Path

import click
from plexapi.myplex import MyPlexAccount

from .download import download_tracks
from .plex import select_playlists, get_tracks_from_playlist


@click.command()
@click.option(
    "username",
    "-u",
    "--username",
    envvar="PLEX_USER",
    prompt="Plex username",
    show_default="Environment variable 'PLEX_USER' or prompt",
    help="Plex username",
)
@click.option(
    "password",
    "-pw",
    "--password",
    envvar="PLEX_PASS",
    prompt="Plex password",
    hide_input=True,
    show_default="Environment variable 'PLEX_PASS' or prompt",
    help="Plex password",
)
@click.option(
    "-o",
    "--out-dir",
    type=click.Path(file_okay=False, writable=True, resolve_path=True, path_type=Path),
    default="./",
)
def main(
    username: str,
    password: str,
    out_dir: Path,
):
    account = MyPlexAccount(username, password)
    playlists = select_playlists(account)
    tracks = get_tracks_from_playlist(playlists)
    return download_tracks(
        tracks=tracks,
        out_dir=out_dir,
    )
