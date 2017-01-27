#include "DollSettings.hpp"

/** @def
 * Model data directory name.
 */
#define MODELS_DIR "models"

/** @def
 * Model file name.
 */
#define MODEL_FILE "model"

DollSettings::DollSettings(QString appdir, QString path)
{
  this->appDir = appdir;
  JsonLoadResult settings = this->loadJson(appdir, path);
  if (settings.scope == None) {
		std::cerr << "Settings file not found: settings.json" << std::endl;
		exit(1);
	}
  this->settings = settings;

  QString modelName = this->getModelName();
	JsonLoadResult model = this->loadJson(appdir, QString(MODELS_DIR)+"/"+modelName+"/"+MODEL_FILE);
	if (model.scope == None) {
		std::cerr << "Model not found:" << modelName.toUtf8().constData() << std::endl;
		exit(1);
	}
  this->model = model;
}

QString DollSettings::getModelName()
{
  return this->settings.data.value("model").toString();
}

QString DollSettings::getBodyPath()
{
  QString modelName = this->getModelName();
  QString bodyPath;
	if (this->model.scope == User) {
		bodyPath = this->appDir + QString(MODELS_DIR)+"/"+modelName+"/"+model.data.value("body").toString();
	} else {
		bodyPath = QString(MODELS_DIR)+"/"+modelName+"/"+model.data.value("body").toString();
	}
  return bodyPath;
}

QString DollSettings::getIconPath()
{
  QString modelName = this->getModelName();
  QString iconPath;
	if (model.scope == User) {
		iconPath = this->appDir + QString(MODELS_DIR)+"/"+modelName+"/"+model.data.value("icon").toString();
	} else {
		iconPath = QString(MODELS_DIR)+"/"+modelName+"/"+model.data.value("icon").toString();
	}
  return iconPath;
}

JsonLoadResult DollSettings::loadJson(QString appdir, QString path)
{
  FileScope scope = None;
	QString userOwnedFileName = appdir + path;
	QFile file;
	if (QFile::exists(userOwnedFileName)){
		scope = User;
		file.setFileName(userOwnedFileName);
	}else if(QFile::exists(path)){
		scope = System;
		file.setFileName(path);
	}else{
		QJsonObject dummy;
		return {scope, dummy};
	}
	file.open(QIODevice::ReadOnly | QIODevice::Text);
	QString contents = file.readAll();
	file.close();
	QJsonObject obj = QJsonDocument::fromJson(contents.toUtf8()).object();
	return {scope, obj};
}