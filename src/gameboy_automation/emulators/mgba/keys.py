from gameboy_automation.emulators import Button


#
# Windows Virtual-Key Codes
#
# https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
#

VK_SHIFT = 0x10
VK_TAB = 0x09
VK_F1 = 0x70

BUTTON_TO_VIRTUAL_KEY = {
    Button.A: ord("X"),
    Button.B: ord("Z"),

    Button.L: ord("A"),
    Button.R: ord("S"),

    Button.START: 0x0D,      # VK_RETURN
    Button.SELECT: 0x08,     # VK_BACK

    Button.UP: 0x26,         # VK_UP
    Button.DOWN: 0x28,       # VK_DOWN
    Button.LEFT: 0x25,       # VK_LEFT
    Button.RIGHT: 0x27,      # VK_RIGHT
}