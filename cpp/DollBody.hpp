#include <QWidget>
#include <QBitmap>
#include <QPainter>
#include <QMouseEvent>
#include <QVector>

#include "MessageView.hpp"

class DollBody : public QWidget
{
	Q_OBJECT

public:
	DollBody();
	void setImage(QString filename);

private slots:

protected:
	void paintEvent(QPaintEvent *event);
	void mousePressEvent(QMouseEvent *event);
	void mouseMoveEvent(QMouseEvent *event);

private:
	QImage *image;
	QPoint *offset;
	QVector<MessageView> messages;
	void dropMessages();
	
};
