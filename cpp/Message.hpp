#pragma once
#include <QString>

enum MessageType { Plain, Fixed };

class Message {
public:
  MessageType type;
  QString id;
  QString text;
  bool isClose() {
    return this->isClosed;
  }
  void close() {
    this->isClosed = true;
  }

private:
  bool isClosed = false;
};