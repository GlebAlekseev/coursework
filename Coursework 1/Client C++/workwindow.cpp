#include "workwindow.h"
#include "ui_workwindow.h"





workWindow::workWindow(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::workWindow)
{
    ui->setupUi(this);
    manager = new QNetworkAccessManager(this);


    connect(ui->select_page_2,static_cast<void(QSpinBox::*)(int)>(&QSpinBox::valueChanged),this,[=](){PAGE_SEARCH = ui->select_page_2->value();DrawSearch();});



    connect(ui->tsearch_request_,&QLineEdit::textChanged,this,[=](){PAGE_SEARCH = ui->select_page_2->value();send_to_Tracked();});


    ui->text_down_4->setText("из 1");
    ui->t_text_down_4->setText("из 1");
    ui->select_page_2->setValue(1);
    ui->find_count_lbl->setText("Найдено: 0");

//    model = new QStandardItemModel(5,2,this);
//    ui->select_page_2->setValue(PAGE_SEARCH);
//    ui->text_down_4->setText(QString::number(PAGE_SEARCH));
//    text_down_4

//    ui->tableView->setModel(model);
//    QModelIndex index;
//    for(int row = 0; row<model->rowCount();++row){
//        for(int col = 0;col<model->columnCount();++col){
//            index = model->index(row,col);
//            model->setData(index,0);

//        }

//    }
//    model->setHeaderData(0,Qt::Horizontal,"x");
//    model->setHeaderData(1,Qt::Horizontal,"y");
    QPixmap pic2("://img_pos//p_def.jpg");
    QSize PicSize(40, 60);
    pic2 = pic2.scaled(PicSize,Qt::KeepAspectRatio);

//    ui->img_1_->setPixmap(pic2);
//    ui->img_2_->setPixmap(pic2);/**/

    QPixmap pic3("://img_pos//p_def.png");
    QSize PicSize3(100, 100);
    pic3 = pic3.scaled(PicSize3,Qt::KeepAspectRatio);

    ui->img_r->setPixmap(pic3);
    ui->img_r->setProperty("styleSheet",QVariant("margin-left:40px;"));
    ui->t_img_r_2->setPixmap(pic3);
    ui->t_img_r_2->setProperty("styleSheet",QVariant("margin-left:40px;"));


connect(ui->open_group,&QPushButton::clicked,this,[=](){QDesktopServices::openUrl(QUrl("https://vk.com/club204853055"));});


//    ui->img_r_2->setPixmap(pic3);
        local_pr.load(":/img_pos/p_def.png");

// общие данные на поиск, и прошлого запроса, обновляются каждый раз когда проходит поиск
    // Страница которую нужно отрисовать



        QPixmap pic4("://img_pos//rightarrow.png");
        QSize Pic4Size(40, 40);
        pic4 = pic4.scaled(Pic4Size,Qt::KeepAspectRatio);
//        ui->img_1_->setPixmap(pic2);
    ui->add__1->setPixmap(pic4);



    QLinearGradient linearGrad(QPointF(100, 100), QPointF(200, 200));
     linearGrad.setColorAt(0, Qt::black);
     linearGrad.setColorAt(1, Qt::white);

//       ui->add__1->set

    ui->add__1->setProperty("styleSheet",QVariant("vertical-align: middle;border-radius:5px;padding-left:20px;background-color: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5,stop: 0 #F3F6FB, stop: 1 #FFFFFF);"));
//        ui->add__1->installEventFilter(this);
//        ui->add__1->setAttribute("QEvent::Enter");



    QPixmap pic12("://img_pos//sort12.png");
    QSize pic_12(25, 25);
    pic12 = pic12.scaled(pic_12,Qt::KeepAspectRatio);
    ui->sort12->setPixmap(pic12);
    ui->tsort12_->setPixmap(pic12);

    QPixmap picAZ("://img_pos//sortAZ.png");
    QSize pic_AZ(25, 25);
    picAZ = picAZ.scaled(pic_AZ,Qt::KeepAspectRatio);
    ui->sortAZ->setPixmap(picAZ);
    ui->tsortAZ_->setPixmap(picAZ);

    if (SHOPW){
        QPixmap picW("://img_pos//w_logo_light.png");
        QSize pic_W(80, 100);
        picW = picW.scaled(pic_W,Qt::KeepAspectRatio);
        ui->w_l->setPixmap(picW);
        ui->tw_l_->setPixmap(picW);
    }else{
        QPixmap picW("://img_pos//w_logo_dark.png");
        QSize pic_W(80, 100);
        picW = picW.scaled(pic_W,Qt::KeepAspectRatio);
        ui->w_l->setPixmap(picW);
        ui->tw_l_->setPixmap(picW);
    }

    if (SHOPD){
        QPixmap picD("://img_pos//dns_logo_light.png");
        QSize pic_D(80, 100);
        picD = picD.scaled(pic_D,Qt::KeepAspectRatio);
        ui->d_s->setPixmap(picD);
        ui->td_s_->setPixmap(picD);
    }else{
        QPixmap picD("://img_pos//dns_logo_dark.png");
        QSize pic_D(80, 100);
        picD = picD.scaled(pic_D,Qt::KeepAspectRatio);
        ui->d_s->setPixmap(picD);
        ui->td_s_->setPixmap(picD);

    }
    if (SHOPM){
        QPixmap picM("://img_pos//ms_logo_light.png");
        QSize pic_M(80, 100);
        picM = picM.scaled(pic_M,Qt::KeepAspectRatio);
        ui->m_l->setPixmap(picM);
        ui->tm_l_->setPixmap(picM);

    }else{
        QPixmap picM("://img_pos//ms_logo_dark.png");
        QSize pic_M(80, 100);
        picM = picM.scaled(pic_M,Qt::KeepAspectRatio);
        ui->m_l->setPixmap(picM);
        ui->tm_l_->setPixmap(picM);

    }




    foreach(auto *item,ui->scrollAreaWidgetContents_2->children()){
    //   qDebug() << item;
        QString name_item= item->objectName();
        /*name_item.contains("body__", Qt::CaseInsensitive)*/; // если содержит подстроку body, если нужный элемент.
        if (name_item.contains("body__", Qt::CaseInsensitive)){
            // скрываем элемент

    //        item->setProperty("maximumHeight",QVariant(0));
               item->setProperty("visible",QVariant(false));}}

send_to_Tracked();




    ui->not_found_lbl->setProperty("visible",QVariant(true));
    ui->tnot_found_lbl_->setProperty("visible",QVariant(true));

//    qDebug()<<ui->verticalWidget->children();

    foreach(auto *item,ui->verticalWidget->children()){
        if(!item->objectName().contains("img")){
       item->setProperty("visible",QVariant(false));
        }
    }
    foreach(auto *item,ui->verticalWidget_2->children()){
        if(!item->objectName().contains("img")){
       item->setProperty("visible",QVariant(false));
        }

    }

       ui->sortAZ->installEventFilter(this);
       ui->sort12->installEventFilter(this);
       ui->m_l->installEventFilter(this);
       ui->w_l->installEventFilter(this);
       ui->d_s->installEventFilter(this);


       ui->tsortAZ_->installEventFilter(this);
       ui->tsort12_->installEventFilter(this);
       ui->tm_l_->installEventFilter(this);
       ui->tw_l_->installEventFilter(this);
       ui->td_s_->installEventFilter(this);

       QUrl url("http://127.0.0.1:5000/get_parse_page");
       QNetworkRequest request(url);
       request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
       QSettings settings ("settings.ini",QSettings::IniFormat);
       settings.beginGroup("Hash");
       QString login = settings.value("login").toString();
       settings.endGroup();
       QJsonObject objObject;
       objObject.insert("login",login);
       QJsonDocument doc(objObject);
       QByteArray data = doc.toJson();
       QNetworkReply* reply=  manager->post(request,data);

       connect(
           reply,&QNetworkReply::finished,this, [=]() {
                            QNetworkReply *reply= qobject_cast<QNetworkReply *>(sender());
                            QByteArray content= reply->readAll();
                            ui->page_parse->setText(QString(content.data()));HOWMUCH = content.toInt();});





//       page_parse


//       ui->w_style->setText(STYLE_COLOR_W.toString());
//       ui->m_style->setText(STYLE_COLOR_M.toString());
//       ui->e_style->setText(STYLE_COLOR_E.toString());
       connect(ui->page_parse,&QLineEdit::textChanged,this,[=](){
           if(ui->page_parse->text().count() !=0){
        QUrl url("http://127.0.0.1:5000/set_parse_page");
        QNetworkRequest request(url);
        request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
        QSettings settings ("settings.ini",QSettings::IniFormat);
        settings.beginGroup("Hash");
        QString login = settings.value("login").toString();
        settings.endGroup();
        QJsonObject objObject;
        objObject.insert("login",login);
        objObject.insert("count",ui->page_parse->text());
        QJsonDocument doc(objObject);
        QByteArray data = doc.toJson();
        QNetworkReply* reply=  manager->post(request,data);}
        HOWMUCH = ui->page_parse->text().toInt();
       });


       QUrl url_("http://127.0.0.1:5000/get_style");
       QNetworkRequest request_(url_);
       request_.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");



       QJsonObject objObject_;
       objObject_.insert("login",login);
       QJsonDocument doc_(objObject_);
       QByteArray data_ = doc_.toJson();
       QNetworkReply* replys=  manager->post(request_,data_);
       connect(replys,&QNetworkReply::finished,this, [=]() {
           QNetworkReply *repl= qobject_cast<QNetworkReply *>(sender());
           QByteArray content= repl->readAll();
           QJsonDocument doc = QJsonDocument::fromJson(content);
           qDebug() << "!!!!!!!!!!!" << doc;
           if(doc[0].toString().count() != 0){
              STYLE_COLOR_W = doc[0].toString();
               ui->w_style->setText(STYLE_COLOR_W.toString());
           }
           if(doc[1].toString().count() != 0){
              STYLE_COLOR_M = doc[1].toString();
                       ui->m_style->setText(STYLE_COLOR_M.toString());;
           }
           if(doc[2].toString().count() != 0){
              STYLE_COLOR_E = doc[2].toString();
              ui->e_style->setText(STYLE_COLOR_E.toString());
           }



           ////////////////////////////////////////


           connect(ui->w_style,&QLineEdit::textChanged,this,[=](){
               STYLE_COLOR_W = ui->w_style->text();
               STYLE_COLOR_M = ui->m_style->text();
               STYLE_COLOR_E = ui->e_style->text();
            QUrl url("http://127.0.0.1:5000/set_style");
            QNetworkRequest request(url);
            request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
            QSettings settings ("settings.ini",QSettings::IniFormat);
            settings.beginGroup("Hash");
            QString login = settings.value("login").toString();
            settings.endGroup();
            QJsonObject objObject;
            objObject.insert("login",login);
            objObject.insert("wild",ui->w_style->text());
            objObject.insert("mshop",ui->m_style->text());
            objObject.insert("eldorado",ui->e_style->text());
            QJsonDocument doc(objObject);
            QByteArray data = doc.toJson();
            QNetworkReply* reply=  manager->post(request,data);

           });

           connect(ui->m_style,&QLineEdit::textChanged,this,[=](){
               STYLE_COLOR_W = ui->w_style->text();
               STYLE_COLOR_M = ui->m_style->text();
               STYLE_COLOR_E = ui->e_style->text();
            QUrl url("http://127.0.0.1:5000/set_style");
            QNetworkRequest request(url);
            request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
            QSettings settings ("settings.ini",QSettings::IniFormat);
            settings.beginGroup("Hash");
            QString login = settings.value("login").toString();
            settings.endGroup();
            QJsonObject objObject;
            objObject.insert("login",login);
            objObject.insert("wild",ui->w_style->text());
            objObject.insert("mshop",ui->m_style->text());
            objObject.insert("eldorado",ui->e_style->text());
            QJsonDocument doc(objObject);
            QByteArray data = doc.toJson();
            QNetworkReply* reply=  manager->post(request,data);

           });
           connect(ui->e_style,&QLineEdit::textChanged,this,[=](){
              STYLE_COLOR_W = ui->w_style->text();
              STYLE_COLOR_M = ui->m_style->text();
              STYLE_COLOR_E = ui->e_style->text();
            QUrl url("http://127.0.0.1:5000/set_style");
            QNetworkRequest request(url);
            request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
            QSettings settings ("settings.ini",QSettings::IniFormat);
            settings.beginGroup("Hash");
            QString login = settings.value("login").toString();
            settings.endGroup();
            QJsonObject objObject;
            objObject.insert("login",login);
            objObject.insert("wild",ui->w_style->text());
            objObject.insert("mshop",ui->m_style->text());
            objObject.insert("eldorado",ui->e_style->text());
            QJsonDocument doc(objObject);
            QByteArray data = doc.toJson();
            QNetworkReply* reply=  manager->post(request,data);

           });


            connect(ui->add_link_,&QPushButton::clicked,this,[=](){
                if(ui->link_line->text().count() !=0){
                QUrl url("http://127.0.0.1:5000/add_item_to_tracking_from_link");
                QNetworkRequest request(url);
                request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
                QSettings settings ("settings.ini",QSettings::IniFormat);
                settings.beginGroup("Hash");
                QString login = settings.value("login").toString();
                settings.endGroup();
                QJsonObject objObject;
                objObject.insert("login",login);
                objObject.insert("link",ui->link_line->text());
                QJsonDocument doc(objObject);
                QByteArray data = doc.toJson();
                QNetworkReply* replys=  manager->post(request,data);
                connect(
                    replys,&QNetworkReply::finished,this, [=]() {
                                     QNetworkReply *reply= qobject_cast<QNetworkReply *>(sender());
                                     QByteArray content= reply->readAll();
                                     qDebug() << QString(content.data());
                                     if(QString(content.data()) == "212"){
                                     ui->is_add_lbl->setPlainText("Server: Ошибка");
                                     }else if(QString(content.data())=="211"){
                                     ui->is_add_lbl->setPlainText("Уже добавлено");
                                     }else if(QString(content.data())=="213"){
                                     ui->is_add_lbl->setPlainText("Неверный Mid");
                                     }else{
                                         ui->is_add_lbl->setPlainText("Добавлено: "+ QString(content.data()));
                                     }

                });}
            });





           ///////////////////////////////////////////
       });




    //add_item_to_tracking_from_link


//                      QNetworkReply *repl= qobject_cast<QNetworkReply *>(sender());
//                      QByteArray content= repl->readAll();
//                      QJsonDocument docH = QJsonDocument::fromJson(content);

                //    qDebug() << "Полученные данные" << docH;
//                      QStringList price_list = docH[0][1].toString().split( "\n" );



        QUrl url_1("http://127.0.0.1:5000/get_vkId");
        QNetworkRequest request_1(url_1);
        request_1.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");



        QJsonObject objObject_1;
        objObject_1.insert("login",login);
        QJsonDocument doc_1(objObject_1);
        QByteArray data_1 = doc_1.toJson();
        QNetworkReply* replys1=  manager->post(request_1,data_1);
        connect(replys1,&QNetworkReply::finished,this, [=]() {
            QNetworkReply *repl= qobject_cast<QNetworkReply *>(sender());
            QByteArray content= repl->readAll();

            if(QString(content.data()) !="721"){
                 ui->current_id->setText("Установален: id"+QString(content.data()));
            }else{
                 ui->current_id->setText("id не установлен");
            }



        });






                connect(ui->enter_id_vk,&QPushButton::clicked,this,[=](){
                    if(ui->inp_id->text().count() !=0){
                    QUrl url("http://127.0.0.1:5000/set_vkId");
                    QNetworkRequest request(url);
                    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
                    QSettings settings ("settings.ini",QSettings::IniFormat);
                    settings.beginGroup("Hash");
                    QString login = settings.value("login").toString();
                    settings.endGroup();
                    QJsonObject objObject;
                    objObject.insert("login",login);
                    objObject.insert("id_vk",ui->inp_id->text());
                    QJsonDocument doc(objObject);
                    QByteArray data = doc.toJson();
                    QNetworkReply* replys=  manager->post(request,data);
                    connect(
                        replys,&QNetworkReply::finished,this, [=]() {
                                         QNetworkReply *reply= qobject_cast<QNetworkReply *>(sender());
                                         QByteArray content= reply->readAll();
                                         qDebug() << QString(content.data());

                                         if(QString(content.data()) == "711"){
                                         ui->msg_im->setPlainText("Вы не выполнили условие");
                                         }else if(QString(content.data())=="710"){
                                         ui->msg_im->setPlainText("vk id сохранен");
                                         QJsonObject objObject_1;
                                         objObject_1.insert("login",login);
                                         QJsonDocument doc_1(objObject_1);
                                         QByteArray data_1 = doc_1.toJson();
                                         QNetworkReply* replys1=  manager->post(request_1,data_1);
                                         connect(replys1,&QNetworkReply::finished,this, [=]() {
                                             QNetworkReply *repl= qobject_cast<QNetworkReply *>(sender());
                                             QByteArray content= repl->readAll();

                                             if(QString(content.data()) !="721"){
                                                  ui->current_id->setText("Установален: id"+QString(content.data()));
                                             }else{
                                                  ui->current_id->setText("id не установлен");
                                             }



                                         });
                                         }


                    });}
                });





//                text_key
                QUrl url_2("http://127.0.0.1:5000/get_keyVk");
                QNetworkRequest request_2(url_2);
                request_2.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");



                QJsonObject objObject_2;
                objObject_2.insert("login",login);
                QJsonDocument doc_2(objObject_2);
                QByteArray data_2 = doc_2.toJson();
                QNetworkReply* replys2=  manager->post(request_2,data_2);
                connect(replys2,&QNetworkReply::finished,this, [=]() {
                    QNetworkReply *repl= qobject_cast<QNetworkReply *>(sender());
                    QByteArray content= repl->readAll();

                         ui->text_key->setText("Вступи в сообщество vk и напиши боту свой ключ: "+QString(content.data()));
                });
}

workWindow::~workWindow()
{
    delete ui;
}

void DrawSearch();
void cked();

void workWindow::DopenAndApply(){

    QSettings settings ("settings.ini",QSettings::IniFormat);
    settings.beginGroup("Hash");
    QString login = settings.value("login").toString();
    settings.endGroup();

    ui->name_login->setText(login);
    this->show();
}

void workWindow::on_Quit_clicked()
{

    QSettings settings("settings.ini",QSettings::IniFormat);
    settings.beginGroup("Hash");
    settings.setValue("hash_time",0);
    settings.setValue("hash",0);
    settings.setValue("login",0);
    settings.endGroup();

    this->close(); //

    emit quitToMainWindow();
}


void workWindow::on_change_pw_btn_clicked()
{

    QSettings settings ("settings.ini",QSettings::IniFormat);
    settings.beginGroup("Hash");
    QString login = settings.value("login").toString();
    settings.endGroup();
    QString curr_password = ui->curr_pw->text();
    QString new_password = ui->new_pw->text();

    QUrl url("http://127.0.0.1:5000/changepw");

    // создаем объект для запроса
    QNetworkRequest request(url);

    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QJsonObject objObject;
    objObject.insert("login",login);
    objObject.insert("curr_password", curr_password);
    objObject.insert("new_password", new_password);

    QJsonDocument doc(objObject);
    QByteArray data = doc.toJson();

    // Выполняем запрос, получаем указатель на объект
    // ответственный за ответ
    QNetworkReply* reply=  manager->post(request,data);


    // Подписываемся на сигнал о готовности загрузки
    connect( reply, SIGNAL(finished()),
             this, SLOT(replyFinishedChange()) );


    // Отправляет  из хеша логин, тек пароль, и новый пароль,
    // Сервер проверяет соответствие старого пароля к логину, изменяет пароль обновляет данные и все.


}


void workWindow::replyFinishedChange() // Вызывается по завершению
{
  QNetworkReply *reply= qobject_cast<QNetworkReply *>(sender());

  if (reply->error() == QNetworkReply::NoError)
  {
    // Получаем содержимое ответа
    QByteArray content= reply->readAll();
    // Выводим результат

    QByteArray st108 = "108";


    if (content.data() == st108){
        ui->status_change_pw->setText("Текущий пароль указан не верно." );
    }else{
        ui->status_change_pw->setText( "Пароль сменен." );

    }

  }
  else{
    // Выводим описание ошибки, если она возникает.
//    ui->msg_info2->setText(reply->errorString());
    ui->status_change_pw->setText("Server Error");
  }

  // разрешаем объекту-ответа "удалится"
  reply->deleteLater();
}



void workWindow::send_to_Tracked(){


    // Собираются критерии поиска и request
        QString request_text = ui->tsearch_request_->text();
        // отправка на сервер /search
    //    QSettings settings ("settings.ini",QSettings::IniFormat);
    //    settings.beginGroup("Hash");
    //    QString login = settings.value("login").toString();
    //    settings.endGroup();
    //    QString curr_password = ui->curr_pw->text();
    //    QString new_password = ui->new_pw->text();

        QUrl url("http://127.0.0.1:5000/get_tracked");

        // создаем объект для запроса
        QNetworkRequest request(url);

        request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");


        QSettings settings ("settings.ini",QSettings::IniFormat);
        settings.beginGroup("Hash");
        QString login = settings.value("login").toString();
        settings.endGroup();


        QJsonObject objObject;
        objObject.insert("request_text",request_text);

        objObject.insert("SORTAZ",TSORTAZ);
        objObject.insert("SORT12",TSORT12);
        objObject.insert("SHOPW",TSHOPW);
        objObject.insert("SHOPD",TSHOPD);
        objObject.insert("SHOPM",TSHOPM);
           objObject.insert("login",login);

    //    objObject.insert("request_text",request_text);   // sort
    //    objObject.insert("request_text",request_text);   // sort 2
    //    objObject.insert("request_text",request_text);   // sort 3
    //    objObject.insert("request_text",request_text);   // sort 4


        QJsonDocument doc(objObject);
        QByteArray data = doc.toJson();

        // Выполняем запрос, получаем указатель на объект
        // ответственный за ответ
        QNetworkReply* reply=  manager->post(request,data);


        // Подписываемся на сигнал о готовности загрузки
        connect( reply, SIGNAL(finished()),
                 this, SLOT(result_get_tracked()) ); // в reply результат


        // Отправляет  из хеша логин, тек пароль, и новый пароль,
        // Сервер проверяет соответствие старого пароля к логину, изменяет пароль обновляет данные и все

}

void workWindow::on_go_main_s_clicked()// Отправка запрос ана поиск из главного поиска
{
//    qDebug() <<SHOPW<< SHOPD << SHOPM;



// Собираются критерии поиска и request
    QString request_text = ui->search_request_->text();
    ui->go_main_s->setEnabled(false);
    // отправка на сервер /search
//    QSettings settings ("settings.ini",QSettings::IniFormat);
//    settings.beginGroup("Hash");
//    QString login = settings.value("login").toString();
//    settings.endGroup();
//    QString curr_password = ui->curr_pw->text();
//    QString new_password = ui->new_pw->text();

    QUrl url("http://127.0.0.1:5000/search");

    // создаем объект для запроса
    QNetworkRequest request(url);

    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QJsonObject objObject;
    objObject.insert("request_text",request_text);

    objObject.insert("SORTAZ",SORTAZ);
    objObject.insert("SORT12",SORT12);
    objObject.insert("SHOPW",SHOPW);
    objObject.insert("SHOPD",SHOPD);
    objObject.insert("SHOPM",SHOPM);
    qDebug() << HOWMUCH<< "HOWMUCH HOWMUCH HOWMUCH";
    objObject.insert("HOWMUCH",HOWMUCH);

qDebug() << "HOWMUCH"<<HOWMUCH;


    QJsonDocument doc(objObject);
    QByteArray data = doc.toJson();

    // Выполняем запрос, получаем указатель на объект
    // ответственный за ответ
    QNetworkReply* reply=  manager->post(request,data);


    // Подписываемся на сигнал о готовности загрузки
    connect( reply, SIGNAL(finished()),
             this, SLOT(result_search()) ); // в reply результат


    // Отправляет  из хеша логин, тек пароль, и новый пароль,
    // Сервер проверяет соответствие старого пароля к логину, изменяет пароль обновляет данные и все.
}
void workWindow::result_get_tracked(){
    QNetworkReply *reply= qobject_cast<QNetworkReply *>(sender());
    if (reply->error() == QNetworkReply::NoError)
    {
      QByteArray content= reply->readAll();
      docT = QJsonDocument::fromJson(content);
        PAGE_TRACKED = 1;
        ui->t_select_page_->setValue(PAGE_TRACKED);
        MAX_PAGE_TRACKED = docT.array().count()/60+1;
        ui->t_select_page_->setRange(1,MAX_PAGE_TRACKED);
        QString main_fnd = "Найдено: " +QString::number(docT.array().count());
         ui->t_find_count_lbl_->setText(main_fnd);
        // отдельная функция которая работает с данными, после сортировки ставит PAGE_SEARCH = 1 // 0 - default mode  // Может принимать сортировку А-Z Z-A 1 - 100 100 -1, по разным полям
        DrawTracked(); // просто отрисовывает главный поиск
        // ЗАПУСТИТЬ ОТРИСОВЩИК

    }
    else{
//      ui->status_change_pw->setText("Server Error");
    }
    reply->deleteLater();
}



void workWindow::result_search(){

    QNetworkReply *reply= qobject_cast<QNetworkReply *>(sender());

    if (reply->error() == QNetworkReply::NoError)
    {
      // Получаем содержимое ответа
      QByteArray content= reply->readAll();
      // Выводим результат


//      qDebug() << content;

      doc = QJsonDocument::fromJson(content);
//       QString tmp = doc[0][1].toString() ; // doc содержит ве позиции
//      foreach (const auto & value, doc.object())
//                  {

//              qDebug() << value;
//      }
//qDebug() << doc.array().count() ;



      // Есть глоб переменная отвечающая за страницу, есть функция которая получает страницу, и парсит ее используя переданные данные

      // стрелки это отдельные слоты, по нажатию выполняется функция а внутри вызывается функция отрисовки, туда передастся проитерированное PAGE_S и, как передать данные... Вынести doc в хэдэр, а тут порсто присваивать.

//      foreach (const auto & value, doc.array())
//                  {

//              qDebug() << value;
//      }
        PAGE_SEARCH = 1;
        ui->select_page_2->setValue(PAGE_SEARCH);
        MAX_PAGE_SEARCH = doc.array().count()/60+1;
        ui->select_page_2->setRange(1,MAX_PAGE_SEARCH);
        QString main_fnd = "Найдено: " +QString::number(doc.array().count());
         ui->find_count_lbl->setText(main_fnd);
        // отдельная функция которая работает с данными, после сортировки ставит PAGE_SEARCH = 1 // 0 - default mode  // Может принимать сортировку А-Z Z-A 1 - 100 100 -1, по разным полям
        DrawSearch(); // просто отрисовывает главный поиск
        // ЗАПУСТИТЬ ОТРИСОВЩИК




//        qDebug() << ui->scrollAreaWidgetContents_2->children();





//          QVariant  root= doc[0][1].toArray();
//        qDebug() << doc[0]["brand"] ;
//        qDebug() << doc[0][1] ;
//        qDebug() << doc[0][1][0] ;


       // Итак, цель построить список из 10 позиций, начало
//       QLabel *nwpos = new QLabel("ОЧередная позиция");
//           ui->scrollAreaWidgetContents_2->insertWidget(nwpos);
    //

       // Структура интерфейса, удалить теккущий мусор

       //Цикл по данным
//       for(int i = 10;i<60;i++){
//           QString ty = "bodyi"+QString::number(i);
//            ui->ty->setMaximumHeight(0);
//           //
//       }

//       QList<QWidget> list = scrollAreaWidgetContents_2;
//       foreach(QPushBtton *x, list) {
//         qDebug() << x->text() << x->metaObject()->className();
//       }
//    ui->body_i01->setMaximumHeight(0);




    }
    else{
      // Выводим описание ошибки, если она возникает.
  //    ui->msg_info2->setText(reply->errorString());
      ui->status_change_pw->setText("Server Error");
    }

    // разрешаем объекту-ответа "удалится"
    reply->deleteLater();

}



void workWindow::DrawTracked(){
    ui->tnot_found_lbl_->setProperty("visible",QVariant(false));
//    qDebug() <<docT;
//        ui->tnot_found_lbl_->setProperty("visible",QVariant(false));
        clear_connects_img();
        ui->t_next_->setEnabled(true);
        ui->t_back_->setEnabled(true);
        if(PAGE_TRACKED >= MAX_PAGE_TRACKED){
            ui->t_next_->setEnabled(false);
        }
        if(PAGE_TRACKED <= 1){
            ui->t_back_->setEnabled(false);
        }

// используя данные и страниц PAGE_SEARCH, делает провреку

int i_begin = (PAGE_TRACKED-1)*page_per_time; // page_per_time = 60
int i_end = PAGE_TRACKED*page_per_time;
qDebug() << "PAGGGG" << PAGE_TRACKED << page_per_time << i_begin << i_end;


 setUpdatesEnabled(false);
// прячем все body


qDebug() << "DRAWTRACKED";
foreach(auto *item,ui->scrollAreaWidgetContents_t->children()){
    qDebug() << "every child";
//   qDebug() << item;
    QString name_item= item->objectName();
    /*name_item.contains("body__", Qt::CaseInsensitive)*/; // если содержит подстроку body, если нужный элемент.
    if (name_item.contains("body", Qt::CaseInsensitive)){
        // скрываем элемент

//        item->setProperty("maximumHeight",QVariant(0));


           item->setProperty("visible",QVariant(false));
               ui->tnot_found_lbl_->setProperty("visible",QVariant(false));
            item->setProperty("styleSheet",QVariant("background-color: #F3F6FB;"));

            foreach(auto *itemD,item->children()){
                  if(itemD->objectName().contains("name", Qt::CaseInsensitive)){
//                      connect(
//                                      itemD,clicked(),this, [=]() { this->replyFinished_img(sender()); }
//                                  );

                    }
                  if(itemD->objectName().contains("img", Qt::CaseInsensitive)){


                    }
                  if(itemD->objectName().contains("cost", Qt::CaseInsensitive)){

//                      itemD->installEventFilter(this);

                    }
                  if(itemD->objectName().contains("add", Qt::CaseInsensitive)){

                      itemD->installEventFilter(this);
                      itemD->setProperty("styleSheet",QVariant("border:none;vertical-align: middle;border-radius:5px;padding-left:20px;background-color: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5,stop: 0 #F3F6FB, stop: 1 #FFFFFF);"));

                  }

                  }
//            connect(
//                item,clicked(),this, [=]() { this->replyFinished_img(sender()); }
//            );




           //заменить каждое имг на соурс картинку

          foreach(auto *itemD,item->children()){
                if(itemD->objectName().contains("img", Qt::CaseInsensitive)){
                    QLabel *labelX = findChild<QLabel *>(itemD->objectName());
                    labelX->setProperty("pixmap",QVariant(local_pr));
//                    itemD->setProperty(
                    labelX->setScaledContents(true);
                    labelX->setFixedSize(60,60);
                }
           }



//        qDebug() << "процесс";
    }
}

//ui->scrollAreaWidgetContents_2->scroll(0,0);
// update();
setUpdatesEnabled(true);
 repaint();
// setUpdatesEnabled(false);

//ui->scrollAreaWidgetContents_2->set
ui->bgitems_3->verticalScrollBar()->setValue(0);

//disconnect(networkManager,&QNetworkReply::finished,this, [=]() { this->replyFinished_img(sender(),itemIn->objectName());

    ui->t_text_down_4->setText(QString::number(docT.array().count()/60 +1));

// заполняем body
//qDebug() << ui-> AreaWidgetContents_2->children();
//     qDebug() << i_begin << i_end << doc.array().size() << "SIZES";
// Прячем все позиции maxh = 0
int counter_block = 1;


    if(0>=docT.array().size()){
    ui->tnot_found_lbl_->setProperty("visible",QVariant(true));
    }
qDebug()<<"se1" << i_begin << i_end;
for(int i = 0;i<docT.array().size();i++) {

    if(i>=i_begin and i_end>i){// если входит в диапазон
    qDebug() << i << counter_block;

        // прохожусь циклом и ищу боди под counter

//qDebug() <<counter_block << "counter_block" ;
        foreach(auto *item,ui->scrollAreaWidgetContents_t->children()){
            QString name_item= item->objectName();
            QString def_text= "t_body__";
            QString inc_text = QString::number(counter_block);
             def_text.append(inc_text);


            if (name_item == def_text){ // Если нужная позиция
                // скрываем элемент
//                item->setProperty("maximumHeight",QVariant(80));
   item->setProperty("visible",QVariant(true));
//                    item->setProperty("maximumHeight",QVariant(80));

             QString df = docT[i][0].toString();
//             qDebug() << "df" << df;
            if (df.contains("M_iD", Qt::CaseInsensitive)){
             item->setProperty("styleSheet",QVariant("background-color:#F3F6FB;border-left: 3px solid "+STYLE_COLOR_M.toString()+";"));
            }else if(df.contains("E_iD", Qt::CaseInsensitive)){
            item->setProperty("styleSheet",QVariant("background-color:#F3F6FB;border-left: 3px solid "+STYLE_COLOR_E.toString()+";"));

            }else if(df.contains("W_iD", Qt::CaseInsensitive)){
            item->setProperty("styleSheet",QVariant("background-color:#F3F6FB;border-left: 3px solid "+STYLE_COLOR_W.toString()+";"));

            }




                // Пройтись по наследникам и каждому заменить текст на doc

                foreach(auto *itemIn,item->children()){

                    if(itemIn->objectName().contains("add", Qt::CaseInsensitive)){

                            itemIn->setProperty("styleSheet",QVariant("border: none;"));

                            QPixmap pic4("://img_pos//rightarrow.png");
                            QSize Pic4Size(40, 40);
                            pic4 = pic4.scaled(Pic4Size,Qt::KeepAspectRatio);

//                            ui->img_1_->setPixmap(pic2);

                        QLabel *body_ = findChild<QLabel *>(itemIn->objectName());
                        body_->setPixmap(pic4);

                        QLinearGradient linearGrad(QPointF(100, 100), QPointF(200, 200));
                         linearGrad.setColorAt(0, Qt::black);
                         linearGrad.setColorAt(1, Qt::white);

                    //       ui->add__1->set

                        body_->setProperty("styleSheet",QVariant("border:none;vertical-align: middle;border-radius:5px;padding-left:20px;background-color: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5,stop: 0 #F3F6FB, stop: 1 #FFFFFF);"));






                    }
                    else if(itemIn->objectName().contains("brand", Qt::CaseInsensitive)){

                    }
                    else if(itemIn->objectName().contains("name", Qt::CaseInsensitive)){
                        QString df = docT[i][1].toString();
                        df.append(" / ");
                        df.append(docT[i][2].toString());
//                        df.append(" / ");
//                        df.append(doc[i]["url_img"].toString());
//                        df.append(" / ");
//                        df.append(doc[i]["url_profile"].toString());
//                        df.append(" / ");
//                        df.append(doc[i]["id"].toString());


                        itemIn->setProperty("plainText",QVariant(df));
                         itemIn->setProperty("styleSheet",QVariant("border:none;text-align:center;vertical-align: middle;padding-top: 5px;padding-left:10px;max-width=400px;"));

//                        qDebug() << "text" << doc[i]["name"];
                    }
                    else if(itemIn->objectName().contains("cost", Qt::CaseInsensitive)){
//                        qDebug() << "cost " << doc[i]["price"].toString();
//                        qDebug() << "cost " << doc[i]["price"].toString().toDouble();
//                        qDebug() << "cost = " <<docT[i][3].toDouble();
                        itemIn->setProperty("plainText",QVariant(QString::number(docT[i][3].toDouble()).append(" ₽")));

                        QTextEdit *cost_ = findChild<QTextEdit *>(itemIn->objectName());
                        cost_->setAlignment(Qt::AlignRight);

                    }
                    else if(itemIn->objectName().contains("comments", Qt::CaseInsensitive)){

                    }
                    else if(itemIn->objectName().contains("img", Qt::CaseInsensitive)){
                        itemIn->setProperty("styleSheet",QVariant("border: none;margin-left:10px;"));
                        QString nm = docT[i][4].toString();
                        QUrl url(nm); // url
//                        QNetworkAccessManager* networkManager = new QNetworkAccessManager(this);
                        QNetworkRequest request(url);
//                        request.setRawHeader("Content-Type", "image");



                        request.setHeader(QNetworkRequest::ContentTypeHeader, "image");
                        QNetworkReply*  networkManager=  manager->get(request);


//                        qDebug() << itemIn->metaObject();
//                        qDebug() <<itemIn << "До";


                        isi = itemIn->objectName();




//                        connect(networkManager,
//                                    SIGNAL(finished()),
//                                    this,
//                                    SLOT(replyFinished_img())); // ,itemIn

//                        connect(networkManager,&QNetworkReply::finished, this, &workWindow::replyFinished_img); // ,itemIn
//                        QVector <QNetworkReply*>connects_img;

                        connects_img.append(networkManager);
                        connect(
                            networkManager,&QNetworkReply::finished,this, [=]() { this->replyFinished_img(sender(),itemIn->objectName(),false); }
                        );
//                        networkManager->disconnect();

                        // соединить коннект с лямбой
//                        connect(
//                            this,workWindow::finish_img(),this, [=]() {}
//                        );


                        // добавить дисконнет который срабатывает если выполняется сигнал, смена страницы


//                        [](double a, double b) {
//                              return (a + b);
//                            }



                    }
                    else if(itemIn->objectName().contains("rating", Qt::CaseInsensitive)){

                    }
                    else if(itemIn->objectName().contains("sale", Qt::CaseInsensitive)){

                    }

                }

//                qDebug() << "процесс";
            }
        }
        counter_block++;



        // отображаю позицию и заполняю данными из doc
        // коунтерблок символизирует позицию

        //maxh=80
    }else{
        continue;
    }

}

}











































void workWindow::DrawSearch(){
//    qDebug() << "doc"<<doc;

        ui->not_found_lbl->setProperty("visible",QVariant(false));
        clear_connects_img();
        ui->next__->setEnabled(true);
        ui->back__->setEnabled(true);
        if(PAGE_SEARCH >= MAX_PAGE_SEARCH){
            ui->next__->setEnabled(false);
        }
        if(PAGE_SEARCH <= 1){
            ui->back__->setEnabled(false);
        }

// используя данные и страниц PAGE_SEARCH, делает провреку

int i_begin = (PAGE_SEARCH-1)*page_per_time; // page_per_time = 60
int i_end = PAGE_SEARCH*page_per_time;

 setUpdatesEnabled(false);
// прячем все body



foreach(auto *item,ui->scrollAreaWidgetContents_2->children()){
//   qDebug() << item;
    QString name_item= item->objectName();
    /*name_item.contains("body__", Qt::CaseInsensitive)*/; // если содержит подстроку body, если нужный элемент.
    if (name_item.contains("body__", Qt::CaseInsensitive)){
        // скрываем элемент

//        item->setProperty("maximumHeight",QVariant(0));


           item->setProperty("visible",QVariant(false));
               ui->not_found_lbl->setProperty("visible",QVariant(false));
            item->setProperty("styleSheet",QVariant("background-color: #F3F6FB;"));

            foreach(auto *itemD,item->children()){
                  if(itemD->objectName().contains("name", Qt::CaseInsensitive)){
//                      connect(
//                                      itemD,clicked(),this, [=]() { this->replyFinished_img(sender()); }
//                                  );

                    }
                  if(itemD->objectName().contains("img", Qt::CaseInsensitive)){


                    }
                  if(itemD->objectName().contains("cost", Qt::CaseInsensitive)){

//                      itemD->installEventFilter(this);

                    }
                  if(itemD->objectName().contains("add", Qt::CaseInsensitive)){

                      itemD->installEventFilter(this);
                      itemD->setProperty("styleSheet",QVariant("border:none;vertical-align: middle;border-radius:5px;padding-left:20px;background-color: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5,stop: 0 #F3F6FB, stop: 1 #FFFFFF);"));

                  }

                  }
//            connect(
//                item,clicked(),this, [=]() { this->replyFinished_img(sender()); }
//            );




           //заменить каждое имг на соурс картинку

          foreach(auto *itemD,item->children()){
                if(itemD->objectName().contains("img", Qt::CaseInsensitive)){
                    QLabel *labelX = findChild<QLabel *>(itemD->objectName());
                    labelX->setProperty("pixmap",QVariant(local_pr));
//                    itemD->setProperty(
                    labelX->setScaledContents(true);
                    labelX->setFixedSize(60,60);
                }
           }



//        qDebug() << "процесс";
    }
}

//ui->scrollAreaWidgetContents_2->scroll(0,0);
// update();
setUpdatesEnabled(true);
 repaint();
// setUpdatesEnabled(false);

//ui->scrollAreaWidgetContents_2->set
ui->bgitems_2->verticalScrollBar()->setValue(0);


//disconnect(networkManager,&QNetworkReply::finished,this, [=]() { this->replyFinished_img(sender(),itemIn->objectName());

    ui->text_down_4->setText(QString::number(doc.array().count()/60 +1));

// заполняем body
//qDebug() << ui->scrollAreaWidgetContents_2->children();
//     qDebug() << i_begin << i_end << doc.array().size() << "SIZES";
// Прячем все позиции maxh = 0
int counter_block = 1;


    if(0>=doc.array().size()){
    ui->not_found_lbl->setProperty("visible",QVariant(true));
    ui->go_main_s->setEnabled(true);
    }

for(int i = 0;i<doc.array().size();i++) {
    if(i>=i_begin and i_end>i){// если входит в диапазон


        // прохожусь циклом и ищу боди под counter

//qDebug() <<counter_block << "counter_block" ;
        foreach(auto *item,ui->scrollAreaWidgetContents_2->children()){
            QString name_item= item->objectName();
            QString def_text= "body__";
            QString inc_text = QString::number(counter_block);
             def_text.append(inc_text);


            if (name_item == def_text){ // Если нужная позиция
                // скрываем элемент
//                item->setProperty("maximumHeight",QVariant(80));
   item->setProperty("visible",QVariant(true));
//                    item->setProperty("maximumHeight",QVariant(80));

             QString df = doc[i]["Mid"].toString();
            if (df.contains("M_iD", Qt::CaseInsensitive)){
             item->setProperty("styleSheet",QVariant("background-color:#F3F6FB;border-left: 2px solid "+STYLE_COLOR_M.toString()+";"));
            }else if(df.contains("E_iD", Qt::CaseInsensitive)){
            item->setProperty("styleSheet",QVariant("background-color:#F3F6FB;border-left: 2px solid "+STYLE_COLOR_E.toString()+";"));

            }else if(df.contains("W_iD", Qt::CaseInsensitive)){
            item->setProperty("styleSheet",QVariant("background-color:#F3F6FB;border-left: 2px solid "+STYLE_COLOR_W.toString()+";"));

            }




                // Пройтись по наследникам и каждому заменить текст на doc

                foreach(auto *itemIn,item->children()){

                    if(itemIn->objectName().contains("add", Qt::CaseInsensitive)){

                            itemIn->setProperty("styleSheet",QVariant("border: none;"));

                            QPixmap pic4("://img_pos//rightarrow.png");
                            QSize Pic4Size(40, 40);
                            pic4 = pic4.scaled(Pic4Size,Qt::KeepAspectRatio);

//                            ui->img_1_->setPixmap(pic2);

                        QLabel *body_ = findChild<QLabel *>(itemIn->objectName());
                        body_->setPixmap(pic4);

                        QLinearGradient linearGrad(QPointF(100, 100), QPointF(200, 200));
                         linearGrad.setColorAt(0, Qt::black);
                         linearGrad.setColorAt(1, Qt::white);

                    //       ui->add__1->set

                        body_->setProperty("styleSheet",QVariant("border:none;vertical-align: middle;border-radius:5px;padding-left:20px;background-color: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5,stop: 0 #F3F6FB, stop: 1 #FFFFFF);"));






                    }
                    else if(itemIn->objectName().contains("brand", Qt::CaseInsensitive)){

                    }
                    else if(itemIn->objectName().contains("name", Qt::CaseInsensitive)){
                        QString df = doc[i]["name"].toString();
                        df.append(" / ");
                        df.append(doc[i]["brand"].toString());
//                        df.append(" / ");
//                        df.append(doc[i]["url_img"].toString());
//                        df.append(" / ");
//                        df.append(doc[i]["url_profile"].toString());
//                        df.append(" / ");
//                        df.append(doc[i]["id"].toString());


                        itemIn->setProperty("plainText",QVariant(df));
                         itemIn->setProperty("styleSheet",QVariant("border:none;text-align:center;vertical-align: middle;padding-top: 5px;padding-left:10px;max-width=400px;"));

//                        qDebug() << "text" << doc[i]["name"];
                    }
                    else if(itemIn->objectName().contains("cost", Qt::CaseInsensitive)){
//                        qDebug() << "cost " << doc[i]["price"].toString();
//                        qDebug() << "cost " << doc[i]["price"].toString().toDouble();
                        itemIn->setProperty("plainText",QVariant(QString::number(doc[i]["price"].toString().toDouble()).append(" ₽")));

                        QTextEdit *cost_ = findChild<QTextEdit *>(itemIn->objectName());
                        cost_->setAlignment(Qt::AlignRight);

                    }
                    else if(itemIn->objectName().contains("comments", Qt::CaseInsensitive)){

                    }
//                    else if(itemIn->objectName().contains("open_profile", Qt::CaseInsensitive)){
//                        QPixmap pic("://img_pos//open.png");
//                        QSize Size(20, 20);
//                        pic = pic.scaled(Size,Qt::KeepAspectRatio);
//                         QLabel* img = findChild<QLabel *>(itemIn->objectName());
//                        img->setPixmap(pic);
//                        itemIn->setProperty("styleSheet",QVariant("border: none;"));
//                    }
                    else if(itemIn->objectName().contains("img", Qt::CaseInsensitive)){
                        itemIn->setProperty("styleSheet",QVariant("border: none;margin-left:10px;"));
                        QString nm = doc[i]["url_img"].toString();
                        QUrl url(nm); // url
//                        QNetworkAccessManager* networkManager = new QNetworkAccessManager(this);
                        QNetworkRequest request(url);
//                        request.setRawHeader("Content-Type", "image");



                        request.setHeader(QNetworkRequest::ContentTypeHeader, "image");
                        QNetworkReply*  networkManager=  manager->get(request);


//                        qDebug() << itemIn->metaObject();
//                        qDebug() <<itemIn << "До";


                        isi = itemIn->objectName();




//                        connect(networkManager,
//                                    SIGNAL(finished()),
//                                    this,
//                                    SLOT(replyFinished_img())); // ,itemIn

//                        connect(networkManager,&QNetworkReply::finished, this, &workWindow::replyFinished_img); // ,itemIn
//                        QVector <QNetworkReply*>connects_img;

                        connects_img.append(networkManager);
                        connect(
                            networkManager,&QNetworkReply::finished,this, [=]() { this->replyFinished_img(sender(),itemIn->objectName(),false); }
                        );
//                        networkManager->disconnect();

                        // соединить коннект с лямбой
//                        connect(
//                            this,workWindow::finish_img(),this, [=]() {}
//                        );


                        // добавить дисконнет который срабатывает если выполняется сигнал, смена страницы


//                        [](double a, double b) {
//                              return (a + b);
//                            }



                    }
                    else if(itemIn->objectName().contains("rating", Qt::CaseInsensitive)){

                    }
                    else if(itemIn->objectName().contains("sale", Qt::CaseInsensitive)){

                    }

                }

//                qDebug() << "процесс";
            }
        }
        counter_block++;
        ui->go_main_s->setEnabled(true);



        // отображаю позицию и заполняю данными из doc
        // коунтерблок символизирует позицию

        //maxh=80
    }else{
        continue;
    }

}

}

qint16 get_digit(QString str){

    int number = str.split('_').last().toInt();



    return number;
}




void workWindow::add_product(QJsonValue docIn,QWidget* body_){
//    qDebug() << "addprofuct";
// отправка на сервер дока выше
qDebug() << "debug" << docIn["Mid"];


// берем адрес введенный в текстовое поле
QUrl url("http://127.0.0.1:5000/add_to_tracked");

// создаем объект для запроса
QNetworkRequest request(url);

request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

QJsonObject objObject;



QSettings settings ("settings.ini",QSettings::IniFormat);
settings.beginGroup("Hash");
QString login = settings.value("login").toString();
settings.endGroup();




objObject.insert("login",login); // логин
if(body_->objectName().contains("t_", Qt::CaseInsensitive)){
objObject.insert("Mid", docIn[0]); // MID
}else{
    objObject.insert("Mid", docIn["Mid"]); // MID
}
QJsonDocument doc(objObject);
QByteArray data = doc.toJson();
// Выполняем запрос, получаем указатель на объект
// ответственный за ответ
QNetworkReply* reply=  manager->post(request,data);
// Подписываемся на сигнал о готовности загрузки
//connect( reply, SIGNAL(finished()),
//         this, SLOT(send_trackInfo()) );
qDebug() << "AS" <<body_;
connect(
    reply,&QNetworkReply::finished,this, [=]() { this->send_trackInfo(docIn,body_); }
);



}
void workWindow::delete_product(QJsonValue docIn,QWidget* body_){
//    qDebug() << "deleteprofuct";
qDebug() << "debug" << docIn["Mid"];

QUrl url("http://127.0.0.1:5000/delete_to_tracked");

QNetworkRequest request(url);

request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

QJsonObject objObject;

QSettings settings ("settings.ini",QSettings::IniFormat);
settings.beginGroup("Hash");
QString login = settings.value("login").toString();
settings.endGroup();

objObject.insert("login",login); // логин
if(body_->objectName().contains("t_", Qt::CaseInsensitive)){
objObject.insert("Mid", docIn[0]); // MID
}else{
    objObject.insert("Mid", docIn["Mid"]); // MID
}

QJsonDocument doc(objObject);
QByteArray data = doc.toJson();

QNetworkReply* reply=  manager->post(request,data);
qDebug() << "AS" <<body_;
connect(
    reply,&QNetworkReply::finished,this, [=]() { this->send_trackInfo(docIn,body_); }
);



}






void workWindow::send_trackInfo(QJsonValue docIn,QWidget* body_){ // Вызывается по завершению

  QNetworkReply *reply= qobject_cast<QNetworkReply *>(sender());

  if (reply->error() == QNetworkReply::NoError)
  {
    // Получаем содержимое ответа
    QByteArray content= reply->readAll();
    // Выводим результат
//    qDebug() << content;
    if(content == "600"){ // Успешно добавлено
//        qDebug()<<body_ <<"need";
        // При условии что удалено или добавлено
        if(body_->objectName().contains("t_", Qt::CaseInsensitive)){
        send_to_Tracked();
//        qDebug() << body_ << "SendTRACKINFO";
        draw_rBlock(docIn,body_,true);
//        qDebug() << "CURRENTS"<<CURRENT_SEARCH_docIn <<CURRENT_SEARCH_WIDGET;
        if(docIn[0]==CURRENT_SEARCH_docIn["Mid"]){ //Если в поиске открыто то самое что удаляется из отслежки, нужно обновить
            draw_rBlock(CURRENT_SEARCH_docIn,CURRENT_SEARCH_WIDGET,false);
//            qDebug() << "RAVNO";
        }else{
//             qDebug() << "NE=RAVNO" <<docIn[0] <<CURRENT_SEARCH_docIn["Mid"] <<CURRENT_SEARCH_docIn;
        }

        }else{

            draw_rBlock(docIn,body_,false);
        }




//        draw_rBlock(docIn,body_);
        //redraw, c заменой



    }else if (content=="601"){ // Ошибка уже добавлено


    }
//    QByteArray st101 = "101";
//    if (content.data() == st101){
//        ui->msg_info2->setText("Логин уже зарегестрирован." );
//    }else{
//            ui->msg_info2->setText( "Успешная регистрация" );

//             // Кеширование
//            //Запись в файл Хеша авторизации
//              QSettings settings("settings.ini",QSettings::IniFormat);
//              QString hash = content.data();
//                double hash_time = time (NULL);

//              settings.beginGroup("Hash");
//              qDebug() << "login" << ui->login_inp->text();
//              settings.setValue( "login", ui->login_inp->text());
//              settings.setValue( "hash", hash);
//              settings.setValue("hash_time",hash_time);
//              settings.endGroup();


//              this->close(); //
//              emit WorkSWindow();
////content.data()  hash
//    }

  }
  else{
    // Выводим описание ошибки, если она возникает.
//    ui->msg_info2->setText(reply->errorString());
//    ui->msg_info2->setText("Server Error");
  }

  // разрешаем объекту-ответа "удалится"
  reply->deleteLater();
}






void workWindow::is_tracking(QJsonValue mid)
{
    // берем адрес введенный в текстовое поле
    QUrl url("http://127.0.0.1:5000/add_to_tracked");

    // создаем объект для запроса
    QNetworkRequest request(url);

    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QJsonObject objObject;



    QSettings settings ("settings.ini",QSettings::IniFormat);
    settings.beginGroup("Hash");
    QString login = settings.value("login").toString();
    settings.endGroup();




    objObject.insert("login",login); // логин
    objObject.insert("Mid", mid); // MID
    QJsonDocument doc(objObject);
    QByteArray data = doc.toJson();
    QNetworkReply* reply=  manager->post(request,data);

    // Подписываемся на сигнал о готовности загрузки
    //connect( reply, SIGNAL(finished()),
    //         this, SLOT(send_trackInfo()) );
    bool status = false;

   connect(
        reply,&QNetworkReply::finished,this, [&]()   { QByteArray st = qobject_cast<QNetworkReply *>(sender())->readAll();if(QString(st) == "601"){status=true;qDebug()<<"statusInIs"<<status;} }
    );

    // ставлю таймер на 10 сек, из connect передается сигнал, тут ождиается, как получен таймер уходит

}
//void workWindow::go_connectAdd(QPushButton* btn_add_,QJsonValue docIn,QWidget* body_){
//    connect(btn_add_,&QPushButton::clicked,this,[=]() {add_product(docIn,body_);}); //add_product(docIn,body_);
//    connects_btn.append(btn_add_);

//}

void workWindow::set_connectOnBtn(QJsonValue docIn,QString body_s,QString btn_add_s ){
//        qDebug() <<"$$$"<<docIn<<body_s<<btn_add_s;
//    connect(btn_add_,&QPushButton::clicked,this,[=]() {add_product(docIn,body_);});
//    connects_btn.append(btn_add_);
//    is_tracking();
//    qDebug() << "find string" << body_s;
    QWidget* body_ = findChild<QWidget *>(body_s);
//    qDebug() << "body_ find"<<body_ ;
    QPushButton* btn_add_ = findChild<QPushButton *>(btn_add_s);

    QUrl url("http://127.0.0.1:5000/add_to_tracked");
    QNetworkRequest request(url);
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
    QJsonObject objObject;
    QSettings settings ("settings.ini",QSettings::IniFormat);
    settings.beginGroup("Hash");
    QString login = settings.value("login").toString();
    settings.endGroup();




    objObject.insert("status_",true); // логин
    objObject.insert("login",login); // логин

    if(body_s.contains("t_", Qt::CaseInsensitive)){
    objObject.insert("Mid", docIn[0]); // MID
    }else{
        objObject.insert("Mid", docIn["Mid"]); // MID
    }
    QJsonDocument doc(objObject);
    QByteArray data = doc.toJson();
    QNetworkReply* reply=  manager->post(request,data);

    // Подписываемся на сигнал о готовности загрузки
    //connect( reply, SIGNAL(finished()),
    //         this, SLOT(send_trackInfo()) );
//    qDebug() << "connect add" << btn_add_ << body_s << body_;
   connect(
        reply,&QNetworkReply::finished,this, [=]()   { QByteArray st = qobject_cast<QNetworkReply *>(sender())->readAll();
                                                       if(QString(st) == "601"){
//                                                           qDebug() << "connect delete";
                                                           btn_add_->setText("Не отслеживать");
                                                           connect(btn_add_,&QPushButton::clicked,this,[=]() {delete_product(docIn,body_);}); //add_product(docIn,body_);

                                                           if(body_s.contains("t_", Qt::CaseInsensitive)){

                                                               connects_btnTrckd.append(btn_add_);
                                                           }else{
                                                               connects_btn.append(btn_add_);
                                                           }
                                                       }else if(QString(st) == "600"){
//                                                            qDebug() << "connect add";
//                                                            go_connectAdd(btn_add_,docIn,body_);
                                                            btn_add_->setText("Отслеживать");
                                                            connect(btn_add_,&QPushButton::clicked,this,[=]() {add_product(docIn,body_);}); //add_product(docIn,body_);
                                                            if(body_s.contains("t_", Qt::CaseInsensitive)){

                                                                connects_btnTrckd.append(btn_add_);
                                                            }else{
                                                                connects_btn.append(btn_add_);
                                                            }
                                                       } });






















};

void workWindow::result_get_history(QObject* sender,QObject* table){
    QNetworkReply *reply= qobject_cast<QNetworkReply *>(sender);
    if (reply->error() == QNetworkReply::NoError)
    {
      QByteArray content= reply->readAll();
      QJsonDocument docH = QJsonDocument::fromJson(content);

//    qDebug() << "Полученные данные" << docH;
      QStringList price_list = docH[0][1].toString().split( "\n" );
      QStringList time_list = docH[0][2].toString().split( "\n" );

//      qDebug() <<"price"<< price_list;
//      qDebug() <<"time"<< time_list;




    QTableWidget *TableW = findChild<QTableWidget *>(table->objectName());
        if(content == "801"){
//            qDebug() << "ПУСТО";
        }else{
//            qDebug() << "Таблица есть";

            for(size_t i = 0;i<price_list.count();i++){
//                qDebug() << "i = "<< i;
                TableW->setColumnCount(2);
                TableW->setRowCount(price_list.count());

                QDateTime t;
                t.setSecsSinceEpoch(time_list[i].toDouble());
                int f= price_list[i].toFloat();
//                qDebug() << f;
                QTableWidgetItem *newItem1 = new QTableWidgetItem(QString::number(f) + " ₽");
                TableW->setItem(i,1,newItem1);
                QTableWidgetItem *newItem2 = new QTableWidgetItem(t.toString("dd-MM-yy HH:mm"));
                TableW->setItem(i,0,newItem2);
                TableW->setHorizontalHeaderItem(0,new QTableWidgetItem("Дата"));
                TableW->setHorizontalHeaderItem(1,new QTableWidgetItem("Цена"));

                TableW->setStyleSheet("QHeaderView::section {background-color:#BDF5FF;color:#190012;}");

            }


        }

    }
    else{
//      ui->status_change_pw->setText("Server Error");
    }
    reply->deleteLater();

}

void workWindow::draw_rBlock(QJsonValue docIn,QWidget* body_,bool clear = false){
    qDebug() << "DRAW_RBLOCK";
//    qDebug() << "clear"<< clear << body_;
    clear_connects_btn(body_);
    if(clear){

        foreach(auto *item,ui->verticalWidget_2->children()){
            item->setProperty("visible",QVariant(false));
        }
        return;
    }
//    qDebug() << "fin clear/" << docIn<<body_;


    qDebug() << "DRAW_RBLOC2K";
    QWidget *widg = findChild<QWidget *>(body_->objectName());
//                QPalette colr;
//                colr.setColor();
//                widg->setPalette();
    QVariant stly = widg->styleSheet() + "background-color: #C7FCFF;";

    body_->setProperty("styleSheet",stly);
    // отрисовывает правую часть
//    qDebug() << docIn;
//qDebug()<<ui->verticalWidget->children();
qDebug() << "DRAW_RBLOCK3";
if(!body_->objectName().contains("t_",Qt::CaseInsensitive)){
    foreach(auto *item,ui->verticalWidget->children()){
        if(!item->objectName().contains("brnd_imge", Qt::CaseInsensitive) and !item->objectName().contains("cst_full", Qt::CaseInsensitive)
                 and !item->objectName().contains("sale", Qt::CaseInsensitive)){
        item->setProperty("visible",QVariant(true));
        }



//        qDebug() << "cikle";
        if(item->objectName().contains("add", Qt::CaseInsensitive)){
        QPushButton *btn_add_ = findChild<QPushButton *>(item->objectName());
//        qDebug()<<btn_add_;
        set_connectOnBtn(docIn,body_->objectName(),btn_add_->objectName());
        }
        else if(item->objectName().contains("brand", Qt::CaseInsensitive)){
            item->setProperty("plainText",QVariant(QString("Бренд: " + docIn["brand"].toString())));
             item->setProperty("styleSheet",QVariant("border:none;text-align:center;vertical-align: middle;padding-left:10px;"));
        }
        else if(item->objectName().contains("name", Qt::CaseInsensitive)){
            QString df = docIn["name"].toString();
            item->setProperty("plainText",QVariant(QString("Название: "+df)));
             item->setProperty("styleSheet",QVariant("border:none;text-align:center;vertical-align: middle;padding-left:10px;"));
    //                        qDebug() << "text" << doc[i]["name"];
        }
        else if(item->objectName().contains("brnd_imge", Qt::CaseInsensitive)){

             QString nm = docIn["url_brand_logo"].toString();
             item->setProperty("visible",QVariant(false));
             if (nm !=""){
                 item->setProperty("visible",QVariant(true));
             }
//             qDebug() << "@@@" << nm;
//             qDebug() << "!!!!!!!!!!!" << nm;
             QUrl url(nm); // url
             QNetworkRequest request(url);

             request.setHeader(QNetworkRequest::ContentTypeHeader, "image");
             QNetworkReply*  networkManager=  manager->get(request);
             connect(
                 networkManager,&QNetworkReply::finished,this, [=]() { this->replyFinished_img(sender(),item->objectName(),false,true); }
             );
        }
        else if(item->objectName().contains("cost", Qt::CaseInsensitive)){
                item->setProperty("plainText",QVariant(QString("Цена: "+QString::number(docIn["price"].toString().toDouble()).append(" ₽"))));

     }

        else if(item->objectName().contains("cst_full", Qt::CaseInsensitive)){
             item->setProperty("visible",QVariant(false));
            if(docIn["Mid"].toString().contains("W_iD", Qt::CaseInsensitive)){
//                if(docIn["price_full"] == 0){
//                item->setProperty("styleSheet",QVariant("color:gray;"));
//                }else{
//                item->setProperty("styleSheet",QVariant("color:black;"));
//                }



                    item->setProperty("visible",QVariant(true));
                    item->setProperty("plainText",QVariant(QString("Цена без скидки: "+QString::number(docIn["price_full"].toString().toDouble()).append(" ₽"))));
              }

       }
        else if(item->objectName().contains("sale", Qt::CaseInsensitive)){
                        item->setProperty("visible",QVariant(false));
                       if(docIn["Mid"].toString().contains("W_iD", Qt::CaseInsensitive)){
//                           if(docIn["sale"] == 0){
//                           item->setProperty("styleSheet",QVariant("color:gray;"));
//                           }else{
//                           item->setProperty("styleSheet",QVariant("color:black;"));
//                           }



                               item->setProperty("visible",QVariant(true));
                               item->setProperty("plainText",QVariant(QString("Скидка: "+QString::number(docIn["sale"].toString().toDouble()).append("%"))));
                         }


       }
        else if(item->objectName().contains("send_notifications", Qt::CaseInsensitive)){
            qDebug()<< "send norification";
            QCheckBox *chbx = findChild<QCheckBox *>(item->objectName());
            // утсановить текущее состояние
            // сделать команду гет на соединение и получить текущее состояние для пользвотаеля

            QUrl url("http://127.0.0.1:5000/tracking");
            QNetworkRequest request(url);
            request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

            QSettings settings ("settings.ini",QSettings::IniFormat);
            settings.beginGroup("Hash");
            QString login = settings.value("login").toString();
            settings.endGroup();


                QJsonObject objObject;
                objObject.insert("login",login);
                objObject.insert("Mid",docIn["Mid"]);

                objObject.insert("is_set",false);
                QJsonDocument doc(objObject);
                QByteArray data = doc.toJson();

                QNetworkReply* reply=  manager->post(request,data);
                connect(
                    reply,&QNetworkReply::finished,this, [=]() { this->result_tracking(sender(),chbx->objectName(),docIn); }
                );


        }



        else if(item->objectName().contains("tble_hist_cst", Qt::CaseInsensitive)){
            // Получаю данные, массив цена дата

            QString Mid = docIn["Mid"].toString();

            QUrl url("http://127.0.0.1:5000/get_history");

            // создаем объект для запроса
            QNetworkRequest request(url);

            request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

            QJsonObject objObject;
            objObject.insert("Mid",Mid);

            QJsonDocument doc(objObject);
            QByteArray data = doc.toJson();
            QNetworkReply* reply=  manager->post(request,data);
            connect(
                reply,&QNetworkReply::finished,this, [=]() { this->result_get_history(sender(),item); }
            );


        }
        else if(item->objectName().contains("open_r", Qt::CaseInsensitive)){
            item->setProperty("plainText",QVariant(QString("Цена: "+QString::number(docIn["price"].toString().toDouble()).append(" Р"))));

                QPushButton *btn_open_ = findChild<QPushButton *>(item->objectName());
//                QString url_o = docIn["url_profile"].toString();
            connect(btn_open_,&QPushButton::clicked,this,[=](){QDesktopServices::openUrl(QUrl(docIn["url_profile"].toString()));});
            connects_btnOpen.append(btn_open_);


        }



        else if(item->objectName().contains("img", Qt::CaseInsensitive)){
            QString nm = docIn["url_img"].toString();
            QUrl url(nm); // url
            QNetworkRequest request(url);

            request.setHeader(QNetworkRequest::ContentTypeHeader, "image");
            QNetworkReply*  networkManager=  manager->get(request);
            connect(
                networkManager,&QNetworkReply::finished,this, [=]() { this->replyFinished_img(sender(),item->objectName(),true); }
            );
            }
    }


}else{
//    qDebug() << "DOCIN"<<docIn;
    foreach(auto *item,ui->verticalWidget_2->children()){

        qDebug() << "NAME = " << item->objectName();
            if(!item->objectName().contains("brnd_imge", Qt::CaseInsensitive) and !item->objectName().contains("cst_full", Qt::CaseInsensitive)
                     and !item->objectName().contains("sale", Qt::CaseInsensitive)){
            item->setProperty("visible",QVariant(true));
            }




    //        qDebug() << "cikle";
            if(item->objectName().contains("add", Qt::CaseInsensitive)){
            QPushButton *btn_add_ = findChild<QPushButton *>(item->objectName());
    //        qDebug()<<btn_add_;
            set_connectOnBtn(docIn,body_->objectName(),btn_add_->objectName());
            }
            else if(item->objectName().contains("brand", Qt::CaseInsensitive)){
                item->setProperty("plainText",QVariant(QString("Бренд: " + docIn[2].toString())));
                 item->setProperty("styleSheet",QVariant("border:none;text-align:center;vertical-align: middle;padding-left:10px;"));
            }
            else if(item->objectName().contains("name", Qt::CaseInsensitive)){
                QString df = docIn[1].toString();
                item->setProperty("plainText",QVariant(QString("Название: "+df)));
                 item->setProperty("styleSheet",QVariant("border:none;text-align:center;vertical-align: middle;padding-left:10px;"));
        //                        qDebug() << "text" << doc[i]["name"];
            }
            else if(item->objectName().contains("brnd_imge", Qt::CaseInsensitive)){

                 QString nm = docIn[6].toString();
                 item->setProperty("visible",QVariant(false));
                 if (nm !=""){
                     item->setProperty("visible",QVariant(true));
                 }
    //             qDebug() << "@@@" << nm;
    //             qDebug() << "!!!!!!!!!!!" << nm;
                 QUrl url(nm); // url
                 QNetworkRequest request(url);

                 request.setHeader(QNetworkRequest::ContentTypeHeader, "image");
                 QNetworkReply*  networkManager=  manager->get(request);
                 connect(
                     networkManager,&QNetworkReply::finished,this, [=]() { this->replyFinished_img(sender(),item->objectName(),false,true); }
                 );
            }
            else if(item->objectName().contains("cost", Qt::CaseInsensitive)){
                qDebug() << "======docIn[3]" << QString::number(docIn[3].toDouble());
                    item->setProperty("plainText",QVariant(QString("Цена: "+QString::number(docIn[3].toDouble()).append(" ₽"))));

         }

//            else if(item->objectName().contains("cst_full", Qt::CaseInsensitive)){
//                 item->setProperty("visible",QVariant(false));
//                if(docIn[0].toString().contains("W_iD", Qt::CaseInsensitive)){
//    //                if(docIn["price_full"] == 0){
//    //                item->setProperty("styleSheet",QVariant("color:gray;"));
//    //                }else{
//    //                item->setProperty("styleSheet",QVariant("color:black;"));
//    //                }



//                        item->setProperty("visible",QVariant(true));
//                        item->setProperty("plainText",QVariant(QString("Цена без скидки: "+QString::number(docIn[3].toString().toDouble()).append(" ₽"))));
//                  }

//           }
//            else if(item->objectName().contains("sale", Qt::CaseInsensitive)){
//                            item->setProperty("visible",QVariant(false));
//                           if(docIn[0].toString().contains("W_iD", Qt::CaseInsensitive)){
//    //                           if(docIn["sale"] == 0){
//    //                           item->setProperty("styleSheet",QVariant("color:gray;"));
//    //                           }else{
//    //                           item->setProperty("styleSheet",QVariant("color:black;"));
//    //                           }



//                                   item->setProperty("visible",QVariant(true));
//                                   item->setProperty("plainText",QVariant(QString("Скидка: "+QString::number(docIn["sale"].toString().toDouble()).append("%"))));
//                             }


//           }
            else if(item->objectName().contains("send_notifications", Qt::CaseInsensitive)){
                qDebug()<< "send norification";
                QCheckBox *chbx = findChild<QCheckBox *>(item->objectName());
                // утсановить текущее состояние
                // сделать команду гет на соединение и получить текущее состояние для пользвотаеля

                QUrl url("http://127.0.0.1:5000/tracking");
                QNetworkRequest request(url);
                request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

                QSettings settings ("settings.ini",QSettings::IniFormat);
                settings.beginGroup("Hash");
                QString login = settings.value("login").toString();
                settings.endGroup();


                    QJsonObject objObject;
                    objObject.insert("login",login);
                    objObject.insert("Mid",docIn[0]);

                    objObject.insert("is_set",false);
                    QJsonDocument doc(objObject);
                    QByteArray data = doc.toJson();

                    QNetworkReply* reply=  manager->post(request,data);
                    connect(
                        reply,&QNetworkReply::finished,this, [=]() { this->result_tracking(sender(),chbx->objectName(),docIn); }
                    );

            qDebug()<< "send norification end";
            }



            else if(item->objectName().contains("tble_hist_cst", Qt::CaseInsensitive)){
                // Получаю данные, массив цена дата

                QString Mid = docIn[0].toString();

                QUrl url("http://127.0.0.1:5000/get_history");

                // создаем объект для запроса
                QNetworkRequest request(url);

                request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

                QJsonObject objObject;
                objObject.insert("Mid",Mid);

                QJsonDocument doc(objObject);
                QByteArray data = doc.toJson();
                QNetworkReply* reply=  manager->post(request,data);
                connect(
                    reply,&QNetworkReply::finished,this, [=]() { this->result_get_history(sender(),item); }
                );

                qDebug()<< "tble end";
            }
            else if(item->objectName().contains("open_r", Qt::CaseInsensitive)){
//                item->setProperty("plainText",QVariant(QString("Цена: "+docIn[3].toString().append(" Р"))));

                    QPushButton *btn_open_ = findChild<QPushButton *>(item->objectName());
    //                QString url_o = docIn[5].toString();
                connect(btn_open_,&QPushButton::clicked,this,[=](){QDesktopServices::openUrl(QUrl(docIn[5].toString()));});
                connects_btnOpenT.append(btn_open_);

                 qDebug()<< "open end";
            }



            else if(item->objectName().contains("img", Qt::CaseInsensitive)){
                QString nm = docIn[4].toString();
                QUrl url(nm); // url
                QNetworkRequest request(url);

                request.setHeader(QNetworkRequest::ContentTypeHeader, "image");
                QNetworkReply*  networkManager=  manager->get(request);
                connect(
                    networkManager,&QNetworkReply::finished,this, [=]() { this->replyFinished_img(sender(),item->objectName(),true); }
                );
                 qDebug()<< "img end";
                }
        }
    qDebug() << "end1";

            }
    qDebug() << "end2";
    }






void  workWindow::change_tracking(bool b,QJsonValue docIn,bool is_set,QObject* itemIn){
        qDebug() << "change_tracking " << b;

        QUrl url("http://127.0.0.1:5000/tracking");
        QNetworkRequest request(url);
        request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

        QSettings settings ("settings.ini",QSettings::IniFormat);
        settings.beginGroup("Hash");
        QString login = settings.value("login").toString();
        settings.endGroup();


            QJsonObject objObject;
            objObject.insert("login",login);
            if(docIn["Mid"].toString().length()==0){
                objObject.insert("Mid",docIn[0]);
            }else{
                objObject.insert("Mid",docIn["Mid"]);
            }

            objObject.insert("bool",b);


            objObject.insert("is_set",true);
            QJsonDocument doc(objObject);
            QByteArray data = doc.toJson();

            QNetworkReply* reply=  manager->post(request,data);
//            connect( reply, SIGNAL(finished()),
//                     this, SLOT(result_tracking()) ); // Получить результат если ортвет 900 то редрав // в reply результат


//            connect(
//                reply,&QNetworkReply::finished,this, [=]() { this->result_tracking(sender(),itemIn->objectName(),docIn); }
//            );


}

void workWindow::result_tracking(QObject* obj,QString objName,QJsonValue docIn){
    // получение ответ, ответ состояниея для установки или код того что уставнолено


        QNetworkReply *reply= qobject_cast<QNetworkReply *>(obj);

        if (reply->error() == QNetworkReply::NoError)
        {
            QByteArray content = reply->readAll();
            QCheckBox *chbx = findChild<QCheckBox *>(objName);
//            qDebug() << "content" << content.data();
            if(QString(content.data()) == "9010"){ // позиция нет в отслежке get
                // текст enabled false
//                qDebug() << "get_9010";
                chbx->setCheckState(Qt::Unchecked);
                 chbx->setVisible(false);
            }
            else if (QString(content.data()) == "900"){ // Успешная устанвока значени
                chbx->setVisible(true);
                qDebug() << "Установлено";

                //redraw draw_rBlock


//                if(CURRENT_SEARCH_docIn == docIn){

//                    draw_rBlock(CURRENT_SEARCH_docIn,CURRENT_SEARCH_WIDGET,false);
//                }
//                if(CURRENT_TRACKED_docIn == docIn){

//                    draw_rBlock(CURRENT_TRACKED_docIn,CURRENT_TRACKED_WIDGET,false);
//                }



            }
            else if (QString(content.data()) == "901" ){ // позиция не в отслежке set
                chbx->setVisible(false);
                qDebug() << "НЕ Установлено";
                // ничего
                // текст enabled false

            }else { // если get вернул значение
                foreach(auto *connect,connects_chBox){
            //        qDebug() << connect;
                    connect->disconnect();
                }
                connects_chBox.clear();
                // ставит текст enabled true
                chbx->setVisible(true);
               if(QString(content.data()) == "0"){
                chbx->setCheckState(Qt::Unchecked);
                qDebug() << "set value " << QString(content.data());
                connects_chBox.append(chbx);
    //            qDebug() << "connects_chBox"<<connects_chBox ;
                connect(
                    chbx,&QCheckBox::stateChanged,this, [=]() { change_tracking(chbx->checkState(),docIn,true,chbx);}); // изменяет статус по нажатию // выполняет обновление отрисовки кdrawvlock
                qDebug() << "set value end";
               }
               else if (QString(content.data()) == "1"){
                chbx->setCheckState(Qt::Checked);
                qDebug() << "set value " ;
                connects_chBox.append(chbx);
    //            qDebug() << "connects_chBox"<<connects_chBox ;
                connect(
                    chbx,&QCheckBox::stateChanged,this, [=]() { change_tracking(chbx->checkState(),docIn,true,chbx);}); // изменяет статус по нажатию // выполняет обновление отрисовки кdrawvlock
                qDebug() << "set value end";

               }

            }


        }

}


bool workWindow::eventFilter(QObject *obj, QEvent *event)
{
//    qDebug() << obj;
    if(event->type() == QEvent::MouseButtonPress)
    {
        if(obj->objectName().contains("add", Qt::CaseInsensitive)){
        //do something
        QString str = obj->objectName();

        qint16 ordObj  = get_digit(str);
//        qDebug() << "Порядок " << ordObj<< obj->objectName();

        // из obj могу получить лейбл
        // надо получить ид, для этого begin + cost__ * // получу то куда нажато, с помощью этой же цифры получу доступ к боди и сменю цвет




        int i_begin;
        int i_end;
QString stWord;
QString stWorda;
        if(obj->objectName().contains("t_", Qt::CaseInsensitive)){
//            qDebug()<<"TRACKED===============================";
            stWord = "t_body__";
            stWorda = "t_add__";
            i_begin = (PAGE_TRACKED-1)*page_per_time; // page_per_time = 60
            i_end = PAGE_TRACKED*page_per_time;

        }else{
//            qDebug() << "SEARCH================================";

            stWord = "body__";
            stWorda = "add__";
            i_begin = (PAGE_SEARCH-1)*page_per_time; // page_per_time = 60
            i_end = PAGE_SEARCH*page_per_time;
        }

        qint16 ordDoc = ordObj+i_begin-1;

        stWord.append(QString::number(ordObj));
        stWorda.append(QString::number(ordObj));
        QWidget *body_ = findChild<QWidget *>(stWord);
        QLabel *add___ = findChild<QLabel *>(stWorda);
//        qDebug() << "body___" << body_;



//        qDebug() << doc[ordDoc];


        if(obj->objectName().contains("t_", Qt::CaseInsensitive)){
//            qDebug()<<"TRACKED===============================";
            draw_rBlock(docT[ordDoc],body_);
            CURRENT_TRACKED_WIDGET = body_;
            CURRENT_TRACKED_docIn=docT[ordDoc];
        }else{
//            qDebug() << "SEARCH================================";
//            qDebug() << body_ << "SEARCH========";
            draw_rBlock(doc[ordDoc],body_);
            CURRENT_SEARCH_WIDGET = body_;
            CURRENT_SEARCH_docIn=doc[ordDoc];
        }
        qDebug() << "OOOO";


        add___->setProperty("styleSheet",QVariant("border:none;vertical-align: middle;border-radius:5px;padding-left:20px;background-color: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5,stop: 0 #C7FCFF, stop: 1 #FFFFFF);"));

        // теперь зная док, делаю функцию отрисовки правой части, передавая только doc
        // нажимая новую предыдущую нужно вернуть назад в цвете, для этого перед стартом все кнопки боди перекрашивать
        return true;}
        else if(obj->objectName()=="sortAZ"){


            if (SORTAZ){ // Клик на кнопку
                // Меняет на темную тему
                // Меняет триггер на 0


                QPixmap picAZ("://img_pos//sortZA.png");
                QSize pic_AZ(25, 25);
                picAZ = picAZ.scaled(pic_AZ,Qt::KeepAspectRatio);
                ui->sortAZ->setPixmap(picAZ);





                SORTAZ = 0;
            }
            else{
                // Меняет на светлую тему
                // Меняет триггер на 1
                QPixmap picAZ("://img_pos//sortAZ.png");
                QSize pic_AZ(25, 25);
                picAZ = picAZ.scaled(pic_AZ,Qt::KeepAspectRatio);

                    ui->sortAZ->setPixmap(picAZ);

                SORTAZ = 1;
            }
            return true;
            // Если клие на sortAZ
    //        QLabel *sortAZ = findChild<QLabel*>(obj->objectName());
    //        sortAZ->setPixmap();


        }
        else if(obj->objectName()=="sort12"){
            if (SORT12){ // Клик на кнопку
                // Меняет на темную тему
                // Меняет триггер на 0
                QPixmap pic12("://img_pos//sort21.png");
                QSize pic_12(25, 25);
                pic12 = pic12.scaled(pic_12,Qt::KeepAspectRatio);

                    ui->sort12->setPixmap(pic12);




                SORT12 = 0;
            }else{
                // Меняет на светлую тему
                // Меняет триггер на 1
                QPixmap pic12("://img_pos//sort12.png");
                QSize pic_12(25, 25);
                pic12 = pic12.scaled(pic_12,Qt::KeepAspectRatio);

                    ui->sort12->setPixmap(pic12);

                SORT12 = 1;
            }
            return true;
            // Если клие на sortAZ
    //        QLabel *sortAZ = findChild<QLabel*>(obj->objectName());
    //        sortAZ->setPixmap();

        }
        else if(obj->objectName()=="w_l"){
            if (SHOPW){ // Клик на кнопку
                // Меняет на темную тему
                // Меняет триггер на 0
                QPixmap picW("://img_pos//w_logo_dark.png");
                QSize pic_W(80, 100);
                picW = picW.scaled(pic_W,Qt::KeepAspectRatio);


                    ui->w_l->setPixmap(picW);


                SHOPW = 0;
            }else{
                // Меняет на светлую тему
                // Меняет триггер на 1
                QPixmap picW("://img_pos//w_logo_light.png");
                QSize pic_W(80, 100);
                picW = picW.scaled(pic_W,Qt::KeepAspectRatio);

                    ui->w_l->setPixmap(picW);

                SHOPW = 1;
            }
            return true;
            // Если клие на sortAZ
    //        QLabel *sortAZ = findChild<QLabel*>(obj->objectName());
    //        sortAZ->setPixmap();

        }
        else if(obj->objectName()=="m_l"){
            if (SHOPM){ // Клик на кнопку
                // Меняет на темную тему
                // Меняет триггер на 0


                QPixmap picM("://img_pos//ms_logo_dark.png");
                QSize pic_M(80, 100);
                picM = picM.scaled(pic_M,Qt::KeepAspectRatio);


                    ui->m_l->setPixmap(picM);

                SHOPM = 0;
            }else{
                // Меняет на светлую тему
                // Меняет триггер на 1
                QPixmap picM("://img_pos//ms_logo_light.png");
                QSize pic_M(80, 100);
                picM = picM.scaled(pic_M,Qt::KeepAspectRatio);

                    ui->m_l->setPixmap(picM);

                SHOPM = 1;
            }
            return true;
            // Если клие на sortAZ
    //        QLabel *sortAZ = findChild<QLabel*>(obj->objectName());
    //        sortAZ->setPixmap();

        }
        else if(obj->objectName()=="d_s") {
            if (SHOPD){ // Клик на кнопку
                // Меняет на темную тему
                // Меняет триггер на 0
                QPixmap picD("://img_pos//dns_logo_dark.png");
                QSize pic_D(80, 100);
                picD = picD.scaled(pic_D,Qt::KeepAspectRatio);


                    ui->d_s->setPixmap(picD);

                SHOPD = 0;
            }else{
                // Меняет на светлую тему
                // Меняет триггер на 1
                QPixmap picD("://img_pos//dns_logo_light.png");
                QSize pic_D(80, 100);
                picD = picD.scaled(pic_D,Qt::KeepAspectRatio);

                    ui->d_s->setPixmap(picD);

                SHOPD = 1;
            }
            return true;
        }
        else if(obj->objectName()=="tsortAZ_"){


            if (TSORTAZ){ // Клик на кнопку
                // Меняет на темную тему
                // Меняет триггер на 0


                QPixmap picAZ("://img_pos//sortZA.png");
                QSize pic_AZ(25, 25);
                picAZ = picAZ.scaled(pic_AZ,Qt::KeepAspectRatio);
                ui->tsortAZ_->setPixmap(picAZ);
                TSORTAZ = 0;
            }
            else{
                // Меняет на светлую тему
                // Меняет триггер на 1
                QPixmap picAZ("://img_pos//sortAZ.png");
                QSize pic_AZ(25, 25);
                picAZ = picAZ.scaled(pic_AZ,Qt::KeepAspectRatio);
                ui->tsortAZ_->setPixmap(picAZ);
                TSORTAZ = 1;
            }
            return true;


        }
        else if(obj->objectName()=="tsort12_"){
            if (TSORT12){ // Клик на кнопку
                // Меняет на темную тему
                // Меняет триггер на 0
                QPixmap pic12("://img_pos//sort21.png");
                QSize pic_12(25, 25);
                pic12 = pic12.scaled(pic_12,Qt::KeepAspectRatio);
                    ui->tsort12_->setPixmap(pic12);
                TSORT12 = 0;
            }else{
                // Меняет на светлую тему
                // Меняет триггер на 1
                QPixmap pic12("://img_pos//sort12.png");
                QSize pic_12(25, 25);
                pic12 = pic12.scaled(pic_12,Qt::KeepAspectRatio);
                    ui->tsort12_->setPixmap(pic12);

                TSORT12 = 1;
            }
            return true;
        }
        else if(obj->objectName()=="tw_l_"){
            if (TSHOPW){ // Клик на кнопку
                // Меняет на темную тему
                // Меняет триггер на 0
                QPixmap picW("://img_pos//w_logo_dark.png");
                QSize pic_W(80, 100);
                picW = picW.scaled(pic_W,Qt::KeepAspectRatio);

                    ui->tw_l_->setPixmap(picW);


                TSHOPW = 0;
            }else{
                // Меняет на светлую тему
                // Меняет триггер на 1
                QPixmap picW("://img_pos//w_logo_light.png");
                QSize pic_W(80, 100);
                picW = picW.scaled(pic_W,Qt::KeepAspectRatio);

                    ui->tw_l_->setPixmap(picW);

                TSHOPW = 1;
            }
            return true;
            // Если клие на sortAZ
    //        QLabel *sortAZ = findChild<QLabel*>(obj->objectName());
    //        sortAZ->setPixmap();

        }
        else if(obj->objectName()=="tm_l_"){
            if (TSHOPM){ // Клик на кнопку
                // Меняет на темную тему
                // Меняет триггер на 0


                QPixmap picM("://img_pos//ms_logo_dark.png");
                QSize pic_M(80, 100);
                picM = picM.scaled(pic_M,Qt::KeepAspectRatio);
                    ui->tm_l_->setPixmap(picM);

                TSHOPM = 0;
            }else{
                // Меняет на светлую тему
                // Меняет триггер на 1
                QPixmap picM("://img_pos//ms_logo_light.png");
                QSize pic_M(80, 100);
                picM = picM.scaled(pic_M,Qt::KeepAspectRatio);
                    ui->tm_l_->setPixmap(picM);

                TSHOPM = 1;
            }
            return true;
            // Если клие на sortAZ
    //        QLabel *sortAZ = findChild<QLabel*>(obj->objectName());
    //        sortAZ->setPixmap();

        }
        else if(obj->objectName()=="td_s_") {
            if (TSHOPD){ // Клик на кнопку
                // Меняет на темную тему
                // Меняет триггер на 0
                QPixmap picD("://img_pos//dns_logo_dark.png");
                QSize pic_D(80, 100);
                picD = picD.scaled(pic_D,Qt::KeepAspectRatio);
                    ui->td_s_->setPixmap(picD);
                TSHOPD = 0;
            }else{
                // Меняет на светлую тему
                // Меняет триггер на 1
                QPixmap picD("://img_pos//dns_logo_light.png");
                QSize pic_D(80, 100);
                picD = picD.scaled(pic_D,Qt::KeepAspectRatio);
                    ui->td_s_->setPixmap(picD);
                TSHOPD = 1;
            }
            return true;
        }
    }
    else {
         // standard event processing
//        qDebug() << "false";
         return QObject::eventFilter(obj, event);
     }
}








void workWindow::replyFinished_img(QObject* sender,QString isi,bool is,bool is_bl)// ,QObject img
{

//            qDebug() <<receivers("mda") << "получатель";
    QNetworkReply *reply= qobject_cast<QNetworkReply *>(sender);
//    qDebug() << reply << "reply";




    if (reply->error() == QNetworkReply::NoError)
    {
        QByteArray data = reply->readAll();
        QImage image = QImage::fromData(data);
        QLabel *labelX = findChild<QLabel *>(isi);

        labelX->setProperty("pixmap",QVariant(QPixmap::fromImage(image)));
        if(is_bl){
            labelX->setScaledContents(true);
            labelX->setFixedSize(160,40);
            labelX->setProperty("styleSheet",QVariant("vertical-align: middle;text-align:center;padding-left:10px;"));


        }else{
        if (is){

            labelX->setScaledContents(true);
            labelX->setFixedSize(200,200);
        }else{
            labelX->setScaledContents(true);
            labelX->setFixedSize(60,60);

        }}

//        qDebug() << QPixmap::fromImage(image);

//        qDebug() << labelX << isi;
    }
}
//connects_img.append(1);
void workWindow::clear_connects_img(){



    foreach(auto *connect,connects_img){
        connect->disconnect();
    }
    connects_img.clear();
//    connect.dis
}

void workWindow::clear_connects_btn(QWidget* body_=nullptr){
    if (!body_->objectName().contains("t_", Qt::CaseInsensitive)){
    foreach(auto *item,ui->scrollAreaWidgetContents_2->children()){


        QString name_item= item->objectName();
        if (name_item.contains("body_", Qt::CaseInsensitive) and name_item!=body_->objectName()){


            QWidget *widg = findChild<QWidget *>(item->objectName());
//                QPalette colr;
//                colr.setColor();
//                widg->setPalette();
            QVariant stly = widg->styleSheet() + "background-color: #F3F6FB;";
//                qDebug()<< widg->styleSheet() << "role"<<stly;
//                widg->setPalette();

                item->setProperty("styleSheet",stly);

                foreach(auto *itemIN,item->children()){
                    QString name_itemIN= itemIN->objectName();
                     if (name_itemIN.contains("add", Qt::CaseInsensitive)){
//                         qDebug() << "label = -"<<name_itemIN;
                itemIN->setProperty("styleSheet",QVariant("border:none;vertical-align: middle;border-radius:5px;padding-left:20px;background-color: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5,stop: 0 #F3F6FB, stop: 1 #FFFFFF);"));


    }}
        }}

//    qDebug() << "start clear" << connects_btn;

    foreach(auto *connect,connects_btn){
//        qDebug() << connect;
        connect->disconnect();
    }
    foreach(auto *connect,connects_btnOpen){
//        qDebug() << connect;
        connect->disconnect();
    }
    connects_btnOpen.clear();
    connects_btn.clear();
    foreach(auto *connect,connects_btnOpenT){
//        qDebug() << connect;
        connect->disconnect();
    }


    connects_chBox.clear();
    }else{
        foreach(auto *item,ui->scrollAreaWidgetContents_t->children()){


            QString name_item= item->objectName();
            if (name_item.contains("body_", Qt::CaseInsensitive) and name_item!=body_->objectName()){


                QWidget *widg = findChild<QWidget *>(item->objectName());
    //                QPalette colr;
    //                colr.setColor();
    //                widg->setPalette();
                QVariant stly = widg->styleSheet() + "background-color: #F3F6FB;";
    //                qDebug()<< widg->styleSheet() << "role"<<stly;
    //                widg->setPalette();

                    item->setProperty("styleSheet",stly);

                    foreach(auto *itemIN,item->children()){
                        QString name_itemIN= itemIN->objectName();
                         if (name_itemIN.contains("add", Qt::CaseInsensitive)){
//                             qDebug() << "label = -"<<name_itemIN;
                    itemIN->setProperty("styleSheet",QVariant("border:none;vertical-align: middle;border-radius:5px;padding-left:20px;background-color: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5,stop: 0 #F3F6FB, stop: 1 #FFFFFF);"));


        }}

                    foreach(auto *connect,connects_btnOpenT){
                //        qDebug() << connect;
                        connect->disconnect();
                    }
                    connects_btnOpenT.clear();
            }}

//        qDebug() << "start clear" << connects_btn;

        foreach(auto *connect,connects_btnTrckd){
//            qDebug() << connect;
            connect->disconnect();
        }
        connects_btnTrckd.clear();

        foreach(auto *connect,connects_chBox){
    //        qDebug() << connect;
            connect->disconnect();
        }

        connects_chBox.clear();
    }




//    connect.dis
}



void workWindow::on_next___clicked()
{
    PAGE_SEARCH++;
    ui->select_page_2->setValue(PAGE_SEARCH);
//    ui->text_down_4->setText(QString::number(PAGE_SEARCH));
//    text_down_4
    DrawSearch();


}

void workWindow::on_back___clicked()
{
    PAGE_SEARCH--;
    ui->next__->setEnabled(true);
    ui->select_page_2->setValue(PAGE_SEARCH);
//    ui->text_down_4->setText(QString::number(PAGE_SEARCH));
    DrawSearch();

}

void workWindow::on_t_back__clicked()
{
    PAGE_TRACKED--;
    ui->t_select_page_->setValue(PAGE_TRACKED);
//    ui->text_down_4->setText(QString::number(PAGE_SEARCH));
//    text_down_4
    DrawTracked();
}

void workWindow::on_t_next__clicked()
{
    PAGE_TRACKED++;
    ui->t_next_->setEnabled(true);
    ui->t_select_page_->setValue(PAGE_TRACKED);
//    ui->text_down_4->setText(QString::number(PAGE_SEARCH));
    DrawTracked();
}
