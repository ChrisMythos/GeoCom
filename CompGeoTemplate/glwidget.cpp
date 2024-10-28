//
// GUI-template for CG-assignments
//
// (c) Georg Umlauf, 2014
// (c) Georg Umlauf, 2020: Qt5
// (c) Georg Umlauf, 2022: Qt6
//
#include "glwidget.h"
#include <QtGui>
#include "glut.h"
#include "qapplication.h"


GLWidget::GLWidget(QWidget *parent) : QOpenGLWidget(parent)
{	
}

GLWidget::~GLWidget()
{
}

void GLWidget::paintGL()
{
    // clear
    glClear(GL_COLOR_BUFFER_BIT);

    // Koordinatensystem
    glColor3f(0.5,0.5,0.5);
    glBegin(GL_LINES);
    glVertex2f(-1.0, 0.0);
    glVertex2f( 1.0, 0.0);
    glVertex2f( 0.0,-1.0);
    glVertex2f( 0.0, 1.0);
    glEnd();

    // TODO: Compute and draw convex hull here
	// TODO: draw convex hull using glBegin(GL_LINE_STRIP); ... glEnd();
}


void GLWidget::initializeGL()
{
    resizeGL(width(),height());
}

void GLWidget::resizeGL(int width, int height)
{
    aspectx=1.0;
    aspecty=1.0;
    if (width>height) aspectx = float(width) /height;
    else              aspecty = float(height)/ width;
    glViewport    (0,0,width,height);
    glMatrixMode  (GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D    (-aspectx,aspectx,-aspecty,aspecty);
    glMatrixMode  (GL_MODELVIEW);
    glLoadIdentity();
}

QPointF GLWidget::transformPosition(QPoint p)
{
    return QPointF( (2.0*p.x()/ width() - 1.0)*aspectx,
		           -(2.0*p.y()/height() - 1.0)*aspecty);
}

void GLWidget::keyPressEvent(QKeyEvent * event)
{
    switch (event->key()) {
    case Qt::Key_Escape:   QApplication::instance()->quit(); break;
    case Qt::Key_Q     :   QApplication::instance()->quit(); break;
    default:               QWidget::keyPressEvent(event);    break;
	}
	update();
}

void GLWidget::mousePressEvent(QMouseEvent *event)
{
	QPointF posF = transformPosition(event->pos());
	if (event->buttons() & Qt::LeftButton ) {
        // TODO: add clicked point to point-list

        qDebug() << "Implement mousePressEvent for mouse-click-input of points at" <<posF;
	}
    update(); 
}


void GLWidget::radioButton1Clicked()
{
	// TODO: toggle to Jarvis' march
    update();
}

void GLWidget::radioButton2Clicked()
{
	// TODO: toggle to Graham's scan
    update();
}
