#include "DollBody.hpp"

DollBody::DollBody()
{
	this->offset = new QPoint(0, 0);
	this->setWindowFlags(Qt::FramelessWindowHint | Qt::WindowStaysOnTopHint | Qt::Tool);
	this->setAttribute(Qt::WA_TranslucentBackground);
	this->setAttribute(Qt::WA_ShowWithoutActivating);
}

void DollBody::setImage(QString filename)
{
	this->image = new QImage(filename);
	QPixmap pixmap = QPixmap::fromImage(*this->image);
	QBitmap mask = pixmap.mask();
	this->setFixedSize(pixmap.width(), pixmap.height());
	this->setMask(mask);
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