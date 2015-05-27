//Code not to be read by Ning Zeng, so no other comments will be inserted
#include <QApplication>
#include <QUrl>
#include <QObject>
#include "main.h"

int main(int argc, char *argv[])
{
  QApplication a(argc, argv);
  MainWindow mainWin;
  mainWin.showFullScreen();
  return a.exec();
}



MainWindow::MainWindow() {
  //TODO, dynamically create frames as specified in config file
  this->web1 = new QWebView(this);
  this->web2 = new QWebView(this);

  //TODO: set timer to interface with python script to do all the logic
  web1->load(QUrl("http://www.atmos.umd.edu"));
  web2->load(QUrl("http://www.atmos.umd.edu/~gcm"));
}



void MainWindow::resizeEvent(QResizeEvent* event) {
  web1->setGeometry(0,0,this->size().width()/2,this->size().height());
  web2->setGeometry(960,0,960,1080);
}
