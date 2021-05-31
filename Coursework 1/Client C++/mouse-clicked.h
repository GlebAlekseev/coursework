#ifndef MOUSECLICKED_H
#define MOUSECLICKED_H

#include <QLabel>
#include <QMouseEvent>
#include <QDebug>

class Label : public QLabel
{
    Q_OBJECT
public:
    explicit Label(QWidget *parent = nullptr);

signals:

public slots:

protected:
    virtual void mousePressEvent(QMouseEvent *event) Q_DECL_OVERRIDE;
};

#endif // MOUSECLICKED_H
