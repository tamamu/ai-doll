#include "MessageReceiver.hpp"

MessageReceiver::MessageReceiver()
{
  this->font = new QFont("sans", 13);
  this->isBadge = false;
  this->body = new DollBody(this);
  
  this->socket = new QUdpSocket(this);
  this->socket->bind(QHostAddress::LocalHost, "8000");
  connect(this->socket, SIGNAL(readyRead()), SOCKET(reveive()));
  
  this->body->show();
}

void MessageReceiver::toggle()
{
  if (this.isBadge) {
    this->body->openAnimation();
  } else {
    this->body->closeAnimation();
  } 
  this->isBadge = !this.isBadge;
}

void MessageReceiver::sortByFixed()
{
  QVector<MessageView> fixed;
  QVector<MessageView> nonfixed;
  for (QVector<Message>::iterator it = this->messages.begin(); it != this->messages.end(); ++it){
    if (it->type == Fixed) {
      fixed << *it;
    } else {
      nonfixed << *it;
    }
  }
  fixed.append(nonfixed);
  this->messages = fixed;
  for (int i=0; i < this->messages.size(); ++i){
    this->messages.at(i)->cnt = i;
  }
}

void MessageReceiver::receive()
{
  
}