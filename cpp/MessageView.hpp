#include <QWidget>
#include <QBitmap>
#include <QPainter>
#include <QMouseEvent>
#include <QLabel>
#include <QPropertyAnimation>
#include <QTimer>
#include <QGridLayout>

#include "Message.hpp"

class MessageView : public QWidget
{
	Q_OBJECT

public:
  int cnt;
  Message *data;
	MessageView(QWidget *parent, Message *data);
  void showMessage(QWidget *parent, QString message);

private slots:
  void closeAnimation();

protected:
  void enterEvent(QEvent *event);
  void leaveEvent(QEvent *event);
	void paintEvent(QPaintEvent *event);
	void mousePressEvent(QMouseEvent *event);

private:
	QWidget *parent;
  
  QLabel *label;
  QPropertyAnimation *fadeAnime;
  QPropertyAnimation *moveAnime;
  QTimer *timer;
	void initUI();
  
  /**
   * @fn
   * Mark to close the view, then remove that by parent.
   * `mousePressEvent` or `closeAnimation` calls it.
   * @brief Mark to close it.
   * @sa MessageView::mousePressEvent MessageView::closeAnimation
   */
  void close();
  
  /**
   * @fn
   * @brief Show the view with fade-in animation.
   */
  void openAnimation();
  
  void follow(QWidget *target);
  

};
