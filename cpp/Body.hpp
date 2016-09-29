#include <QWidget>
#include <QBitmap>
#include <QPainter>

class Body : public QWidget
{
	Q_OBJECT

public:
	Body(QString filename);

private slots:

protected:
	void paintEvent(QPaintEvent *event);

private:
	QImage *image;
	void initUI();
	
};
