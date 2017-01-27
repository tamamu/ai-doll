#pragma once
#include <iostream>
#include <QFile>
#include <QJsonDocument>
#include <QJsonObject>

/**
 * @enum FileScope
 * Kind of file path. It identify the prefix of the path.
 */
enum FileScope { None, System, User };


struct JsonLoadResult {
	FileScope scope;
	QJsonObject data;
};

class DollSettings
{

public:
  DollSettings(QString appdir, QString path);
  QString getModelName();
  QString getBodyPath();
  QString getIconPath();
  
protected:

private:
  QString appDir;
  JsonLoadResult settings;
  JsonLoadResult model;
  JsonLoadResult loadJson(QString appdir, QString path);

};
