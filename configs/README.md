# configs/

Router and switch configs saved as text after every phase.

Layout: `configs/<phase>/<device>.txt`, for example `configs/phase2/R-H1.txt`.

Devices: R-CORE, R-CTRL, R-H1, R-H2, R-H3, R-AMB, SW-CTRL, SW-H1, SW-H2, SW-H3, SW-AMB.

Save steps on each device:

```
copy running-config startup-config
show running-config
```

Paste the output into the matching file. Do not hand-edit saved configs.
