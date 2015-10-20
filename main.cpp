////////////////////////////////////////////////////////////////////////////////
// TheDisplayer
//
// A Qt based web browser with a python based backend to handle automatic
//  scheduling of the AOSC signage in the main hall.
// The python section is responsible for loading a series of user defined 
//  plugins, each responsible for a different type of display. The plugin
//  specifies logic to define the priority, size, expected display durations,
//  and method of generating the html to display.
//
//  Travis T. Sluka (tsluka@atmos.umd.edu)
//  Cory T. Martin  (cmartin@atmos.umd.edu)
////////////////////////////////////////////////////////////////////////////////

#include <Python.h>
#include <signal.h>

#include <QApplication>
#include <QUrl>
#include <QObject>
#include <QtGlobal>
#include <QString>
#include <QResizeEvent>
#include <QDesktopWidget>

#include "main.h"

const int TIMER_FREQUENCY   = 10000;  // how often python logic is called (msec)
const int FULLSCREEN_HEIGHT = 1920;
const int FULLSCREEN_WIDTH  = 1080;

int PAD_LEFT          = 22;
int PAD_RIGHT         = 21;
int PAD_TOP           = 38;
int PAD_BOTTOM        = 0;

int HEADER_HEIGHT     = 120;
int FOOTER_HEIGHT     = 130;

bool fullScreen = false;


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
    //    return 1;
  }
  QString configFile = argv[1];

  
  //Initialize Python, import the python 'main' module and save references
  // to it, then tell the main.py to initialize
  Py_SetProgramName(argv[0]);
  Py_Initialize(); 
  PyRun_SimpleString("import sys; sys.path.insert(0,'.'); import main");
  PyObject* moduleStr   = PyString_FromString((char*)"main");
    if (moduleStr == 0) qFatal("Unable to load python files");
  pyModule              = PyImport_Import(moduleStr);
    if (pyModule == 0)  qFatal("Unable to load main python 'main' module");
  Py_INCREF(pyModule); //no idea if this is required
  pyUpdate              = PyObject_GetAttrString(pyModule,(char*)"update");
    if (pyUpdate == 0)  qFatal("Unable to load pyUpdate function");
  Py_INCREF(pyUpdate);
  QString pyInitCommand = "main.init('"+configFile+"');";
  PyRun_SimpleString(pyInitCommand.toStdString().c_str());

  
  //Get configuration parameters from the config.py file that Qt needs
  PyObject* result;
  PyObject* func;
  func = PyObject_GetAttrString(pyModule, (char*)"getConfig");
    if (func == 0)  qFatal("unable to load main.getConfig");
  result = PyObject_CallObject(func, NULL);
  PyArg_ParseTuple(result, "biiii",
		   &fullScreen, &PAD_LEFT, &PAD_TOP, &PAD_RIGHT, &PAD_BOTTOM);
  Py_DECREF(result);
 
  
  //initialize Qt
  QApplication app(argc, argv);
  MainWindow mainWin(pyUpdate);
  if (fullScreen)
    mainWin.showFullScreen();
  else {
    // if not full screen, show as a scaled version with 9:16 ratio
    QRect winSize = QApplication::desktop()->screenGeometry();
    int w,h;
    h = winSize.height()-100;
    w = h/16.0*9.0;
    mainWin.setFixedSize(w,h);
    mainWin.show();
  }
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
  //  this->center_full   = new QWebView(this);
  this->center_half_1 = new QWebView(this);
  this->center_half_2 = new QWebView(this);
  this->webList << this->header << this->footer
    //<< this->center_full
		<< this->center_half_1	<< this->center_half_2;

  
  //setup the main timer that periodically makes calls to the python logic
  // and determines what should be reloaded
  timer = new QTimer(this);
  connect(timer, SIGNAL(timeout()), this, SLOT(updateTimer()));
  timer->start(TIMER_FREQUENCY);
  updateTimer();
}


void MainWindow::resizeEvent(QResizeEvent* event) {

  const int width  = event->size().width() - PAD_LEFT - PAD_RIGHT;
  const int height = event->size().height() - PAD_TOP - PAD_BOTTOM;

  // check to see if we aren't the full width/height, (debug mode)
  //  if so scale the web widgets down
  float ratio = 1.0;
  if (!fullScreen){
    ratio = (float)width/FULLSCREEN_WIDTH;
    for (int i = 0; i < this->webList.size(); ++i) {
      this->webList[i]->setZoomFactor(ratio);
    }
  }

  int headerHeight = HEADER_HEIGHT*ratio;
  int footerHeight = FOOTER_HEIGHT*ratio;
  int halfHeight = floor((height-headerHeight-footerHeight)/2);
 
  //set the position of the web widgets
  this->header->setGeometry(PAD_LEFT, PAD_TOP, width, headerHeight);
  //  this->center_full->setGeometry(0,headerHeight, width,height-headerHeight-footerHeight);
  this->center_half_2->setGeometry(PAD_LEFT, headerHeight+PAD_TOP, width, halfHeight);
  this->center_half_1->setGeometry(PAD_LEFT, headerHeight+PAD_TOP+halfHeight,  width, halfHeight);
  this->footer->setGeometry(PAD_LEFT, headerHeight+PAD_TOP+2*halfHeight, width, footerHeight);

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
