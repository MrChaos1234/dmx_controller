import QtQuick 2.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.2
import QtQuick.Window 2.15

Item {
    id: rotary_encoder
    property string purpose: "None"
    property int position: 0
    property int min: 0
    property int max: 255
    property string darker_color: "#1b1b1b"
    width: 230
    height: 121

    function visualize_pushbutton_pressed() {
        pushbutton_pressed_display.color = "red"
        visualize_pushbutton_pressed_timer.restart()
    }
    function visualize_pushbutton_released() {
        pushbutton_released_display.color = "brown"
        visualize_pushbutton_released_timer.restart()
    }

    Timer {
        id: visualize_pushbutton_pressed_timer
        interval: 500
        onTriggered: pushbutton_pressed_display.color = "white"
    }

    Timer {
        id: visualize_pushbutton_released_timer
        interval: 500
        onTriggered: pushbutton_released_display.color = "white"
    }

    
    GridLayout {
        id: grid_layout
        columns: 3
        width: parent.width
        height: parent.height
        Rectangle {
            Layout.row: 0
            Layout.columnSpan: 3
            Layout.column: 0
            Layout.fillWidth: true
            implicitHeight: 50
            color: darker_color

            Text {
                id: purpose
                anchors.centerIn: parent
                color: "white"
                text: rotary_encoder.purpose
                font.family: "TW Cen MT"
                font.pixelSize: 22
            }     
        }
        
        Rectangle {
            Layout.row: 1
            Layout.column: 0
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: darker_color

            Image {
                id: icon
                anchors.centerIn: parent
            }
        }

        Rectangle {
            Layout.row: 1
            Layout.column: 1
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: darker_color

            Text {
                id: encoder_value
                anchors.centerIn: parent
                color: "white"
                text: rotary_encoder.position
                font.family: "TW Cen MT"
                font.pixelSize: 25
            }
        }

        Rectangle {
            Layout.row: 1
            Layout.column: 2
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: darker_color

            Rectangle {
                id: pushbutton_pressed_display_outter
                anchors.centerIn: parent
                color: "black"
                width: 20
                height: 20

                Rectangle {
                    id: pushbutton_pressed_display
                    anchors.centerIn: parent
                    color: darker_color
                    width: 16
                    height: 16
                }
            }
        }
    }


    // // DEBUG
    // PropertyAnimation on position {
    //     from: min; to: max; duration: 1000; loops: Animation.Infinite
    // }

    // // DEBUG
    // Rectangle {
    //     anchors.fill: parent
    //     color: "red"
    //     opacity: 0.3
    // }
    // Rectangle {
    //     anchors.fill: parent
    //     border.color: "yellow"
    //     border.width: 1
    //     color: "transparent"
    // }
}
