#include <QDebug>
#include <QApplication>
#include <QAction>
#include <QMenu>
#include <QIcon>
#include <QSystemTrayIcon>
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

	MessageReceiver *receiver = new MessageReceiver(settings);

	QString iconPath = settings->getIconPath();
	// qDebug() << iconPath;
	
	QSystemTrayIcon *trayIcon = new QSystemTrayIcon();
	trayIcon->setIcon(QIcon(iconPath));
	//connect(trayIcon, SIGNAL(activated(QSystemTrayIcon::ActivationReason)), &app, SLOT(receiver->(QSystemTrayIcon::ActivationReason)));

	QMenu *menu = new QMenu();
	
	QAction *exitAction = menu->addAction("Exit");
	QObject::connect(exitAction, SIGNAL(triggered()), &app, SLOT(quit()));
	menu->addAction(exitAction);

	trayIcon->setContextMenu(menu);
	trayIcon->show();

	

	return app.exec();
}
