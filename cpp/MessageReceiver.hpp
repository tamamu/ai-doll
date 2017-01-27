#include <QObject>
#include <QUdpSocket>
#include <QVector>
#include <QFont>

#include "Message.hpp"
#include "DollSettings.hpp"

#include "DollBody.hpp"

class MessageReceiver : public QObject
{
	Q_OBJECT

public:
  MessageReceiver(DollSettings *settings);
  QVector<Message> messages;
  void toggle();

private slots:
  void receive();

protected:

private:
	DollSettings *settings;
  QFont *font;
  bool isBadge;
  QUdpSocket *socket;
  DollBody *body;
  
  void showMessage();
  void deleteMessages();
  void parseMessage();
  void modelLoad(QString path);
  
  

};
