#include <QDebug>
#include <QApplication>
#include <QAction>
#include <QMenu>
#include <QIcon>
#include <QSystemTrayIcon>
#include <QJsonDocument>
#include <QJsonObject>
#include <QObject>

#include "DollSettings.hpp"
#include "MessageReceiver.hpp"

/** @def
 * Settings file name.
 */
#define SETTINGS_FILE "settings.json"

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
	DollSettings *settings = new DollSettings(appDir, QString(SETTINGS_FILE));

	QString iconPath = settings->getIconPath();
	// qDebug() << iconPath;
	
	QSystemTrayIcon *trayIcon = new QSystemTrayIcon();
	trayIcon->setIcon(QIcon(iconPath));

	QMenu *menu = new QMenu();
	
	QAction *exitAction = menu->addAction("Exit");
	QObject::connect(exitAction, SIGNAL(triggered()), &app, SLOT(quit()));
	menu->addAction(exitAction);

	trayIcon->setContextMenu(menu);
	trayIcon->show();

	MessageReceiver *receiver = new MessageReceiver(settings);

	return app.exec();
}
