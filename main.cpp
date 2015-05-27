//Code not to be read by Ning Zeng, so no other comments will be inserted
#include <Python.h>
#include <QApplication>
#include <QUrl>
#include <QObject>
#include <QtGlobal>
#include <QString>
#include "main.h"


int main(int argc, char *argv[])
{
  //ensure command line argument gives name of config file
  if (argc != 2){
    qCritical("usage: \n  display <config_file.py>");
    return 1;
  }
  QString configFile = argv[1];

  //Initialize Python with the config file specified
  Py_Initialize();
  QString pyInitCommand =
    "import sys;"
    "sys.path.append('.');"
    "import display;"
    "display.init('"+configFile+"');";
  PyRun_SimpleString(pyInitCommand.toAscii());

  //initialize Qt
  QApplication a(argc, argv);
  MainWindow mainWin;
  mainWin.show();
//  mainWin.showFullScreen();


  //run the main window loop
  // calling python update logic within the timer in the main window
  return a.exec();
}



//******************************************************************
//Qt Class for handling the main window
//******************************************************************

MainWindow::MainWindow() {
  //TODO, dynamically create frames as specified in config file
  this->web1 = new QWebView(this);
  this->web2 = new QWebView(this);

  //setup the main timer that periodically makes calls to the python logic
  // and determines what should be reloaded
  timer = new QTimer(this);
  connect(timer, SIGNAL(timeout()), this, SLOT(updateTimer()));
  timer->start(10000);
  updateTimer();
}


void MainWindow::resizeEvent(QResizeEvent* event) {
  //TODO: handle different display layouts
  int width  = this->size().width()/2;
  int height = this->size().height();
  web1->setGeometry(0,0,width,height);
  web2->setGeometry(width,0,width,height);
}


void MainWindow::updateTimer(){
  //have the python script run its update logic
  PyObject* moduleStr   = PyString_FromString((char*)"display");
  PyObject* module      = PyImport_Import(moduleStr);
  PyObject* dispUpdate  = PyObject_GetAttrString(module,(char*)"update");

  PyObject* args        = PyTuple_Pack(1,PyInt_FromLong(0));
  PyObject* result      = PyObject_CallObject(dispUpdate, args);
  const char* s = PyString_AsString(result);
  web1->load(QUrl(s));

  args        = PyTuple_Pack(1,PyInt_FromLong(1));
  result      = PyObject_CallObject(dispUpdate, args);
  s = PyString_AsString(result);
  web2->load(QUrl(s));

  //TODO: redo this to work with arbitrary number of frames
}
