#include "DollBody.hpp"



DollBody::DollBody(MessageReceiver *parent)
{
	this->parent = parent;
	this->offset = new QPoint(0, 0);
	this->setWindowFlags(Qt::FramelessWindowHint | Qt::WindowStaysOnTopHint | Qt::Tool);
	this->setAttribute(Qt::WA_TranslucentBackground);
	this->setAttribute(Qt::WA_ShowWithoutActivating);
	this->fadeAnime = new QPropertyAnimation();
	this->fadeAnime->setTargetObject(this);
  this->fadeAnime->setPropertyName("windowOpacity");
  this->fadeAnime->setDuration(150);
}

void DollBody::setImage(QString filename)
{
	this->image = new QImage(filename);
	QPixmap pixmap = QPixmap::fromImage(*this->image);
	QBitmap mask = pixmap.mask();
	this->setFixedSize(pixmap.width(), pixmap.height());
	this->setMask(mask);
}

void DollBody::sortMessages()
{
  QVector<MessageView*> fixed;
  QVector<MessageView*> nonfixed;
  for (QVector<MessageView*>::iterator it = this->messages.begin(); it != this->messages.end(); ++it){
    if ((*it)->data->type == Fixed) {
      fixed << *it;
    } else {
      nonfixed << *it;
    }
  }
  fixed.append(nonfixed);
  this->messages = fixed;
  for (int i=0; i < this->messages.size(); ++i){
    this->messages[i]->cnt = i;
  }
}

void DollBody::openAnimation()
{
	this->fadeAnime->setStartValue(0.0);
  this->fadeAnime->setEndValue(1.0);
  this->fadeAnime->start();
}


void DollBody::closeAnimation()
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

void DollBody::paintEvent(QPaintEvent *event)
{
	QPainter painter(this);
	painter.drawImage(0, 0, *this->image);
}

void DollBody::mousePressEvent(QMouseEvent *event)
{
	*this->offset = event->pos();
}

void DollBody::mouseMoveEvent(QMouseEvent *event)
{
	QPoint diff = event->pos() - *this->offset;
	QPoint newpos = this->pos() + diff;
	this->move(newpos);
}