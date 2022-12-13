import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.12
import QtQuick.Window 2.12
import QtQuick.Dialogs 1.1
import QtGraphicalEffects 1.0

ApplicationWindow {
    visible: true
    width: 3200
    height: 1800
    title: "Blender"

    LinearGradient {
        anchors.fill: parent
        start: Qt.point(0, 0)
        end: Qt.point(width, height)
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#4f0396" }
            GradientStop { position: 0.1; color: "#423461" }
            GradientStop { position: 0.2; color: "#232c3d" }
            GradientStop { position: 0.8; color: "#232c3d" }
            GradientStop { position: 0.9; color: "#345661" }
            GradientStop { position: 1.0; color: "#03a0a6" }
        }
    }
    
    RoundButton{
        id: start_button
        enabled: true
        visible: true
        anchors.centerIn: parent;
        Item{
            anchors.centerIn: parent;
            width: 700
            height: width
            Image{
                id: image
                anchors.centerIn: parent;
                source: "power.png"
                sourceSize: Qt.size(parent.width, parent.height)
                ColorOverlay{
                    id: overlay
                    anchors.fill: image
                    source: image
                    color: "red"
                }
            }
            
            
        }
        SequentialAnimation{
            id: animation
            running: false
            ScaleAnimator { target: image; from: 1; to: 0; duration: 750; easing.type: Easing.InQuart}
            PropertyAction { target: image; property: "source"; value: "tick.png" }
            PropertyAction { target: overlay; property: "color"; value: "green" }
            PropertyAction { target: rect; property: "border.color"; value: "green" }
            ScaleAnimator { target: image; from: 0; to: 1.5; duration: 750; easing.type: Easing.OutQuart}
            PropertyAction { target: start_button; property: "enabled"; value: false}
            PropertyAction { target: start_button; property: "visible"; value: false}
        }
        background: Rectangle {
            id: rect
            implicitWidth: start_button.hovered ? 920 : 900
            implicitHeight: start_button.hovered ? 920 : 900
            border.width: start_button.hovered ? 80 : 60
            border.color: "red"
            radius: start_button.hovered ? 455 : 450
            color: "transparent"
        }
        onClicked: {
            helper.OnStart()
            animation.running = true
        }
    }
    

}