#include <QMainWindow>
#include <QObject>
#include <QWebView>

class MainWindow : public QMainWindow
{
  Q_OBJECT

 public:
  MainWindow();

 protected:
  void resizeEvent(QResizeEvent* event) override;

 protected:
  QWebView *web1;
  QWebView *web2;

};
