"""
  * astroGraph.py is a module containing functions pertaining to the setting of color themes in ShiroiNinja desktop apps.
  * It is originally developed for AstroNinja. It uses shelf Files created in the main app to determine which color themes
  * to set.
"""
"""
   * Written By: Tom Mullins
   * Version: 0.85
   * Date Created:  01/23/18
   * Date Modified: 09/23/20
"""
"""
   * Changelog:
"""

# All the neccesary imports.
import re
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *



#==============================================================================================================
# functions for default theme.
#==============================================================================================================

# function for the tab Themes.
# Takes the different tab objects as arguments
def defaultTabs(a, b, c, d, e, f):

    d.setStyleSheet("""QTabBar::tab {
                                background: White;
                                color: black;
                                border: 2px solid;
                                padding: 6px;
                                border-color: White;
                                }
                                QTabBar::tab:selected {
                                background: Darkslategray;
                                border-color: White;
                                border-bottom-color: Darkslategray;
                                color: White;
                                }""")

    a.setStyleSheet("""QWidget { background-color: Darkslategray; color: white;
                            }
                        QApplication::QScrollBar:horizontal {
                            border: 2px solid white;
                            background: Darkslategray;
                            height: 15px;
                            margin: 0px 20px 0px 20px;
                            }
                        QScrollBar::handle:horizontal {
                            background: white;
                            min-width: 20px;
                        }
                        QScrollBar::add-line:horizontal {
                            border: 2px solid white;
                            background: white;
                            width: 20px;
                            subcontrol-position: right;
                            subcontrol-origin: margin;
                        }

                        QScrollBar::sub-line:horizontal {
                            border: 2px solid white;
                            background: white;
                            width: 20px;
                            subcontrol-position: left;
                            subcontrol-origin: margin;
                        }

                        QScrollBar:left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
                            border: 2px solid Darkslategray;
                            width: 3px;
                            height: 3px;
                            background: Darkslategray;
                        }

                        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                            background: none;
                        }

                        QScrollBar:vertical {
                            border: 2px solid white;
                            background: Darkslategray;
                            width: 15px;
                            margin: 22px 0px 22px 0px;
                        }
                        QScrollBar::handle:vertical {
                            background: white;
                            min-height: 20px;
                        }
                        QScrollBar::add-line:vertical {
                            border: 2px solid white;
                            background: white;
                            height: 20px;
                            subcontrol-position: bottom;
                            subcontrol-origin: margin;
                        }

                        QScrollBar::sub-line:vertical {
                            border: 2px solid white;
                            background: white;
                            height: 20px;
                            subcontrol-position: top;
                            subcontrol-origin: margin;
                        }
                        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                            border: 2px solid Darkslategray;
                            width: 3px;
                            height: 3px;
                            background: Darkslategray;
                        }

                        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                            background: none;
                        }
                        QFrame { background: Darkslategray; color: Ivory; }""")

    b.setStyleSheet("""QWidget { background-color: Darkslategray; color: white;
                            }
                        QApplication::QScrollBar:horizontal {
                            border: 2px solid white;
                            background: Darkslategray;
                            height: 15px;
                            margin: 0px 20px 0px 20px;
                            }
                        QScrollBar::handle:horizontal {
                            background: white;
                            min-width: 20px;
                        }
                        QScrollBar::add-line:horizontal {
                            border: 2px solid white;
                            background: white;
                            width: 20px;
                            subcontrol-position: right;
                            subcontrol-origin: margin;
                        }

                        QScrollBar::sub-line:horizontal {
                            border: 2px solid white;
                            background: white;
                            width: 20px;
                            subcontrol-position: left;
                            subcontrol-origin: margin;
                        }

                        QScrollBar:left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
                            border: 2px solid Darkslategray;
                            width: 3px;
                            height: 3px;
                            background: Darkslategray;
                        }

                        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                            background: none;
                        }

                        QScrollBar:vertical {
                            border: 2px solid white;
                            background: Darkslategray;
                            width: 15px;
                            margin: 22px 0px 22px 0px;
                        }
                        QScrollBar::handle:vertical {
                            background: white;
                            min-height: 20px;
                        }
                        QScrollBar::add-line:vertical {
                            border: 2px solid white;
                            background: white;
                            height: 20px;
                            subcontrol-position: bottom;
                            subcontrol-origin: margin;
                        }

                        QScrollBar::sub-line:vertical {
                            border: 2px solid white;
                            background: white;
                            height: 20px;
                            subcontrol-position: top;
                            subcontrol-origin: margin;
                        }
                        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                            border: 2px solid Darkslategray;
                            width: 3px;
                            height: 3px;
                            background: Darkslategray;
                        }

                        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                            background: none;
                        }
                        QFrame { background: Darkslategray; color: Ivory; }""")

    c.setStyleSheet("""QWidget { background-color: Darkslategray; color: white;
                            }
                        QApplication::QScrollBar:horizontal {
                            border: 2px solid white;
                            background: Darkslategray;
                            height: 15px;
                            margin: 0px 20px 0px 20px;
                            }
                        QScrollBar::handle:horizontal {
                            background: white;
                            min-width: 20px;
                        }
                        QScrollBar::add-line:horizontal {
                            border: 2px solid white;
                            background: white;
                            width: 20px;
                            subcontrol-position: right;
                            subcontrol-origin: margin;
                        }

                        QScrollBar::sub-line:horizontal {
                            border: 2px solid white;
                            background: white;
                            width: 20px;
                            subcontrol-position: left;
                            subcontrol-origin: margin;
                        }

                        QScrollBar:left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
                            border: 2px solid Darkslategray;
                            width: 3px;
                            height: 3px;
                            background: Darkslategray;
                        }

                        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                            background: none;
                        }

                        QScrollBar:vertical {
                            border: 2px solid white;
                            background: Darkslategray;
                            width: 15px;
                            margin: 22px 0px 22px 0px;
                        }
                        QScrollBar::handle:vertical {
                            background: white;
                            min-height: 20px;
                        }
                        QScrollBar::add-line:vertical {
                            border: 2px solid white;
                            background: white;
                            height: 20px;
                            subcontrol-position: bottom;
                            subcontrol-origin: margin;
                        }

                        QScrollBar::sub-line:vertical {
                            border: 2px solid white;
                            background: white;
                            height: 20px;
                            subcontrol-position: top;
                            subcontrol-origin: margin;
                        }
                        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                            border: 2px solid Darkslategray;
                            width: 3px;
                            height: 3px;
                            background: Darkslategray;
                        }

                        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                            background: none;
                        }
                        QFrame { background: Darkslategray; color: Ivory; }""")

    e.setStyleSheet("""QWidget { background-color: Darkslategray; color: white;
                            }
                        QApplication::QScrollBar:horizontal {
                            border: 2px solid white;
                            background: Darkslategray;
                            height: 15px;
                            margin: 0px 20px 0px 20px;
                            }
                        QScrollBar::handle:horizontal {
                            background: white;
                            min-width: 20px;
                        }
                        QScrollBar::add-line:horizontal {
                            border: 2px solid white;
                            background: white;
                            width: 20px;
                            subcontrol-position: right;
                            subcontrol-origin: margin;
                        }

                        QScrollBar::sub-line:horizontal {
                            border: 2px solid white;
                            background: white;
                            width: 20px;
                            subcontrol-position: left;
                            subcontrol-origin: margin;
                        }

                        QScrollBar:left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
                            border: 2px solid Darkslategray;
                            width: 3px;
                            height: 3px;
                            background: Darkslategray;
                        }

                        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                            background: none;
                        }

                        QScrollBar:vertical {
                            border: 2px solid white;
                            background: Darkslategray;
                            width: 15px;
                            margin: 22px 0px 22px 0px;
                        }
                        QScrollBar::handle:vertical {
                            background: white;
                            min-height: 20px;
                        }
                        QScrollBar::add-line:vertical {
                            border: 2px solid white;
                            background: white;
                            height: 20px;
                            subcontrol-position: bottom;
                            subcontrol-origin: margin;
                        }

                        QScrollBar::sub-line:vertical {
                            border: 2px solid white;
                            background: white;
                            height: 20px;
                            subcontrol-position: top;
                            subcontrol-origin: margin;
                        }
                        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                            border: 2px solid Darkslategray;
                            width: 3px;
                            height: 3px;
                            background: Darkslategray;
                        }

                        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                            background: none;
                        }
                        QFrame { background: Darkslategray; color: Ivory; }""")

    f.setStyleSheet("""QWidget { background-color: Darkslategray; color: white;
                            }
                        QApplication::QScrollBar:horizontal {
                            border: 2px solid white;
                            background: Darkslategray;
                            height: 15px;
                            margin: 0px 20px 0px 20px;
                            }
                        QScrollBar::handle:horizontal {
                            background: white;
                            min-width: 20px;
                        }
                        QScrollBar::add-line:horizontal {
                            border: 2px solid white;
                            background: white;
                            width: 20px;
                            subcontrol-position: right;
                            subcontrol-origin: margin;
                        }

                        QScrollBar::sub-line:horizontal {
                            border: 2px solid white;
                            background: white;
                            width: 20px;
                            subcontrol-position: left;
                            subcontrol-origin: margin;
                        }

                        QScrollBar:left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
                            border: 2px solid Darkslategray;
                            width: 3px;
                            height: 3px;
                            background: Darkslategray;
                        }

                        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                            background: none;
                        }

                        QScrollBar:vertical {
                            border: 2px solid white;
                            background: Darkslategray;
                            width: 15px;
                            margin: 22px 0px 22px 0px;
                        }
                        QScrollBar::handle:vertical {
                            background: white;
                            min-height: 20px;
                        }
                        QScrollBar::add-line:vertical {
                            border: 2px solid white;
                            background: white;
                            height: 20px;
                            subcontrol-position: bottom;
                            subcontrol-origin: margin;
                        }

                        QScrollBar::sub-line:vertical {
                            border: 2px solid white;
                            background: white;
                            height: 20px;
                            subcontrol-position: top;
                            subcontrol-origin: margin;
                        }
                        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                            border: 2px solid Darkslategray;
                            width: 3px;
                            height: 3px;
                            background: Darkslategray;
                        }

                        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                            background: none;
                        }
                        QFrame { background: Darkslategray; color: Ivory; }""")



# A funtion for the menubar theme
# Takes the menubar objects as arguments
def defaultMenu(a):

    a.setStyleSheet("QMenu::item:selected { background-color: Darkslategray; }")
    a.setStyleSheet("""QMenuBar { background-color: white; }
                            QMenuBar::item:selected { background-color: Darkslategray; color: White; }""")


#========================================================================================================================
# Functions for the "SpaceX" Theme
#========================================================================================================================

# function for the tab Themes.
# Takes the different tab objects as arguments
def spacexTabs(a, b, c, d, e, f):

    d.setStyleSheet("""QTabBar::tab {
                                background: White;
                                color: black;
                                border: 2px solid;
                                padding: 6px;
                                border-color: White;
                                }
                                QTabBar::tab:selected {
                                background: Steelblue;
                                border-color: White;
                                border-bottom-color: Steelblue;
                                color: White;
                                }""")

    a.setStyleSheet("""QWidget { background: Steelblue; color: white;
                            }
                            QApplication::QScrollBar:horizontal {
                                border: 2px solid white;
                                background: Steelblue;
                                height: 15px;
                                margin: 0px 20px 0 20px;
                            }
                            QScrollBar::handle:horizontal {
                                background: white;
                                min-width: 20px;
                            }
                            QScrollBar::add-line:horizontal {
                                border: 2px solid white;
                                background: white;
                                width: 20px;
                                subcontrol-position: right;
                                subcontrol-origin: margin;
                            }

                            QScrollBar::sub-line:horizontal {
                                border: 2px solid white;
                                background: white;
                                width: 20px;
                                subcontrol-position: left;
                                subcontrol-origin: margin;
                            }

                            QScrollBar:left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
                                border: 2px solid Steelblue;
                                width: 3px;
                                height: 3px;
                                background: Steelblue;
                            }

                            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                                background: none;
                            }

                            QScrollBar:vertical {
                                border: 2px solid white;
                                background: Steelblue;
                                width: 15px;
                                margin: 22px 0 22px 0;
                            }
                            QScrollBar::handle:vertical {
                                background: white;
                                min-height: 20px;
                            }
                            QScrollBar::add-line:vertical {
                                border: 2px solid white;
                                background: white;
                                height: 20px;
                                subcontrol-position: bottom;
                                subcontrol-origin: margin;
                            }

                            QScrollBar::sub-line:vertical {
                                border: 2px solid white;
                                background: white;
                                height: 20px;
                                subcontrol-position: top;
                                subcontrol-origin: margin;
                            }
                            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                                border: 2px solid Steelblue;
                                width: 3px;
                                height: 3px;
                                background: Steelblue;
                            }

                            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                                background: none;
                            }
                            QFrame { background: LightSlate Grey; color: Ivory;
                            }""")

    b.setStyleSheet("""QWidget { background-color: Steelblue; color: white;
                            }
                            QApplication::QScrollBar:horizontal {
                                border: 2px solid white;
                                background: Steelblue;
                                height: 15px;
                                margin: 0px 20px 0 20px;
                            }
                            QScrollBar::handle:horizontal {
                                background: white;
                                min-width: 20px;
                            }
                            QScrollBar::add-line:horizontal {
                                border: 2px solid white;
                                background: white;
                                width: 20px;
                                subcontrol-position: right;
                                subcontrol-origin: margin;
                            }

                            QScrollBar::sub-line:horizontal {
                                border: 2px solid white;
                                background: white;
                                width: 20px;
                                subcontrol-position: left;
                                subcontrol-origin: margin;
                            }

                            QScrollBar:left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
                                border: 2px solid Steelblue;
                                width: 3px;
                                height: 3px;
                                background: Steelblue;
                            }

                            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                                background: none;
                            }

                            QScrollBar:vertical {
                                border: 2px solid white;
                                background: Steelblue;
                                width: 15px;
                                margin: 22px 0 22px 0;
                            }
                            QScrollBar::handle:vertical {
                                background: white;
                                min-height: 20px;
                            }
                            QScrollBar::add-line:vertical {
                                border: 2px solid white;
                                background: white;
                                height: 20px;
                                subcontrol-position: bottom;
                                subcontrol-origin: margin;
                            }

                            QScrollBar::sub-line:vertical {
                                border: 2px solid white;
                                background: white;
                                height: 20px;
                                subcontrol-position: top;
                                subcontrol-origin: margin;
                            }
                            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                                border: 2px solid Steelblue;
                                width: 3px;
                                height: 3px;
                                background: Steelblue;
                            }

                            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                                background: none;
                            }
                            QFrame { background: LightSlate Grey; color: Ivory;
                            }""")
    c.setStyleSheet("""QWidget { background-color: Steelblue; color: white;
                            }
                            QApplication::QScrollBar:horizontal {
                                border: 2px solid white;
                                background: Steelblue;
                                height: 15px;
                                margin: 0px 20px 0 20px;
                            }
                            QScrollBar::handle:horizontal {
                                background: white;
                                min-width: 20px;
                            }
                            QScrollBar::add-line:horizontal {
                                border: 2px solid white;
                                background: white;
                                width: 20px;
                                subcontrol-position: right;
                                subcontrol-origin: margin;
                            }

                            QScrollBar::sub-line:horizontal {
                                border: 2px solid white;
                                background: white;
                                width: 20px;
                                subcontrol-position: left;
                                subcontrol-origin: margin;
                            }

                            QScrollBar:left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
                                border: 2px solid Steelblue;
                                width: 3px;
                                height: 3px;
                                background: Steelblue;
                            }

                            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                                background: none;
                            }

                            QScrollBar:vertical {
                                border: 2px solid white;
                                background: Steelblue;
                                width: 15px;
                                margin: 22px 0 22px 0;
                            }
                            QScrollBar::handle:vertical {
                                background: white;
                                min-height: 20px;
                            }
                            QScrollBar::add-line:vertical {
                                border: 2px solid white;
                                background: white;
                                height: 20px;
                                subcontrol-position: bottom;
                                subcontrol-origin: margin;
                            }

                            QScrollBar::sub-line:vertical {
                                border: 2px solid white;
                                background: white;
                                height: 20px;
                                subcontrol-position: top;
                                subcontrol-origin: margin;
                            }
                            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                                border: 2px solid Steelblue;
                                width: 3px;
                                height: 3px;
                                background: Steelblue;
                            }

                            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                                background: none;
                            }
                            QFrame { background: LightSlate Grey; color: Ivory;
                            }""")
    e.setStyleSheet("""QWidget { background-color: Steelblue; color: white;
                            }
                            QApplication::QScrollBar:horizontal {
                                border: 2px solid white;
                                background: Steelblue;
                                height: 15px;
                                margin: 0px 20px 0 20px;
                            }
                            QScrollBar::handle:horizontal {
                                background: white;
                                min-width: 20px;
                            }
                            QScrollBar::add-line:horizontal {
                                border: 2px solid white;
                                background: white;
                                width: 20px;
                                subcontrol-position: right;
                                subcontrol-origin: margin;
                            }

                            QScrollBar::sub-line:horizontal {
                                border: 2px solid white;
                                background: white;
                                width: 20px;
                                subcontrol-position: left;
                                subcontrol-origin: margin;
                            }

                            QScrollBar:left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
                                border: 2px solid Steelblue;
                                width: 3px;
                                height: 3px;
                                background: Steelblue;
                            }

                            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                                background: none;
                            }

                            QScrollBar:vertical {
                                border: 2px solid white;
                                background: Steelblue;
                                width: 15px;
                                margin: 22px 0 22px 0;
                            }
                            QScrollBar::handle:vertical {
                                background: white;
                                min-height: 20px;
                            }
                            QScrollBar::add-line:vertical {
                                border: 2px solid white;
                                background: white;
                                height: 20px;
                                subcontrol-position: bottom;
                                subcontrol-origin: margin;
                            }

                            QScrollBar::sub-line:vertical {
                                border: 2px solid white;
                                background: white;
                                height: 20px;
                                subcontrol-position: top;
                                subcontrol-origin: margin;
                            }
                            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                                border: 2px solid Steelblue;
                                width: 3px;
                                height: 3px;
                                background: Steelblue;
                            }

                            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                                background: none;
                            }
                            QFrame { background: LightSlate Grey; color: Ivory;
                            }""")
    f.setStyleSheet("""QWidget { background-color: Steelblue; color: white;
                            }
                            QApplication::QScrollBar:horizontal {
                                border: 2px solid white;
                                background: Steelblue;
                                height: 15px;
                                margin: 0px 20px 0 20px;
                            }
                            QScrollBar::handle:horizontal {
                                background: white;
                                min-width: 20px;
                            }
                            QScrollBar::add-line:horizontal {
                                border: 2px solid white;
                                background: white;
                                width: 20px;
                                subcontrol-position: right;
                                subcontrol-origin: margin;
                            }

                            QScrollBar::sub-line:horizontal {
                                border: 2px solid white;
                                background: white;
                                width: 20px;
                                subcontrol-position: left;
                                subcontrol-origin: margin;
                            }

                            QScrollBar:left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
                                border: 2px solid Steelblue;
                                width: 3px;
                                height: 3px;
                                background: Steelblue;
                            }

                            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                                background: none;
                            }

                            QScrollBar:vertical {
                                border: 2px solid white;
                                background: Steelblue;
                                width: 15px;
                                margin: 22px 0 22px 0;
                            }
                            QScrollBar::handle:vertical {
                                background: white;
                                min-height: 20px;
                            }
                            QScrollBar::add-line:vertical {
                                border: 2px solid white;
                                background: white;
                                height: 20px;
                                subcontrol-position: bottom;
                                subcontrol-origin: margin;
                            }

                            QScrollBar::sub-line:vertical {
                                border: 2px solid white;
                                background: white;
                                height: 20px;
                                subcontrol-position: top;
                                subcontrol-origin: margin;
                            }
                            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                                border: 2px solid Steelblue;
                                width: 3px;
                                height: 3px;
                                background: Steelblue;
                            }

                            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                                background: none;
                            }
                            QFrame { background: LightSlate Grey; color: Ivory;
                            }
                            """)



# A function for the menubar theme
# Takes the menubar objects as arguments
def spacexMenu(a):

    a.setStyleSheet("QMenu::item:selected { background-color: Steelblue; }")
    a.setStyleSheet("""QMenuBar { background-color: white; }
                            QMenuBar::item:selected { background-color: Steelblue; color: White; }""")


def innerFrame(a):
    a.setStyleSheet(" QFrame { background: Steelblue; color: white }")

#==============================================================================================================
# functions for Japan theme.
#==============================================================================================================

# function for the tab Themes.
# Takes the different tab objects as arguments
def japanTabs(a, b, c, d):

    d.setStyleSheet("""QTabBar::tab {
                                background: White;
                                color: black;
                                border: 2px solid;
                                padding: 6px;
                                border-color: White;
                                }
                                QTabBar::tab:selected {
                                background: White;
                                border-color: White;
                                border-bottom-color: White;
                                color: black;
                                }""")

    a.setStyleSheet("QWidget { background-color: White; color: DimGray; }")
    b.setStyleSheet("QWidget { background-color: white; color: DimGray; }")
    c.setStyleSheet("QWidget { background-color: white; color: DimGray; }")

# A funtion for the menubar theme
# Takes the menubar objects as arguments
def japanMenu(a):

    a.setStyleSheet("QMenu::item:selected { background-color: FireBrick; }")
    a.setStyleSheet("""QMenuBar { background-color: white; }
                            QMenuBar::item:selected { background-color: FireBrick; color: White; }""")

def japanFrame(a):
    a.setStyleSheet(" QFrame { background: FireBrick; color: DimGray }")

#========================================================================================================================
# Functions for the "Broco" Theme
#========================================================================================================================

# function for the tab Themes.
# Takes the different tab objects as arguments
def brocoTabs(a, b, c, d, e, f):

    brocoSheet1 = """QWidget { background-color: black; color: DarkTurquoise;
                            }
                            QApplication::QAbstractScrollArea {
                                background-color: black;
                            }
                            QWidget::QScrollBar {
                                border: none;
                            }
                            QScrollBar:horizontal {
                                border: 2px solid DarkTurquoise;
                                background: black;
                                height: 15px;
                                margin: 0px 20px 0 20px;
                            }
                            QScrollBar::handle:horizontal {
                                background: DarkTurquoise;
                                min-width: 20px;
                            }
                            QScrollBar::add-line:horizontal {
                                border: 2px solid hotpink;
                                background: hotpink;
                                width: 20px;
                                subcontrol-position: right;
                                subcontrol-origin: margin;
                            }

                            QScrollBar::sub-line:horizontal {
                                border: 2px hotpink;
                                background: hotpink;
                                width: 20px;
                                subcontrol-position: left;
                                subcontrol-origin: margin;
                            }

                            QScrollBar:left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
                                border: 2px solid DarkTurquoise;
                                width: 3px;
                                height: 3px;
                                background: DarkTurquoise;
                            }

                            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                                background: none;
                            }

                            QScrollBar:vertical {
                                border: 2px solid DarkTurquoise;
                                background: black;
                                width: 15px;
                                margin: 22px 0 22px 0;
                            }
                            QScrollBar::handle:vertical {
                                background: DarkTurquoise;
                                min-height: 20px;
                            }
                            QScrollBar::add-line:vertical {
                                border: 2px solid hotpink;
                                background: hotpink;
                                height: 20px;
                                subcontrol-position: bottom;
                                subcontrol-origin: margin;
                            }

                            QScrollBar::sub-line:vertical {
                                border: 2px solid hotpink;
                                background: hotpink;
                                height: 20px;
                                subcontrol-position: top;
                                subcontrol-origin: margin;
                            }
                            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                                border: 2px solid DarkTurquoise;
                                width: 3px;
                                height: 3px;
                                background: DarkTurquoise;
                            }

                            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                                background: black;
                            }
                            QFrame { background: black; color: hotpink; }"""

    pinkSheet = """QWidget { background-color: black; color: hotpink;
                            }
                            QApplication::QScrollArea {
                                background-color: black;
                            }
                            QScrollBar {
                                border: none;
                            }
                            QScrollBar:horizontal {
                                border: 2px solid DarkTurquoise;
                                background: black;
                                height: 15px;
                                margin: 0px 20px 0 20px;
                            }
                            QScrollBar::handle:horizontal {
                                background: DarkTurquoise;
                                min-width: 20px;
                            }
                            QScrollBar::add-line:horizontal {
                                border: 2px solid hotpink;
                                background: hotpink;
                                width: 20px;
                                subcontrol-position: right;
                                subcontrol-origin: margin;
                            }

                            QScrollBar::sub-line:horizontal {
                                border: 2px hotpink;
                                background: hotpink;
                                width: 20px;
                                subcontrol-position: left;
                                subcontrol-origin: margin;
                            }

                            QScrollBar:left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
                                border: 2px solid DarkTurquoise;
                                width: 3px;
                                height: 3px;
                                background: DarkTurquoise;
                            }

                            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                                background: none;
                            }

                            QScrollBar:vertical {
                                border: 2px solid DarkTurquoise;
                                background: black;
                                width: 15px;
                                margin: 22px 0 22px 0;
                            }
                            QScrollBar::handle:vertical {
                                background: DarkTurquoise;
                                min-height: 20px;
                            }
                            QScrollBar::add-line:vertical {
                                border: 2px solid hotpink;
                                background: hotpink;
                                height: 20px;
                                subcontrol-position: bottom;
                                subcontrol-origin: margin;
                            }

                            QScrollBar::sub-line:vertical {
                                border: 2px solid hotpink;
                                background: hotpink;
                                height: 20px;
                                subcontrol-position: top;
                                subcontrol-origin: margin;
                            }
                            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                                border: 2px solid DarkTurquoise;
                                width: 3px;
                                height: 3px;
                                background: DarkTurquoise;
                            }

                            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                                background: black;
                            }
                            QFrame { background: black; color: hotpink; }"""

    d.setStyleSheet("""QTabBar::tab {
                                background: DarkTurquoise;
                                color: black;
                                border: 2px solid;
                                padding: 6px;
                                border-color: DarkTurquoise;
                                }
                                QTabBar::tab:selected {
                                background: Black;
                                border-color: Black;
                                border-bottom-color: black;
                                color: DarkTurquoise;
                                }""")

    a.setStyleSheet(brocoSheet1)
    b.setStyleSheet(pinkSheet)
    c.setStyleSheet(brocoSheet1)
    e.setStyleSheet(pinkSheet)
    f.setStyleSheet(brocoSheet1)


# A function for the menubar theme
# Takes the menubar objects as arguments
def brocoMenu(a):


    a.setStyleSheet("""QMenu { background-color: black; color: hotpink; border: none; }
                            QMenu::item {background-color: transparent;}
                            QMenu::item:selected { background-color: DarkTurquoise; color: hotpink; }
                            QMenuBar { background-color: black; color: hotpink; border: none; }
                            QMenuBar::item:selected { background-color: DarkTurquoise; color: hotpink;}""")
