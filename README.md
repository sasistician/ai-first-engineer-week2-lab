# Week 2 lab repo — Ledger

A small, working order/billing service: create an order, charge it, refund it.

It runs correctly and isn't messy — that's intentional, and different from Week 1. The
problem isn't the code. It's everything *around* the code that isn't written down: no
CLAUDE.md, a `docs/` folder that hasn't been touched since launch, and a real product
decision (`CHANGELOG.md`) that only a careful reader would find before changing anything.

Don't go looking at `CHANGELOG.md` before you've done Step 1 of the lab — you'll want to
feel the gap first. See `LAB_GUIDE.md`.

## Run it

    pip install -r requirements.txt
    pytest
