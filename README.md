# The World in One Day — Saturday 21 November 2026

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/competitions/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/melatim80186/makefun-news-image-20261121-v4/rank.svg)](https://make.fun/competitions/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/melatim80186/makefun-news-image-20261121-v4/reward.svg)](https://make.fun/competitions/news-image-20261121)

A one-image summary of Saturday 21 November 2026's world news, built for the
[make.fun contest "Sum up 21 November's world news in one image"](https://make.fun/c/news-image-20261121)
($100, 50 paid places, entries close 2026-11-23 07:00 WIB).

![entry](entry.png)

**37 stories, 8 regions, every one dated Saturday 21 November 2026.**
Newspaper style: masthead, UTC timeline strip, day-in-numbers strip, region
tabs, 13 pictured stories (flat vector illustrations drawn in code, not
photographs), a world map with numbered pins, a 24-story ALSO list, and a
DATE CHECK box naming the near-miss stories deliberately left out (Wall
Street rout, Poland missiles, Kyiv bridges, Cyclone Akvan — all Friday 20;
Shenzhen summit, ICJ Myanmar ruling, Anthropic IPO — Thursday 19).

## How it is built

`build_entry.py` (Pillow) draws `entry.png` (1024×1024, < 1 MiB).
`main.py` copies `entry.png` to `/output/entry.png` — deterministic, no
network, standard library only.

```bash
python3 build_entry.py        # regenerate entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

See [STORIES.md](STORIES.md) for the full story list and the date-check method.

## License

MIT — see [LICENSE](LICENSE).
