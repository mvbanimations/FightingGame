"""Package a reviewed pose set as a minimal Ikemen fighter. Requires Pillow.

Usage: python tools/export-ikemen.py --poses PATH --runtime PATH --name NAME
The input filenames are declared in POSES; legacy names are input adapters only.
"""
import argparse
import io
import json
from pathlib import Path
import re
import struct
from collections import deque
from PIL import Image

POSES = {
    'stance': 'martin-idle.webp', 'attack': 'martin-move-lp.webp',
    'walk': 'martin-walk-forward.webp', 'back': 'martin-walk-backward.webp',
    'crouch': 'martin-crouch.webp', 'jump': 'martin-jump-up.webp',
    'block': 'martin-block.webp', 'hit': 'martin-body-hit.webp',
    'down': 'martin-down.webp', 'win': 'martin-victory.webp',
}


def sff(sprites):
    """SFF 2.1 with PNG32 payloads, matching Ikemen's readHeaderV2/readV2."""
    header = bytearray(512)
    header[:12] = b'ElecbyteSpr\0'
    header[12:16] = bytes([0, 0, 1, 2])
    data_start = 512 + 28 * len(sprites)
    payload = bytearray()
    records = bytearray()
    for group, number, image, ax, fy in sprites:
        png = io.BytesIO()
        image.save(png, format='PNG')
        data = struct.pack('<I', image.width * image.height * 4) + png.getvalue()
        records += struct.pack('<HHHHhhHBBIIHH', group, number,
                               image.width, image.height, ax, fy,
                               0, 12, 32, len(payload), len(data), 0, 0)
        payload += data
    struct.pack_into('<IIIIIIII', header, 36,
                     512, len(sprites), data_start, 0,
                     data_start, len(payload), data_start + len(payload), 0)
    return bytes(header + records + payload)


def build(poses, runtime, name, pose_map=None):
    if not re.fullmatch(r'[a-z][a-z0-9_-]{0,39}', name):
        raise ValueError('Name must be a lowercase character folder identifier')
    out = runtime / 'chars' / name
    if out.exists() and not (out / 'asset-manifest.json').exists():
        raise ValueError('Refusing to replace an unrelated character folder')
    images = {}
    source_map = pose_map or {key: key + '.png' for key in POSES}
    if set(source_map) != set(POSES):
        raise ValueError('Pose map must provide: ' + ', '.join(POSES))
    for key, filename in source_map.items():
        source = (poses / filename).resolve()
        if not source.is_relative_to(poses.resolve()):
            raise ValueError('Pose images must stay inside the pose folder')
        image = Image.open(source).convert('RGBA')
        # Legacy preview exports contain an opaque black/magenta guide backdrop.
        # Flood from the border, retaining enclosed dark character details.
        pixels = image.load()
        pending = (deque([(x, y) for x in range(image.width) for y in (0, image.height-1)] +
                         [(x, y) for y in range(image.height) for x in (0, image.width-1)])
                   if image.getextrema()[3][0] == 255 else deque())
        visited = set()
        while pending:
            x, y = pending.popleft()
            if (x, y) in visited or not (0 <= x < image.width and 0 <= y < image.height):
                continue
            visited.add((x, y))
            r, g, b, a = pixels[x, y]
            if a == 0 or max(r, g, b) < 35 or (r > g * 1.35 and b > g * 1.35):
                pixels[x, y] = (0, 0, 0, 0)
                pending.extend(((x-1,y),(x+1,y),(x,y-1),(x,y+1)))
        # Preserve shared canvas geometry instead of independently rescaling poses.
        image = image.resize((120, 120), Image.Resampling.LANCZOS)
        images[key] = image
    out.mkdir(parents=True, exist_ok=True)
    sprites = [(i, 0, img, 60, 113) for i, img in enumerate(images.values())]
    portrait = images['stance'].copy()
    sprites += [(9000, 0, portrait.resize((25, 25)), 0, 0),
                (9000, 1, portrait.resize((120, 140)), 0, 0)]
    (out / f'{name}.sff').write_bytes(sff(sprites))
    ids = {key: i for i, key in enumerate(images)}
    # Cover the common movement/reaction action IDs from the bundled example.
    actions = sorted(set(map(int, re.findall(r'\[Begin Action\s+(\d+)\]',
                           (runtime / 'chars/kfm/kfm.air').read_text(), re.I))))
    air = []
    for action in actions:
        if action == 200:
            continue
        pose = ('hit' if 5000 <= action < 5100 else 'down' if 5100 <= action < 6000
                else 'block' if 120 <= action <= 155 else 'crouch' if action in (10, 11, 12)
                else 'walk' if action == 20 else 'back' if action == 21
                else 'jump' if 40 <= action <= 52 else 'win' if action in (180, 181)
                else 'stance')
        air += [f'[Begin Action {action}]', 'Clsn2Default: 1',
                'Clsn2[0] = -18,-108,18,0', f'{ids[pose]},0,0,0,6', '']
    air += ['[Begin Action 200]', 'Clsn2Default: 1', 'Clsn2[0] = -18,-108,18,0',
            f'{ids["stance"]},0,0,0,6', 'Clsn1: 1', 'Clsn1[0] = 18,-88,52,-60',
            f'{ids["attack"]},0,0,0,3', f'{ids["stance"]},0,0,0,15', '']
    (out / f'{name}.air').write_text('\n'.join(air))
    constants = (runtime / 'chars/kfm/kfm.cns').read_text(encoding='utf-8').split('[Statedef 170]')[0]
    constants = constants.replace('height = 60', 'height = 108')
    states = '''
[Statedef 200]
type = S
movetype = A
physics = S
anim = 200
ctrl = 0
velset = 0,0
[State 200, Contact]
type = HitDef
trigger1 = AnimElem = 2
attr = S, NA
damage = 45, 0
animtype = Light
guardflag = MA
hitflag = MAF
priority = 3, Hit
pausetime = 8,8
sparkno = 2
guard.sparkno = 40
sparkxy = -10,-80
hitsound = F0,0
guardsound = F6,0
ground.type = High
ground.slidetime = 10
ground.hittime = 14
ground.velocity = -3
air.velocity = -2,-3
[State 200, Recover]
type = ChangeState
trigger1 = AnimTime = 0
value = 0
ctrl = 1

[Statedef 170]
type = S
movetype = I
physics = S
anim = 170
ctrl = 0
[Statedef 180]
type = S
movetype = I
physics = S
anim = 180
ctrl = 0
[Statedef 190]
type = S
movetype = I
physics = S
anim = 0
[State 190, Ready]
type = ChangeState
trigger1 = Time = 1
value = 0
ctrl = 1
'''
    (out / f'{name}.cns').write_text(constants.split('[Quotes]')[0] + states, encoding='utf-8')
    commands = '''[Remap]
x=x
y=y
z=z
a=a
b=b
c=c
s=s
[Defaults]
command.time = 15
command.buffer.time = 1
[Command]
name = "jab"
command = x
time = 1
[Command]
name = "holdfwd"
command = /$F
time = 1
[Command]
name = "holdback"
command = /$B
time = 1
[Command]
name = "holdup"
command = /$U
time = 1
[Command]
name = "holddown"
command = /$D
time = 1
[Statedef -1]
[State -1, Jab]
type = ChangeState
value = 200
triggerall = StateType = S
triggerall = ctrl
trigger1 = command = "jab"
trigger2 = AILevel > 0
trigger2 = P2BodyDist X < 34
[Statedef -2]
[State -2, Approach for basic CPU test]
type = VelSet
triggerall = AILevel > 0
triggerall = RoundState = 2
triggerall = StateType = S
triggerall = ctrl
trigger1 = P2BodyDist X >= 34
x = 2
'''
    (out / f'{name}.cmd').write_text(commands)
    (out / f'{name}.def').write_text(f'''[Info]
name = "{name}"
displayname = "MVB Prototype"
author = "mvbanimations"
mugenversion = 1.1
localcoord = 320,240
[Files]
cmd = {name}.cmd
cns = {name}.cns
st = {name}.cns
stcommon = common1.cns
sprite = {name}.sff
anim = {name}.air
''')
    manifest = {'character': name, 'source': str(poses), 'poses': source_map,
                'attack': {'startup': 6, 'active': 3, 'recovery': 15, 'damage': 45},
                'limitations': ['Static movement/reaction placeholders',
                                'Single grounded jab on x', 'Basic approach-and-jab CPU only; no specials'],
                'constantsReference': 'Bundled Elecbyte Kung Fu Man example; retain its upstream licenses'}
    (out / 'asset-manifest.json').write_text(json.dumps(manifest, indent=2))
    print(out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--poses', type=Path, required=True)
    parser.add_argument('--runtime', type=Path, required=True)
    parser.add_argument('--name', default='mvb_prototype')
    parser.add_argument('--legacy-preview', action='store_true',
                        help='Import the archived jean-jacket preview filenames')
    parser.add_argument('--pose-map', type=Path, help='JSON mapping pose names to exported image filenames')
    args = parser.parse_args()
    mapping = json.loads(args.pose_map.read_text(encoding='utf-8')) if args.pose_map else (POSES if args.legacy_preview else None)
    build(args.poses, args.runtime, args.name, mapping)
