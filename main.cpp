////////////////////////////////////////////////////////////////////////////////
// TheDisplayer
// A Qt based web browser with a python based backend to handle automatic
//  scheduling of the AOSC signage in the main hall.
// The python section is responsible for loading a series of user defined 
//  plugins, each responsible for a different type of display. The plugin
//  specifies logic to define the priority, size, expected display durations,
//  and method of generating the html to display.
////////////////////////////////////////////////////////////////////////////////
#include <Python.h>

#include <signal.h>

#include <QApplication>
#include <QUrl>
#include <QObject>
#include <QtGlobal>
#include <QString>
#include <QResizeEvent>

#include "main.h"

const int TIMER_FREQUENCY = 1000;

// Handles to the required static python objects
PyObject* pyModule;  // handle to main python script module
PyObject* pyUpdate;  // handle to main python script update method


////////////////////////////////////////////////////////////////////////////////
// Main method
////////////////////////////////////////////////////////////////////////////////
int main(int argc, char *argv[])
{
  //ensure command line argument gives name of config file
  if (argc != 2){
    qCritical("usage: \n  display <config_file.py>");
    return 1;
  }
  QString configFile = argv[1];


  //Initialize Python, import the required 'display' module and save references
  // to it, then tell the display to initialize
  Py_SetProgramName(argv[0]);
  Py_Initialize(); 
  PyRun_SimpleString("import sys; sys.path.insert(0,'.'); import main");
  PyObject* moduleStr   = PyString_FromString((char*)"main");
    if (moduleStr == 0) qFatal("Unable to load python files");
  pyModule              = PyImport_Import(moduleStr);
    if (pyModule == 0)  qFatal("Unable to load main python 'main' module");
  pyUpdate              = PyObject_GetAttrString(pyModule,(char*)"update");
    if (pyUpdate == 0)  qFatal("Unable to load pyUpdate function");
  QString pyInitCommand = "main.init('"+configFile+"');";
  PyRun_SimpleString(pyInitCommand.toAscii());

  //Get configuration parameters from the config.py file that Qt needs
  bool fullScreen;
  //  PyObject* args;
  PyObject* result;
  PyObject* func;
  func = PyObject_GetAttrString(pyModule, (char*)"isFullscreen");
    if (func == 0)  qFatal("unable to load main.isFullscreen");
  result = PyObject_CallObject(func, NULL);
    if (result == 0)  qFatal("unable to run main.isFullscreen");
  fullScreen = (result == Py_True);
  Py_DECREF(result);
  Py_DECREF(func);


  //initialize Qt
  QApplication app(argc, argv);
  MainWindow mainWin(pyUpdate);
  if (fullScreen)
    mainWin.showFullScreen();
  else
    mainWin.showMaximized();
  QApplication::setOverrideCursor(Qt::BlankCursor);
    
  //force everything to shutdown if ctrl-c is pressed
  //TODO: this should be changed to handle a graceful shutdown
  signal(SIGINT,SIG_DFL);

  //run the main window loop
  // calling python update logic within the timer in the main window
  int val = app.exec();

  //clean up after everything is done
  Py_Finalize();
  return val;
}



//******************************************************************
//Qt Class for handling the main window
//******************************************************************

MainWindow::MainWindow(PyObject* pyUpdate) {
  this->pyUpdate = pyUpdate;

  //get python ready
  //TODO, dynamically create frames as specified in config file
  this->header = new QWebView(this);
  this->footer = new QWebView(this);
  this->center_full   = new QWebView(this);
  this->center_half_1 = new QWebView(this);
  this->center_half_2 = new QWebView(this);


  //setup the main timer that periodically makes calls to the python logic
  // and determines what should be reloaded
  timer = new QTimer(this);
  connect(timer, SIGNAL(timeout()), this, SLOT(updateTimer()));
  timer->start(TIMER_FREQUENCY);
   updateTimer();
}


void MainWindow::resizeEvent(QResizeEvent* event) {
  //TODO: handle different display layouts
  const int width  = event->size().width();
  const int height = event->size().height();

  const int headerHeight = 100;
  const int footerHeight = 100;
 

  this->header->setGeometry(0,0,width,headerHeight);
  this->footer->setGeometry(0,height-footerHeight,width,footerHeight);
  this->center_full->setGeometry(0,headerHeight, width,height-headerHeight-footerHeight);
  this->center_half_1->setGeometry(
	     0, headerHeight,
	     width, floor((height-headerHeight-footerHeight)/2));
  this->center_half_2->setGeometry(
	     0, headerHeight+floor((height-headerHeight-footerHeight)/2),
	     width, height-headerHeight-floor((height-headerHeight-footerHeight)/2)-footerHeight);
}


void MainWindow::updateTimer(){
  int len;
  
  //have the python code update the displays
  PyObject* result      = PyObject_CallObject(this->pyUpdate, NULL);
  if (result == 0)  qFatal("pyUpdate result == 0");

  //above function returns a list of displayname/url tuples
  len = PySequence_Size(result);
  for (int i = 0; i < len; i++)
  {
    //for each tuple, extract the display location name and new url
    PyObject* tuple = PySequence_Fast_GET_ITEM(result, i);
    PyObject* t1 = PyTuple_GetItem(tuple,0);
    PyObject* t2 = PyTuple_GetItem(tuple,1);
    if (tuple == NULL) qFatal("tuple = null");
    if (t1 == NULL) qFatal("t1 = null");
    if (t2 == NULL) qFatal("t2 = null");
    char* location = PyString_AsString(t1);
    char* url = PyString_AsString(t2);
    if (location == NULL) qFatal("location = null");
    if (url== NULL) qFatal("url = null");

    //find which webview object this tuple refers to
    QWebView* view;
    if (strcmp(location,"header") == 0)
      view = this->header;
    else if(strcmp(location,"footer") == 0)
      view = this->footer;
    else if(strcmp(location,"half_1") == 0)
      view = this->center_half_1;
    else if(strcmp(location,"half_2") == 0)
      view = this->center_half_2;
    else
      qFatal("Illegal return value specified from python:update()");

    //update the web url for that display location
    view->load(QUrl(url));
  }
  Py_DECREF(result);
}
