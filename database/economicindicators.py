#!/usr/bin/env python
""" economicindicators.py
Economic indicators
"""

from ..sources import fred
from datetime import date

class EconomicIndicator(object):
    def __init__(self, name, column_name,frequency_hint=None):
        self.name = name
        self.column_name = name
        self.frequency = frequency_hint

    def update

    def _row_exists(self, session, fordate):
        """ Return true if a row exists for the specified date
        """
        return (session.query(EconomicIndicator).filter_by(Date=fordate).count() > 0)

    def _get_most_recent_row(self, session):
        last = (session.query(EconomicIndicator).order_by(EconomicIndicator.Date.desc())
                                    .first())
        return last

    def _new_data_available(self,  session):
        """ Check if column is up to date
        """
        available = False
        data = fred.get(self.column_name)
        newest_available = data['dates'][0]
        last = self._get_most_recent_row(session)

        # Here we check for the whole row's existance in case this is the first column we're updating
        if last is not None:
            newest_stored = last.Date
        else:
            newest_stored = date(1900,01,01)
        if newest_available > newest_stored:
            # The row doesn't exist yet
            available = True

        if available is False:
            # The row already exists, see if this column is populated
            if getattr(last, self.column_name) is None:
                available = True
        return available


