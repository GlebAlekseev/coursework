#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "registerwindow.h"
#include "workwindow.h"







QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_pushButton_clicked();
    void on_enter_btn_clicked();
    void replyFinished(); // cлот, выполняемый при завершении запроса
    void replyFinishedCH();

signals:
    void goToWork();


private:
    Ui::MainWindow *ui;
    registerWindow *window;

    workWindow *windowWork;
    QNetworkAccessManager* manager;
};
#endif // MAINWINDOW_H
