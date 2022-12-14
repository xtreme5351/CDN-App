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
    id: window
    property int circle_diameter: 900
    property int circle_thickness: 60
    property int cluster_button_offset: 120

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
        anchors.centerIn: parent
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
            id: start_button_animation
            running: false
            PropertyAction { target: start_button; property: "enabled"; value: false}
            PropertyAction { target: rect; property: "border.color"; value: "red" }
            ScaleAnimator { target: image; from: 1; to: 0; duration: 750; easing.type: Easing.InQuart}
            PropertyAction { target: image; property: "source"; value: "tick.png" }
            PropertyAction { target: overlay; property: "color"; value: "green" }
            PropertyAction { target: rect; property: "border.color"; value: "green" }
            ScaleAnimator { target: image; from: 0; to: 1.5; duration: 750; easing.type: Easing.OutQuart}
            PropertyAction { target: ring; property: "visible"; value: true}
            PropertyAction { target: calibrate_button; property: "visible"; value: true}
            PropertyAction { target: parameters_button; property: "visible"; value: true}
            PropertyAction { target: divider; property: "visible"; value: true}
            ParallelAnimation{
                ScaleAnimator { target: image; from: 1.5; to: 0; duration: 750; easing.type: Easing.InQuart}

                PropertyAnimation { target: ring.border ; property: "color"; to: "#1b7bab"; duration: 1500 }

                NumberAnimation { target: calibrate_button; property: "opacity"; from: 0; to: 1; easing.type: Easing.InQuart; duration: 1500}
                NumberAnimation { target: calibrate_button; property: "y"; to: (circle_diameter/2)-cluster_button_offset*2; easing.type: Easing.OutQuad; duration: 1500}
                NumberAnimation { target: parameters_button; property: "opacity"; from: 0; to: 1; easing.type: Easing.InQuart; duration: 1500}
                NumberAnimation { target: parameters_button; property: "y"; to: circle_diameter/2; easing.type: Easing.OutQuad; duration: 1500}
                NumberAnimation { target: divider; property: "opacity"; from: 0; to: 1; easing.type: Easing.InQuart; duration: 1500}
            }
            PropertyAction { target: calibrate_button; property: "enabled"; value: true}
            PropertyAction { target: parameters_button; property: "enabled"; value: true}
            
            PropertyAction { target: start_button; property: "visible"; value: false}
            
        }
        background: Rectangle {
            id: rect
            implicitWidth: start_button.hovered ? circle_diameter + 20 : circle_diameter
            implicitHeight: start_button.hovered ? circle_diameter + 20 : circle_diameter
            border.width: start_button.hovered ? circle_thickness + 20 : circle_thickness
            border.color: "red"
            radius: start_button.hovered ? (circle_diameter + 10)/2 : circle_diameter/2
            color: "transparent"
        }
        onClicked: {
            helper.OnStart()
            start_button_animation.running = true
        }
    }

    

    Item{
        id: cluster
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.horizontalCenterOffset: 0
        width: circle_diameter
        height: width
        Button{
            id: calibrate_button
            property bool begin_calibration: false
            enabled: false
            visible: false
            opacity: 0
            y: -cluster_button_offset
            Text{
                anchors.centerIn: parent
                text: "Calibrate"
                color: "white"
                font.pointSize: calibrate_button.hovered ? 24 : 20
            }
            background: Rectangle{
                color: "transparent"
                border.width: 0
                implicitWidth: circle_diameter
                implicitHeight: cluster_button_offset*2
            }
            onClicked: {
                if (begin_calibration){
                    helper.OnCalibrate()
                    begin_calibration_animation.running = true
                }
                else{
                    calibrate_button_animation.running = true
                }
                
            }   
        }

        Button{
            id: parameters_button
            enabled: false
            visible: false
            opacity: 0
            y: circle_diameter+cluster_button_offset
            Text{
                anchors.centerIn: parent
                text: "Parameters"
                color: "white"
                font.pointSize: parameters_button.hovered ? 24 : 20
            }
            background: Rectangle{
                color: "transparent"
                border.width: 0
                implicitWidth: circle_diameter
                implicitHeight: cluster_button_offset*2
            }
            onClicked: {
                parameters_button_animation.running = true
            }
        }
        
        Rectangle{
            id: ring
            visible: false
            anchors.centerIn: parent
            implicitWidth: circle_diameter
            implicitHeight: circle_diameter
            border.width: circle_thickness
            border.color: "green"
            radius: circle_diameter/2
            color: "transparent"
        }

        Rectangle{
            id: divider
            visible: false
            anchors.centerIn: parent
            implicitWidth: circle_diameter - (circle_thickness * 2) - 60
            implicitHeight: 5
            border.width: 0
            color: "white"
        }

        Text{
            id: counter
            visible: false
            opacity: 0
            anchors.centerIn: parent
            text: "3"
            color: "white"
            font.pointSize: 72
        }

        Image{
            id: loading_icon
            visible: false
            opacity: 0
            anchors.centerIn: parent;
            source: "loading.png"
            sourceSize: Qt.size(parent.width, parent.height)
            rotation: 0
            RotationAnimation on rotation{
                target: loading_icon
                loops: Animation.Infinite
                from:0
                to: 360
                duration: 2000
            }
        }

        SequentialAnimation{
            id: parameters_button_animation
            running: false
            PropertyAction { target: calibrate_button; property: "enabled"; value: false}
            PropertyAction { target: parameters_button; property: "enabled"; value: false}
            PropertyAction { target: parameters_page; property: "visible"; value: true}
            ParallelAnimation{
                ScaleAnimator { target: ring; from: 1; to: 3.5; duration: 1000; easing.type: Easing.InOutQuart}
                PropertyAnimation { target: parameters_button; property: "opacity"; to: 0; easing.type: Easing.OutQuart; duration: 1000}
                PropertyAnimation { target: calibrate_button; property: "opacity"; to: 0; easing.type: Easing.OutQuart; duration: 1000}
                PropertyAnimation { target: divider; property: "opacity"; to: 0; easing.type: Easing.OutQuart; duration: 1000}
                PropertyAnimation { target: parameters_page; property: "opacity"; to: 1; easing.type: Easing.InQuart; duration: 1000}
                NumberAnimation { target: ring; property: "border.width"; to: circle_thickness/3.5; easing.type: Easing.InOutQuart; duration: 1000}
            }
            PropertyAction { target: calibrate_button; property: "visible"; value: false}
            PropertyAction { target: parameters_button; property: "visible"; value: false}
            PropertyAction { target: parameters_page; property: "enabled"; value: true}
            PropertyAction { target: calibrate_button; property: "begin_calibration"; value: false}
        }

        SequentialAnimation{
            id: calibrate_button_animation
            running: false
            PropertyAction { target: calibrate_button; property: "enabled"; value: false}
            PropertyAction { target: parameters_button; property: "enabled"; value: false}
            PropertyAction { target: pix_image; property: "visible"; value: true}
            ParallelAnimation{
                NumberAnimation{ target: cluster.anchors; property: "horizontalCenterOffset"; to: -window.width/2 + circle_diameter/2 + circle_thickness; duration: 1000; easing.type: Easing.InOutQuart}
                PropertyAnimation { target: parameters_button; property: "opacity"; to: 0; easing.type: Easing.OutQuart; duration: 1000}
                PropertyAnimation { target: divider; property: "opacity"; to: 0; easing.type: Easing.OutQuart; duration: 1000}
                NumberAnimation { target: calibrate_button; property: "y"; to: (circle_diameter/2)-cluster_button_offset; easing.type: Easing.InOutQuart; duration: 1000}
                PropertyAnimation { target: pix_image; property: "opacity"; from: 0; to: 1; easing.type: Easing.InQuart; duration: 1000}
                ScaleAnimator { target: pix_image; from: 0.5; to: 1; duration: 1000; easing.type: Easing.OutQuart}
            }
            PropertyAction { target: calibrate_button; property: "enabled"; value: true}
            PropertyAction { target: parameters_button; property: "visible"; value: false}
            PropertyAction { target: divider; property: "visible"; value: false}
            PropertyAction { target: calibrate_button; property: "begin_calibration"; value: true}

        }

        SequentialAnimation{
            id: begin_calibration_animation
            running: false
            PropertyAction { target: calibrate_button; property: "enabled"; value: false}
            PropertyAnimation { target: calibrate_button; property: "opacity"; to: 0; easing.type: Easing.OutQuart; duration: 1000}
            PropertyAction { target: calibrate_button; property: "visible"; value: false}
            PropertyAction { target: counter; property: "visible"; value: true}
            PropertyAnimation { target: counter; property: "opacity"; from: 0; to: 1; easing.type: Easing.InQuart; duration: 500}
            PropertyAnimation { target: counter; property: "opacity"; from: 1; to: 0; easing.type: Easing.OutQuart; duration: 500}
            PropertyAction { target: counter; property: "text"; value: "2"}
            PropertyAnimation { target: counter; property: "opacity"; from: 0; to: 1; easing.type: Easing.InQuart; duration: 500}
            PropertyAnimation { target: counter; property: "opacity"; from: 1; to: 0; easing.type: Easing.OutQuart; duration: 500}
            PropertyAction { target: counter; property: "text"; value: "1"}
            PropertyAnimation { target: counter; property: "opacity"; from: 0; to: 1; easing.type: Easing.InQuart; duration: 500}
            PropertyAnimation { target: counter; property: "opacity"; from: 1; to: 0; easing.type: Easing.OutQuart; duration: 500}
            ScaleAnimator { target: loading_icon; to: 0; duration: 0; easing.type: Easing.OutQuart}
            PropertyAction { target: loading_icon; property: "visible"; value: true}
            ParallelAnimation{
                ScaleAnimator { target: loading_icon; from: 0; to: 0.5; duration: 1000; easing.type: Easing.OutQuart}
                PropertyAnimation { target: loading_icon; property: "opacity"; from: 0; to: 1; easing.type: Easing.OutQuart; duration: 500}
            }
        }
    }

    Rectangle{
        id: pix_image
        visible: false
        opacity: 0
        width: window.width-circle_diameter-circle_thickness*3
        height: width*9/16
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenterOffset: window.width/2 - width/2 - circle_thickness
        radius: 40
    }


    Item{
        id: parameters_page
        anchors.centerIn: parent
        enabled: false
        visible: false
        opacity: 0

        property int text_size: 16
        property string text_colour: "white"
        property int column_spacing: 60
        property int row_spacing: 30
        property int int_input_width: 120
        property int str_input_width: 500
        property int input_text_size: 14
        property int input_height: 70
        property int input_border_thickness: 5
        property int input_radius: 10
        property string input_border_colour: "white"
        property string input_colour: "transparent"
        property string placeholder_text_colour: "#858585"
        
        Column{
            spacing: 150
            anchors.centerIn: parent
            Row{
                spacing: parameters_page.row_spacing
                Column{
                    spacing: parameters_page.column_spacing
                    Text{
                        text: "Integer input:"
                        anchors.right: parent.right
                        color: parameters_page.text_colour
                        font.pointSize: parameters_page.text_size
                    }
                    Text{
                        text: "Double input:"
                        anchors.right: parent.right
                        color: parameters_page.text_colour
                        font.pointSize: parameters_page.text_size
                    }
                    Text{
                        text: "String input:"
                        anchors.right: parent.right
                        color: parameters_page.text_colour
                        font.pointSize: parameters_page.text_size
                    }
                }
                Column{
                    spacing: parameters_page.column_spacing
                    TextField{
                        placeholderText: qsTr("Int")
                        validator: IntValidator{bottom:0; top:999}
                        placeholderTextColor: parameters_page.placeholder_text_colour
                        color: parameters_page.text_colour
                        font.pointSize: parameters_page.input_text_size
                        horizontalAlignment: TextInput.AlignHCenter
                        background: Rectangle{
                            color: parameters_page.input_colour
                            border.width: parameters_page.input_border_thickness
                            border.color: parameters_page.input_border_colour
                            radius: parameters_page.input_radius
                            implicitWidth: parameters_page.int_input_width
                            implicitHeight: parameters_page.input_height
                        }
                    }
                    TextField{
                        placeholderText: qsTr("Double")
                        validator: DoubleValidator{bottom:0; top:999}
                        placeholderTextColor: parameters_page.placeholder_text_colour
                        color: parameters_page.text_colour
                        font.pointSize: parameters_page.input_text_size
                        horizontalAlignment: TextInput.AlignHCenter
                        background: Rectangle{
                            color: parameters_page.input_colour
                            border.width: parameters_page.input_border_thickness
                            border.color: parameters_page.input_border_colour
                            radius: parameters_page.input_radius
                            implicitWidth: parameters_page.int_input_width
                            implicitHeight: parameters_page.input_height
                        }
                    }
                    TextField{
                        placeholderText: qsTr("String")
                        placeholderTextColor: parameters_page.placeholder_text_colour
                        color: parameters_page.text_colour
                        font.pointSize: parameters_page.input_text_size
                        horizontalAlignment: TextInput.AlignHCenter
                        background: Rectangle{
                            color: parameters_page.input_colour
                            border.width: parameters_page.input_border_thickness
                            border.color: parameters_page.input_border_colour
                            radius: parameters_page.input_radius
                            implicitWidth: parameters_page.str_input_width
                            implicitHeight: parameters_page.input_height
                        }
                    }   
                }
            }   
            Button{
                anchors.horizontalCenter: parent.horizontalCenter
                id: parameters_page_return_button
                Text{
                    anchors.centerIn: parent
                    text: "Return"
                    color: "white"
                    font.pointSize:  14
                }
                background: Rectangle{
                    color: "transparent"
                    border.width: parameters_page_return_button.hovered ? parameters_page.input_border_thickness * 2 : parameters_page.input_border_thickness
                    border.color: parameters_page.input_border_colour
                    implicitWidth: parameters_page_return_button.hovered ? parameters_page.input_border_thickness + 200 : 200
                    implicitHeight: parameters_page.input_height
                    radius: parameters_page.input_radius
                }
                onClicked: {
                    helper.OnParameters()
                    parameters_page_return_button_animation.running = true
                }
            }
        }
        SequentialAnimation{
            id: parameters_page_return_button_animation
            running: false
            PropertyAction { target: calibrate_button; property: "visible"; value: true}
            PropertyAction { target: parameters_button; property: "visible"; value: true}
            PropertyAction { target: parameters_page; property: "enabled"; value: false}
            ParallelAnimation{
                ScaleAnimator { target: ring; from: 3.5; to: 1; duration: 1000; easing.type: Easing.InOutQuart}
                PropertyAnimation { target: parameters_button; property: "opacity"; to: 1; easing.type: Easing.InQuart; duration: 1000}
                PropertyAnimation { target: calibrate_button; property: "opacity"; to: 1; easing.type: Easing.InQuart; duration: 1000}
                PropertyAnimation { target: divider; property: "opacity"; to: 1; easing.type: Easing.InQuart; duration: 1000}
                PropertyAnimation { target: parameters_page; property: "opacity"; to: 0; easing.type: Easing.OutQuart; duration: 1000}
                NumberAnimation { target: ring; property: "border.width"; to: circle_thickness; easing.type: Easing.InOutQuart; duration: 1000}
            }
            PropertyAction { target: calibrate_button; property: "enabled"; value: true}
            PropertyAction { target: parameters_button; property: "enabled"; value: true}
            PropertyAction { target: parameters_page; property: "visible"; value: false}
        }   
    }
}