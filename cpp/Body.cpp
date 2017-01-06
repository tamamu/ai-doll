#include "Body.hpp"

Body::Body(QString filename)
{
	this->image = new QImage(filename);
	this->offset = new QPoint(0, 0);
	initUI();
}

void Body::initUI()
{
	this->setWindowFlags(Qt::FramelessWindowHint | Qt::WindowStaysOnTopHint | Qt::Tool);
	this->setAttribute(Qt::WA_TranslucentBackground);
	this->setAttribute(Qt::WA_ShowWithoutActivating);

	QPixmap pixmap = QPixmap::fromImage(*this->image);
	QBitmap mask = pixmap.mask();
	this->setFixedSize(pixmap.width(), pixmap.height());
	this->setMask(mask);
}

void Body::paintEvent(QPaintEvent *event)
{
	QPainter painter(this);
	painter.drawImage(0, 0, *this->image);
}

void Body::mousePressEvent(QMouseEvent *event)
{
	*this->offset = event->pos();
}

void Body::mouseMoveEvent(QMouseEvent *event)
{
	auto diff = event->pos() - *this->offset;
	auto newpos = this->pos() + diff;
	this->move(newpos);
}