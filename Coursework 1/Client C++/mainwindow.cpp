#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    window = new registerWindow(); //
    connect(window, &registerWindow::firstWindow, this, &MainWindow::show); //
        windowWork = new workWindow(); //quitToMainWindow
        connect(window, SIGNAL(WorkSWindow()), windowWork, SLOT(DopenAndApply())); //
        connect(this, SIGNAL(goToWork()), windowWork, SLOT(DopenAndApply())); //

    window->setWindowTitle("Регистрация");
     windowWork->setWindowTitle("Парсер");
    this->setWindowTitle("Авторизация");
    connect(windowWork, &workWindow::quitToMainWindow, this, &MainWindow::show); //
    manager = new QNetworkAccessManager(this);
     QSettings settings ("settings.ini",QSettings::IniFormat);
     settings.beginGroup("Hash");
     QString hash = settings.value("hash").toString();
     QString login = settings.value("login").toString();
     QString hash_time = settings.value("hash_time").toString();
     settings.endGroup();
    if (time(NULL) - 60*60*24*30 < hash_time.toDouble()){ // Если срок годности месяц
        // берем адрес введенный в текстовое поле
        QUrl url("http://127.0.0.1:5000/checkauth");
        QNetworkRequest request(url);
        request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
//        qDebug() <<"HASH"<< hash;
        QJsonObject objObject;
        objObject.insert("login",login);
        objObject.insert("hash", hash);
        objObject.insert("hash_time", hash_time);
        QJsonDocument doc(objObject);
        QByteArray data = doc.toJson();
        QNetworkReply* reply=  manager->post(request,data);
        connect( reply, SIGNAL(finished()),
                 this, SLOT(replyFinishedCH()) );
    }

}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_pushButton_clicked() // Регистрация окно
{
   window->show(); //
   ui->msg_info_1->setText("");
   this->close(); //
}

void MainWindow::on_enter_btn_clicked() // Войти внутрь
{

    QUrl url("http://127.0.0.1:5000/login");
    QNetworkRequest request(url);
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
    QJsonObject objObject;
    objObject.insert("login",ui->login_inp->text());
    objObject.insert("password", ui->passw_inp->text());
    QJsonDocument doc(objObject);
    QByteArray data = doc.toJson();
    QNetworkReply* reply=  manager->post(request,data);
    connect( reply, SIGNAL(finished()),
             this, SLOT(replyFinished()) );
}




void MainWindow::replyFinished() // Вызывается по завершению
{
    QNetworkReply *reply= qobject_cast<QNetworkReply *>(sender());
    if (reply->error() == QNetworkReply::NoError)
    {
        QByteArray content= reply->readAll();
//        qDebug() << "ОТВЕТ логин" << content;
      QByteArray st102 = "102";
      QByteArray st103 = "103";
      if (content.data() == st102 or content.data() == st103){
          ui->msg_info_1->setText("Неверные данные." );
      }else{
              ui->msg_info_1->setText( "Успешная авторизация" );
                QSettings settings("settings.ini",QSettings::IniFormat);
                QString hash = content.data();
//                qDebug() << "setHASH"<< hash;
                double hash_time = time (NULL);
                settings.beginGroup("Hash");
                settings.setValue( "login", ui->login_inp->text());
                settings.setValue( "hash", hash);
                settings.setValue("hash_time",hash_time);
                settings.endGroup();
                emit goToWork();
                ui->msg_info_1->setText("");
                this->close(); //
      }

    }
    else{
      ui->msg_info_1->setText(reply->errorString());
    }
    reply->deleteLater();
}



void MainWindow::replyFinishedCH() // Вызывается по завершению
{
    QNetworkReply *reply= qobject_cast<QNetworkReply *>(sender());

    if (reply->error() == QNetworkReply::NoError)
    {
      QByteArray content= reply->readAll();
      QByteArray st104 = "104";
      QByteArray st105 = "105";
      QByteArray st106 = "106";
      QString Go = "Go";

      if (content.data() == st104 or content.data() == st105 or content.data() == st106){
            ui->msg_info_1->setText(content.data());
      }else if(content.data() == Go){
              ui->msg_info_1->setText( "Успешная авторизация" );
                QSettings settings("settings.ini",QSettings::IniFormat);
                double hash_time = time (NULL);
                settings.beginGroup("Hash");
                settings.setValue("hash_time",hash_time);
                settings.endGroup();
                ui->msg_info_1->setText("");
                this->close(); //
                emit goToWork();

      }

    }
    else{
      ui->msg_info_1->setText(reply->errorString());
    }
    reply->deleteLater();
}








