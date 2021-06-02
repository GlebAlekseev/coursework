#include "registerwindow.h"
#include "ui_registerwindow.h"



registerWindow::registerWindow(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::registerWindow)
{
    ui->setupUi(this);

    manager = new QNetworkAccessManager(this);
}

registerWindow::~registerWindow()
{
    delete ui;
}


void registerWindow::on_pushButton_clicked() // Смена окна
{
    ui->msg_info2->setText("");
    this->close(); // Закрываем окно
    emit firstWindow(); // И вызываем сигнал на открытие главного окна

}




void registerWindow::on_enter_btn_clicked() // Регистрация, посыл сигнала
{
//    this->close(); //


    if (ui->login_inp->text().size() < 4){
        ui->msg_info2->setText("Логин менее 4-х символов");
        return;
    }

    if (ui->passw_inp->text().size() < 6 and ui->passw_inp_2->text().size() < 6){
        ui->msg_info2->setText("Пароль менее 6 символов");
        return;
    }


    if(ui->passw_inp->text() != ui->passw_inp_2->text()){
        ui->msg_info2->setText("Пароли не совпадают");
        return;
    }




    // берем адрес введенный в текстовое поле
    QUrl url("http://127.0.0.1:5000/register");

    // создаем объект для запроса
    QNetworkRequest request(url);

    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QJsonObject objObject;
    objObject.insert("login",ui->login_inp->text());
    objObject.insert("password", ui->passw_inp->text());


    QJsonDocument doc(objObject);
    QByteArray data = doc.toJson();


    // Выполняем запрос, получаем указатель на объект
    // ответственный за ответ
    QNetworkReply* reply=  manager->post(request,data);


    // Подписываемся на сигнал о готовности загрузки
    connect( reply, SIGNAL(finished()),
             this, SLOT(replyFinishedR()) );

    //    windowWork->show(); //
    //    this->close(); //
}




void registerWindow::replyFinishedR() // Вызывается по завершению
{
  QNetworkReply *reply= qobject_cast<QNetworkReply *>(sender());

  if (reply->error() == QNetworkReply::NoError)
  {
    // Получаем содержимое ответа
    QByteArray content= reply->readAll();
    // Выводим результат
    QByteArray st101 = "101";
    if (content.data() == st101){
        ui->msg_info2->setText("Логин уже зарегестрирован." );
    }else{
            ui->msg_info2->setText( "Успешная регистрация" );

             // Кеширование
            //Запись в файл Хеша авторизации
              QSettings settings("settings.ini",QSettings::IniFormat);
              QString hash = content.data();
                double hash_time = time (NULL);

              settings.beginGroup("Hash");
//              qDebug() << "login" << ui->login_inp->text();
              settings.setValue( "login", ui->login_inp->text());
              settings.setValue( "hash", hash);
              settings.setValue("hash_time",hash_time);
              settings.endGroup();


              ui->msg_info2->setText("");
              this->close(); //
              emit WorkSWindow();
//content.data()  hash
    }

  }
  else{
    // Выводим описание ошибки, если она возникает.
//    ui->msg_info2->setText(reply->errorString());
    ui->msg_info2->setText("Server Error");
  }

  // разрешаем объекту-ответа "удалится"
  reply->deleteLater();
}
