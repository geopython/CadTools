# -*- coding: utf-8 -*-99

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import sys

from ui_cadconsole import Ui_CadConsole


class CadConsole(QDockWidget, Ui_CadConsole,  object):
    """This class 
    """
    
    def __init__(self, plugin, digitizer):
        """The constructor."""

        QDockWidget.__init__(self, None)
        self.setupUi(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.digitizer = digitizer
        self.plugin = plugin
        self.mapTool=None
        self.__dlgAddRel=None
                
    def initGui(self):
##        self.textEdit = QTextEdit(self.dockWidgetContents)
##        self.textEdit.setObjectName("textEdit")
##        self.vboxlayout.addWidget(self.textEdit)
        self.edit = CadPythonEdit(self.digitizer, self.dockWidgetContents)
        self.edit.setObjectName("textEdit")
        self.vboxlayout.addWidget(self.edit)
        
        pass
##        self.textEdit.setTextInteractionFlags(Qt.TextEditorInteraction)
##        self.textEdit.setAcceptDrops(False)
##        #self.textEdit.setMinimumSize(30, 30)
##        self.textEdit.setUndoRedoEnabled(False)
##        self.textEdit.setAcceptRichText(False)
##        monofont = QFont("Bitstream Vera Sans Mono", 10)
##        self.textEdit.setFont(monofont)
        
        
class CadPythonEdit(QTextEdit):

  def __init__(self, digitizer, parent=None):
    QTextEdit.__init__(self)
##    code.InteractiveInterpreter.__init__(self, locals=None)

    self.digitizer = digitizer

    self.setTextInteractionFlags(Qt.TextEditorInteraction)
    self.setAcceptDrops(False)
    self.setMinimumSize(30, 30)
    self.setUndoRedoEnabled(False)
    self.setAcceptRichText(False)
    monofont = QFont("Bitstream Vera Sans Mono", 10)
    self.setFont(monofont)

    self.buffer = []

    self.insertTaggedText("Welcome to the CAD console.\n" "\n", ConsoleHighlighter.INIT)

##    for line in _init_commands:
##      self.runsource(line)
##
    self.displayPrompt(False)

    self.history = QStringList()
    self.historyIndex = 0

    self.high = ConsoleHighlighter(self)

  def displayPrompt(self, more=False):
    self.currentPrompt = "... " if more else "cad> "
    self.currentPromptLength = len(self.currentPrompt)
    self.insertTaggedLine(self.currentPrompt, ConsoleHighlighter.EDIT_LINE)
    self.moveCursor(QTextCursor.End, QTextCursor.MoveAnchor)

  def isCursorInEditionZone(self):
    cursor = self.textCursor()
    pos = cursor.position()
    block = self.document().lastBlock()
    last = block.position() + self.currentPromptLength
    return pos >= last

  def currentCommand(self):
    block = self.cursor.block()
    text = block.text()
    return text.right(text.length()-self.currentPromptLength)

  def showPrevious(self):
        if self.historyIndex < len(self.history) and not self.history.isEmpty():
            self.cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.MoveAnchor)
            self.cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.KeepAnchor)
            self.cursor.removeSelectedText()
            self.cursor.insertText(self.currentPrompt)
            self.historyIndex += 1
            if self.historyIndex == len(self.history):
                self.insertPlainText("")
            else:
                self.insertPlainText(self.history[self.historyIndex])
                
  def showNext(self):
        if  self.historyIndex > 0 and not self.history.isEmpty():
            self.cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.MoveAnchor)
            self.cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.KeepAnchor)
            self.cursor.removeSelectedText()
            self.cursor.insertText(self.currentPrompt)
            self.historyIndex -= 1
            if self.historyIndex == len(self.history):
                self.insertPlainText("")
            else:
                self.insertPlainText(self.history[self.historyIndex])

  def updateHistory(self, command):
        if isinstance(command, QStringList):
            for line in command:
                self.history.append(line)
        elif not command == "":
            if len(self.history) <= 0 or \
            not command == self.history[-1]:
                self.history.append(command)
        self.historyIndex = len(self.history)
 
  def keyPressEvent(self, e):
    self.cursor = self.textCursor()
    # if the cursor isn't in the edition zone, don't do anything except Ctrl+C
    if not self.isCursorInEditionZone():
        if e.modifiers() & Qt.ControlModifier or e.modifiers() & Qt.MetaModifier:
            if e.key() == Qt.Key_C or e.key() == Qt.Key_A:
                QTextEdit.keyPressEvent(self, e)
        else:
            # all other keystrokes get sent to the input line
            self.cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)        
                        
    else:
        # if Return is pressed, then perform the commands
        if e.key() == Qt.Key_Return:
            self.entered()
        # if Up or Down is pressed
        elif e.key() == Qt.Key_Down:
            self.showPrevious()
            pass
        elif e.key() == Qt.Key_Up:
            self.showNext()
            pass
        # if backspace is pressed, delete until we get to the prompt
        elif e.key() == Qt.Key_Backspace:
            if not self.cursor.hasSelection() and self.cursor.columnNumber() == self.currentPromptLength:
                return
            QTextEdit.keyPressEvent(self, e)
        # if the left key is pressed, move left until we get to the prompt
        elif e.key() == Qt.Key_Left and self.cursor.position() > self.document().lastBlock().position() + self.currentPromptLength:
            anchor = QTextCursor.KeepAnchor if e.modifiers() & Qt.ShiftModifier else QTextCursor.MoveAnchor
            move = QTextCursor.WordLeft if e.modifiers() & Qt.ControlModifier or e.modifiers() & Qt.MetaModifier else QTextCursor.Left
            self.cursor.movePosition(move, anchor)
        # use normal operation for right key
        elif e.key() == Qt.Key_Right:
            anchor = QTextCursor.KeepAnchor if e.modifiers() & Qt.ShiftModifier else QTextCursor.MoveAnchor
            move = QTextCursor.WordRight if e.modifiers() & Qt.ControlModifier or e.modifiers() & Qt.MetaModifier else QTextCursor.Right
            self.cursor.movePosition(move, anchor)
        # if home is pressed, move cursor to right of prompt
        elif e.key() == Qt.Key_Home:
            anchor = QTextCursor.KeepAnchor if e.modifiers() & Qt.ShiftModifier else QTextCursor.MoveAnchor
            self.cursor.movePosition(QTextCursor.StartOfBlock, anchor, 1)
            self.cursor.movePosition(QTextCursor.Right, anchor, self.currentPromptLength)
        # use normal operation for end key
        elif e.key() == Qt.Key_End:
            anchor = QTextCursor.KeepAnchor if e.modifiers() & Qt.ShiftModifier else QTextCursor.MoveAnchor
            self.cursor.movePosition(QTextCursor.EndOfBlock, anchor, 1)
        # use normal operation for all remaining keys
        else:
            QTextEdit.keyPressEvent(self, e)

    self.setTextCursor(self.cursor)
    self.ensureCursorVisible()
##
##  def insertFromMimeData(self, source):
##        self.cursor = self.textCursor()
##        self.cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor, 1)
##        self.setTextCursor(self.cursor)
##        if source.hasText():
##            pasteList = QStringList()
##            pasteList = source.text().split("\n")
##            for line in pasteList:
##		self.insertPlainText(line)
##		self.runCommand(unicode(line))
##
  def entered(self):
    self.cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)
    self.setTextCursor(self.cursor)
    print self.currentCommand()
    self.runCommand( unicode(self.currentCommand()) )

  def insertTaggedText(self, txt, tag):

    if len(txt) > 0 and txt[-1] == '\n': # remove trailing newline to avoid one more empty line
      txt = txt[0:-1]

    c = self.textCursor()
    for line in txt.split('\n'):
      b = c.block()
      b.setUserState(tag)
      c.insertText(line)
      c.insertBlock()

  def insertTaggedLine(self, txt, tag):
    c = self.textCursor()
    b = c.block()
    b.setUserState(tag)
    c.insertText(txt)

  def runCommand(self, cmd):

    self.updateHistory(cmd)

    cmds = cmd.strip().split()
    if len(cmds) == 1 and (cmds[0] == "exit" or cmds[0] == "quit"):
        self.parentWidget().parentWidget().close()
    elif len(cmds) == 2 and cmds[0] == "close" and cmds[1] == "poly":
        self.digitizer.closePolygon()
    elif len(cmds) == 2 and cmds[0] == "close" and cmds[1] == "line":
        self.digitizer.closeLine()        
    elif len(cmds) == 2 and cmds[0] == "ortho" and cmds[1] == "on":
        self.digitizer.setOrtho(True)
    elif len(cmds) == 2 and cmds[0] == "ortho" and cmds[1] == "off":
        self.digitizer.setOrtho(False)
    elif len(cmds) == 2 and cmds[0] == "length":   
        if cmds[1] == "off":
            self.digitizer.setLength(-1)
        else:
            try:
                length = float(cmds[1])
                if length == 0 or length < 0:
                    ## Ok, this is stupid... but it throws an exception.
                    float("a")
                else:
                    self.digitizer.setLength(length)
            except ValueError:
                self.insertPlainText("\n")
                self.insertTaggedText("error", ConsoleHighlighter.ERROR)
    elif len(cmds) == 3:
        if cmds[0] == "polar":
            try:
                azi = float(cmds[1])
                dist = float(cmds[2])
                output = self.digitizer.movePointPolar(azi,dist)    
                if output == False:
                      self.insertPlainText("\n")
                      self.insertTaggedText("error", ConsoleHighlighter.ERROR) 
            except ValueError:
                self.insertPlainText("\n")
                self.insertTaggedText("error", ConsoleHighlighter.ERROR)
                
        elif cmds[0] == "ortho":
            try:
                abs = float(cmds[1])
                ord = float(cmds[2])
                output = self.digitizer.movePointOrthogonal(abs,ord)

                if output == False:
                      self.insertPlainText("\n")
                      self.insertTaggedText("error", ConsoleHighlighter.ERROR)
            except ValueError:
                self.insertPlainText("\n")
                self.insertTaggedText("error", ConsoleHighlighter.ERROR)
    else:
        self.insertPlainText("\n")
        self.insertTaggedText("unknown command", ConsoleHighlighter.ERROR)

    self.insertPlainText("\n")

    self.buffer.append(cmd)
    src = "\n".join(self.buffer)
    
    #print "runCommand"
    #print self.digitizer
    
    self.displayPrompt(False)
    
    
class ConsoleHighlighter(QSyntaxHighlighter):
  EDIT_LINE, ERROR, OUTPUT, INIT = range(4)
  def __init__(self, doc):
    QSyntaxHighlighter.__init__(self,doc)
    formats = { self.OUTPUT : Qt.black, self.ERROR : Qt.red, self.EDIT_LINE : Qt.darkGreen, self.INIT : Qt.gray }
    self.f = {}
    for tag, color in formats.iteritems():
      self.f[tag] = QTextCharFormat()
      self.f[tag].setForeground(color)

  def highlightBlock(self, txt):
    size = txt.length()
    state = self.currentBlockState()
    if state == self.OUTPUT or state == self.ERROR or state == self.INIT:
      self.setFormat(0,size, self.f[state])
    # highlight prompt only
    if state == self.EDIT_LINE:
      self.setFormat(0,3, self.f[self.EDIT_LINE]) 
