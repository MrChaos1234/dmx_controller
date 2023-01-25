import QtQuick 2.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.2
import QtQuick.Window 2.15



 // FILE DOESNT DO ANYTHING; IT SHOULD BE DELETED






Item {
    id: rotaryEncoder
    property string purpose: "None"
    property var model: None
    property int min: 0
    property int max: 255
    property string darker_color: "#1b1b1b"
    property string state: model.state
    property alias state: stateDisplay.text

    width: 230
    height: 121


    Connections {
        target: model
        function onPushbutton_pressed() {
            rotaryEncoder.visualize_pushbutton_pressed()
        }
        function onPushbutton_released() {
            rotaryEncoder.visualize_pushbutton_released()
        }
    }
    function visualize_pushbutton_pressed() {
        pushbuttonPressedDisplay.color = "red"
        visualizePushbuttonPressedTimer.restart()
    }
    function visualize_pushbutton_released() {
        pushbuttonPressedDisplay.color = "brown"
        visualizePushbuttonPressedTimer.restart()
    }

    Timer {
        id: visualizePushbuttonPressedTimer
        interval: 500
        onTriggered: pushbuttonPressedDisplay.color = "white"
    }

    Timer {
        id: visualizePushbuttonReleasedTimer
        interval: 500
        onTriggered: pushbuttonPressedDisplay.color = "white"
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
                id: encoderValue
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
                id: pushbuttonPressedDisplayOutter
                anchors.centerIn: parent
                color: "black"
                width: 20
                height: 20

                Rectangle {
                    id: pushbuttonPressedDisplay
                    anchors.centerIn: parent
                    color: darker_color
                    width: 16
                    height: 16
                }
            }
        }
    }

}
