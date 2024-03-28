# SPDX-License-Identifier: MIT
# Copyright (C) 2023 Eloi Torrents
"""TimeTo
~~~~~~~~~~~~

Personal Productivity Tool.

    .. figure:: res/screenshots/Puzzle15App.png
        :width: 179

        Screenshot of the 15 puzzle application
"""

import wasp
import widgets
import fonts
import os
import time
from micropython import const

_DIRECTORY = const('timeto')
_ACTIVITIES = const('timeto/activities.txt')
_CURRENT = const('timeto/current.txt')
_LOG = const('timeto/log.txt')

# 2-bit RLE, 96x64, generated from res/icons/puzzle_15_icon.png, 566 bytes
icon = (
    b'\x02'
    b'`@'
    b'\x10\xbf\x01 \xbf\x01 \xbf\x01 \x83@\xfaM\x82M'
    b'\x82M\x82M\x83 \x83M\x82M\x82M\x82M\x83 '
    b'\x83M\x82M\x82M\x82M\x83 \x83M\x82M\x82M'
    b'\x82M\x83 \x83M\x82M\x82M\x82M\x83 \x83M'
    b'\x82M\x82M\x82M\x83 \x83M\x82M\x82M\x82M'
    b'\x83 \x83M\x82M\x82M\x82M\x83 \x83M\x82M'
    b'\x82M\x82M\x83 \x83M\x82M\x82M\x82M\x83 '
    b'\x83M\x82M\x82M\x82M\x83 \x83M\x82M\x82M'
    b'\x82M\x83 \x83M\x82M\x82M\x82M\x83 \xbf\x01'
    b' \xbf\x01 \x83M\x82M\x82M\x82M\x83 \x83M'
    b'\x82M\x82M\x82M\x83 \x83M\x82M\x82M\x82M'
    b'\x83 \x83M\x82M\x82M\x82M\x83 \x83M\x82M'
    b'\x82M\x82M\x83 \x83M\x82M\x82M\x82M\x83 '
    b'\x83M\x82M\x82M\x82M\x83 \x83M\x82M\x82M'
    b'\x82M\x83 \x83M\x82M\x82M\x82M\x83 \x83M'
    b'\x82M\x82M\x82M\x83 \x83M\x82M\x82M\x82M'
    b'\x83 \x83M\x82M\x82M\x82M\x83 \x83M\x82M'
    b'\x82M\x82M\x83 \xbf\x01 \xbf\x01 \x83M\x82M'
    b'\x82M\x82M\x83 \x83M\x82M\x82M\x82M\x83 '
    b'\x83M\x82M\x82M\x82M\x83 \x83M\x82M\x82M'
    b'\x82M\x83 \x83M\x82M\x82M\x82M\x83 \x83M'
    b'\x82M\x82M\x82M\x83 \x83M\x82M\x82M\x82M'
    b'\x83 \x83M\x82M\x82M\x82M\x83 \x83M\x82M'
    b'\x82M\x82M\x83 \x83M\x82M\x82M\x82M\x83 '
    b'\x83M\x82M\x82M\x82M\x83 \x83M\x82M\x82M'
    b'\x82M\x83 \x83M\x82M\x82M\x82M\x83 \xbf\x01'
    b' \xbf\x01 \x83M\x82M\x82M\x82\x80\x81\x8d\xc0\xdb'
    b'\xc3 \xc3M\xc2M\xc2M\xc2\x8d\xc3 \xc3M\xc2M'
    b'\xc2M\xc2\x8d\xc3 \xc3M\xc2M\xc2M\xc2\x8d\xc3 '
    b'\xc3M\xc2M\xc2M\xc2\x8d\xc3 \xc3M\xc2M\xc2M'
    b'\xc2\x8d\xc3 \xc3M\xc2M\xc2M\xc2\x8d\xc3 \xc3M'
    b'\xc2M\xc2M\xc2\x8d\xc3 \xc3M\xc2M\xc2M\xc2\x8d'
    b'\xc3 \xc3M\xc2M\xc2M\xc2\x8d\xc3 \xc3M\xc2M'
    b'\xc2M\xc2\x8d\xc3 \xc3M\xc2M\xc2M\xc2\x8d\xc3 '
    b'\xc3M\xc2M\xc2M\xc2\x8d\xc3 \xff\x01 \xff\x01 '
    b'\xff\x01\x10'
)

class TimetoApp():
    """Personal Productivity Tools"""
    NAME = 'TimeTo'
    ICON = icon

    def __init__(self):
        """Initialize the application."""
        if not os.path.exists(_DIRECTORY):
            os.makedirs(_DIRECTORY)
        if not os.path.exists(_ACTIVITIES):
            # Create the file with the template
            with open(_ACTIVITIES, 'w') as f:
                current_time = int(time.time())
                template = f"""# ID\tNAME\tTIMER
{current_time}\tMeditation\t1200
{current_time + 1}\tWork\t2400
{current_time + 2}\tHobby\t3600
{current_time + 3}\tPersonal development\t1800
{current_time + 4}\tExercises / Health\t1200
{current_time + 5}\tWalk\t1800
{current_time + 6}\tGetting ready\t1800
{current_time + 7}\tSleep / Rest\t28800
{current_time + 8}\tOther\t3600"""
                f.write(template)
        self._page = 0
        self._scroll = wasp.widgets.ScrollIndicator(y=6)

    def foreground(self):
        self._activities = []
        with open('timeto/activities.txt') as f:
            for line in f:
                if line.startswith('#'):
                    continue
        
                data = line.strip().split('\t')
                if len(data) == 3:
                    id, name, timer = data
                    self._activities.append((id, name, timer))
                else:
                    print(f"Illegal line format: {line}")
        print(len(self._activities))

        wasp.system.request_event(wasp.EventMask.TOUCH |
                                  wasp.EventMask.SWIPE_UPDOWN)

        self._draw()

    def swipe(self, event):
        i = self._page
        n = self._num_pages
        if event[0] == wasp.EventType.UP:
            i += 1
            if i >= n:
                i -= 1
                wasp.watch.vibrator.pulse()
                return
        else:
            i -= 1
            if i < 0:
                wasp.system.switch(wasp.system.quick_ring[0])
                return

        self._page = i
        wasp.watch.display.mute(True)
        self._draw()
        wasp.watch.display.mute(False)

    def touch(self, event):
        page = self._get_page(self._page)
        x = event[1]
        y = event[2]
        activity = page[(y // 30) - 2]
        print(activity)

    @property
    def _num_pages(self):
        """Work out what the highest possible pages it."""
        num_apps = len(self._activities)
        return (num_apps + 5) // 6

    def _get_page(self, i):
        page = self._activities[6*i: 6*(i+1)]
        while len(page) < 6:
            page.append(None)
        return page

    def _draw(self):
        """Draw the display from scratch."""
        draw = wasp.watch.drawable
        draw.set_color(wasp.system.theme('bright'))
        draw.fill()

        page_num = self._page
        page = self._get_page(page_num)
        draw.set_color(wasp.system.theme('mid'))
        draw.set_font(fonts.sans18)
        for i in range(6):
            try:
                draw.string(page[i][1], 10, 60 + i*30)
            except:
                pass

        scroll = self._scroll
        scroll.up = page_num > 0
        scroll.down = page_num < (self._num_pages-1)
        scroll.draw()
