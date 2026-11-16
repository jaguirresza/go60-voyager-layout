import json, sys
src, dst = sys.argv[1], sys.argv[2]
d = json.load(open(src))

def kp(k):
    # "LG(LEFT)" -> nested params
    if "(" in k:
        mod, inner = k.split("(", 1)
        return {"value": mod, "params": [kp(inner[:-1])]}
    return {"value": k}
def K(k): return {"value": "&kp", "params": [kp(k)]}
def LT(layer, k): return {"value": "&lt", "params": [{"value": layer}, kp(k)]}
def MKP(b): return {"value": "&mkp", "params": [{"value": b}]}
T = {"value": "&trans"}
MAGIC = {"value": "&magic"}
# Shift: tap/hold = Shift, double-tap = Caps Word (defined below).
# The Layout Editor only accepts custom behaviors wrapped in a "Custom" key.
def CUSTOM(name): return {"value": "Custom", "params": [{"value": name}]}
LSHIFT_CW = CUSTOM("&td_lshft_cw")
RSHIFT_CW = CUSTOM("&td_rshft_cw")

def keys(row): return [T if k == "_T" else K(k) for k in row]

LOWER, RAISE, MAGIC_L, FACTORY, MOUSE = 1, 2, 3, 4, 5

# Index order: R1..R4 = 12 each (left to right), then
# 48-50 LH bottom row (under W E R), 51-53 RH bottom row (under U I O),
# 54-56 LH thumbs (outer -> inner), 57-59 RH thumbs (inner -> outer).
base = (
    [MAGIC] + keys("N1 N2 N3 N4 N5 N6 N7 N8 N9 N0 BSPC".split()) +
    keys("GRAVE Q W E R T Y U I O P BSLH".split()) +
    keys("TAB A S D F G H J K L SEMI SQT".split()) +
    [LSHIFT_CW] + keys("Z X C V B N M COMMA DOT FSLH".split()) + [RSHIFT_CW] +
    keys("TAB LCTRL LALT".split()) +
    keys("RALT RCTRL DEL".split()) +
    [K("LGUI"), LT(RAISE, "SPACE"), LT(LOWER, "BSPC"),
     LT(LOWER, "ESC"), LT(RAISE, "RET"), K("RGUI")]
)
lower = (
    keys("F1 F2 F3 F4 F5 F6 F7 F8 F9 F10 F11 F12".split()) +
    keys("ESC N1 N2 N3 N4 N5 N6 N7 N8 N9 N0 BSPC".split()) +
    keys("_T EXCL AT HASH DLLR PRCNT CARET AMPS STAR LPAR RPAR RET".split()) +
    keys("_T UNDER MINUS PLUS EQUAL _T _T LBRC RBRC LBKT RBKT _T".split()) +
    [T] * 12
)
raise_ = (
    [T] * 12 +
    # Opt+arrows above the arrows (move by word / paragraph)
    keys("ESC _T _T _T _T _T LA(LEFT) LA(DOWN) LA(UP) LA(RIGHT) _T BSPC".split()) +
    keys("_T _T _T _T _T _T LEFT DOWN UP RIGHT _T RET".split()) +
    # Undo / cut / copy / paste under Z X C V; Cmd+arrows under the arrows
    keys("_T LG(Z) LG(X) LG(C) LG(V) _T LG(LEFT) LG(DOWN) LG(UP) LG(RIGHT) _T _T".split()) +
    [T] * 12
)
# Mouse layer: turns on by itself while the right trackpad is in use.
# J K L = left / middle / right click; , = Mission Control; . = Spotlight.
mouse = (
    [T] * 12 +
    [T] * 12 +
    [T] * 7 + [MKP("LCLK"), MKP("MCLK"), MKP("RCLK")] + [T] * 2 +
    [T] * 8 + keys("LC(UP) LG(SPACE)".split()) + [T] * 2 +
    [T] * 12
)
for L in (base, lower, raise_, mouse): assert len(L) == 60, len(L)

d["layers"][0], d["layers"][1], d["layers"][2] = base, lower, raise_
d["layers"] = d["layers"][:5] + [mouse]

# Magic is held on the top-left key, so move "Clear Bluetooth" from there
# to the Z key, next to the Bluetooth profile keys (on X C V B).
magic_layer = d["layers"][MAGIC_L]
assert magic_layer[0] == {"value": "&bt", "params": [{"value": "BT_CLR"}]}
magic_layer[37] = magic_layer[0]
magic_layer[0] = {"value": "&none"}
d["layer_names"] = ["Base", "Lower", "Raise", "Magic", "Factory", "Mouse"]

d["custom_defined_behaviors"] = """behaviors {
    td_lshft_cw: td_lshft_cw {
        compatible = "zmk,behavior-tap-dance";
        #binding-cells = <0>;
        tapping-term-ms = <200>;
        bindings = <&kp LSHFT>, <&caps_word>;
    };
    td_rshft_cw: td_rshft_cw {
        compatible = "zmk,behavior-tap-dance";
        #binding-cells = <0>;
        tapping-term-ms = <200>;
        bindings = <&kp RSHFT>, <&caps_word>;
    };
};"""

# Right trackpad: turn on the Mouse layer while moving, off 500 ms after.
rh = next(l for l in d["inputListeners"] if l["code"] == "&cirque_rh_listener")
rh["inputProcessors"] = [p for p in rh["inputProcessors"] if p["code"] != "&zip_temp_layer"]
rh["inputProcessors"].append({"code": "&zip_temp_layer", "params": [MOUSE, 500]})

d["title"] = "Voyager-Aligned Layout (macOS)"
d["tags"] = ["qwerty", "mac", "voyager"]
d["notes"] = (
    "Go60 layout aligned with my ZSA Voyager layout (Oryx R7Y9a).\n\n"
    "- Base: Voyager alpha block on rows 2-4 (` / Tab / Shift on the left edge, \\ / ' / Shift on the right). "
    "Number row = Magic 1-0 Backspace. Bottom row: Tab Ctrl Opt | Opt Ctrl Delete.\n"
    "- Shift: double-tap either Shift for Caps Word.\n"
    "- Thumbs (tap / hold): left Space/Raise, Backspace/Lower; right Esc/Lower, Enter/Raise. "
    "Outer thumb key on each side (next to the bottom row) is Cmd.\n"
    "- Lower (1): numbers and symbols, F1-F12 on the top row.\n"
    "- Raise (2): arrows on the HJKL row, Opt+arrows above, Cmd+arrows below; "
    "undo / cut / copy / paste under Z X C V.\n"
    "- Mouse (5): turns on automatically while the right trackpad moves (off after 500 ms). "
    "J K L = left / middle / right click, comma = Mission Control, period = Spotlight.\n"
    "- Magic (3) and Factory (4): unchanged from the Go60 factory layout."
)
json.dump(d, open(dst, "w"), indent=2)
print("written", dst)
