from pathlib import Path
import time

from gameboy_automation.emulators import Button
from gameboy_automation.runtime.session import Session


PC_TEMPLATE_DIRECTORY = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "templates"
    / "screens"
    / "pc"
)

DEPOSIT_PARTY_TEMPLATE_PATH = (
    PC_TEMPLATE_DIRECTORY
    / "deposit_party.png"
)

ACTION_MENU_TEMPLATE_DIRECTORY = (
    PC_TEMPLATE_DIRECTORY
    / "action_menu"
)

ACTION_MENU_TEMPLATE_PATHS = (
    ACTION_MENU_TEMPLATE_DIRECTORY / "store.png",
    ACTION_MENU_TEMPLATE_DIRECTORY / "summary.png",
    ACTION_MENU_TEMPLATE_DIRECTORY / "mark.png",
    ACTION_MENU_TEMPLATE_DIRECTORY / "release.png",
    ACTION_MENU_TEMPLATE_DIRECTORY / "cancel.png",
)

BOX_SELECTION_TEMPLATE_PATH = (
    PC_TEMPLATE_DIRECTORY
    / "box_selection.png"
)

BOX_FULL_TEMPLATE_PATH = (
    PC_TEMPLATE_DIRECTORY
    / "box_full.png"
)

class PCScreen:
    """Represents Pokémon Ultra Violet PC storage screens."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def is_deposit_party_visible(
        self,
    ) -> bool:
        """Return True when the Deposit Pokémon party screen is visible."""
        screen = self.session.screenshot()

        match = screen.find_template(
            template_path=DEPOSIT_PARTY_TEMPLATE_PATH,
        )

        return match.found

    def is_action_menu_visible(
        self,
    ) -> bool:
        """Return True when the Pokémon action menu is visible."""
        screen = self.session.screenshot()

        for template_path in ACTION_MENU_TEMPLATE_PATHS:
            match = screen.find_template(
                template_path=template_path,
            )

            if not match.found:
                return False

        return True

    def open_deposit_party(
        self,
    ) -> None:
        """Open the Deposit Pokémon screen from directly in front of the PC."""
        print("Opening PC...")

        self.session.press(
            Button.A,
            duration_seconds=0.2,
        )

        time.sleep(1.0)

        print("Advancing PC startup dialogue...")

        self.session.press(
            Button.A,
            duration_seconds=0.2,
        )

        time.sleep(1.0)

        print("Selecting BILL'S PC...")

        # BILL'S PC is already selected.
        self.session.press(
            Button.A,
            duration_seconds=0.2,
        )

        time.sleep(1.0)

        print("Advancing BILL'S PC dialogue...")

        self.session.press(
            Button.A,
            duration_seconds=0.2,
        )

        time.sleep(1.0)

        print("Opening Pokémon Storage System...")

        self.session.press(
            Button.A,
            duration_seconds=0.2,
        )

        time.sleep(1.0)

        print("Selecting DEPOSIT POKéMON...")

        # WITHDRAW POKéMON starts selected.
        self.session.press(
            Button.DOWN,
            duration_seconds=0.2,
        )

        time.sleep(0.5)

        self.session.press(
            Button.A,
            duration_seconds=0.2,
        )

        time.sleep(2.0)

        if not self.is_deposit_party_visible():
            raise RuntimeError(
                "PC Deposit Pokémon screen did not open."
            )

        print("PC Deposit Pokémon screen opened successfully!")

    def move_to_bottom_full_party_slot(
        self,
    ) -> None:
        """Move from SLOT_1 to SLOT_6 for a full six-Pokémon party."""
        print("Moving PC cursor from SLOT_1 to SLOT_6...")

        for slot_number in range(2, 7):
            print(
                f"Moving to SLOT_{slot_number}..."
            )

            self.session.press(
                Button.DOWN,
                duration_seconds=0.2,
            )

            time.sleep(0.4)

        print("PC cursor should now be on SLOT_6.")

    def is_box_selection_visible(
        self,
    ) -> bool:
        """Return True when the deposit box-selection screen is visible."""
        screen = self.session.screenshot()

        match = screen.find_template(
            template_path=BOX_SELECTION_TEMPLATE_PATH,
        )

        return match.found

    def is_selected_box_full(
        self,
    ) -> bool:
        """Return True when the currently selected PC box is full."""
        screen = self.session.screenshot()

        match = screen.find_template(
            template_path=BOX_FULL_TEMPLATE_PATH,
        )

        return match.found

    def find_box_with_space(
        self,
        max_boxes: int = 14,
    ) -> None:
        """Move to the first PC box that has space for a Pokémon."""
        print("Searching for a PC box with space...")

        for box_number in range(1, max_boxes + 1):
            full = self.is_selected_box_full()

            print(
                f"Box {box_number}: "
                f"full={full}"
            )

            if not full:
                print(
                    f"Found available space in box {box_number}."
                )
                return

            if box_number < max_boxes:
                print("Moving RIGHT to next box...")

                self.session.press(
                    Button.RIGHT,
                    duration_seconds=0.2,
                )

                time.sleep(0.5)

        raise RuntimeError(
            f"Could not find PC box with space "
            f"after checking {max_boxes} boxes."
        )

    def deposit_all_except_first(
        self,
    ) -> None:
        """Deposit SLOT_6 through SLOT_2, leaving SLOT_1 in the party."""
        print("Depositing all Pokémon except SLOT_1...")

        self.move_to_bottom_full_party_slot()

        for slot_number in range(6, 1, -1):
            print()
            print(
                f"Depositing SLOT_{slot_number}..."
            )

            print(
                f"Opening action menu for SLOT_{slot_number}..."
            )

            self.session.press(
                Button.A,
                duration_seconds=0.2,
            )

            time.sleep(1.0)

            if not self.is_action_menu_visible():
                raise RuntimeError(
                    f"Could not open action menu for SLOT_{slot_number}."
                )

            print("Selecting STORE...")

            # STORE is selected when the action menu opens.
            self.session.press(
                Button.A,
                duration_seconds=0.2,
            )

            time.sleep(1.0)

            if not self.is_box_selection_visible():
                raise RuntimeError(
                    f"Box selection screen did not open "
                    f"for SLOT_{slot_number}."
                )

            self.find_box_with_space()

            print(
                f"Depositing SLOT_{slot_number} into PC box..."
            )

            self.session.press(
                Button.A,
                duration_seconds=0.2,
            )

            time.sleep(2.0)

            if not self.is_deposit_party_visible():
                raise RuntimeError(
                    f"Did not return to Deposit Pokémon screen "
                    f"after depositing SLOT_{slot_number}."
                )

            print(
                f"SLOT_{slot_number} deposited successfully."
            )

            if slot_number > 2:
                print(
                    f"Moving UP from empty SLOT_{slot_number} "
                    f"to SLOT_{slot_number - 1}..."
                )

                self.session.press(
                    Button.UP,
                    duration_seconds=0.2,
                )

                time.sleep(0.5)

        print()
        print(
            "Finished depositing SLOT_6 through SLOT_2. "
            "SLOT_1 remains in the party."
        )

    def exit_to_overworld(
    self,
    ) -> None:
        """Exit the PC menus and return to normal player control."""
        for _ in range(8):
            self.session.press(
                Button.B,
                duration_seconds=0.2,
            )

            time.sleep(0.5)

        print("Exited PC menus and returned to overworld.")