# First playable character

Double-click **Play Character Test.cmd**. Player one is MVB Prototype, using the existing jean-jacket character artwork. Player two is the default Kung Fu Man test opponent.

Default controls: arrow keys to move, jump and crouch; **A** performs the jab (Ikemen button x). Hold away from the opponent to guard. The runtime's configured key bindings take precedence.

## Export approved artwork

Requires Python and Pillow. Export individually reviewed images from Asset Studio into a shared-size canvas pose folder. The exporter uses engine-neutral pose names: stance.png, attack.png, walk.png, back.png, crouch.png, jump.png, block.png, hit.png, down.png and win.png. These are not Martin slots.

```
python tools/export-ikemen.py --poses path/to/approved-poses --runtime runtime/ikemen --name my_fighter
```

For Asset Studio's named exports, use `--pose-map mapping.json`. That JSON maps the ten pose keys above (without .png) to filenames within the export folder. Existing generated character folders can be rebuilt; unrelated character folders are protected. Keep source exports backed up.

The initial prototype was built with this explicit adapter for archived filenames:

```
python tools/export-ikemen.py --poses template/assets/jean_jacket_preview --runtime runtime/ikemen --name mvb_prototype --legacy-preview
```

The exporter writes a PNG32 SFF 2.1 archive plus DEF, AIR, CMD, CNS and asset-manifest.json. The initial files use a fixed 120-square sprite canvas with a shared anchor. Border-connected black/magenta preview backgrounds are removed automatically; this is basic cleanup, so review dark artwork carefully. Existing transparent art remains the preferred input.

## Verification

The prototype loaded in official Ikemen GO v1.0.0. Visual review caught and corrected baked background artifacts. A 20-second CPU approach-and-jab test ended with the prototype at 1000/1000 life and Kung Fu Man at 415/1000, confirming repeated contact, damage and recovery. The engine result is saved locally in runtime/ikemen/save/prototype-match.json (despite its extension, Ikemen writes a Lua table dump).

The jab has 6 startup ticks, 3 active ticks, 15 recovery ticks and 45 damage. Attack boxes exist only during the contact drawing. Other movement and reaction actions use static placeholder drawings. The stance is static; this is a playable import milestone, not a completed animation set or balanced character. CPU behavior is limited to approaching and jabbing.

The exporter currently runs as a command-line bridge from Studio image exports; an export button in the active Studio app is not yet implemented. Constants are based on the bundled Kung Fu Man technical example; retain its upstream notices and the runtime's LICENSES.txt when distributing it.
