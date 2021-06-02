#ifndef WORKWINDOW_H
#define WORKWINDOW_H

#include <QDialog>
#include <QStandardItemModel>

#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>
#include <QUrl>

#include <QJsonDocument>
#include <QJsonValue>
#include <QJsonArray>
#include <QJsonObject>
#include <QScrollBar>

#include <QSettings>
#include <ctime>
#include <QDesktopServices>

#include <QTimer>
#include <QTableWidget>

#include <QCheckBox>
namespace Ui {
class workWindow;
}

class workWindow : public QDialog
{
    Q_OBJECT

public:
    explicit workWindow(QWidget *parent = nullptr);
    ~workWindow();

    QJsonDocument doc;
    QJsonDocument docT;
    int PAGE_SEARCH = 1;
    int MAX_PAGE_SEARCH = 1;

    int HOWMUCH;

    bool SORTAZ = true;
    bool SORT12 = true;
    bool SHOPW = true;
    bool SHOPD = true;
    bool SHOPM = true;

    int PAGE_TRACKED= 1;
    int MAX_PAGE_TRACKED = 1;
    bool TSORTAZ = true;
    bool TSORT12 = true;

    bool TSHOPW = true;
    bool TSHOPD = false;
    bool TSHOPM = true;

    QWidget* CURRENT_TRACKED_WIDGET = nullptr;
    QWidget* CURRENT_SEARCH_WIDGET = nullptr;
    QJsonValue CURRENT_TRACKED_docIn=0;
    QJsonValue CURRENT_SEARCH_docIn=0;


    QVariant STYLE_COLOR_W= "red";
    QVariant STYLE_COLOR_E = "green";
    QVariant STYLE_COLOR_M = "purple";

    int page_per_time = 60;
    QString isi;
    QVector <QNetworkReply*>connects_img;
    QVector <QPushButton*>connects_btn;
    QVector <QPushButton*>connects_btnTrckd;


    QVector <QCheckBox*> connects_chBox;
    QVector <QCheckBox*> connects_chBoxTrckd;

    QVector <QPushButton*>connects_btnOpen;
    QVector <QPushButton*>connects_btnOpenT;
    QPixmap local_pr;


//    QVector<QNetworkReply*> connects_img;

signals:
    void WorkSWindow(); // Сигнал для первого окна на открытие
    void quitToMainWindow();
//    void finish_img();


private slots:
    void on_Quit_clicked();


    void on_change_pw_btn_clicked();
    void replyFinishedChange();


    void DopenAndApply();

    void on_go_main_s_clicked();
    void result_search();
    void result_get_tracked();

    void DrawSearch();
    void DrawTracked();

    void on_next___clicked();

    void on_back___clicked();
    void replyFinished_img(QObject*,QString,bool,bool is_bl = false); // ,QObject img

    void clear_connects_img();


    bool eventFilter(QObject *obj, QEvent *event);

    void draw_rBlock(QJsonValue docIn,QWidget*,bool clear);
    void add_product(QJsonValue,QWidget* body_);
    void delete_product(QJsonValue,QWidget* body_);
    void send_trackInfo(QJsonValue docIn,QWidget* body_);
    void clear_connects_btn(QWidget* body_);
    void is_tracking(QJsonValue mid);
    void set_connectOnBtn(QJsonValue docIn,QString body_,QString);

    void result_get_history(QObject*,QObject* table);
    void send_to_Tracked();
    void result_tracking(QObject*,QString,QJsonValue docIn);

    void change_tracking(bool,QJsonValue docIn,bool,QObject*);
//    void go_connectAdd(QPushButton* btn_add_,QJsonValue docIn,QWidget* body_);

    void on_t_back__clicked();

    void on_t_next__clicked();

private:
    Ui::workWindow *ui;
    QStringList myList;
    QStandardItemModel *model;
    QNetworkAccessManager* manager;



};

#endif // WORKWINDOW_H
