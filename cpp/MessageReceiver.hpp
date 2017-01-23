#include <QObject>
#include <QUdpSocket>
#include <QVector>

#include "Message.hpp"
#include "DollBody.hpp"

class MessageReceiver : public QObject
{
	Q_OBJECT

public:
  MessageReceiver();
  QVector<Message> messages;
  void toggle();

private slots:
  void receive();

protected:

private:
	//DollSettings settings;
  QFont *font;
  bool isBadge;
  QUdpSocket socket;
  DollBody body;
  
  void sortByFixed();
  void showMessage();
  void deleteMessages();
  void parseMessage();
  void modelLoad(QString path);
  
  

};
