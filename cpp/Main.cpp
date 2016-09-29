#include <iostream>
#include <QDebug>
#include <QApplication>
#include <QAction>
#include <QMenu>
#include <QIcon>
#include <QFile>
#include <QSystemTrayIcon>
#include <QJsonDocument>
#include <QJsonObject>
#include <QObject>

#include "Body.hpp"


#define SETTINGS_FILE "settings.json"
#define MODELS_DIR "models"
#define MODEL_FILE "model"


enum FileScope { None, System, User };
struct DataLoadResult {
	FileScope scope;
	QJsonObject data;
};

DataLoadResult loadAppData(QString appdir, QString path)
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

int main(int argc, char **argv)
{
	QApplication app (argc, argv);
#if defined(Q_OS_WIN)
	QString appDir = QString::fromUtf8(qgetenv("APPDATA").append("\\AIDoll\\"));
#else
	QString appDir = QString::fromUtf8(qgetenv("HOME").append("/.config/ai-doll/"));
#endif

	//  Load settings file
	//
	DataLoadResult settings = loadAppData(appDir, QString(SETTINGS_FILE));
	if (settings.scope == None) {
		std::cerr << "Settings file not found: settings.json" << std::endl;
		exit(1);
	}

	//	Load model file
	//
	QString modelName = settings.data.value("model").toString();
	DataLoadResult model = loadAppData(appDir, QString(MODELS_DIR)+"/"+modelName+"/"+MODEL_FILE);
	if (model.scope == None) {
		std::cerr << "Model not found:" << modelName.toUtf8().constData() << std::endl;
		exit(1);
	}
	
	// Read badge path for tray icon
	//
	QString badgePath, bodyPath;
	if (model.scope == User) {
		badgePath = appDir + QString(MODELS_DIR)+"/"+modelName+"/"+model.data.value("badge").toString();
		bodyPath = appDir + QString(MODELS_DIR)+"/"+modelName+"/"+model.data.value("body").toString();
	} else {
		badgePath = QString(MODELS_DIR)+"/"+modelName+"/"+model.data.value("badge").toString();
		bodyPath = QString(MODELS_DIR)+"/"+modelName+"/"+model.data.value("body").toString();
	}

	qDebug() << badgePath;
	
	QSystemTrayIcon *trayIcon = new QSystemTrayIcon();
	trayIcon->setIcon(QIcon(badgePath));

	QMenu *menu = new QMenu();
	
	QAction *exitAction = menu->addAction("Exit");
	QObject::connect(exitAction, SIGNAL(triggered()), &app, SLOT(quit()));
	menu->addAction(exitAction);

	trayIcon->setContextMenu(menu);
	trayIcon->show();

	Body *body = new Body(bodyPath);
	body->show();

	return app.exec();
}
