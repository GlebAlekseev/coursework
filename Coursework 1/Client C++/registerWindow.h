#pragma once
#ifndef REGISTERWINDOW_H
#define REGISTERWINDOW_H

#include <QDialog>
//#include "mainwindow.h"

#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>
#include <QUrl>

#include <QJsonDocument>
#include <QJsonValue>
#include <QJsonArray>
#include <QJsonObject>

#include <QSettings>

#include <ctime>
namespace Ui {
class registerWindow;
}

class registerWindow : public QDialog
{
    Q_OBJECT

public:
    explicit registerWindow(QWidget *parent = nullptr);
    ~registerWindow();

signals:
    void firstWindow(); // Сигнал для первого окна на открытие
    void WorkSWindow();
private slots:
    void on_pushButton_clicked(); // Слот-обработчик нажатия кнопки
    void on_enter_btn_clicked();

    void replyFinishedR();


private:
    Ui::registerWindow *ui;
    QNetworkAccessManager* manager;
};

#endif // REGISTERWINDOW_H
