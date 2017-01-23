#include "MessageView.hpp"

MessageView::MessageView(QWidget *parent, Message *data)
{
  this->parent = parent;
  this->data = data;
  
  this->label = new QLabel(this);
  this->cnt = 0;
  this->fadeAnime = new QPropertyAnimation(this);
  this->moveAnime = new QPropertyAnimation(this);
  this->timer = new QTimer(this);
	initUI();
}

void MessageView::initUI()
{
  this->resize(0, 64);
  this->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Fixed);
	this->setWindowFlags(Qt::FramelessWindowHint | Qt::WindowStaysOnTopHint | Qt::Tool);
	this->setAttribute(Qt::WA_TranslucentBackground);
  this->setAttribute(Qt::WA_DeleteOnClose);
	this->setAttribute(Qt::WA_ShowWithoutActivating);

	this->fadeAnime->setTargetObject(this);
  this->fadeAnime->setPropertyName("windowOpacity");
  this->fadeAnime->setDuration(150);
  
  QGridLayout *layout = new QGridLayout(this);
  this->label->setAlignment(Qt::AlignCenter);
  layout->addWidget(this->label);
  this->setLayout(layout);
  
  this->setWindowOpacity(0.0);
}

void MessageView::follow(QWidget *target)
{
  int lw = this->label->fontMetrics().boundingRect(this->label->text()).width();
  QPoint base = target->pos();
  this->move(base.x()-lw, base.y());
}

void MessageView::close()
{
  this->data->close();
//  this->parent->boxCloseEvent();
}

void MessageView::openAnimation()
{
	this->fadeAnime->setStartValue(0.0);
  this->fadeAnime->setEndValue(1.0);
  this->fadeAnime->start();
}


void MessageView::closeAnimation()
{
  this->fadeAnime = new QPropertyAnimation(this);
  this->fadeAnime->setTargetObject(this);
  this->fadeAnime->setPropertyName("windowOpacity");
  this->fadeAnime->setDuration(150);
  this->fadeAnime->setStartValue(this->windowOpacity());
  this->fadeAnime->setEndValue(0.0);
  connect(this->fadeAnime, SIGNAL(finished()), SLOT(close()));
  this->fadeAnime->start();
}

void MessageView::showMessage(QWidget *target, QString message)
{
  this->show();
  this->label->setText(message);
  this->follow(target);
  this->openAnimation();
  if (this->data->type == Fixed) {
    this->timer->singleShot(9000, this, SLOT(closeAnimation()));
  }
}

void MessageView::enterEvent(QEvent *event)
{
  this->repaint();
}

void MessageView::leaveEvent(QEvent *event)
{
  this->repaint();
}

void MessageView::paintEvent(QPaintEvent *event)
{
	QPainter painter(this);
  QRect *rect = new QRect();
  QRect box = this->rect();
  rect->setX(box.x()+5);
  rect->setY(box.y()+5);
  rect->setWidth(box.width()-10);
  rect->setHeight(box.height()-10);
  painter.setBrush(Qt::white);
  QPen *pen = new QPen();
  if (this->underMouse()) {
    pen->setColor(Qt::gray);
  } else {
    pen->setColor(Qt::black);
  }
  pen->setWidth(3);
  painter.setPen(*pen);
  painter.drawRoundedRect(*rect, 15.0, 15.0);
  painter.setPen(Qt::NoPen);
  QBrush *black = new QBrush(Qt::black);
  painter.setBrush(*black);
  QPoint points[3] = {
    QPoint(rect->x(), rect->height()/2-5+3),
    QPoint(rect->x(), rect->height()/2+5+3),
    QPoint(rect->x() - 5, rect->height()/2+3)
  };
  painter.drawPolygon(points, 3);
}

void MessageView::mousePressEvent(QMouseEvent *event)
{
  this->fadeAnime->stop();
  this->moveAnime->stop();
  this->setWindowOpacity(0.0);
  this->close();
}