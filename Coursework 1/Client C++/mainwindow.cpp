#include "mainwindow.h"
#include "ui_mainwindow.h"






MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    // НАЧАЛО







    // Инициализируем второе окно
    window = new registerWindow(); //
    // подключаем к слоту запуска главного окна по кнопке во втором окне
    connect(window, &registerWindow::firstWindow, this, &MainWindow::show); //

    // Инициализируем третье окно
        windowWork = new workWindow(); //quitToMainWindow
//    // подключаем к слоту запуска главного окна по кнопке во втором окне
//                qDebug() << "no connect";
        connect(window, SIGNAL(WorkSWindow()), windowWork, SLOT(DopenAndApply())); //                                // ..&workWindow::show
        // Инициализируем третье окно
//            windowWork = new workWindow(); //quitToMainWindow
    //    // подключаем к слоту запуска главного окна по кнопке во втором окне

//        qDebug() << "Pochti connect";
        connect(this, SIGNAL(goToWork()), windowWork, SLOT(DopenAndApply())); //                                // ..&workWindow::show
//        qDebug() << "END connect";


    window->setWindowTitle("Регистрация");
     windowWork->setWindowTitle("Парсер");
    this->setWindowTitle("Авторизация");
//    windowWork = new workWindow(); //quitToMainWindow
// подключаем к слоту запуска главного окна по кнопке во втором окне
//connect(window,  SIGNAL(WorkSWindow), this, SLOT(registerAcc)); //




    // Инициализируем выход окно
    // подключаем к слоту запуска главного окна по кнопке во втором окне
    connect(windowWork, &workWindow::quitToMainWindow, this, &MainWindow::show); //


    // Создаем объект менеджера
    manager = new QNetworkAccessManager(this);



   // Проверка на авторизованность

    //Чтение данный из файла
     QSettings settings ("settings.ini",QSettings::IniFormat);
     settings.beginGroup("Hash");

     QString hash = settings.value("hash").toString();
     QString login = settings.value("login").toString();
     QString hash_time = settings.value("hash_time").toString();
     settings.endGroup();

//     qDebug() <<hash  << " # "<< login << " # " << hash_time << "\n";

    if (time(NULL) - 60*60*24*30 < hash_time.toDouble()){ // Если срок годности месяц
        // берем адрес введенный в текстовое поле
        QUrl url("http://127.0.0.1:5000/checkauth");

        // создаем объект для запроса
        QNetworkRequest request(url);

        request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
        qDebug() <<"HASH"<< hash;
        QJsonObject objObject;
        objObject.insert("login",login);
        objObject.insert("hash", hash);
        objObject.insert("hash_time", hash_time);


        QJsonDocument doc(objObject);
        QByteArray data = doc.toJson();


        // Выполняем запрос, получаем указатель на объект
        // ответственный за ответ
        QNetworkReply* reply=  manager->post(request,data);


        // Подписываемся на сигнал о готовности загрузки
        connect( reply, SIGNAL(finished()),
                 this, SLOT(replyFinishedCH()) );


    }



// Тут все команды
   // connect(windowWork, &workWindow::quitToMainWindow, this, &MainWindow::show); //
    // Тут все команды из  всех окон собраны, и к каждому сигналу присваивается фнукция,


    // Ниже перечислить слоты-функции в которых будет проходить отправка запроса и их обработка

    // Значит тут нужно подключить winsock, т к отсюда идет отправка
}

MainWindow::~MainWindow()
{
    delete ui;
}




void MainWindow::on_pushButton_clicked() // Регистрация окно
{
   window->show(); //
   this->close(); //
}



void MainWindow::on_enter_btn_clicked() // Войти внутрь
{


//    if (ui->login_inp->text().size() < 4){
//        ui->msg_info2->setText("Логин менее 4-х символов");
//        return;
//    }

//    if (ui->passw_inp->text().size() < 6 and ui->passw_inp_2->text().size() < 6){
//        ui->msg_info2->setText("Пароль менее 6 символов");
//        return;
//    }


//    if(ui->passw_inp->text() != ui->passw_inp_2->text()){
//        ui->msg_info2->setText("Пароли не совпадают");
//        return;
//    }



    // берем адрес введенный в текстовое поле
    QUrl url("http://127.0.0.1:5000/login");

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
             this, SLOT(replyFinished()) );

    //    windowWork->show(); //
    //    this->close(); //
//    windowWork->show(); //
//    this->close(); //
}




void MainWindow::replyFinished() // Вызывается по завершению
{
    QNetworkReply *reply= qobject_cast<QNetworkReply *>(sender());

    if (reply->error() == QNetworkReply::NoError)
    {
        QByteArray content= reply->readAll();
        qDebug() << "ОТВЕТ логин" << content;
      // Получаем содержимое ответа

      // Выводим результат
      QByteArray st102 = "102";
      QByteArray st103 = "103";
      if (content.data() == st102 or content.data() == st103){
          ui->msg_info_1->setText("Неверные данные." );

      }else{
              ui->msg_info_1->setText( "Успешная авторизация" );


               // Кеширование
              //Запись в файл Хеша авторизации
                QSettings settings("settings.ini",QSettings::IniFormat);
                QString hash = content.data();
                qDebug() << "setHASH"<< hash;
                double hash_time = time (NULL);

                settings.beginGroup("Hash");
                settings.setValue( "login", ui->login_inp->text());
                settings.setValue( "hash", hash);
                settings.setValue("hash_time",hash_time);
                settings.endGroup();
//                windowWork->show(); //
                emit goToWork();
                this->close(); //

  //content.data()  hash
      }

    }
    else{
      // Выводим описание ошибки, если она возникает.
      ui->msg_info_1->setText(reply->errorString());
//      ui->msg_info_1->setText("Server Error");
    }

    // разрешаем объекту-ответа "удалится"
    reply->deleteLater();
}



void MainWindow::replyFinishedCH() // Вызывается по завершению
{
    QNetworkReply *reply= qobject_cast<QNetworkReply *>(sender());

    if (reply->error() == QNetworkReply::NoError)
    {
      // Получаем содержимое ответа
      QByteArray content= reply->readAll();
      // Выводим результат
      QByteArray st104 = "104";
      QByteArray st105 = "105";
      QByteArray st106 = "106";
      QString Go = "Go";

      if (content.data() == st104 or content.data() == st105 or content.data() == st106){
        // Токен не валиден

            ui->msg_info_1->setText(content.data());
      }else if(content.data() == Go){
          // Обновить на сервере время хеша

              ui->msg_info_1->setText( "Успешная авторизация" );


               // Кеширование
              //Запись в файл Хеша авторизации
                QSettings settings("settings.ini",QSettings::IniFormat);
                double hash_time = time (NULL);
                settings.beginGroup("Hash");
                settings.setValue("hash_time",hash_time);
                settings.endGroup();

                // Переход к основному окну
//                windowWork->show(); //
                this->close(); //
                emit goToWork();

      }

    }
    else{
      // Выводим описание ошибки, если она возникает.
      ui->msg_info_1->setText(reply->errorString());
//      ui->msg_info_1->setText("Server Error");
    }

    // разрешаем объекту-ответа "удалится"
    reply->deleteLater();
}








