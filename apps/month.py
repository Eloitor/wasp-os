# SPDX-License-Identifier: MIT
# Copyright (C) 2023 Eloi Torrents
"""Month
~~~~~~~~~~~~

Simple calendar that displays months and highlights the current day.

Controls:
    - Swipe up to show next month.
    - Swipe down to show previous month.
    - Press the button to return to current month.
"""

import wasp
import icons
import fonts

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
MLENGTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def is_leap_year(year):
    return year % 400 == 0 or (year % 100 != 0 and year % 4 == 0)

def days_in_month(y, m):
    if m != 2:
        return MLENGTH[m - 1]
    if is_leap_year(int(y)):
        return 29
    return 28

class MonthApp():
    """Monthly calenadar application.
    """
    NAME = 'Month'
    ICON = icons.app

    def __init__(self):
        self._reset()

    def _reset(self):
        now = wasp.watch.rtc.get_localtime()
        self._year = now[0]
        self._month = now[1]
        self._today =  now[2]
        self._start = (now[2] - now[6]) % 7 - 7

    def foreground(self):
        wasp.system.bar.clock = True
        self._draw()

        wasp.system.request_event(wasp.EventMask.SWIPE_UPDOWN | wasp.EventMask.BUTTON)
        wasp.system.request_tick(15000)

    def swipe(self, event):
        if event[0] == wasp.EventType.UP:
            self._start = - ((-self._start + days_in_month(self._year, self._month)) % 7)
            self._month += 1
            if self._month == 12:
                self._month = 0
                self._year += 1
        elif event[0] == wasp.EventType.DOWN:
            self._start = (self._start  + days_in_month(self._year, (self._month - 1) % 12)) % 7 - 7
            self._month += -1
            if self._month == -1:
                self._month = 11
                self._year += -1
        self._draw()

    def press(self, button, state):
        if not state:
            return
        self._reset()
        self._draw()

    def tick(self, ticks):
        wasp.system.bar.update()

    def _draw(self, redraw=False):
        """Draw the display from scratch."""
        draw = wasp.watch.drawable
        hi = wasp.system.theme('bright')
        lo = draw.darken(wasp.system.theme('mid'), 2)
        wasp.system.bar.draw()
        draw.fill(y=40)

        if redraw:
            draw.reset()
        draw.set_font(fonts.sans24)
        draw.string(MONTHS[self._month - 1] + " " + str(self._year), 0, 50, width=240)

        # Gray
        draw.set_font(fonts.sans18)
        draw.set_color(lo)

        start = self._start - 1
        day = start 
        if day == -7:
            day = 0
        d_in_month = days_in_month(self._year, (self._month - 1) % 12) 
        d_prev_month = d_in_month
        for i in range(6*7):
            y_coord = 90 + 25 * (i//7)
            day += 1
            if day == 1:
                d_prev_month = 0
                d_in_month = days_in_month(self._year, self._month)
                draw.set_color(hi)
            if day == d_in_month + 1:
                draw.set_color(lo)
                day = 1
            day_str = str((day + d_prev_month - 1) % d_in_month +1)
            draw.string(day_str, 13 + 32*(i % 7),y_coord, width=20)
                       
        now = wasp.watch.rtc.get_localtime()
        if self._year == now[0] and self._month == now[1]:
            i = now[2] - self._start
            y_coord = 90 + 25 * (i//7)
            draw.set_color(hi, bg=0x64c8)
            draw.string(str(now[2]),13 + 32*(i % 7), y_coord, width=20)
            draw.set_color(0xFFFF)
