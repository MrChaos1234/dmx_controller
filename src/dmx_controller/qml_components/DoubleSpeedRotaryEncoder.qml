import QtQuick 2.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.2
import QtQuick.Window 2.15

Item {
    id: doubleSpeedRotaryEncoder
    property string purpose: "None"
    property var model: None
    property int position: model.position
    property int min: 0
    property int max: 255
    property string darker_color: "#1b1b1b"
    property bool isInDoubleSpeedMode: model.is_in_double_speed_mode

    width: 170
    height: 114

    Rectangle{
        id: background
        anchors.fill: parent
        color: "#2a2a2a"
        width: parent.width
        height: parent.height
        border.color: "black"
        border.width: 4
    }

    GridLayout {
        id: grid_layout
        columns: 3
        width: parent.width - 16
        height: parent.height - 16
        anchors.centerIn: parent 
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
                text: doubleSpeedRotaryEncoder.purpose
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
                text: doubleSpeedRotaryEncoder.position
                font.family: "TW Cen MT"
                font.pixelSize: 21
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

                MouseArea {
                    anchors.fill: parent
                        onClicked: {
                            model.toggle_is_in_double_speed_mode()
                        }
                    }     

                Rectangle {
                    id: isInDoubleSpeedModeDisplay
                    anchors.centerIn: parent
                    color: isInDoubleSpeedMode ? "white" : darker_color
                    width: 16
                    height: 16
                }
            }
        }
    }
}
