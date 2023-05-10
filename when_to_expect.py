#!/usr/bin/env python3
"""This module contains a 'WhenToExpect' plugin that calculates the expected number of
trials before an event occurs given a probability and confidence level. It is designed
to work with Flow Launcher, which is a productivity tool for Windows."""
import math
import os
import re
import sys
from typing import List

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, "lib"))
sys.path.append(os.path.join(parent_folder_path, "plugin"))

from flowlauncher import FlowLauncher


class WhenToExpect(FlowLauncher):
    """A class for calculating the expected number of trials before an event occurs
    given a probability (or odds) and confidence level.

    The expected number of trials is calculated using the formula: $log(1 - c) / log(1 -
    p)$, where $p$ is the probability of the event occurring and $c$ is the desired
    confidence level. If $c$ is not specified, it defaults to 0.5.

    This class is designed to work with Flow Launcher, which is a productivity tool for
    Windows."""

    def fraction_to_float(self, fraction: str) -> float:
        """Converts a fraction like 1/20 to a float (i.e. 0.05).

        Parameters
        ----------
        fraction : str
            Fraction as a string

        Returns
        -------
        float
            Floating point representation of the fraction
        """
        try:
            return float(fraction)
        except ValueError:
            matches = re.match(r"(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)", fraction)
            if matches and all(matches.groups()):
                try:
                    return float(matches.group(1)) / float(matches.group(2))
                except ValueError:
                    pass
            else:
                # Calculate odds instead of probability
                # https://www.statisticshowto.com/chance-vs-probability-vs-odds/
                matches = re.match(r"(\d+(?:\.\d+)?):(\d+(?:\.\d+)?)", fraction)
                if matches and all(matches.groups()):
                    try:
                        return float(matches.group(1)) / (
                            float(matches.group(1)) + float(matches.group(2))
                        )
                    except ValueError:
                        pass
        return 0.0

    def query(self, query: str) -> List[dict]:
        """Returns the expected number of trials before an event occurs given a
        probability and confidence level.

        The query should be in the form `p [c]`, where `p` is the probability (or odds)
        of the event occurring and `c` is the desired confidence level (expressed as a
        fraction; defaults to 0.5 if not specified). For example, `1/6 0.95` would
        calculate the expected number of dice rolls needed to get a specific number at
        least once with 95 % confidence.

        `p` can be given as probability (`0.n`/`n/m`) or odds (`n:m`).

        Parameters
        ----------
        query: str
            Query string from the user

        Returns
        -------
        List[dict]
            A list containing a single dictionary with keys "Title" and "IcoPath",
            representing the title of the result item and the icon path respectively.
        """
        query_parts = query.strip().split()
        result = {
            "Title": "Enter a probability (n/m) or odds (n:m) and optionally how sure "
            "you want to be that it occurs (default: 0.5)!",
            "IcoPath": "icon/expect.png",
        }
        if len(query_parts) in (1, 2):
            probability = self.fraction_to_float(query_parts[0])
            confidence_level = (
                self.fraction_to_float(query_parts[1]) if len(query_parts) >= 2 else 0.5
            )

            try:
                expected_trials_precise = round(
                    math.log(1 - confidence_level, 1 - probability), 2
                )
                expected_trials = math.ceil(expected_trials_precise)

                # Output formatting
                expected_trials_output = (
                    str(expected_trials_precise).rstrip("0.")
                    if str(expected_trials_precise) != "0"
                    else "0"
                )
                tries = "tries" if expected_trials_precise != 1 else "try"
                expected_trials_output = (
                    f" ({expected_trials_output})"
                    if expected_trials_output not in (str(expected_trials), "-")
                    else ""
                )

                result["Title"] = (
                    f"Event is expected with a probability of {round(confidence_level * 100, 2)} % "
                    f"after {expected_trials}{expected_trials_output} {tries}."
                )
            except (ValueError, ZeroDivisionError):
                result["Title"] = "Invalid input(s)!"
        elif len(query_parts):
            result["Title"] = "Too many inputs!"
        return [result]


if __name__ == "__main__":
    WhenToExpect()
