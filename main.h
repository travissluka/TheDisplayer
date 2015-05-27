#include <QMainWindow>
#include <QObject>
#include <QWebView>
#include <QTimer>

class MainWindow : public QMainWindow
{
  Q_OBJECT

public:
  MainWindow();

public slots:
  void updateTimer();

protected:
  void resizeEvent(QResizeEvent* event) override;

protected:
  QWebView *web1;
  QWebView *web2;
  QTimer *timer;

};
