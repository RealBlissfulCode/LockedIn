# -*- coding: utf-8 -*-
"""The screen before you are signed in.

This used to be a passcode keypad that decrypted the whole application out of
the page. That made sense while there was one household and no server. Now the
markup is just a shell, and app_auth fills it with the Google button, the invite
code box or an error, depending on where you are in the flow.
"""

GATE_HTML = (
    '<div id="gate">'
    '<div class="gatebox">'
    '<div class="gatemark"></div>'
    '<h1>LockedIn</h1>'
    '<p class="gsub">Loading</p>'
    '</div></div>'
)
