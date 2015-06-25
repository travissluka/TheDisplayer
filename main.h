#include <Python.h>

#include <QMainWindow>
#include <QObject>
#include <QWebView>
#include <QTimer>
#include <QList>




class MainWindow : public QMainWindow
{
  Q_OBJECT

public:
  MainWindow(PyObject* pyUpdate);

public slots:
  void updateTimer();

protected:
  void resizeEvent(QResizeEvent* event);

protected:
<<<<<<< HEAD
=======
  QList<QWebView*> webList;
  
>>>>>>> dev-travis
  QWebView* header;
  QWebView* footer;
  QWebView* center_full;
  QWebView* center_half_1;
  QWebView* center_half_2;

  QTimer *timer;

  PyObject* pyUpdate;
};
