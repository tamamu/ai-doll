#include <QWidget>
#include <QBitmap>
#include <QPainter>
#include <QMouseEvent>

class Body : public QWidget
{
	Q_OBJECT

public:
	Body(QString filename);

private slots:

protected:
	void paintEvent(QPaintEvent *event);
	void mousePressEvent(QMouseEvent *event);
	void mouseMoveEvent(QMouseEvent *event);

private:
	QImage *image;
	QPoint *offset;
	void initUI();
	
};
