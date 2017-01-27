#pragma once
#include <QWidget>
#include <QBitmap>
#include <QPainter>
#include <QMouseEvent>
#include <QVector>

#include "MessageView.hpp"

class MessageReceiver;

class DollBody : public QWidget
{
	Q_OBJECT

public:
	DollBody(MessageReceiver *parent);
	void setImage(QString filename);
	void sortMessages();
	void openAnimation();
	void closeAnimation();

private slots:

protected:
	void paintEvent(QPaintEvent *event);
	void mousePressEvent(QMouseEvent *event);
	void mouseMoveEvent(QMouseEvent *event);

private:
	MessageReceiver *parent;
	QImage *image;
	QPoint *offset;
	QVector<MessageView*> messages;
	QPropertyAnimation *fadeAnime;
	void dropMessages();
	
};
