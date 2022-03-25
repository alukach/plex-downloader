from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm
from plexapi.utils import cleanFilename


def download_tracks(*, tracks, out_dir: Path):
    with ThreadPoolExecutor() as executor:
        futures = {}

        for track in tracks:
            name = track._prettyfilename()
            ext = next(track.iterParts()).container

            if not ext:
                print(f"skipping {name}, no extension")
                continue

            if ext.lower() != "mp3":
                print(f"skipping {name}, bad extension: {ext}")
                continue

            artist = name.split(" - ")[0]
            artist_dir = out_dir / artist
            filepath = artist_dir / cleanFilename(f"{name}.{ext}")
            if filepath.exists():
                print(f"skipping {name}, already exists: {filepath}")
                continue
            artist_dir.mkdir(parents=True, exist_ok=True)

            futures[
                executor.submit(track.download, artist_dir)
            ] = track._prettyfilename()

        with tqdm(total=len(futures)) as pbar:
            for future in as_completed(futures):
                tqdm.write(futures[future])
                pbar.update(1)
