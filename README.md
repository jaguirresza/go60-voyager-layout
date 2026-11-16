# Go60 × Voyager layout

My [MoErgo Go60](https://www.moergo.com/) keyboard layout for macOS, built to match my [ZSA Voyager](https://www.zsa.io/voyager) layout ([Oryx `R7Y9a`](https://configure.zsa.io/voyager/layouts/R7Y9a/latest/0)) so I can switch between the two boards without relearning.

## Install on the keyboard

1. Open the [MoErgo Layout Editor](https://my.glove80.com/) and import `Voyager-Aligned Layout (macOS).json`.
2. Build the firmware and download the `.uf2` file.
3. Flash it to the Go60.

## Change the layout

The JSON is generated. Edit `remap.py`, then rebuild:

```bash
python3 remap.py "Factory Default Layout (macOS).json" "Voyager-Aligned Layout (macOS).json"
```

Then import and flash again.

## Layout

### Base

```
 Magic  1    2    3    4    5   |  6    7    8    9    0    Bksp
 `      Q    W    E    R    T   |  Y    U    I    O    P    \
 Tab    A    S    D    F    G   |  H    J    K    L    ;    '
 Shift  Z    X    C    V    B   |  N    M    ,    .    /    Shift

 Bottom row + thumbs:
 Tab  Ctrl  Opt  Cmd  Space  Bksp  |  Esc  Enter  Cmd  Opt  Ctrl  Delete
```

- **Thumbs (tap / hold):** Space / Raise, Backspace / Lower, Esc / Lower, Enter / Raise.
- **Shift:** double-tap for Caps Word, which types the next word in capitals.
- **Magic:** hold the top-left key for Bluetooth, lighting, bootloader and reset.

### Lower (hold Backspace or Esc)

```
 F1     F2   F3   F4   F5   F6  |  F7   F8   F9   F10  F11  F12
 Esc    1    2    3    4    5   |  6    7    8    9    0    Bksp
        !    @    #    $    %   |  ^    &    *    (    )    Enter
        _    -    +    =        |       {    }    [    ]
```

### Raise (hold Space or Enter)

```
 Esc                            |  ⌥←   ⌥↓   ⌥↑   ⌥→        Bksp
                                |  ←    ↓    ↑    →         Enter
        ⌘Z   ⌘X   ⌘C   ⌘V       |  ⌘←   ⌘↓   ⌘↑   ⌘→
```

### Mouse (turns on automatically while the right trackpad moves)

```
                                |       Left  Mid  Right
                                |             Mission  Spotlight
                                |             Control
```

J, K and L click. The layer turns off half a second after the trackpad stops.

## Files

| File | |
|---|---|
| `remap.py` | Builds the layout. Edit this. |
| `Voyager-Aligned Layout (macOS).json` | Generated layout to import into the Layout Editor. |
| `Factory Default Layout (macOS).json` | Go60 factory layout the script starts from. |
| `Oryx_ The ZSA Keyboard Configurator.pdf` | Print of the Voyager layout this matches. |
| `CLAUDE.md` | Notes for Claude Code: key numbering, editor quirks, history. |
