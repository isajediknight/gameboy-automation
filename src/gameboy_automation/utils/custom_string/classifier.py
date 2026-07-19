from __future__ import annotations

import datetime as dt
import os
import re
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ClassificationResult:
    valid_phone_number: bool = False
    is_file: bool = False
    is_directory: bool = False

    is_date: bool = False
    date: Optional[dt.datetime] = None

    location_city: str = ""
    location_state_territory: str = ""
    location_region: str = ""
    location_country: str = ""

    def as_dict(self) -> Dict[str, Any]:
        return {
            "VALID_PHONE_NUMBER": self.valid_phone_number,
            "IS_FILE": self.is_file,
            "IS_DIRECTORY": self.is_directory,
            "IS_DATE": self.is_date,
            "date": self.date,
            "location_city": self.location_city,
            "location_state_territory": self.location_state_territory,
            "location_region": self.location_region,
            "location_country": self.location_country,
        }


class ValueClassifier:
    """Keeps detection logic out of CustomString."""

    _PHONE_RE = re.compile(r"^(?:\+\d{1,3}[-\s]?)?\(?\d{3}\)?[-\s.]?\d{3}[-\s.]?\d{4}$")

    _COUNTRIES = ("United States", "India", "Canada", "Mexico")
    _COUNTRIES_LC = tuple(c.lower() for c in _COUNTRIES)

    _US_STATES = (
        "Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia",
        "Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts",
        "Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey",
        "New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island",
        "South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia",
        "Wisconsin","Wyoming",
    )
    _US_STATES_LC = tuple(s.lower() for s in _US_STATES)
    _US_ST_ABBR = (
        "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI",
        "MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT",
        "VT","VA","WA","WV","WI","WY"
    )

    @classmethod
    def classify(cls, value: str) -> ClassificationResult:
        res = ClassificationResult()
        if value is None:
            return res

        v = str(value)
        vs = v.strip()
        if not vs:
            return res

        # filesystem
        if os.path.isdir(v):
            res.is_directory = True
            return res
        if os.path.isfile(v):
            res.is_file = True
            return res

        # phone
        if cls._PHONE_RE.fullmatch(vs):
            res.valid_phone_number = True
            return res

        # country
        v_lc = vs.lower()
        if v_lc in cls._COUNTRIES_LC:
            idx = cls._COUNTRIES_LC.index(v_lc)
            res.location_country = cls._COUNTRIES[idx]
            return res

        # exact state name
        if v_lc in cls._US_STATES_LC:
            idx = cls._US_STATES_LC.index(v_lc)
            res.location_state_territory = cls._US_STATES[idx]
            res.location_country = "United States"
            return res

        # trailing state abbreviation
        m = re.search(r"(?i)\b([A-Z]{2})\s*$", vs)
        if m:
            abbr = m.group(1).upper()
            if abbr in cls._US_ST_ABBR:
                idx = cls._US_ST_ABBR.index(abbr)
                res.location_state_territory = cls._US_STATES[idx]
                res.location_country = "United States"
                city = re.sub(r"(?i)\b" + re.escape(abbr) + r"\s*$", "", vs).rstrip(", ").strip('" ').strip()
                res.location_city = city
                return res

        # date
        parsed = cls._try_parse_date(vs)
        if parsed is not None:
            res.is_date = True
            res.date = parsed
            return res

        return res

    @staticmethod
    def _try_parse_date(s: str) -> Optional[dt.datetime]:
        """Practical parser:
        - YYYY-MM-DD / YYYY/MM/DD / YYYY.MM.DD
        - MM/DD/YYYY (preferred) or DD/MM/YYYY if MM invalid
        """
        for sep in ("/", "-", "."):
            if sep not in s:
                continue
            parts = s.split(sep)
            if len(parts) != 3:
                return None

            a, b, c = [p.strip() for p in parts]
            if not (a.isdigit() and b.isdigit() and c.isdigit()):
                return None

            # YYYY-...
            if len(a) == 4:
                year, month, day = int(a), int(b), int(c)
            else:
                # ...-YYYY
                if len(c) != 4:
                    return None
                year = int(c)
                x, y = int(a), int(b)

                # prefer MM/DD/YYYY
                if 1 <= x <= 12 and 1 <= y <= 31:
                    month, day = x, y
                # fallback to DD/MM/YYYY
                elif 1 <= y <= 12 and 1 <= x <= 31:
                    day, month = x, y
                else:
                    return None

            try:
                return dt.datetime(year, month, day)
            except ValueError:
                return None

        return None
