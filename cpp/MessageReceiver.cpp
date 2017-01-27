#include "MessageReceiver.hpp"

MessageReceiver::MessageReceiver(DollSettings *settings)
{
  this->settings = settings;
  this->font = new QFont("sans", 13);
  this->isBadge = false;
  this->body = new DollBody(this);
  this->body->setImage(this->settings->getBodyPath());
  
  this->socket = new QUdpSocket(this);
  this->socket->bind(QHostAddress::LocalHost, 8000);
  connect(this->socket, SIGNAL(readyRead()), SLOT(receive()));
  
  this->body->show();
}

void MessageReceiver::toggle()
{
  if (this->isBadge) {
    this->body->openAnimation();
  } else {
    this->body->closeAnimation();
  } 
  this->isBadge = !this->isBadge;
}

void MessageReceiver::receive()
{
  
}