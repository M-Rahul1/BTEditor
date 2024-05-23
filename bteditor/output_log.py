import re
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QAbstractScrollArea
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDockWidget
from PyQt5 import QtCore

class scrollProxy(QAbstractScrollArea):
    def __init__(self, widget):
        self.__widget = widget
        self.__widgetType = type(widget)
        self.__widget.focusInEvent = self.focusInEvent
        self.__widget.focusOutEvent = self.focusOutEvent

    def focusOutEvent(self, *args, **kwargs):
        # print('debug: %s focus OUT' & self.__widgetType.__name__)
        self.__widget.verticalScrollBar().setProperty('parentFocus', False)
        self.__widget.horizontalScrollBar().setProperty('parentFocus', False)
        self.__widget.verticalScrollBar().setStyle(QApplication.style())
        self.__widget.horizontalScrollBar().setStyle(QApplication.style())
        self.__widgetType.focusOutEvent(self.__widget, *args, **kwargs)

    def focusInEvent(self, *args, **kwargs):
        # print('debug: %s focus IN' & self.__widgetType.__name__)
        self.__widget.verticalScrollBar().setProperty('parentFocus', True)
        self.__widget.horizontalScrollBar().setProperty('parentFocus', True)
        self.__widget.verticalScrollBar().setStyle(QApplication.style())
        self.__widget.horizontalScrollBar().setStyle(QApplication.style())
        self.__widgetType.focusOutEvent(self.__widget, *args, **kwargs)

class Language(QtCore.QObject):
    English = u'english'
    Russian = u'русский'

    __languages = {
        u'english': English,
        u'eng': English,
        u'английский': English,
        u'англ': English,
        u'russian': Russian,
        u'rus': Russian,
        u'русский': Russian,
        u'рус': Russian
    }

    languageChanged = QtCore.pyqtSignal(str)  # Language change notification signal

    def __init__(self):
        QtCore.QObject.__init__(self, None)
        self.language = Language.English

    @QtCore.pyqtSlot(str)
    def changeLanguage(self, lang):
        """ Changes current language.

        Note that it also emits signal if language value would be changed.

        :param lang: Language name alias
        """
        if self.rightLanguage(lang):
            self.language = self.__languages[lang]
            self.languageChanged.emit(self.language)

    def rightLanguage(self, lang):
        """ Checks if passed language name string (alias) is available.

        :param lang: Language name alias
        :return: True if 'lang' alias present in available aliases list, False - otherwise
        """
        return lang in self.__languages

    def possibleValues(self):
        """ Returns all possible languages aliases. """
        return self.__languages.keys()

globalLanguage = Language()
    
class trStr(object):
    def __init__(self, eng, rus):
        self.__text = {
            Language.English: eng,
            Language.Russian: rus
        }

    def text(self):
        """ Returns text on appropriate language based on 'globalLanguage.language' value.

        :return: English or Russian translation
        """
        global globalLanguage
        return self.__text[globalLanguage.language]

    def rus(self):
        """ Returns Russian text string. """
        return self.__text[Language.Russian]

    def eng(self):
        """ Returns English text string. """
        return self.__text[Language.English]

    def setRus(self, text):
        """ Sets russian translation.

        :param text: Text in russian
        """
        self.__text[Language.Russian] = text

    def setEng(self, text):
        """ Sets english translation.

        :param text: Text in english
        """
        self.__text[Language.English] = text

    def __str__(self):
        """ Same as 'text()' method. """
        return self.text()

    def __repr__(self):
        """ Same as 'text()' method. """
        return self.text()
    
class trDockWidget(QDockWidget):
    def __init__(self, title, parent=None):
        isTr = isinstance(title, trStr)
        if isTr:
            txt = title.text()
        else:
            txt = title
        QDockWidget.__init__(self, txt, parent)
        if isTr:
            self._title = title
        else:
            self._title = trStr(title, title)

    def setWindowTitle(self, title):
        if isinstance(title, trStr):
            self._title = title
            QDockWidget.setWindowTitle(self, self._title.text())
        else:
            self._title = trStr(title, title)
            QDockWidget.setWindowTitle(self, title)
            
class ConsoleLog(QTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._focusProxy = scrollProxy(self)
        self.setAcceptRichText(True)
        self.setTextInteractionFlags(Qt.TextBrowserInteraction | Qt.TextSelectableByKeyboard)
        self.__text = u'> '
        self.__fontCol = False
        self.__ignoreEndl = False

    def appendText(self, text):
        if text == '\n' and self.__ignoreEndl:
            self.__ignoreEndl = False
            return

        self.__ignoreEndl = False

        # replace symbols '<' and '>' because these are html special symbols
        text = text.replace(u'<', u'&lt;').replace(u'>', u'&gt;')

        # закрытие тэга <font>, если требуется
        if self.__fontCol and '\n' in text:
            text = u'</font>' + text
            self.__fontCol = False

        # replace '\n' with html '<br/>' and insert '> ' sub-string into the beginning of every new line
        theText = text.replace(u'\n', u'<br/>> ')

        lowerStr = theText.lower().strip()

        # messages colorizing
        if u'error:' in lowerStr[:6]:
            p = re.compile(u'error:', re.IGNORECASE)
            theText = u'<font color=\"Red\">{0}'.format(p.sub(u'', theText, 1))
            self.__fontCol = True
        elif u'warning:' in lowerStr[:9]:
            p = re.compile(u'warning:', re.IGNORECASE)
            theText = u'<font color=\"Orange\">{0}'.format(p.sub(u'', theText, 1))
            self.__fontCol = True
        elif u'info:' in lowerStr[:5]:
            p = re.compile(u'info:', re.IGNORECASE)
            theText = u'<font color=\"CadetBlue\">{0}'.format(p.sub(u'', theText, 1))
            self.__fontCol = True
        elif u'ok:' in lowerStr[:3]:
            p = re.compile(u'ok:', re.IGNORECASE)
            theText = u'<font color=\"YellowGreen\">{0}'.format(p.sub(u'', theText, 1))
            self.__fontCol = True
        elif u'debug:' in lowerStr[:6]:
            # if not globals.debugMode:
            #     self.__ignoreEndl = True
            #     return
            p = re.compile(u'debug:', re.IGNORECASE)
            theText = u'<font color=\"RosyBrown\">{0}'.format(p.sub(u'', theText, 1))
            self.__fontCol = True

        # put new text into the end
        self.__text += theText

        # set new text to the QTextEdit to see changes
        self.setHtml(self.__text)

        # move scroll-bar into the end to be able to watch last message immediately
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

class OutputDock(trDockWidget):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.__writer = self.__write
        self.__textEdit = ConsoleLog(self)
        self.setWidget(self.__textEdit)

    def setSilent(self, silent):
        """ Changes '__writer' method to be able to write text or to be idle (depends on 'silent' value).

        :param silent: Boolean value; if True, then all new text would be displayed in QTextEdit,
                        otherwise - new text will be ignored
        """
        if silent:
            self.__writer = self.__doNotWrite
        else:
            self.__writer = self.__write

    def scrollBottom(self):
        """ Scrolls QTextEdit to the last message. """
        self.__textEdit.verticalScrollBar().setValue(self.__textEdit.verticalScrollBar().maximum())

    def scrollTop(self):
        """ Scrolls QTextEdit to the top (first message). """
        self.__textEdit.verticalScrollBar().setValue(self.__textEdit.verticalScrollBar().minimum())

    @QtCore.pyqtSlot(str)
    def write(self, text):
        """ Calls another method to write input text or to do nothing.

        :param text: Input text
        """
        self.__writer(text)

    def __write(self, text):
        """ Writes text into the end of text of self QTextEdit.

        :param text: Input text that will be displayed in QTextEdit
        """
        self.__textEdit.appendText(text)

    def __doNotWrite(self, text):
        """ Does nothing.

        :param text: Input text that will be ignored
        """
        pass

    def flush(self, *args, **kwargs):
        """ This method is called on application exit maybe by QApplication, I don't know,
        But it must exist or application will crush on exit.
        """
        pass
