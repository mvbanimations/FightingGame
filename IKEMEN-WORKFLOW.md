# FightingGame workflow

Ikemen GO is our active game engine, replacing the Martin browser-template setup. Fighter Asset Studio remains our artwork preparation and approval tool.

## Character pipeline

1. Approve original character identity and consistent reference views.
2. Plan anticipation, active contact, recovery and return to stance for each move before generating animation.
3. Generate or import motion footage or pose sequences. Preserve original footage and transparent animation masters.
4. Select useful frames, maintain fixed scale and feet anchors, and assign frame durations in engine ticks. Review silhouette, character consistency, background cleanup, foot sliding and loop transitions.
5. Package sprites as SFF, animations and hitboxes/hurtboxes as AIR, identity as DEF, commands as CMD, and combat behavior as CNS or supported engine scripts. Collision boxes and combat timing require deliberate design and gameplay testing.
6. Register characters in the playable runtime's data/select.def and test movement, attacks, guarding, reactions and transitions.

## Replacement of the Martin setup

Martin sprite slots, pose IDs, canvas dimensions and combat timings are archived reference, not requirements for new characters. Preserve earlier artwork for review and reuse where suitable.

The existing Game Template ZIP exporter targets the older browser game and is not Ikemen-compatible. A first command-line exporter is available in tools/export-ikemen.py. Export approved individual images and animation masters from Studio, then follow IKEMEN-CHARACTER-TEST.md. An in-app Studio export button remains pending. Copying PNGs into chars alone does not create a playable fighter.

Use our in-house tools for reference artwork, asset preparation, scripting and integration. The transcript's video-generation service is optional; no dependency on it is required by this workflow.

## Setup and current status

This fork contains Ikemen GO engine source. Follow BUILDING.md for source builds. Official playable releases are at https://github.com/ikemen-engine/Ikemen-GO/releases. Keep a playable runtime separate from engine source, and record the version used for testing.

Our local development workspace has the official v1.0.0 Windows runtime in runtime/ikemen, upstream source in reference/Ikemen-GO, and Play Ikemen.cmd. Runtime startup with default fighters has been verified. Those local tools and artwork are not automatically included in this fork. The MVB Prototype character now loads with custom stance artwork and a working jab; the combat test confirmed 585 damage in a 20-second round. The develop source checkout is not assumed to match the stable runtime binary.

## First milestone

The first character import milestone is verified locally: custom stance, jab contact, damage and recovery. See IKEMEN-CHARACTER-TEST.md. Full animation sequences, additional moves, balance and Studio UI integration remain future work. Preserve the bundled Kung Fu Man examples as technical references.

Retain upstream license notices. Engine source is MIT licensed; bundled artwork, sounds and screenpack content have separate licenses.
