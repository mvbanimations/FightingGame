# Main game workflow

As of October 31, 2026, the Martin-based browser game in template/ is the main working game again. Ikemen GO remains a separate preserved experiment.

## Play and edit

- Launch Play.cmd to play at http://127.0.0.1:4175/game/.
- Launch Template Studio.cmd to edit at http://127.0.0.1:4175/.
- Both use template-server.cjs. If that server is already running, use the URLs directly.

## Artwork pipeline

1. Prepare and approve character designs, individual poses and backgrounds in the active Fighter Asset Studio.
2. Use its existing Game template slot mappings and Export Game Template ZIP. Keep the template's required dimensions, filenames and feet anchors.
3. In Template Studio, import the ZIP and refresh the game. Review movement, attack artwork, alignment and transitions against the existing gameplay.
4. Improve one animation or move at a time. Video-to-frame extraction and animation principles from the video remain useful where the browser game's renderer supports the resulting frames; they do not require switching engines.

See TEMPLATE-GUIDE.md for existing export/import behavior. Existing template artwork and customization settings are retained. The earlier sketch served by serve.cjs on port 4173 is not the main playable template.

## Preserved experiment

runtime/ikemen, reference/Ikemen-GO, tools/export-ikemen.py, Play Ikemen.cmd and Play Character Test.cmd remain available. The first Ikemen character had a working jab but static animation placeholders and is not the current production direction.

The GitHub repository mvbanimations/FightingGame remains an Ikemen source fork with our workflow notes and experimental tools. This change of direction does not upload or replace the local Martin game or its artwork in that repository.

