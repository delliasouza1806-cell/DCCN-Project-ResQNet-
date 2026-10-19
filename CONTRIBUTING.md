# Working rules for ResQNet

## The one rule for Packet Tracer files

`.pkt` files cannot be merged, so only one person edits the network at a time.

- Name files `resqnet_v1.pkt`, `resqnet_v2.pkt`, and so on.
- **Never overwrite a working version.** Open the latest, then File > Save As with the next number.
- Save a new version at the end of every numbered step in Phase 2, and after every phase.
- Say who holds the file ("I have v4") in the team chat before editing.
- Log each version in `pkt/README.md` and the hand-offs in `docs/TEAM.md`.

## Saving router configs

After every phase, on each device:

```
copy running-config startup-config
show running-config
```

Copy the output into `configs/<phase>/<device>.txt`, for example `configs/phase2/R-H1.txt`.

## Test evidence

Every test goes in the test matrix with Pass or Fail and a screenshot. Name screenshots
`captures/<phase>-<test>-<nn>.png`, for example `captures/p3-nurse-ping-admin-01.png`.

## Backups

Copy the whole `resqnet` folder to a second place (pen drive or cloud drive) at the end of
every work session.
